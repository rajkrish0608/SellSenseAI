/**
 * Theme Toggle with Floating Button
 * Beautiful animated theme switcher
 */

(function() {
    // Create floating button
    const button = document.createElement('button');
    button.className = 'theme-toggle-floating';
    button.id = 'themeToggleFloating';
    button.setAttribute('aria-label', 'Toggle theme');
    button.innerHTML = '<span class="icon">🌙</span>';
    
    // Add to body
    document.body.appendChild(button);
    
    // Initialize theme
    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateIcon(currentTheme);
    
    // Click handler
    button.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        
        // Update theme
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
        
        // Add ripple effect
        createRipple(button);
    });
    
    function updateIcon(theme) {
        const icon = button.querySelector('.icon');
        icon.textContent = theme === 'dark' ? '🌙' : '☀️';
    }
    
    function createRipple(element) {
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
})();