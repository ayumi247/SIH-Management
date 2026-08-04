async function loadComponent(elementId, componentPath) {
    try {
        const response = await fetch(componentPath);
        if (!response.ok) throw new Error(`Failed to load component: ${componentPath}`);
        const html = await response.text();
        
        const el = document.getElementById(elementId);
        if (el) {
            el.innerHTML = html;
            
            // Execute any scripts that might have been loaded
            const scripts = el.getElementsByTagName('script');
            for (let i = 0; i < scripts.length; i++) {
                eval(scripts[i].innerText);
            }
        }
    } catch (error) {
        console.error('UI Error:', error);
    }
}

function showToast(message, type = 'success') {
    // Simple toast notification implementation (can be expanded later)
    alert(message); 
}

document.addEventListener('DOMContentLoaded', () => {
    // --- Task 2: Mock function for triggering Error Shake ---
    window.triggerError = function() {
        const inputWrapper = document.querySelector('.input-border-expand');
        
        if (inputWrapper) {
            inputWrapper.classList.remove('input-error-shake');
            void inputWrapper.offsetWidth; 
            inputWrapper.classList.add('input-error-shake');
        }
    };

    // --- Task 3: Hide Telemetry Loader ---
    window.hideGlobalLoader = function() {
        const loader = document.getElementById('global-loader');
        if (loader) {
            loader.classList.add('is-hidden');
        }
    };
    
    window.showGlobalLoader = function() {
        const loader = document.getElementById('global-loader');
        if (loader) {
            loader.classList.remove('is-hidden');
        }
    }
});