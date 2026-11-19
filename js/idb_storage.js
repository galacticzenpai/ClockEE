/**
 * ClockEE IndexedDB Wrapper for CBT Exam Session State
 * Provides high-reliability atomic writes with fallbacks.
 */

class ClockEEIDBStorage {
  constructor(dbName = 'ClockEE_CBT_DB', storeName = 'session_snapshots') {
    this.dbName = dbName;
    this.storeName = storeName;
    this.db = null;
  }

  async open() {
    if (this.db) return this.db;
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'exam_id' });
        }
      };
      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };
      request.onerror = (event) => {
        console.error('[IDB] Failed to open storage:', event.target.error);
        reject(event.target.error);
      };
    });
  }

  async saveSnapshot(snapshot) {
    try {
      const db = await this.open();
      return new Promise((resolve, reject) => {
        const tx = db.transaction([this.storeName], 'readwrite');
        const store = tx.objectStore(this.storeName);
        const req = store.put(snapshot);
        req.onsuccess = () => resolve(true);
        req.onerror = (e) => reject(e.target.error);
      });
    } catch (err) {
      console.warn('[IDB] Fallback to localStorage:', err);
      localStorage.setItem(`clockee_snap_${snapshot.exam_id}`, JSON.stringify(snapshot));
      return true;
    }
  }

  async loadSnapshot(examId) {
    try {
      const db = await this.open();
      return new Promise((resolve) => {
        const tx = db.transaction([this.storeName], 'readonly');
        const store = tx.objectStore(this.storeName);
        const req = store.get(examId);
        req.onsuccess = () => {
          if (req.result) resolve(req.result);
          else {
            const fallback = localStorage.getItem(`clockee_snap_${examId}`);
            resolve(fallback ? JSON.parse(fallback) : null);
          }
        };
        req.onerror = () => {
          const fallback = localStorage.getItem(`clockee_snap_${examId}`);
          resolve(fallback ? JSON.parse(fallback) : null);
        };
      });
    } catch {
      const fallback = localStorage.getItem(`clockee_snap_${examId}`);
      return fallback ? JSON.parse(fallback) : null;
    }
  }

  async clearSnapshot(examId) {
    try {
      const db = await this.open();
      const tx = db.transaction([this.storeName], 'readwrite');
      tx.objectStore(this.storeName).delete(examId);
    } catch {
      // ignore
    }
    localStorage.removeItem(`clockee_snap_${examId}`);
  }
}

if (typeof window !== 'undefined') {
  window.ClockEEIDBStorage = ClockEEIDBStorage;
}
