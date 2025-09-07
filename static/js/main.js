// Main JavaScript functionality for Community Empowerment Platform
class CommunityPlatform {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.handleRouting();
        this.setupAccessibility();
    }
    
    setupEventListeners() {
        // Handle dynamic content loading
        document.addEventListener('click', this.handleClicks.bind(this));
        
        // Handle form submissions
        document.addEventListener('submit', this.handleFormSubmissions.bind(this));
        
        // Handle keyboard navigation
        document.addEventListener('keydown', this.handleKeyboardNavigation.bind(this));
        
        // Handle window resize for responsive adjustments
        window.addEventListener('resize', this.handleResize.bind(this));
        
        // Handle scroll events for animations
        window.addEventListener('scroll', this.handleScroll.bind(this));
    }
    
    handleClicks(event) {
        const target = event.target;
        
        // Handle card animations
        if (target.closest('.module-card, .quick-action-card, .stat-card')) {
            this.animateCard(target.closest('.module-card, .quick-action-card, .stat-card'));
        }
        
        // Handle external links
        if (target.tagName === 'A' && target.hostname !== window.location.hostname) {
            event.preventDefault();
            this.handleExternalLink(target.href);
        }
        
        // Handle modal triggers
        if (target.getAttribute('data-bs-toggle') === 'modal') {
            this.prepareModal(target.getAttribute('data-bs-target'));
        }
    }
    
    handleFormSubmissions(event) {
        const form = event.target;
        
        // Add loading states to forms
        if (form.tagName === 'FORM') {
            this.addLoadingState(form);
        }
    }
    
    handleKeyboardNavigation(event) {
        // Enhanced keyboard navigation
        switch (event.key) {
            case 'Tab':
                this.handleTabNavigation(event);
                break;
            case 'Enter':
                if (event.target.classList.contains('card-clickable')) {
                    event.target.click();
                }
                break;
            case '/':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.focusSearch();
                }
                break;
        }
    }
    
    handleResize() {
        // Adjust components based on screen size
        this.adjustForScreenSize();
        this.repositionModals();
    }
    
    handleScroll() {
        // Implement scroll-based animations
        this.handleScrollAnimations();
        this.updateNavigationState();
    }
    
    initializeComponents() {
        this.initializeTooltips();
        this.initializePopovers();
        this.initializeCarousels();
        this.initializeCharts();
        this.initializeAnimations();
    }
    
    initializeTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    initializePopovers() {
        // Initialize Bootstrap popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
    
    initializeCarousels() {
        // Initialize any carousels on the page
        const carousels = document.querySelectorAll('.carousel');
        carousels.forEach(carousel => {
            new bootstrap.Carousel(carousel);
        });
    }
    
    initializeCharts() {
        // Initialize Chart.js charts if present
        const chartElements = document.querySelectorAll('[data-chart]');
        chartElements.forEach(element => {
            this.createChart(element);
        });
    }
    
    createChart(element) {
        const chartType = element.getAttribute('data-chart');
        const ctx = element.getContext('2d');
        
        // Sample chart configurations
        const configs = {
            'health-stats': this.getHealthStatsConfig(),
            'climate-data': this.getClimateDataConfig(),
            'skills-progress': this.getSkillsProgressConfig(),
            'food-security': this.getFoodSecurityConfig()
        };
        
        if (configs[chartType] && typeof Chart !== 'undefined') {
            new Chart(ctx, configs[chartType]);
        }
    }
    
    getHealthStatsConfig() {
        return {
            type: 'doughnut',
            data: {
                labels: ['Services Accessed', 'Assessments Completed', 'Resources Used'],
                datasets: [{
                    data: [65, 45, 80],
                    backgroundColor: ['#dc3545', '#28a745', '#007bff']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
    }
    
    getClimateDataConfig() {
        return {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Temperature',
                    data: [10, 15, 20, 25, 30, 35],
                    borderColor: '#28a745',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
    }
    
    getSkillsProgressConfig() {
        return {
            type: 'bar',
            data: {
                labels: ['Digital Literacy', 'Entrepreneurship', 'Technical Skills', 'Life Skills'],
                datasets: [{
                    label: 'Progress %',
                    data: [75, 60, 45, 85],
                    backgroundColor: '#007bff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        };
    }
    
    getFoodSecurityConfig() {
        return {
            type: 'radar',
            data: {
                labels: ['Availability', 'Access', 'Utilization', 'Stability'],
                datasets: [{
                    label: 'Food Security Score',
                    data: [80, 65, 70, 85],
                    backgroundColor: 'rgba(255, 193, 7, 0.2)',
                    borderColor: '#ffc107'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        };
    }
    
    initializeAnimations() {
        // Set up intersection observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate
        const animatedElements = document.querySelectorAll('.module-card, .quick-action-card, .stat-card, .feature-card');
        animatedElements.forEach(el => {
            this.observer.observe(el);
        });
    }
    
    handleRouting() {
        // Handle client-side routing for SPA-like behavior
        const currentPath = window.location.pathname;
        this.updateActiveNavigation(currentPath);
    }
    
    updateActiveNavigation(currentPath) {
        // Update active navigation states
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath || 
                (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
                link.classList.add('active');
            }
        });
    }
    
    setupAccessibility() {
        // Enhanced accessibility features
        this.setupSkipLinks();
        this.setupFocusManagement();
        this.setupAriaLabels();
        this.setupKeyboardTraps();
    }
    
    setupSkipLinks() {
        // Add skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link visually-hidden-focusable';
        skipLink.textContent = 'Skip to main content';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            background: #000;
            color: white;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
            z-index: 10000;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);
    }
    
    setupFocusManagement() {
        // Manage focus for modal dialogs
        document.addEventListener('shown.bs.modal', (event) => {
            const modal = event.target;
            const focusableElements = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            if (focusableElements.length > 0) {
                focusableElements[0].focus();
            }
        });
    }
    
    setupAriaLabels() {
        // Automatically add ARIA labels where missing
        const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                const icon = button.querySelector('i[class*="fa-"]');
                if (icon) {
                    const iconClass = Array.from(icon.classList).find(cls => cls.startsWith('fa-'));
                    const label = iconClass ? iconClass.replace('fa-', '').replace('-', ' ') : 'button';
                    button.setAttribute('aria-label', label);
                }
            }
        });
    }
    
    setupKeyboardTraps() {
        // Trap focus within modals
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Tab') {
                const activeModal = document.querySelector('.modal.show');
                if (activeModal) {
                    this.trapFocusInModal(event, activeModal);
                }
            }
        });
    }
    
    trapFocusInModal(event, modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (event.shiftKey) {
            if (document.activeElement === firstElement) {
                lastElement.focus();
                event.preventDefault();
            }
        } else {
            if (document.activeElement === lastElement) {
                firstElement.focus();
                event.preventDefault();
            }
        }
    }
    
    // Utility methods
    animateCard(card) {
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
        }, 150);
    }
    
    handleExternalLink(url) {
        if (confirm('This link will open in a new window. Continue?')) {
            window.open(url, '_blank', 'noopener,noreferrer');
        }
    }
    
    prepareModal(targetSelector) {
        const modal = document.querySelector(targetSelector);
        if (modal) {
            // Prepare modal content if needed
            this.loadModalContent(modal);
        }
    }
    
    loadModalContent(modal) {
        // Load dynamic content for modals
        const contentUrl = modal.getAttribute('data-content-url');
        if (contentUrl) {
            fetch(contentUrl)
                .then(response => response.text())
                .then(html => {
                    const modalBody = modal.querySelector('.modal-body');
                    if (modalBody) {
                        modalBody.innerHTML = html;
                    }
                })
                .catch(error => {
                    console.error('Error loading modal content:', error);
                });
        }
    }
    
    addLoadingState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            
            // Restore button after form submission
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }, 2000);
        }
    }
    
    handleTabNavigation(event) {
        // Enhanced tab navigation for cards
        const activeElement = document.activeElement;
        if (activeElement.classList.contains('module-card') || 
            activeElement.classList.contains('quick-action-card')) {
            // Add visual indicator for keyboard navigation
            activeElement.style.boxShadow = '0 0 0 3px rgba(0, 123, 255, 0.25)';
            
            activeElement.addEventListener('blur', () => {
                activeElement.style.boxShadow = '';
            }, { once: true });
        }
    }
    
    focusSearch() {
        const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="search"], input[id*="search"]');
        if (searchInputs.length > 0) {
            searchInputs[0].focus();
        }
    }
    
    adjustForScreenSize() {
        // Responsive adjustments
        const screenWidth = window.innerWidth;
        
        if (screenWidth < 768) {
            // Mobile adjustments
            this.adjustForMobile();
        } else if (screenWidth < 1200) {
            // Tablet adjustments
            this.adjustForTablet();
        } else {
            // Desktop adjustments
            this.adjustForDesktop();
        }
    }
    
    adjustForMobile() {
        // Mobile-specific adjustments
        const cards = document.querySelectorAll('.module-card, .quick-action-card');
        cards.forEach(card => {
            card.style.marginBottom = '1rem';
        });
    }
    
    adjustForTablet() {
        // Tablet-specific adjustments
        const sidebar = document.querySelector('.chat-sidebar, .services-sidebar');
        if (sidebar) {
            sidebar.style.marginTop = '1rem';
        }
    }
    
    adjustForDesktop() {
        // Desktop-specific adjustments
        const sidebar = document.querySelector('.chat-sidebar, .services-sidebar');
        if (sidebar) {
            sidebar.style.marginTop = '0';
        }
    }
    
    repositionModals() {
        // Adjust modal positioning on resize
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalDialog = modal.querySelector('.modal-dialog');
            if (modalDialog) {
                modalDialog.style.marginTop = '1.75rem';
            }
        });
    }
    
    handleScrollAnimations() {
        // Handle scroll-based animations
        const scrollY = window.scrollY;
        const elements = document.querySelectorAll('[data-scroll-animation]');
        
        elements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                const animationType = element.getAttribute('data-scroll-animation');
                element.classList.add(animationType);
            }
        });
    }
    
    updateNavigationState() {
        // Update navigation based on scroll position
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    }
    
    // Public API methods
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 300px;
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    loadComponent(url, container) {
        return fetch(url)
            .then(response => response.text())
            .then(html => {
                const targetContainer = typeof container === 'string' 
                    ? document.querySelector(container) 
                    : container;
                
                if (targetContainer) {
                    targetContainer.innerHTML = html;
                    // Reinitialize components in loaded content
                    this.initializeComponents();
                }
            })
            .catch(error => {
                console.error('Error loading component:', error);
                this.showNotification('Error loading content', 'danger');
            });
    }
    
    // Data management
    saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }
    
    loadFromLocalStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return defaultValue;
        }
    }
    
    // Performance monitoring
    measurePerformance(name, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        console.log(`${name} took ${end - start} milliseconds`);
        return result;
    }
}

// Initialize the platform when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main platform functionality
    window.communityPlatform = new CommunityPlatform();
    
    // Set up global error handling
    window.addEventListener('error', function(event) {
        console.error('Global error:', event.error);
        if (window.communityPlatform) {
            window.communityPlatform.showNotification('An error occurred. Please try again.', 'danger');
        }
    });
    
    // Set up offline handling
    window.addEventListener('online', function() {
        if (window.communityPlatform) {
            window.communityPlatform.showNotification('Connection restored', 'success');
        }
    });
    
    window.addEventListener('offline', function() {
        if (window.communityPlatform) {
            window.communityPlatform.showNotification('Connection lost. Some features may not work.', 'warning');
        }
    });
});

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommunityPlatform;
}

// Global utility functions
window.utils = {
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    formatTime: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }).format(new Date(date));
    },
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};
