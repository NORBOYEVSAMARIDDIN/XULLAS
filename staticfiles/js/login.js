// Auto-close alert after 3 seconds
setTimeout(() => {
    const alert = document.getElementById('auto-close-alert');
    if (alert) {
        $(alert).alert('close');
    }
}, 3000);

// Toggle password visibility
function togglePassword(inputId, element) {
    const input = document.getElementById(inputId);
    const icon = element.querySelector('i');
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("ri-eye-line");
        icon.classList.add("ri-eye-off-line");
    } else {
        input.type = "password";
        icon.classList.remove("ri-eye-off-line");
        icon.classList.add("ri-eye-line");
    }
}

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.login-form');
    const inputs = document.querySelectorAll('.form-input');
    const loginBtn = document.querySelector('.login-btn');
    
    // Add floating label effect
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.input-wrapper').classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.closest('.input-wrapper').classList.remove('focused');
            }
        });
        
        // Check if input has value on page load
        if (input.value !== '') {
            input.closest('.input-wrapper').classList.add('focused');
        }
    });
    
    // Form submission with loading state
    form.addEventListener('submit', function(e) {
        const username = form.querySelector('input[name="username"]').value;
        const password = form.querySelector('input[name="password"]').value;
        
        if (!username || !password) {
            e.preventDefault();
            showError('Please fill in all fields');
            return;
        }
        
        // Show loading state
        loginBtn.disabled = true;
        loginBtn.innerHTML = '<i class="ri-loader-4-line ri-spin"></i> Signing in...';
        
        // If there's an error, reset the button after 3 seconds
        setTimeout(() => {
            if (loginBtn.disabled) {
                resetButton();
            }
        }, 3000);
    });
    
    function resetButton() {
        loginBtn.disabled = false;
        loginBtn.innerHTML = '<span>Sign In</span><i class="ri-arrow-right-line"></i>';
    }
    
    function showError(message) {
        // Remove existing error alerts
        const existingAlert = document.querySelector('.custom-alert');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        // Create new error alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show custom-alert';
        alert.innerHTML = `
            <div class="alert-content">
                <i class="ri-error-warning-line"></i>
                ${message}
            </div>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (alert) {
                $(alert).alert('close');
            }
        }, 3000);
    }
    
    // Add ripple effect to button
    loginBtn.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const focusedElement = document.activeElement;
            if (focusedElement.classList.contains('form-input')) {
                const inputs = Array.from(document.querySelectorAll('.form-input'));
                const currentIndex = inputs.indexOf(focusedElement);
                
                if (currentIndex < inputs.length - 1) {
                    e.preventDefault();
                    inputs[currentIndex + 1].focus();
                }
            }
        }
    });
    
    // Smooth scroll for alerts
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('custom-alert')) {
                        node.style.opacity = '0';
                        node.style.transform = 'translateX(-50%) translateY(-20px)';
                        
                        setTimeout(() => {
                            node.style.transition = 'all 0.3s ease';
                            node.style.opacity = '1';
                            node.style.transform = 'translateX(-50%) translateY(0)';
                        }, 10);
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, { childList: true });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .login-btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .ri-spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .input-wrapper.focused .input-icon {
        color: #667eea;
    }
`;
document.head.appendChild(style);