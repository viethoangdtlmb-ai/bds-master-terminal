document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.nav-item');
    const iframes = document.querySelectorAll('.app-frame');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Remove loading overlay after initial load
    window.addEventListener('load', () => {
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 800); // Give iframes some time to render initially
    });

    // Navigation logic
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Avoid doing anything if already active
            if (item.classList.contains('active')) return;

            // Update Active Nav Class
            document.querySelector('.nav-item.active').classList.remove('active');
            item.classList.add('active');



            // Switch active iframe visibility
            const targetId = item.getAttribute('data-target');
            
            // Hide current active iframe
            const currentActiveIframe = document.querySelector('.app-frame.active');
            if (currentActiveIframe) {
                currentActiveIframe.classList.remove('active');
            }
            
            // Show new target iframe and implement Lazy Loading
            const targetIframe = document.getElementById(targetId);
            
            // If the iframe hasn't been loaded yet (has data-src but no src)
            const dataSrc = targetIframe.getAttribute('data-src');
            if (dataSrc) {
                loadingOverlay.classList.remove('hidden');
                targetIframe.src = dataSrc; // Start loading
                targetIframe.removeAttribute('data-src'); // Remove so it doesn't trigger again
                
                targetIframe.addEventListener('load', function handler() {
                    setTimeout(() => {
                        loadingOverlay.classList.add('hidden');
                    }, 400);
                    targetIframe.removeEventListener('load', handler);
                });
            }
            
            targetIframe.classList.add('active');
        });
    });
});

