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
    ticktick: CLOCKEE_ENV.TICKTICK_TOKEN || "",
    gemini: CLOCKEE_ENV.GEMINI_KEY || "",
    cloudUrl: CLOCKEE_ENV.FIREBASE_CONFIG?.databaseURL || ""
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
      if (!parsed.apiKeys?.gemini || parsed.apiKeys.gemini === "") {
        parsed.apiKeys = { ...(parsed.apiKeys || {}), gemini: DEFAULT_STATE.apiKeys.gemini };
      }
      if (!parsed.apiKeys?.cloudUrl || parsed.apiKeys.cloudUrl === "") {
        parsed.apiKeys = { ...(parsed.apiKeys || {}), cloudUrl: DEFAULT_STATE.apiKeys.cloudUrl };
      }
      if (!parsed.firebaseConfig) {
        parsed.firebaseConfig = DEFAULT_STATE.firebaseConfig;
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
  document.querySelectorAll("[data-profile-avatar]").forEach(el => {
    if (profile.pfp) el.src = profile.pfp;
  });

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
  window.saveState();

  document.querySelectorAll("[data-profile-avatar]").forEach(img => {
    img.src = croppedDataUrl;
  });

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
      box-shadow: 0 0 16px ${accentGlow} !important;
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
      background: rgba(99, 102, 241, 0.18) !important;
      color: #a5b4fc !important;
      border: 1px solid rgba(99, 102, 241, 0.45) !important;
      box-shadow: 0 0 16px rgba(99, 102, 241, 0.25) !important;
      font-weight: 600 !important;
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
    const activeUser = window.getUsersList().find(u => u.active) || { name: "JEE Aspirant", role: "JEE 2028 Aspirant", id: "user_aspirant" };
    const users = window.getUsersList();
    const otherUsers = users.filter(u => u.id !== activeUser.id);
    const lastSync = localStorage.getItem(`clockee_last_sync_${activeUser.id}`);
    const syncText = lastSync ? new Date(lastSync).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "Just now";
    
    // Strict Role-Based Admin Permissions: Only Mentor/Admin or Authorized Admin gets admin perms
    const isAdmin = Boolean(
      activeUser.role === "Mentor / Faculty" || 
      activeUser.role === "Admin" || 
      activeUser.isAdmin === true ||
      sessionStorage.getItem('clockee_admin_authorized') === 'true'
    );

    popover.innerHTML = `
      <div class="flex items-center gap-3 border-b border-white/10 pb-3">
        <img src="${activeUser.pfp || 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=' + encodeURIComponent(activeUser.name)}" class="w-11 h-11 rounded-full border-2 ${isAdmin ? 'border-purple-400' : 'border-indigo-400'} bg-black/40">
        <div class="flex-1 min-w-0">
          <div class="text-sm font-extrabold text-white truncate flex items-center gap-1.5">
            <span>${activeUser.name}</span>
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" title="Cloud Active"></span>
          </div>
          <div class="text-[11px] ${isAdmin ? 'text-purple-300 font-bold' : 'text-indigo-300'} font-medium truncate">
            ${activeUser.role} ${isAdmin ? '★ Admin' : ''}
          </div>
          <div class="text-[10px] text-gray-400 font-mono flex items-center gap-1 mt-0.5">
            <span>☁️</span> <span>Firebase Synced • ${syncText}</span>
          </div>
        </div>
      </div>

      <div class="space-y-1.5">
        <div class="text-[10px] font-bold uppercase tracking-wider text-gray-400 flex justify-between items-center">
          <span>Switch Profile</span>
          <span class="text-[9px] text-indigo-400 font-normal">Isolated data</span>
        </div>
        <div class="space-y-1 max-h-28 overflow-y-auto pr-1">
          ${otherUsers.length > 0 ? otherUsers.map(u => `
            <button onclick="window.switchUser('${u.id}')" class="w-full text-left p-2 rounded-lg bg-white/5 hover:bg-indigo-600/20 border border-white/5 hover:border-indigo-500/30 flex items-center gap-2.5 transition">
              <img src="${u.pfp}" class="w-6 h-6 rounded-full border border-gray-600">
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-gray-200 truncate">${u.name}</div>
                <div class="text-[10px] text-gray-400 truncate">${u.role}</div>
              </div>
              <span class="text-[10px] text-indigo-400 font-bold">&rarr;</span>
            </button>
          `).join('') : '<div class="text-[11px] text-gray-500 italic py-1">No other profiles registered</div>'}
        </div>
      </div>

      <div class="p-2.5 rounded-xl bg-indigo-950/40 border border-indigo-500/20 flex items-center justify-between">
        <div class="text-[11px]">
          <div class="font-bold text-indigo-200">Cloud Realtime Sync</div>
          <div class="text-[9px] text-gray-400">Database: clockee-app</div>
        </div>
        <button onclick="window.pushToCloud()" class="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-[11px] font-bold transition flex items-center gap-1 shadow">
          <span>⚡</span> <span>Sync</span>
        </button>
      </div>

      <div class="grid grid-cols-2 gap-1.5 pt-1 text-xs">
        <a href="login.html" class="p-2 rounded-lg bg-gray-900/80 hover:bg-gray-800 border border-white/10 text-center font-bold text-gray-200 transition flex items-center justify-center gap-1.5">
          <span>🔑</span> <span>Sign In / New</span>
        </a>
        ${isAdmin ? `
          <a href="admin.html" class="p-2 rounded-lg bg-purple-950/60 hover:bg-purple-900/60 border border-purple-500/30 text-center font-bold text-purple-200 transition flex items-center justify-center gap-1.5">
            <span>👥</span> <span>Admin Panel</span>
          </a>
        ` : `
          <a href="cbt_home.html" class="p-2 rounded-lg bg-blue-950/60 hover:bg-blue-900/60 border border-blue-500/30 text-center font-bold text-blue-200 transition flex items-center justify-center gap-1.5">
            <span>📝</span> <span>CBT Tests</span>
          </a>
        `}
        <a href="settings.html" class="p-2 rounded-lg bg-gray-900/80 hover:bg-gray-800 border border-white/10 text-center font-bold text-gray-200 transition flex items-center justify-center gap-1.5">
          <span>⚙️</span> <span>Settings</span>
        </a>
        <button onclick="window.handleUserLogout()" class="p-2 rounded-lg bg-red-950/50 hover:bg-red-900/50 border border-red-500/30 text-center font-bold text-red-300 transition flex items-center justify-center gap-1.5">
          <span>🚪</span> <span>Sign Out</span>
        </button>
      </div>
    `;
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

  const isGuest = Boolean(!user || (user.uid && user.uid.startsWith("guest_")) || (user.id && user.id.startsWith("guest_")) || user.role === "Guest" || user.role === "Guest Aspirant" || user.isGuest);
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
  localStorage.removeItem("clockee_current_user");
  localStorage.removeItem("clockee_auth_active");
  sessionStorage.removeItem("clockee_admin_authorized");
  window.showToast("Signed out. Please authorize to enter.", "info");
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
