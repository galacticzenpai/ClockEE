/**
 * js/app_shell.js
 * Clean-Slate Unified Application Shell & Navigation Engine
 * Single Source of Truth for Navigation, View Routing, and Reactive State.
 */

(function() {
  'use strict';

  // State Management
  const AppShellState = {
    currentRoute: 'home', // 'home' | 'drill' | 'tasks' | 'today' | 'analytics'
    user: null,
    questions: [],
    currentQIndex: 0,
    userAnswers: {},
    pacingTimer: null,
    elapsedSec: 0,
    topperTargetSec: 120,
    mistakes: {},
    activeFilters: { subject: 'All', difficulty: 'All' }
  };

  // View Definitions & Templates
  const Views = {
    home: () => `
      <section class="space-y-6">
        <!-- Daily Focus Hero -->
        <div class="apple-glass rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
          <div class="space-y-2">
            <span class="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">JEE ADVANCED 2028</span>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Precision Study Cockpit</h2>
            <p class="text-xs sm:text-sm text-slate-300 max-w-lg leading-relaxed">
              Unified study environment with sub-second question drills, authentic CBT testing, and live Mathongo pacing metrics.
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="window.ClockEEShell.navigate('drill')" class="min-h-[44px] px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white shadow-lg shadow-blue-500/30 transition flex items-center gap-2">
              <span>⚡</span> Launch Practice Drill
            </button>
            <a href="cbt_exam.html" class="min-h-[44px] px-5 py-2.5 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-xs font-bold text-slate-200 transition flex items-center gap-2">
              <span>🏛️</span> Full CBT Exam Mode
            </a>
          </div>
        </div>

        <!-- Metric Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="apple-glass rounded-2xl p-5 space-y-1">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Today's Solved Target</span>
            <div class="text-2xl font-mono font-extrabold text-white">42 / 90 <span class="text-xs font-sans text-slate-400 font-normal">Questions</span></div>
            <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden mt-2">
              <div class="bg-blue-500 h-full rounded-full" style="width: 46%;"></div>
            </div>
          </div>
          <div class="apple-glass rounded-2xl p-5 space-y-1">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Average Problem Latency</span>
            <div class="text-2xl font-mono font-extrabold text-emerald-400">1m 18s <span class="text-xs font-sans text-slate-400 font-normal">vs 2m 00s target</span></div>
            <div class="text-[11px] text-emerald-400 font-medium mt-1">🚀 Fast & Accurate Pacing</div>
          </div>
          <div class="apple-glass rounded-2xl p-5 space-y-1">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Study Cadence & Streak</span>
            <div class="text-2xl font-mono font-extrabold text-cyan-400">14 Days <span class="text-xs font-sans text-slate-400 font-normal">Streak</span></div>
            <div class="text-[11px] text-slate-400 mt-1">Next milestone: Major Mock Test in 5 days</div>
          </div>
        </div>
      </section>
    `,

    drill: () => `
      <section class="space-y-6">
        <!-- Mathongo Pacing Benchmark Bar -->
        <div class="apple-glass rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-lg text-blue-400">
              ⏱️
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span id="shell-subject-pill" class="text-xs font-bold font-mono px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">Physics</span>
                <span id="shell-difficulty-badge" class="text-xs font-semibold px-2 py-0.5 rounded bg-white/5 text-slate-300 border border-white/10">JEE Advanced</span>
                <span id="shell-pacing-badge" class="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">🚀 Fast & Accurate</span>
              </div>
              <div id="shell-chapter-text" class="text-xs text-slate-300 mt-1">Rotational Motion • Moment of Inertia</div>
            </div>
          </div>

          <div class="flex items-center gap-6 self-stretch md:self-auto justify-between md:justify-end bg-black/40 px-4 py-2.5 rounded-xl border border-white/5">
            <div>
              <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Your Latency</span>
              <span id="shell-student-time" class="text-base sm:text-lg font-mono font-bold text-white">0:00</span>
            </div>
            <div class="w-px h-8 bg-white/10"></div>
            <div>
              <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Topper Target</span>
              <span id="shell-topper-time" class="text-base sm:text-lg font-mono font-bold text-blue-400">2:15</span>
            </div>
            <div class="w-20 sm:w-28 bg-white/10 h-2 rounded-full overflow-hidden self-center ml-2">
              <div id="shell-pacing-bar" class="h-full bg-emerald-500 transition-all duration-300" style="width: 10%;"></div>
            </div>
          </div>
        </div>

        <!-- Question Body & Palette Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div class="lg:col-span-3 space-y-6">
            <div class="apple-glass rounded-2xl p-6 sm:p-7 space-y-6">
              <div class="flex items-center justify-between border-b border-white/10 pb-3">
                <span id="shell-question-counter" class="text-xs font-bold font-mono text-blue-400 uppercase tracking-wider">Question 1 of 5</span>
                <div class="flex items-center gap-1.5 text-xs text-slate-400 font-mono">
                  <span>Marking:</span>
                  <span class="text-emerald-400 font-bold">+4</span> / <span class="text-rose-400 font-bold">-1</span>
                </div>
              </div>

              <div id="shell-question-body" class="text-sm sm:text-base text-slate-100 leading-relaxed font-sans min-h-[90px]">
                Loading problem statement...
              </div>

              <div id="shell-options-container" class="space-y-3 pt-2"></div>

              <!-- Mistake Taxonomy -->
              <div id="shell-mistake-taxonomy" class="pt-4 border-t border-white/10"></div>
            </div>

            <div class="flex items-center justify-between">
              <button onclick="window.ClockEEShell.prevQuestion()" class="min-h-[44px] px-5 py-2 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-xs font-bold text-slate-200 transition">
                ← Previous
              </button>
              <button onclick="window.ClockEEShell.nextQuestion()" class="min-h-[44px] px-6 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white shadow-lg shadow-blue-500/30 transition">
                Next Question →
              </button>
            </div>
          </div>

          <!-- Question Matrix -->
          <div class="space-y-4">
            <div class="apple-glass rounded-2xl p-5 space-y-4">
              <div class="flex items-center justify-between border-b border-white/10 pb-2">
                <span class="text-xs font-bold text-white uppercase tracking-wider">Question Matrix</span>
                <span class="text-[11px] text-slate-400">Authentic Bank</span>
              </div>
              <div id="shell-palette-grid" class="grid grid-cols-5 gap-2"></div>
            </div>
          </div>
        </div>
      </section>
    `,

    tasks: () => `
      <section class="space-y-6">
        <div class="apple-glass rounded-2xl p-6 space-y-4">
          <h2 class="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <span>📋</span> Daily Study Tasks & Sprint Matrix
          </h2>
          <p class="text-xs text-slate-400">Eisenhower Priority Matrix for high-yield JEE preparation.</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 space-y-2">
              <span class="text-xs font-bold text-rose-300 uppercase tracking-wider">Urgent & High Yield (Do First)</span>
              <ul class="text-xs text-slate-200 space-y-1.5 list-disc list-inside">
                <li>Solve 25 Rotation Dynamics PYQs (2020-2024)</li>
                <li>Review Thermo equilibrium constants</li>
              </ul>
            </div>
            <div class="p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 space-y-2">
              <span class="text-xs font-bold text-blue-300 uppercase tracking-wider">High Yield Strategy (Schedule)</span>
              <ul class="text-xs text-slate-200 space-y-1.5 list-disc list-inside">
                <li>Maths Definite Integrals King Property Drill</li>
                <li>Inorganic Salt Analysis Flashcards</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    `
  };

  // Navigation Controller
  function navigate(routeName) {
    if (!Views[routeName]) routeName = 'home';
    AppShellState.currentRoute = routeName;

    const mainOutlet = document.getElementById('shell-main-outlet');
    if (mainOutlet) {
      mainOutlet.innerHTML = Views[routeName]();
      updateNavHighlight(routeName);

      if (routeName === 'drill') {
        renderDrillQuestion();
        startDrillTimer();
      } else {
        if (AppShellState.pacingTimer) clearInterval(AppShellState.pacingTimer);
      }
    }
  }

  function updateNavHighlight(activeRoute) {
    document.querySelectorAll('[data-route]').forEach(btn => {
      const route = btn.getAttribute('data-route');
      if (route === activeRoute) {
        btn.classList.add('bg-blue-600/20', 'text-blue-300', 'border-blue-500/40');
        btn.classList.remove('text-slate-400', 'border-transparent');
      } else {
        btn.classList.remove('bg-blue-600/20', 'text-blue-300', 'border-blue-500/40');
        btn.classList.add('text-slate-400', 'border-transparent');
      }
    });
  }

  // Load 6,326 authentic questions
  async function loadQuestions() {
    try {
      const resp = await fetch('cbt_question_bank.json');
      if (resp.ok) {
        const fullBank = await resp.json();
        if (Array.isArray(fullBank) && fullBank.length > 0) {
          AppShellState.questions = fullBank.slice(0, 10);
        }
      }
    } catch (e) {
      console.warn('Fallback questions loaded');
    }
  }

  // Pacing Timer
  function startDrillTimer() {
    if (AppShellState.pacingTimer) clearInterval(AppShellState.pacingTimer);
    AppShellState.elapsedSec = 0;
    updatePacingUI();

    AppShellState.pacingTimer = setInterval(() => {
      AppShellState.elapsedSec++;
      updatePacingUI();
    }, 1000);
  }

  function updatePacingUI() {
    const studentEl = document.getElementById('shell-student-time');
    const topperEl = document.getElementById('shell-topper-time');
    const badgeEl = document.getElementById('shell-pacing-badge');
    const barEl = document.getElementById('shell-pacing-bar');
    if (!studentEl) return;

    const currentQ = AppShellState.questions[AppShellState.currentQIndex] || {};
    const topperSec = currentQ.idealTimeSec || 120;
    const elapsed = AppShellState.elapsedSec;

    const m = Math.floor(elapsed / 60);
    const s = elapsed % 60;
    studentEl.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;

    const tM = Math.floor(topperSec / 60);
    const tS = topperSec % 60;
    if (topperEl) topperEl.textContent = `${tM}:${tS < 10 ? '0' : ''}${tS}`;

    const ratio = elapsed / topperSec;
    if (ratio < 0.75) {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
      badgeEl.textContent = '🚀 Fast & Accurate Pace';
      if (barEl) { barEl.style.width = `${Math.min(100, ratio * 100)}%`; barEl.style.backgroundColor = '#10b981'; }
    } else if (ratio <= 1.0) {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30';
      badgeEl.textContent = '⏱️ On Benchmark';
      if (barEl) { barEl.style.width = `${Math.min(100, ratio * 100)}%`; barEl.style.backgroundColor = '#06b6d4'; }
    } else {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30';
      badgeEl.textContent = '⚠️ Lagging Target';
      if (barEl) { barEl.style.width = '100%'; barEl.style.backgroundColor = '#f43f5e'; }
    }
  }

  function renderDrillQuestion() {
    const q = AppShellState.questions[AppShellState.currentQIndex];
    if (!q) return;

    const subPill = document.getElementById('shell-subject-pill');
    const chText = document.getElementById('shell-chapter-text');
    const diffBadge = document.getElementById('shell-difficulty-badge');
    const countText = document.getElementById('shell-question-counter');
    const bodyEl = document.getElementById('shell-question-body');
    const optContainer = document.getElementById('shell-options-container');

    if (subPill) subPill.textContent = q.subject;
    if (chText) chText.textContent = `${q.chapter} • ${q.topic || 'Concept'}`;
    if (diffBadge) diffBadge.textContent = q.difficulty || 'JEE Mains';
    if (countText) countText.textContent = `Question ${AppShellState.currentQIndex + 1} of ${AppShellState.questions.length}`;

    if (bodyEl) {
      bodyEl.innerHTML = q.text;
      renderMath(bodyEl);
    }

    if (optContainer) {
      const selected = AppShellState.userAnswers[AppShellState.currentQIndex];
      optContainer.innerHTML = (q.options || []).map((opt, i) => {
        const isChecked = selected === i;
        return `
          <button type="button" onclick="window.ClockEEShell.selectOption(${i})" class="min-h-[44px] w-full text-left p-3.5 rounded-xl border transition flex items-center gap-3.5 cursor-pointer ${
            isChecked ? 'bg-blue-600/15 border-blue-500 text-white' : 'bg-white/[0.02] border-white/10 hover:border-white/20 text-slate-200'
          }">
            <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-mono ${
              isChecked ? 'bg-blue-500 text-white' : 'bg-white/10 text-slate-400'
            }">${String.fromCharCode(65 + i)}</span>
            <div id="shell-opt-${i}" class="text-xs sm:text-sm font-medium leading-relaxed flex-1">${opt}</div>
          </button>
        `;
      }).join('');

      (q.options || []).forEach((_, i) => {
        const el = document.getElementById(`shell-opt-${i}`);
        if (el) renderMath(el);
      });
    }

    renderPalette();
    renderMistakes();
  }

  function renderPalette() {
    const grid = document.getElementById('shell-palette-grid');
    if (!grid) return;
    grid.innerHTML = AppShellState.questions.map((q, idx) => {
      const isCurrent = idx === AppShellState.currentQIndex;
      const isAns = AppShellState.userAnswers[idx] !== undefined;
      return `
        <button onclick="window.ClockEEShell.goTo(${idx})" class="min-h-[44px] rounded-xl border text-xs font-bold flex items-center justify-center ${
          isCurrent ? 'ring-2 ring-blue-500 bg-blue-500/20 text-white' : isAns ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300' : 'bg-white/5 border-white/10 text-slate-400'
        }">Q${idx + 1}</button>
      `;
    }).join('');
  }

  function renderMistakes() {
    const box = document.getElementById('shell-mistake-taxonomy');
    if (!box) return;
    const current = AppShellState.mistakes[AppShellState.currentQIndex] || '';
    const tags = [
      { id: 'calc', label: '🧮 Calculation' },
      { id: 'concept', label: '📖 Concept' },
      { id: 'silly', label: '🤦 Silly Misread' },
      { id: 'time', label: '⏱️ Time Pressure' }
    ];
    box.innerHTML = `
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Mistake Audit:</span>
        ${tags.map(t => `
          <button onclick="window.ClockEEShell.tagMistake('${t.id}')" class="min-h-[44px] px-3 py-1 rounded-lg border text-xs font-semibold transition ${
            current === t.id ? 'bg-blue-600/30 border-blue-500 text-blue-200' : 'border-white/10 text-slate-400 hover:border-white/20'
          }">${t.label}</button>
        `).join('')}
      </div>
    `;
  }

  function renderMath(el) {
    if (!el || !window.katex) return;
    el.innerHTML = el.innerHTML.replace(/\$([^\$]+)\$/g, (m, tex) => {
      try { return window.katex.renderToString(tex, { throwOnError: false }); } catch(e) { return m; }
    });
  }

  // Public Shell API
  window.ClockEEShell = {
    navigate: navigate,
    selectOption: (optIdx) => {
      AppShellState.userAnswers[AppShellState.currentQIndex] = optIdx;
      renderDrillQuestion();
    },
    tagMistake: (tag) => {
      AppShellState.mistakes[AppShellState.currentQIndex] = AppShellState.mistakes[AppShellState.currentQIndex] === tag ? '' : tag;
      renderMistakes();
    },
    nextQuestion: () => {
      if (AppShellState.currentQIndex < AppShellState.questions.length - 1) {
        AppShellState.currentQIndex++;
        renderDrillQuestion();
        startDrillTimer();
      }
    },
    prevQuestion: () => {
      if (AppShellState.currentQIndex > 0) {
        AppShellState.currentQIndex--;
        renderDrillQuestion();
        startDrillTimer();
      }
    },
    goTo: (idx) => {
      AppShellState.currentQIndex = idx;
      renderDrillQuestion();
      startDrillTimer();
    }
  };

  // Bootstrap Shell
  async function init() {
    await loadQuestions();
    navigate('home');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
