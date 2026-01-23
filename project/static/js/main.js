/* ========================================
   Interactive Features for SpamShield
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    initSmoothScroll();
    
    // Add animations to cards on scroll
    initScrollAnimations();
    
    // Form validation and feedback
    initFormHandling();
});

/**
 * Initialize smooth scrolling for navigation links
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add animation classes as elements scroll into view
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Apply to info cards
    const cards = document.querySelectorAll('.info-card, .case-study, .tip-item');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

/**
 * Initialize form handling and validation
 */
function initFormHandling() {
    const messageForm = document.querySelector('.detection-form');
    if (messageForm) {
        const textarea = messageForm.querySelector('textarea');
        
        if (textarea) {
            // Auto-expand textarea as user types
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 400) + 'px';
            });
            
            // Add focus effect
            textarea.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            textarea.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        }
        
        // Form submission feedback
        messageForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && textarea.value.trim()) {
                // Show loading state
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
                
                // Reset after submission (form will refresh)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 1000);
            }
        });
    }
}

/**
 * Utility function to copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Show temporary notification message
 */
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; animation: slideIn 0.3s ease;';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit detection form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.querySelector('.detection-form');
        if (form) {
            form.submit();
        }
    }
});

// Export functions for use in templates if needed
window.SpamShield = {
    copyToClipboard,
    showNotification
};
