/*
 * script.js
 *
 * This file contains client‑side enhancements for the book exchange
 * platform. It currently provides a small utility to auto‑dismiss
 * flash messages after a delay. Additional interactive features can
 * be added here (e.g. real‑time search filtering or AJAX requests).
 */

document.addEventListener('DOMContentLoaded', () => {
    // Automatically hide flash messages after 5 seconds
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => flash.remove(), 500);
        }, 5000);
    });
});