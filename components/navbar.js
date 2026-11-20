/**
 * ClockEE OS 2.0 - Universal Master Navigation Bar
 * Apple Human Interface Design System + Matte Obsidian Architecture
 * The single source of truth across all 15+ ClockEE views.
 */

(function () {
  const NAV_LINKS = [
    { id: 'hud', label: 'HUD', href: 'index.html', icon: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>' },
    { id: 'timer', label: 'Focus Chamber', href: 'timer.html', icon: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>' },
    { id: 'today', label: 'Daily Practice', href: 'today.html', icon: '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>' },
    { id: 'task', label: 'Tasks & DPP', href: 'task.html', icon: '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>' },
    { id: 'cbt', label: 'NTA CBT Suite', href: 'cbt_home.html', icon: '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>' },
    { id: 'mistakes', label: 'Mistake Vault', href: 'cbt_mistakes.html', icon: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>' },
    { id: 'notebooks', label: 'Formula Vault', href: 'cbt_notebooks.html', icon: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>' },
    { id: 'tracker', label: '75 Syllabus', href: 'tracker.html', icon: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>' },
    { id: 'coaching', label: 'Coaching Matrix', href: 'coaching.html', icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>' },
    { id: 'live', label: 'Mesh Cockpit', href: 'live_tracker.html', icon: '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>' }
  ];

  function detectActiveId() {
    const path = window.location.pathname.toLowerCase();
    const explicit = document.body ? document.body.getAttribute('data-page') : null;
    if (explicit) return explicit;

    if (path.includes('cbt_exam') || path.includes('cbt_home') || path.includes('cbt_analysis') || path.includes('cbt_instructions')) return 'cbt';
    if (path.includes('cbt_mistakes')) return 'mistakes';
    if (path.includes('cbt_notebooks')) return 'notebooks';
    if (path.includes('live_tracker')) return 'live';
    if (path.includes('tracker')) return 'tracker';
    if (path.includes('timer')) return 'timer';
    if (path.includes('today')) return 'today';
    if (path.includes('task')) return 'task';
    if (path.includes('coaching')) return 'coaching';
    return 'hud';
  }

  function renderNavbar() {
    let mountPoint = document.getElementById('clockee-nav');
    if (!mountPoint) {
      mountPoint = document.createElement('div');
      mountPoint.id = 'clockee-nav';
      document.body.insertBefore(mountPoint, document.body.firstChild);
    }

    const activeId = detectActiveId();

    mountPoint.innerHTML = `
      <header class="bg-[#0a0c10]/90 border-b border-white/[0.08] sticky top-0 z-50 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between gap-3">
          
          <!-- Brand Mark -->
          <div class="flex items-center gap-3 flex-shrink-0">
            <a href="index.html" class="flex items-center gap-2.5 touch-target no-underline text-white group" title="ClockEE OS 2.0 Command Center">
              <div class="w-8 h-8 rounded-lg bg-white/[0.06] border border-white/[0.12] flex items-center justify-center font-bold text-white text-xs mono group-hover:border-blue-500/50 transition">
                CK
              </div>
              <div class="flex flex-col">
                <span class="text-sm font-bold tracking-tight text-white group-hover:text-blue-400 transition">ClockEE <span class="text-blue-400 font-mono text-xs">2.0</span></span>
                <span class="text-[9px] font-semibold text-slate-400 tracking-wider uppercase mono">Cognitive OS</span>
              </div>
            </a>
          </div>

          <!-- Main Desktop Nav Links -->
          <nav class="hidden md:flex items-center gap-1 overflow-x-auto py-1 scrollbar-none flex-nowrap" aria-label="Main Navigation">
            ${NAV_LINKS.map(link => {
              const isActive = link.id === activeId;
              return `
                <a 
                  href="${link.href}" 
                  class="shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.04] border border-transparent'
                  }"
                  ${isActive ? 'aria-current="page"' : ''}
                >
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${link.icon}</svg>
                  <span>${link.label}</span>
                </a>
              `;
            }).join('')}
          </nav>

          <!-- Right Status Telemetry & Controls -->
          <div class="flex items-center gap-2.5 flex-shrink-0">
            <!-- JEE Countdown Ticker -->
            <div class="hidden sm:flex items-center gap-2 px-3 py-1 rounded-lg bg-white/[0.03] border border-white/[0.08] text-xs font-medium min-h-[34px]">
              <span class="text-slate-500 font-mono text-[11px]">JEE '27:</span>
              <span id="nav-jee-ticker" class="text-amber-400 mono tabular-nums text-xs font-bold">Loading...</span>
            </div>

            <!-- Sync Indicator -->
            <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/[0.03] border border-white/[0.08] text-xs" title="Offline-First Sync Engine Active">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-slate-400 font-mono text-[10px] hidden lg:inline">SYNC</span>
            </div>

            <!-- Settings & Admin Quick Access -->
            <a href="settings.html" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition" title="User Settings & Aura">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            </a>

            <!-- Mobile Menu Toggle Button -->
            <button id="clockee-mobile-nav-toggle" class="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition" aria-label="Toggle Navigation">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
            </button>
          </div>

        </div>

        <!-- Mobile Drawer Menu -->
        <div id="clockee-mobile-drawer" class="hidden md:hidden border-t border-white/[0.08] bg-[#0a0c10] px-4 py-3 space-y-1">
          ${NAV_LINKS.map(link => {
            const isActive = link.id === activeId;
            return `
              <a 
                href="${link.href}" 
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold ${
                  isActive
                    ? 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                    : 'text-slate-300 hover:bg-white/[0.04]'
                }"
              >
                <svg class="w-4 h-4 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${link.icon}</svg>
                <span>${link.label}</span>
              </a>
            `;
          }).join('')}
        </div>
      </header>
    `;

    // Bind mobile menu toggle
    const toggleBtn = document.getElementById('clockee-mobile-nav-toggle');
    const drawer = document.getElementById('clockee-mobile-drawer');
    if (toggleBtn && drawer) {
      toggleBtn.addEventListener('click', () => {
        drawer.classList.toggle('hidden');
      });
    }

    initNavTicker();
  }

  function initNavTicker() {
    const tickerEl = document.getElementById('nav-jee-ticker');
    if (!tickerEl) return;

    // Target: JEE Main 2027 Session 1
    const targetDate = new Date('2027-01-24T09:00:00+05:30').getTime();

    function updateTicker() {
      const now = Date.now();
      const diff = targetDate - now;
      if (diff <= 0) {
        tickerEl.innerText = "EXAM DAY";
        return;
      }
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const mins = Math.floor((diff / (1000 * 60)) % 60);
      tickerEl.innerText = `${days}d ${hours}h ${mins}m`;
    }

    updateTicker();
    setInterval(updateTicker, 60000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderNavbar);
  } else {
    renderNavbar();
  }
})();
