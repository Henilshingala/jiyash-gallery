/* ═══════════════════════════════════════════════════════════
   JIYA & SHAILESH GALLERY — Main JavaScript
═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar scroll effect ──────────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const updateNav = () => {
      navbar.style.background = window.scrollY > 60
        ? 'rgba(13,13,15,0.97)'
        : 'rgba(13,13,15,0.85)';
    };
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }

  // ── Mobile nav toggle ─────────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMobile = document.getElementById('navMobile');
  if (navToggle && navMobile) {
    navToggle.addEventListener('click', () => {
      navMobile.classList.toggle('open');
    });
  }

  // ── Intersection Observer: fade-in elements ───────────
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    fadeEls.forEach(el => {
      el.style.animationPlayState = 'paused';
      obs.observe(el);
    });
  }

  // ── Auto-dismiss messages ─────────────────────────────
  const alerts = document.querySelectorAll('.dash-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

});
