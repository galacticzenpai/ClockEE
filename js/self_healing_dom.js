/**
 * ClockEE Self-Healing DOM Protector
 * Intercepts missing DOM nodes and safely wraps critical listeners to prevent exam crashes.
 */

class SelfHealingDOM {
  constructor() {
    this.criticalSelectors = [
      '#save-next-btn',
      '#mark-review-btn',
      '#clear-btn',
      '#question-container',
      '#palette-container'
    ];
    this.observer = null;
    this.init();
  }

  init() {
    // Intercept uncaught errors to prevent exam halt
    window.addEventListener('error', (event) => {
      console.warn('[SelfHealingDOM] Unhandled runtime error suppressed:', event.message);
      // Ensure timer and inputs stay unlocked
      this.healInterface();
    });

    window.addEventListener('unhandledrejection', (event) => {
      console.warn('[SelfHealingDOM] Unhandled promise rejection suppressed:', event.reason);
    });

    this.setupMutationObserver();
  }

  setupMutationObserver() {
    if (typeof MutationObserver === 'undefined') return;
    this.observer = new MutationObserver(() => {
      this.healInterface();
    });
    this.observer.observe(document.body, { childList: true, subtree: true });
  }

  healInterface() {
    // Ensure all critical buttons have pointer events enabled
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
      if (btn.style.pointerEvents === 'none' && !btn.disabled) {
        btn.style.pointerEvents = 'auto';
      }
    });

    // Ensure scrolling isn't accidentally locked
    if (document.body.style.overflow === 'hidden' && !document.querySelector('.modal-open')) {
      document.body.style.overflow = '';
    }
  }

  safeQuery(selector, fallbackCreator = null) {
    let el = document.querySelector(selector);
    if (!el && fallbackCreator) {
      console.warn(`[SelfHealingDOM] Element '${selector}' not found. Auto-healing...`);
      el = fallbackCreator();
    }
    return el;
  }
}

if (typeof window !== 'undefined') {
  window.SelfHealingDOM = new SelfHealingDOM();
}
