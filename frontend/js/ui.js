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