window.renderClockEESidebar = function() {
  const mount = document.getElementById("clockee-sidebar-root");
  if (!mount) return;

  const now = new Date();
  const weekday = now.toLocaleDateString("en-US", { weekday: "long" });
  const fullDate = now.toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" });
  const s = window.getState ? window.getState() : {};
  const year = (s.jeeDate || "2026-05-17").slice(0, 4) || "2026";
  const quotes = [
    "“Consistency is the DNA of IIT-JEE mastery.”",
    "“Hard work beats talent when talent doesn’t work hard.”",
    "“Small disciplines repeated every day lead to great achievements.”",
    "“AIR 1 isn’t born in a day; it’s forged question by question.”",
    "“Do something today that your future self will thank you for.”",
    "“Focus on the process, and the rank will follow.”"
  ];
  const activeQuote = quotes[now.getDate() % quotes.length];

  mount.innerHTML = `
<aside class="w-full h-full glass-card border border-white/10 p-4 space-y-3.5 shadow-2xl relative bg-[#090b14]/90 backdrop-blur-2xl flex flex-col justify-between">
  <!-- Today is Header Card (Prominent Large Display) -->
  <div class="pb-3 border-b border-white/10 space-y-1.5">
    <div class="flex items-center justify-between">
      <span class="text-[10px] font-black uppercase tracking-widest text-cyan-400 flex items-center gap-1.5 bg-cyan-950/70 border border-cyan-500/30 px-2 py-0.5 rounded-md shadow-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
        TODAY IS
      </span>
      <span class="text-xs font-mono font-bold text-slate-400" id="sidebar-today-time-indicator">LIVE</span>
    </div>
    <div class="flex items-baseline justify-between flex-wrap gap-1">
      <div class="text-xl sm:text-2xl font-black tracking-tight text-white drop-shadow" id="sidebar-today-weekday">
        ${weekday}
      </div>
      <div class="text-xs sm:text-sm font-extrabold font-mono text-cyan-300 tracking-tight" id="sidebar-today-full-date">
        ${fullDate}
      </div>
    </div>
  </div>

  <!-- Aspirant Profile Card with Inspiring Quote & Dynamic JEE Year -->
  <div class="p-3.5 rounded-2xl bg-black/40 border border-white/10 hover:border-white/20 transition-all shadow-md relative group">
    <div class="relative w-16 h-16 mx-auto mb-2">
      <img class="w-16 h-16 rounded-full bg-[#070913] object-cover border-2 border-indigo-400/80 shadow-[0_0_20px_rgba(99,102,241,0.25)]" data-profile-avatar src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant" alt="Avatar" />
      <span class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-emerald-400 ring-2 ring-[#070913]" title="Active"></span>
    </div>
    <div class="text-center space-y-1">
      <div class="text-base font-black text-white tracking-tight" data-profile-name>JEE Aspirant</div>
      <div class="text-[11px] text-cyan-200/90 italic font-medium pt-0.5 px-1 leading-snug tracking-tight" id="sidebar-profile-quote">${activeQuote}</div>
    </div>
    <div class="text-[11px] font-extrabold uppercase tracking-wider text-indigo-300 bg-indigo-950/50 border border-indigo-500/30 rounded-lg py-1 px-2.5 text-center mt-2 flex items-center justify-center gap-1.5 shadow-sm" id="sidebar-jee-target-badge">
      <svg class="w-3.5 h-3.5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
      <span id="sidebar-jee-badge-text">JEE ${year}</span>
    </div>
  </div>

  <!-- Progress Card (Level & Daily Vitals) -->
  <div class="rounded-xl p-3 bg-gradient-to-br from-[#0c0f1d] to-[#121628] border border-white/10 space-y-2 shadow-md">
    <div class="flex items-center justify-between text-xs">
      <span class="font-extrabold text-indigo-300 flex items-center gap-1.5">
        <span id="sidebar-lvl-badge" class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-[10px] font-black border border-amber-500/30">Lv.1</span>
        <span id="sidebar-lvl-title" class="truncate max-w-[110px] uppercase tracking-wider text-[11px]">JEE Commander</span>
      </span>
      <span id="sidebar-xp-text" class="text-[10px] font-mono font-bold text-slate-400">0 / 500 XP</span>
    </div>
    <div class="w-full bg-gray-900 rounded-full h-1.5 overflow-hidden">
      <div id="sidebar-xp-bar" class="h-full bg-gradient-to-r from-amber-400 to-indigo-500 rounded-full transition-all duration-500" style="width: 0%"></div>
    </div>
    <div class="flex items-center justify-between pt-1 border-t border-white/5 text-[10px]">
      <div class="flex items-center gap-1.5 text-slate-400">
        <span class="flex items-center gap-1 font-bold uppercase text-[9px] tracking-wider text-slate-400">
          <svg class="w-3 h-3 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          Today
        </span>
        <span id="sidebar-today-qs" class="font-mono text-cyan-300 font-black">0 Qs</span>
      </div>
      <div class="flex items-center gap-1.5 text-slate-400">
        <span class="flex items-center gap-1 font-bold uppercase text-[9px] tracking-wider text-slate-400">
          <svg class="w-3 h-3 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Time
        </span>
        <span id="sidebar-today-hrs" class="font-mono text-purple-300 font-black">0.0 h</span>
      </div>
    </div>
  </div>

  <!-- Monthly Heatmap Calendar -->
  <div class="pt-2 border-t border-white/10 space-y-2">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>
        <span class="text-xs font-black uppercase tracking-wider text-white">Monthly Heatmap</span>
      </div>
      <div class="flex items-center gap-1 bg-black/40 border border-white/10 rounded-lg p-0.5">
        <button onclick="changeMonthlyHeatmap(-1)" class="w-5 h-5 flex items-center justify-center rounded text-gray-400 hover:text-white hover:bg-white/10 transition text-[11px]" title="Previous Month">◀</button>
        <span id="sidebar-month-title" class="text-[10px] font-mono font-bold text-indigo-300 px-1 cursor-pointer" onclick="resetMonthlyHeatmap()" title="Reset to current month">Oct 2026</span>
        <button onclick="changeMonthlyHeatmap(1)" class="w-5 h-5 flex items-center justify-center rounded text-gray-400 hover:text-white hover:bg-white/10 transition text-[11px]" title="Next Month">▶</button>
      </div>
    </div>

    <!-- Weekday Headers -->
    <div class="grid grid-cols-7 gap-1 text-center text-[9px] text-gray-500 font-mono uppercase pb-0.5 font-bold">
      <div>S</div><div>M</div><div>T</div><div>W</div><div>T</div><div>F</div><div>S</div>
    </div>

    <!-- 7x5/6 Calendar Days Grid -->
    <div id="sidebar-month-grid" class="grid grid-cols-7 gap-1"></div>
  </div>

  <!-- Graph 1: 7-Day Performance Trend Graph (Expanded Size) -->
  <div class="pt-3 border-t border-white/10 space-y-2">
    <div class="flex items-center justify-between text-xs">
      <div class="flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
        <span class="text-xs font-black uppercase tracking-wider text-slate-200">7-Day Velocity &amp; Latency</span>
      </div>
      <span id="sidebar-trend-tag" class="text-[9px] font-mono text-cyan-400 font-black px-1.5 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30">Target: 90 Q/d</span>
    </div>
    <div class="h-28 w-full relative bg-black/40 rounded-xl p-2 border border-white/5 shadow-inner">
      <canvas id="sidebar-mini-chart"></canvas>
    </div>
  </div>

  <!-- Graph 2: PCM Subject Focus Distribution (Fills vertical space symmetrically) -->
  <div class="pt-3 border-t border-white/10 space-y-2 flex-1 flex flex-col justify-end">
    <div class="flex items-center justify-between text-xs">
      <div class="flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
        <span class="text-xs font-black uppercase tracking-wider text-slate-200">PCM Focus Balance</span>
      </div>
      <span class="text-[9px] font-mono text-indigo-300 font-bold" id="sidebar-pcm-acc">Accuracy: --</span>
    </div>
    
    <div class="flex items-center gap-3 bg-black/40 rounded-xl p-2.5 border border-white/5 shadow-inner">
      <!-- Donut Canvas -->
      <div class="w-20 h-20 relative shrink-0">
        <canvas id="sidebar-pcm-chart"></canvas>
      </div>

      <!-- Subject Metric Breakdown -->
      <div class="flex-1 min-w-0 space-y-1.5 text-[10px] font-mono">
        <div class="flex items-center justify-between">
          <span class="text-blue-400 font-bold flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-400 inline-block shadow-[0_0_6px_rgba(96,165,250,0.6)]"></span> Physics
          </span>
          <span id="sidebar-pcm-phy" class="text-gray-300 font-extrabold">38%</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-emerald-400 font-bold flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 inline-block shadow-[0_0_6px_rgba(52,211,153,0.6)]"></span> Chemistry
          </span>
          <span id="sidebar-pcm-chem" class="text-gray-300 font-extrabold">34%</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-amber-400 font-bold flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400 inline-block shadow-[0_0_6px_rgba(251,191,36,0.6)]"></span> Maths
          </span>
          <span id="sidebar-pcm-math" class="text-gray-300 font-extrabold">28%</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Symmetrical Bottom Status Line -->
  <div class="pt-3 border-t border-white/10 flex items-center justify-between text-[10px] text-gray-400 font-mono">
    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> ClockEE Engine Active</span>
    <span class="text-cyan-400 font-bold uppercase tracking-wider text-[9px] flex items-center gap-1">
      <svg class="w-3 h-3 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>
      All Data Synced
    </span>
  </div>
</aside>
  `;
};

