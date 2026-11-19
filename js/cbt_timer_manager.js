/**
 * ⚡ ClockEE — Reel #10: CBT Timer Manager (js/cbt_timer_manager.js)
 * Crash-resilient client-side manager controlling cbt_timer_worker.js with anchor recovery.
 */

(function(window) {
  'use strict';

  class CBTTimerManager {
    constructor() {
      this.worker = null;
      this.targetTimestamp = 0;
      this.totalDurationSeconds = 180 * 60;
      this.isRunning = false;
      this.callbacks = new Set();
      this.initWorker();
    }

    initWorker() {
      try {
        this.worker = new Worker('js/workers/cbt_timer_worker.js');
        this.worker.onmessage = (e) => this.handleWorkerMessage(e.data);
      } catch (err) {
        console.warn('⚡ Web Worker initialization failed, using high-precision fallback:', err);
        this.worker = null;
      }
    }

    start(durationSeconds = 180 * 60) {
      this.totalDurationSeconds = durationSeconds;
      const storedAnchor = localStorage.getItem('clockee_cbt_timer_anchor');
      let targetTs = storedAnchor ? parseInt(storedAnchor, 10) : 0;

      // Check if existing valid anchor in future
      if (!targetTs || targetTs <= Date.now()) {
        targetTs = Date.now() + (durationSeconds * 1000);
        localStorage.setItem('clockee_cbt_timer_anchor', targetTs.toString());
      }
      this.targetTimestamp = targetTs;
      this.isRunning = true;

      if (this.worker) {
        this.worker.postMessage({
          command: 'START',
          durationSeconds: durationSeconds,
          targetTimestamp: targetTs
        });
      } else {
        this.runFallbackLoop();
      }
    }

    handleWorkerMessage(data) {
      if (data.type === 'TICK') {
        this.broadcast(data);
      } else if (data.type === 'EXPIRED') {
        localStorage.removeItem('clockee_cbt_timer_anchor');
        this.isRunning = false;
        window.dispatchEvent(new CustomEvent('clockee:timer-expired'));
      }
    }

    runFallbackLoop() {
      if (!this.isRunning) return;
      const diffMs = this.targetTimestamp - Date.now();
      const remainingSeconds = Math.max(0, Math.ceil(diffMs / 1000));
      const elapsedSeconds = this.totalDurationSeconds - remainingSeconds;
      const progressPct = Math.min(100, Math.max(0, (elapsedSeconds / this.totalDurationSeconds) * 100));

      const tickData = {
        type: 'TICK',
        remainingSeconds: remainingSeconds,
        elapsedSeconds: elapsedSeconds,
        progressPercentage: Math.round(progressPct * 10) / 10,
        isUrgent: remainingSeconds <= (15 * 60),
        isCritical: remainingSeconds <= (5 * 60),
        formattedTime: this.formatTime(remainingSeconds)
      };

      this.broadcast(tickData);

      if (remainingSeconds <= 0) {
        this.isRunning = false;
        localStorage.removeItem('clockee_cbt_timer_anchor');
        window.dispatchEvent(new CustomEvent('clockee:timer-expired'));
      } else {
        setTimeout(() => this.runFallbackLoop(), 500);
      }
    }

    broadcast(data) {
      this.callbacks.forEach(cb => {
        try { cb(data); } catch (e) {}
      });
      window.dispatchEvent(new CustomEvent('clockee:timer-tick', { detail: data }));
    }

    onTick(callback) {
      this.callbacks.add(callback);
      return () => this.callbacks.delete(callback);
    }

    formatTime(sec) {
      const h = Math.floor(sec / 3600);
      const m = Math.floor((sec % 3600) / 60);
      const s = sec % 60;
      return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }
  }

  window.ClockEETimer = new CBTTimerManager();

})(typeof window !== 'undefined' ? window : this);
