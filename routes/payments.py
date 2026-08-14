from flask import Blueprint, render_template, request, redirect, jsonify, url_for
import stripe
import os
import logging
from models import FoodListing

payments_bp = Blueprint('payments', __name__)

# Configure Stripe only when a secure key is available. The marketplace
# remains browseable without checkout configuration.
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


def _stripe_mode():
    """Return a safe, user-facing mode label without exposing the key."""
    key = os.environ.get('STRIPE_SECRET_KEY', '')
    if key.startswith('sk_test_'):
        return 'test'
    if key.startswith('sk_live_'):
        return 'live'
    return None


def _absolute_url(endpoint, **values):
    """Build redirects from the current proxied request host."""
    return url_for(endpoint, _external=True, **values)


@payments_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session for marketplace purchases"""
    try:
        if not stripe.api_key:
            error = 'Stripe test checkout is not configured yet. Add STRIPE_SECRET_KEY in Replit Secrets to enable it.'
            if request.is_json:
                return jsonify({'error': error, 'code': 'stripe_not_configured'}), 503
            return redirect('/food/marketplace?error=stripe_not_configured')

        data = request.get_json() if request.is_json else request.form

        # Always resolve the product and price on the server. Never trust an
        # amount or title supplied by the browser for a marketplace purchase.
        item_id = data.get('item_id')
        try:
            item_id = int(item_id)
        except (TypeError, ValueError):
            item_id = None

        listing = FoodListing.query.filter_by(
            id=item_id, category='marketplace', is_available=True
        ).first() if item_id else None

        if not listing or listing.price is None or listing.price <= 0:
            if request.is_json:
                return jsonify({
                    'error': 'This marketplace item is unavailable or has no valid price.',
                    'code': 'invalid_listing'
                }), 400
            else:
                return redirect('/food/marketplace?error=invalid_listing')

        amount = int(round(float(listing.price) * 100))
        return_url = data.get('return_url', '/food/marketplace')

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': listing.title,
                            'description': listing.description[:500],
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=_absolute_url(
                'payments.payment_success',
                session_id='{CHECKOUT_SESSION_ID}'
            ),
            cancel_url=_absolute_url('payments.payment_cancel'),
            client_reference_id=f'food_listing:{listing.id}',
            metadata={
                'return_url': return_url,
                'food_listing_id': str(listing.id),
                'item_name': listing.title,
            }
        )

        if request.is_json:
            return jsonify({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id,
                'mode': _stripe_mode() or 'configured'
            })
        else:
            return redirect(checkout_session.url, code=303)

    except stripe.error.InvalidRequestError as e:
        logging.warning("Stripe rejected checkout request: %s", e)
        error = 'Stripe could not create this checkout session. Check the test key and try again.'
        if request.is_json:
            return jsonify({'error': error, 'code': 'stripe_request_error'}), 400
        return redirect('/food/marketplace?error=payment_failed')
    except Exception as e:
        logging.exception("Payment session error")
        if request.is_json:
            return jsonify({
                'error': 'Payment processing failed. Please try again.',
                'code': 'payment_failed'
            }), 500
        else:
            return redirect('/food/marketplace?error=payment_failed')


@payments_bp.route('/status')
def payment_status():
    """Expose configuration state, never credentials."""
    return jsonify({
        'configured': bool(stripe.api_key),
        'mode': _stripe_mode(),
        'checkout_available': bool(stripe.api_key),
        'webhooks_configured': bool(stripe.api_key and os.environ.get('STRIPE_WEBHOOK_SECRET'))
    })


@payments_bp.route('/success')
def payment_success():
    """Payment success page"""
    session_id = request.args.get('session_id')

    try:
        if not stripe.api_key:
            return render_template('payments/success.html',
                                   return_url='/food/marketplace',
                                   error='Stripe checkout is not configured yet.')
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            return_url = session.metadata.get('return_url', '/dashboard')

            return render_template('payments/success.html', 
                                 session=session, 
                                  return_url=return_url,
                                  mode=_stripe_mode())
        else:
            return render_template('payments/success.html', 
                                 return_url='/dashboard')
    except Exception as e:
        logging.exception("Payment success page error")
        return render_template('payments/success.html', 
                             return_url='/dashboard',
                              error='Unable to retrieve payment details from Stripe.')

@payments_bp.route('/cancel')
def payment_cancel():
    """Payment cancellation page"""
    return render_template('payments/cancel.html', return_url='/food/marketplace')

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    if not stripe.api_key or not endpoint_secret:
        return jsonify({
            'error': 'Stripe webhooks are not configured',
            'code': 'webhook_not_configured'
        }), 503
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        logging.warning("Invalid Stripe webhook payload")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        logging.warning("Invalid Stripe webhook signature")
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logging.info("Payment completed for Stripe checkout session %s", session['id'])
        # The verified event is the source of truth for fulfillment. The
        # marketplace currently has no fulfillment workflow, so we only log
        # the event and leave the listing available for future orders.
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logging.warning("Payment failed for intent %s", payment_intent['id'])
    else:
        logging.info("Unhandled Stripe event type: %s", event['type'])

    return jsonify({'status': 'success'})
