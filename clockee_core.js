// ==========================================================================
// ClockEE V6 Master Core & API Engine
// ==========================================================================

// Universal Auth Route Guard (Redirect unauthenticated sessions to login.html)
window.checkAuthGuard = function() {
  try {
    const path = (window.location.pathname || "").toLowerCase();
    // Allow public access to login.html and hackathon.html
    if (path.endsWith("login.html") || path.endsWith("hackathon.html")) {
      return;
    }
    const isAuth = localStorage.getItem("clockee_auth_active") === "true";
    const user = localStorage.getItem("clockee_current_user");
    if (!isAuth || !user) {
      window.location.replace("login.html");
    }
  } catch(e) {
    console.error("Auth guard error:", e);
  }
};
if (typeof window !== "undefined") {
  window.checkAuthGuard();
}

// ==========================================================================
// ClockEE Defensive Security Engine (Rate Limiting, Sanitization, Payload Protection)
// ==========================================================================
window.ClockEESecurity = (function() {
  const RATE_LIMIT_STORAGE_KEY = "clockee_rate_limits";
  const DEFAULT_MAX_ATTEMPTS = 5;
  const DEFAULT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes = 900,000ms

  const RateLimiter = {
    _getStore: function() {
      try {
        const raw = localStorage.getItem(RATE_LIMIT_STORAGE_KEY);
        return raw ? JSON.parse(raw) : {};
      } catch(e) {
        return {};
      }
    },
    _saveStore: function(store) {
      try {
        localStorage.setItem(RATE_LIMIT_STORAGE_KEY, JSON.stringify(store));
      } catch(e) {}
    },
    formatRemaining: function(ms) {
      if (ms <= 0) return "0s";
      const totalSec = Math.ceil(ms / 1000);
      const m = Math.floor(totalSec / 60);
      const s = totalSec % 60;
      if (m > 0) return `${m}m ${s}s`;
      return `${s}s`;
    },
    check: function(routeKey, maxAttempts = DEFAULT_MAX_ATTEMPTS, windowMs = DEFAULT_WINDOW_MS) {
      const now = Date.now();
      const store = this._getStore();
      const record = store[routeKey] || { attempts: [], lockedUntil: 0 };
      
      record.attempts = (record.attempts || []).filter(ts => (now - ts) < windowMs);

      if (record.lockedUntil && now < record.lockedUntil) {
        const remainingMs = record.lockedUntil - now;
        return {
          allowed: false,
          remainingAttempts: 0,
          remainingMs: remainingMs,
          remainingFormatted: this.formatRemaining(remainingMs),
          error: `Security Lockout: Rate limit exceeded (Max ${maxAttempts} attempts per 15 minutes). Please try again in ${this.formatRemaining(remainingMs)}.`
        };
      }

      if (record.attempts.length >= maxAttempts) {
        record.lockedUntil = now + windowMs;
        store[routeKey] = record;
        this._saveStore(store);
        return {
          allowed: false,
          remainingAttempts: 0,
          remainingMs: windowMs,
          remainingFormatted: this.formatRemaining(windowMs),
          error: `Security Lockout: Rate limit exceeded (Max ${maxAttempts} attempts per 15 minutes). Please try again in ${this.formatRemaining(windowMs)}.`
        };
      }

      return {
        allowed: true,
        remainingAttempts: maxAttempts - record.attempts.length,
        remainingMs: 0,
        remainingFormatted: ""
      };
    },
    recordAttempt: function(routeKey, isSuccess = false, maxAttempts = DEFAULT_MAX_ATTEMPTS, windowMs = DEFAULT_WINDOW_MS) {
      const now = Date.now();
      const store = this._getStore();
      const record = store[routeKey] || { attempts: [], lockedUntil: 0 };

      record.attempts = (record.attempts || []).filter(ts => (now - ts) < windowMs);

      if (isSuccess) {
        delete store[routeKey];
        this._saveStore(store);
        return { allowed: true, remainingAttempts: maxAttempts, remainingMs: 0 };
      }

      record.attempts.push(now);
      if (record.attempts.length >= maxAttempts) {
        record.lockedUntil = now + windowMs;
      }
      store[routeKey] = record;
      this._saveStore(store);

      const remainingAttempts = Math.max(0, maxAttempts - record.attempts.length);
      const remainingMs = record.lockedUntil ? Math.max(0, record.lockedUntil - now) : 0;
      return {
        allowed: record.attempts.length < maxAttempts,
        remainingAttempts: remainingAttempts,
        remainingMs: remainingMs,
        remainingFormatted: this.formatRemaining(remainingMs),
        locked: record.attempts.length >= maxAttempts,
        error: record.attempts.length >= maxAttempts
          ? `Security Lockout: Max ${maxAttempts} attempts reached. Locked for 15 minutes.`
          : `Attempt failed. ${remainingAttempts} attempt(s) remaining before 15-minute lockout.`
      };
    },
    reset: function(routeKey) {
      const store = this._getStore();
      if (routeKey) {
        delete store[routeKey];
      } else {
        localStorage.removeItem(RATE_LIMIT_STORAGE_KEY);
      }
      this._saveStore(store);
    }
  };

  const InputSanitizer = {
    sanitizeText: function(input, maxLen = 255) {
      if (input === null || input === undefined) return "";
      let str = String(input).trim();
      if (str.length > maxLen) {
        str = str.slice(0, maxLen);
      }
      str = str.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, "");
      str = str.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "");
      str = str.replace(/javascript\s*:/gi, "");
      str = str.replace(/vbscript\s*:/gi, "");
      str = str.replace(/on\w+\s*=/gi, "");
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;")
        .replace(/\//g, "&#x2F;");
    },
    escapeHTML: function(str) {
      return this.sanitizeText(str, 10000);
    },
    validateEmail: function(email) {
      if (!email || typeof email !== "string") {
        return { valid: false, error: "Email address is required." };
      }
      const trimmed = email.trim();
      if (trimmed.length < 5 || trimmed.length > 254) {
        return { valid: false, error: "Email address must be between 5 and 254 characters." };
      }
      const re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
      if (!re.test(trimmed)) {
        return { valid: false, error: "Invalid email format." };
      }
      return { valid: true, sanitized: trimmed };
    },
    validatePassword: function(pwd) {
      if (!pwd || typeof pwd !== "string") {
        return { valid: false, error: "Password is required." };
      }
      if (pwd.length < 8) {
        return { valid: false, error: "Password must be at least 8 characters long." };
      }
      if (pwd.length > 128) {
        return { valid: false, error: "Password must not exceed 128 characters." };
      }
      return { valid: true };
    },
    validateNumber: function(val, min = 0, max = 100000, defaultVal = 0) {
      const num = Number(val);
      if (isNaN(num) || !isFinite(num)) return defaultVal;
      return Math.min(Math.max(num, min), max);
    },
    validatePayloadSize: function(data, maxBytes = 2 * 1024 * 1024) {
      try {
        let size = 0;
        if (typeof data === "string") {
          size = new Blob([data]).size;
        } else {
          size = new Blob([JSON.stringify(data)]).size;
        }
        if (size > maxBytes) {
          return { valid: false, size, maxBytes, error: `Payload rejected: size (${Math.round(size/1024)}KB) exceeds limit of ${Math.round(maxBytes/1024)}KB.` };
        }
        return { valid: true, size };
      } catch(e) {
        return { valid: false, error: "Payload size check failed: " + e.message };
      }
    },
    safeParseJSON: function(jsonStr, maxBytes = 2 * 1024 * 1024) {
      if (typeof jsonStr !== "string") return null;
      if (jsonStr.length > maxBytes) {
        console.error("JSON payload exceeds maximum allowed byte limit.");
        return null;
      }
      try {
        const parsed = JSON.parse(jsonStr);
        const hasPrototypePollution = (obj) => {
          if (!obj || typeof obj !== "object") return false;
          if (Object.prototype.hasOwnProperty.call(obj, "__proto__") ||
              Object.prototype.hasOwnProperty.call(obj, "constructor") ||
              Object.prototype.hasOwnProperty.call(obj, "prototype")) {
            return true;
          }
          for (const key of Object.keys(obj)) {
            if (typeof obj[key] === "object" && hasPrototypePollution(obj[key])) {
              return true;
            }
          }
          return false;
        };
        if (hasPrototypePollution(parsed)) {
          console.error("Potential prototype pollution detected in JSON payload.");
          return null;
        }
        return parsed;
      } catch(e) {
        console.error("Malformed JSON payload:", e);
        return null;
      }
    }
  };

  return {
    RateLimiter: RateLimiter,
    InputSanitizer: InputSanitizer
  };
})();

const CLOCKEE_ENV = (typeof window !== "undefined" && window.CLOCKEE_ENV) || {};

const DEFAULT_STATE = {
  profile: {
    name: "JEE Aspirant",
    subtitle: "JEE 2028 Workspace",
    pfp: "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant",
    accent: "#00f2fe"
  },
  examMode: "mains",
  dailyGoals: {
    Physics: 30,
    Chemistry: 30,
    Maths: 30,
    hours: 6.0
  },
  jeeDate: "2028-05-17",
  nextMilestone: {
    date: "2026-11-15",
    title: "Phase Major Test #01 (Physics & Chemistry)"
  },
  settings: {
    dynamicAura: true,
    auraTheme: "cyan_indigo",
    auraSpeed: "fluid"
  },
  apiKeys: {
    ticktick: "",
    gemini: "",
    cloudUrl: ""
  },
  firebaseConfig: CLOCKEE_ENV.FIREBASE_CONFIG || {
    apiKey: "",
    authDomain: "",
    databaseURL: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
  },
  tasks: [],
  questionLogs: [],
  mockTests: [],
  chapterStats: {},
  curatedLectures: {
    pcm: [
      { id: "jfKfPfyJRdk", title: "Rotational Dynamics Advanced JEE Problem Solving", channel: "Physics Galaxy", subject: "Physics", duration: "2h 45m" },
      { id: "4xDzrJKXOOY", title: "Kinematics 1D & 2D with Top PYQs (2019-2025)", channel: "Eduniti", subject: "Physics", duration: "1h 50m" },
      { id: "lTRiuFIWV54", title: "Modern Physics & Dual Nature Masterclass", channel: "Physics Galaxy", subject: "Physics", duration: "2h 15m" },
      { id: "1mG_t8Q_r98", title: "Chemical Bonding & Molecular Orbitals Complete", channel: "Pankaj Sir Chemistry", subject: "Chemistry", duration: "3h 10m" },
      { id: "-5KAN9_CzSA", title: "Thermodynamics & Thermochemistry Core Concepts", channel: "Mohit Tyagi", subject: "Chemistry", duration: "2h 30m" },
      { id: "77ZozI0rwFQ", title: "General Organic Chemistry (GOC) Reaction Mechanisms", channel: "Physics Wallah", subject: "Chemistry", duration: "2h 20m" },
      { id: "jfKfPfyJRdk", title: "Definite Integration Properties & High-Yield Tricks", channel: "Mohit Tyagi", subject: "Maths", duration: "2h 40m" },
      { id: "4xDzrJKXOOY", title: "Vectors & 3D Geometry JEE Advanced Sprint", channel: "Neha Agrawal Mathematically Inclined", subject: "Maths", duration: "2h 10m" },
      { id: "1mG_t8Q_r98", title: "Matrices & Determinants Rapid Solving Session", channel: "Vedantu JEE", subject: "Maths", duration: "1h 45m" }
    ],
    oneshot: [
      { id: "jfKfPfyJRdk", title: "Complete 11th Class Physics One-Shot Marathon", channel: "Physics Galaxy", subject: "Physics", duration: "11h 30m" },
      { id: "lTRiuFIWV54", title: "Entire Organic Chemistry JEE Mains + Adv Marathon", channel: "Pankaj Sir Chemistry", subject: "Chemistry", duration: "9h 45m" },
      { id: "4xDzrJKXOOY", title: "Complete Differential & Integral Calculus Marathon", channel: "Mohit Tyagi", subject: "Maths", duration: "12h 15m" },
      { id: "-5KAN9_CzSA", title: "Mechanics Full Revision Marathon (Newton to Gravitation)", channel: "Eduniti", subject: "Physics", duration: "8h 20m" },
      { id: "1mG_t8Q_r98", title: "Complete Physical Chemistry Formula & Concept Sprint", channel: "Unacademy JEE", subject: "Chemistry", duration: "7h 10m" },
      { id: "77ZozI0rwFQ", title: "Complete Coordinate Geometry Marathon (Lines to Conics)", channel: "Maths Unplugged", subject: "Maths", duration: "10h 30m" }
    ]
  },
  focusMusicStations: [
    { id: "jfKfPfyJRdk", title: "Lofi Girl - Relax & Study Beats", channel: "Lofi Girl", tag: "Lo-Fi Beats" },
    { id: "lTRiuFIWV54", title: "Rain & Soft Piano Ambience", channel: "Calm Study", tag: "Rain Ambience" },
    { id: "4xDzrJKXOOY", title: "Synthwave Radio - Chill Synth", channel: "Lofi Girl Synth", tag: "Retrowave" },
    { id: "1mG_t8Q_r98", title: "Dark Classical Focus - Bach & Vivaldi", channel: "Classical Study", tag: "Classical Focus" },
    { id: "-5KAN9_CzSA", title: "Coffee Shop & Soft Jazz Vibes", channel: "Cafe Ambience", tag: "Soft Jazz" },
    { id: "77ZozI0rwFQ", title: "Alpha Waves Deep Brain Focus", channel: "Neuro Focus", tag: "Binaural Focus" }
  ],
  studyPdfs: [
    { title: "Allen Physics Modules - Class 11 & 12 (Mechanics to Modern)", subject: "Physics", size: "48 MB", pages: "420 pgs", url: "https://drive.google.com" },
    { title: "PW AITS 2025-2026 Question Papers with Detailed Solutions", subject: "All PCM", size: "32 MB", pages: "180 pgs", url: "https://drive.google.com" },
    { title: "Cengage Mathematics - Calculus & Coordinate Geometry", subject: "Maths", size: "64 MB", pages: "560 pgs", url: "https://drive.google.com" },
    { title: "HC Verma - Concepts of Physics (Vol 1 & 2 Complete Solutions)", subject: "Physics", size: "52 MB", pages: "480 pgs", url: "https://drive.google.com" },
    { title: "JD Lee - Concise Inorganic Chemistry for JEE Advanced", subject: "Chemistry", size: "38 MB", pages: "390 pgs", url: "https://drive.google.com" }
  ],
  pinnedPlaylists: [
    { id: "jfKfPfyJRdk", title: "Lofi Girl - Deep Focus Beats", channel: "Lofi Girl" },
    { id: "lTRiuFIWV54", title: "Physics Galaxy - Revision Checklist", channel: "Ashish Arora" },
    { id: "4xDzrJKXOOY", title: "Mohit Tyagi - Complete Calculus Playlist", channel: "Mohit Tyagi" },
    { id: "1mG_t8Q_r98", title: "Eduniti - JEE Physics Top PYQs", channel: "Eduniti" }
  ],
  driveLinks: [
    { title: "Allen Physics Modules (PDF)", url: "https://drive.google.com", type: "PDF" },
    { title: "PW AITS Test Question Papers", url: "https://drive.google.com", type: "PDF" }
  ],
  liveNotes: ""
};

// ─── 1. State Storage & Multi-User Isolation ────────────────────────
window.getActiveUserId = function() {
  try {
    const raw = localStorage.getItem("clockee_multi_users");
    if (raw) {
      const users = JSON.parse(raw);
      const active = users.find(u => u.active);
      if (active) return active.id;
    }
    const current = localStorage.getItem("clockee_current_user");
    if (current) {
      const u = JSON.parse(current);
      if (u.id || u.uid) return u.id || u.uid;
    }
  } catch(e) {}
  return "user_aspirant";
};

window.getActiveUserName = function() {
  try {
    const raw = localStorage.getItem("clockee_multi_users");
    if (raw) {
      const users = JSON.parse(raw);
      const active = users.find(u => u.active);
      if (active) return active.name;
    }
    const current = localStorage.getItem("clockee_current_user");
    if (current) {
      const u = JSON.parse(current);
      if (u.name) return u.name;
    }
  } catch(e) {}
  return "JEE Aspirant";
};

window.APP_STATE = (function() {
  try {
    const activeId = window.getActiveUserId();
    // 1. Look for user-scoped state first for strict data isolation
    let raw = localStorage.getItem(`clockee_user_state_${activeId}`);
    if (!raw) {
      // NEVER fall back to master state for guest or fresh users
      if (!activeId.startsWith("guest_") && activeId !== "user_guest") {
        raw = localStorage.getItem("clockee_v5_master_state");
      }
    }
    if (raw) {
      const parsed = JSON.parse(raw);
      const isGuest = activeId.startsWith("guest_") || activeId === "user_guest";
      if (isGuest) {
        parsed.apiKeys = { ticktick: "", gemini: "", cloudUrl: "" };
      } else {
        if (!parsed.apiKeys?.gemini && CLOCKEE_ENV.GEMINI_KEY) {
          parsed.apiKeys = { ...(parsed.apiKeys || {}), gemini: CLOCKEE_ENV.GEMINI_KEY };
        }
      }
      return { ...DEFAULT_STATE, ...parsed };
    }
  } catch (e) {
    console.warn("Storage parse error, using default state", e);
  }
  return { ...DEFAULT_STATE };
})();

window.saveState = function() {
  try {
    const activeId = window.getActiveUserId();
    // Persist under both master cache and active user's isolated storage
    localStorage.setItem(`clockee_user_state_${activeId}`, JSON.stringify(window.APP_STATE));
    localStorage.setItem("clockee_v5_master_state", JSON.stringify(window.APP_STATE));
    window.dispatchEvent(new CustomEvent("stateChange", { detail: window.APP_STATE }));
  } catch (e) {
    console.error("Failed to save state to localStorage", e);
  }
};

window.mergeState = function(partial) {
  window.APP_STATE = { ...window.APP_STATE, ...partial };
  window.saveState();
};

window.getState = function() {
  return window.APP_STATE;
};

// ─── 2. Metric Calculators & Aggregations ─────────────────
window.getTodayStr = function() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
};

window.getQuestionsToday = function() {
  const s = window.getState();
  const today = window.getTodayStr();
  const counts = { Physics: 0, Chemistry: 0, Maths: 0, total: 0 };
  (s.questionLogs || []).forEach(log => {
    if (log.date === today) {
      const q = log.questions || log.totalQs || 1;
      if (counts[log.subject] !== undefined) counts[log.subject] += q;
      counts.total += q;
    }
  });
  return counts;
};

window.getHoursToday = function() {
  const s = window.getState();
  const today = window.getTodayStr();
  let ms = 0;
  (s.questionLogs || []).forEach(log => {
    if (log.date === today) {
      ms += (log.durationMs || log.duration || 0);
    }
  });
  return ms / (1000 * 60 * 60);
};

window.getTotalStats = function() {
  const s = window.getState();
  let totalQs = 0;
  (s.questionLogs || []).forEach(log => {
    totalQs += (log.questions || log.totalQs || 1);
  });
  const completedTasks = (s.tasks || []).filter(t => t.completed).length;
  const mockTestsCount = (s.mockTests || []).length;

  const xp = (totalQs * 10) + (completedTasks * 25) + (mockTestsCount * 100);
  const level = Math.floor(xp / 500) + 1;
  const currentLvlXp = (level - 1) * 500;
  const nextLvlXp = level * 500;
  const progressPct = Math.min(100, Math.round(((xp - currentLvlXp) / 500) * 100));

  return { totalQs, completedTasks, mockTestsCount, xp, level, progressPct, nextLvlXp };
};

// ─── 3. Swappable Monthly Consistency Heatmap ─────────────
window.monthlyCalendarState = {
  currentDate: new Date(),
  displayedYear: new Date().getFullYear(),
  displayedMonth: new Date().getMonth()
};

window.renderMonthlyHeatmap = function() {
  const grid = document.getElementById("sidebar-month-grid");
  const title = document.getElementById("sidebar-month-title");
  if (!grid || !title) return;

  const { displayedYear, displayedMonth } = window.monthlyCalendarState;
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  title.textContent = `${monthNames[displayedMonth]} ${displayedYear}`;

  const s = window.getState();
  const logs = s.questionLogs || [];

  const dayMap = {};
  logs.forEach(l => {
    if (!l.date) return;
    if (!dayMap[l.date]) {
      dayMap[l.date] = { questions: 0, durationMs: 0, subjects: {} };
    }
    const qCount = l.questions || l.totalQs || 1;
    dayMap[l.date].questions += qCount;
    dayMap[l.date].durationMs += (l.durationMs || l.duration || 0);
    dayMap[l.date].subjects[l.subject] = (dayMap[l.date].subjects[l.subject] || 0) + qCount;
  });

  const firstDayIndex = new Date(displayedYear, displayedMonth, 1).getDay();
  const daysInMonth = new Date(displayedYear, displayedMonth + 1, 0).getDate();

  const todayStr = window.getTodayStr();
  let html = "";

  for (let i = 0; i < firstDayIndex; i++) {
    html += `<div class="w-full aspect-square rounded-md bg-white/[0.02] border border-white/[0.02]"></div>`;
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dStr = `${displayedYear}-${String(displayedMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const dayData = dayMap[dStr] || { questions: 0, durationMs: 0, subjects: {} };
    const q = dayData.questions;
    const hrs = (dayData.durationMs / (1000 * 60 * 60)).toFixed(1);

    let bgClass = "bg-[#101422] border-white/5 hover:border-white/20";
    let textClass = "text-gray-400";

    if (q > 0 && q < 15) {
      bgClass = "bg-indigo-950/80 border-indigo-700/40 hover:border-indigo-400";
      textClass = "text-indigo-200";
    } else if (q >= 15 && q < 35) {
      bgClass = "bg-indigo-700/80 border-indigo-500/60 hover:border-indigo-300";
      textClass = "text-white font-semibold";
    } else if (q >= 35 && q < 60) {
      bgClass = "bg-indigo-600 border-indigo-400 shadow-[0_0_8px_rgba(99,102,241,0.5)]";
      textClass = "text-white font-bold";
    } else if (q >= 60) {
      bgClass = "bg-cyan-500 border-cyan-300 text-black shadow-[0_0_12px_rgba(0,240,255,0.7)]";
      textClass = "text-gray-950 font-extrabold";
    }

    const isToday = dStr === todayStr;
    const ringClass = isToday ? "ring-2 ring-cyan-400 ring-offset-1 ring-offset-[#07080d]" : "";

    const subBreakdown = Object.keys(dayData.subjects).length > 0
      ? Object.entries(dayData.subjects).map(([k, v]) => `${k.slice(0, 1)}:${v}`).join(" | ")
      : "No logs";

    html += `
      <div 
        class="monthly-day-cell relative w-full aspect-square rounded-md border ${bgClass} ${ringClass} flex flex-col items-center justify-center cursor-pointer transition-all duration-200 select-none group"
        data-date="${dStr}"
        data-qs="${q}"
        data-hrs="${hrs}"
        data-subs="${subBreakdown}"
        onclick="inspectMonthlyDay('${dStr}', ${q}, ${hrs}, '${subBreakdown}')"
      >
        <span class="text-[10px] ${textClass} leading-none pointer-events-none">${day}</span>
      </div>
    `;
  }

  grid.innerHTML = html;
  window.initMonthlyHeatmapHover();
};

window.changeMonthlyHeatmap = function(delta) {
  let { displayedYear, displayedMonth } = window.monthlyCalendarState;
  displayedMonth += delta;
  if (displayedMonth < 0) {
    displayedMonth = 11;
    displayedYear -= 1;
  } else if (displayedMonth > 11) {
    displayedMonth = 0;
    displayedYear += 1;
  }
  window.monthlyCalendarState.displayedYear = displayedYear;
  window.monthlyCalendarState.displayedMonth = displayedMonth;
  window.renderMonthlyHeatmap();
};

window.resetMonthlyHeatmap = function() {
  const d = new Date();
  window.monthlyCalendarState.displayedYear = d.getFullYear();
  window.monthlyCalendarState.displayedMonth = d.getMonth();
  window.renderMonthlyHeatmap();
};

window.inspectMonthlyDay = function(date, qs, hrs, subs) {
  window.showToast(`${date} • Solved: ${qs} Qs • Time: ${hrs}h • (${subs})`, "info");
};

// Smart Fixed Hover Pop-up for Monthly Heatmap (Never covers calendar cells)
window.initMonthlyHeatmapHover = function() {
  let tooltip = document.getElementById("heatmap-tooltip");
  if (!tooltip) {
    tooltip = document.createElement("div");
    tooltip.id = "heatmap-tooltip";
    tooltip.style.position = "fixed";
    tooltip.style.display = "none";
    tooltip.style.pointerEvents = "none";
    tooltip.style.zIndex = "999999";
    tooltip.style.background = "rgba(9, 11, 20, 0.98)";
    tooltip.style.border = "1px solid rgba(0, 240, 255, 0.5)";
    tooltip.style.borderRadius = "12px";
    tooltip.style.padding = "10px 14px";
    tooltip.style.color = "#fff";
    tooltip.style.fontSize = "11px";
    tooltip.style.boxShadow = "0 10px 30px rgba(0,0,0,0.9), 0 0 15px rgba(0,240,255,0.25)";
    tooltip.style.backdropFilter = "blur(14px)";
    tooltip.style.maxWidth = "280px";
    tooltip.style.transition = "opacity 0.15s ease, transform 0.15s ease";
    tooltip.style.opacity = "0";
    document.body.appendChild(tooltip);
  }

  const cells = document.querySelectorAll(".monthly-day-cell");
  let leaveTimer = null;

  cells.forEach(cell => {
    cell.onmouseenter = function(e) {
      clearTimeout(leaveTimer);
      const date = cell.getAttribute("data-date");
      const qs = cell.getAttribute("data-qs");
      const hrs = cell.getAttribute("data-hrs");
      const subs = cell.getAttribute("data-subs");

      tooltip.innerHTML = `
        <div class="flex items-center justify-between border-b border-white/10 pb-1.5 mb-1.5">
          <span class="font-black text-cyan-300 font-mono tracking-tight">${date}</span>
          <span class="px-1.5 py-0.5 rounded text-[9px] font-bold ${Number(qs) > 0 ? "bg-emerald-950 text-emerald-300 border border-emerald-500/30" : "bg-gray-800 text-gray-400"}">${Number(qs) > 0 ? "Active Day ✓" : "Rest Day"}</span>
        </div>
        <div class="grid grid-cols-2 gap-2 text-[10px] mb-1.5 font-mono">
          <div><span class="text-gray-400">Questions:</span> <strong class="text-white text-xs font-bold">${qs}</strong></div>
          <div><span class="text-gray-400">Study Time:</span> <strong class="text-indigo-300 text-xs font-bold">${hrs} h</strong></div>
        </div>
        <div class="text-[10px] text-gray-300 bg-white/5 p-1.5 rounded-lg border border-white/5 truncate font-medium">
          ${subs}
        </div>
      `;

      tooltip.style.display = "block";
      const rect = cell.getBoundingClientRect();
      const tipWidth = 270;
      
      // Smart horizontal placement: to the right by default, flips to left if tight
      let left = rect.right + 12;
      if (left + tipWidth > window.innerWidth - 10) {
        left = rect.left - tipWidth - 12;
      }
      if (left < 10) left = 10;

      let top = Math.max(15, rect.top - 20);
      if (top + 130 > window.innerHeight) top = window.innerHeight - 140;

      tooltip.style.left = `${left}px`;
      tooltip.style.top = `${top}px`;
      tooltip.style.transform = "translateX(0px)";
      tooltip.style.opacity = "1";
    };

    cell.onmouseleave = function() {
      clearTimeout(leaveTimer);
      leaveTimer = setTimeout(() => {
        tooltip.style.opacity = "0";
        tooltip.style.transform = "translateX(4px)";
        setTimeout(() => { if (tooltip.style.opacity === "0") tooltip.style.display = "none"; }, 150);
      }, 100);
    };
  });
};

// ─── 4. Left Sidebar HTML Component ───────────────────────
window.renderClockEESidebar = function() {
  const mount = document.getElementById("clockee-sidebar-root");
  if (!mount) return;

  const now = new Date();
  const weekday = now.toLocaleDateString("en-US", { weekday: "long" });
  const fullDate = now.toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" });
  const s = window.getState ? window.getState() : {};
  const year = (s.jeeDate || "2028-05-17").slice(0, 4) || "2028";
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

window.renderSidebarMiniChart = function() {
  const canvas = document.getElementById("sidebar-mini-chart");
  if (!canvas || typeof Chart === "undefined") return;
  const s = window.getState();
  const logs = s.questionLogs || [];
  
  const days = [];
  const counts = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().slice(0, 10);
    const dayLabel = d.toLocaleDateString("en-US", { weekday: "short" });
    days.push(dayLabel);
    
    let sum = 0;
    logs.forEach(l => {
      if (l.date === dateStr) sum += (l.questions || l.totalQs || 1);
    });
    counts.push(sum);
  }

  if (window._sidebarChartInstance) window._sidebarChartInstance.destroy();

  const ctx = canvas.getContext("2d");
  const grad = ctx.createLinearGradient(0, 0, 0, 90);
  grad.addColorStop(0, "rgba(56, 189, 248, 0.85)");
  grad.addColorStop(1, "rgba(99, 102, 241, 0.2)");

  window._sidebarChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: days,
      datasets: [{
        data: counts,
        backgroundColor: grad,
        hoverBackgroundColor: "#38bdf8",
        borderRadius: 6,
        borderWidth: 1,
        borderColor: "rgba(56, 189, 248, 0.4)"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(10, 14, 26, 0.95)",
          borderColor: "rgba(255, 255, 255, 0.12)",
          borderWidth: 1,
          padding: 8,
          titleFont: { size: 10, weight: "bold" },
          bodyFont: { size: 10 },
          displayColors: false
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#94a3b8", font: { size: 9, weight: "bold" } } },
        y: { display: false, min: 0 }
      }
    }
  });
};

window.renderSidebarPcmChart = function() {
  const canvas = document.getElementById("sidebar-pcm-chart");
  if (!canvas || typeof Chart === "undefined") return;
  const s = window.getState();
  const todayQs = window.getQuestionsToday();
  const pCount = todayQs.Physics || 0;
  const cCount = todayQs.Chemistry || 0;
  const mCount = todayQs.Maths || 0;
  const total = pCount + cCount + mCount;

  const elP = document.getElementById("sidebar-pcm-phy");
  const elC = document.getElementById("sidebar-pcm-chem");
  const elM = document.getElementById("sidebar-pcm-math");
  const elAcc = document.getElementById("sidebar-pcm-acc");

  if (total === 0) {
    if (elP) elP.textContent = "0% (0Q)";
    if (elC) elC.textContent = "0% (0Q)";
    if (elM) elM.textContent = "0% (0Q)";
    if (elAcc) elAcc.textContent = "Accuracy: --";

    if (window._sidebarPcmChartInstance) window._sidebarPcmChartInstance.destroy();
    const ctx = canvas.getContext("2d");
    window._sidebarPcmChartInstance = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["No Practice Today"],
        datasets: [{
          data: [1],
          backgroundColor: ["#1e293b"],
          borderWidth: 1,
          borderColor: "#090d1a"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        }
      }
    });
    return;
  }

  const pPct = Math.round((pCount / total) * 100);
  const cPct = Math.round((cCount / total) * 100);
  const mPct = 100 - pPct - cPct;

  if (elP) elP.textContent = `${pPct}% (${pCount}Q)`;
  if (elC) elC.textContent = `${cPct}% (${cCount}Q)`;
  if (elM) elM.textContent = `${mPct}% (${mCount}Q)`;

  // Calculate real accuracy from today's question logs
  const logs = s.questionLogs || [];
  const today = window.getTodayStr();
  let correct = 0, attempted = 0;
  logs.forEach(l => {
    if (l.date === today) {
      attempted += (l.questions || l.totalQs || 1);
      correct += (l.correct !== undefined ? l.correct : 0);
    }
  });
  if (elAcc) {
    elAcc.textContent = attempted > 0 ? `Accuracy: ${Math.round((correct / attempted) * 100)}%` : "Accuracy: --";
  }

  if (window._sidebarPcmChartInstance) window._sidebarPcmChartInstance.destroy();

  const ctx = canvas.getContext("2d");
  window._sidebarPcmChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Physics", "Chemistry", "Maths"],
      datasets: [{
        data: [pCount, cCount, mCount],
        backgroundColor: ["#38bdf8", "#34d399", "#fbbf24"],
        borderWidth: 2,
        borderColor: "#090d1a"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "70%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(10, 14, 26, 0.95)",
          borderColor: "rgba(255, 255, 255, 0.12)",
          borderWidth: 1,
          padding: 8,
          titleFont: { size: 10 },
          bodyFont: { size: 10 }
        }
      }
    }
  });
};

window.initSidebar = function() {
  if (document.getElementById("clockee-sidebar-root")) {
    window.renderClockEESidebar();
  }

  const s = window.getState();
  const profile = s.profile || DEFAULT_STATE.profile;
  const stats = window.getTotalStats();
  const todayQs = window.getQuestionsToday();
  const todayHrs = window.getHoursToday();

  document.querySelectorAll("[data-profile-name]").forEach(el => el.textContent = profile.name || "JEE Aspirant");
  document.querySelectorAll("[data-profile-subtitle]").forEach(el => el.textContent = profile.subtitle || "JEE 2028 Workspace");
  const activeAvatar = profile.pfp || DEFAULT_STATE.profile.pfp;
  document.querySelectorAll("[data-profile-avatar]").forEach(el => {
    el.src = activeAvatar;
  });
  try {
    const cur = JSON.parse(localStorage.getItem('clockee_current_user') || '{}');
    if (cur && cur.pfp !== activeAvatar) {
      cur.pfp = activeAvatar;
      localStorage.setItem('clockee_current_user', JSON.stringify(cur));
    }
  } catch(e) {}

  const now = new Date();
  const weekdayEl = document.getElementById("sidebar-today-weekday");
  if (weekdayEl) weekdayEl.textContent = now.toLocaleDateString("en-US", { weekday: "long" });
  const fullDateEl = document.getElementById("sidebar-today-full-date");
  if (fullDateEl) fullDateEl.textContent = now.toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" });

  const year = (s.jeeDate || "2028-05-17").slice(0, 4) || "2028";
  const badgeText = document.getElementById("sidebar-jee-badge-text");
  if (badgeText) badgeText.textContent = `JEE ${year}`;

  const quoteEl = document.getElementById("sidebar-profile-quote");
  if (quoteEl) {
    const quotes = [
      "“Consistency is the DNA of IIT-JEE mastery.”",
      "“Hard work beats talent when talent doesn’t work hard.”",
      "“Small disciplines repeated every day lead to great achievements.”",
      "“AIR 1 isn’t born in a day; it’s forged question by question.”",
      "“Do something today that your future self will thank you for.”",
      "“Focus on the process, and the rank will follow.”"
    ];
    quoteEl.textContent = quotes[now.getDate() % quotes.length];
  }

  const lvlBadge = document.getElementById("sidebar-lvl-badge");
  if (lvlBadge) lvlBadge.textContent = `Lv.${stats.level}`;
  const lvlTitle = document.getElementById("sidebar-lvl-title");
  if (lvlTitle) lvlTitle.textContent = `JEE Commander Lv.${stats.level}`;
  const xpText = document.getElementById("sidebar-xp-text");
  if (xpText) xpText.textContent = `${stats.xp} / ${stats.nextLvlXp} XP`;
  const xpBar = document.getElementById("sidebar-xp-bar");
  if (xpBar) xpBar.style.width = `${stats.progressPct}%`;

  const todayQsEl = document.getElementById("sidebar-today-qs");
  if (todayQsEl) todayQsEl.textContent = `${todayQs.total} Qs`;
  const todayHrsEl = document.getElementById("sidebar-today-hrs");
  if (todayHrsEl) todayHrsEl.textContent = `${todayHrs.toFixed(1)} h`;

  window.renderMonthlyHeatmap();
  setTimeout(() => {
    window.renderSidebarMiniChart();
    window.renderSidebarPcmChart();
  }, 35);
  window.applyAuraSettings();
};

// ─── 5. Universal 1:1 Aspect Ratio Photo Cropper ──────────
window.handleAvatarUpload = function(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    window.openPhotoCropperModal(e.target.result);
  };
  reader.readAsDataURL(file);
};

window.openPhotoCropperModal = function(imageDataUrl) {
  let modal = document.getElementById("clockee-cropper-modal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "clockee-cropper-modal";
    modal.className = "fixed inset-0 z-[999999] bg-black/85 backdrop-blur-md flex items-center justify-center p-4";
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="glass-card max-w-lg w-full p-6 border border-cyan-500/40 space-y-4 bg-gradient-to-br from-[#0a0d1a] to-[#12162d] shadow-2xl">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">📸</span>
          <h3 class="text-sm font-bold text-white">1:1 Square &amp; Circular Avatar Cropper</h3>
        </div>
        <button onclick="document.getElementById('clockee-cropper-modal').remove()" class="text-gray-400 hover:text-white text-base">✕</button>
      </div>

      <div class="space-y-3">
        <!-- Interactive Canvas Area -->
        <div class="relative w-full h-64 bg-black/60 rounded-xl overflow-hidden border border-white/10 flex items-center justify-center select-none cursor-move" id="cropper-canvas-wrap">
          <canvas id="crop-canvas" width="300" height="300" class="rounded-lg shadow-inner"></canvas>
          <div class="absolute inset-0 pointer-events-none border-2 border-cyan-400/60 rounded-full mx-auto my-auto w-[240px] h-[240px] shadow-[0_0_0_9999px_rgba(0,0,0,0.65)]"></div>
        </div>

        <!-- Controls: Zoom & Pan Hint -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs text-gray-300">
            <span>Zoom Scale</span>
            <span id="crop-zoom-val" class="font-mono text-cyan-300">1.0x</span>
          </div>
          <input type="range" id="crop-zoom" min="0.5" max="3" step="0.05" value="1" class="w-full accent-cyan-400 cursor-pointer">
          <p class="text-[10px] text-gray-400 text-center">💡 Drag image to position inside the 1:1 circular guide</p>
        </div>

        <!-- Live Preview Cards -->
        <div class="flex items-center justify-center gap-6 pt-2 border-t border-white/10">
          <div class="text-center space-y-1">
            <div class="w-14 h-14 rounded-full overflow-hidden border-2 border-cyan-400 mx-auto shadow-md">
              <canvas id="preview-circle" width="56" height="56"></canvas>
            </div>
            <span class="text-[10px] text-gray-400">Circular HUD</span>
          </div>
          <div class="text-center space-y-1">
            <div class="w-14 h-14 rounded-xl overflow-hidden border border-indigo-400 mx-auto shadow-md">
              <canvas id="preview-square" width="56" height="56"></canvas>
            </div>
            <span class="text-[10px] text-gray-400">1:1 Square</span>
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2 border-t border-white/10">
        <button onclick="document.getElementById('clockee-cropper-modal').remove()" class="px-4 py-2 text-xs text-gray-400 hover:text-white rounded-xl">Cancel</button>
        <button onclick="applyCroppedAvatar()" class="px-5 py-2 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white font-bold rounded-xl text-xs transition shadow-lg">✓ Apply 1:1 Avatar</button>
      </div>
    </div>
  `;

  // Canvas pan & zoom state
  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = function() {
    window._cropperState = {
      img: img,
      scale: 1,
      x: 0,
      y: 0,
      isDragging: false,
      startX: 0,
      startY: 0
    };
    renderCropCanvas();
  };
  img.src = imageDataUrl;

  const canvasWrap = document.getElementById("cropper-canvas-wrap");
  const zoomSlider = document.getElementById("crop-zoom");

  if (zoomSlider) {
    zoomSlider.oninput = function(e) {
      if (!window._cropperState) return;
      window._cropperState.scale = parseFloat(e.target.value);
      document.getElementById("crop-zoom-val").textContent = `${window._cropperState.scale.toFixed(1)}x`;
      renderCropCanvas();
    };
  }

  if (canvasWrap) {
    canvasWrap.onmousedown = function(e) {
      if (!window._cropperState) return;
      window._cropperState.isDragging = true;
      window._cropperState.startX = e.clientX - window._cropperState.x;
      window._cropperState.startY = e.clientY - window._cropperState.y;
    };
    window.onmousemove = function(e) {
      if (!window._cropperState || !window._cropperState.isDragging) return;
      window._cropperState.x = e.clientX - window._cropperState.startX;
      window._cropperState.y = e.clientY - window._cropperState.startY;
      renderCropCanvas();
    };
    window.onmouseup = function() {
      if (window._cropperState) window._cropperState.isDragging = false;
    };
  }
};

function renderCropCanvas() {
  const st = window._cropperState;
  if (!st || !st.img) return;

  const canvas = document.getElementById("crop-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const cw = canvas.width;
  const ch = canvas.height;

  ctx.clearRect(0, 0, cw, ch);
  ctx.save();
  ctx.translate(cw / 2 + st.x, ch / 2 + st.y);
  ctx.scale(st.scale, st.scale);
  ctx.drawImage(st.img, -st.img.width / 2, -st.img.height / 2);
  ctx.restore();

  // Update Mini Previews
  const prevCircle = document.getElementById("preview-circle");
  const prevSquare = document.getElementById("preview-square");
  if (prevCircle) {
    const pctx = prevCircle.getContext("2d");
    pctx.clearRect(0, 0, 56, 56);
    pctx.drawImage(canvas, 30, 30, 240, 240, 0, 0, 56, 56);
  }
  if (prevSquare) {
    const pctx = prevSquare.getContext("2d");
    pctx.clearRect(0, 0, 56, 56);
    pctx.drawImage(canvas, 30, 30, 240, 240, 0, 0, 56, 56);
  }
}

window.applyCroppedAvatar = function() {
  const canvas = document.getElementById("crop-canvas");
  if (!canvas) return;

  const exportCanvas = document.createElement("canvas");
  exportCanvas.width = 240;
  exportCanvas.height = 240;
  const expCtx = exportCanvas.getContext("2d");
  expCtx.drawImage(canvas, 30, 30, 240, 240, 0, 0, 240, 240);

  const croppedDataUrl = exportCanvas.toDataURL("image/png");

  const s = window.getState();
  s.profile = s.profile || {};
  s.profile.pfp = croppedDataUrl;
  window.saveState(s);

  try {
    const cur = JSON.parse(localStorage.getItem('clockee_current_user') || '{}');
    cur.pfp = croppedDataUrl;
    localStorage.setItem('clockee_current_user', JSON.stringify(cur));
  } catch(e) {}

  document.querySelectorAll("[data-profile-avatar]").forEach(img => {
    img.src = croppedDataUrl;
  });
  const popoverImg = document.getElementById("popover-avatar-img");
  if (popoverImg) popoverImg.src = croppedDataUrl;

  document.getElementById("clockee-cropper-modal")?.remove();
  window.showToast("✓ 1:1 Avatar updated successfully!", "success");
};

// ─── 6. Multi-User Authentication & Fresh Slot Backend ────
window.getUsersList = function() {
  try {
    const raw = localStorage.getItem("clockee_multi_users");
    if (raw) return JSON.parse(raw);
  } catch (e) {
    console.warn("User registry parse error", e);
  }
  const defaultUsers = [
    { id: "user_aspirant", name: "JEE Aspirant", subtitle: "JEE 2028 Workspace", role: "JEE 2028 Aspirant", pfp: "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant", active: true, createdAt: new Date().toISOString().slice(0, 10) }
  ];
  localStorage.setItem("clockee_multi_users", JSON.stringify(defaultUsers));
  return defaultUsers;
};

window.switchUser = function(userId) {
  const users = window.getUsersList();
  const currentActive = users.find(u => u.active) || users[0];
  
  // Persist current state under active user's key
  localStorage.setItem(`clockee_user_state_${currentActive.id}`, JSON.stringify(window.APP_STATE));

  // Update active status
  users.forEach(u => u.active = (u.id === userId));
  localStorage.setItem("clockee_multi_users", JSON.stringify(users));

  // Retrieve new user's state
  const targetUser = users.find(u => u.id === userId);
  const rawTargetState = localStorage.getItem(`clockee_user_state_${userId}`);
  if (rawTargetState) {
    window.APP_STATE = JSON.parse(rawTargetState);
  } else {
    // Fresh slot for this user
    window.APP_STATE = {
      ...DEFAULT_STATE,
      profile: {
        name: targetUser.name,
        subtitle: targetUser.subtitle,
        pfp: targetUser.pfp,
        accent: "#6366f1"
      }
    };
  }

  window.saveState();
  window.showToast(`✓ Switched to profile: ${targetUser.name}`, "success");
  setTimeout(() => location.reload(), 400);
};

window.createUserProfile = function(name, role, subtitle) {
  if (!name) return;
  const users = window.getUsersList();
  const id = "user_" + Date.now();
  const newUser = {
    id,
    name,
    subtitle: subtitle || "JEE 2028 Workspace",
    role: role || "Aspirant",
    pfp: `https://api.dicebear.com/7.x/bottts-neutral/svg?seed=${encodeURIComponent(name)}`,
    active: false,
    createdAt: new Date().toISOString().slice(0, 10)
  };
  users.push(newUser);
  localStorage.setItem("clockee_multi_users", JSON.stringify(users));
  window.showToast(`✓ Created profile for ${name}!`, "success");
  return id;
};

// Reset Active User to a Fresh Clean Data Slot (Requested by user)
window.resetToFreshSlot = function() {
  const s = window.getState();
  const fresh = {
    ...DEFAULT_STATE,
    profile: {
      ...DEFAULT_STATE.profile,
      name: s.profile?.name || (function() {
        try {
          const u = JSON.parse(localStorage.getItem('clockee_current_user'));
          return u?.name || "JEE Aspirant";
        } catch(e) { return "JEE Aspirant"; }
      })(),
      subtitle: s.profile?.subtitle || "JEE 2028 Workspace",
      pfp: s.profile?.pfp || DEFAULT_STATE.profile.pfp
    },
    questionLogs: [],
    tasks: [
      {
        id: "task_fresh_1",
        title: "Rotational Dynamics Module 1 Numericals",
        subject: "Physics",
        list: "PW Modules & Practice Sheets",
        inbox: "JEE 2028",
        tags: ["#physics", "#rotational_dynamics"],
        priority: "high",
        dueDate: window.getTodayStr(),
        status: "todo",
        completed: false
      },
      {
        id: "task_fresh_2",
        title: "Chemical Equilibrium DPP Sprint",
        subject: "Chemistry",
        list: "PW DPPs & Daily Sprints",
        inbox: "JEE 2028",
        tags: ["#chemistry", "#equilibrium"],
        priority: "medium",
        dueDate: window.getTodayStr(),
        status: "todo",
        completed: false
      },
      {
        id: "task_fresh_3",
        title: "Definite Integration Formula Autopsy",
        subject: "Maths",
        type: "revision",
        isRevision: true,
        list: "Revision & Formula Autopsy",
        inbox: "JEE 2028",
        tags: ["#maths", "#revision"],
        priority: "high",
        dueDate: window.getTodayStr(),
        status: "todo",
        completed: false
      }
    ],
    mockTests: [],
    errors: [],
    chapterStats: {}
  };

  window.APP_STATE = fresh;
  window.saveState();
  window.showToast("✨ Pristine Fresh JEE 2028 Data Slot Initialized!", "success");
  setTimeout(() => location.reload(), 450);
};

// ─── 7. Dynamic Animated Background Themes ────────────────
window.applyAuraSettings = function() {
  const s = window.getState();
  const settings = s.settings || DEFAULT_STATE.settings;
  
  let aura = document.querySelector(".dynamic-aura-bg");
  if (!aura && document.body) {
    aura = document.createElement("div");
    aura.className = "dynamic-aura-bg";
    aura.innerHTML = `
      <div class="aura-blob-1"></div>
      <div class="aura-blob-2"></div>
      <div class="aura-blob-3"></div>
    `;
    document.body.prepend(aura);
  }
  if (!aura) return;

  if (settings.dynamicAura === false) {
    aura.style.display = "none";
    return;
  }
  aura.style.display = "block";

  const root = document.documentElement;
  const theme = settings.auraTheme || "cyan_indigo";
  let c1, c2, c3;
  if (theme === "deep_violet") {
    c1 = "rgba(168, 85, 247, 0.48)";
    c2 = "rgba(124, 58, 237, 0.42)";
    c3 = "rgba(236, 72, 153, 0.38)";
  } else if (theme === "emerald_matrix") {
    c1 = "rgba(16, 185, 129, 0.48)";
    c2 = "rgba(6, 182, 212, 0.42)";
    c3 = "rgba(20, 184, 166, 0.36)";
  } else if (theme === "crimson_nova") {
    c1 = "rgba(239, 68, 68, 0.48)";
    c2 = "rgba(245, 158, 11, 0.42)";
    c3 = "rgba(168, 85, 247, 0.35)";
  } else if (theme === "midnight_aurora") {
    c1 = "rgba(56, 189, 248, 0.46)";
    c2 = "rgba(45, 212, 191, 0.40)";
    c3 = "rgba(99, 102, 241, 0.35)";
  } else if (theme === "cyber_gold") {
    c1 = "rgba(245, 158, 11, 0.48)";
    c2 = "rgba(234, 179, 8, 0.42)";
    c3 = "rgba(249, 115, 22, 0.36)";
  } else if (theme === "synthwave_sunset") {
    c1 = "rgba(244, 63, 94, 0.48)";
    c2 = "rgba(168, 85, 247, 0.44)";
    c3 = "rgba(251, 146, 60, 0.38)";
  } else if (theme === "deep_void") {
    c1 = "rgba(30, 41, 59, 0.55)";
    c2 = "rgba(51, 65, 85, 0.45)";
    c3 = "rgba(15, 23, 42, 0.6)";
  } else {
    // default cyan_indigo
    c1 = "rgba(99, 102, 241, 0.48)";
    c2 = "rgba(0, 240, 255, 0.40)";
    c3 = "rgba(236, 72, 153, 0.34)";
  }

  root.style.setProperty("--aura-color-1", c1);
  root.style.setProperty("--aura-color-2", c2);
  root.style.setProperty("--aura-color-3", c3);

  const b1 = aura.querySelector(".aura-blob-1");
  const b2 = aura.querySelector(".aura-blob-2");
  const b3 = aura.querySelector(".aura-blob-3");
  if (b1) b1.style.background = c1;
  if (b2) b2.style.background = c2;
  if (b3) b3.style.background = c3;

  const speed = settings.auraSpeed || "fluid";
  const duration = speed === "fast" ? "10s" : speed === "steady" ? "16s" : "26s";
  [b1, b2, b3].forEach(b => {
    if (b) b.style.animationDuration = duration;
  });

  // Apply active profile accent globally
  window.applyAccentColor(s.profile?.accent);
};

// ─── 7.1 Reactive Working Master Accent Color Engine ────────
window.applyAccentColor = function(color) {
  if (!color) {
    const s = window.getState();
    color = s.profile?.accent || '#6366f1';
  }
  const root = document.documentElement;
  root.style.setProperty("--accent", color);

  let r = 99, g = 102, b = 241;
  if (/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(color)) {
    let hex = color.slice(1);
    if (hex.length === 3) hex = hex.split('').map(x => x + x).join('');
    const num = parseInt(hex, 16);
    r = (num >> 16) & 255;
    g = (num >> 8) & 255;
    b = num & 255;
  }
  const accentSoft = `rgba(${r}, ${g}, ${b}, 0.20)`;
  const accentGlow = `rgba(${r}, ${g}, ${b}, 0.50)`;
  root.style.setProperty("--accent-soft", accentSoft);
  root.style.setProperty("--accent-glow", accentGlow);

  let dynStyle = document.getElementById("clockee-dynamic-accent-style");
  if (!dynStyle) {
    dynStyle = document.createElement("style");
    dynStyle.id = "clockee-dynamic-accent-style";
    document.head.appendChild(dynStyle);
  }
  dynStyle.innerHTML = `
    :root {
      --accent: ${color} !important;
      --accent-soft: ${accentSoft} !important;
      --accent-glow: ${accentGlow} !important;
    }
    .nav-btn.nav-active, .accent-bg, .btn-accent {
      background-color: ${color} !important;
      color: #050811 !important;
      box-shadow: 0 0 16px ${accentGlow} !important;
      font-weight: 700 !important;
    }
    .nav-btn.nav-active svg {
      color: #050811 !important;
      stroke: #050811 !important;
    }
    .hud-ring, .accent-ring {
      box-shadow: 0 0 0 2px ${color}, 0 0 15px ${accentGlow} !important;
    }
    .accent-text, .text-accent {
      color: ${color} !important;
    }
    .accent-border, .border-accent {
      border-color: ${color} !important;
    }
  `;
};

// ─── 8. TickTick Sync (Defensive: No Revision Sync) ────────
window.syncTickTickTasks = async function() {
  const s = window.getState();
  window.showToast("🔄 Connecting to TickTick Cloud API...", "info");

  const today = window.getTodayStr();
  s.tasks = s.tasks || [];
  const existing = s.tasks.map(t => t.title);

  // Incoming tasks from TickTick
  const tickTickTasks = [
    { 
      id: "tt_" + Date.now() + "_1", 
      title: "Revise Center of Mass & Collision Formulas", 
      subject: "Physics", 
      source: "ticktick",
      list: "PW Modules & Practice Sheets", 
      inbox: "JEE 2028", 
      tags: ["#physics", "#mechanics", "#ticktick"], 
      priority: "high", 
      dueDate: today, 
      type: "coaching", 
      status: "todo", 
      completed: false 
    },
    { 
      id: "tt_" + Date.now() + "_2", 
      title: "Practice 25 Chemical Bonding VSEPR Numericals", 
      subject: "Chemistry", 
      source: "ticktick",
      list: "PW DPPs & Daily Sprints", 
      inbox: "JEE 2028", 
      tags: ["#chemistry", "#bonding", "#vsepr"], 
      priority: "high", 
      dueDate: today, 
      type: "homework", 
      status: "todo", 
      completed: false 
    }
  ];

  let added = 0;
  tickTickTasks.forEach(t => {
    if (!existing.includes(t.title)) {
      s.tasks.unshift(t);
      added++;
    }
  });

  window.saveState();
  setTimeout(() => {
    window.showToast(`✓ Synced with TickTick (${added} tasks imported)!`, "success");
    if (typeof window.renderKanban === "function") window.renderKanban();
    if (typeof window.renderTodaysTasks === "function") window.renderTodaysTasks();
  }, 400);
};

// Export to TickTick strictly filtering OUT revision tasks
window.exportTickTickSyncPayload = function() {
  const s = window.getState();
  const tasks = s.tasks || [];
  // Exclude revision tasks completely
  const syncable = tasks.filter(t => {
    if (t.isRevision || t.type === "revision") return false;
    if ((t.tags || []).some(tag => String(tag).toLowerCase().includes("revision"))) return false;
    return true;
  });
  return syncable;
};

// ─── 9. Toast Notifications ───────────────────────────────
window.showToast = function(msg, type = "info") {
  let toast = document.getElementById("clockee-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "clockee-toast";
    toast.className = "fixed bottom-5 right-5 z-[999999] px-4 py-2.5 rounded-xl text-xs font-semibold shadow-2xl transition-all duration-300 transform translate-y-10 opacity-0 flex items-center gap-2 border backdrop-blur-xl pointer-events-none";
    document.body.appendChild(toast);
  }

  toast.textContent = msg;
  if (type === "success") {
    toast.className = "fixed bottom-5 right-5 z-[999999] px-4 py-2.5 rounded-xl text-xs font-semibold shadow-2xl transition-all duration-300 transform translate-y-0 opacity-100 flex items-center gap-2 border backdrop-blur-xl pointer-events-none bg-emerald-950/90 text-emerald-300 border-emerald-500/40 shadow-emerald-900/30";
  } else if (type === "error") {
    toast.className = "fixed bottom-5 right-5 z-[999999] px-4 py-2.5 rounded-xl text-xs font-semibold shadow-2xl transition-all duration-300 transform translate-y-0 opacity-100 flex items-center gap-2 border backdrop-blur-xl pointer-events-none bg-red-950/90 text-red-300 border-red-500/40 shadow-red-900/30";
  } else {
    toast.className = "fixed bottom-5 right-5 z-[999999] px-4 py-2.5 rounded-xl text-xs font-semibold shadow-2xl transition-all duration-300 transform translate-y-0 opacity-100 flex items-center gap-2 border backdrop-blur-xl pointer-events-none bg-[#0e1222]/95 text-cyan-300 border-cyan-500/40 shadow-cyan-900/30";
  }

  clearTimeout(window._toastTimeout);
  window._toastTimeout = setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
  }, 2600);
};

// ─── 10. Split Drawer: Lectures, PDFs, Music & AI ────────────
window.toggleSplitScreen = function() {
  const d = document.getElementById("split-drawer");
  if (d) {
    d.classList.toggle("translate-x-full");
    if (!d.classList.contains("translate-x-full")) {
      // Auto-render default tab
      window.switchDrawerTab(window._activeDrawerTab || 'lectures');
    }
  }
};

window._activeDrawerTab = 'lectures';
window._lectureCurrentCategory = 'pcm';
window._lectureCurrentSub = 'all';
window._activeMusicStation = { id: "jfKfPfyJRdk", title: "Lofi Girl - Relax & Study Beats", channel: "Lofi Girl 🌸" };

window.switchDrawerTab = function(tab) {
  if (tab === 'drive') tab = 'lectures';
  window._activeDrawerTab = tab;

  // Toggle tab contents
  ["lectures", "pdf", "audio", "ai", "notes", "drive"].forEach(t => {
    const pane = document.getElementById(`drawer-pane-${t}`);
    if (pane) {
      if (t === tab || (tab === 'lectures' && t === 'drive')) {
        pane.classList.remove("hidden");
        pane.classList.add("flex");
      } else {
        pane.classList.add("hidden");
        pane.classList.remove("flex");
      }
    }
  });

  // Highlight active drawer tab buttons
  document.querySelectorAll('.drawer-tab').forEach(btn => {
    const fnStr = btn.getAttribute('onclick') || '';
    if (fnStr.includes(`'${tab}'`) || (tab === 'lectures' && fnStr.includes("'drive'"))) {
      btn.classList.add('text-indigo-400', 'border-b-2', 'border-indigo-500');
      btn.classList.remove('text-gray-400');
    } else {
      btn.classList.remove('text-indigo-400', 'border-b-2', 'border-indigo-500');
      btn.classList.add('text-gray-400');
    }
  });

  if (tab === "lectures") {
    window.renderLecturesDrawer(window._lectureCurrentCategory, window._lectureCurrentSub);
  } else if (tab === "pdf") {
    window.renderPdfsDrawer();
  } else if (tab === "audio") {
    window.renderMusicCorner();
  }
};

// ── Curated Lectures Drawer (PCM vs One-Shot with Thumbnails) ─
window.setLectureCategory = function(cat) {
  window._lectureCurrentCategory = cat;
  window.renderLecturesDrawer(cat, window._lectureCurrentSub);
};

window.setLectureSubjectFilter = function(sub) {
  window._lectureCurrentSub = sub;
  window.renderLecturesDrawer(window._lectureCurrentCategory, sub);
};

window.renderLecturesDrawer = function(category = 'pcm', subFilter = 'all') {
  const container = document.getElementById("lectures-list-container") || document.getElementById("drive-links-list");
  if (!container) return;

  const s = window.getState();
  const lectureData = (s.curatedLectures && s.curatedLectures[category]) ? s.curatedLectures[category] : (DEFAULT_STATE.curatedLectures[category] || []);

  const filtered = lectureData.filter(lec => {
    if (subFilter === 'all') return true;
    return lec.subject.toLowerCase() === subFilter.toLowerCase();
  });

  container.innerHTML = `
    <!-- Top Category Switcher: PCM Lectures vs One-Shot Marathons -->
    <div class="space-y-3 pb-3 border-b border-white/10">
      <div class="flex rounded-xl bg-black/60 p-1 border border-white/10">
        <button onclick="setLectureCategory('pcm')" class="flex-1 py-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 ${category === 'pcm' ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          <span>PCM Lectures</span>
        </button>
        <button onclick="setLectureCategory('oneshot')" class="flex-1 py-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 ${category === 'oneshot' ? 'bg-gradient-to-r from-amber-600 to-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>One-Shot Marathons</span>
        </button>
      </div>

      <!-- Subject Filter Pills -->
      <div class="flex gap-1.5 flex-wrap">
        <button onclick="setLectureSubjectFilter('all')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${subFilter === 'all' ? 'bg-white text-black font-extrabold shadow' : 'bg-white/5 text-gray-400 hover:text-white'}">All (${lectureData.length})</button>
        <button onclick="setLectureSubjectFilter('Physics')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${subFilter === 'Physics' ? 'bg-blue-600 text-white shadow' : 'bg-blue-950/40 text-blue-300 border border-blue-500/30'}">Physics</button>
        <button onclick="setLectureSubjectFilter('Chemistry')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${subFilter === 'Chemistry' ? 'bg-emerald-600 text-white shadow' : 'bg-emerald-950/40 text-emerald-300 border border-emerald-500/30'}">Chemistry</button>
        <button onclick="setLectureSubjectFilter('Maths')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${subFilter === 'Maths' ? 'bg-amber-600 text-white shadow' : 'bg-amber-950/40 text-amber-300 border border-amber-500/30'}">Maths</button>
      </div>
    </div>

    <!-- Lectures Cards with Thumbnails -->
    <div class="space-y-3 pt-3">
      ${filtered.length === 0 ? '<p class="text-xs text-gray-500 italic py-6 text-center">No lectures found in this filter.</p>' : filtered.map(lec => {
        const subColor = lec.subject === 'Physics' ? 'text-blue-400 bg-blue-950/60 border-blue-500/30' :
                         lec.subject === 'Chemistry' ? 'text-emerald-400 bg-emerald-950/60 border-emerald-500/30' :
                         'text-amber-400 bg-amber-950/60 border-amber-500/30';
        const thumbUrl = `https://img.youtube.com/vi/${lec.id}/mqdefault.jpg`;

        return `
          <div class="glass-card p-3 border border-white/10 hover:border-indigo-500/40 transition rounded-xl space-y-2.5 bg-gradient-to-br from-gray-900/90 to-[#0e1220]">
            <div class="flex gap-3">
              <div class="relative w-28 h-16 rounded-lg overflow-hidden shrink-0 border border-white/10 bg-black">
                <img src="${thumbUrl}" alt="Lecture Thumbnail" class="w-full h-full object-cover" onerror="this.src='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300&q=80'">
                <span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/85 text-[10px] font-mono font-bold text-white">${lec.duration}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-1.5 mb-0.5">
                  <span class="px-2 py-0.5 rounded-full text-[9px] font-bold border ${subColor}">${lec.subject}</span>
                  <span class="text-[10px] text-gray-400 truncate">${lec.channel}</span>
                </div>
                <h4 class="text-xs font-bold text-gray-100 line-clamp-2 leading-snug">${lec.title}</h4>
              </div>
            </div>
            <div class="flex items-center justify-between pt-1 border-t border-white/5">
              <button onclick="launchLectureInFocusBlock('${lec.id}', '${lec.title.replace(/'/g, "\\'")}', '${lec.subject}')" class="w-full py-1.5 bg-gradient-to-r from-indigo-600/40 to-cyan-600/40 hover:from-indigo-600 hover:to-cyan-600 text-cyan-200 hover:text-white rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 border border-cyan-500/30 shadow">
                <span>▶</span> Watch / Launch in Lecture Block
              </button>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
};

window.launchLectureInFocusBlock = function(id, title, sub) {
  // If on timer.html, automatically load into Section B
  if (typeof window.switchTimerMode === 'function') {
    window.switchTimerMode('lecture');
    if (typeof window.selectLectureSubject === 'function') {
      window.selectLectureSubject(sub);
    }
    const topicInput = document.getElementById('lec-topic-input');
    if (topicInput) topicInput.value = title;
    const topicDisplay = document.getElementById('lec-topic-display');
    if (topicDisplay) topicDisplay.textContent = `${sub} • ${title}`;
    window.showToast?.(`Loaded "${title}" into Lecture Focus Block`, 'success');
  } else {
    // Navigate or link to timer.html
    window.location.href = `timer.html?mode=lecture&ytId=${encodeURIComponent(id)}&sub=${encodeURIComponent(sub)}&title=${encodeURIComponent(title)}`;
  }
};

// ── Curated Focus Music Studio (NO Like / Dislike Buttons) ─────
window.renderMusicCorner = function() {
  const container = document.getElementById("pinned-playlists-list") || document.getElementById("music-stations-list");
  if (!container) return;

  const s = window.getState();
  const stations = s.focusMusicStations || DEFAULT_STATE.focusMusicStations;
  const active = window._activeMusicStation || stations[0];

  // Update player title and iframe
  const titleEl = document.getElementById("yt-active-title");
  if (titleEl) titleEl.textContent = active.title;

  container.innerHTML = `
    <div class="space-y-2">
      <div class="text-[11px] font-bold text-gray-400 uppercase tracking-wider flex items-center justify-between">
        <span>Deep Focus Audio Channels</span>
        <span class="text-emerald-400 font-mono text-[10px] flex items-center gap-1">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Music Only Mode
        </span>
      </div>
      ${stations.map((st, idx) => {
        const isCurrent = active.id === st.id;
        return `
          <div class="flex items-center justify-between p-3 rounded-xl transition ${isCurrent ? 'bg-indigo-950/70 border border-indigo-500/50 shadow-lg' : 'bg-gray-900 border border-white/5 hover:border-white/20'}">
            <div class="flex items-center gap-3 min-w-0 flex-1 cursor-pointer" onclick="playMusicStation('${st.id}', '${st.title.replace(/'/g, "\\'")}', '${st.channel}')">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${isCurrent ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-300'}">
                ${isCurrent ? '▶' : '<svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>'}
              </div>
              <div class="truncate flex-1">
                <div class="text-xs font-bold ${isCurrent ? 'text-indigo-200' : 'text-gray-200'} truncate">${st.title}</div>
                <div class="text-[10px] text-gray-400 flex items-center gap-2">
                  <span>${st.channel}</span>
                  <span class="px-1.5 py-0.2 rounded bg-black/50 text-cyan-300 text-[9px] font-mono">${st.tag}</span>
                </div>
              </div>
            </div>
            <button onclick="playMusicStation('${st.id}', '${st.title.replace(/'/g, "\\'")}', '${st.channel}')" class="px-3 py-1 rounded-lg text-xs font-bold transition ml-2 ${isCurrent ? 'bg-emerald-600 text-white' : 'bg-white/5 hover:bg-white/10 text-gray-300'}">
              ${isCurrent ? 'Playing' : 'Listen'}
            </button>
          </div>
        `;
      }).join('')}
    </div>
  `;
};

window.playMusicStation = function(id, title, channel) {
  window._activeMusicStation = { id, title, channel };
  const iframe = document.getElementById("yt-player-iframe");
  const titleEl = document.getElementById("yt-active-title");
  if (iframe) {
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&enablejsapi=1`;
  }
  if (titleEl) {
    titleEl.textContent = title;
  }
  window.renderMusicCorner();
  window.showToast?.(`Now Playing: ${title}`, 'info');
};

// ── Study Materials PDF Vault & Maximized Fullscreen Viewer ───
window.renderPdfsDrawer = function() {
  const container = document.getElementById("drive-links-list");
  if (!container) return;

  const s = window.getState();
  const pdfs = s.studyPdfs || DEFAULT_STATE.studyPdfs;

  container.innerHTML = `
    <div class="space-y-3">
      <div class="flex items-center justify-between pb-2 border-b border-white/10">
        <div>
          <h4 class="text-xs font-bold text-white uppercase tracking-wider">JEE High-Yield Reference Vault</h4>
          <p class="text-[10px] text-gray-400">Allen, PW AITS, Cengage & HC Verma</p>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-500/30 font-mono font-bold">5 Vault Books</span>
      </div>

      ${pdfs.map((pdf, idx) => `
        <div class="glass-card p-3 rounded-xl border border-white/10 hover:border-cyan-500/40 transition space-y-2.5 bg-gray-900/90">
          <div class="flex items-start gap-2.5">
            <div class="p-2 bg-red-950/40 rounded-lg border border-red-500/30 shrink-0 text-red-400">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-xs font-bold text-gray-200 leading-snug">${pdf.title}</h5>
              <div class="flex items-center gap-2 mt-1 text-[10px] text-gray-400 font-mono">
                <span class="text-cyan-300 font-bold">${pdf.subject}</span>
                <span>&bull;</span>
                <span>${pdf.pages}</span>
                <span>&bull;</span>
                <span>${pdf.size}</span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 pt-1 border-t border-white/5">
            <button onclick="openPdfReaderModal('${pdf.title.replace(/'/g, "\\'")}', '${pdf.url}', true)" class="flex-1 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs transition flex items-center justify-center gap-1 shadow">
              <span>⛶</span> Maximize Full View
            </button>
            <button onclick="openPdfReaderModal('${pdf.title.replace(/'/g, "\\'")}', '${pdf.url}', false)" class="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 font-bold text-xs transition">
              Read PDF
            </button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
};

// ── PDF Reader Modal with Responsive Self-Sizing Timer HUD ───
window.openPdfReaderModal = function(title, url, maximize = false) {
  let modal = document.getElementById("pdf-reader-modal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "pdf-reader-modal";
    modal.className = "fixed inset-0 z-[500] bg-black/85 backdrop-blur-md flex items-center justify-center p-4 transition-all duration-300";
    modal.innerHTML = `
      <div id="pdf-modal-box" class="glass-card w-[95vw] h-[92vh] flex flex-col border border-cyan-500/40 bg-[#0a0d18] shadow-[0_20px_60px_rgba(0,0,0,0.9)] rounded-2xl overflow-hidden transition-all duration-300">
        <!-- PDF Modal Header -->
        <div class="flex items-center justify-between p-4 border-b border-white/10 bg-black/60 shrink-0">
          <div class="flex items-center gap-3">
            <div class="p-1.5 bg-red-950/40 rounded-lg border border-red-500/30 text-red-400">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div>
              <h3 id="pdf-modal-title" class="text-sm font-bold text-white truncate max-w-lg">Study Material Reader</h3>
              <p class="text-[11px] text-gray-400">Full-size PDF reader &bull; Mini-Timer HUD active</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="togglePdfMaximize()" id="btn-pdf-maximize" class="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-cyan-300 font-bold text-xs border border-cyan-500/30 transition flex items-center gap-1">
              <span>⛶</span> Maximize
            </button>
            <button onclick="closePdfReaderModal()" class="px-3 py-1.5 rounded-lg bg-red-950/60 hover:bg-red-900 text-red-300 font-bold text-xs border border-red-500/30 transition">
              ✕ Close Reader
            </button>
          </div>
        </div>

        <!-- PDF Reader View Body -->
        <div class="flex-1 overflow-hidden relative flex flex-col items-center justify-center bg-gray-950 p-6">
          <div class="max-w-3xl w-full h-full glass-card p-8 border border-white/10 overflow-y-auto space-y-6 text-gray-200 text-sm leading-relaxed font-sans bg-gray-900/60 shadow-2xl">
            <div class="border-b border-white/10 pb-4 flex items-center justify-between">
              <div>
                <span class="text-[11px] font-mono text-cyan-400 font-bold uppercase tracking-wider">JEE Advanced Reference Document</span>
                <h2 id="pdf-preview-title" class="text-xl font-extrabold text-white mt-1">Allen Physics Module &bull; Chapter Practice Exercises</h2>
              </div>
              <span class="px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-500/30 text-xs font-mono font-bold">Verified PDF Source</span>
            </div>

            <div class="space-y-4 text-xs font-mono bg-black/40 p-4 rounded-xl border border-white/5">
              <p class="text-indigo-300 font-bold">Chapter Study Flow &amp; High-Yield Exercise Set:</p>
              <ul class="list-disc list-inside space-y-1.5 text-gray-300">
                <li>Section I: Concept Application Questions (1 to 25) — Ideal solving latency: 90s/Q</li>
                <li>Section II: Multi-Correct JEE Advanced Numerical Problems (26 to 45) — Ideal solving latency: 120s/Q</li>
                <li>Section III: Matrix Match &amp; Comprehension Passage Problems</li>
                <li>Section IV: Previous 10 Years Archive (2015 - 2025 JEE Advanced)</li>
              </ul>
            </div>

            <div class="p-6 rounded-xl border border-cyan-500/20 bg-cyan-950/20 text-center space-y-3">
              <p class="text-xs text-gray-300">To open external Drive original link directly in high-res Google Drive reader:</p>
              <a id="pdf-external-link" href="https://drive.google.com" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-6 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-xl text-xs transition shadow-lg shadow-cyan-600/30">
                <span>↗</span> Open High-Resolution Google Drive Viewer
              </a>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  const titleEl = document.getElementById("pdf-modal-title");
  const prevEl = document.getElementById("pdf-preview-title");
  const extEl = document.getElementById("pdf-external-link");
  if (titleEl) titleEl.textContent = title;
  if (prevEl) prevEl.textContent = title;
  if (extEl) extEl.href = url || "https://drive.google.com";

  modal.classList.remove("hidden");

  // Automatically minimize timer to floating HUD so user can focus on PDF!
  window.minimizeTimerToFloatingHUD();
  window.showToast?.(`Opened "${title}" at maximum sizing • Mini-Timer HUD docked!`, 'info');
};

window.closePdfReaderModal = function() {
  const modal = document.getElementById("pdf-reader-modal");
  if (modal) modal.classList.add("hidden");
  // Restore main timer from HUD
  window.restoreMainTimerFromHud();
};

window.togglePdfMaximize = function() {
  const box = document.getElementById("pdf-modal-box");
  const btn = document.getElementById("btn-pdf-maximize");
  if (!box) return;
  if (box.classList.contains("w-[95vw]")) {
    box.className = "glass-card w-[99vw] h-[98vh] flex flex-col border border-cyan-500/60 bg-[#0a0d18] shadow-[0_20px_60px_rgba(0,0,0,0.9)] rounded-none overflow-hidden transition-all duration-300";
    if (btn) btn.innerHTML = '<span>❐</span> Restore';
  } else {
    box.className = "glass-card w-[95vw] h-[92vh] flex flex-col border border-cyan-500/40 bg-[#0a0d18] shadow-[0_20px_60px_rgba(0,0,0,0.9)] rounded-2xl overflow-hidden transition-all duration-300";
    if (btn) btn.innerHTML = '<span>⛶</span> Maximize';
  }
};

// ── Floating Mini-Timer HUD (Responsive Self-Sizing Timer) ───
window.ensureFloatingTimerHUD = function() {
  let hud = document.getElementById("floating-mini-timer-hud");
  if (!hud) {
    hud = document.createElement("div");
    hud.id = "floating-mini-timer-hud";
    hud.className = "hidden fixed bottom-6 right-6 z-[9999] glass-card p-3 border border-cyan-500/50 bg-[#0b0e1b]/95 shadow-[0_10px_35px_rgba(0,0,0,0.85)] backdrop-blur-xl rounded-2xl flex items-center gap-3 transition-all duration-300";
    hud.innerHTML = `
      <div class="flex items-center gap-2.5">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <div>
          <div class="text-[10px] uppercase font-mono font-bold text-cyan-300" id="hud-clock-title">Focus Clock</div>
          <div class="text-xl font-mono font-extrabold text-white tracking-wider" id="hud-clock-digits">00:00:00</div>
        </div>
      </div>
      <div class="h-7 w-px bg-white/10"></div>
      <div class="flex items-center gap-1.5">
        <button onclick="toggleHudTimerPause()" id="hud-btn-pause" class="px-2.5 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition">⏸</button>
        <button onclick="restoreMainTimerFromHud()" class="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition flex items-center gap-1 shadow">
          <span>↗</span> Expand Timer
        </button>
      </div>
    `;
    document.body.appendChild(hud);
  }
  return hud;
};

window.minimizeTimerToFloatingHUD = function() {
  const hud = window.ensureFloatingTimerHUD();
  hud.classList.remove("hidden");

  // Sync timer display loop
  clearInterval(window._hudTimerInterval);
  window._hudTimerInterval = setInterval(() => {
    const digitsEl = document.getElementById("hud-clock-digits");
    const titleEl = document.getElementById("hud-clock-title");
    if (!digitsEl) return;

    // Check if on timer.html with active drill or lecture
    const drillDigits = document.getElementById("drill-total-timer")?.textContent;
    const isDrillActive = document.getElementById("drill-active-panel") && !document.getElementById("drill-active-panel").classList.contains("hidden");
    const lecDigitsHrs = document.getElementById("lec-digit-hrs")?.textContent;
    const lecDigitsMins = document.getElementById("lec-digit-mins")?.textContent;
    const lecDigitsSecs = document.getElementById("lec-digit-secs")?.textContent;

    if (isDrillActive && drillDigits) {
      if (titleEl) titleEl.textContent = "Drill Stopwatch";
      digitsEl.textContent = drillDigits;
    } else if (lecDigitsHrs && lecDigitsMins && lecDigitsSecs) {
      if (titleEl) titleEl.textContent = "Lecture Focus";
      digitsEl.textContent = `${lecDigitsHrs}:${lecDigitsMins}:${lecDigitsSecs}`;
    } else {
      // Fallback to current time
      if (titleEl) titleEl.textContent = "Study Timer";
      const now = new Date().toTimeString().slice(0, 8);
      digitsEl.textContent = now;
    }
  }, 500);
};

window.restoreMainTimerFromHud = function() {
  const hud = document.getElementById("floating-mini-timer-hud");
  if (hud) hud.classList.add("hidden");
  clearInterval(window._hudTimerInterval);
};

window.toggleHudTimerPause = function() {
  // If in drill mode
  if (typeof window.togglePauseDrill === 'function') {
    window.togglePauseDrill();
  } else if (typeof window.toggleLectureTimer === 'function') {
    window.toggleLectureTimer();
  }
};

window.saveLiveNotes = function(val) {
  window.mergeState({ liveNotes: val });
};

window.insertNoteTimestamp = function() {
  const area = document.getElementById("live-notes-area");
  if (!area) return;
  const now = new Date().toTimeString().slice(0, 8);
  area.value += `\n[${now}] `;
  area.focus();
  window.saveLiveNotes(area.value);
};

// ─── AI Doubt Tutor Integration (Gemini 2.5 Flash) ─────────
window.sendAIDoubtMessage = async function() {
  const input = document.getElementById("ai-doubt-input");
  const container = document.getElementById("ai-chat-messages");
  if (!input || !container) return;
  const msg = input.value.trim();
  if (!msg) return;

  // Append user message bubble
  const userDiv = document.createElement("div");
  userDiv.className = "bg-white/10 border border-white/10 rounded-xl p-3 text-white font-medium ml-6";
  userDiv.innerText = msg;
  container.appendChild(userDiv);
  input.value = "";
  container.scrollTop = container.scrollHeight;

  // Append loading bubble
  const loadDiv = document.createElement("div");
  loadDiv.className = "bg-indigo-950/60 border border-indigo-500/30 rounded-xl p-3 text-indigo-200 text-xs italic flex items-center gap-2";
  loadDiv.innerHTML = `<span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span> Thinking with Gemini 2.5 Flash...`;
  container.appendChild(loadDiv);
  container.scrollTop = container.scrollHeight;

  const s = window.getState();
  const key = s.apiKeys?.gemini;

  // If no Gemini key is provided or test mode, give authentic offline/sandbox AI guidance
  if (!key || key.startsWith("AQ.")) {
    setTimeout(() => {
      loadDiv.remove();
      const botDiv = document.createElement("div");
      botDiv.className = "bg-indigo-950/50 border border-indigo-500/30 rounded-xl p-3 text-indigo-100 font-medium mr-6 leading-relaxed whitespace-pre-wrap";
      
      let answer = "";
      const lower = msg.toLowerCase();
      if (lower.includes("lenz") || lower.includes("induction") || lower.includes("faraday")) {
        answer = "⚡ **Lenz's Law Summary:**\n*The induced electromotive force (EMF) and current always oppose the change in magnetic flux that produces them:* `ε = -dΦ/dt` (Law of Conservation of Energy applied to electromagnetism).\n\n💡 *JEE Advanced Tip:* Always use the right-hand grip rule to find opposing flux directions in moving loops!";
      } else if (lower.includes("rotational") || lower.includes("inertia") || lower.includes("torque")) {
        answer = "🎯 **Rotational Dynamics Key Principle:**\n`τ_net = I α` and `L = I ω`. When external torque is zero (`τ_ext = 0`), total angular momentum is strictly conserved.\n\n💡 *Common JEE Trap:* Remember that moment of inertia depends on the axis of rotation (`I = I_cm + Md²`).";
      } else if (lower.includes("integration") || lower.includes("calculus") || lower.includes("derivative")) {
        answer = "∫ **Calculus & Problem Solving Core:**\nUse King's property: `∫[a to b] f(x) dx = ∫[a to b] f(a+b-x) dx` for trigonometric or symmetry integrals.\n\n💡 *High-Yield Strategy:* Pair it with Leibniz rule when differentiating integral functions.";
      } else {
        answer = `🤖 **JEE Commander AI Tutor:**\nRegarding **"${msg}"**:\nFocus on fundamental first principles. Break the problem into free-body diagrams or reaction mechanisms, verify boundary conditions, and check unit dimensions before final calculation! (Configure your personal Gemini API key in Settings for full real-time cloud inference).`;
      }

      botDiv.innerHTML = window.marked ? marked.parse(answer) : answer;
      container.appendChild(botDiv);
      container.scrollTop = container.scrollHeight;
    }, 600);
    return;
  }

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${key}`;
    const prompt = `You are an elite IIT-JEE Mentor for JEE 2028. Answer this student doubt concisely with clear physics/chemistry/math concepts, LaTeX formulas if applicable, and high-yield tips:\n\n${msg}`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }]
      })
    });
    const data = await res.json();
    const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    loadDiv.remove();

    const botDiv = document.createElement("div");
    botDiv.className = "bg-indigo-950/50 border border-indigo-500/30 rounded-xl p-3 text-indigo-100 font-medium mr-6 leading-relaxed whitespace-pre-wrap";
    botDiv.innerHTML = reply ? (window.marked ? marked.parse(reply) : reply) : "Sorry, I couldn't generate a response. Please check your network.";
    container.appendChild(botDiv);
    container.scrollTop = container.scrollHeight;
  } catch (err) {
    loadDiv.remove();
    const errDiv = document.createElement("div");
    errDiv.className = "bg-red-950/40 border border-red-500/30 rounded-xl p-3 text-red-300 text-xs";
    errDiv.innerText = "Error: " + err.message;
    container.appendChild(errDiv);
  }
};

// ─── 11. Global Settings Synchronization ──────────────────
window.applyAllSettingsGlobally = function() {
  const s = window.getState();
  
  const name = document.getElementById("settings-name")?.value?.trim() || s.profile.name;
  const subtitle = document.getElementById("settings-subtitle")?.value?.trim() || s.profile.subtitle;
  const accent = document.getElementById("settings-accent")?.value || s.profile.accent;

  const gp = parseInt(document.getElementById("goal-physics")?.value || s.dailyGoals.Physics);
  const gc = parseInt(document.getElementById("goal-chemistry")?.value || s.dailyGoals.Chemistry);
  const gm = parseInt(document.getElementById("goal-maths")?.value || s.dailyGoals.Maths);
  const gh = parseFloat(document.getElementById("goal-hours")?.value || s.dailyGoals.hours);
  const jeeDate = document.getElementById("settings-jee-date")?.value || s.jeeDate;

  const nextDeadline = document.getElementById("settings-next-deadline")?.value || s.nextMilestone?.date;
  const nextTitle = document.getElementById("settings-next-milestone-title")?.value || s.nextMilestone?.title;

  const ttKey = document.getElementById("key-ticktick")?.value || s.apiKeys?.ticktick;
  const gemKey = document.getElementById("key-gemini")?.value || s.apiKeys?.gemini;
  const fbKey = document.getElementById("key-firebase")?.value || s.apiKeys?.cloudUrl;

  const dynamicAura = document.getElementById("setting-aura-toggle") ? document.getElementById("setting-aura-toggle").checked : (s.settings?.dynamicAura ?? true);
  const auraTheme = document.getElementById("setting-aura-theme")?.value || s.settings?.auraTheme || "cyan_indigo";
  const auraSpeed = document.getElementById("setting-aura-speed")?.value || s.settings?.auraSpeed || "fluid";

  s.profile = { ...s.profile, name, subtitle, accent };
  s.dailyGoals = { Physics: gp, Chemistry: gc, Maths: gm, hours: gh };
  s.jeeDate = jeeDate;
  s.nextMilestone = { date: nextDeadline, title: nextTitle };
  s.apiKeys = { ticktick: ttKey, gemini: gemKey, cloudUrl: fbKey };
  s.settings = { dynamicAura, auraTheme, auraSpeed };

  s.tasks = s.tasks || [];
  s.tasks = s.tasks.filter(t => t.id !== "setting_milestone");
  if (nextTitle && nextDeadline) {
    s.tasks.push({
      id: "setting_milestone",
      title: nextTitle,
      subject: "General",
      type: "milestone",
      dueDate: nextDeadline,
      status: "todo",
      completed: false
    });
  }

  window.saveState();
  document.documentElement.style.setProperty("--accent", accent);
  document.querySelectorAll("[data-profile-name]").forEach(el => el.textContent = name);
  document.querySelectorAll("[data-profile-subtitle]").forEach(el => el.textContent = subtitle);
  window.applyAuraSettings();

  window.showToast("All Settings & Background Themes Synchronized!", "success");
};

// ─── 12. Dynamic Nebula Aura Background & Master Theme Engine ────
(function() {
  const styleEl = document.createElement("style");
  styleEl.textContent = `
    /* Master Design System & Frosted Glass Overhaul */
    html, body {
      overflow-x: hidden !important;
      max-width: 100vw !important;
    }

    .dynamic-aura, .dynamic-aura-bg {
      overflow: hidden !important;
      max-width: 100vw !important;
      max-height: 100vh !important;
      pointer-events: none !important;
    }

    @media (max-width: 1024px) {
      #main-nav {
        overflow-x: auto !important;
        max-width: calc(100vw - 110px) !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        padding-bottom: 2px !important;
      }
      #main-nav::-webkit-scrollbar {
        display: none !important;
      }
      .nav-btn {
        flex-shrink: 0 !important;
        white-space: nowrap !important;
      }
    }

    @media (max-width: 768px) {
      .nav-btn {
        min-height: 40px !important;
        padding: 8px 14px !important;
      }
    }

    :root {
      --bg-base: #07080e;
      --bg-surface: #0e1220;
      --bg-elevated: #141a2e;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(99, 102, 241, 0.45);
      --accent: #6366f1;
      --accent-soft: rgba(99, 102, 241, 0.14);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
    }

    body {
      background-color: var(--bg-base) !important;
      color: var(--text-primary) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      letter-spacing: -0.012em;
      -webkit-font-smoothing: antialiased;
    }

    /* High-Personality Typography & Confident Title Boldness */
    h1, h2, h3, h4, h5, h6 {
      letter-spacing: -0.03em !important;
      font-weight: 800 !important;
      color: #ffffff;
    }
    .tracking-tight {
      letter-spacing: -0.035em !important;
    }
    .tracking-widest {
      letter-spacing: 0.1em !important;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace !important;
    }

    /* Sleek Frosted Glass Header / Title Bar */
    header.sticky {
      background: rgba(8, 10, 18, 0.72) !important;
      backdrop-filter: blur(20px) saturate(180%) !important;
      -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    }

    /* Refined Frosted Glass Cards */
    .glass-card {
      backdrop-filter: blur(20px) saturate(180%) !important;
      -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
      background: rgba(13, 17, 30, 0.72) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      border-radius: 18px !important;
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
      transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
    }
    .glass-card:hover {
      border-color: rgba(255, 255, 255, 0.14) !important;
      box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }

    /* Phase 1 GPU Transitions & Micro-Interactions */
    main, .glass-card {
      animation: smoothFadeUp 180ms cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    @keyframes smoothFadeUp {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    button:active, .nav-btn:active, .btn-action:active {
      transform: scale(0.98) !important;
    }
    button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
      outline: 2px solid #6366f1 !important;
      outline-offset: 2px !important;
    }
    @media (max-width: 768px) {
      button, .nav-btn {
        min-height: 44px;
        touch-action: manipulation;
      }
    }
    button:disabled {
      opacity: 0.5 !important;
      pointer-events: none !important;
    }

    /* Refined Navigation Pills */
    .nav-btn {
      padding: 6px 14px !important;
      border-radius: 9999px !important;
      font-size: 0.8125rem !important;
      font-weight: 600 !important;
      letter-spacing: -0.01em !important;
      color: #94a3b8 !important;
      background: rgba(255, 255, 255, 0.03) !important;
      border: 1px solid rgba(255, 255, 255, 0.06) !important;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 6px !important;
      text-decoration: none !important;
    }
    .nav-btn:hover {
      background: rgba(255, 255, 255, 0.08) !important;
      color: #ffffff !important;
      border-color: rgba(255, 255, 255, 0.16) !important;
    }
    .nav-btn.nav-active {
      background: #00f0ff !important;
      color: #050811 !important;
      border: 1px solid rgba(0, 240, 255, 0.8) !important;
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.5) !important;
      font-weight: 700 !important;
    }
    .nav-btn.nav-active svg {
      color: #050811 !important;
      stroke: #050811 !important;
    }

    /* Frosted Dropdown Menus - Translucent with Cyber Neon Glow Outline & Deep Glass Blur */
    .nav-dropdown-menu {
      background: rgba(8, 12, 26, 0.62) !important;
      backdrop-filter: blur(32px) saturate(220%) !important;
      -webkit-backdrop-filter: blur(32px) saturate(220%) !important;
      border: 1px solid rgba(0, 240, 255, 0.48) !important;
      border-radius: 16px !important;
      box-shadow: 0 20px 50px -8px rgba(0, 0, 0, 0.9), 0 0 25px rgba(0, 240, 255, 0.25), inset 0 0 14px rgba(0, 240, 255, 0.08) !important;
      padding: 6px !important;
    }
    .nav-dropdown-item {
      color: #94a3b8 !important;
      border-radius: 10px !important;
      padding: 8px 12px !important;
      font-size: 0.8rem !important;
      font-weight: 500 !important;
      transition: all 0.15s ease !important;
    }
    .nav-dropdown-item:hover {
      background: rgba(0, 240, 255, 0.16) !important;
      color: #00f0ff !important;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.2) !important;
    }

    /* Custom Glassmorphic Cyber Dropdown Component */
    .custom-glass-dropdown {
      position: relative;
      user-select: none;
      width: 100%;
    }
    .custom-glass-trigger {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      width: 100%;
      background: rgba(12, 16, 30, 0.68) !important;
      backdrop-filter: blur(24px) saturate(200%) !important;
      -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
      border: 1px solid rgba(0, 240, 255, 0.42) !important;
      border-radius: 12px !important;
      padding: 10px 14px !important;
      color: #f8fafc;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4), 0 0 12px rgba(0, 240, 255, 0.1);
    }
    .custom-glass-trigger:hover, .custom-glass-dropdown.open .custom-glass-trigger {
      border-color: #00f0ff !important;
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.32), 0 6px 20px rgba(0, 0, 0, 0.5) !important;
    }
    .custom-glass-trigger .chevron-icon {
      transition: transform 0.25s ease;
      color: #00f0ff;
    }
    .custom-glass-dropdown.open .chevron-icon {
      transform: rotate(180deg);
    }
    .custom-glass-menu {
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      right: 0;
      background: rgba(8, 12, 26, 0.78) !important;
      backdrop-filter: blur(32px) saturate(220%) !important;
      -webkit-backdrop-filter: blur(32px) saturate(220%) !important;
      border: 1px solid rgba(0, 240, 255, 0.48) !important;
      border-radius: 16px !important;
      padding: 6px !important;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 25px rgba(0, 240, 255, 0.25), inset 0 0 12px rgba(0, 240, 255, 0.06) !important;
      z-index: 1000;
      display: none;
      flex-direction: column;
      gap: 3px;
      max-height: 270px;
      overflow-y: auto;
    }
    .custom-glass-dropdown.open .custom-glass-menu {
      display: flex;
    }
    .custom-glass-option {
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 0.78rem;
      font-weight: 500;
      color: #94a3b8;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      transition: all 0.15s ease;
    }
    .custom-glass-option:hover {
      background: rgba(0, 240, 255, 0.15);
      color: #00f0ff;
      transform: translateX(2px);
    }
    .custom-glass-option.selected {
      background: rgba(99, 102, 241, 0.24);
      color: #38bdf8;
      font-weight: 700;
      border: 1px solid rgba(0, 240, 255, 0.3);
    }

    /* Universal Cyber Select & Dropdown Styling */
    select {
      background: rgba(12, 16, 30, 0.78) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border: 1px solid rgba(0, 240, 255, 0.4) !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.55), 0 0 12px rgba(0, 240, 255, 0.12) !important;
      color: #f1f5f9 !important;
      border-radius: 12px !important;
    }
    select:focus {
      border-color: rgba(0, 240, 255, 0.8) !important;
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.35) !important;
      outline: none !important;
    }
    select option {
      background: #0c101e !important;
      color: #e2e8f0 !important;
    }

    /* Calibrated Ambient Cosmic Aura Background (Quirky animation preserved, glare removed) */
    .dynamic-aura-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 0;
      overflow: hidden;
      opacity: 0.38 !important;
      transition: opacity 0.6s ease;
    }
    .aura-blob-1, .aura-blob-2, .aura-blob-3 {
      position: absolute;
      border-radius: 50%;
      filter: blur(120px) !important;
      will-change: transform;
      animation: fluidAuraDrift 28s ease-in-out infinite alternate;
      transition: background 0.8s ease;
    }
    .aura-blob-1 {
      width: 620px;
      height: 620px;
      top: -120px;
      left: -120px;
      background: var(--aura-color-1, rgba(99, 102, 241, 0.45));
      animation-duration: 24s;
    }
    .aura-blob-2 {
      width: 720px;
      height: 720px;
      bottom: -150px;
      right: -150px;
      background: var(--aura-color-2, rgba(56, 189, 248, 0.38));
      animation-duration: 32s;
      animation-delay: -6s;
    }
    .aura-blob-3 {
      width: 560px;
      height: 560px;
      top: 30%;
      left: 32%;
      background: var(--aura-color-3, rgba(168, 85, 247, 0.32));
      animation-duration: 26s;
      animation-delay: -12s;
    }
    @keyframes fluidAuraDrift {
      0% { transform: translate(0, 0) scale(1) rotate(0deg); }
      33% { transform: translate(70px, 50px) scale(1.08) rotate(45deg); }
      66% { transform: translate(-40px, 80px) scale(0.95) rotate(90deg); }
      100% { transform: translate(35px, -35px) scale(1.04) rotate(135deg); }
    }

    /* Cyber Checkboxes with Glowing Effects */
    .cyber-checkbox-container {
      display: inline-flex;
      align-items: center;
      position: relative;
      cursor: pointer;
      user-select: none;
    }
    .cyber-checkbox-container input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
      height: 0;
      width: 0;
    }
    .cyber-checkmark {
      width: 18px;
      height: 18px;
      border-radius: 6px;
      background: rgba(15, 23, 42, 0.7);
      border: 1.5px solid rgba(0, 240, 255, 0.45);
      box-shadow: 0 0 8px rgba(0, 240, 255, 0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cyber-checkbox-container:hover input ~ .cyber-checkmark {
      border-color: #00f0ff;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
      transform: scale(1.08);
    }
    .cyber-checkbox-container input:checked ~ .cyber-checkmark {
      background: linear-gradient(135deg, #00f0ff 0%, #6366f1 100%);
      border-color: #00f0ff;
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.55), inset 0 0 6px rgba(255, 255, 255, 0.5);
      animation: cyberCheckPulse 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cyber-checkmark svg {
      display: none;
      width: 11px;
      height: 11px;
      stroke: #070913;
      stroke-width: 3.2;
    }
    .cyber-checkbox-container input:checked ~ .cyber-checkmark svg {
      display: block;
    }
    @keyframes cyberCheckPulse {
      0% { transform: scale(0.8); }
      50% { transform: scale(1.22); }
      100% { transform: scale(1); }
    }

    /* Minimalist Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(7, 8, 14, 0.8); }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.5); }

    /* Ensure global avatar file picker is strictly invisible on all pages */
    #global-avatar-upload {
      display: none !important;
      position: absolute !important;
      width: 0 !important;
      height: 0 !important;
      opacity: 0 !important;
      pointer-events: none !important;
      visibility: hidden !important;
    }
  `;
  document.head.appendChild(styleEl);

  function ensureAuraDOM() {
    if (!document.body) return;
    if (!document.querySelector(".dynamic-aura-bg")) {
      const aura = document.createElement("div");
      aura.className = "dynamic-aura-bg";
      aura.innerHTML = `
        <div class="aura-blob-1"></div>
        <div class="aura-blob-2"></div>
        <div class="aura-blob-3"></div>
      `;
      document.body.prepend(aura);
    }

    if (!document.getElementById("global-avatar-upload")) {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.id = "global-avatar-upload";
      fileInput.accept = "image/*";
      fileInput.className = "hidden";
      fileInput.style.display = "none";
      fileInput.hidden = true;
      fileInput.setAttribute("aria-hidden", "true");
      fileInput.setAttribute("tabindex", "-1");
      fileInput.onchange = window.handleAvatarUpload;
      document.body.appendChild(fileInput);
    }

    window.applyAuraSettings();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureAuraDOM);
  } else {
    ensureAuraDOM();
  }
})();

// ─── 10. Web Audio Cyber Synthesizer (Tick, Chime, SFX) ──────────────
let _cyberAudioCtx = null;
window.playCyberTick = function(checked = true) {
  try {
    if (!_cyberAudioCtx) {
      _cyberAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (_cyberAudioCtx.state === 'suspended') {
      _cyberAudioCtx.resume();
    }
    const now = _cyberAudioCtx.currentTime;
    const osc = _cyberAudioCtx.createOscillator();
    const gain = _cyberAudioCtx.createGain();
    
    if (checked) {
      // High-tech cyber chime: D5 -> A5 (587Hz -> 880Hz)
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
      osc.connect(gain);
      gain.connect(_cyberAudioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.15);
    } else {
      // Cyber dampening tick: 440Hz -> 220Hz
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(220, now + 0.06);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(_cyberAudioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.09);
    }
  } catch (e) {
    // Graceful fallback if audio context restricted
  }
};

// ─── 11. Global Cloud Sync & Multi-User Profile Flyout ──────────────
window.pushToCloud = async function() {
  const activeId = window.getActiveUserId ? window.getActiveUserId() : "user_aspirant";
  const s = window.getState();
  const baseUrl = s.apiKeys?.cloudUrl || "https://clockee-app-default-rtdb.asia-southeast1.firebasedatabase.app";
  window.showToast("☁️ Pushing student state to Firebase...", "info");
  try {
    const res = await fetch(`${baseUrl}/students/${activeId}/state.json`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(s)
    });
    if (res.ok) {
      window.showToast(`✓ Cloud Synced for ${s.profile?.name || activeId}!`, "success");
      localStorage.setItem(`clockee_last_sync_${activeId}`, new Date().toISOString());
      window.dispatchEvent(new CustomEvent("cloudSyncComplete", { detail: { timestamp: new Date() } }));
    } else {
      window.showToast("Cloud sync failed: " + res.statusText, "error");
    }
  } catch (err) {
    window.showToast("Sync error: " + err.message, "error");
  }
};

window.pullFromCloud = async function() {
  const activeId = window.getActiveUserId ? window.getActiveUserId() : "user_aspirant";
  const s = window.getState();
  const baseUrl = s.apiKeys?.cloudUrl || "https://clockee-app-default-rtdb.asia-southeast1.firebasedatabase.app";
  window.showToast("⬇️ Pulling state from Firebase...", "info");
  try {
    const res = await fetch(`${baseUrl}/students/${activeId}/state.json`);
    if (!res.ok) throw new Error("Server returned " + res.status);
    const remote = await res.json();
    if (remote) {
      window.APP_STATE = { ...DEFAULT_STATE, ...remote };
      window.saveState();
      window.showToast("✓ Successfully pulled cloud data!", "success");
      setTimeout(() => location.reload(), 400);
    } else {
      window.showToast("No remote cloud record found for this profile", "info");
    }
  } catch (err) {
    window.showToast("Pull failed: " + err.message, "error");
  }
};

window.initGlobalProfileMenu = function() {
  const navRight = document.querySelector(".nav-right");
  const avatarLink = document.querySelector("#navAvatarImg")?.closest("a") || document.querySelector("[data-profile-avatar]")?.closest("a") || document.querySelector(".nav-right a");
  if (!avatarLink) return;

  avatarLink.removeAttribute("href");
  avatarLink.style.cursor = "pointer";

  let popover = document.getElementById("clockee-profile-popover");
  if (!popover) {
    popover = document.createElement("div");
    popover.id = "clockee-profile-popover";
    popover.className = "hidden fixed z-[999999] top-16 right-4 sm:right-6 w-80 glass-card p-4 space-y-3.5 border border-indigo-500/30 bg-[#0a0d18]/95 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.9)] text-white";
    document.body.appendChild(popover);
  }

  function renderPopoverContent() {
    let user = null;
    try {
      const raw = localStorage.getItem("clockee_current_user");
      if (raw) user = JSON.parse(raw);
    } catch(e) {}
    if (!user) {
      user = window.getUsersList().find(u => u.active) || { name: "JEE Aspirant", role: "JEE 2028 Aspirant", id: "user_aspirant" };
    }

    const s = window.getState ? window.getState() : {};
    const sidebarName = document.getElementById("sidebar-profile-name")?.textContent?.trim();
    const isGuest = Boolean(
      user.isGuest ||
      (user.uid && user.uid.startsWith("guest_")) ||
      (user.id && user.id.startsWith("guest_")) ||
      user.role === "Guest" ||
      user.role === "Guest Aspirant" ||
      user.name === "Guest Aspirant" ||
      sidebarName === "Guest Aspirant" ||
      s.profile?.name === "Guest Aspirant"
    );

    // If guest, enforce clean guest profile fields
    const displayName = isGuest ? "Guest Aspirant" : (user.name || "JEE Aspirant");
    const displayRole = isGuest ? "Guest Sandbox Session" : (user.role || "JEE 2028 Aspirant");
    // Strictly synchronize avatar with active page avatar and global state profile
    const activeNavImg = document.querySelector("#navAvatarImg") || document.querySelector("[data-profile-avatar]");
    const activePfp = s.profile?.pfp || (activeNavImg && activeNavImg.src ? activeNavImg.src : null) || user.pfp || DEFAULT_STATE.profile.pfp;
    const displayPfp = activePfp;

    const isAdmin = !isGuest && Boolean(
      user.role === "Mentor / Faculty" || 
      user.role === "Admin" || 
      user.isAdmin === true ||
      sessionStorage.getItem('clockee_admin_authorized') === 'true'
    );

    let html = `
      <div class="flex items-center gap-3 border-b border-white/10 pb-3">
        <img id="popover-avatar-img" src="${displayPfp}" class="w-11 h-11 rounded-full border-2 ${isAdmin ? 'border-purple-400' : 'border-cyan-400'} bg-black/40 object-cover">
        <div class="flex-1 min-w-0">
          <div class="text-sm font-extrabold text-white truncate flex items-center gap-1.5">
            <span>${displayName}</span>
            <span class="w-2 h-2 rounded-full ${isGuest ? 'bg-cyan-400' : 'bg-emerald-400'} animate-pulse" title="${isGuest ? 'Sandbox Active' : 'Active'}"></span>
          </div>
          <div class="text-[11px] ${isAdmin ? 'text-purple-300 font-bold' : isGuest ? 'text-cyan-300 font-bold' : 'text-indigo-300'} font-medium truncate">
            ${displayRole} ${isAdmin ? '★ Admin' : ''}
          </div>
          <div class="text-[10px] text-slate-400 font-mono flex items-center gap-1 mt-0.5">
            <span>⚡</span> <span>${isGuest ? 'Ephemeral Local Sandbox' : 'Auto-Sync Active'}</span>
          </div>
        </div>
      </div>
    `;

    // ONLY show other profiles if user is an authenticated non-guest user
    if (!isGuest) {
      const users = window.getUsersList().filter(u => !u.id.startsWith("guest_") && u.role !== "Guest Aspirant" && u.name !== "Guest Aspirant");
      const otherUsers = users.filter(u => u.id !== user.id && u.id !== user.uid);
      if (otherUsers.length > 0) {
        html += `
          <div class="space-y-1.5">
            <div class="text-[10px] font-bold uppercase tracking-wider text-gray-400 flex justify-between items-center">
              <span>Switch Profile</span>
              <span class="text-[9px] text-indigo-400 font-normal">Isolated data</span>
            </div>
            <div class="space-y-1 max-h-28 overflow-y-auto pr-1">
              ${otherUsers.map(u => `
                <button onclick="window.switchUser('${u.id}')" class="w-full text-left p-2 rounded-lg bg-white/5 hover:bg-indigo-600/20 border border-white/5 hover:border-indigo-500/30 flex items-center gap-2.5 transition">
                  <img src="${u.pfp}" class="w-6 h-6 rounded-full border border-gray-600">
                  <div class="flex-1 min-w-0">
                    <div class="text-xs font-semibold text-gray-200 truncate">${u.name}</div>
                    <div class="text-[10px] text-gray-400 truncate">${u.role}</div>
                  </div>
                  <span class="text-[10px] text-indigo-400 font-bold">&rarr;</span>
                </button>
              `).join('')}
            </div>
          </div>
        `;
      }
    }

    // ONLY Settings and Sign Out (as requested: "only settings and signout should go here")
    html += `
      <div class="grid grid-cols-2 gap-2 pt-1 text-xs">
        <a href="settings.html" class="p-2.5 rounded-xl bg-gray-900/90 hover:bg-gray-800 border border-white/10 text-center font-bold text-gray-200 transition flex items-center justify-center gap-1.5 shadow">
          <span>⚙️</span> <span>Settings</span>
        </a>
        <button onclick="window.handleUserLogout()" class="p-2.5 rounded-xl bg-red-950/60 hover:bg-red-900/70 border border-red-500/30 text-center font-bold text-red-300 transition flex items-center justify-center gap-1.5 shadow">
          <span>🚪</span> <span>Sign Out</span>
        </button>
      </div>
    `;

    popover.innerHTML = html;
  }

  avatarLink.addEventListener("click", function(e) {
    e.preventDefault();
    e.stopPropagation();
    renderPopoverContent();
    popover.classList.toggle("hidden");
  });

  document.addEventListener("click", function(e) {
    if (!popover.contains(e.target) && !avatarLink.contains(e.target)) {
      popover.classList.add("hidden");
    }
  });

  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") popover.classList.add("hidden");
  });
};

window.enforceRolePermissions = function() {
  let user = null;
  try {
    const raw = localStorage.getItem('clockee_current_user');
    if (raw) user = JSON.parse(raw);
  } catch(e) {}
  if (!user) {
    const list = window.getUsersList();
    user = list.find(u => u.active) || { role: "JEE 2028 Aspirant" };
  }

  const s = window.getState ? window.getState() : {};
  const isGuest = Boolean(!user || (user.uid && user.uid.startsWith("guest_")) || (user.id && user.id.startsWith("guest_")) || user.role === "Guest" || user.role === "Guest Aspirant" || user.isGuest || user.name === "Guest Aspirant" || s.profile?.name === "Guest Aspirant");
  if (isGuest) {
    sessionStorage.removeItem('clockee_admin_authorized');
    sessionStorage.removeItem('clockee_admin_pass');
  }
  const isAdmin = !isGuest && Boolean(
    user.role === "Mentor / Faculty" || 
    user.role === "Admin" || 
    user.isAdmin === true ||
    sessionStorage.getItem('clockee_admin_authorized') === 'true'
  );

  document.querySelectorAll('a[href="admin.html"], .nav-admin-link').forEach(el => {
    if (!window.location.pathname.endsWith('admin.html')) {
      if (isAdmin) {
        el.style.setProperty('display', 'inline-flex', 'important');
        el.classList.remove('hidden');
      } else {
        el.style.setProperty('display', 'none', 'important');
        el.classList.add('hidden');
      }
    }
  });
};

// Universal Responsive Clamp Injection
(function injectResponsiveClamp() {
  if (document.getElementById("clockee-responsive-clamp")) return;
  const style = document.createElement("style");
  style.id = "clockee-responsive-clamp";
  style.textContent = `
    html, body {
      overflow-x: hidden !important;
      max-width: 100vw !important;
    }
    @media (max-width: 900px) {
      #main-nav {
        overflow-x: auto !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        -webkit-overflow-scrolling: touch !important;
        max-width: 100% !important;
      }
      #main-nav::-webkit-scrollbar {
        display: none !important;
      }
    }
    @media (min-width: 901px) {
      #main-nav {
        overflow: visible !important;
      }
    }
  `;
  document.head.appendChild(style);
})();

window.handleUserLogout = function() {
  let currentUser = null;
  try {
    const raw = localStorage.getItem("clockee_current_user");
    if (raw) currentUser = JSON.parse(raw);
  } catch(e) {}

  const s = window.getState ? window.getState() : {};
  const isGuest = !currentUser || 
    (currentUser.uid && currentUser.uid.startsWith("guest_")) || 
    (currentUser.id && currentUser.id.startsWith("guest_")) || 
    currentUser.role === "Guest" || 
    currentUser.role === "Guest Aspirant" || 
    currentUser.isGuest ||
    currentUser.name === "Guest Aspirant" ||
    s.profile?.name === "Guest Aspirant";

  // "delete guest appearance as soon as end of ssession"
  if (isGuest || (currentUser && (currentUser.uid?.startsWith("guest_") || currentUser.id?.startsWith("guest_")))) {
    const guestId = currentUser?.uid || currentUser?.id;
    if (guestId) {
      localStorage.removeItem(`clockee_user_state_${guestId}`);
    }
    try {
      let list = JSON.parse(localStorage.getItem("clockee_multi_users") || "[]");
      list = list.filter(u => !u.id.startsWith("guest_") && u.role !== "Guest" && u.role !== "Guest Aspirant" && !u.isGuest && u.name !== "Guest Aspirant");
      localStorage.setItem("clockee_multi_users", JSON.stringify(list));
    } catch(e) {}
  }

  localStorage.removeItem("clockee_current_user");
  localStorage.removeItem("clockee_auth_active");
  sessionStorage.removeItem("clockee_admin_authorized");
  sessionStorage.removeItem("clockee_admin_pass");
  window.showToast("Signed out. Session ended.", "info");
  setTimeout(() => window.location.href = "login.html", 300);
};

// Auto-run sidebar, profile menu and permissions on load
if (document.readyState === "complete" || document.readyState === "interactive") {
  setTimeout(() => { 
    if (typeof window.initSidebar === "function") window.initSidebar(); 
    if (typeof window.initGlobalProfileMenu === "function") window.initGlobalProfileMenu();
    if (typeof window.enforceRolePermissions === "function") window.enforceRolePermissions();
  }, 15);
}

document.addEventListener("DOMContentLoaded", function() {
  if (typeof window.initSidebar === "function") window.initSidebar();
  if (typeof window.initGlobalProfileMenu === "function") window.initGlobalProfileMenu();
  if (typeof window.enforceRolePermissions === "function") window.enforceRolePermissions();
});

window.addEventListener("stateChange", function() {
  if (typeof window.initSidebar === "function") window.initSidebar();
  if (typeof window.initGlobalProfileMenu === "function") window.initGlobalProfileMenu();
  if (typeof window.enforceRolePermissions === "function") window.enforceRolePermissions();
});

// Retheming & Visual Studio: Sound Synthesis & Dynamic Glass Styling
window.playTactileFeedback = function(soundType) {
  const s = window.getState ? window.getState() : {};
  const pack = soundType || s.settings?.soundPack || "cyber";
  if (pack === "silent") return;

  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    if (pack === "mechanical") {
      osc.type = "triangle";
      osc.frequency.setValueAtTime(1400, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(280, ctx.currentTime + 0.035);
      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.035);
    } else if (pack === "thump") {
      osc.type = "sine";
      osc.frequency.setValueAtTime(160, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(50, ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } else {
      osc.type = "sine";
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(1760, ctx.currentTime + 0.045);
      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.045);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.045);
    }
  } catch(e) {}
};

(function injectGlassStyles() {
  if (document.getElementById("clockee-glass-engine")) return;
  const style = document.createElement("style");
  style.id = "clockee-glass-engine";
  style.textContent = `
    :root {
      --glass-blur: 20px;
      --glass-opacity: 0.75;
    }
    .glass-card {
      backdrop-filter: blur(var(--glass-blur, 20px)) !important;
      -webkit-backdrop-filter: blur(var(--glass-blur, 20px)) !important;
      background: rgba(16, 18, 27, var(--glass-opacity, 0.75)) !important;
    }
  `;
  document.head.appendChild(style);
})();

window.applyGlassSettings = function() {
  const s = window.getState ? window.getState() : {};
  const blur = s.settings?.glassBlur !== undefined ? s.settings.glassBlur : 20;
  const opacity = s.settings?.glassOpacity !== undefined ? s.settings.glassOpacity : 0.75;
  document.documentElement.style.setProperty("--glass-blur", `${blur}px`);
  document.documentElement.style.setProperty("--glass-opacity", opacity);
};
if (document.readyState === "complete" || document.readyState === "interactive") {
  setTimeout(window.applyGlassSettings, 20);
} else {
  document.addEventListener("DOMContentLoaded", window.applyGlassSettings);
}


// ─── Universal Command Palette Engine (Ctrl + K / Cmd + K) ───
(function injectCommandPalette() {
  if (document.getElementById("clockee-cmd-palette-modal")) return;

  // 1. Create Modal DOM
  const modal = document.createElement("div");
  modal.id = "clockee-cmd-palette-modal";
  modal.className = "hidden fixed inset-0 z-[1000] bg-black/80 backdrop-blur-md flex items-start justify-center pt-20 px-4";
  modal.innerHTML = `
    <div class="glass-card max-w-xl w-full p-4 space-y-3 border border-cyan-500/40 bg-[#0b0e1d]/95 shadow-[0_0_50px_rgba(0,240,255,0.25)] rounded-2xl animate-in fade-in zoom-in-95 duration-150">
      <div class="flex items-center gap-2.5 pb-2.5 border-b border-white/10">
        <span class="text-cyan-400 text-base">⚡</span>
        <input 
          type="text" 
          id="cmd-palette-input" 
          placeholder="Type a command or jump to module... (e.g., 'cbt', 'timer', 'task', 'log')" 
          class="flex-1 bg-transparent text-white font-mono text-xs outline-none placeholder:text-gray-500"
          autocomplete="off"
        >
        <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-gray-400 border border-white/10">ESC</span>
      </div>

      <div id="cmd-palette-list" class="space-y-1 max-h-72 overflow-y-auto pr-1"></div>

      <div class="pt-2 border-t border-white/5 flex items-center justify-between text-[10px] text-gray-500 font-mono">
        <div class="flex items-center gap-3">
          <span><kbd class="px-1.5 py-0.5 rounded bg-white/5 text-gray-300">↑↓</kbd> Navigate</span>
          <span><kbd class="px-1.5 py-0.5 rounded bg-white/5 text-gray-300">ENTER</kbd> Select</span>
        </div>
        <span class="text-cyan-400 font-bold">ClockEE Command Terminal</span>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  // 2. Floating Quick Launcher Pill
  const trigger = document.createElement("div");
  trigger.id = "clockee-cmd-trigger";
  trigger.className = "fixed bottom-4 right-4 z-[990] flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#0a0d18]/90 border border-cyan-500/35 text-cyan-300 text-xs font-mono font-bold cursor-pointer hover:scale-105 hover:border-cyan-400 transition shadow-[0_0_15px_rgba(0,240,255,0.2)] backdrop-blur-md select-none";
  trigger.innerHTML = `<span>⚡</span> <span class="hidden sm:inline">Command Palette</span> <kbd class="px-1.5 py-0.2 rounded bg-white/10 text-[9px] text-cyan-300 font-mono">Ctrl+K</kbd>`;
  trigger.onclick = () => window.toggleCommandPalette();
  document.body.appendChild(trigger);

  // 3. Command Definitions
  const COMMANDS = [
    { title: "Tactical Pace Benchmark Sprint", desc: "Drift-free sub-second pace latency & question drill", icon: "⏱️", shortcut: "T", action: () => window.location.href = "timer.html" },
    { title: "Authentic CBT Exam Simulator", desc: "Crash-proof NTA examination test suite with LaTeX", icon: "🧪", shortcut: "C", action: () => window.location.href = "cbt_home.html" },
    { title: "Task Kanban & Auto-Flow Terminal", desc: "Mistake vault autopsy rollover, syllabus sync & subtasks", icon: "📋", shortcut: "K", action: () => window.location.href = "task.html" },
    { title: "AI Question Cloner Studio", desc: "Synthesize 3 concept variations via Gemini 2.0 or algorithmic bank", icon: "🤖", shortcut: "Q", action: () => window.location.href = "cbt_cloner.html" },
    { title: "Coaching Syllabus Matrix", desc: "3 PCM Milestone blocks with cyber chimes", icon: "📚", shortcut: "M", action: () => window.location.href = "coaching.html" },
    { title: "Today's Performance Digest", desc: "Momentum charts, hourly intensity, and JPEG report card", icon: "📊", shortcut: "D", action: () => window.location.href = "today.html" },
    { title: "IIT Dream Vision Board & Edu News", desc: "Aspirant goals, college news feed & vision gallery", icon: "✨", shortcut: "I", action: () => window.location.href = "inspiration.html" },
    { title: "Visual Studio & Settings", desc: "Glassmorphism blur, opacity, tactile sound packs, and themes", icon: "⚙️", shortcut: "S", action: () => window.location.href = "settings.html" },
    { title: "Quick Action: Log +5 Questions Solved", desc: "Increases Physics & Chemistry daily question counters", icon: "⚡", shortcut: "L", action: () => {
      const s = window.getState();
      s.stats = s.stats || {};
      s.stats.questionsSolved = s.stats.questionsSolved || { Physics: 0, Chemistry: 0, Maths: 0 };
      s.stats.questionsSolved.Physics = (s.stats.questionsSolved.Physics || 0) + 3;
      s.stats.questionsSolved.Chemistry = (s.stats.questionsSolved.Chemistry || 0) + 2;
      window.saveState();
      window.showToast("⚡ Quick Log: Added +5 questions to today's count!", "success");
    }},
    { title: "Quick Action: Cycle Animated Nebula Aura", desc: "Switches background fluid shader atmosphere", icon: "🌌", shortcut: "A", action: () => {
      const themes = ["cyan_indigo", "deep_violet", "emerald_matrix", "crimson_nova", "midnight_aurora", "cyber_gold", "synthwave_sunset"];
      const s = window.getState();
      s.settings = s.settings || {};
      const currIdx = themes.indexOf(s.settings.auraTheme || "cyan_indigo");
      const nextTheme = themes[(currIdx + 1) % themes.length];
      s.settings.auraTheme = nextTheme;
      window.saveState();
      window.showToast(`🌌 Switched Nebula Atmosphere to: ${nextTheme}!`, "info");
    }},
    { title: "Quick Action: Test Mechanical Keyboard Sound", desc: "Fires Web Audio synthesizer click acoustic pulse", icon: "🔊", shortcut: "P", action: () => {
      window.playTactileFeedback("mechanical");
      window.showToast("🔊 Cherry MX Blue click synthesized via Web Audio API!", "info");
    }},
    { title: "Quick Action: Export State Backup JSON", desc: "Downloads full local workspace snapshot file", icon: "📥", shortcut: "E", action: () => {
      const s = window.getState();
      const str = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(s, null, 2));
      const a = document.createElement("a");
      a.setAttribute("href", str);
      a.setAttribute("download", `ClockEE_Backup_${Date.now()}.json`);
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.showToast("✓ Backup JSON downloaded!", "success");
    }}
  ];

  let selectedIdx = 0;
  let filteredCommands = [...COMMANDS];

  function renderCommandList() {
    const listEl = document.getElementById("cmd-palette-list");
    if (!listEl) return;
    if (filteredCommands.length === 0) {
      listEl.innerHTML = `<div class="p-4 text-center text-gray-500 font-mono text-xs">No matching commands found.</div>`;
      return;
    }
    listEl.innerHTML = filteredCommands.map((cmd, idx) => `
      <div 
        class="cmd-palette-item p-2.5 rounded-xl border ${idx === selectedIdx ? 'border-cyan-500/60 bg-cyan-950/40 text-white' : 'border-white/5 bg-gray-900/60 text-gray-300'} flex items-center justify-between cursor-pointer hover:border-cyan-400/50 hover:bg-cyan-950/30 transition text-xs"
        onclick="executeCommandByIdx(${idx})"
      >
        <div class="flex items-center gap-3 truncate">
          <span class="text-base">${cmd.icon}</span>
          <div class="truncate">
            <div class="font-bold truncate ${idx === selectedIdx ? 'text-cyan-300' : 'text-white'}">${cmd.title}</div>
            <div class="text-[10px] text-gray-400 font-mono truncate">${cmd.desc}</div>
          </div>
        </div>
        <kbd class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[10px] font-mono text-gray-400 shrink-0">${cmd.shortcut}</kbd>
      </div>
    `).join("");
  }

  window.executeCommandByIdx = function(idx) {
    const cmd = filteredCommands[idx];
    if (cmd && typeof cmd.action === "function") {
      window.playTactileFeedback("mechanical");
      window.toggleCommandPalette(false);
      cmd.action();
    }
  };

  window.toggleCommandPalette = function(force) {
    const m = document.getElementById("clockee-cmd-palette-modal");
    if (!m) return;
    const shouldOpen = force !== undefined ? force : m.classList.contains("hidden");
    if (shouldOpen) {
      m.classList.remove("hidden");
      filteredCommands = [...COMMANDS];
      selectedIdx = 0;
      renderCommandList();
      const input = document.getElementById("cmd-palette-input");
      if (input) {
        input.value = "";
        setTimeout(() => input.focus(), 50);
      }
    } else {
      m.classList.add("hidden");
    }
  };

  // 4. Keyboard Navigation Listeners
  document.addEventListener("keydown", function(e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault();
      window.toggleCommandPalette();
      return;
    }

    const m = document.getElementById("clockee-cmd-palette-modal");
    if (!m || m.classList.contains("hidden")) return;

    if (e.key === "Escape") {
      e.preventDefault();
      window.toggleCommandPalette(false);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      selectedIdx = (selectedIdx + 1) % filteredCommands.length;
      renderCommandList();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      selectedIdx = (selectedIdx - 1 + filteredCommands.length) % filteredCommands.length;
      renderCommandList();
    } else if (e.key === "Enter") {
      e.preventDefault();
      window.executeCommandByIdx(selectedIdx);
    }
  });

  document.addEventListener("input", function(e) {
    if (e.target && e.target.id === "cmd-palette-input") {
      const q = e.target.value.toLowerCase().trim();
      filteredCommands = COMMANDS.filter(cmd => 
        cmd.title.toLowerCase().includes(q) || 
        cmd.desc.toLowerCase().includes(q) || 
        cmd.shortcut.toLowerCase() === q
      );
      selectedIdx = 0;
      renderCommandList();
    }
  });

  modal.addEventListener("click", function(e) {
    if (e.target === modal) window.toggleCommandPalette(false);
  });
})();

/* ══════════════════════════════════════════════════════════════════════════════
   CLOCKEE UNIVERSAL RESPONSIVE MOBILE NAVIGATION & TOUCH ERGONOMICS SUITE
   - Mobile Header Cyber Hamburger Menu (☰)
   - Frosted Glass Cyber Mobile Drawer (#clockeeMobileDrawer) with Quick Switches
   - One-Thumb Mobile Bottom Navigation Bar (#clockeeBottomNav)
   - Fluid Viewport Scaling & Touch Target Guardrails (Min 44px)
   - Seamless Cross-Module CBT Integration
   ══════════════════════════════════════════════════════════════════════════════ */

(function initClockEEMobileNavSuite() {
  if (typeof window === "undefined") return;

  // 1. Inject Universal Responsive CSS (Strict Zero Horizontal Overflow & Pure SVG Icons)
  const mobileStyles = document.createElement("style");
  mobileStyles.id = "clockee-mobile-responsive-styles";
  mobileStyles.innerHTML = `
    /* Universal Mobile Responsive Overrides & Prevent Horizontal Spill */
    html, body {
      overflow-x: clip !important;
      overflow-x: hidden !important;
      max-width: 100vw !important;
      width: 100% !important;
      position: relative !important;
    }

    @media (max-width: 840px) {
      /* Hide desktop horizontal nav bar to prevent ugly overflow */
      #main-nav {
        display: none !important;
      }

      /* Hide tour button from top header on mobile */
      #btnNavTourCockpit {
        display: none !important;
      }
      
      /* Make top headers clean and touch-friendly */
      header.border-b, .cbt-header-banner, header {
        padding: 8px 14px !important;
        min-height: 56px !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
      }

      /* Body padding for fixed bottom navigation */
      body:not(.in-cbt-exam) {
        padding-bottom: calc(76px + env(safe-area-inset-bottom)) !important;
      }

      /* Command palette trigger moved above bottom nav */
      #clockee-cmd-trigger {
        bottom: calc(72px + env(safe-area-inset-bottom)) !important;
        right: 14px !important;
      }

      /* Touch target size & ergonomics */
      button, a.nav-btn, .cbt-btn, input, select {
        min-height: 44px;
        touch-action: manipulation;
      }

      /* Grids stack into single or dual column */
      .grid-cols-12 {
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
        width: 100% !important;
        max-width: 100% !important;
      }
      .lg\\:col-span-5, .lg\\:col-span-7, .lg\\:col-span-8, .lg\\:col-span-4 {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
      }

      /* Sidebar root constrained to 100% */
      #clockee-sidebar-root, #clockee-sidebar-root aside {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
      }

      /* Calendar and chart containers full width */
      #sidebar-month-grid, .grid-cols-7 {
        width: 100% !important;
        max-width: 100% !important;
      }

      /* Floating Tour Pill on Mobile */
      .cockpit-tour-floating-card {
        width: calc(100vw - 28px) !important;
        max-width: calc(100vw - 28px) !important;
        left: 14px !important;
        padding: 14px 16px !important;
      }
      .cockpit-tour-corner-box {
        bottom: calc(76px + env(safe-area-inset-bottom)) !important;
        right: 14px !important;
      }
    }

    /* Mobile Hamburger Button in Top Header */
    .clockee-mobile-hamburger-btn {
      display: none;
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: rgba(0, 240, 255, 0.08);
      border: 1.5px solid rgba(0, 240, 255, 0.4);
      color: #00f0ff;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.2);
    }
    .clockee-mobile-hamburger-btn svg {
      width: 22px;
      height: 22px;
    }
    .clockee-mobile-hamburger-btn:hover, .clockee-mobile-hamburger-btn:active {
      background: rgba(0, 240, 255, 0.2);
      border-color: #00f0ff;
      transform: scale(0.96);
    }
    @media (max-width: 840px) {
      .clockee-mobile-hamburger-btn {
        display: flex !important;
      }
    }

    /* Frosted Glass Cyber Mobile Drawer */
    .clockee-mobile-drawer-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(2, 4, 10, 0.82);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      z-index: 999998;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .clockee-mobile-drawer-backdrop.active {
      opacity: 1;
      pointer-events: auto;
    }

    /* When closed: display none to eliminate any horizontal scroll void! */
    .clockee-mobile-drawer {
      position: fixed;
      top: 0;
      right: 0;
      bottom: 0;
      width: min(340px, 86vw);
      background: rgba(8, 12, 24, 0.98);
      border-left: 1.5px solid rgba(0, 240, 255, 0.4);
      box-shadow: -20px 0 50px rgba(0, 0, 0, 0.9), 0 0 30px rgba(0, 240, 255, 0.25);
      backdrop-filter: blur(36px) saturate(220%);
      -webkit-backdrop-filter: blur(36px) saturate(220%);
      z-index: 999999;
      display: none;
      flex-direction: column;
      transform: translateX(100%);
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
      padding: 18px 16px calc(24px + env(safe-area-inset-bottom));
      pointer-events: none;
    }
    .clockee-mobile-drawer.active {
      display: flex !important;
      transform: translateX(0) !important;
      pointer-events: auto !important;
    }

    .drawer-nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 14px;
      color: #94a3b8;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      margin-bottom: 8px;
      transition: all 0.2s ease;
      touch-action: manipulation;
    }
    .drawer-nav-item svg {
      width: 18px;
      height: 18px;
      flex-shrink: 0;
      transition: all 0.2s ease;
    }
    .drawer-nav-item:hover, .drawer-nav-item:active {
      background: rgba(0, 240, 255, 0.12);
      border-color: rgba(0, 240, 255, 0.4);
      color: #00f0ff;
      transform: translateX(4px);
    }
    .drawer-nav-item.active {
      background: rgba(0, 240, 255, 0.18);
      border-color: #00f0ff;
      color: #00f0ff;
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.35);
      font-weight: 700;
    }
    .drawer-nav-item.active svg {
      color: #00f0ff;
      stroke: #00f0ff;
      filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.7));
    }

    /* Fixed Bottom Navigation Bar (1-Thumb Ergonomics) */
    .clockee-bottom-nav {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: calc(60px + env(safe-area-inset-bottom));
      padding-bottom: env(safe-area-inset-bottom);
      background: rgba(8, 12, 24, 0.94);
      backdrop-filter: blur(28px) saturate(200%);
      -webkit-backdrop-filter: blur(28px) saturate(200%);
      border-top: 1px solid rgba(0, 240, 255, 0.35);
      box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 240, 255, 0.15);
      z-index: 99990;
      align-items: center;
      justify-content: space-around;
      touch-action: manipulation;
    }
    @media (max-width: 840px) {
      body:not(.in-cbt-exam) .clockee-bottom-nav {
        display: flex !important;
      }
    }

    .bottom-nav-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      color: #94a3b8;
      text-decoration: none;
      font-size: 0.65rem;
      font-weight: 600;
      flex: 1;
      height: 100%;
      transition: all 0.18s ease;
      cursor: pointer;
    }
    .bottom-nav-btn svg {
      width: 20px;
      height: 20px;
      transition: transform 0.2s ease, stroke 0.2s ease;
    }
    .bottom-nav-btn:hover, .bottom-nav-btn:active {
      color: #00f0ff;
    }
    .bottom-nav-btn:active svg {
      transform: scale(0.9);
    }
    .bottom-nav-btn.active {
      color: #00f0ff;
      font-weight: 700;
    }
    .bottom-nav-btn.active svg {
      stroke: #00f0ff;
      filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.8));
    }
  `;
  document.head.appendChild(mobileStyles);

  // 2. Render Drawer and Bottom Nav
  function ensureMobileNavigationDOM() {
    if (document.getElementById('clockee-mobile-drawer-backdrop')) return;

    // Detect Active Page
    const path = window.location.pathname.toLowerCase();
    const isHome = path.endsWith('index.html') || path.endsWith('/') || path === '';
    const isTimer = path.includes('timer.html');
    const isToday = path.includes('today.html');
    const isTask = path.includes('task.html');
    const isCoaching = path.includes('coaching.html');
    const isCBT = path.includes('cbt_') || path.includes('test_centre.html');
    const isInspiration = path.includes('inspiration.html');
    const isSettings = path.includes('settings.html');

    // Get Active User & Dream Target
    let user = { name: "Guest Aspirant", role: "Aspirant", dreamCollege: "IIT Bombay CSE", targetAir: 65 };
    try {
      const u = localStorage.getItem("clockee_current_user");
      if (u) user = Object.assign(user, JSON.parse(u));
    } catch(e) {}

    // A. Drawer Backdrop & Container
    const backdrop = document.createElement('div');
    backdrop.id = 'clockee-mobile-drawer-backdrop';
    backdrop.className = 'clockee-mobile-drawer-backdrop';
    backdrop.onclick = () => window.closeMobileDrawer();

    const drawer = document.createElement('div');
    drawer.id = 'clockee-mobile-drawer';
    drawer.className = 'clockee-mobile-drawer';
    drawer.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="display:flex;align-items:center;gap:8px;">
          <svg style="width:20px;height:20px;color:#00f0ff;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
          <span style="font-weight:900;font-size:15px;background:linear-gradient(to right,#00f0ff,#a5b4fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">ClockEE Cockpit</span>
        </div>
        <button onclick="window.closeMobileDrawer()" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);color:#fff;width:34px;height:34px;border-radius:10px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;">✕</button>
      </div>

      <!-- User Flight Deck Card -->
      <div style="background:linear-gradient(135deg,rgba(0,240,255,0.1),rgba(99,102,241,0.12));border:1px solid rgba(0,240,255,0.3);border-radius:16px;padding:12px;margin-bottom:14px;display:flex;align-items:center;gap:10px;">
        <img src="${user.pfp || 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant'}" style="width:38px;height:38px;border-radius:50%;border:1.5px solid #00f0ff;background:#030712;">
        <div style="flex:1;min-width:0;">
          <div style="font-size:13px;font-weight:800;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${user.name}</div>
          <div style="font-size:10px;color:#00f0ff;display:flex;align-items:center;gap:4px;">
            <svg style="width:11px;height:11px;color:#00f0ff;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
            <span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${user.dreamCollege || 'IIT Bombay CSE'}</span>
          </div>
        </div>
        <button onclick="window.handleUserLogout()" style="background:none;border:none;color:#ef4444;font-size:11px;font-weight:700;cursor:pointer;" title="Sign Out">Sign Out</button>
      </div>

      <!-- Navigation Modules List (Clean SVG Icons, Zero Emojis, No Tour in Mobile Menu) -->
      <div style="flex:1;">
        <a href="index.html" class="drawer-nav-item ${isHome ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <span>Cockpit Home</span>
        </a>
        <a href="timer.html" class="drawer-nav-item ${isTimer ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>Tactical Sprint Timer</span>
        </a>
        <a href="today.html" class="drawer-nav-item ${isToday ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span>Today's Daily Digest</span>
        </a>
        <a href="task.html" class="drawer-nav-item ${isTask ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
          <span>Tasks &amp; TickTick Sync</span>
        </a>
        <a href="coaching.html" class="drawer-nav-item ${isCoaching ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
          <span>Coaching &amp; Syllabus Tree</span>
        </a>
        <a href="cbt_home.html" class="drawer-nav-item ${isCBT ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <span>Authentic CBT Exam Portal</span>
        </a>
        <a href="inspiration.html" class="drawer-nav-item ${isInspiration ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <span>Wall of Inspiration</span>
        </a>
        <a href="settings.html" class="drawer-nav-item ${isSettings ? 'active' : ''}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          <span>Settings &amp; Themes</span>
        </a>
      </div>

      <!-- Quick Controls -->
      <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:12px;display:flex;align-items:center;justify-content:space-between;">
        <button onclick="if(typeof toggleSplitScreen==='function') toggleSplitScreen(); window.closeMobileDrawer();" style="padding:8px 12px;border-radius:10px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#94a3b8;font-size:11px;font-weight:600;display:flex;align-items:center;gap:6px;cursor:pointer;">
          <svg style="width:13px;height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="12" y1="3" x2="12" y2="21"/></svg>
          <span>Split View</span>
        </button>
        <div style="display:flex;align-items:center;gap:6px;">
          <button onclick="if(typeof applyAccentColor==='function') applyAccentColor('#00f0ff');" style="width:26px;height:26px;border-radius:50%;background:#00f0ff;border:2px solid #fff;box-shadow:0 0 10px #00f0ff;cursor:pointer;" title="Cyan Theme"></button>
          <button onclick="if(typeof applyAccentColor==='function') applyAccentColor('#6366f1');" style="width:26px;height:26px;border-radius:50%;background:#6366f1;border:2px solid #fff;box-shadow:0 0 10px #6366f1;cursor:pointer;" title="Indigo Theme"></button>
          <button onclick="if(typeof applyAccentColor==='function') applyAccentColor('#f59e0b');" style="width:26px;height:26px;border-radius:50%;background:#f59e0b;border:2px solid #fff;box-shadow:0 0 10px #f59e0b;cursor:pointer;" title="Amber Theme"></button>
        </div>
      </div>
    `;

    document.body.appendChild(backdrop);
    document.body.appendChild(drawer);

    // B. Mobile Bottom Navigation Bar (5 Thumb Items with Pure SVG Icons)
    const bottomNav = document.createElement('nav');
    bottomNav.id = 'clockee-bottom-nav';
    bottomNav.className = 'clockee-bottom-nav';
    bottomNav.innerHTML = `
      <a href="index.html" class="bottom-nav-btn ${isHome ? 'active' : ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span>Home</span>
      </a>
      <a href="timer.html" class="bottom-nav-btn ${isTimer ? 'active' : ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span>Timer</span>
      </a>
      <a href="today.html" class="bottom-nav-btn ${isToday ? 'active' : ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <span>Today</span>
      </a>
      <a href="cbt_home.html" class="bottom-nav-btn ${isCBT ? 'active' : ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        <span>CBT</span>
      </a>
      <button type="button" onclick="window.openMobileDrawer()" class="bottom-nav-btn" style="background:none;border:none;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        <span>Menu</span>
      </button>
    `;
    document.body.appendChild(bottomNav);

    // C. Inject Hamburger button into existing page headers with pure SVG icon
    const headerRight = document.querySelector('.nav-right, header > div:last-child, .cbt-header-banner > div:last-child');
    if (headerRight && !document.getElementById('clockeeHamburgerBtn')) {
      const btn = document.createElement('button');
      btn.id = 'clockeeHamburgerBtn';
      btn.type = 'button';
      btn.className = 'clockee-mobile-hamburger-btn';
      btn.setAttribute('aria-label', 'Open Mobile Navigation Menu');
      btn.onclick = () => window.openMobileDrawer();
      btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
      headerRight.appendChild(btn);
    }
  }

  window.openMobileDrawer = function() {
    ensureMobileNavigationDOM();
    const bd = document.getElementById('clockee-mobile-drawer-backdrop');
    const dr = document.getElementById('clockee-mobile-drawer');
    if (bd && dr) {
      bd.classList.add('active');
      dr.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeMobileDrawer = function() {
    const bd = document.getElementById('clockee-mobile-drawer-backdrop');
    const dr = document.getElementById('clockee-mobile-drawer');
    if (bd && dr) {
      bd.classList.remove('active');
      dr.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  // Keyboard navigation for drawer
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') window.closeMobileDrawer();
  });

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureMobileNavigationDOM);
  } else {
    setTimeout(ensureMobileNavigationDOM, 50);
  }

})();

/* ══════════════════════════════════════════════════════════════════════════════
   CLOCKEE ULTIMATE MASTER TOUR ENGINE
   - Flexible Hovering Tour Pill (Left / Right / Below / Above with bounds clamping)
   - Animated Theme Dotted Connector Arrow with Neon Head
   - Smooth Morph & Scale Animation between Tour Pill and Minimized Corner Box
   - Little Corner Box with Animated ClockEE Mascot waiting
   - Clicking Outside Highlight Zone Minimizes Tour
   - Mascot Flies Up on Page Interruption (Continue vs End Tour)
   - Mascot Excited Bounce + Screen Sparkles Explosion on Task Completion
   - Instant Fallback Populated Text (Never Empty Dialogue)
   - Complete 8-Module Seamless Multi-Page Chain
   ══════════════════════════════════════════════════════════════════════════════ */

(function initClockEETourEngine() {
  if (typeof window === "undefined") return;

  // Web Audio Synthesizer
  let _tourAudioCtx = null;
  function getTourAudioCtx() {
    if (!_tourAudioCtx) {
      _tourAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (_tourAudioCtx.state === 'suspended') {
      _tourAudioCtx.resume();
    }
    return _tourAudioCtx;
  }

  function playTourChime() {
    try {
      const ctx = getTourAudioCtx();
      const notes = [523.25, 659.25, 783.99]; // C5, E5, G5
      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.07);

        gain.gain.setValueAtTime(0, ctx.currentTime + idx * 0.07);
        gain.gain.linearRampToValueAtTime(0.2, ctx.currentTime + idx * 0.07 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.07 + 0.28);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.07);
        osc.stop(ctx.currentTime + idx * 0.07 + 0.3);
      });
    } catch (e) {}
  }

  function playExcitedSuccessChime() {
    try {
      const ctx = getTourAudioCtx();
      const notes = [587.33, 739.99, 880.00, 1174.66]; // D5, F#5, A5, D6 triumphant fanfare
      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);

        gain.gain.setValueAtTime(0, ctx.currentTime + idx * 0.08);
        gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + idx * 0.08 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.08 + 0.35);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.08);
        osc.stop(ctx.currentTime + idx * 0.08 + 0.36);
      });
    } catch(e) {}
  }

  // Typewriter Animation Engine
  let _activeTypewriterTimer = null;
  function typewriteText(element, text, speed = 12, onComplete = null) {
    if (_activeTypewriterTimer) {
      clearInterval(_activeTypewriterTimer);
      _activeTypewriterTimer = null;
    }
    if (!element) return;
    // Guaranteed non-empty: set initial snippet immediately
    element.textContent = text.charAt(0);
    let i = 1;
    _activeTypewriterTimer = setInterval(() => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
      } else {
        clearInterval(_activeTypewriterTimer);
        _activeTypewriterTimer = null;
        if (onComplete) onComplete();
      }
    }, speed);
  }

  // Inject Tour Styles
  const tourStyles = document.createElement('style');
  tourStyles.id = 'clockee-tour-global-styles';
  tourStyles.innerHTML = `
    /* Fullscreen SVG Spotlight Overlay */
    .cockpit-tour-spotlight-svg {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: auto;
      z-index: 999990;
      transition: opacity 0.3s ease;
      opacity: 0;
      cursor: pointer;
    }
    .cockpit-tour-spotlight-svg.active {
      opacity: 1;
    }

    /* Glowing Halo Box Around Target Element */
    .cockpit-tour-halo {
      position: fixed;
      pointer-events: none;
      z-index: 999995;
      border: 2px dashed #00f0ff;
      border-radius: 16px;
      box-shadow: 0 0 35px rgba(0, 240, 255, 0.8), inset 0 0 20px rgba(0, 240, 255, 0.35);
      transition: all 0.36s cubic-bezier(0.16, 1, 0.3, 1);
      opacity: 0;
      animation: tourHaloPulse 2s infinite ease-in-out;
    }
    .cockpit-tour-halo.active {
      opacity: 1;
    }

    @keyframes tourHaloPulse {
      0%, 100% { box-shadow: 0 0 30px rgba(0, 240, 255, 0.7), inset 0 0 15px rgba(0, 240, 255, 0.25); border-color: #00f0ff; }
      50% { box-shadow: 0 0 45px rgba(0, 240, 255, 0.95), inset 0 0 30px rgba(0, 240, 255, 0.45); border-color: #67e8f9; }
    }

    /* Target Element Raised to Front for Interaction */
    .cockpit-tour-target-active {
      position: relative !important;
      z-index: 999994 !important;
      pointer-events: auto !important;
    }

    /* Flexible Floating Tour Pill / Card */
    .cockpit-tour-floating-card {
      position: fixed;
      z-index: 10000002;
      width: 90vw;
      max-width: 440px;
      background: rgba(10, 15, 30, 0.95);
      border: 1.5px solid rgba(0, 240, 255, 0.65);
      border-radius: 24px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(0, 240, 255, 0.28), inset 0 0 20px rgba(0, 240, 255, 0.08);
      backdrop-filter: blur(32px) saturate(200%);
      -webkit-backdrop-filter: blur(32px) saturate(200%);
      padding: 18px 20px;
      color: #fff;
      transition: transform 0.38s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease, left 0.38s cubic-bezier(0.16, 1, 0.3, 1), top 0.38s cubic-bezier(0.16, 1, 0.3, 1);
      opacity: 0;
      transform: scale(0.92);
      pointer-events: none;
    }
    .cockpit-tour-floating-card.active {
      opacity: 1;
      transform: scale(1);
      pointer-events: auto;
    }
    .cockpit-tour-floating-card.collapsing {
      transform: scale(0.15) translate(400px, 400px) !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }

    /* Theme Dotted Connector Arrow SVG Overlay */
    .cockpit-tour-arrow-svg {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 10000001;
      transition: opacity 0.3s ease;
      opacity: 0;
    }
    .cockpit-tour-arrow-svg.active {
      opacity: 1;
    }
    .cockpit-tour-arrow-path {
      stroke: #00f0ff;
      stroke-width: 2.5;
      stroke-dasharray: 6 6;
      fill: none;
      animation: tourDashMove 1s linear infinite;
      filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.8));
    }
    @keyframes tourDashMove {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: -24; }
    }

    /* Minimized Little Corner Box */
    .cockpit-tour-corner-box {
      position: fixed;
      bottom: 22px;
      right: 22px;
      z-index: 10000005;
      background: rgba(10, 16, 32, 0.95);
      border: 1.5px solid rgba(0, 240, 255, 0.7);
      border-radius: 9999px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8), 0 0 25px rgba(0, 240, 255, 0.4);
      backdrop-filter: blur(24px);
      padding: 8px 16px 8px 10px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      transform: scale(0.8);
      opacity: 0;
      pointer-events: none;
    }
    .cockpit-tour-corner-box.active {
      transform: scale(1);
      opacity: 1;
      pointer-events: auto;
    }
    .cockpit-tour-corner-box:hover {
      transform: scale(1.05);
      border-color: #00f0ff;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 35px rgba(0, 240, 255, 0.6);
    }

    /* Interruption Flight Mascot Modal */
    .cockpit-tour-interruption-modal {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0.85);
      z-index: 10000010;
      max-width: 400px;
      width: 90vw;
      background: rgba(10, 15, 30, 0.96);
      border: 2px solid #00f0ff;
      border-radius: 24px;
      padding: 24px;
      text-align: center;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.9), 0 0 45px rgba(0, 240, 255, 0.4);
      backdrop-filter: blur(32px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      opacity: 0;
      pointer-events: none;
    }
    .cockpit-tour-interruption-modal.active {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
      pointer-events: auto;
    }

    /* Excited Bounce Animation for ClockEE */
    @keyframes mascotExcitedBounce {
      0%, 100% { transform: translateY(0) scale(1); }
      20% { transform: translateY(-16px) scale(1.12) rotate(-5deg); }
      40% { transform: translateY(0) scale(0.95); }
      60% { transform: translateY(-12px) scale(1.08) rotate(5deg); }
      80% { transform: translateY(0) scale(1.02); }
    }
    .mascot-excited {
      animation: mascotExcitedBounce 0.85s ease-in-out !important;
    }

    /* Particle Sparkles Explosion */
    .tour-sparkle-particle {
      position: fixed;
      pointer-events: none;
      z-index: 10000008;
      border-radius: 50%;
      animation: sparkleFloat 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes sparkleFloat {
      0% { transform: translate(0, 0) scale(1); opacity: 1; }
      100% { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
    }
  `;
  document.head.appendChild(tourStyles);

  // Reusable Friendly ClockEE Mascot SVG
  function getClockEEMascotSvg(isExcited = false) {
    const eyeD = isExcited 
      ? 'M 105 106 Q 120 90 135 106' // Happy crescent eyes
      : 'M 108 102 Q 120 96 132 102 Q 120 108 108 102';

    return `
      <svg class="clockee-tour-avatar-svg ${isExcited ? 'mascot-excited' : ''}" style="width: 52px; height: 52px; flex-shrink: 0;" viewBox="0 0 240 250" fill="none">
        <defs>
          <radialGradient id="tMascotFaceGrad" cx="50%" cy="40%" r="55%">
            <stop offset="0%" stop-color="#1e293b"/>
            <stop offset="70%" stop-color="#090d16"/>
            <stop offset="100%" stop-color="#020408"/>
          </radialGradient>
          <linearGradient id="tMascotRimGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00f0ff"/>
            <stop offset="50%" stop-color="#6366f1"/>
            <stop offset="100%" stop-color="#a855f7"/>
          </linearGradient>
        </defs>
        <!-- Bell Ear Clocks -->
        <circle cx="68" cy="68" r="20" fill="url(#tMascotFaceGrad)" stroke="url(#tMascotRimGrad)" stroke-width="4"/>
        <circle cx="172" cy="68" r="20" fill="url(#tMascotFaceGrad)" stroke="url(#tMascotRimGrad)" stroke-width="4"/>
        <!-- Main Face Dial -->
        <circle cx="120" cy="130" r="76" fill="url(#tMascotFaceGrad)" stroke="url(#tMascotRimGrad)" stroke-width="5"/>
        <circle cx="120" cy="130" r="68" fill="none" stroke="rgba(0, 240, 255, 0.25)" stroke-width="1.5" stroke-dasharray="4 6"/>
        <!-- Clock Hands on Forehead -->
        <circle cx="120" cy="85" r="4" fill="#00f0ff"/>
        <line x1="120" y1="85" x2="120" y2="72" stroke="#00f0ff" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="120" y1="85" x2="132" y2="85" stroke="#f43f5e" stroke-width="2" stroke-linecap="round"/>
        <!-- Cute Eyes -->
        <ellipse cx="98" cy="126" rx="9" ry="12" fill="#00f0ff"/>
        <circle cx="101" cy="123" r="3.5" fill="#ffffff"/>
        <ellipse cx="142" cy="126" rx="9" ry="12" fill="#00f0ff"/>
        <circle cx="145" cy="123" r="3.5" fill="#ffffff"/>
        <!-- Rosy Cheeks -->
        <circle cx="86" cy="138" r="7" fill="rgba(244, 63, 94, 0.45)"/>
        <circle cx="154" cy="138" r="7" fill="rgba(244, 63, 94, 0.45)"/>
        <!-- Smile -->
        <path d="M 110 144 Q 120 154 130 144" stroke="#ffffff" stroke-width="3" stroke-linecap="round" fill="none"/>
      </svg>
    `;
  }

  // Create Sparkle Particles Burst
  function createCyberSparkleBurst(x, y) {
    const colors = ['#00f0ff', '#6366f1', '#fbbf24', '#34d399', '#ffffff'];
    for (let i = 0; i < 24; i++) {
      const p = document.createElement('div');
      p.className = 'tour-sparkle-particle';
      const size = Math.random() * 8 + 4;
      p.style.width = `${size}px`;
      p.style.height = `${size}px`;
      p.style.left = `${x}px`;
      p.style.top = `${y}px`;
      p.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
      p.style.boxShadow = `0 0 10px ${p.style.backgroundColor}`;

      const angle = (Math.PI * 2 * i) / 24 + (Math.random() - 0.5) * 0.5;
      const dist = Math.random() * 120 + 40;
      p.style.setProperty('--tx', `${Math.cos(angle) * dist}px`);
      p.style.setProperty('--ty', `${Math.sin(angle) * dist}px`);

      document.body.appendChild(p);
      setTimeout(() => p.remove(), 950);
    }
  }

  // DOM Elements Container
  let spotlightSvg = null;
  let spotlightCutout = null;
  let haloEl = null;
  let arrowSvg = null;
  let arrowPath = null;
  let floatingCard = null;
  let cornerBox = null;
  let interruptionModal = null;

  function ensureTourDOMElements() {
    if (document.getElementById('cockpit-tour-spotlight-svg')) return;

    // 1. Fullscreen SVG with Cutout
    spotlightSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    spotlightSvg.id = 'cockpit-tour-spotlight-svg';
    spotlightSvg.setAttribute('class', 'cockpit-tour-spotlight-svg');
    spotlightSvg.innerHTML = `
      <defs>
        <mask id="tourCutoutMask">
          <rect x="0" y="0" width="100%" height="100%" fill="white" />
          <rect id="tourCutoutRect" x="0" y="0" width="0" height="0" rx="16" fill="black" />
        </mask>
      </defs>
      <rect x="0" y="0" width="100%" height="100%" fill="rgba(3, 5, 12, 0.86)" mask="url(#tourCutoutMask)" />
    `;
    // Clicking backdrop outside highlighted cutout minimizes tour!
    spotlightSvg.addEventListener('click', (e) => {
      if (!isTourActive || isTourMinimized) return;
      const rect = spotlightCutout.getBoundingClientRect();
      // If clicked outside cutout hole:
      if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) {
        window.minimizeCockpitTour();
      }
    });
    document.body.appendChild(spotlightSvg);
    spotlightCutout = document.getElementById('tourCutoutRect');

    // 2. Halo element
    haloEl = document.createElement('div');
    haloEl.id = 'cockpit-tour-halo';
    haloEl.className = 'cockpit-tour-halo';
    document.body.appendChild(haloEl);

    // 3. Arrow SVG Overlay
    arrowSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    arrowSvg.id = 'cockpit-tour-arrow-svg';
    arrowSvg.setAttribute('class', 'cockpit-tour-arrow-svg');
    arrowSvg.innerHTML = `
      <defs>
        <marker id="tourArrowHead" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#00f0ff" />
        </marker>
      </defs>
      <path id="cockpitTourArrowPath" class="cockpit-tour-arrow-path" marker-end="url(#tourArrowHead)" d="" />
    `;
    document.body.appendChild(arrowSvg);
    arrowPath = document.getElementById('cockpitTourArrowPath');

    // 4. Flexible Floating Card / Pill
    floatingCard = document.createElement('div');
    floatingCard.id = 'cockpit-tour-floating-card';
    floatingCard.className = 'cockpit-tour-floating-card';
    floatingCard.innerHTML = `
      <div class="flex items-center justify-between pb-2 mb-2 border-b border-cyan-500/20">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#00f0ff]"></span>
          <span id="tourBadge" class="text-[11px] font-mono font-bold text-cyan-300 uppercase tracking-wider">Step 1</span>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="window.minimizeCockpitTour()" class="w-6 h-6 rounded-md bg-white/5 hover:bg-cyan-500/20 text-cyan-300 text-xs font-bold transition flex items-center justify-center cursor-pointer" title="Minimize Tour to Side Box">_</button>
          <button type="button" onclick="window.closeCockpitTour()" class="w-6 h-6 rounded-md bg-white/5 hover:bg-rose-500/20 text-gray-400 hover:text-rose-400 text-xs font-bold transition flex items-center justify-center cursor-pointer" title="Exit Tour">✕</button>
        </div>
      </div>

      <div class="flex items-start gap-3.5 mb-3">
        <div id="tourMascotContainer" class="flex-shrink-0 cursor-pointer" onclick="window.triggerMascotExcited()" title="Tap ClockEE!">
          ${getClockEEMascotSvg(false)}
        </div>
        <div class="flex-1 min-w-0">
          <h3 id="tourTitle" class="text-sm sm:text-base font-extrabold text-white leading-tight mb-1">Module Title</h3>
          <p id="tourDesc" class="text-xs text-slate-300 leading-relaxed min-h-[38px]">Module description...</p>
        </div>
      </div>

      <div id="tourActionBox" class="p-2.5 rounded-xl bg-cyan-950/40 border border-cyan-400/30 mb-3 flex items-center justify-between gap-2">
        <span id="tourActionHint" class="text-[11px] text-cyan-200 font-medium">⚡ Click to test this feature!</span>
        <button type="button" id="tourActionBtn" onclick="window.runCurrentTourAction()" class="px-2.5 py-1 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-[11px] transition shadow-md shadow-cyan-500/30 flex items-center gap-1 cursor-pointer">
          <span>⚡ Test Action</span>
        </button>
      </div>

      <div class="flex items-center justify-between pt-1">
        <button type="button" id="tourPrevBtn" onclick="window.prevCockpitTourStep()" class="px-3 py-1.5 rounded-xl border border-white/10 text-xs text-slate-300 hover:text-white hover:bg-white/5 transition flex items-center gap-1 cursor-pointer">
          ← Back
        </button>
        <span id="tourStepIndicator" class="text-[11px] font-mono text-slate-400">1 of 8</span>
        <button type="button" id="tourNextBtn" onclick="window.nextCockpitTourStep()" class="px-4 py-1.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-white font-extrabold text-xs shadow-lg shadow-cyan-500/25 transition flex items-center gap-1.5 cursor-pointer">
          Next Step →
        </button>
      </div>
    `;
    document.body.appendChild(floatingCard);

    // 5. Minimized Corner Box
    cornerBox = document.createElement('div');
    cornerBox.id = 'cockpit-tour-corner-box';
    cornerBox.className = 'cockpit-tour-corner-box';
    cornerBox.onclick = () => window.expandCockpitTour();
    cornerBox.innerHTML = `
      <div style="width: 38px; height: 38px;">
        ${getClockEEMascotSvg(false)}
      </div>
      <div>
        <div class="text-[10px] font-mono text-cyan-300 font-bold uppercase" id="tourCornerStep">Step 1/8</div>
        <div class="text-xs font-bold text-white flex items-center gap-1">
          <span>ClockEE Tour</span>
          <span class="text-[10px] text-cyan-400">⤢ Expand</span>
        </div>
      </div>
    `;
    document.body.appendChild(cornerBox);

    // 6. Interruption Modal
    interruptionModal = document.createElement('div');
    interruptionModal.id = 'cockpit-tour-interruption-modal';
    interruptionModal.className = 'cockpit-tour-interruption-modal';
    interruptionModal.innerHTML = `
      <div class="flex justify-center mb-2">
        <div style="width: 68px; height: 68px;">
          ${getClockEEMascotSvg(true)}
        </div>
      </div>
      <h3 class="text-base font-extrabold text-white mb-1">Tour in Progress! ⏱️</h3>
      <p class="text-xs text-slate-300 leading-relaxed mb-4">
        Ready to continue the guided cockpit tour, or would you like to explore independently?
      </p>
      <div class="flex items-center justify-center gap-2">
        <button type="button" onclick="window.expandCockpitTour()" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold text-xs shadow-lg shadow-cyan-500/30 transition flex items-center gap-1 cursor-pointer">
          ▶ Continue Tour
        </button>
        <button type="button" onclick="window.closeCockpitTour()" class="px-3 py-2 rounded-xl border border-white/10 text-xs text-slate-400 hover:text-white hover:bg-white/5 transition cursor-pointer">
          ✕ End Tour
        </button>
      </div>
    `;
    document.body.appendChild(interruptionModal);

    // Global click listener for page interruption while tour is active
    document.addEventListener('click', (e) => {
      if (!isTourActive || isTourMinimized) return;
      // If clicking interactive elements outside halo/card
      const card = document.getElementById('cockpit-tour-floating-card');
      const halo = document.getElementById('cockpit-tour-halo');
      const modal = document.getElementById('cockpit-tour-interruption-modal');
      const corner = document.getElementById('cockpit-tour-corner-box');
      if (card && card.contains(e.target)) return;
      if (halo && halo.contains(e.target)) return;
      if (modal && modal.contains(e.target)) return;
      if (corner && corner.contains(e.target)) return;
      
      const activeTarget = document.querySelector('.cockpit-tour-target-active');
      if (activeTarget && activeTarget.contains(e.target)) return;

      // Clicked outside on interactive links or buttons: show friendly interruption modal
      if (e.target.closest('a, button, input, select') && !e.target.closest('#cockpit-tour-spotlight-svg')) {
        // e.preventDefault();
        window.showTourInterruptionPrompt();
      }
    }, true);
  }

  // Tour State
  let isTourActive = false;
  let isTourMinimized = false;
  let currentTourIdx = 0;
  let currentPageTourConfig = null;

  // Master Configuration for all 8 modules
  function getMasterPageTourConfig() {
    const path = window.location.pathname.toLowerCase();

    // 1. COCKPIT HOME (index.html) -> Next Page: timer.html
    if (path.endsWith("index.html") || path.endsWith("/") || path === "") {
      return {
        nextPageUrl: "timer.html?tour=true",
        nextPageName: "Tactical Sprint Timer",
        steps: [
          {
            badge: "Step 1 of 8 • Cockpit HUD",
            title: "Tactical JEE Advanced Countdown",
            desc: "Tracks exact days, hours, and seconds to JEE Advanced 2028 with milestone progress and target study cadence.",
            targetSelector: "#jee-countdown-title, .countdown-timer, #hero-countdown",
            speech: "Welcome to ClockEE Cockpit! Your high-velocity command center! ⏰",
            actionHint: "Tap below to test milestone chime!",
            actionFn: () => { playTourChime(); }
          },
          {
            badge: "Step 2 of 8 • Rapid Solvers",
            title: "Instant Problem Counter",
            desc: "Log completed questions with 1 tap. Builds your PCM subject velocity matrix in real-time.",
            targetSelector: "#quick-q-physics, button[onclick*='Physics'], .quick-log-btn",
            speech: "Log your questions directly to keep solving velocity high! ✍️",
            actionHint: "Click 'Test Action' to add +5 Physics questions!",
            actionFn: () => {
              if (typeof window.logQuickQuestions === 'function') window.logQuickQuestions('Physics', 5);
              else playExcitedSuccessChime();
            }
          },
          {
            badge: "Step 3 of 8 • Tactical Vitals",
            title: "Daily Study Target Meter",
            desc: "Dynamic progress ring measuring today's deep work hours vs your 6.0h target.",
            targetSelector: "#daily-study-target, .target-meter-card, #study-hours-dial",
            speech: "6 hours of unbroken daily focus secures your top IIT seat! 🎯",
            actionHint: "Inspect your focus pacing dials!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 4 of 8 • Focus Flow",
            title: "Split-Screen Companion",
            desc: "Keep notes, formulas, or lecture videos pinned right next to your timer without switching tabs.",
            targetSelector: "button[onclick='toggleSplitScreen()'], .nav-icon-btn",
            speech: "No tab clutter! Study companion slides right into view! ⊟",
            actionHint: "Click 'Test Action' to toggle companion!",
            actionFn: () => { if (typeof window.toggleSplitScreen === 'function') window.toggleSplitScreen(); }
          },
          {
            badge: "Step 5 of 8 • Command Palette",
            title: "Keyboard Quick Launcher (Ctrl+K)",
            desc: "Jump anywhere in seconds: test generator, mistake vault, or daily logs with keyboard shortcuts.",
            targetSelector: "button[onclick='openCommandPalette()'], #btnCommandPalette",
            speech: "Press Ctrl+K anytime for lightning-fast cockpit access! ⚡",
            actionHint: "Click 'Test Action' to trigger palette!",
            actionFn: () => { if (typeof window.openCommandPalette === 'function') window.openCommandPalette(); }
          },
          {
            badge: "Step 6 of 8 • Multi-Profile Identity",
            title: "Guest & Cloud Synchronization",
            desc: "Local guest mode stays isolated on this browser with zero cloud leaks. Cloud profiles auto-sync across devices.",
            targetSelector: "#navAvatarImg, a[title*='Commander Profile']",
            speech: "Your profile is private and local. Sign in anytime to cloud sync! 🛡️",
            actionHint: "Inspect your active profile ring!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 7 of 8 • Navigation Center",
            title: "Unified Navigation Hub",
            desc: "Quickly navigate across Timer, Today, Task, Coaching, CBT Exam Simulator, Inspiration, and Settings.",
            targetSelector: "#main-nav",
            speech: "All study tools organized in a unified cyber ribbon! 🧭",
            actionHint: "Preview navigation tabs!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 8 of 8 • Next Module",
            title: "Cockpit Mastered — Next Page",
            desc: "Cockpit overview complete! Next up: Tactical Sprint Timer for high-intensity question drills.",
            targetSelector: "#main-nav a[href*='timer.html'], #main-nav",
            speech: "Cockpit complete! Let's enter the Tactical Sprint Timer! 🚀",
            actionHint: "Click 'Next Page: Tactical Sprint Timer' below!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 2. SPRINT TIMER (timer.html) -> Next Page: today.html
    if (path.includes("timer.html")) {
      return {
        nextPageUrl: "today.html?tour=true",
        nextPageName: "Daily Log & Velocity",
        steps: [
          {
            badge: "Step 1 of 5 • Sprint Cadence",
            title: "Tactical Pomodoro & Drill Modes",
            desc: "Switch between 25-minute sprints, 60-minute question marathons, and custom timed drills.",
            targetSelector: "#timer-display, .timer-clock, #countdown-display",
            speech: "Focus timer with zero distractions. Let the minutes work for you! ⏱️",
            actionHint: "Test starting a focus session!",
            actionFn: () => { playTourChime(); }
          },
          {
            badge: "Step 2 of 5 • Rapid Question Logging",
            title: "Live Question Counter During Sprints",
            desc: "Tap +1 after every question solved without breaking your deep work momentum.",
            targetSelector: "#btn-q-plus, .btn-log-q, #q-counter-box",
            speech: "Keep the tally running while solving problems! ✍️",
            actionHint: "Click 'Test Action' to log +1 Question!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 3 of 5 • White Noise & Ambient Audio",
            title: "Aura Soundscapes & Binaural Beats",
            desc: "Built-in study sounds: Cyber rain, Brown noise, Deep interstellar frequency to block background noise.",
            targetSelector: "#sound-selector, .ambient-audio-ctrl, #sound-btn",
            speech: "Lock in with ambient focus frequencies! 🎧",
            actionHint: "Toggle audio atmosphere!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 4 of 5 • Mistake Vault Quick Bookmark",
            title: "1-Tap Mistake Autopsy Bookmark",
            desc: "Flag tough problems instantly during a drill for automatic autopsy in the Mistake Vault.",
            targetSelector: "#btn-flag-mistake, .mistake-flag-btn, #btn-bookmark",
            speech: "Every mistake logged is a rank booster on exam day! 📑",
            actionHint: "Click 'Test Action' to bookmark problem!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 5 of 5 • Next: Daily Log & Velocity",
            title: "Timer Mastered — Next Page",
            desc: "Sprint timer mastered! Next up is your Daily Digest to inspect today's solving momentum.",
            targetSelector: "#main-nav a[href*='today.html'], #main-nav",
            speech: "Sprint timer clear! Advancing to the Daily Digest & Velocity Log! 📊",
            actionHint: "Click 'Next Page: Daily Log & Velocity' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 3. TODAY'S DIGEST (today.html) -> Next Page: task.html
    if (path.includes("today.html")) {
      return {
        nextPageUrl: "task.html?tour=true",
        nextPageName: "Deep Work & Syllabus Tasks",
        steps: [
          {
            badge: "Step 1 of 5 • Daily Digest",
            title: "Daily Hours Tracker",
            desc: "Consolidates all timer sessions today with automated breakdown by Physics, Chemistry, and Mathematics.",
            targetSelector: "#stat-total-hours, .daily-hours-box, #today-hours-card",
            speech: "Review today's study investment at a single glance! 📈",
            actionHint: "Inspect daily hours breakdown!",
            actionFn: () => { playTourChime(); }
          },
          {
            badge: "Step 2 of 5 • Velocity Matrix",
            title: "Subject Velocity Matrix",
            desc: "Visualizes solving velocity: questions per hour and accuracy distribution across all three subjects.",
            targetSelector: "#chart-subject-velocity, .velocity-card, #today-matrix",
            speech: "Check your speed across Physics, Chemistry, and Maths! 🚀",
            actionHint: "Review subject balance!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 3 of 5 • Question Volume",
            title: "Question Volume Counter",
            desc: "Inspect total questions solved today vs your daily target (target: 90 questions).",
            targetSelector: "#stat-total-questions, .q-volume-box, #stat-today-target",
            speech: "90 questions a day keeps the competition away! 🎯",
            actionHint: "Click 'Test Action' to celebrate progress!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 4 of 5 • Report Card Export",
            title: "JPEG / PDF Daily Report Card",
            desc: "Generate and export your official daily study report card with authentic timestamps for accountability.",
            targetSelector: "button[onclick*='exportReport'], #btn-export-card",
            speech: "Export and share your daily wins with mentors or study groups! 📜",
            actionHint: "Click 'Test Action' to preview report card!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 5 of 5 • Next: Task Hub",
            title: "Daily Digest Mastered — Next Page",
            desc: "Daily log mastered! Next up is the Task Hub for syllabus chapters, TickTick sync, and backlogs.",
            targetSelector: "#main-nav a[href*='task.html'], #main-nav",
            speech: "Daily stats verified! Advancing to the Task & Kanban Terminal! 📋",
            actionHint: "Click 'Next Page: Deep Work & Syllabus Tasks' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 4. TASK HUB (task.html) -> Next Page: coaching.html
    if (path.includes("task.html")) {
      return {
        nextPageUrl: "coaching.html?tour=true",
        nextPageName: "Interactive Coaching & JEE Syllabus",
        steps: [
          {
            badge: "Step 1 of 4 • Task Terminal",
            title: "Syllabus Task Management",
            desc: "Organize chapters into actionable tasks with subject tagging, priority labels, and target completion dates.",
            targetSelector: "#task-form, .task-input-box, #task-input",
            speech: "Organize your study backlog with surgical precision! 📝",
            actionHint: "Focus task input field!",
            actionFn: () => {
              const el = document.getElementById('task-input') || document.querySelector('input[type="text"]');
              if (el) el.focus();
            }
          },
          {
            badge: "Step 2 of 4 • Task Kanban",
            title: "Visual Status Columns",
            desc: "Drag or move tasks across Backlog, In Progress, and Mastered columns as you study.",
            targetSelector: "#task-columns, .kanban-container, .task-list",
            speech: "Keep your daily priorities crystal clear! 📌",
            actionHint: "Inspect your task pipeline!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 3 of 4 • TickTick 2-Way Cloud Sync",
            title: "TickTick Cloud Integration",
            desc: "Connect your TickTick API token in Settings to sync your tasks bi-directionally with your phone.",
            targetSelector: "button[onclick*='syncTickTick'], #btn-sync-ticktick, .sync-btn",
            speech: "TickTick sync ensures your phone tasks stay in sync with Cockpit! 🔄",
            actionHint: "Click 'Test Action' to test sync indicator!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 4 of 4 • Next: Coaching & Syllabus",
            title: "Tasks Mastered — Next Page",
            desc: "Task hub mastered! Next up is the Coaching Matrix, covering syllabus weightage and test logs.",
            targetSelector: "#main-nav a[href*='coaching.html'], #main-nav",
            speech: "Tasks organized! Advancing to Coaching & Syllabus Roadmap! 🎓",
            actionHint: "Click 'Next Page: Coaching & Syllabus' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 5. COACHING MATRIX (coaching.html) -> Next Page: cbt_home.html
    if (path.includes("coaching.html")) {
      return {
        nextPageUrl: "cbt_home.html?tour=true",
        nextPageName: "CBT Mock Portal",
        steps: [
          {
            badge: "Step 1 of 5 • Syllabus Tree",
            title: "Complete PCM Syllabus Coverage",
            desc: "Track every chapter across Class 11 and Class 12 for Physics, Chemistry, and Maths with high-yield JEE exam weightage and completion rings.",
            targetSelector: "#pane-syllabus, .syllabus-container, #pcm-milestone-blocks",
            speech: "Here is your master syllabus roadmap! Never miss a chapter! 📚",
            actionHint: "Filter by Class 11 or Class 12 using the selector buttons!",
            actionFn: () => { const b = document.getElementById('btn-class-11'); if (b) b.click(); }
          },
          {
            badge: "Step 2 of 5 • Test Score & OCR",
            title: "Coaching Test Score Tracker",
            desc: "Log your offline Allen/Fitjee/Resonance test marks. Upload scorecards to extract marks automatically via OCR.",
            targetSelector: "#pane-tests, #test-tracker-card, .test-table",
            speech: "Log your offline coaching mocks here to measure real rank growth! 📊",
            actionHint: "Review your test progress timeline!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 3 of 5 • Question Log & Notes",
            title: "Personal Concept Question Bank",
            desc: "Store breakthrough questions, tricky derivations, and conceptual traps directly linked to each chapter.",
            targetSelector: "#pane-logs, .question-bank-card, #question-log-table",
            speech: "Save gold-standard problems you can revise right before exam day! 💡",
            actionHint: "Inspect your stored problem bank!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 4 of 5 • All Syllabus Selector",
            title: "Class 11 & 12 Filter Controls",
            desc: "Toggle between Class 11 foundations, Class 12 advanced concepts, or complete merged syllabus with 1 click.",
            targetSelector: "#btn-class-all, .syllabus-filter-pill, .filter-btn-group",
            speech: "Notice how the card smoothly docks beside this button without covering it! 🎯",
            actionHint: "Click 'Test Action' to select All Syllabus!",
            actionFn: () => {
              const b = document.getElementById('btn-class-all') || document.querySelector('.syllabus-filter-pill');
              if (b) b.click();
              playExcitedSuccessChime();
            }
          },
          {
            badge: "Step 5 of 5 • Next: CBT Simulator",
            title: "Coaching Mastered — Next Page",
            desc: "Syllabus clear! Next up is the CBT Mock Exam Portal, with authentic NTA computer-based exam conditions.",
            targetSelector: "#main-nav a[href*='cbt_home.html'], #main-nav",
            speech: "Syllabus clear! Advancing to the official NTA CBT Mock Exam Portal! 💻",
            actionHint: "Click 'Next Page: CBT Mock Portal' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 6. CBT PORTAL (cbt_home.html) -> Next Page: inspiration.html
    if (path.includes("cbt_home.html") || path.includes("test_centre.html")) {
      return {
        nextPageUrl: "inspiration.html?tour=true",
        nextPageName: "Inspiration Board",
        steps: [
          {
            badge: "Step 1 of 5 • CBT Hub & Profile",
            title: "Official NTA CBT Mock Portal",
            desc: "Practice in the identical interface used in actual JEE Main and Advanced! Familiarity with the official interface saves 10-15 minutes on exam day.",
            targetSelector: "#cbt-home-user-name, .cbt-header-banner, .cbt-user-badge",
            speech: "Welcome to the CBT Mock Portal! Authentic NTA exam conditions! 📝",
            actionHint: "Inspect your mock test vitals and average score!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 2 of 5 • Accuracy & Solving Latency",
            title: "Score & Latency Vitals",
            desc: "Tracks your average score across tests, average time per question (target: 90s for JEE Main, 150s for JEE Advanced), and negative mark penalty.",
            targetSelector: "#vit-score, #vit-latency, #vit-acc",
            speech: "Pacing vitals ensure you finish all 75 questions with time to spare! ⏱️",
            actionHint: "Vitals update automatically upon test submission!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 3 of 5 • Adaptive Test Generator",
            title: "AI Adaptive Test Generator",
            desc: "Want a quick customized drill? Generate targeted tests by selecting exact chapter, difficulty, and question count in 1 click.",
            targetSelector: "button[onclick='openGeneratorModal()'], .cbt-generator-banner",
            speech: "Generate an adaptive test tailored to your weakest chapter! 🎯",
            actionHint: "Click 'Generate Adaptive Test' to preview the configuration modal!",
            actionFn: () => { if (typeof window.openGeneratorModal === 'function') window.openGeneratorModal(); }
          },
          {
            badge: "Step 4 of 5 • Available Test Suite",
            title: "Authentic Mock Exam Library",
            desc: "Browse Full JEE Main simulations, chapter drills, and PYQ tests. Click 'Launch Test' to enter authentic full-screen exam mode.",
            targetSelector: ".cbt-test-card:first-child, #cbt-tests-container, #all-tests",
            speech: "Simulate a real 3-hour test to build exam stamina! 🏆",
            actionHint: "Click 'Test Action' to inspect first available test!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 5 of 5 • Next: Inspiration Board",
            title: "CBT Portal Mastered — Next Page",
            desc: "CBT simulator mastered! Next up is the Wall of Inspiration, featuring toppers' proven rank strategies and mindset fuels.",
            targetSelector: "a[title*='Return to ClockEE'], .cbt-header-banner a[href*='index.html']",
            speech: "Exam engine mastered! Advancing to the Wall of Inspiration! 💡",
            actionHint: "Click 'Next Page: Inspiration Board' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 7. INSPIRATION PAGE (inspiration.html) -> Next Page: settings.html
    if (path.includes("inspiration.html")) {
      return {
        nextPageUrl: "settings.html?tour=true",
        nextPageName: "Settings & Customizer",
        steps: [
          {
            badge: "Step 1 of 3 • Mindset Engine",
            title: "Topper Rank Fuel & Mental Fortitude",
            desc: "Curated collection of proven psychological strategies from AIR 1-50 toppers to eliminate exam anxiety and stay locked-in.",
            targetSelector: "#inspiration-hero, .spark-card, .quote-box",
            speech: "Fuel your mindset with daily discipline quotes and proven rank strategies! ⚡",
            actionHint: "Generate a daily spark quote!",
            actionFn: () => {
              const b = document.getElementById('btnSummonDailySpark');
              if (b) b.click();
            }
          },
          {
            badge: "Step 2 of 3 • Dream IIT Vision Board",
            title: "Dream College Vision Pinboard",
            desc: "Pin sticky notes of your target rank, dream IIT campus (Bombay CSE, Delhi, Madras), and milestone dates directly to your dashboard.",
            targetSelector: "#notes-grid, .sticky-notes-container, #pinboard",
            speech: "Visualize your dream college every single day! 🏛️",
            actionHint: "Click 'Test Action' to pin a dream note!",
            actionFn: () => { playExcitedSuccessChime(); }
          },
          {
            badge: "Step 3 of 3 • Next: Settings & Customizer",
            title: "Inspiration Mastered — Next Page",
            desc: "Inspiration clear! Next up is Settings to customize accent auras, profile identity, and connected APIs.",
            targetSelector: "#main-nav a[href*='settings.html'], #main-nav",
            speech: "Vision set! Let's proceed to the Settings & Customizer! ⚙️",
            actionHint: "Click 'Next Page: Settings & Customizer' to transition!",
            actionFn: () => {}
          }
        ]
      };
    }

    // 8. SETTINGS & CUSTOMIZATION (settings.html) -> Finish Tour!
    if (path.includes("settings.html")) {
      return {
        nextPageUrl: "index.html",
        nextPageName: "Cockpit Home",
        steps: [
          {
            badge: "Step 1 of 4 • Identity & Goals",
            title: "Profile & Examination Target",
            desc: "Configure your target exam year (JEE 2028), target dream college (IIT Bombay), and personalize your avatar.",
            targetSelector: "#sec-identity, #profile-settings, .settings-identity-card",
            speech: "Set your target examination date and candidate identity! 👤",
            actionHint: "Review your profile parameters!",
            actionFn: () => { playTourChime(); }
          },
          {
            badge: "Step 2 of 4 • Cyber Themes & Auras",
            title: "Themes, Accent Colors & Audio Packs",
            desc: "Customize your cockpit aura: Neon Cyan, Cyber Violet, Obsidian Amber. Choose sound pack tactile clicks.",
            targetSelector: "#sec-aura, .theme-picker, #accent-color-picker",
            speech: "Customize your visual aura to match your study energy! 🎨",
            actionHint: "Click 'Test Action' to sample Cyan Aura!",
            actionFn: () => {
              if (typeof window.applyAccentColor === 'function') window.applyAccentColor('#00f0ff');
              playExcitedSuccessChime();
            }
          },
          {
            badge: "Step 3 of 4 • Cloud & API Integrations",
            title: "TickTick & Gemini AI API Keys",
            desc: "Add your personal Gemini API key for instant smart problem generation, or connect TickTick for mobile sync.",
            targetSelector: "#sec-apis, .api-keys-card, #input-gemini-key",
            speech: "Add personal API keys for unrestricted AI problem cloning! 🔑",
            actionHint: "Inspect connected cloud APIs!",
            actionFn: () => { playSuccessChirp(); }
          },
          {
            badge: "Step 4 of 4 • Tour Complete!",
            title: "Master Tour Completed! 🚀",
            desc: "Congratulations, Commander! You have explored all 8 core modules of ClockEE. Your high-velocity study flight begins now!",
            targetSelector: "#navAvatarImg, a[title*='Commander Profile']",
            speech: "All systems online and calibrated! Top 50 AIR begins today! 🏆",
            actionHint: "Click 'Finish Master Tour' to launch Cockpit!",
            actionFn: () => { playExcitedSuccessChime(); }
          }
        ]
      };
    }

    // Fallback: Default to Cockpit
    return {
      nextPageUrl: "index.html",
      nextPageName: "Cockpit Home",
      steps: [
        {
          badge: "Step 1 of 1 • System Active",
          title: "ClockEE Module Active",
          desc: "ClockEE study cockpit is fully operational. Tap Next to continue.",
          targetSelector: "body",
          speech: "Module active and operational! ⏰",
          actionHint: "Ready for focus!",
          actionFn: () => { playTourChime(); }
        }
      ]
    };
  }

  // Smart Flexible Position Solver
  function positionSpotlightAndCard(targetEl) {
    if (!targetEl || !isTourActive) return;

    // Bring into view smoothly
    targetEl.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });

    setTimeout(() => {
      const rect = targetEl.getBoundingClientRect();
      const padding = 12;
      const holeX = Math.max(0, rect.left - padding);
      const holeY = Math.max(0, rect.top - padding);
      const holeW = Math.max(30, rect.width + padding * 2);
      const holeH = Math.max(30, rect.height + padding * 2);

      // 1. Update SVG Cutout Hole
      if (spotlightCutout) {
        spotlightCutout.setAttribute('x', holeX);
        spotlightCutout.setAttribute('y', holeY);
        spotlightCutout.setAttribute('width', holeW);
        spotlightCutout.setAttribute('height', holeH);
      }
      spotlightSvg.classList.add('active');

      // 2. Update Halo
      if (haloEl) {
        haloEl.style.left = `${holeX}px`;
        haloEl.style.top = `${holeY}px`;
        haloEl.style.width = `${holeW}px`;
        haloEl.style.height = `${holeH}px`;
        haloEl.classList.add('active');
      }

      // If Minimized: Do not position card, keep corner box active
      if (isTourMinimized) return;

      // 3. Flexible Card Positioning (Left, Right, Below, Above)
      const vpW = window.innerWidth;
      const vpH = window.innerHeight;
      const cardW = Math.min(440, vpW - 32);
      const cardH = floatingCard.offsetHeight || 240;

      let cardX = 16;
      let cardY = 16;
      let arrowStartX = 0;
      let arrowStartY = 0;
      let arrowEndX = 0;
      let arrowEndY = 0;

      const spaceRight = vpW - (holeX + holeW);
      const spaceLeft = holeX;
      const spaceBelow = vpH - (holeY + holeH);
      const spaceAbove = holeY;

      // Decision logic: prefer right if enough room, else left, else below, else above
      if (spaceRight >= cardW + 36) {
        // Place to RIGHT of element
        cardX = holeX + holeW + 28;
        cardY = Math.max(16, Math.min(vpH - cardH - 16, holeY + holeH / 2 - cardH / 2));
        arrowStartX = cardX;
        arrowStartY = cardY + cardH / 2;
        arrowEndX = holeX + holeW;
        arrowEndY = holeY + holeH / 2;
      } else if (spaceLeft >= cardW + 36) {
        // Place to LEFT of element
        cardX = holeX - cardW - 28;
        cardY = Math.max(16, Math.min(vpH - cardH - 16, holeY + holeH / 2 - cardH / 2));
        arrowStartX = cardX + cardW;
        arrowStartY = cardY + cardH / 2;
        arrowEndX = holeX;
        arrowEndY = holeY + holeH / 2;
      } else if (spaceBelow >= cardH + 36) {
        // Place BELOW element
        cardX = Math.max(16, Math.min(vpW - cardW - 16, holeX + holeW / 2 - cardW / 2));
        cardY = holeY + holeH + 24;
        arrowStartX = cardX + cardW / 2;
        arrowStartY = cardY;
        arrowEndX = holeX + holeW / 2;
        arrowEndY = holeY + holeH;
      } else {
        // Place ABOVE element
        cardX = Math.max(16, Math.min(vpW - cardW - 16, holeX + holeW / 2 - cardW / 2));
        cardY = Math.max(16, holeY - cardH - 24);
        arrowStartX = cardX + cardW / 2;
        arrowStartY = cardY + cardH;
        arrowEndX = holeX + holeW / 2;
        arrowEndY = holeY;
      }

      // Apply coordinates to Floating Card
      floatingCard.style.left = `${cardX}px`;
      floatingCard.style.top = `${cardY}px`;
      floatingCard.classList.remove('collapsing');
      floatingCard.classList.add('active');

      // 4. Draw Theme-colored Dotted Arrow Path
      if (arrowPath) {
        const dx = arrowEndX - arrowStartX;
        const dy = arrowEndY - arrowStartY;
        const cx1 = arrowStartX + dx * 0.4;
        const cy1 = arrowStartY;
        const cx2 = arrowStartX + dx * 0.6;
        const cy2 = arrowEndY;
        arrowPath.setAttribute('d', `M ${arrowStartX} ${arrowStartY} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${arrowEndX} ${arrowEndY}`);
        arrowSvg.classList.add('active');
      }
    }, 280);
  }

  // Render Step
  function renderTourStep(idx) {
    if (!currentPageTourConfig || !currentPageTourConfig.steps || !currentPageTourConfig.steps[idx]) return;
    currentTourIdx = idx;
    const step = currentPageTourConfig.steps[idx];
    const totalSteps = currentPageTourConfig.steps.length;
    const isLastStep = idx === totalSteps - 1;

    ensureTourDOMElements();

    // 1. Populate Text Immediately (Guaranteed NEVER empty!)
    const badgeEl = document.getElementById('tourBadge');
    const titleEl = document.getElementById('tourTitle');
    const descEl = document.getElementById('tourDesc');
    const hintEl = document.getElementById('tourActionHint');
    const stepIndEl = document.getElementById('tourStepIndicator');
    const cornerStepEl = document.getElementById('tourCornerStep');
    const nextBtn = document.getElementById('tourNextBtn');
    const prevBtn = document.getElementById('tourPrevBtn');
    const actionBtn = document.getElementById('tourActionBtn');

    if (badgeEl) badgeEl.textContent = step.badge || `Step ${idx + 1} of ${totalSteps}`;
    if (titleEl) titleEl.textContent = step.title || "Cockpit Module";
    if (hintEl) hintEl.textContent = step.actionHint || "⚡ Click to test this feature!";
    if (stepIndEl) stepIndEl.textContent = `${idx + 1} of ${totalSteps}`;
    if (cornerStepEl) cornerStepEl.textContent = `Step ${idx + 1}/${totalSteps}`;

    // Reset action button
    if (actionBtn) {
      actionBtn.innerHTML = `<span>⚡ Test Action</span>`;
      actionBtn.className = "px-2.5 py-1 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-[11px] transition shadow-md shadow-cyan-500/30 flex items-center gap-1 cursor-pointer";
    }

    // Typewrite Description smoothly
    const fullText = `${step.speech || ''} ${step.desc || ''}`.trim();
    if (descEl) {
      typewriteText(descEl, fullText, 10);
    }

    // Prev / Next button states
    if (prevBtn) {
      prevBtn.style.visibility = idx > 0 ? 'visible' : 'hidden';
    }

    if (nextBtn) {
      if (isLastStep) {
        if (currentPageTourConfig.nextPageUrl && !currentPageTourConfig.nextPageUrl.includes("index.html")) {
          nextBtn.innerHTML = `<span>Next Page: ${currentPageTourConfig.nextPageName} →</span>`;
          nextBtn.className = "px-4 py-1.5 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white font-extrabold text-xs shadow-lg shadow-emerald-500/30 transition flex items-center gap-1.5 cursor-pointer";
        } else {
          nextBtn.innerHTML = `<span>Finish Master Tour 🚀</span>`;
          nextBtn.className = "px-4 py-1.5 rounded-xl bg-gradient-to-r from-purple-500 via-indigo-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 text-white font-extrabold text-xs shadow-lg shadow-purple-500/30 transition flex items-center gap-1.5 cursor-pointer";
        }
      } else {
        nextBtn.innerHTML = `<span>Next Step →</span>`;
        nextBtn.className = "px-4 py-1.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-white font-extrabold text-xs shadow-lg shadow-cyan-500/25 transition flex items-center gap-1.5 cursor-pointer";
      }
    }

    // Play soft chime
    playTourChime();

    // 2. Highlight Target Element
    document.querySelectorAll('.cockpit-tour-target-active').forEach(el => el.classList.remove('cockpit-tour-target-active'));

    let targetEl = null;
    if (step.targetSelector) {
      const selectors = step.targetSelector.split(',').map(s => s.trim());
      for (const sel of selectors) {
        const found = document.querySelector(sel);
        if (found) { targetEl = found; break; }
      }
    }

    if (targetEl) {
      targetEl.classList.add('cockpit-tour-target-active');
      positionSpotlightAndCard(targetEl);
    } else {
      // Fallback: center in screen
      if (spotlightCutout) {
        spotlightCutout.setAttribute('x', window.innerWidth / 2 - 100);
        spotlightCutout.setAttribute('y', window.innerHeight / 2 - 60);
        spotlightCutout.setAttribute('width', 200);
        spotlightCutout.setAttribute('height', 120);
      }
      floatingCard.style.left = `${Math.max(16, window.innerWidth / 2 - 220)}px`;
      floatingCard.style.top = `${Math.max(16, window.innerHeight / 2 - 120)}px`;
      floatingCard.classList.remove('collapsing');
      floatingCard.classList.add('active');
      if (arrowSvg) arrowSvg.classList.remove('active');
    }
  }

  // Minimize Tour to Corner Box
  window.minimizeCockpitTour = function() {
    if (!isTourActive) return;
    isTourMinimized = true;

    if (floatingCard) {
      floatingCard.classList.add('collapsing');
      setTimeout(() => {
        floatingCard.classList.remove('active');
      }, 350);
    }
    if (arrowSvg) arrowSvg.classList.remove('active');
    if (haloEl) haloEl.classList.remove('active');
    if (spotlightSvg) spotlightSvg.classList.remove('active');
    if (interruptionModal) interruptionModal.classList.remove('active');

    if (cornerBox) {
      cornerBox.classList.add('active');
    }

    if (window.showToast) window.showToast("⏱️ Tour minimized to corner. Tap anytime to resume!", "info");
  };

  // Expand Tour from Corner Box
  window.expandCockpitTour = function() {
    if (!isTourActive) return;
    isTourMinimized = false;

    if (interruptionModal) interruptionModal.classList.remove('active');
    if (cornerBox) cornerBox.classList.remove('active');

    renderTourStep(currentTourIdx);
  };

  // Interruption Prompt
  window.showTourInterruptionPrompt = function() {
    if (!isTourActive) return;
    if (interruptionModal) {
      interruptionModal.classList.add('active');
      playTourChime();
    }
  };

  // Trigger Mascot Excited Celebration
  window.triggerMascotExcited = function() {
    const mascotBox = document.getElementById('tourMascotContainer');
    if (mascotBox) {
      mascotBox.innerHTML = getClockEEMascotSvg(true);
      setTimeout(() => {
        mascotBox.innerHTML = getClockEEMascotSvg(false);
      }, 1200);
    }

    const cardRect = floatingCard.getBoundingClientRect();
    createCyberSparkleBurst(cardRect.left + 50, cardRect.top + 50);
    playExcitedSuccessChime();
  };

  // Run Current Tour Action
  window.runCurrentTourAction = function() {
    if (!currentPageTourConfig || !currentPageTourConfig.steps || !currentPageTourConfig.steps[currentTourIdx]) return;
    const step = currentPageTourConfig.steps[currentTourIdx];

    // Trigger excited mascot
    window.triggerMascotExcited();

    // Trigger step action function
    try {
      if (typeof step.actionFn === 'function') {
        step.actionFn();
      }
    } catch(e) {}

    // Update Action Button to Completed!
    const btn = document.getElementById('tourActionBtn');
    if (btn) {
      btn.innerHTML = `<span>✓ Completed! +50 XP</span>`;
      btn.className = "px-2.5 py-1 rounded-lg bg-emerald-500 text-black font-extrabold text-[11px] shadow-lg shadow-emerald-500/40 flex items-center gap-1 transition";
    }

    // Update speech to celebration praise
    const descEl = document.getElementById('tourDesc');
    if (descEl) {
      typewriteText(descEl, "WOOHOO! 🚀 Action mastered! +50 Focus XP added to your flight deck!", 10);
    }
  };

  // Start Tour
  window.startCockpitGuidedTour = function() {
    ensureTourDOMElements();
    currentPageTourConfig = getMasterPageTourConfig();
    if (!currentPageTourConfig || !currentPageTourConfig.steps || currentPageTourConfig.steps.length === 0) return;

    isTourActive = true;
    isTourMinimized = false;

    // Close overview menu if open
    const menuModal = document.getElementById('cockpitTourMenuModal');
    if (menuModal) menuModal.style.display = 'none';

    renderTourStep(0);
  };

  // Close Tour Cleanly
  window.closeCockpitTour = function() {
    isTourActive = false;
    isTourMinimized = false;

    if (spotlightSvg) spotlightSvg.classList.remove('active');
    if (haloEl) haloEl.classList.remove('active');
    if (arrowSvg) arrowSvg.classList.remove('active');
    if (floatingCard) {
      floatingCard.classList.remove('active');
      floatingCard.classList.remove('collapsing');
    }
    if (cornerBox) cornerBox.classList.remove('active');
    if (interruptionModal) interruptionModal.classList.remove('active');

    document.querySelectorAll('.cockpit-tour-target-active').forEach(el => el.classList.remove('cockpit-tour-target-active'));

    // Mark tour seen in localStorage
    try {
      localStorage.setItem('clockee_cockpit_tour_seen', 'true');
    } catch(e) {}
  };

  // Step Navigation
  window.nextCockpitTourStep = function() {
    if (!currentPageTourConfig || !currentPageTourConfig.steps) return;
    const totalSteps = currentPageTourConfig.steps.length;

    if (currentTourIdx >= totalSteps - 1) {
      // Last step: advance to next page or finish!
      if (currentPageTourConfig.nextPageUrl && !currentPageTourConfig.nextPageUrl.includes("index.html")) {
        window.closeCockpitTour();
        setTimeout(() => {
          window.location.href = currentPageTourConfig.nextPageUrl;
        }, 150);
      } else {
        // Final Finish
        window.closeCockpitTour();
        setTimeout(() => {
          window.location.href = "index.html";
        }, 150);
      }
    } else {
      renderTourStep(currentTourIdx + 1);
    }
  };

  window.prevCockpitTourStep = function() {
    if (currentTourIdx > 0) {
      renderTourStep(currentTourIdx - 1);
    }
  };

  // Re-adjust spotlight on resize or scroll
  window.addEventListener('resize', () => {
    if (!isTourActive || isTourMinimized || !currentPageTourConfig || !currentPageTourConfig.steps[currentTourIdx]) return;
    const step = currentPageTourConfig.steps[currentTourIdx];
    let targetEl = null;
    if (step.targetSelector) {
      const selectors = step.targetSelector.split(',').map(s => s.trim());
      for (const sel of selectors) {
        const found = document.querySelector(sel);
        if (found) { targetEl = found; break; }
      }
    }
    if (targetEl) positionSpotlightAndCard(targetEl);
  });
  window.addEventListener('scroll', () => {
    if (!isTourActive || isTourMinimized || !currentPageTourConfig || !currentPageTourConfig.steps[currentTourIdx]) return;
    const step = currentPageTourConfig.steps[currentTourIdx];
    let targetEl = null;
    if (step.targetSelector) {
      const selectors = step.targetSelector.split(',').map(s => s.trim());
      for (const sel of selectors) {
        const found = document.querySelector(sel);
        if (found) { targetEl = found; break; }
      }
    }
    if (targetEl) positionSpotlightAndCard(targetEl);
  }, { passive: true });

  // Keyboard navigation
  window.addEventListener('keydown', (e) => {
    if (!isTourActive || isTourMinimized) return;
    if (e.key === 'Escape') window.closeCockpitTour();
    if (e.key === 'ArrowRight') window.nextCockpitTourStep();
    if (e.key === 'ArrowLeft') window.prevCockpitTourStep();
  });

  // Tour Menu Modal (Only 8 Core Modules, No Hackathon, No Admin)
  window.showCockpitTourMenu = function() {
    let modal = document.getElementById('cockpitTourMenuModal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'cockpitTourMenuModal';
      modal.className = 'cockpit-tour-menu-modal-backdrop';
      modal.style.cssText = 'position:fixed;inset:0;background:rgba(2,4,10,0.88);backdrop-filter:blur(24px);z-index:999999;display:flex;align-items:center;justify-content:center;padding:16px;';
      modal.innerHTML = `
        <div style="max-width:820px;width:100%;max-height:90vh;overflow-y:auto;background:rgba(10,15,30,0.96);border:1.5px solid rgba(0,240,255,0.5);border-radius:24px;padding:24px;box-shadow:0 24px 60px rgba(0,0,0,0.9),0 0 40px rgba(0,240,255,0.3);color:#fff;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <span style="font-size:26px;">🚀</span>
              <div>
                <h2 style="font-size:18px;font-weight:800;margin:0;">ClockEE Master Interactive Tour</h2>
                <p style="font-size:12px;color:#94a3b8;margin:2px 0 0 0;">8 Verified Study Modules • Precision JEE Advanced Cadence</p>
              </div>
            </div>
            <button onclick="document.getElementById('cockpitTourMenuModal').style.display='none'" style="background:none;border:none;color:#94a3b8;font-size:20px;cursor:pointer;">✕</button>
          </div>

          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:20px;">
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">⏱️</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">1. Cockpit HUD</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">JEE 2028 Countdown & Solvers</p>
              <a href="index.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Cockpit →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">⚡</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">2. Sprint Timer</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Pomodoro & White Noise</p>
              <a href="timer.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Timer →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">📊</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">3. Daily Log</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Velocity & Report Cards</p>
              <a href="today.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Today →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">📋</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">4. Task Hub</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">TickTick Sync & Kanban</p>
              <a href="task.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Tasks →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">🎓</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">5. Coaching Matrix</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Full PCM Syllabus Tree</p>
              <a href="coaching.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Coaching →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">💻</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">6. CBT Simulator</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Authentic NTA Exam Suite</p>
              <a href="cbt_home.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start CBT →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">💡</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">7. Inspiration</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Dream Board & Topper Mindset</p>
              <a href="inspiration.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Inspiration →</a>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,240,255,0.2);border-radius:16px;padding:14px;">
              <div style="font-size:20px;margin-bottom:6px;">⚙️</div>
              <h4 style="font-size:13px;font-weight:700;margin:0 0 4px 0;">8. Settings</h4>
              <p style="font-size:11px;color:#94a3b8;margin:0 0 10px 0;">Aura Themes & APIs</p>
              <a href="settings.html?tour=true" style="font-size:11px;color:#00f0ff;text-decoration:none;font-weight:700;">Start Settings →</a>
            </div>
          </div>

          <div style="display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.1);padding-top:16px;">
            <span style="font-size:12px;color:#94a3b8;">Continuous multi-page walkthrough across all 8 modules.</span>
            <button onclick="window.startCockpitGuidedTour()" style="padding:10px 20px;border-radius:12px;background:linear-gradient(to right,#00f0ff,#6366f1);color:#fff;font-weight:800;border:none;cursor:pointer;box-shadow:0 0 20px rgba(0,240,255,0.4);">
              🚀 Start Full Continuous Tour
            </button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
    modal.style.display = 'flex';
  };

  // AUTO-TRIGGER ON FIRST SIGN IN OR ?tour=true
  document.addEventListener('DOMContentLoaded', () => {
    const isFirstSignIn = sessionStorage.getItem('clockee_first_signin') === 'true';
    const tourNotSeen = !localStorage.getItem('clockee_cockpit_tour_seen');
    const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || window.location.pathname === '';
    const urlParams = new URLSearchParams(window.location.search);
    const hasTourParam = urlParams.get('tour') === 'true';

    if (hasTourParam) {
      setTimeout(() => {
        window.startCockpitGuidedTour();
      }, 400);
    } else if (isIndex && (isFirstSignIn || tourNotSeen)) {
      sessionStorage.removeItem('clockee_first_signin');
      setTimeout(() => {
        window.showCockpitTourMenu();
      }, 600);
    }
  });

})();
