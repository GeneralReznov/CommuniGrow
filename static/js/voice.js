// Voice Navigation and Accessibility System
class VoiceNavigationSystem {
    constructor() {
        this.isListening = false;
        this.isSpeaking = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.currentVoice = null;
        
        this.init();
    }
    
    init() {
        this.setupSpeechRecognition();
        this.setupTextToSpeech();
        this.setupEventListeners();
        this.loadVoiceSettings();
    }
    
    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.updateVoiceStatus('Listening...');
                this.isListening = true;
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript.toLowerCase();
                this.handleVoiceCommand(transcript);
                this.updateVoiceStatus('Command received');
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceStatus('Voice recognition error');
                this.isListening = false;
            };
            
            this.recognition.onend = () => {
                this.updateVoiceStatus('Ready for voice commands');
                this.isListening = false;
            };
        }
    }
    
    setupTextToSpeech() {
        if (this.synthesis) {
            this.synthesis.onvoiceschanged = () => {
                this.voices = this.synthesis.getVoices();
                this.selectBestVoice();
            };
            
            // Initial load of voices
            this.voices = this.synthesis.getVoices();
            if (this.voices.length > 0) {
                this.selectBestVoice();
            }
        }
    }
    
    selectBestVoice() {
        // Prefer English voices, female voices for accessibility
        const preferredVoices = [
            'Google US English Female',
            'Microsoft Zira',
            'Alex',
            'Samantha'
        ];
        
        for (let preferred of preferredVoices) {
            const voice = this.voices.find(v => v.name.includes(preferred));
            if (voice) {
                this.currentVoice = voice;
                return;
            }
        }
        
        // Fallback to any English voice
        const englishVoice = this.voices.find(v => v.lang.startsWith('en'));
        if (englishVoice) {
            this.currentVoice = englishVoice;
        }
    }
    
    setupEventListeners() {
        // Voice tour button
        const voiceTourBtn = document.getElementById('voice-tour-btn');
        if (voiceTourBtn) {
            voiceTourBtn.addEventListener('click', () => this.startVoiceTour());
        }
        
        // Speak button
        const speakBtn = document.getElementById('speak-btn');
        if (speakBtn) {
            speakBtn.addEventListener('click', () => this.speakCurrentPage());
        }
        
        // Listen button
        const listenBtn = document.getElementById('listen-btn');
        if (listenBtn) {
            listenBtn.addEventListener('click', () => this.toggleListening());
        }
        
        // Emergency button
        const emergencyBtn = document.getElementById('emergency-btn');
        if (emergencyBtn) {
            emergencyBtn.addEventListener('click', () => this.handleEmergency());
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            this.handleKeyboardShortcuts(event);
        });
    }
    
    handleKeyboardShortcuts(event) {
        // Alt + V: Start voice tour
        if (event.altKey && event.key.toLowerCase() === 'v') {
            event.preventDefault();
            this.startVoiceTour();
        }
        
        // Alt + L: Toggle listening
        if (event.altKey && event.key.toLowerCase() === 'l') {
            event.preventDefault();
            this.toggleListening();
        }
        
        // Alt + S: Speak current page
        if (event.altKey && event.key.toLowerCase() === 's') {
            event.preventDefault();
            this.speakCurrentPage();
        }
        
        // Alt + E: Emergency information
        if (event.altKey && event.key.toLowerCase() === 'e') {
            event.preventDefault();
            this.handleEmergency();
        }
        
        // Escape: Stop speaking or listening
        if (event.key === 'Escape') {
            this.stopAllVoiceActivities();
        }
    }
    
    speak(text, options = {}) {
        if (!this.synthesis || !text) return;
        
        // Stop any current speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configure utterance
        utterance.voice = this.currentVoice;
        utterance.rate = options.rate || 0.9;
        utterance.pitch = options.pitch || 1.0;
        utterance.volume = options.volume || 1.0;
        
        utterance.onstart = () => {
            this.isSpeaking = true;
            this.updateVoiceStatus('Speaking...');
        };
        
        utterance.onend = () => {
            this.isSpeaking = false;
            this.updateVoiceStatus('Ready for voice commands');
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.isSpeaking = false;
            this.updateVoiceStatus('Speech error');
        };
        
        this.synthesis.speak(utterance);
    }
    
    startVoiceTour() {
        const currentPage = this.getCurrentPageContext();
        let tourText = '';
        
        switch (currentPage) {
            case 'index':
                tourText = this.getIndexTourText();
                break;
            case 'dashboard':
                tourText = this.getDashboardTourText();
                break;
            case 'climate':
                tourText = this.getClimateTourText();
                break;
            case 'skills':
                tourText = this.getSkillsTourText();
                break;
            case 'food':
                tourText = this.getFoodTourText();
                break;
            case 'health':
                tourText = this.getHealthTourText();
                break;
            default:
                tourText = this.getGeneralTourText();
        }
        
        this.speak(tourText);
    }
    
    getCurrentPageContext() {
        const path = window.location.pathname;
        if (path === '/') return 'index';
        if (path === '/dashboard') return 'dashboard';
        if (path.startsWith('/climate')) return 'climate';
        if (path.startsWith('/skills')) return 'skills';
        if (path.startsWith('/food')) return 'food';
        if (path.startsWith('/health')) return 'health';
        return 'general';
    }
    
    getIndexTourText() {
        return `Welcome to the Community Empowerment Platform. This is your starting point for accessing climate action, skills development, food security, and health resources. 
        
        Use voice commands like "go to dashboard", "show me climate information", or "find health services". 
        
        The platform is designed for accessibility with voice navigation throughout. Press Alt+L to start voice commands, Alt+S to have content read aloud, or Alt+E for emergency information.
        
        Would you like me to take you to the main dashboard?`;
    }
    
    getDashboardTourText() {
        return `You're on the main dashboard with four core modules: 
        
        Climate Action provides weather alerts and sustainable practices. 
        Skills and Employment offers job matching and learning opportunities. 
        Food and Nutrition connects you to local marketplace and nutrition guidance. 
        Health and Well-being provides AI health support and service mapping.
        
        Quick action buttons let you check weather, ask health questions, post food items, or create job listings. 
        
        Say "open climate module", "show me jobs", or "health services" to navigate.`;
    }
    
    getClimateTourText() {
        return `Climate Action module helps you prepare for weather challenges and practice sustainability. 
        
        View current weather conditions, receive climate alerts, and learn sustainable farming, energy, and water practices. 
        
        IoT sensor integration shows environmental data when hardware is detected. 
        
        Voice commands: "check weather", "show alerts", "sustainable farming", or "energy tips".`;
    }
    
    getSkillsTourText() {
        return `Skills and Employment module connects you with learning and work opportunities. 
        
        Browse job listings with AI-powered matching, access microlearning modules, find volunteer opportunities, and share your skills with the community. 
        
        Say "find jobs", "start learning", "volunteer opportunities", or "post my skills" to navigate.`;
    }
    
    getFoodTourText() {
        return `Food and Nutrition module supports food security and healthy eating. 
        
        Access the local marketplace, community food sharing, surplus rescue, and get AI nutrition advice. 
        
        Voice commands: "show marketplace", "nutrition advice", "post food", or "community recipes".`;
    }
    
    getHealthTourText() {
        return `Health and Well-being module provides comprehensive health support. 
        
        Chat with AI health assistant, find local health services on the map, take health assessments, and access emergency information. 
        
        Say "health chat", "find clinics", "health assessment", or "emergency info" to navigate.`;
    }
    
    getGeneralTourText() {
        return `This platform helps underserved communities with climate action, skills development, food security, and healthcare access. 
        
        Use voice commands to navigate: "go to dashboard", "show climate", "find jobs", "food marketplace", or "health services". 
        
        Press Alt+L for voice commands or Alt+E for emergency information.`;
    }
    
    speakCurrentPage() {
        const pageContent = this.extractPageContent();
        if (pageContent) {
            this.speak(pageContent);
        } else {
            this.speak('Page content is not available for reading.');
        }
    }
    
    extractPageContent() {
        // Get main content, prioritizing specific content areas
        const contentSelectors = [
            'main#main-content',
            '.container .row',
            '.hero-content',
            'main',
            '.content'
        ];
        
        for (let selector of contentSelectors) {
            const element = document.querySelector(selector);
            if (element) {
                return this.extractTextContent(element);
            }
        }
        
        return null;
    }
    
    extractTextContent(element) {
        // Extract meaningful text, excluding navigation and scripts
        const clone = element.cloneNode(true);
        
        // Remove unwanted elements
        const unwanted = clone.querySelectorAll('nav, script, style, .btn, .navbar, .modal, .d-none');
        unwanted.forEach(el => el.remove());
        
        // Get text content and clean it up
        let text = clone.textContent || clone.innerText;
        text = text.replace(/\s+/g, ' ').trim();
        text = text.substring(0, 1000); // Limit length
        
        return text;
    }
    
    toggleListening() {
        if (!this.recognition) {
            this.speak('Voice recognition is not supported in your browser.');
            return;
        }
        
        if (this.isListening) {
            this.recognition.stop();
            this.updateVoiceStatus('Voice commands stopped');
        } else {
            this.recognition.start();
            this.updateVoiceStatus('Say a command...');
        }
    }
    
    handleVoiceCommand(command) {
        console.log('Voice command received:', command);
        
        // Global navigation commands
        if (command.includes('dashboard') || command.includes('home')) {
            window.location.href = '/dashboard';
            this.speak('Going to dashboard');
            return;
        }
        
        if (command.includes('climate') || command.includes('weather')) {
            window.location.href = '/climate';
            this.speak('Opening climate module');
            return;
        }
        
        if (command.includes('skills') || command.includes('jobs') || command.includes('employment')) {
            window.location.href = '/skills';
            this.speak('Opening skills and employment module');
            return;
        }
        
        if (command.includes('food') || command.includes('nutrition') || command.includes('marketplace')) {
            window.location.href = '/food';
            this.speak('Opening food and nutrition module');
            return;
        }
        
        if (command.includes('health') || command.includes('medical') || command.includes('doctor')) {
            window.location.href = '/health';
            this.speak('Opening health and well-being module');
            return;
        }
        
        // Emergency commands
        if (command.includes('emergency') || command.includes('help') || command.includes('911')) {
            this.handleEmergency();
            return;
        }
        
        // Utility commands
        if (command.includes('stop') || command.includes('quiet')) {
            this.stopAllVoiceActivities();
            this.speak('Voice activities stopped');
            return;
        }
        
        if (command.includes('repeat') || command.includes('say again')) {
            this.repeatLastSpoken();
            return;
        }
        
        if (command.includes('tour') || command.includes('guide')) {
            this.startVoiceTour();
            return;
        }
        
        // Page-specific commands (delegate to global handler if available)
        if (typeof window.globalVoiceHandler === 'function') {
            window.globalVoiceHandler(command);
        } else {
            this.speak('Command not recognized. Try saying "tour" for guidance, or "dashboard" to navigate.');
        }
    }
    
    handleEmergency() {
        const emergencyText = `Emergency information: Call 911 for life-threatening emergencies. Call 988 for mental health crisis support. Call 1-800-222-1222 for poison control. This platform provides information only - always call professionals for real emergencies.`;
        
        this.speak(emergencyText, { rate: 0.8 }); // Slower for emergency info
        
        // Show emergency modal if available
        const emergencyModal = document.getElementById('emergencyModal');
        if (emergencyModal) {
            const modal = new bootstrap.Modal(emergencyModal);
            modal.show();
        }
    }
    
    stopAllVoiceActivities() {
        if (this.synthesis) {
            this.synthesis.cancel();
        }
        
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
        
        this.isSpeaking = false;
        this.isListening = false;
        this.updateVoiceStatus('Voice activities stopped');
    }
    
    repeatLastSpoken() {
        // This would require storing the last spoken text
        this.speak('Repeat function not yet implemented. Use specific commands to navigate.');
    }
    
    updateVoiceStatus(status) {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = status;
        }
    }
    
    loadVoiceSettings() {
        // Load user preferences from localStorage
        const settings = localStorage.getItem('voiceSettings');
        if (settings) {
            try {
                const parsed = JSON.parse(settings);
                // Apply saved settings for rate, pitch, volume
            } catch (e) {
                console.error('Error loading voice settings:', e);
            }
        }
    }
    
    saveVoiceSettings(settings) {
        localStorage.setItem('voiceSettings', JSON.stringify(settings));
    }
}

// Accessibility Enhancement Functions
function increaseFontSize() {
    document.body.classList.toggle('large-text');
    const isLarge = document.body.classList.contains('large-text');
    localStorage.setItem('largeFontEnabled', isLarge);
    
    if (window.voiceSystem) {
        window.voiceSystem.speak(isLarge ? 'Large font enabled' : 'Normal font restored');
    }
}

function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
    const isHighContrast = document.body.classList.contains('high-contrast');
    localStorage.setItem('highContrastEnabled', isHighContrast);
    
    if (window.voiceSystem) {
        window.voiceSystem.speak(isHighContrast ? 'High contrast mode enabled' : 'Normal contrast restored');
    }
}

function toggleReducedMotion() {
    document.body.classList.toggle('reduced-motion');
    const isReduced = document.body.classList.contains('reduced-motion');
    localStorage.setItem('reducedMotionEnabled', isReduced);
    
    if (isReduced) {
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        style.id = 'reduced-motion-style';
        document.head.appendChild(style);
    } else {
        const existingStyle = document.getElementById('reduced-motion-style');
        if (existingStyle) {
            existingStyle.remove();
        }
    }
    
    if (window.voiceSystem) {
        window.voiceSystem.speak(isReduced ? 'Motion reduction enabled' : 'Normal animations restored');
    }
}

// Global convenience function for speaking text
function speakText(text, options = {}) {
    if (window.voiceSystem) {
        window.voiceSystem.speak(text, options);
    }
}

// Initialize voice system when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize voice navigation system
    window.voiceSystem = new VoiceNavigationSystem();
    
    // Load accessibility preferences
    const largeFontEnabled = localStorage.getItem('largeFontEnabled') === 'true';
    const highContrastEnabled = localStorage.getItem('highContrastEnabled') === 'true';
    const reducedMotionEnabled = localStorage.getItem('reducedMotionEnabled') === 'true';
    
    if (largeFontEnabled) {
        document.body.classList.add('large-text');
    }
    
    if (highContrastEnabled) {
        document.body.classList.add('high-contrast');
    }
    
    if (reducedMotionEnabled) {
        toggleReducedMotion(); // This will apply the reduced motion styles
    }
    
    // Announce page load for screen readers
    setTimeout(() => {
        const pageTitle = document.title || 'Community Platform page loaded';
        if (window.voiceSystem) {
            // Don't auto-announce on every page load, but make it available
            console.log('Voice system ready:', pageTitle);
        }
    }, 1000);
});

// Handle visibility change to pause voice when tab is not active
document.addEventListener('visibilitychange', function() {
    if (document.hidden && window.voiceSystem && window.voiceSystem.isSpeaking) {
        window.voiceSystem.synthesis.pause();
    } else if (!document.hidden && window.voiceSystem) {
        window.voiceSystem.synthesis.resume();
    }
});

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceNavigationSystem;
}
