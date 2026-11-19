/**
 * ⚡ ClockEE — Reel #6: Offline CRDT Sync Worker (js/offline_sync_worker.js)
 * Client-Side Conflict-Free Replicated Data Type (CRDT) Engine for Exam & Study State.
 */

(function(window) {
  'use strict';

  class ClockEECRDTWorker {
    constructor() {
      this.clientId = 'client_' + Math.random().toString(36).substring(2, 9);
      this.pendingDeltas = this.loadDeltas();
      this.state = this.loadState();
      this.initListeners();
    }

    loadDeltas() {
      try {
        return JSON.parse(localStorage.getItem('clockee_crdt_deltas') || '[]');
      } catch (e) {
        return [];
      }
    }

    loadState() {
      try {
        return JSON.parse(localStorage.getItem('clockee_crdt_state') || '{}');
      } catch (e) {
        return {};
      }
    }

    save() {
      try {
        localStorage.setItem('clockee_crdt_deltas', JSON.stringify(this.pendingDeltas));
        localStorage.setItem('clockee_crdt_state', JSON.stringify(this.state));
      } catch (e) {}
    }

    recordDelta(entityType, entityId, payload) {
      const delta = {
        deltaId: 'd_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
        clientId: this.clientId,
        entityType: entityType,
        entityId: entityId,
        timestamp: Date.now(),
        payload: payload
      };
      this.pendingDeltas.push(delta);
      this.applyDelta(delta);
      this.save();
      return delta;
    }

    applyDelta(delta) {
      const id = delta.entityId;
      if (!this.state[id] || delta.timestamp >= (this.state[id]._ts || 0)) {
        this.state[id] = {
          ...this.state[id],
          ...delta.payload,
          _ts: delta.timestamp,
          _clientId: delta.clientId
        };
      }
    }

    async flushToServer() {
      if (!navigator.onLine || this.pendingDeltas.length === 0) return;
      try {
        const res = await fetch('/api/sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: (JSON.parse(localStorage.getItem('clockee_current_user') || '{}')).uid,
            crdt_deltas: this.pendingDeltas
          })
        });
        if (res.ok) {
          this.pendingDeltas = [];
          this.save();
        }
      } catch (e) {
        console.warn('CRDT sync deferred until online:', e);
      }
    }

    initListeners() {
      window.addEventListener('online', () => {
        console.info('⚡ ClockEE Reconnected: Flushing offline CRDT deltas...');
        this.flushToServer();
      });
    }
  }

  window.ClockEECRDT = new ClockEECRDTWorker();

})(typeof window !== 'undefined' ? window : this);
