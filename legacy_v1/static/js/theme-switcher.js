/**
 * Enhanced Theme Switcher
 * Features:
 * - Smooth animations
 * - System preference detection
 * - LocalStorage persistence
 * - Keyboard shortcuts
 * - Custom events
 * - Automatic UI updates
 */

class ThemeSwitcher {
    constructor() {
        this.theme = this.getStoredTheme() || this.getSystemTheme();
        this.transitionDuration = 300; // ms
        this.init();
        this.setupKeyboardShortcuts();
    }
    
    /**
     * Get theme from localStorage
     */
    getStoredTheme() {
        try {
            return localStorage.getItem('theme');
        } catch (e) {
            console.warn('localStorage not available:', e);
            return null;
        }
    }
    
    /**
     * Detect system color scheme preference
     */
    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }
    
    /**
     * Initialize theme switcher
     */
    init() {
        // Set initial theme
        this.applyTheme(this.theme, false);
        this.updateUI();
        
        // Listen for system theme changes
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            // Modern browsers
            if (darkModeQuery.addEventListener) {
                darkModeQuery.addEventListener('change', (e) => this.handleSystemThemeChange(e));
            } 
            // Legacy browsers
            else if (darkModeQuery.addListener) {
                darkModeQuery.addListener((e) => this.handleSystemThemeChange(e));
            }
        }
        
        // Log initialization
        console.log('🌓 Theme Switcher initialized:', this.theme);
    }
    
    /**
     * Handle system theme changes
     */
    handleSystemThemeChange(e) {
        // Only auto-switch if user hasn't manually set a preference
        if (!this.getStoredTheme()) {
            const newTheme = e.matches ? 'dark' : 'light';
            this.setTheme(newTheme, false);
            console.log('🌓 System theme changed to:', newTheme);
        }
    }
    
    /**
     * Toggle between light and dark themes
     */
    toggle() {
        const newTheme = this.theme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme, true);
    }
    
    /**
     * Set specific theme
     * @param {string} theme - 'light' or 'dark'
     * @param {boolean} save - Whether to save to localStorage
     */
    setTheme(theme, save = true) {
        if (theme !== 'light' && theme !== 'dark') {
            console.error('Invalid theme:', theme);
            return;
        }
        
        this.theme = theme;
        this.applyTheme(theme, true);
        
        if (save) {
            this.saveTheme(theme);
        }
        
        this.updateUI();
        this.dispatchThemeChangeEvent(theme);
    }
    
    /**
     * Apply theme to document
     * @param {string} theme - Theme to apply
     * @param {boolean} animate - Whether to animate the transition
     */
    applyTheme(theme, animate = false) {
        if (animate) {
            // Add transition class
            document.body.classList.add('theme-transitioning');
        }
        
        // Update data attribute
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor(theme);
        
        if (animate) {
            // Remove transition class after animation completes
            setTimeout(() => {
                document.body.classList.remove('theme-transitioning');
            }, this.transitionDuration);
        }
    }
    
    /**
     * Update mobile browser theme color
     */
    updateMetaThemeColor(theme) {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        // Set color based on theme
        const colors = {
            light: '#f5f7fa',
            dark: '#0a0e27'
        };
        
        metaThemeColor.content = colors[theme] || colors.dark;
    }
    
    /**
     * Save theme to localStorage
     */
    saveTheme(theme) {
        try {
            localStorage.setItem('theme', theme);
        } catch (e) {
            console.warn('Failed to save theme:', e);
        }
    }
    
    /**
     * Update UI elements (toggle buttons, icons, etc.)
     */
    updateUI() {
        // Update main toggle button
        const toggle = document.getElementById('themeToggle');
        const icon = document.getElementById('toggleIcon');
        
        if (toggle && icon) {
            if (this.theme === 'light') {
                toggle.classList.add('active');
                icon.textContent = '☀️';
            } else {
                toggle.classList.remove('active');
                icon.textContent = '🌙';
            }
        }
        
        // Update floating button if it exists
        const floatingToggle = document.getElementById('themeToggleFloating');
        if (floatingToggle) {
            const floatingIcon = floatingToggle.querySelector('.icon');
            if (floatingIcon) {
                floatingIcon.textContent = this.theme === 'dark' ? '🌙' : '☀️';
            }
        }
        
        // Update any other theme-dependent elements
        this.updateCharts();
    }
    
    /**
     * Update chart colors if Chart.js is present
     */
    updateCharts() {
        if (typeof Chart !== 'undefined' && Chart.instances) {
            const textColor = this.theme === 'dark' ? '#8b92b2' : '#4a5578';
            const gridColor = this.theme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
            
            // Update all chart instances
            Object.values(Chart.instances).forEach(chart => {
                if (chart.options.scales) {
                    // Update scales
                    Object.keys(chart.options.scales).forEach(scaleKey => {
                        const scale = chart.options.scales[scaleKey];
                        if (scale.ticks) scale.ticks.color = textColor;
                        if (scale.grid) scale.grid.color = gridColor;
                    });
                    
                    // Update legend
                    if (chart.options.plugins && chart.options.plugins.legend) {
                        chart.options.plugins.legend.labels.color = textColor;
                    }
                    
                    // Re-render chart
                    chart.update();
                }
            });
        }
    }
    
    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+T or Cmd+Shift+T
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.toggle();
                this.showThemeToast();
            }
        });
    }
    
    /**
     * Show toast notification when theme changes
     */
    showThemeToast() {
        // Remove existing toast if any
        const existingToast = document.getElementById('themeToast');
        if (existingToast) {
            existingToast.remove();
        }
        
        // Create toast
        const toast = document.createElement('div');
        toast.id = 'themeToast';
        toast.className = 'theme-toast';
        toast.innerHTML = `
            <span class="toast-icon">${this.theme === 'dark' ? '🌙' : '☀️'}</span>
            <span class="toast-text">${this.theme === 'dark' ? 'Dark' : 'Light'} mode activated</span>
        `;
        
        // Add styles if not already present
        if (!document.getElementById('themeToastStyles')) {
            const style = document.createElement('style');
            style.id = 'themeToastStyles';
            style.textContent = `
                .theme-toast {
                    position: fixed;
                    bottom: 30px;
                    left: 50%;
                    transform: translateX(-50%) translateY(100px);
                    background: var(--bg-card);
                    color: var(--text-primary);
                    padding: 12px 20px;
                    border-radius: 50px;
                    box-shadow: var(--shadow-lg);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    z-index: 10000;
                    animation: toastSlideUp 0.3s ease forwards;
                    border: 1px solid var(--border-color);
                }
                
                @keyframes toastSlideUp {
                    to {
                        transform: translateX(-50%) translateY(0);
                    }
                }
                
                .theme-toast .toast-icon {
                    font-size: 20px;
                }
                
                .theme-toast .toast-text {
                    font-size: 14px;
                    font-weight: 500;
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(toast);
        
        // Remove toast after 2 seconds
        setTimeout(() => {
            toast.style.animation = 'toastSlideDown 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }
    
    /**
     * Dispatch custom theme change event
     */
    dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themechange', {
            detail: {
                theme: theme,
                timestamp: new Date().toISOString()
            }
        });
        window.dispatchEvent(event);
    }
    
    /**
     * Get current theme
     */
    getCurrentTheme() {
        return this.theme;
    }
    
    /**
     * Check if dark mode is active
     */
    isDarkMode() {
        return this.theme === 'dark';
    }
    
    /**
     * Check if light mode is active
     */
    isLightMode() {
        return this.theme === 'light';
    }
}

// Initialize theme switcher
const themeSwitcher = new ThemeSwitcher();

// Global toggle function for HTML onclick handlers
function toggleTheme() {
    themeSwitcher.toggle();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeSwitcher;
}

// Make available globally
window.themeSwitcher = themeSwitcher;
window.toggleTheme = toggleTheme;

// Listen for theme changes
window.addEventListener('themechange', (e) => {
    console.log('Theme changed:', e.detail);
});

// Add toast slide down animation
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    @keyframes toastSlideDown {
        to {
            transform: translateX(-50%) translateY(100px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(toastStyle);

// Log ready state
console.log('🌓 Theme Switcher ready. Press Ctrl+Shift+T to toggle.');