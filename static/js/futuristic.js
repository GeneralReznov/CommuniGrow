// Futuristic Landing Page JavaScript

class FuturisticEffects {
    constructor() {
        this.init();
    }

    init() {
        this.initParticles();
        this.initScrollEffects();
        this.initAnimations();
        this.initScrollProgress();
        this.initAOS();
    }

    initParticles() {
        if (document.getElementById('particles-js')) {
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 120,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": "#ffffff"
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        }
                    },
                    "opacity": {
                        "value": 0.5,
                        "random": false,
                        "anim": {
                            "enable": false,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": {
                            "enable": false,
                            "speed": 40,
                            "size_min": 0.1,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#ffffff",
                        "opacity": 0.4,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": "none",
                        "random": false,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false,
                        "attract": {
                            "enable": false,
                            "rotateX": 600,
                            "rotateY": 1200
                        }
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "repulse"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        },
                        "resize": true
                    },
                    "modes": {
                        "grab": {
                            "distance": 400,
                            "line_linked": {
                                "opacity": 1
                            }
                        },
                        "bubble": {
                            "distance": 400,
                            "size": 40,
                            "duration": 2,
                            "opacity": 8,
                            "speed": 3
                        },
                        "repulse": {
                            "distance": 200,
                            "duration": 0.4
                        },
                        "push": {
                            "particles_nb": 4
                        },
                        "remove": {
                            "particles_nb": 2
                        }
                    }
                },
                "retina_detect": true
            });
        }
    }

    initScrollEffects() {
        window.addEventListener('scroll', () => {
            this.updateScrollProgress();
            this.handleParallaxEffects();
        });
    }

    updateScrollProgress() {
        const scrollProgress = document.querySelector('.scroll-progress');
        if (scrollProgress) {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            scrollProgress.style.width = scrollPercent + '%';
        }
    }

    handleParallaxEffects() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }

    initAnimations() {
        // Animate counters
        this.animateCounters();
        
        // Add hover effects to feature cards
        this.initCardHoverEffects();
        
        // Initialize typing animation
        this.initTypingAnimation();
    }

    animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-count]');
        
        const animateCounter = (counter) => {
            const target = parseInt(counter.dataset.count);
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            const updateCounter = () => {
                current += increment;
                if (current >= target) {
                    counter.textContent = target + (counter.dataset.suffix || '');
                } else {
                    counter.textContent = Math.floor(current) + (counter.dataset.suffix || '');
                    requestAnimationFrame(updateCounter);
                }
            };
            
            updateCounter();
        };

        // Intersection Observer for counters
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                    entry.target.classList.add('animated');
                    animateCounter(entry.target);
                }
            });
        });

        counters.forEach(counter => counterObserver.observe(counter));
    }

    initCardHoverEffects() {
        const cards = document.querySelectorAll('.feature-card-futuristic, .timeline-item');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.createRippleEffect(e);
            });
        });
    }

    createRippleEffect(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('div');
        ripple.style.position = 'absolute';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = '1px';
        ripple.style.height = '1px';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'radial-gradient(circle, rgba(0, 212, 255, 0.6) 0%, transparent 70%)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.pointerEvents = 'none';
        ripple.style.zIndex = '1';
        
        card.style.position = 'relative';
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    initTypingAnimation() {
        const typingElement = document.querySelector('.typing-text');
        if (!typingElement) return;
        
        const messages = [
            "Building Resilient Communities",
            "Empowering Sustainable Development",
            "Connecting People & Resources",
            "Creating Lasting Impact"
        ];
        
        let messageIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        const typeWriter = () => {
            const currentMessage = messages[messageIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentMessage.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentMessage.substring(0, charIndex + 1);
                charIndex++;
            }
            
            let typeSpeed = isDeleting ? 50 : 100;
            
            if (!isDeleting && charIndex === currentMessage.length) {
                typeSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                messageIndex = (messageIndex + 1) % messages.length;
                typeSpeed = 500;
            }
            
            setTimeout(typeWriter, typeSpeed);
        };
        
        typeWriter();
    }

    initScrollProgress() {
        // Create scroll progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
    }

    initAOS() {
        // Initialize AOS (Animate On Scroll)
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 1000,
                once: true,
                offset: 100,
                easing: 'ease-out-cubic'
            });
        }
    }

    // Smooth scrolling for anchor links
    initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// CSS for ripple animation
const futuristicStyle = document.createElement('style');
futuristicStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(50);
            opacity: 0;
        }
    }
    
    .typing-text::after {
        content: '|';
        display: inline-block;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
`;
document.head.appendChild(futuristicStyle);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FuturisticEffects();
});

// Export for global access
window.FuturisticEffects = FuturisticEffects;