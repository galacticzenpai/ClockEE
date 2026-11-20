/**
 * js/demo_app_shell.js
 * Isolated Prototype Sandbox Architecture (Apple HIG + Mathongo MARKS UX)
 * Zero dependency on legacy core files.
 */

(function() {
  'use strict';

  // Master State for Demo Sandbox
  const DemoState = {
    questions: [],
    currentIndex: 0,
    userAnswers: {}, // index -> selectedOption index or numerical val
    questionTimes: {}, // index -> seconds spent
    timerInterval: null,
    currentElapsedSec: 0,
    topperBenchmarkSec: 120, // Default 2 minutes
    isLegacySplitActive: false,
    mistakes: {}, // index -> { tag: 'calculation'|'concept'|'silly'|'timeout', notes: '' }
    activeTab: 'practice' // 'practice' | 'analysis' | 'mistakes'
  };

  // Sample 5 authentic questions for instant zero-lag prototype demonstration
  const FALLBACK_QUESTIONS = [
    {
      id: "demo_q1",
      subject: "Physics",
      chapter: "Rotational Motion",
      topic: "Moment of Inertia",
      difficulty: "Advanced",
      idealTimeSec: 135,
      text: "A thin uniform rod of length $L$ and mass $M$ is swinging freely about a horizontal axis through one end. The maximum angular velocity is $\\omega$. Its center of mass rises to a maximum height of:",
      options: [
        "$\\frac{L^2 \\omega^2}{6g}$",
        "$\\frac{L^2 \\omega^2}{3g}$",
        "$\\frac{L \\omega^2}{2g}$",
        "$\\frac{2L^2 \\omega^2}{3g}$"
      ],
      correct: 0,
      solution: "By energy conservation: $\\frac{1}{2} I \\omega^2 = Mgh_{cm}$. For a rod pivoted at one end, $I = \\frac{1}{3} M L^2$. Hence $\\frac{1}{2} (\\frac{1}{3} M L^2) \\omega^2 = Mgh_{cm} \\implies h_{cm} = \\frac{L^2 \\omega^2}{6g}$."
    },
    {
      id: "demo_q2",
      subject: "Chemistry",
      chapter: "Chemical Thermodynamics",
      topic: "Entropy & Spontaneity",
      difficulty: "Mains",
      idealTimeSec: 90,
      text: "For the reaction $2A(g) + B(g) \\rightarrow 2D(g)$, $\\Delta U^\\circ = -10.5\\text{ kJ}$ and $\\Delta S^\\circ = -44.1\\text{ J K}^{-1}$ at $298\\text{ K}$. The value of $\\Delta G^\\circ$ for the reaction is:",
      options: [
        "$-0.16\\text{ kJ}$",
        "$-1.25\\text{ kJ}$",
        "$+2.14\\text{ kJ}$",
        "$-12.98\\text{ kJ}$"
      ],
      correct: 0,
      solution: "$\\Delta n_g = 2 - (2 + 1) = -1$. $\\Delta H^\\circ = \\Delta U^\\circ + \\Delta n_g RT = -10.5 + (-1)(8.314 \\times 10^{-3})(298) \\approx -12.98\\text{ kJ}$. Then $\\Delta G^\\circ = \\Delta H^\\circ - T\\Delta S^\\circ = -12.98 - 298(-0.0441) \\approx -0.16\\text{ kJ}$."
    },
    {
      id: "demo_q3",
      subject: "Mathematics",
      chapter: "Definite Integrals",
      topic: "King's Property",
      difficulty: "Advanced",
      idealTimeSec: 150,
      text: "The value of the integral $I = \\int_{0}^{\\pi/2} \\frac{\\sin^3 x}{\\sin x + \\cos x} \\, dx - \\int_{0}^{\\pi/2} \\frac{\\cos^3 x}{\\sin x + \\cos x} \\, dx$ is:",
      options: [
        "$0$",
        "$\\frac{\\pi}{4}$",
        "$\\frac{1}{2}$",
        "$\\frac{\\pi}{2}$"
      ],
      correct: 0,
      solution: "Let $f(x) = \\frac{\\sin^3 x - \\cos^3 x}{\\sin x + \\cos x}$. Applying King's Rule $x \\rightarrow \\frac{\\pi}{2} - x$, the integrand transforms into its negative: $I = -I \\implies 2I = 0 \\implies I = 0$."
    },
    {
      id: "demo_q4",
      subject: "Physics",
      chapter: "Electrostatics",
      topic: "Gauss's Law",
      difficulty: "Mains",
      idealTimeSec: 100,
      text: "A point charge $q$ is placed at the center of an imaginary cube of side $a$. The electric flux emerging through one face of the cube is:",
      options: [
        "$\\frac{q}{6\\varepsilon_0}$",
        "$\\frac{q}{\\varepsilon_0}$",
        "$\\frac{q}{4\\pi \\varepsilon_0 a^2}$",
        "$\\frac{q}{8\\varepsilon_0}$"
      ],
      correct: 0,
      solution: "By symmetry, the total flux $\\Phi = \\frac{q}{\\varepsilon_0}$ is evenly distributed across the 6 identical faces. Thus, flux through one face = $\\frac{q}{6\\varepsilon_0}$."
    },
    {
      id: "demo_q5",
      subject: "Mathematics",
      chapter: "Matrices & Determinants",
      topic: "Properties of Adjoint",
      difficulty: "Mains",
      idealTimeSec: 110,
      text: "If $A$ is a $3 \\times 3$ non-singular matrix such that $\\det(A) = 4$, then $\\det(2 \\cdot \\text{adj}(3A))$ is equal to:",
      options: [
        "$2^3 \\cdot 3^4 \\cdot 4^2$",
        "$2^3 \\cdot 3^6 \\cdot 4^2$",
        "$2^3 \\cdot 3^2 \\cdot 4$",
        "$3^6 \\cdot 4^2$"
      ],
      correct: 1,
      solution: "For an $n \\times n$ matrix: $\\text{adj}(kA) = k^{n-1} \\text{adj}(A)$. Here $n=3$, so $\\text{adj}(3A) = 3^2 \\text{adj}(A) = 9 \\text{adj}(A)$. Then $\\det(2 \\cdot 9 \\text{adj}(A)) = \\det(18 \\text{adj}(A)) = 18^3 \\det(\\text{adj}(A)) = (2 \\cdot 3^2)^3 (\\det(A))^2 = 2^3 \\cdot 3^6 \\cdot 4^2$."
    }
  ];

  // Initialize
  async function initDemo() {
    try {
      const resp = await fetch('cbt_question_bank.json');
      if (resp.ok) {
        const fullBank = await resp.json();
        if (Array.isArray(fullBank) && fullBank.length >= 5) {
          DemoState.questions = fullBank.slice(0, 5);
        } else {
          DemoState.questions = FALLBACK_QUESTIONS;
        }
      } else {
        DemoState.questions = FALLBACK_QUESTIONS;
      }
    } catch (e) {
      DemoState.questions = FALLBACK_QUESTIONS;
    }

    renderCurrentQuestion();
    startPacingTimer();
    bindUIEvents();
  }

  // Pacing Timer with Mathongo-style Topper Benchmark Speed Comparison
  function startPacingTimer() {
    if (DemoState.timerInterval) clearInterval(DemoState.timerInterval);
    DemoState.currentElapsedSec = DemoState.questionTimes[DemoState.currentIndex] || 0;
    updatePacingDisplay();

    DemoState.timerInterval = setInterval(() => {
      DemoState.currentElapsedSec++;
      DemoState.questionTimes[DemoState.currentIndex] = DemoState.currentElapsedSec;
      updatePacingDisplay();
    }, 1000);
  }

  function updatePacingDisplay() {
    const timeEl = document.getElementById('demo-student-time');
    const badgeEl = document.getElementById('demo-pacing-badge');
    const barEl = document.getElementById('demo-pacing-bar');
    if (!timeEl) return;

    const currentQ = DemoState.questions[DemoState.currentIndex] || {};
    const topperSec = currentQ.idealTimeSec || 120;
    const elapsed = DemoState.currentElapsedSec;

    const m = Math.floor(elapsed / 60);
    const s = elapsed % 60;
    timeEl.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;

    const topperM = Math.floor(topperSec / 60);
    const topperS = topperSec % 60;
    const topperEl = document.getElementById('demo-topper-time');
    if (topperEl) topperEl.textContent = `${topperM}:${topperS < 10 ? '0' : ''}${topperS}`;

    // Mathongo Live Benchmark Pacing Tag
    const ratio = elapsed / topperSec;
    if (ratio < 0.75) {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
      badgeEl.textContent = '🚀 Fast & Accurate Pace';
      if (barEl) {
        barEl.style.width = `${Math.min(100, (elapsed / topperSec) * 100)}%`;
        barEl.style.backgroundColor = '#10b981';
      }
    } else if (ratio <= 1.0) {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30';
      badgeEl.textContent = '⏱️ On Topper Benchmark';
      if (barEl) {
        barEl.style.width = `${Math.min(100, (elapsed / topperSec) * 100)}%`;
        barEl.style.backgroundColor = '#06b6d4';
      }
    } else if (ratio <= 1.5) {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30';
      badgeEl.textContent = '⚠️ Lagging Benchmark';
      if (barEl) {
        barEl.style.width = '100%';
        barEl.style.backgroundColor = '#f59e0b';
      }
    } else {
      badgeEl.className = 'px-2 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30';
      badgeEl.textContent = '🚨 High Latency Trap';
      if (barEl) {
        barEl.style.width = '100%';
        barEl.style.backgroundColor = '#f43f5e';
      }
    }
  }

  // Render Question
  function renderCurrentQuestion() {
    const q = DemoState.questions[DemoState.currentIndex];
    if (!q) return;

    // Header Meta
    const subEl = document.getElementById('demo-subject-pill');
    const chEl = document.getElementById('demo-chapter-text');
    const diffEl = document.getElementById('demo-difficulty-badge');
    const countEl = document.getElementById('demo-question-counter');

    if (subEl) subEl.textContent = q.subject;
    if (chEl) chEl.textContent = `${q.chapter} • ${q.topic || 'Core Concept'}`;
    if (diffEl) diffEl.textContent = q.difficulty || 'JEE Mains';
    if (countEl) countEl.textContent = `Question ${DemoState.currentIndex + 1} of ${DemoState.questions.length}`;

    // Question Body
    const bodyEl = document.getElementById('demo-question-body');
    if (bodyEl) {
      bodyEl.innerHTML = q.text;
      renderKaTeX(bodyEl);
    }

    // Options
    const optContainer = document.getElementById('demo-options-container');
    if (optContainer) {
      const selected = DemoState.userAnswers[DemoState.currentIndex];
      optContainer.innerHTML = (q.options || []).map((opt, i) => {
        const isChecked = selected === i;
        return `
          <button 
            type="button" 
            onclick="window.DemoAppShell.selectOption(${i})" 
            class="min-h-[44px] w-full text-left p-3.5 rounded-xl border transition flex items-center gap-3.5 cursor-pointer select-none ${
              isChecked 
                ? 'bg-blue-600/15 border-blue-500 text-white shadow-sm' 
                : 'bg-white/[0.02] border-white/10 hover:border-white/20 text-slate-200 hover:bg-white/[0.04]'
            }"
          >
            <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-mono ${
              isChecked ? 'bg-blue-500 text-white' : 'bg-white/10 text-slate-400'
            }">
              ${String.fromCharCode(65 + i)}
            </span>
            <div id="demo-opt-text-${i}" class="text-xs sm:text-sm font-medium leading-relaxed flex-1">${opt}</div>
          </button>
        `;
      }).join('');

      (q.options || []).forEach((_, i) => {
        const el = document.getElementById(`demo-opt-text-${i}`);
        if (el) renderKaTeX(el);
      });
    }

    // Active Mistake Tag
    renderMistakeTaxonomy();

    // Palette Grid
    renderPaletteGrid();
  }

  // Mathongo-style Mistake Tagging Taxonomy
  function renderMistakeTaxonomy() {
    const container = document.getElementById('demo-mistake-taxonomy');
    if (!container) return;

    const currentMistake = DemoState.mistakes[DemoState.currentIndex] || {};
    const tags = [
      { key: 'calculation', label: '🧮 Calculation Error', color: 'border-amber-500/40 text-amber-300' },
      { key: 'concept', label: '📖 Conceptual Gap', color: 'border-purple-500/40 text-purple-300' },
      { key: 'silly', label: '🤦 Silly Misread', color: 'border-rose-500/40 text-rose-300' },
      { key: 'timeout', label: '⏱️ Time Pressure', color: 'border-cyan-500/40 text-cyan-300' }
    ];

    container.innerHTML = `
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Mistake Audit:</span>
        ${tags.map(t => {
          const isTagged = currentMistake.tag === t.key;
          return `
            <button 
              type="button" 
              onclick="window.DemoAppShell.tagMistake('${t.key}')" 
              class="min-h-[44px] px-3 py-1.5 rounded-lg border text-xs font-semibold transition cursor-pointer ${
                isTagged ? 'bg-white/15 ' + t.color + ' ring-1 ring-white/30' : 'bg-transparent border-white/10 text-slate-400 hover:border-white/20'
              }"
            >
              ${t.label}
            </button>
          `;
        }).join('')}
      </div>
    `;
  }

  function renderPaletteGrid() {
    const gridEl = document.getElementById('demo-palette-grid');
    if (!gridEl) return;

    gridEl.innerHTML = DemoState.questions.map((q, idx) => {
      const isCurrent = idx === DemoState.currentIndex;
      const hasAnswer = DemoState.userAnswers[idx] !== undefined;
      const isTagged = !!DemoState.mistakes[idx];

      let badgeBg = 'bg-white/5 border-white/10 text-slate-400';
      if (hasAnswer) badgeBg = 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300';
      if (isCurrent) badgeBg += ' ring-2 ring-blue-500';

      return `
        <button 
          type="button" 
          onclick="window.DemoAppShell.goToQuestion(${idx})" 
          class="min-h-[44px] min-w-[44px] rounded-xl border flex flex-col items-center justify-center p-1.5 transition text-xs font-bold ${badgeBg}"
        >
          <span>Q${idx + 1}</span>
          ${isTagged ? '<span class="text-[9px]">⚠️</span>' : ''}
        </button>
      `;
    }).join('');
  }

  // Render KaTeX Math safely
  function renderKaTeX(el) {
    if (!el || !window.katex) return;
    el.innerHTML = el.innerHTML.replace(/\$([^\$]+)\$/g, (match, tex) => {
      try {
        return window.katex.renderToString(tex, { throwOnError: false });
      } catch (e) {
        return match;
      }
    });
  }

  // Bind Buttons & Split View Toggle
  function bindUIEvents() {
    const prevBtn = document.getElementById('demo-prev-btn');
    const nextBtn = document.getElementById('demo-next-btn');
    const splitBtn = document.getElementById('demo-split-toggle');

    if (prevBtn) prevBtn.onclick = () => window.DemoAppShell.prevQuestion();
    if (nextBtn) nextBtn.onclick = () => window.DemoAppShell.nextQuestion();
    if (splitBtn) splitBtn.onclick = () => window.DemoAppShell.toggleLegacySplit();
  }

  // Public Interface
  window.DemoAppShell = {
    selectOption: function(optIdx) {
      DemoState.userAnswers[DemoState.currentIndex] = optIdx;
      renderCurrentQuestion();
    },
    tagMistake: function(tagKey) {
      if (!DemoState.mistakes[DemoState.currentIndex]) {
        DemoState.mistakes[DemoState.currentIndex] = { tag: tagKey, timestamp: Date.now() };
      } else if (DemoState.mistakes[DemoState.currentIndex].tag === tagKey) {
        delete DemoState.mistakes[DemoState.currentIndex];
      } else {
        DemoState.mistakes[DemoState.currentIndex].tag = tagKey;
      }
      renderMistakeTaxonomy();
      renderPaletteGrid();
    },
    nextQuestion: function() {
      if (DemoState.currentIndex < DemoState.questions.length - 1) {
        DemoState.currentIndex++;
        renderCurrentQuestion();
        startPacingTimer();
      }
    },
    prevQuestion: function() {
      if (DemoState.currentIndex > 0) {
        DemoState.currentIndex--;
        renderCurrentQuestion();
        startPacingTimer();
      }
    },
    goToQuestion: function(idx) {
      if (idx >= 0 && idx < DemoState.questions.length) {
        DemoState.currentIndex = idx;
        renderCurrentQuestion();
        startPacingTimer();
      }
    },
    toggleLegacySplit: function() {
      DemoState.isLegacySplitActive = !DemoState.isLegacySplitActive;
      const splitContainer = document.getElementById('demo-legacy-split-frame');
      const toggleLabel = document.getElementById('demo-split-label');
      if (splitContainer) {
        splitContainer.style.display = DemoState.isLegacySplitActive ? 'block' : 'none';
      }
      if (toggleLabel) {
        toggleLabel.textContent = DemoState.isLegacySplitActive ? 'Hide Legacy Comparison' : 'Compare with Legacy Design';
      }
    }
  };

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDemo);
  } else {
    initDemo();
  }
})();
