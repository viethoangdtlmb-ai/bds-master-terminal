document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.nav-item');
    const iframes = document.querySelectorAll('.app-frame');
    const moduleTitle = document.getElementById('module-title');
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

            // Update Title
            const title = item.querySelector('span').textContent;
            moduleTitle.textContent = title;

            // Switch active iframe visibility
            const targetId = item.getAttribute('data-target');
            
            // Hide current active iframe
            const currentActiveIframe = document.querySelector('.app-frame.active');
            if (currentActiveIframe) {
                currentActiveIframe.classList.remove('active');
            }
            
            // Show new target iframe
            document.getElementById(targetId).classList.add('active');
        });
    });
});

// Top bar actions
function refreshIframe() {
    const activeIframe = document.querySelector('.app-frame.active');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    loadingOverlay.classList.remove('hidden');
    
    // Reload only the active iframe
    activeIframe.src = activeIframe.src;
    
    // Remove loading overlay when this specific iframe finishes loading
    activeIframe.addEventListener('load', function handler() {
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 300);
        activeIframe.removeEventListener('load', handler);
    });
}

function openFullscreen() {
    const appContainer = document.querySelector('.app-container');
    
    if (!document.fullscreenElement) {
        if (appContainer.requestFullscreen) {
            appContainer.requestFullscreen();
        } else if (appContainer.webkitRequestFullscreen) { /* Safari */
            appContainer.webkitRequestFullscreen();
        } else if (appContainer.msRequestFullscreen) { /* IE11 */
            appContainer.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) { /* Safari */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE11 */
            document.msExitFullscreen();
        }
    }
}
