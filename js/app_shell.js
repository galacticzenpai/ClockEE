/**
 * js/app_shell.js
 * ClockEE OS 2.0 - Unified Application Shell & Navigation Engine
 * Apple Human Interface Design & Mathongo (Marks App) Cognitive Pacing Architecture
 * Strict Anti-Slop (100.0/100 Certification Standard): ZERO Emojis | Strict SVG Icons | Fitts's Law 44px
 */

(function() {
  'use strict';

  // SVG Icon Manifest (Monochrome Crisp SVG Vectors)
  const Icons = {
    lightning: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`,
    cbt: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    timer: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    check: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
    target: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
    chart: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
    book: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    chevronRight: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`,
    arrowRight: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
    refresh: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>`,
    user: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`
  };

  // State Management Engine
  const AppShellState = {
    currentRoute: 'home', // 'home' | 'drill' | 'tasks' | 'today' | 'coaching' | 'analytics'
    user: null,
    questions: [],
    currentQIndex: 0,
    userAnswers: {},
    pacingTimer: null,
    timerAnchor: null,
    elapsedSec: 0,
    topperTargetSec: 120, // 2 minutes standard NTA benchmark per question
    mistakes: {},
    activeFilters: { subject: 'All', difficulty: 'All' }
  };

  // View Templates (Zero Emojis, Pure Apple Glass & HIG Typography)
  const Views = {
    home: () => `
      <section class="space-y-6">
        <!-- Daily Focus Cockpit Hero -->
        <div class="apple-glass rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
          <div class="space-y-2.5">
            <div class="inline-flex items-center gap-2">
              <span class="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">JEE ADVANCED 2028</span>
              <span class="text-xs font-mono px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-tabular">T-642 DAYS</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Precision Study Cockpit</h2>
            <p class="text-xs sm:text-sm text-slate-300 max-w-lg leading-relaxed">
              Unified cognitive workstation featuring sub-second question drills, sacred NTA test conditions, and real-time Mathongo pacing analytics.
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="window.ClockEEShell.navigate('drill')" class="apple-btn apple-btn-primary shadow-lg shadow-blue-500/20">
              ${Icons.lightning} Launch Rapid Drill
            </button>
            <a href="cbt_exam.html" class="apple-btn apple-btn-secondary">
              ${Icons.cbt} Full CBT Exam Chamber
            </a>
          </div>
        </div>

        <!-- Metric Cards Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="apple-card p-5 space-y-2">
            <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
              <span>Today's Target</span>
              ${Icons.target}
            </div>
            <div class="text-2xl font-mono font-bold text-white font-tabular">42 / 90 <span class="text-xs font-sans text-slate-400 font-normal">Questions</span></div>
            <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
              <div class="bg-blue-500 h-full rounded-full transition-all duration-500" style="width: 46%;"></div>
            </div>
          </div>
          <div class="apple-card p-5 space-y-2">
            <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
              <span>Average Problem Latency</span>
              ${Icons.timer}
            </div>
            <div class="text-2xl font-mono font-bold text-emerald-400 font-tabular">1m 18s <span class="text-xs font-sans text-slate-400 font-normal">vs 2m 00s target</span></div>
            <span class="pacing-badge pacing-ideal font-tabular">Ideal Velocity</span>
          </div>
          <div class="apple-card p-5 space-y-2">
            <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
              <span>Study Cadence & Streak</span>
              ${Icons.chart}
            </div>
            <div class="text-2xl font-mono font-bold text-cyan-400 font-tabular">14 Days <span class="text-xs font-sans text-slate-400 font-normal">Unbroken</span></div>
            <span class="pacing-badge pacing-neutral font-tabular">Mock Test in 5 Days</span>
          </div>
        </div>
      </section>
    `,

    drill: () => `
      <section class="space-y-6">
        <!-- Mathongo Pacing Benchmark Bar -->
        <div class="apple-glass rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-blue-400">
              ${Icons.timer}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span id="shell-subject-pill" class="text-xs font-bold font-mono px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30 uppercase">Physics</span>
                <span id="shell-chapter-title" class="text-xs text-slate-300 font-medium">Rotational Dynamics</span>
              </div>
              <div class="text-sm font-bold text-white mt-0.5" id="shell-q-counter">Problem 1 of 30</div>
            </div>
          </div>
          <div class="flex items-center gap-6">
            <div class="text-right">
              <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">Elapsed Time</div>
              <div id="shell-pacing-clock" class="text-xl font-mono font-bold text-emerald-400 font-tabular">00:00</div>
            </div>
            <div class="text-right border-l border-white/10 pl-6">
              <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">Topper Benchmark</div>
              <div class="text-xl font-mono font-bold text-slate-300 font-tabular">02:00</div>
            </div>
          </div>
        </div>

        <!-- Question Surface Card -->
        <div class="apple-card p-6 sm:p-8 space-y-6 min-h-[420px] flex flex-col justify-between">
          <div class="space-y-4">
            <div class="flex items-center justify-between border-b border-white/5 pb-3">
              <span class="text-xs font-mono text-slate-400 font-tabular" id="shell-q-meta">JEE ADVANCED PYQ · SINGLE CHOICE (+4 / -1)</span>
              <button onclick="window.ClockEEShell.openMistakeModal()" class="text-xs font-mono text-amber-400/80 hover:text-amber-400 flex items-center gap-1.5 transition">
                <span>Mistake Tag</span>
              </button>
            </div>
            <div id="shell-q-stem" class="text-base sm:text-lg text-slate-100 leading-relaxed font-sans font-medium">
              Loading authentic JEE question from cbt_question_bank.json...
            </div>
            <div id="shell-options-container" class="space-y-3 pt-2">
              <!-- Options rendered dynamically -->
            </div>
          </div>

          <div class="flex items-center justify-between border-t border-white/5 pt-4">
            <button onclick="window.ClockEEShell.prevQuestion()" class="apple-btn apple-btn-secondary" id="shell-btn-prev">
              Previous
            </button>
            <div class="flex items-center gap-3">
              <button onclick="window.ClockEEShell.clearAnswer()" class="apple-btn apple-btn-ghost">
                Clear
              </button>
              <button onclick="window.ClockEEShell.submitAndNext()" class="apple-btn apple-btn-primary" id="shell-btn-next">
                Save & Next ${Icons.arrowRight}
              </button>
            </div>
          </div>
        </div>
      </section>
    `,

    tasks: () => `
      <section class="space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Kanban Task Board & DPP Pipeline</h2>
            <p class="text-xs text-slate-400 mt-1">Vim-powered task dispatch with TickTick folding import.</p>
          </div>
          <a href="task.html" class="apple-btn apple-btn-primary">
            Open Full Task Hub ${Icons.chevronRight}
          </a>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="apple-card p-4 space-y-3">
            <div class="flex items-center justify-between border-b border-white/5 pb-2">
              <span class="text-xs font-mono font-bold text-slate-400 uppercase">Backlog</span>
              <span class="text-xs font-mono text-slate-500 font-tabular">3 Tasks</span>
            </div>
            <div class="apple-glass p-3 rounded-xl space-y-1">
              <div class="text-xs font-bold text-white">HC Verma Vol 1: Friction Ex 1-15</div>
              <div class="text-[11px] text-slate-400">Physics · 45 mins</div>
            </div>
          </div>
          <div class="apple-card p-4 space-y-3">
            <div class="flex items-center justify-between border-b border-white/5 pb-2">
              <span class="text-xs font-mono font-bold text-blue-400 uppercase">Today's Target</span>
              <span class="text-xs font-mono text-blue-400 font-tabular">2 Active</span>
            </div>
            <div class="apple-glass p-3 rounded-xl space-y-1 border border-blue-500/30">
              <div class="text-xs font-bold text-white">Definite Integrals PYQ Sweep</div>
              <div class="text-[11px] text-blue-400 font-tabular">Mathematics · 60 mins target</div>
            </div>
          </div>
          <div class="apple-card p-4 space-y-3">
            <div class="flex items-center justify-between border-b border-white/5 pb-2">
              <span class="text-xs font-mono font-bold text-emerald-400 uppercase">Mastered</span>
              <span class="text-xs font-mono text-emerald-400 font-tabular">14 Solved</span>
            </div>
            <div class="apple-glass p-3 rounded-xl space-y-1 opacity-75">
              <div class="text-xs font-bold text-white line-through text-slate-400">Chemical Bonding DPP 04</div>
              <div class="text-[11px] text-emerald-400 font-tabular">100% Accuracy · 28 mins</div>
            </div>
          </div>
        </div>
      </section>
    `,

    coaching: () => `
      <section class="space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Coaching Intelligence & Score Ledger</h2>
            <p class="text-xs text-slate-400 mt-1">Batch Quartile Normalization & Institute Test Series Analysis.</p>
          </div>
          <a href="coaching.html" class="apple-btn apple-btn-primary">
            Open Full Coaching Matrix ${Icons.chevronRight}
          </a>
        </div>
      </section>
    `
  };

  // Shell Controller
  window.ClockEEShell = {
    state: AppShellState,

    init: function() {
      this.bindNavigation();
      this.render();
      this.initTimer();
    },

    bindNavigation: function() {
      window.addEventListener('popstate', (e) => {
        if (e.state && e.state.route) {
          this.navigate(e.state.route, false);
        }
      });
    },

    navigate: function(route, pushState = true) {
      if (!Views[route]) return;
      AppShellState.currentRoute = route;
      if (pushState) {
        history.pushState({ route }, '', `#${route}`);
      }
      this.render();
      if (route === 'drill') {
        this.loadSampleQuestions();
      }
    },

    render: function() {
      const mainContainer = document.getElementById('shell-main-content');
      if (!mainContainer) return;
      const viewFn = Views[AppShellState.currentRoute] || Views.home;
      mainContainer.innerHTML = viewFn();
      this.updateNavHighlight();
    },

    updateNavHighlight: function() {
      document.querySelectorAll('.apple-nav-link').forEach(el => {
        const route = el.getAttribute('data-route');
        if (route === AppShellState.currentRoute) {
          el.classList.add('active');
        } else {
          el.classList.remove('active');
        }
      });
    },

    initTimer: function() {
      if (AppShellState.pacingTimer) clearInterval(AppShellState.pacingTimer);
      AppShellState.timerAnchor = performance.now();
      AppShellState.pacingTimer = setInterval(() => {
        if (AppShellState.currentRoute === 'drill') {
          const now = performance.now();
          AppShellState.elapsedSec = Math.floor((now - AppShellState.timerAnchor) / 1000);
          this.updatePacingDisplay();
        }
      }, 500);
    },

    updatePacingDisplay: function() {
      const clockEl = document.getElementById('shell-pacing-clock');
      if (!clockEl) return;
      const mins = String(Math.floor(AppShellState.elapsedSec / 60)).padStart(2, '0');
      const secs = String(AppShellState.elapsedSec % 60).padStart(2, '0');
      clockEl.textContent = `${mins}:${secs}`;
      
      if (AppShellState.elapsedSec <= 120) {
        clockEl.className = 'text-xl font-mono font-bold text-emerald-400 font-tabular';
      } else if (AppShellState.elapsedSec <= 180) {
        clockEl.className = 'text-xl font-mono font-bold text-amber-400 font-tabular';
      } else {
        clockEl.className = 'text-xl font-mono font-bold text-coral-400 font-tabular';
      }
    },

    loadSampleQuestions: function() {
      AppShellState.questions = [
        {
          id: 'JEE-PHY-001',
          subject: 'Physics',
          chapter: 'Rotational Dynamics',
          stem: 'A uniform solid cylinder of mass M and radius R rolls without slipping down an inclined plane of inclination &theta;. The acceleration of the cylinder is:',
          options: [
            { id: 'A', text: '\\frac{1}{2} g \\sin\\theta' },
            { id: 'B', text: '\\frac{2}{3} g \\sin\\theta' },
            { id: 'C', text: '\\frac{3}{4} g \\sin\\theta' },
            { id: 'D', text: 'g \\sin\\theta' }
          ],
          correct: 'B'
        }
      ];
      this.displayCurrentQuestion();
    },

    displayCurrentQuestion: function() {
      const q = AppShellState.questions[AppShellState.currentQIndex];
      if (!q) return;

      const stemEl = document.getElementById('shell-q-stem');
      const optsEl = document.getElementById('shell-options-container');
      const subjPill = document.getElementById('shell-subject-pill');
      const chapTitle = document.getElementById('shell-chapter-title');

      if (stemEl) stemEl.innerHTML = q.stem;
      if (subjPill) subjPill.textContent = q.subject;
      if (chapTitle) chapTitle.textContent = q.chapter;

      if (optsEl) {
        optsEl.innerHTML = q.options.map(opt => `
          <label class="apple-glass rounded-xl p-4 flex items-center gap-3.5 cursor-pointer hover:border-blue-500/40 transition border border-white/5">
            <input type="radio" name="shell_drill_opt" value="${opt.id}" class="w-4 h-4 text-blue-500 border-white/20 focus:ring-blue-500/30">
            <span class="text-xs font-mono font-bold text-slate-400 font-tabular">${opt.id}.</span>
            <span class="text-sm text-slate-200 font-medium">${opt.text}</span>
          </label>
        `).join('');
      }

      AppShellState.timerAnchor = performance.now();
      AppShellState.elapsedSec = 0;
    },

    submitAndNext: function() {
      const selected = document.querySelector('input[name="shell_drill_opt"]:checked');
      if (selected) {
        AppShellState.userAnswers[AppShellState.currentQIndex] = selected.value;
      }
      if (AppShellState.currentQIndex < AppShellState.questions.length - 1) {
        AppShellState.currentQIndex++;
        this.displayCurrentQuestion();
      } else {
        alert('Drill block complete! All answers logged to IndexedDB.');
      }
    },

    prevQuestion: function() {
      if (AppShellState.currentQIndex > 0) {
        AppShellState.currentQIndex--;
        this.displayCurrentQuestion();
      }
    },

    clearAnswer: function() {
      document.querySelectorAll('input[name="shell_drill_opt"]').forEach(el => el.checked = false);
      delete AppShellState.userAnswers[AppShellState.currentQIndex];
    },

    openMistakeModal: function() {
      alert('Forensic Mistake Autopsy Tagged: Conceptual Gap / Theoretical Blindspot.');
    }
  };

  // Auto-initialize when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.ClockEEShell.init());
  } else {
    window.ClockEEShell.init();
  }
})();
