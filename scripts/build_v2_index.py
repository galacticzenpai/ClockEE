import os, re

with open('scripts/card_1.html', 'r', encoding='utf-8') as f:
    card_1 = f.read().strip()

# Add tabular-nums and mono to countdown header to satisfy linter
card_1 = re.sub(r'class="text-base sm:text-lg font-black text-white tracking-tight"\s*id="jee-countdown-title"', 'id="jee-countdown-title" class="text-base sm:text-lg font-black text-white tracking-tight tabular-nums mono"', card_1)

with open('scripts/card_2.html', 'r', encoding='utf-8') as f:
    card_2 = f.read().strip()

# Sanitize card 2 arbitrary shadow
card_2 = card_2.replace('shadow-[0_0_14px_rgba(249,115,22,0.3)]', 'shadow-sm')

with open('scripts/card_3.html', 'r', encoding='utf-8') as f:
    card_3 = f.read().strip()

with open('scripts/card_5.html', 'r', encoding='utf-8') as f:
    card_5 = f.read().strip()

with open('scripts/v1_drawer_full.html', 'r', encoding='utf-8') as f:
    drawer_html = f.read().strip()

# Sanitize drawer shadow
drawer_html = drawer_html.replace('shadow-[-10px_0_40px_rgba(0,0,0,0.8)]', 'shadow-[-4px_0_12px_rgba(0,0,0,0.7)]')

with open('scripts/v1_styles.css', 'r', encoding='utf-8') as f:
    v1_styles = f.read().strip()

# Sanitize v1_styles shadows
v1_styles = re.sub(r'box-shadow:\s*0\s+16px\s+40px[^;]+;', 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);', v1_styles)
v1_styles = re.sub(r'box-shadow:\s*0\s+0\s+(?:1[3-9]|[2-9][0-9])px[^;]+;', 'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);', v1_styles)
v1_styles = re.sub(r'box-shadow:\s*0\s+[0-9]+px\s+(?:1[3-9]|[2-9][0-9])px[^;]+;', 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);', v1_styles)

index_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ClockEE OS 2.0 // High-Precision Cockpit</title>
  
  <script src="env.js" onerror="/* env.js optional */"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- CDNs -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
        }},
      }},
    }};
  </script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

  <link rel="stylesheet" href="styles/clockee_motion.css" />
  <link rel="stylesheet" href="styles/tokens.css" />

  <style>
    :root {{
      --bg-base: #070913;
      --bg-surface: #0a0c10;
      --bg-elevated: #12151c;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.16);
      --accent: #0a84ff;
      --accent-cyan: #00f0ff;
      --text-primary: #ffffff;
      --text-secondary: #94a3b8;
    }}

    body {{
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }}

    .glass-card {{
      background: rgba(10, 12, 18, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .glass-card:hover {{
      border-color: rgba(255, 255, 255, 0.14);
    }}

    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .tabular-nums {{ font-variant-numeric: tabular-nums; }}

    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #070913; }}
    ::-webkit-scrollbar-thumb {{ background: #1e293b; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #334155; }}

    @keyframes spinSlow {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .animate-spin-slow {{
      animation: spinSlow 14s linear infinite;
    }}

    {v1_styles}
  </style>

  <!-- Core Scripts -->
  <script src="cbt_master_bank.js"></script>
  <script src="cbt_shared.js"></script>
  <script src="clockee_core.js"></script>
  <script src="js/clockee_runtime.js"></script>
  <script src="components/navbar.js"></script>
</head>
<body data-page="home" class="min-h-screen flex flex-col relative antialiased selection:bg-[#0a84ff] selection:text-white bg-[#070913]">

  <!-- Universal Master Navigation Bar -->
  <div id="clockee-nav"></div>

  <!-- Main Cockpit Workspace -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 pb-24 grid grid-cols-1 lg:grid-cols-12 gap-6 relative w-full flex-1">
    
    <!-- Left Column: Aspirant Profile, XP Status, Monthly Heatmap & Dual Graphs (lg:col-span-4) -->
    <aside class="lg:col-span-4 flex flex-col gap-6" id="clockee-sidebar-root">
      <!-- Dynamically mounted by window.renderClockEESidebar() -->
    </aside>

    <!-- Right Column: Symmetrical Alignment & Balanced Spacing (lg:col-span-8) -->
    <div class="lg:col-span-8 flex flex-col gap-6 min-w-0">
      
      <!-- 1. JEE Target Countdown Card: Months, Total Weeks, Days -->
      {card_1}

      <!-- 2. Aspirant Daily Target & Readiness HUD -->
      {card_2}

      <!-- 3. Quick Log Solved Questions (+1, +5, -1 with top counter) -->
      {card_3}

      <!-- 4. Tactical Simulation & Error Diagnostics Control EXCLUDED AS REQUESTED -->

      <!-- 5. Today's Queue (Foldable TickTick section) & Upcoming Milestones -->
      {card_5}

    </div>
  </main>

  <!-- Split Screen Focus Drawer -->
  {drawer_html}

  <!-- Floating Action Triggers -->
  <div class="fixed bottom-4 right-4 z-40 flex items-center gap-2">
    <button onclick="window.toggleSplitScreen ? window.toggleSplitScreen() : (function(){{ var d = document.getElementById('split-drawer'); if (d) d.classList.toggle('translate-x-full'); }})()" id="clockee-chat-floating-pill" class="px-3.5 py-2 rounded-full bg-[#0a0c10]/90 border border-white/10 hover:border-blue-400/50 text-slate-300 hover:text-white text-xs font-bold shadow-sm backdrop-blur-xl flex items-center gap-2 transition cursor-pointer">
      <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
      <span>AI TUTOR</span>
    </button>
  </div>

  <!-- Home Page Reactive Engine -->
  <script>
    let tickTickFolded = true;

    function tickCountdown() {{
      const s = window.getState ? window.getState() : {{}};
      const targetStr = s.jeeDate || '2028-05-17';
      const targetDate = new Date(targetStr + 'T06:00:00');
      const now = new Date();
      const diff = targetDate - now;

      // Dynamic JEE Year
      const year = targetStr.slice(0, 4) || '2028';
      const titleEl = document.getElementById('jee-countdown-title');
      if (titleEl) titleEl.textContent = `Target: JEE ${{year}}`;
      const subEl = document.getElementById('daily-mission-subtitle');
      if (subEl) subEl.textContent = `Current target mastery for JEE ${{year}}`;

      if (diff <= 0) {{
        ['cd-months', 'cd-weeks', 'cd-days'].forEach(id => {{
          const el = document.getElementById(id);
          if (el) el.textContent = '00';
        }});
        return;
      }}

      // Calendar month progression for precise individual counting
      let temp = new Date(now.getTime());
      let months = 0;
      while (true) {{
        let next = new Date(temp.getTime());
        next.setMonth(next.getMonth() + 1);
        if (next <= targetDate) {{
          months++;
          temp = next;
        }} else {{
          break;
        }}
      }}

      const totalDays = Math.floor(diff / 86400000);
      const totalWeeks = Math.floor(totalDays / 7);

      const elMonths = document.getElementById('cd-months');
      if (elMonths) elMonths.textContent = String(months).padStart(2, '0');
      const elWeeks = document.getElementById('cd-weeks');
      if (elWeeks) elWeeks.textContent = String(totalWeeks).padStart(2, '0');
      const elDays = document.getElementById('cd-days');
      if (elDays) elDays.textContent = String(totalDays);

      const elLabel = document.getElementById('jee-target-date-label');
      if (elLabel) elLabel.textContent = s.jeeDate || 'May 17, 2028';
    }}

    function updateDailyProgress() {{
      const s = window.getState ? window.getState() : {{}};
      const qs = window.getQuestionsToday ? window.getQuestionsToday() : {{ Physics: 0, Chemistry: 0, Maths: 0, total: 0 }};
      
      const qPhy = document.getElementById('quick-phy-today');
      if (qPhy) qPhy.textContent = String(qs.Physics || 0);
      const qChem = document.getElementById('quick-chem-today');
      if (qChem) qChem.textContent = String(qs.Chemistry || 0);
      const qMath = document.getElementById('quick-math-today');
      if (qMath) qMath.textContent = String(qs.Maths || 0);

      const streak = s.stats?.streakDays || 0;
      const streakEl = document.getElementById('home-mission-streak-text');
      if (streakEl) streakEl.textContent = `${{streak}}-Day Streak`;

      const inProgTask = (s.tasks || []).find(t => !t.completed && t.subject);
      const chNameEl = document.getElementById('active-chapter-name');
      const chTopicEl = document.getElementById('active-chapter-topic');
      if (inProgTask && chNameEl) {{
        chNameEl.textContent = inProgTask.title || 'Kinematics & Vectors';
        if (chTopicEl) chTopicEl.textContent = inProgTask.list || 'Active Target';
      }}
    }}
    window.updateDailyProgress = updateDailyProgress;

    window.toggleTickTickFold = function() {{
      tickTickFolded = !tickTickFolded;
      const btn = document.getElementById('btn-toggle-tt-fold');
      if (btn) btn.textContent = tickTickFolded ? '▾ TickTick Fold' : '▴ TickTick Unfold';
      renderTodaysTasks();
    }};

    function renderTodaysTasks() {{
      const container = document.getElementById('home-tasks-list');
      if (!container) return;
      const s = window.getState ? window.getState() : {{ tasks: [] }};
      const today = window.getTodayStr ? window.getTodayStr() : new Date().toISOString().slice(0, 10);
      const allTodayTasks = (s.tasks || []).filter(t => (t.dueDate || '').slice(0, 10) === today || t.status === 'in_progress');

      if (allTodayTasks.length === 0) {{
        container.innerHTML = '<p class="text-xs text-slate-500 font-medium italic py-4 text-center">No tasks scheduled for today — all caught up.</p>';
        return;
      }}

      const regularTasks = [];
      const tickTickTasks = [];

      allTodayTasks.forEach(t => {{
        const isTT = (t.id && String(t.id).startsWith('tt_')) || t.source === 'ticktick';
        if (isTT) tickTickTasks.push(t);
        else regularTasks.push(t);
      }});

      const renderCard = (t) => {{
        const isTickTick = (t.id && String(t.id).startsWith('tt_')) || t.source === 'ticktick';
        const subCol = isTickTick ? 'text-cyan-300 bg-cyan-950/70 border-cyan-500/40' :
                       t.subject === 'Physics' ? 'text-blue-300 bg-blue-950/60 border-blue-500/30' :
                       t.subject === 'Chemistry' ? 'text-emerald-300 bg-emerald-950/60 border-emerald-500/30' :
                       t.subject === 'Maths' ? 'text-amber-300 bg-amber-950/60 border-amber-500/30' :
                       'text-gray-300 bg-gray-800 border-gray-700';

        const subBadgeText = isTickTick ? 'From TickTick' : (t.subject || 'General');

        return `
          <div class="p-2.5 rounded-xl bg-gray-900/80 border border-white/5 space-y-1.5 hover:border-white/10 transition">
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-2 truncate">
                <input type="checkbox" ${{t.completed ? 'checked' : ''}} onchange="toggleTaskDone('${{t.id}}')" class="rounded text-[#0a84ff] focus:ring-0 cursor-pointer">
                <span class="text-xs ${{t.completed ? 'line-through text-slate-500' : 'text-slate-100 font-bold'}} truncate">${{t.title}}</span>
              </div>
              <span class="text-[9px] px-2 py-0.5 rounded-full border ${{subCol}} font-mono shrink-0 font-bold">${{subBadgeText}}</span>
            </div>
            <div class="flex items-center justify-between text-[10px] text-slate-400 pl-6">
              <span class="flex items-center gap-1.5 text-slate-300">
                <svg class="w-3 h-3 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                <span class="font-bold text-slate-300">${{t.list || 'PW Modules & Practice Sheets'}}</span>
              </span>
              <span class="text-[9px] text-slate-400 font-mono font-bold">${{t.dueDate || 'Today'}}</span>
            </div>
          </div>
        `;
      }};

      let html = regularTasks.map(renderCard).join('');

      if (tickTickTasks.length > 0) {{
        html += `
          <div class="pt-2 border-t border-cyan-500/20">
            <div onclick="toggleTickTickFold()" class="p-2 rounded-xl bg-cyan-950/40 border border-cyan-500/30 flex items-center justify-between cursor-pointer hover:bg-cyan-950/60 transition">
              <span class="text-xs font-black uppercase tracking-wider text-cyan-300 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>
                <span>TickTick Folded Tasks (${{tickTickTasks.length}})</span>
              </span>
              <span class="text-[10px] font-mono font-bold text-cyan-400">${{tickTickFolded ? '▾ Expand' : '▴ Collapse'}}</span>
            </div>
            ${{tickTickFolded ? '' : `<div class="space-y-1.5 pt-2 pl-1">${{tickTickTasks.map(renderCard).join('')}}</div>`}}
          </div>
        `;
      }}

      container.innerHTML = html;
    }}

    window.toggleTaskDone = function(id) {{
      const s = window.getState ? window.getState() : {{}};
      const t = (s.tasks || []).find(x => x.id === id);
      if (t) {{
        t.completed = !t.completed;
        t.status = t.completed ? 'done' : 'todo';
        if (window.saveState) window.saveState();
        renderTodaysTasks();
      }}
    }};

    function renderMilestones() {{
      const container = document.getElementById('milestones-list');
      if (!container) return;
      const s = window.getState ? window.getState() : {{}};
      const today = window.getTodayStr ? window.getTodayStr() : new Date().toISOString().slice(0, 10);
      const items = (s.tasks || []).filter(t => (t.type === 'milestone' || t.type === 'aits') && (t.dueDate || '') >= today);

      if (s.nextMilestone && s.nextMilestone.date && s.nextMilestone.date >= today) {{
        if (!items.some(x => x.title === s.nextMilestone.title)) {{
          items.unshift({{
            id: 'setting_milestone',
            title: s.nextMilestone.title || 'Target Major Exam',
            dueDate: s.nextMilestone.date,
            type: 'milestone'
          }});
        }}
      }}

      if (items.length === 0) {{
        container.innerHTML = '<p class="text-xs text-slate-500 font-medium italic py-4 text-center">No upcoming test deadlines. Set target in Settings.</p>';
        return;
      }}
      container.innerHTML = items.map(m => `
        <div class="flex items-center justify-between p-2.5 rounded-xl bg-gray-900/80 border border-white/5 hover:border-white/10 transition">
          <div class="flex items-center gap-2 truncate">
            <svg class="w-3.5 h-3.5 text-amber-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            <span class="text-xs font-bold text-white truncate">${{m.title}}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-[#161b24] text-[#0a84ff] border border-white/10 font-mono font-bold">${{m.dueDate}}</span>
            <a href="cbt_home.html" class="text-[10px] bg-[#0a84ff] hover:bg-[#0a84ff] text-white font-extrabold px-2.5 py-1 rounded-lg transition">CBT</a>
          </div>
        </div>
      `).join('');
    }}

    // Quick Logger
    window.logQuickQuestions = function(subject, delta) {{
      const s = window.getState ? window.getState() : {{}};
      s.questionLogs = s.questionLogs || [];
      const today = window.getTodayStr ? window.getTodayStr() : new Date().toISOString().slice(0, 10);

      if (delta < 0) {{
        let remainingToDeduct = Math.abs(delta);
        for (let i = s.questionLogs.length - 1; i >= 0; i--) {{
          const log = s.questionLogs[i];
          if (log.date === today && log.subject === subject) {{
            const currentQ = log.questions || log.totalQs || 1;
            if (currentQ <= remainingToDeduct) {{
              remainingToDeduct -= currentQ;
              s.questionLogs.splice(i, 1);
            }} else {{
              log.questions = currentQ - remainingToDeduct;
              remainingToDeduct = 0;
            }}
            if (remainingToDeduct === 0) break;
          }}
        }}
        if (window.showToast) window.showToast(`Deducted 1 question from ${{subject}}`, 'info');
      }} else {{
        s.questionLogs.push({{
          date: today,
          subject: subject,
          chapter: `${{subject}} Daily Practice`,
          questions: delta,
          correct: delta,
          score: delta * 4,
          durationMs: delta * 90000,
          source: 'manual_drill',
          timestamp: Date.now()
        }});
        if (window.showToast) window.showToast(`+${{delta}} ${{subject}} questions logged`, 'success');
      }}

      if (window.saveState) window.saveState();
      updateDailyProgress();
      if (typeof window.renderMonthlyHeatmap === 'function') window.renderMonthlyHeatmap();
      if (typeof window.renderSidebarMiniChart === 'function') window.renderSidebarMiniChart();
    }};

    window.logCustomQuestions = function(subject) {{
      const key = subject === 'Physics' ? 'custom-phy-input' : subject === 'Chemistry' ? 'custom-chem-input' : 'custom-math-input';
      const input = document.getElementById(key);
      const val = parseInt(input?.value || '0');
      if (val > 0) {{
        logQuickQuestions(subject, val);
        if (input) input.value = '';
      }}
    }};

    // Setup Enter key on custom inputs
    function setupCustomInputs() {{
      [['custom-phy-input', 'Physics'], ['custom-chem-input', 'Chemistry'], ['custom-math-input', 'Maths']].forEach(([id, sub]) => {{
        const el = document.getElementById(id);
        if (el) {{
          el.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter') {{
              logCustomQuestions(sub);
            }}
          }});
        }}
      }});
    }}

    document.addEventListener('DOMContentLoaded', function() {{
      tickCountdown();
      setInterval(tickCountdown, 1000);
      updateDailyProgress();
      renderTodaysTasks();
      renderMilestones();
      setupCustomInputs();
      if (typeof window.renderClockEESidebar === 'function') {{
        window.renderClockEESidebar();
      }}
    }});

    window.addEventListener('stateChange', function() {{
      updateDailyProgress();
      renderTodaysTasks();
      renderMilestones();
      if (typeof window.renderClockEESidebar === 'function') {{
        window.renderClockEESidebar();
      }}
    }});
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(index_html)

print("Generated clean index.html, lines:", len(index_html.splitlines()), "size:", len(index_html))
