// FAQ functionality
function setupFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const isActive = question.classList.contains('active');
            
            // Close all other FAQ items
            faqQuestions.forEach(q => {
                q.classList.remove('active');
                q.nextElementSibling.classList.remove('active');
            });
            
            // Toggle current item
            if (!isActive) {
                question.classList.add('active');
                answer.classList.add('active');
            }
        });
    });
}

// Contact form functionality
function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(contactForm);
            const data = {
                firstName: document.getElementById('first-name').value,
                lastName: document.getElementById('last-name').value,
                email: document.getElementById('email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value
            };
            
            // Validate form
            if (!validateContactForm(data)) {
                return;
            }
            
            // Simulate form submission
            showNotification('Message sent successfully! We\'ll get back to you within 24 hours.', 'success');
            contactForm.reset();
        });
    }
}

function validateContactForm(data) {
    if (!data.firstName || !data.lastName || !data.email || !data.subject || !data.message) {
        showNotification('Please fill in all fields.', 'error');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showNotification('Please enter a valid email address.', 'error');
        return false;
    }
    
    return true;
}

// Chat functionality
class ChatWidget {
    constructor() {
        this.isOpen = false;
        this.messages = [
            {
                type: 'bot',
                text: 'Hi! Welcome to SHALLION. How can I help you today?',
                timestamp: new Date()
            }
        ];
        
        this.responses = {
            'hello': 'Hello! How can I assist you today?',
            'hi': 'Hi there! What can I help you with?',
            'order': 'I can help you with your order. Do you need to track an order, make changes, or have questions about delivery?',
            'delivery': 'Our standard delivery takes 3-5 business days. Express delivery (1-2 days) is available for an additional fee. Food delivery is typically within 30 minutes.',
            'return': 'We offer a 30-day return policy for most items. Food items cannot be returned for safety reasons. Please contact our support team to initiate a return.',
            'payment': 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay. All payments are processed securely through Stripe.',
            'track': 'You can track your order by logging into your account and visiting the "My Orders" section. You\'ll receive tracking updates via email and SMS.',
            'help': 'I\'m here to help! You can ask me about orders, delivery, returns, payments, or any other questions about SHALLION.',
            'thanks': 'You\'re welcome! Is there anything else I can help you with?',
            'bye': 'Thank you for chatting with us! Have a great day!'
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.renderMessages();
    }
    
    setupEventListeners() {
        const chatToggle = document.getElementById('chat-toggle');
        const chatClose = document.getElementById('chat-close');
        const chatSend = document.getElementById('chat-send');
        const chatInput = document.getElementById('chat-input');
        
        if (chatToggle) {
            chatToggle.addEventListener('click', () => this.toggleChat());
        }
        
        if (chatClose) {
            chatClose.addEventListener('click', () => this.closeChat());
        }
        
        if (chatSend) {
            chatSend.addEventListener('click', () => this.sendMessage());
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }
    }
    
    toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            chatWindow.classList.add('active');
        } else {
            chatWindow.classList.remove('active');
        }
    }
    
    closeChat() {
        const chatWindow = document.getElementById('chat-window');
        this.isOpen = false;
        chatWindow.classList.remove('active');
    }
    
    sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        chatInput.value = '';
        
        // Simulate typing delay
        setTimeout(() => {
            this.generateResponse(message);
        }, 1000);
    }
    
    addMessage(type, text) {
        this.messages.push({
            type,
            text,
            timestamp: new Date()
        });
        this.renderMessages();
    }
    
    generateResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        let response = 'I\'m sorry, I didn\'t understand that. Could you please rephrase or ask about orders, delivery, returns, or payments?';
        
        // Check for keywords in user message
        for (const [keyword, botResponse] of Object.entries(this.responses)) {
            if (lowerMessage.includes(keyword)) {
                response = botResponse;
                break;
            }
        }
        
        // Add some variety to responses
        if (lowerMessage.includes('how are you')) {
            response = 'I\'m doing great, thank you for asking! How can I help you today?';
        }
        
        if (lowerMessage.includes('what time') || lowerMessage.includes('hours')) {
            response = 'Our support hours are Monday - Friday: 9AM - 6PM, Saturday: 10AM - 4PM, Sunday: Closed.';
        }
        
        this.addMessage('bot', response);
    }
    
    renderMessages() {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        chatMessages.innerHTML = this.messages.map(message => `
            <div class="chat-message ${message.type}">
                ${message.text}
            </div>
        `).join('');
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#f39c12';
    notification.style.color = 'white';
    notification.style.padding = 'var(--space-sm) var(--space-md)';
    notification.style.borderRadius = 'var(--border-radius)';
    notification.style.zIndex = '1000';
    notification.style.boxShadow = 'var(--shadow-md)';
    notification.style.transform = 'translateX(100%)';
    notification.style.transition = 'transform 0.3s ease';
    notification.style.maxWidth = '300px';
    notification.style.wordWrap = 'break-word';
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Quick actions functionality
function setupQuickActions() {
    const quickActions = document.querySelectorAll('.quick-action');
    
    quickActions.forEach(action => {
        action.addEventListener('click', (e) => {
            const actionType = action.querySelector('span').textContent.toLowerCase();
            
            switch(actionType) {
                case 'faq':
                    // Already handled by smooth scrolling
                    break;
                case 'contact us':
                    // Already handled by smooth scrolling
                    break;
                case 'live chat':
                    e.preventDefault();
                    const chatWidget = new ChatWidget();
                    chatWidget.toggleChat();
                    break;
                case 'track order':
                    e.preventDefault();
                    showNotification('Order tracking feature coming soon! Please contact our support team for order status.', 'info');
                    break;
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupFAQ();
    setupContactForm();
    setupSmoothScrolling();
    setupQuickActions();
    
    // Initialize chat widget
    const chatWidget = new ChatWidget();
    
    // Add some interactive elements
    console.log('Help page loaded successfully!');
}); 