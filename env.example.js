/**
 * ClockEE Runtime Environment Configuration Template
 * ------------------------------------------------------------------
 * Copy this file to `env.js` (which is strictly .gitignored)
 * to configure runtime secrets locally without exposing them to Git.
 * ------------------------------------------------------------------
 */
window.CLOCKEE_ENV = {
  // TickTick Tasks API Client Token
  TICKTICK_TOKEN: "",

  // Google Gemini API Key
  GEMINI_KEY: "",

  // Firebase Realtime DB & Modular Auth Config
  FIREBASE_CONFIG: {
    apiKey: "",
    authDomain: "clockee-app.firebaseapp.com",
    databaseURL: "https://clockee-app-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "clockee-app",
    storageBucket: "clockee-app.firebasestorage.app",
    messagingSenderId: "66153109265",
    appId: "1:66153109265:web:dde95257b9b1ae0c6c9eb0",
    measurementId: "G-BFSXRW308R"
  },

  // Supervisor Admin Unlock PIN
  ADMIN_PIN: "2028"
};
