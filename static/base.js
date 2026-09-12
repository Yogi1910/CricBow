// base.js

document.addEventListener('DOMContentLoaded', () => {
    // Execute this code when the DOM is fully loaded

    // Feature box hover effect
    const featureBoxes = document.querySelectorAll('.feature-box');

    featureBoxes.forEach(box => {
        box.addEventListener('mouseenter', () => {
            box.classList.add('hovered');
        });

        box.addEventListener('mouseleave', () => {
            box.classList.remove('hovered');
        });
    });

    // Smooth scroll to sections
    const scrollTo = (target) => {
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    };

    const ctaButton = document.querySelector('.cta-button');
    ctaButton.addEventListener('click', event => {
        event.preventDefault();
        scrollTo(document.querySelector('.section-target')); // Replace with the actual target section's selector
    });

    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mobileNavMenu = document.querySelector('.mobile-nav-menu');

    mobileNavToggle.addEventListener('click', () => {
        mobileNavMenu.classList.toggle('open');
    });
    
    // Close mobile navigation on link click
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-menu a');

    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileNavMenu.classList.remove('open');
        });
    });
});
