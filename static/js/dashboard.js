/* ═══════════════════════════════════════════════════════════
   LUMINARY GALLERY — Dashboard JavaScript
═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sidebar mobile toggle ─────────────────────────────
  const sidebar    = document.getElementById('sidebar');
  const sidebarOpen  = document.getElementById('sidebarOpen');
  const sidebarClose = document.getElementById('sidebarClose');

  if (sidebarOpen && sidebar) {
    sidebarOpen.addEventListener('click', () => sidebar.classList.add('open'));
  }
  if (sidebarClose && sidebar) {
    sidebarClose.addEventListener('click', () => sidebar.classList.remove('open'));
  }

  // Close sidebar on outside click (mobile)
  document.addEventListener('click', e => {
    if (sidebar && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && !sidebarOpen?.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    }
  });

  // ── Auto-dismiss alerts ───────────────────────────────
  document.querySelectorAll('.dash-alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease, max-height 0.5s ease';
      alert.style.opacity = '0';
      alert.style.maxHeight = '0';
      alert.style.overflow = 'hidden';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

});
