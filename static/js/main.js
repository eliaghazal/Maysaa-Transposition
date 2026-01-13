// Main JavaScript for Columnar Transposition Cipher System

// Toast Notification System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${getToastIcon(type)}</div>
        <div class="toast-message">${message}</div>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ'
    };
    return icons[type] || icons['info'];
}

// Loading Overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Copy to Clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy: ' + err, 'error');
    });
}

// Active Navigation Link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = 'rgba(255, 255, 255, 0.2)';
        }
    });
});

// Form Validation Helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    let isValid = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'var(--danger-color)';
        } else {
            input.style.borderColor = 'var(--border-color)';
        }
    });
    
    return isValid;
}

// Key Validation
async function validateKey(key) {
    try {
        const response = await fetch('/api/validate_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: key })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error validating key:', error);
        return { valid: false };
    }
}

// Auto-save to localStorage (optional feature)
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key) {
    try {
        return localStorage.getItem(key);
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format large numbers
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Export results as JSON
function exportAsJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    
    URL.revokeObjectURL(url);
}

// Export results as text
function exportAsText(text, filename) {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    
    URL.revokeObjectURL(url);
}

// Character counter for textareas
function setupCharacterCounter(textareaId, counterId) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (textarea && counter) {
        textarea.addEventListener('input', () => {
            counter.textContent = textarea.value.length;
        });
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Focus on key input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const keyInput = document.getElementById('key');
        if (keyInput) keyInput.focus();
    }
    
    // Escape: Close modals/overlays
    if (e.key === 'Escape') {
        hideLoading();
    }
});

// Matrix animation helper
function animateMatrix(matrixElement) {
    const cells = matrixElement.querySelectorAll('.matrix-cell:not(.header-cell)');
    
    cells.forEach((cell, index) => {
        setTimeout(() => {
            cell.style.animation = 'fadeIn 0.3s ease';
            cell.style.animationFillMode = 'forwards';
        }, index * 50);
    });
}

// Add fadeIn animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Progress indicator
class ProgressIndicator {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.value = 0;
    }
    
    update(value) {
        this.value = Math.max(0, Math.min(100, value));
        if (this.container) {
            this.container.style.width = this.value + '%';
        }
    }
    
    increment(step = 1) {
        this.update(this.value + step);
    }
    
    reset() {
        this.update(0);
    }
    
    complete() {
        this.update(100);
    }
}

// Result highlighter - highlight best results
function highlightBestResult() {
    const results = document.querySelectorAll('.result-item, .recommendation-item');
    if (results.length > 0) {
        results[0].style.border = '3px solid var(--success-color)';
        results[0].style.boxShadow = '0 0 20px rgba(72, 187, 120, 0.3)';
    }
}

// Auto-resize textarea
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Setup auto-resize for all textareas
document.addEventListener('DOMContentLoaded', () => {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', () => autoResizeTextarea(textarea));
    });
});

// Print/Export functionality
function printResults() {
    window.print();
}

// Statistics calculator
function calculateStatistics(scores) {
    if (scores.length === 0) return null;
    
    const sum = scores.reduce((a, b) => a + b, 0);
    const mean = sum / scores.length;
    const sorted = [...scores].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const max = Math.max(...scores);
    const min = Math.min(...scores);
    
    return { mean, median, max, min };
}

// Color interpolation for confidence levels
function getConfidenceColor(confidence) {
    // Red to Green gradient based on confidence
    if (confidence >= 80) return '#48bb78';
    if (confidence >= 60) return '#4299e1';
    if (confidence >= 40) return '#ed8936';
    return '#f56565';
}

// Initialize tooltips (if needed)
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = element.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = element.getBoundingClientRect();
            tooltip.style.position = 'absolute';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
            
            element._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', (e) => {
            if (element._tooltip) {
                element._tooltip.remove();
                element._tooltip = null;
            }
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTooltips();
    
    // Show welcome toast on home page
    if (window.location.pathname === '/') {
        setTimeout(() => {
            showToast('Welcome to Columnar Transposition Cipher System!', 'info');
        }, 500);
    }
});

// Performance monitoring (optional)
if (window.performance) {
    window.addEventListener('load', () => {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`Page load time: ${pageLoadTime}ms`);
    });
}

// Error boundary
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // Optionally show user-friendly error message
    showToast('An unexpected error occurred. Please refresh the page.', 'error');
});

// Service worker registration (for PWA support - optional)
if ('serviceWorker' in navigator) {
    // Can be enabled later for offline support
    // navigator.serviceWorker.register('/sw.js');
}

console.log('Columnar Transposition Cipher System loaded successfully!');
