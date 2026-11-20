/**
 * ClockEE OS 2.0 - Universal Master Navigation Bar
 * Apple Human Interface Design System + Matte Obsidian Architecture
 * Uncluttered top-level layout with organized dropdowns referencing v1.
 */

(function () {
  // Styles for the unified navbar and dropdown menus
  const NAV_CSS = `
    .nav-btn {
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.8125rem;
      font-weight: 500;
      color: #94a3b8;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      gap: 5px;
      text-decoration: none;
      white-space: nowrap;
      user-select: none;
    }
    .nav-btn:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.06);
    }
    .nav-active {
      background: #0a84ff !important;
      color: #ffffff !important;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .nav-dropdown {
      position: relative;
      display: inline-block;
    }
    .nav-caret {
      font-size: 0.65rem;
      margin-left: 2px;
      opacity: 0.7;
      display: inline-block;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .nav-dropdown:hover .nav-caret,
    .nav-dropdown:focus-within .nav-caret {
      transform: rotate(180deg);
    }
    .nav-dropdown-menu {
      position: absolute;
      top: 100%;
      left: 0;
      margin-top: 6px;
      min-width: 230px;
      background: rgba(10, 12, 18, 0.98);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 6px;
      display: none;
      flex-direction: column;
      gap: 2px;
      z-index: 100;
      box-shadow: 0 8px 12px -4px rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px) saturate(180%);
      animation: navDropdownFadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes navDropdownFadeIn {
      from { opacity: 0; transform: translateY(-4px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .nav-dropdown:hover .nav-dropdown-menu,
    .nav-dropdown:focus-within .nav-dropdown-menu {
      display: flex;
    }
    .nav-dropdown-item {
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.78rem;
      color: #94a3b8;
      text-decoration: none;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }
    .nav-dropdown-item:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.08);
      transform: translateX(2px);
    }
    .nav-icon-btn {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .nav-icon-btn:hover {
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.25);
      background: rgba(255, 255, 255, 0.1);
    }
    .hud-ring {
      border: 1.5px solid rgba(10, 132, 255, 0.6);
    }
  `;

  function injectStyles() {
    if (!document.getElementById('clockee-navbar-styles')) {
      const styleEl = document.createElement('style');
      styleEl.id = 'clockee-navbar-styles';
      styleEl.innerHTML = NAV_CSS;
      document.head.appendChild(styleEl);
    }
  }

  function detectActiveSection() {
    const path = window.location.pathname.toLowerCase();
    const explicit = document.body ? document.body.getAttribute('data-page') : null;
    if (explicit) return explicit;

    if (path.includes('task')) return 'task';
    if (path.includes('today')) return 'today';
    if (path.includes('timer')) return 'timer';
    if (path.includes('coaching')) return 'coaching';
    if (path.includes('cbt') || path.includes('mistakes') || path.includes('notebooks') || path.includes('reference')) return 'cbt';
    if (path.includes('inspiration')) return 'inspiration';
    if (path.includes('settings') || path.includes('admin') || path.includes('live_tracker') || path.includes('tracker')) return 'settings';
    return 'home';
  }

  function renderNavbar() {
    injectStyles();

    let mountPoint = document.getElementById('clockee-nav');
    if (!mountPoint) {
      mountPoint = document.createElement('div');
      mountPoint.id = 'clockee-nav';
      document.body.insertBefore(mountPoint, document.body.firstChild);
    }

    const activeSec = detectActiveSection();

    mountPoint.innerHTML = `
      <header class="sticky top-0 z-50 px-4 py-2.5 sm:px-6 transition-all duration-300 bg-[#080a14]/85 backdrop-blur-2xl border-b border-white/10 shadow-sm">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-2 sm:gap-4">
          
          <!-- Brand / Logo -->
          <div class="nav-left flex items-center gap-3 flex-shrink-0">
            <a href="index.html" class="flex items-center gap-2.5 cursor-pointer no-underline group" title="ClockEE Home Command Center">
              <div class="relative w-8 h-8 flex items-center justify-center rounded-xl bg-gradient-to-br from-[#0a84ff]/20 to-cyan-500/20 border border-white/15 group-hover:border-blue-400/50 transition">
                <svg class="w-4 h-4 text-cyan-400 animate-spin-slow" viewBox="0 0 64 64" fill="none">
                  <circle cx="32" cy="32" r="28" stroke="url(#navLogoGrad)" stroke-width="4" stroke-dasharray="6 6"/>
                  <path d="M32 16V32L42 42" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
                  <circle cx="32" cy="32" r="4" fill="#38bdf8"/>
                  <defs>
                    <linearGradient id="navLogoGrad" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                      <stop stop-color="#38bdf8"/>
                      <stop offset="0.5" stop-color="#818cf8"/>
                      <stop offset="1" stop-color="#c084fc"/>
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <span class="text-base sm:text-lg font-bold tracking-tight text-white flex items-center">
                ClockEE
                <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#161b24] text-[#0a84ff] border border-white/10 font-bold ml-1.5">v2.0</span>
              </span>
            </a>
          </div>

          <!-- Center Nav Links with Dropdowns (Clean v1 Layout) -->
          <nav class="hidden md:flex items-center gap-1 sm:gap-1.5" id="main-nav" aria-label="Master Navigation">
            <a href="index.html" class="nav-btn ${activeSec === 'home' ? 'nav-active' : ''}">Home</a>
            <a href="task.html" class="nav-btn ${activeSec === 'task' ? 'nav-active' : ''}">Task</a>
            <a href="today.html" class="nav-btn ${activeSec === 'today' ? 'nav-active' : ''}">Today</a>

            <!-- Timer Dropdown -->
            <div class="nav-dropdown">
              <a href="timer.html" class="nav-btn ${activeSec === 'timer' ? 'nav-active' : ''}">
                <span>Timer</span> <span class="nav-caret">▼</span>
              </a>
              <div class="nav-dropdown-menu">
                <a href="timer.html?mode=drill" class="nav-dropdown-item group">
                  <div class="w-6 h-6 rounded-md bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-105 transition">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                  </div>
                  <div>
                    <div class="font-bold text-white group-hover:text-cyan-300 transition text-xs flex items-center gap-1.5">
                      <span>Tactical Pace Sprint</span>
                      <span class="text-[9px] px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 border border-cyan-500/30 font-mono">NEW</span>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono">Pace benchmark &amp; lap latency</div>
                  </div>
                </a>
                <a href="timer.html?mode=lecture" class="nav-dropdown-item group">
                  <div class="w-6 h-6 rounded-md bg-[#0a84ff]/15 border border-white/10 flex items-center justify-center text-[#0a84ff] group-hover:scale-105 transition">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  </div>
                  <div>
                    <div class="font-bold text-white group-hover:text-blue-300 transition text-xs">Lecture Focus Timer</div>
                    <div class="text-[10px] text-slate-400 font-mono">Dual-screen &amp; mini timer HUD</div>
                  </div>
                </a>
              </div>
            </div>

            <!-- Coaching Dropdown -->
            <div class="nav-dropdown">
              <a href="coaching.html" class="nav-btn ${activeSec === 'coaching' ? 'nav-active' : ''}">
                <span>Coaching</span> <span class="nav-caret">▼</span>
              </a>
              <div class="nav-dropdown-menu">
                <a href="coaching.html?sub=syllabus" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                  <span>Syllabus Covered</span>
                </a>
                <a href="coaching.html?sub=tests" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                  <span>Test Performance &amp; OCR</span>
                </a>
                <a href="coaching.html?sub=logs" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 12h6"/><path d="M9 16h6"/></svg>
                  <span>Personal Question Log</span>
                </a>
              </div>
            </div>

            <!-- CBT Portal Dropdown (Hiding excess CBT views) -->
            <div class="nav-dropdown">
              <a href="cbt_home.html" class="nav-btn ${activeSec === 'cbt' ? 'nav-active' : ''} text-cyan-300">
                <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                <span>CBT Portal</span> <span class="nav-caret">▼</span>
              </a>
              <div class="nav-dropdown-menu">
                <a href="cbt_home.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
                  <span>NTA Mock Exam Lobby</span>
                </a>
                <a href="cbt_exam.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  <span>Live Exam Chamber</span>
                </a>
                <a href="cbt_analysis.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                  <span>7-Pillar Performance Analysis</span>
                </a>
                <a href="cbt_mistakes.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                  <span>Mistake Autopsy Vault</span>
                </a>
                <a href="cbt_notebooks.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                  <span>Formula &amp; Method Notebooks</span>
                </a>
                <a href="cbt_reference_vault.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                  <span>Official Exam Paper Vault</span>
                </a>
              </div>
            </div>

            <!-- Inspiration Board -->
            <a href="inspiration.html" class="nav-btn ${activeSec === 'inspiration' ? 'nav-active' : ''} text-amber-300 hover:text-amber-200" title="Dream Vision & Inspiration Board">
              <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
              <span>Inspiration</span>
            </a>

            <!-- Settings / More Dropdown -->
            <div class="nav-dropdown">
              <a href="settings.html" class="nav-btn ${activeSec === 'settings' ? 'nav-active' : ''}">
                <span>Settings</span> <span class="nav-caret">▼</span>
              </a>
              <div class="nav-dropdown-menu">
                <a href="settings.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                  <span>Global Settings</span>
                </a>
                <a href="settings.html#sec-identity" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-[#0a84ff]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  <span>Profile &amp; Identity</span>
                </a>
                <a href="settings.html#sec-aura" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/></svg>
                  <span>Themes &amp; Background</span>
                </a>
                <a href="settings.html#sec-goals" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                  <span>JEE Examination Goals</span>
                </a>
                <a href="tracker.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                  <span>75-Chapter Syllabus Matrix</span>
                </a>
                <a href="live_tracker.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
                  <span>Mesh Cockpit &amp; Cloud Telemetry</span>
                </a>
                <a href="settings.html#sec-apis" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  <span>Connected APIs</span>
                </a>
                <a href="settings.html#sec-data" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                  <span>Data Backup &amp; Reset</span>
                </a>
                <a href="admin.html" class="nav-dropdown-item">
                  <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  <span>Admin Cockpit</span>
                </a>
              </div>
            </div>
          </nav>

          <!-- Right Status Telemetry & Quick Action Controls -->
          <div class="nav-right flex items-center gap-2 sm:gap-3 flex-shrink-0">
            <!-- Live Edge Connection Status Pill -->
            <a href="live_tracker.html" id="edge-connection-pill" class="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/40 text-[11px] font-mono font-bold text-emerald-400 hover:border-emerald-400 transition" title="Connected to Vercel Edge &amp; Supabase Cloud Mesh">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>EDGE LIVE</span>
            </a>

            <!-- Tour Launcher -->
            <button id="btnNavTourCockpit" class="hidden md:inline-flex px-2.5 py-1 rounded-full bg-cyan-950/80 border border-cyan-400/50 text-cyan-300 hover:bg-cyan-900 text-xs font-black items-center gap-1.5 transition cursor-pointer" onclick="window.showCockpitTourMenu ? window.showCockpitTourMenu() : alert('Tour initialized')" title="Open Interactive Cockpit Tour Menu">
              <span class="animate-pulse">🚀</span>
              <span>Tour</span>
            </button>

            <!-- Focus Drawer Toggle Button -->
            <button class="nav-icon-btn hover:border-cyan-400 hover:text-cyan-300 min-h-[34px] min-w-[34px]" title="Toggle Focus Drawer (Split Panel)" onclick="window.toggleSplitScreen ? window.toggleSplitScreen() : (function(){ var d = document.getElementById('split-drawer'); if (d) d.classList.toggle('translate-x-full'); })()">⊟</button>

            <!-- Commander Avatar with Glowing Ring -->
            <a href="settings.html" class="relative p-[2px] rounded-full hud-ring cursor-pointer inline-block" title="Commander Profile &amp; Settings">
              <img
                class="w-8 h-8 rounded-full bg-[#070913] object-cover block cursor-pointer border border-white/20"
                data-profile-avatar
                id="navAvatarImg"
                src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant"
                alt="Avatar"
              />
            </a>

            <!-- Mobile Menu Toggle Button -->
            <button id="clockee-mobile-nav-toggle" class="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition" aria-label="Toggle Navigation">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
            </button>
          </div>

        </div>

        <!-- Mobile Drawer Menu (Hierarchical Accordions) -->
        <div id="clockee-mobile-drawer" class="hidden md:hidden border-t border-white/10 bg-[#090b14] px-4 py-3 space-y-1.5 max-h-[80vh] overflow-y-auto">
          <a href="index.html" class="block px-3 py-2 rounded-lg text-xs font-semibold ${activeSec === 'home' ? 'bg-[#0a84ff] text-white' : 'text-slate-300 hover:bg-white/5'}">Home Command Center</a>
          <a href="task.html" class="block px-3 py-2 rounded-lg text-xs font-semibold ${activeSec === 'task' ? 'bg-[#0a84ff] text-white' : 'text-slate-300 hover:bg-white/5'}">Tasks &amp; DPP Kanban</a>
          <a href="today.html" class="block px-3 py-2 rounded-lg text-xs font-semibold ${activeSec === 'today' ? 'bg-[#0a84ff] text-white' : 'text-slate-300 hover:bg-white/5'}">Daily Practice Log</a>
          
          <div class="pt-2 border-t border-white/10 text-[10px] font-mono uppercase text-slate-500 font-bold px-3">Timer Modes</div>
          <a href="timer.html?mode=drill" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">Tactical Pace Sprint</a>
          <a href="timer.html?mode=lecture" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">Lecture Focus Timer</a>

          <div class="pt-2 border-t border-white/10 text-[10px] font-mono uppercase text-slate-500 font-bold px-3">CBT Mock Suite</div>
          <a href="cbt_home.html" class="block px-3 py-1.5 rounded-lg text-xs text-cyan-400 hover:bg-white/5">NTA Mock Exam Lobby</a>
          <a href="cbt_exam.html" class="block px-3 py-1.5 rounded-lg text-xs text-emerald-400 hover:bg-white/5">Live Exam Chamber</a>
          <a href="cbt_analysis.html" class="block px-3 py-1.5 rounded-lg text-xs text-blue-400 hover:bg-white/5">7-Pillar Performance Analysis</a>
          <a href="cbt_mistakes.html" class="block px-3 py-1.5 rounded-lg text-xs text-red-400 hover:bg-white/5">Mistake Autopsy Vault</a>
          <a href="cbt_notebooks.html" class="block px-3 py-1.5 rounded-lg text-xs text-purple-400 hover:bg-white/5">Formula Notebooks</a>

          <div class="pt-2 border-t border-white/10 text-[10px] font-mono uppercase text-slate-500 font-bold px-3">Coaching &amp; Syllabus</div>
          <a href="coaching.html?sub=syllabus" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">Syllabus Covered</a>
          <a href="coaching.html?sub=tests" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">Test Performance</a>
          <a href="tracker.html" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">75-Chapter Syllabus Matrix</a>
          <a href="inspiration.html" class="block px-3 py-1.5 rounded-lg text-xs text-amber-300 hover:bg-white/5">Inspiration Board</a>
          <a href="settings.html" class="block px-3 py-1.5 rounded-lg text-xs text-slate-300 hover:bg-white/5">Settings &amp; Backup</a>
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

    // Auto-sync avatar from local state
    if (window.getState) {
      try {
        const s = window.getState();
        const av = document.getElementById('navAvatarImg');
        if (av && s.profile && s.profile.avatar) {
          av.src = s.profile.avatar;
        }
      } catch (e) {}
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderNavbar);
  } else {
    renderNavbar();
  }
})();
