/**
 * ClockEE OS 2.0 - Unified Master Navigation Bar
 * Standard across all ClockEE application views:
 * index.html, timer.html, today.html, task.html, coaching.html,
 * cbt_home.html, cbt_exam.html, cbt_mistakes.html, cbt_notebooks.html,
 * tracker.html, live_tracker.html
 *
 * Enforces:
 * - Apple HIG minimum 44x44px touch targets
 * - Strict Matte Obsidian Slate token hierarchy
 * - APCA-compliant contrast (#94a3b8 / #f8fafc)
 * - Monospace tabular countdown tickers
 */

(function () {
  const NAV_LINKS = [
    { id: 'hud', label: 'HUD', href: 'index.html' },
    { id: 'timer', label: 'Focus Chamber', href: 'timer.html' },
    { id: 'today', label: 'Daily Practice', href: 'today.html' },
    { id: 'task', label: 'Tasks & DPP', href: 'task.html' },
    { id: 'coaching', label: 'Coaching Matrix', href: 'coaching.html' },
    { id: 'cbt', label: 'NTA CBT Suite', href: 'cbt_home.html' },
    { id: 'mistakes', label: 'Mistake Vault', href: 'cbt_mistakes.html' },
    { id: 'notebooks', label: 'Formula Vault', href: 'cbt_notebooks.html' },
    { id: 'tracker', label: '75 Syllabus', href: 'tracker.html' },
    { id: 'live', label: 'Mesh Cockpit', href: 'live_tracker.html' }
  ];

  function detectActiveId() {
    const path = window.location.pathname.toLowerCase();
    const explicit = document.body.getAttribute('data-page');
    if (explicit) return explicit;

    if (path.includes('cbt_exam') || path.includes('cbt_home')) return 'cbt';
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
      <header class="bg-[#090d16] border-b border-slate-800/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between gap-3">
          
          <!-- Brand Mark -->
          <div class="flex items-center gap-3 flex-shrink-0">
            <a href="index.html" class="flex items-center gap-2.5 touch-target no-underline text-white group">
              <span class="w-8 h-8 rounded-lg bg-sky-500/20 border border-sky-500/40 flex items-center justify-center font-black text-sky-400 text-xs mono">
                CK
              </span>
              <div class="flex flex-col">
                <span class="text-sm font-extrabold tracking-tight text-white group-hover:text-sky-300 transition">ClockEE <span class="text-sky-400">2.0</span></span>
                <span class="text-[9px] font-bold text-slate-400 tracking-wider uppercase mono">JEE Cockpit</span>
              </div>
            </a>
          </div>

          <!-- Main Module Navigation Links (Horizontal Scroll on Mobile) -->
          <nav class="flex items-center gap-1 overflow-x-auto py-1 scrollbar-none" aria-label="Main Navigation">
            ${NAV_LINKS.map(link => {
              const isActive = link.id === activeId;
              return `
                <a 
                  href="${link.href}" 
                  class="touch-target px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-sky-500/20 text-sky-300 border border-sky-400/50 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent'
                  }"
                  ${isActive ? 'aria-current="page"' : ''}
                >
                  ${link.label}
                </a>
              `;
            }).join('')}
          </nav>

          <!-- Right Telemetry Strip & JEE Countdown -->
          <div class="hidden lg:flex items-center gap-3 flex-shrink-0">
            <!-- JEE Countdown Ticker -->
            <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold min-h-[44px]">
              <span class="text-slate-400">JEE '27:</span>
              <span id="nav-jee-ticker" class="text-amber-400 mono tabular-nums tabular">Loading...</span>
            </div>

            <!-- Offline-First DB Sync Beacon -->
            <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs min-h-[44px]" title="IndexedDB clockee_db v2 Storage Ready">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-slate-300 font-medium">IDB v2</span>
            </div>
          </div>

        </div>
      </header>
    `;

    initNavTicker();
  }

  function initNavTicker() {
    const tickerEl = document.getElementById('nav-jee-ticker');
    if (!tickerEl) return;

    // Target: JEE Main 2027 Session 1 (Approx Jan 24, 2027)
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
