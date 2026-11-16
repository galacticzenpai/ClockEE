/**
 * ClockEE CBT Session Snapshot Manager
 * Debounces exam state updates to 500ms intervals and saves to IndexedDB.
 */

class SessionSnapshotManager {
  constructor(examId, studentId, onRestoreCallback = null) {
    this.examId = examId;
    this.studentId = studentId;
    this.storage = new ClockEEIDBStorage();
    this.debounceTimer = null;
    this.debounceMs = 500;
    this.onRestoreCallback = onRestoreCallback;
    this.channel = typeof BroadcastChannel !== 'undefined' ? new BroadcastChannel('clockee_cbt_sync') : null;
    this.init();
  }

  async init() {
    if (this.channel) {
      this.channel.onmessage = (event) => {
        if (event.data?.type === 'CBT_RESTORE_REQUEST' && event.data.examId === this.examId) {
          console.log('[SnapshotManager] Cross-tab sync event received');
        }
      };
    }
  }

  scheduleSync(state) {
    if (this.debounceTimer) {
      clearTimeout(this.debounceTimer);
    }
    this.debounceTimer = setTimeout(() => {
      this.persistNow(state);
    }, this.debounceMs);
  }

  async persistNow(state) {
    const payload = {
      exam_id: this.examId,
      student_id: this.studentId,
      timestamp: Date.now(),
      current_question: state.current_question || 1,
      answers: state.answers || {},
      marked_for_review: state.marked_for_review || [],
      remaining_sec: state.remaining_sec || 10800
    };
    await this.storage.saveSnapshot(payload);
    if (this.channel) {
      this.channel.postMessage({ type: 'CBT_SAVED', examId: this.examId, timestamp: payload.timestamp });
    }
    return payload;
  }

  async restore() {
    const snap = await this.storage.loadSnapshot(this.examId);
    if (snap && this.onRestoreCallback) {
      this.onRestoreCallback(snap);
    }
    return snap;
  }

  async clear() {
    await this.storage.clearSnapshot(this.examId);
  }
}

if (typeof window !== 'undefined') {
  window.SessionSnapshotManager = SessionSnapshotManager;
}
