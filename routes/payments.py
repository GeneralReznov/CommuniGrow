from flask import Blueprint, render_template, request, redirect, jsonify
import stripe
import os
import logging

payments_bp = Blueprint('payments', __name__)

# Configure Stripe
os.environ['STRIPE_SECRET_KEY']="sk_test_51Rjy7j1XN8PJc0L4c7zuZyiHsgD1HLdHvH8VBOsR9KQnFMccsFMqpQK87JoKLZGOX4P6t8zI8elxHkb7OeIzuE4B00NhmJ8fvt"
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_default')

# Get domain for redirect URLs
YOUR_DOMAIN = os.environ.get('REPLIT_DEV_DOMAIN') if os.environ.get('REPLIT_DEPLOYMENT') != '' else (
    os.environ.get('REPLIT_DOMAINS').split(',')[0] if os.environ.get('REPLIT_DOMAINS') else 'localhost:5000'
)

@payments_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session for marketplace purchases"""
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Get payment details
        amount = int(float(data.get('amount', 0)) * 100)  # Convert to cents
        item_name = data.get('item_name', 'Community Marketplace Item')
        item_description = data.get('item_description', '')
        return_url = data.get('return_url', '/food/marketplace')
        
        if amount <= 0:
            if request.is_json:
                return jsonify({'error': 'Invalid amount'}), 400
            else:
                return redirect(return_url + '?error=invalid_amount')
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item_name,
                            'description': item_description,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'https://{YOUR_DOMAIN}/payments/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'https://{YOUR_DOMAIN}/payments/cancel',
            metadata={
                'return_url': return_url
            }
        )
        
        if request.is_json:
            return jsonify({'checkout_url': checkout_session.url})
        else:
            return redirect(checkout_session.url, code=303)
            
    except Exception as e:
        logging.error(f"Payment session error: {e}")
        if request.is_json:
            return jsonify({'error': 'Payment processing failed'}), 500
        else:
            return redirect('/food/marketplace?error=payment_failed')

@payments_bp.route('/success')
def payment_success():
    """Payment success page"""
    session_id = request.args.get('session_id')
    
    try:
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            return_url = session.metadata.get('return_url', '/dashboard')
            
            return render_template('payments/success.html', 
                                 session=session, 
                                 return_url=return_url)
        else:
            return render_template('payments/success.html', 
                                 return_url='/dashboard')
    except Exception as e:
        logging.error(f"Payment success page error: {e}")
        return render_template('payments/success.html', 
                             return_url='/dashboard',
                             error='Unable to retrieve payment details')

@payments_bp.route('/cancel')
def payment_cancel():
    """Payment cancellation page"""
    return render_template('payments/cancel.html')

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        logging.error("Invalid payload in webhook")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        logging.error("Invalid signature in webhook")
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle successful payment
        logging.info(f"Payment completed for session: {session['id']}")
        
        # Here you could update your database, send confirmation emails, etc.
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logging.error(f"Payment failed: {payment_intent['id']}")
        
    else:
        logging.info(f"Unhandled event type: {event['type']}")
    
    return jsonify({'status': 'success'})
