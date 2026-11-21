
    let tickTickFolded = true;

    function tickCountdown() {
      const s = window.getState ? window.getState() : {};
      const targetStr = s.jeeDate || '2026-05-17';
      const targetDate = new Date(targetStr + 'T06:00:00');
      const now = new Date();
      const diff = targetDate - now;

      // Dynamic JEE Year
      const year = targetStr.slice(0, 4) || '2026';
      const titleEl = document.getElementById('jee-countdown-title');
      if (titleEl) titleEl.textContent = `Target: JEE ${year}`;
      const subEl = document.getElementById('daily-mission-subtitle');
      if (subEl) subEl.textContent = `Current target mastery for JEE ${year}`;

      if (diff <= 0) {
        ['cd-months', 'cd-weeks', 'cd-days'].forEach(id => {
          const el = document.getElementById(id);
          if (el) el.textContent = '00';
        });
        return;
      }

      // Calendar month progression for precise individual counting (18 months)
      let temp = new Date(now.getTime());
      let months = 0;
      while (true) {
        let next = new Date(temp.getTime());
        next.setMonth(next.getMonth() + 1);
        if (next <= targetDate) {
          months++;
          temp = next;
        } else {
          break;
        }
      }

      // Total days and total weeks
      const totalDays = Math.floor(diff / 86400000);
      const totalWeeks = Math.floor(totalDays / 7);

      const elMonths = document.getElementById('cd-months');
      if (elMonths) elMonths.textContent = String(months).padStart(2, '0');
      const elWeeks = document.getElementById('cd-weeks');
      if (elWeeks) elWeeks.textContent = String(totalWeeks).padStart(2, '0');
      const elDays = document.getElementById('cd-days');
      if (elDays) elDays.textContent = String(totalDays);

      const elLabel = document.getElementById('jee-target-date-label');
      if (elLabel) elLabel.textContent = s.jeeDate || 'May 17, 2026';
    }

    function updateDailyProgress() {
      const s = window.getState ? window.getState() : {};
      const qs = window.getQuestionsToday();
      const qPhy = document.getElementById('quick-phy-today');
      if (qPhy) qPhy.textContent = `${qs.Physics}`;
      const qChem = document.getElementById('quick-chem-today');
      if (qChem) qChem.textContent = `${qs.Chemistry}`;
      const qMath = document.getElementById('quick-math-today');
      if (qMath) qMath.textContent = `${qs.Maths}`;

      const streak = s.stats?.streakDays || 0;
      const streakEl = document.getElementById('home-mission-streak-text');
      if (streakEl) streakEl.textContent = `${streak}-Day Streak`;

      const inProgTask = (s.tasks || []).find(t => !t.completed && t.subject);
      const chNameEl = document.getElementById('active-chapter-name');
      const chTopicEl = document.getElementById('active-chapter-topic');
      if (inProgTask && chNameEl) {
        chNameEl.textContent = inProgTask.title || 'Kinematics & Vectors';
        if (chTopicEl) chTopicEl.textContent = inProgTask.list || 'Active Target';
      }
    }
    window.updateDailyProgress = updateDailyProgress;

    window.toggleTickTickFold = function() {
      tickTickFolded = !tickTickFolded;
      const btn = document.getElementById('btn-toggle-tt-fold');
      if (btn) btn.textContent = tickTickFolded ? '▾ TickTick Fold' : '▴ TickTick Unfold';
      renderTodaysTasks();
    };

    function renderTodaysTasks() {
      const container = document.getElementById('home-tasks-list');
      if (!container) return;
      const s = window.getState();
      const today = window.getTodayStr();
      const allTodayTasks = (s.tasks || []).filter(t => (t.dueDate || '').slice(0, 10) === today || t.status === 'in_progress');

      if (allTodayTasks.length === 0) {
        container.innerHTML = '<p class="text-xs text-slate-500 font-medium italic py-4 text-center">No tasks scheduled for today — all caught up.</p>';
        return;
      }

      const regularTasks = [];
      const tickTickTasks = [];

      allTodayTasks.forEach(t => {
        const isTT = (t.id && String(t.id).startsWith('tt_')) || t.source === 'ticktick';
        if (isTT) tickTickTasks.push(t);
        else regularTasks.push(t);
      });

      const renderCard = (t) => {
        const isTickTick = (t.id && String(t.id).startsWith('tt_')) || t.source === 'ticktick';
        const isRevision = t.type === 'revision' || (t.tags || []).some(x => String(x).toLowerCase().includes('revision'));

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
                <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleTaskDone('${t.id}')" class="rounded text-[#0a84ff] focus:ring-0">
                <span class="text-xs ${t.completed ? 'line-through text-slate-500' : 'text-slate-100 font-bold'} truncate">${t.title}</span>
              </div>
              <span class="text-[9px] px-2 py-0.5 rounded-full border ${subCol} font-mono shrink-0 font-bold">${subBadgeText}</span>
            </div>
            <div class="flex items-center justify-between text-[10px] text-slate-400 pl-6">
              <span class="flex items-center gap-1.5 text-slate-300">
                <svg class="w-3 h-3 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                <span class="font-bold text-slate-300">${t.list || 'PW Modules & Practice Sheets'}</span>
              </span>
              <span class="text-[9px] text-slate-400 font-mono font-bold">${t.dueDate || 'Today'}</span>
            </div>
          </div>
        `;
      };

      let html = regularTasks.map(renderCard).join('');

      if (tickTickTasks.length > 0) {
        html += `
          <div class="pt-2 border-t border-cyan-500/20">
            <div onclick="toggleTickTickFold()" class="p-2 rounded-xl bg-cyan-950/40 border border-cyan-500/30 flex items-center justify-between cursor-pointer hover:bg-cyan-950/60 transition">
              <span class="text-xs font-black uppercase tracking-wider text-cyan-300 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>
                <span>TickTick Folded Tasks (${tickTickTasks.length})</span>
              </span>
              <span class="text-[10px] font-mono font-bold text-cyan-400">${tickTickFolded ? '▾ Expand' : '▴ Collapse'}</span>
            </div>
            ${tickTickFolded ? '' : `<div class="space-y-1.5 pt-2 pl-1">${tickTickTasks.map(renderCard).join('')}</div>`}
          </div>
        `;
      }

      container.innerHTML = html;
    }

    window.toggleTaskDone = function(id) {
      const s = window.getState();
      const t = (s.tasks || []).find(x => x.id === id);
      if (t) {
        t.completed = !t.completed;
        t.status = t.completed ? 'done' : 'todo';
        window.saveState();
        renderTodaysTasks();
      }
    };

    function renderMilestones() {
      const container = document.getElementById('milestones-list');
      if (!container) return;
      const s = window.getState();
      const today = window.getTodayStr();
      const items = (s.tasks || []).filter(t => (t.type === 'milestone' || t.type === 'aits') && (t.dueDate || '') >= today);

      if (s.nextMilestone && s.nextMilestone.date && s.nextMilestone.date >= today) {
        if (!items.some(x => x.title === s.nextMilestone.title)) {
          items.unshift({
            id: 'setting_milestone',
            title: s.nextMilestone.title || 'Target Major Exam',
            dueDate: s.nextMilestone.date,
            type: 'milestone'
          });
        }
      }

      if (items.length === 0) {
        container.innerHTML = '<p class="text-xs text-slate-500 font-medium italic py-4 text-center">No upcoming test deadlines. Set target in Settings.</p>';
        return;
      }
      container.innerHTML = items.map(m => `
        <div class="flex items-center justify-between p-2.5 rounded-xl bg-gray-900/80 border border-white/5 hover:border-white/10 transition">
          <div class="flex items-center gap-2 truncate">
            <svg class="w-3.5 h-3.5 text-amber-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            <span class="text-xs font-bold text-white truncate">${m.title}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-[#161b24] text-[#0a84ff] border border-white/10 font-mono font-bold">${m.dueDate}</span>
            <a href="cbt_home.html" class="text-[10px] bg-[#0a84ff] hover:bg-[#0a84ff] text-white font-extrabold px-2.5 py-1 rounded-lg transition">CBT</a>
          </div>
        </div>
      `).join('');
    }

    // Quick Logger
    window.logQuickQuestions = function(subject, delta) {
      const s = window.getState();
      s.questionLogs = s.questionLogs || [];
      const today = window.getTodayStr();

      if (delta < 0) {
        let remainingToDeduct = Math.abs(delta);
        for (let i = s.questionLogs.length - 1; i >= 0; i--) {
          const log = s.questionLogs[i];
          if (log.date === today && log.subject === subject) {
            const currentQ = log.questions || log.totalQs || 1;
            if (currentQ <= remainingToDeduct) {
              remainingToDeduct -= currentQ;
              s.questionLogs.splice(i, 1);
            } else {
              log.questions = currentQ - remainingToDeduct;
              remainingToDeduct = 0;
            }
            if (remainingToDeduct === 0) break;
          }
        }
        window.showToast(`Deducted 1 question from ${subject}`, 'info');
      } else {
        s.questionLogs.push({
          date: today,
          subject: subject,
          chapter: `${subject} Daily Practice`,
          questions: delta,
          correct: delta,
          score: delta * 4,
          durationMs: delta * 90000,
          source: 'manual_drill',
          timestamp: Date.now()
        });
        window.showToast(`+${delta} ${subject} questions logged`, 'success');
      }

      window.saveState();
      updateDailyProgress();
      if (typeof window.renderMonthlyHeatmap === 'function') window.renderMonthlyHeatmap();
      if (typeof window.renderSidebarMiniChart === 'function') window.renderSidebarMiniChart();
    };

    window.logCustomQuestions = function(subject) {
      const key = subject === 'Physics' ? 'custom-phy-input' : subject === 'Chemistry' ? 'custom-chem-input' : 'custom-math-input';
      const input = document.getElementById(key);
      const val = parseInt(input?.value || '0');
      if (val > 0) {
        logQuickQuestions(subject, val);
        if (input) input.value = '';
      }
    };

    // ─── Main Control Simulation & Error Diagnostics Control ───
    function renderSimulationControlHUD() {
      const s = window.getState ? window.getState() : {};
      const simulations = s.simulations || [];
      const mistakes = s.mistakeVault || [];

      // Metrics HUD
      const totalRunsEl = document.getElementById('sim-total-runs');
      if (totalRunsEl) totalRunsEl.textContent = simulations.length;

      const activeErrorsEl = document.getElementById('sim-active-errors');
      if (activeErrorsEl) activeErrorsEl.textContent = mistakes.length;

      const avgAccEl = document.getElementById('sim-avg-accuracy');
      if (avgAccEl) {
        if (simulations.length > 0) {
          const avg = Math.round(simulations.reduce((sum, sim) => sum + (sim.accuracy || 0), 0) / simulations.length);
          avgAccEl.textContent = `${avg}%`;
        } else {
          avgAccEl.textContent = '--%';
        }
      }

      const avgLatEl = document.getElementById('sim-avg-latency');
      if (avgLatEl) {
        if (simulations.length > 0) {
          const lat = Math.round(simulations.reduce((sum, sim) => sum + (sim.avgLatencySec || 75), 0) / simulations.length);
          avgLatEl.textContent = `${lat}s`;
        } else {
          avgLatEl.textContent = '--s';
        }
      }

      // Recent Simulations History
      const countEl = document.getElementById('sim-stream-count');
      if (countEl) countEl.textContent = `${simulations.length} recorded`;

      const recentList = document.getElementById('sim-recent-list');
      if (recentList) {
        if (simulations.length === 0) {
          recentList.innerHTML = `
            <div class="p-3 text-center rounded-xl bg-black/20 border border-white/5 space-y-2">
              <p class="text-xs text-slate-400 font-medium">No simulation tests run yet.</p>
              <button onclick="triggerMainControlSimulationModal()" class="px-3 py-1 bg-cyan-600/20 hover:bg-cyan-600 text-cyan-300 hover:text-white border border-cyan-500/30 rounded-lg text-xs font-bold transition">
                ⚡ Run First Simulation
              </button>
            </div>
          `;
        } else {
          recentList.innerHTML = simulations.slice(0, 6).map(sim => {
            const subBadge = sim.subject === 'Physics' ? 'text-blue-300 bg-blue-950/60 border-blue-500/30' :
                             sim.subject === 'Chemistry' ? 'text-emerald-300 bg-emerald-950/60 border-emerald-500/30' :
                             sim.subject === 'Maths' ? 'text-amber-300 bg-amber-950/60 border-amber-500/30' :
                             'text-cyan-300 bg-cyan-950/60 border-cyan-500/30';
            const accCol = (sim.accuracy >= 75) ? 'text-emerald-400' : (sim.accuracy >= 50 ? 'text-amber-400' : 'text-rose-400');
            const scoreCol = (sim.score / (sim.maxScore || 100) >= 0.6) ? 'text-cyan-400' : 'text-slate-200';

            return `
              <div class="p-2 rounded-xl bg-gray-900/70 border border-white/5 hover:border-white/10 transition flex items-center justify-between gap-2">
                <div class="truncate flex-1 min-w-0">
                  <div class="flex items-center gap-1.5 truncate">
                    <span class="text-[9px] px-1.5 py-0.2 rounded-full border ${subBadge} font-mono font-bold shrink-0">${sim.subject || 'Full'}</span>
                    <span class="text-xs font-bold text-white truncate" title="${sim.title}">${sim.title}</span>
                  </div>
                  <div class="text-[10px] text-slate-400 font-mono mt-0.5 flex items-center gap-2">
                    <span>Score: <strong class="${scoreCol}">${sim.score}/${sim.maxScore}</strong></span>
                    <span>•</span>
                    <span>Acc: <strong class="${accCol}">${sim.accuracy}%</strong></span>
                    <span>•</span>
                    <span class="text-rose-400">${sim.errorsCount || 0} errs</span>
                  </div>
                </div>
                <a href="cbt_analysis.html?testId=${encodeURIComponent(sim.id)}" class="px-2 py-1 bg-white/5 hover:bg-white/15 text-slate-300 rounded text-[10px] font-mono shrink-0 transition" title="Inspect Test Diagnostics">
                  Inspect →
                </a>
              </div>
            `;
          }).join('');
        }
      }

      // Live Error Autopsy Radar Stream
      const errorsList = document.getElementById('sim-errors-list');
      if (errorsList) {
        if (mistakes.length === 0) {
          errorsList.innerHTML = `
            <div class="p-3 text-center rounded-xl bg-black/20 border border-white/5 space-y-1">
              <p class="text-xs text-emerald-400 font-bold">✓ Zero Unresolved Errors in Vault</p>
              <p class="text-[11px] text-slate-400">Run a simulation benchmark to test your formula derivations & pacing.</p>
            </div>
          `;
        } else {
          errorsList.innerHTML = mistakes.slice(0, 5).map(m => {
            const catCol = m.errorCategory === 'Calculation Mistake' ? 'bg-amber-950/60 text-amber-300 border-amber-500/30' :
                           m.errorCategory === 'Concept Gap' ? 'bg-rose-950/60 text-rose-300 border-rose-500/30' :
                           'bg-[#161b24] text-[#0a84ff] border-white/10';

            const subCol = m.subject === 'Physics' ? 'text-blue-400' :
                           m.subject === 'Chemistry' ? 'text-emerald-400' : 'text-amber-400';

            const snippet = (m.questionText || '').replace(/\n/g, ' ').slice(0, 55) + '...';

            return `
              <div class="p-2 rounded-xl bg-gray-900/70 border border-white/5 hover:border-rose-500/30 transition flex items-center justify-between gap-2">
                <div class="truncate flex-1 min-w-0">
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="text-[9px] font-mono font-bold ${subCol}">Q#${m.qNum}</span>
                    <span class="text-[9px] font-mono px-1.5 py-0.2 rounded-full border ${catCol} font-bold">${m.errorCategory || 'Mistake'}</span>
                    <span class="text-xs font-bold text-slate-200 truncate">${m.chapter || m.topic}</span>
                  </div>
                  <div class="text-[10px] text-slate-400 truncate mt-0.5" title="${m.questionText || ''}">${snippet}</div>
                  <div class="text-[9px] font-mono text-slate-500 mt-0.5">
                    Marked: <span class="text-rose-400">${m.markedOption}</span> -> Correct: <span class="text-emerald-400">${m.correctOption}</span> (${m.timeSpentSec || 75}s)
                  </div>
                </div>
                <button onclick="createTaskFromMistake('${m.id}')" class="px-2 py-1 rounded bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 text-[10px] font-mono font-bold transition shrink-0" title="Convert to Actionable Revision Task">
                  + Task
                </button>
              </div>
            `;
          }).join('');
        }
      }
    }

    window.createTaskFromMistake = function(mistakeId) {
      const s = window.getState ? window.getState() : {};
      s.mistakeVault = s.mistakeVault || [];
      s.tasks = s.tasks || [];
      const m = s.mistakeVault.find(x => x.id === mistakeId);
      if (!m) return;

      const already = s.tasks.some(t => t.mistakeId === mistakeId);
      if (already) {
        window.showToast("Task already queued for this mistake!", "info");
        return;
      }

      s.tasks.unshift({
        id: `task_autopsy_${Date.now()}`,
        mistakeId: mistakeId,
        title: `[Autopsy] Master Error Q#${m.qNum}: ${m.topic || m.chapter || 'Problem'}`,
        subject: m.subject || 'Physics',
        list: 'Revision & Formula Autopsy',
        inbox: 'JEE 2026',
        tags: ['#simulation_error', '#autopsy'],
        priority: 'high',
        dueDate: window.getTodayStr(),
        type: 'revision',
        status: 'todo',
        completed: false,
        subtasks: [
          { title: `Forensic Review: Root cause analysis (${m.errorCategory})`, done: false },
          { title: `Re-derive without answer key (${m.markedOption} -> ${m.correctOption})`, done: false },
          { title: "Solve clone problem in AI Cloner Studio", done: false }
        ]
      });

      window.saveState();
      renderTodaysTasks();
      window.showToast(`✓ Queued revision task for Q#${m.qNum}!`, "success");
    };

    window.autoFlowSimulationErrors = function() {
      const s = window.getState ? window.getState() : {};
      const mistakes = s.mistakeVault || [];
      if (mistakes.length === 0) {
        window.showToast("Zero unresolved errors in Mistake Vault! Run a simulation first.", "info");
        return;
      }
      s.tasks = s.tasks || [];
      let count = 0;
      mistakes.forEach(m => {
        if (!s.tasks.some(t => t.mistakeId === m.id)) {
          s.tasks.unshift({
            id: `task_autopsy_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            mistakeId: m.id,
            title: `[Autopsy] Master Error Q#${m.qNum}: ${m.topic || m.chapter || 'Problem'}`,
            subject: m.subject || 'Physics',
            list: 'Revision & Formula Autopsy',
            inbox: 'JEE 2026',
            tags: ['#simulation_error', '#autopsy'],
            priority: 'high',
            dueDate: window.getTodayStr(),
            type: 'revision',
            status: 'todo',
            completed: false,
            subtasks: [
              { title: `Forensic Review: Root cause analysis (${m.errorCategory})`, done: false },
              { title: `Re-derive solution (${m.markedOption} -> ${m.correctOption})`, done: false },
              { title: "Solve 1 clone in Question Cloner Studio", done: false }
            ]
          });
          count++;
        }
      });

      if (count > 0) {
        window.saveState();
        renderTodaysTasks();
        renderSimulationControlHUD();
        window.showToast(`⚡ Converted ${count} simulation errors into priority Kanban tasks!`, "success");
      } else {
        window.showToast("All current errors are already queued in Task Flow.", "info");
      }
    };

    window.triggerMainControlSimulationModal = function() {
      let modal = document.getElementById('main-control-sim-modal');
      if (modal) modal.remove();

      modal = document.createElement('div');
      modal.id = 'main-control-sim-modal';
      modal.className = 'fixed inset-0 z-[300] bg-[#000000]/90 backdrop-blur-2xl flex items-center justify-center p-4';
      modal.innerHTML = `
        <div class="glass-card max-w-lg w-full p-6 border border-cyan-500/40 bg-[#0d1124] shadow-2xl space-y-5">
          <div class="flex items-center justify-between pb-3 border-b border-white/10">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-cyan-950/60 border border-cyan-500/40 flex items-center justify-center text-cyan-300">
                ⚡
              </div>
              <div>
                <h3 class="text-sm font-black text-white uppercase tracking-wider">Run Tactical Simulation &amp; Error Check</h3>
                <p class="text-[11px] text-slate-400 font-medium">Evaluate questions &bull; Categorize mistakes &bull; Send to Main Control</p>
              </div>
            </div>
            <button onclick="document.getElementById('main-control-sim-modal').remove()" class="text-slate-400 hover:text-white text-lg">&times;</button>
          </div>

          <div class="space-y-3.5">
            <div>
              <label class="block text-xs font-bold text-slate-300 mb-1.5">Simulation Syllabus Target:</label>
              <select id="sim-target-sub" class="w-full bg-black/60 border border-white/10 rounded-xl px-3 py-2 text-xs text-white font-medium outline-none focus:border-cyan-400">
                <option value="Full">Full Syllabus JEE Main Simulation (75 Questions)</option>
                <option value="Physics">Physics High-Pace Simulation (25 Questions)</option>
                <option value="Chemistry">Chemistry Speed &amp; Accuracy Drill (25 Questions)</option>
                <option value="Maths">Mathematics Numerical Benchmark (25 Questions)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-300 mb-1.5">Simulated Candidate Skill Level:</label>
              <select id="sim-target-skill" class="w-full bg-black/60 border border-white/10 rounded-xl px-3 py-2 text-xs text-white font-medium outline-none focus:border-cyan-400">
                <option value="balanced">Balanced Aspirant (70-75% Accuracy • Real-world Calculation Slips)</option>
                <option value="topper">Target AIR &lt; 500 Topper (90%+ Accuracy • Sub-second Pacing)</option>
                <option value="stress">Stress Test (50% Accuracy • High Concept Confusion & Latency Drift)</option>
              </select>
            </div>

            <div class="p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/20 text-xs text-cyan-200/90 space-y-1">
              <div class="font-bold flex items-center gap-1.5 text-cyan-300">
                <span>ℹ️</span> Simulation Pipeline Workflow:
              </div>
              <p class="text-[11px] text-slate-300 leading-relaxed">
                1. Retrieves authentic PYQ/adaptive questions from the 139,000+ question bank.<br>
                2. Simulates candidate response latency, choices, and numerical entries.<br>
                3. Checks each answer, categorizes errors into Calculation, Concept, and Latency.<br>
                4. Transmits full autopsy telemetry to Main Control, Mistake Vault, and Task Flow!
              </p>
            </div>
          </div>

          <div class="flex gap-2.5 pt-2">
            <button onclick="document.getElementById('main-control-sim-modal').remove()" class="flex-1 py-2.5 rounded-xl border border-white/10 text-xs font-bold text-slate-400 hover:text-white transition">
              Cancel
            </button>
            <button id="btn-run-sim-confirm" onclick="executeMainControlSimulation()" class="flex-1 py-2.5 bg-gradient-to-r from-cyan-500 to-[#0071e3] hover:from-cyan-400 hover:to-[#0071e3] text-white font-extrabold rounded-xl text-xs transition shadow-lg shadow-cyan-500/25 flex items-center justify-center gap-1.5">Launch &amp; Audit Now
            </button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    };

    window.executeMainControlSimulation = function() {
      const subSelect = document.getElementById('sim-target-sub');
      const skillSelect = document.getElementById('sim-target-skill');
      const sub = subSelect ? subSelect.value : 'Full';
      const skill = skillSelect ? skillSelect.value : 'balanced';

      const btn = document.getElementById('btn-run-sim-confirm');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span class="animate-spin">⏳</span> Running & Auditing Simulation...`;
      }

      setTimeout(() => {
        if (typeof window.runSimulationBenchmark === 'function') {
          const res = window.runSimulationBenchmark({
            subject: sub,
            qCount: sub === 'Full' ? 75 : 25,
            skillProfile: skill
          });

          const modal = document.getElementById('main-control-sim-modal');
          if (modal) modal.remove();

          renderSimulationControlHUD();
          updateDailyProgress();
          renderTodaysTasks();
          if (typeof window.renderMonthlyHeatmap === 'function') window.renderMonthlyHeatmap();

          window.showToast(`✓ Simulation Complete: ${res.evalResult.score}/${res.evalResult.maxScore} pts • ${res.evalResult.mistakes.length} errors autopsied & sent to Main Control!`, "success");
        } else {
          window.showToast("CBT Simulation Engine is initializing...", "info");
        }
      }, 400);
    };

    // Cross-Tab Broadcast Synchronization
    try {
      const channel = new BroadcastChannel('clockee_main_control_sync');
      channel.onmessage = function(e) {
        if (e.data && e.data.type === 'SIMULATION_COMPLETED') {
          renderSimulationControlHUD();
          updateDailyProgress();
          renderTodaysTasks();
          if (typeof window.renderMonthlyHeatmap === 'function') window.renderMonthlyHeatmap();
          window.showToast(`📡 Telemetry incoming: ${e.data.errorsCount} errors sent to Main Control!`, "info");
        }
      };
    } catch(e) {}

    document.addEventListener('DOMContentLoaded', function() {
      try {
        var u = JSON.parse(localStorage.getItem('clockee_current_user') || '{}');
        var isAdmin = u.role === 'Admin' || u.role === 'Mentor / Faculty' || u.isAdmin === true || sessionStorage.getItem('clockee_admin_authorized') === 'true';
        if (isAdmin) {
          document.querySelectorAll('.nav-admin-link').forEach(function(el) {
            el.classList.remove('hidden');
            el.style.setProperty('display', 'inline-flex', 'important');
          });
        }
      } catch(e) {}
      tickCountdown();
      setInterval(tickCountdown, 1000);
      updateDailyProgress();
      renderTodaysTasks();
      renderMilestones();
      renderSimulationControlHUD();
    });

    window.addEventListener('stateChange', function() {
      updateDailyProgress();
      renderTodaysTasks();
      renderMilestones();
      renderSimulationControlHUD();
    });
  