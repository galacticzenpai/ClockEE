/**
 * ⚡ ClockEE — Reel #11: Client-Side IRT Adaptive Sequencer (js/adaptive_sequencer.js)
 * 3-Parameter Logistic (3PL) Item Response Theory Engine for In-Browser Adaptive Testing.
 */

(function(window) {
  'use strict';

  class ClientIRTEngine {
    constructor(initialTheta = 0.0) {
      this.theta = initialTheta;
      this.history = [];
      this.c = 0.25; // 4-choice guessing probability
    }

    probCorrect(theta, a, b) {
      const expTerm = Math.exp(-a * (theta - b));
      return this.c + (1.0 - this.c) / (1.0 + expTerm);
    }

    fisherInfo(theta, a, b) {
      const p = this.probCorrect(theta, a, b);
      const q = 1.0 - p;
      if (p <= this.c || q <= 0) return 0;
      const num = Math.pow(a, 2) * Math.pow(p - this.c, 2) * q;
      const denom = Math.pow(1.0 - this.c, 2) * p;
      return denom > 0 ? num / denom : 0;
    }

    recordAnswer(correct, a = 1.2, b = 0.0) {
      this.history.push({ correct, a, b });
      // Approximate Bayesian EAP update
      const delta = correct ? (1.0 - this.probCorrect(this.theta, a, b)) : (-this.probCorrect(this.theta, a, b));
      const stepSize = 0.5 / (1.0 + this.history.length * 0.1);
      this.theta = Math.max(-3.0, Math.min(3.0, Math.round((this.theta + delta * stepSize * a) * 100) / 100));
      return this.theta;
    }

    selectNext(questionPool, excludedIds = []) {
      const excluded = new Set(excludedIds);
      const available = questionPool.filter(q => !excluded.has(q.id));
      if (available.length === 0) return null;

      let bestQ = available[0];
      let maxInfo = -1;

      for (const q of available) {
        const a = q.discrimination || 1.2;
        const b = q.difficulty || 0.0;
        const info = this.fisherInfo(this.theta, a, b);
        if (info > maxInfo) {
          maxInfo = info;
          bestQ = q;
        }
      }
      return { ...bestQ, targetTheta: this.theta };
    }
  }

  window.ClockEEIRT = new ClientIRTEngine();

})(typeof window !== 'undefined' ? window : this);
