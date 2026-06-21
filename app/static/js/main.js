document.addEventListener('DOMContentLoaded', function() {
    // Add 'reveal' class to main content elements for scroll animation
    const elementsToReveal = document.querySelectorAll('.card, .table-responsive, .alert');
    elementsToReveal.forEach(el => {
        el.classList.add('reveal');
    });

    // Sidebar active state logic based on current URL
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('#sidebar ul li a');
    
    sidebarLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.parentElement.classList.add('active');
        }
    });
});
