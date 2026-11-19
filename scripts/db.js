/**
 * ClockEE OS 2.0 - Unified Offline-First IndexedDB Storage Client
 * Component: scripts/db.js
 * Author: DB / Backend Architect
 * Compliance: CLOCKEE_V2_MASTER_SPECIFICATION.md (TASK-005 / JEE-DAT-003)
 *
 * Provides:
 * - 8 Object Stores: sessions, syllabus, exams, exam_responses, mistakes, tasks, coaching_tests, settings
 * - Zero dependencies, pure Promise-based transaction layer with automatic connection management
 * - Full backward & forward compatibility with CRUD helpers: get, set/put, add, delete, getAll, queryByIndex/getByIndex, clear, count, bulkPut
 * - Specialized crash-resilient NTA CBT auto-save helpers: saveExamResponse, getExamResponses, saveExamState, getExamState
 * - Cross-environment UMD wrapper (ES module, CommonJS, and browser window.ClockEEDB & window.db)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    const exports = factory();
    const target = typeof window !== 'undefined' ? window : (typeof self !== 'undefined' ? self : root);
    target.ClockEEDB = exports;
    target.db = exports;
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const DB_NAME = 'clockee_db';
  const DB_VERSION = 2;

  const STORE_SCHEMAS = {
    sessions: {
      keyPath: 'id',
      indexes: [
        { name: 'timestamp', keyPath: 'timestamp', unique: false },
        { name: 'subject', keyPath: 'subject', unique: false },
        { name: 'chapter', keyPath: 'chapter', unique: false },
        { name: 'focusRating', keyPath: 'focusRating', unique: false }
      ]
    },
    syllabus: {
      keyPath: 'chapterId',
      indexes: [
        { name: 'subject', keyPath: 'subject', unique: false },
        { name: 'classGrade', keyPath: 'classGrade', unique: false },
        { name: 'weightage', keyPath: 'weightage', unique: false },
        { name: 'theoryStatus', keyPath: 'theoryStatus', unique: false },
        { name: 'exercisesStatus', keyPath: 'exercisesStatus', unique: false },
        { name: 'pyqStatus', keyPath: 'pyqStatus', unique: false }
      ]
    },
    exams: {
      keyPath: 'examId',
      indexes: [
        { name: 'dateAttempted', keyPath: 'dateAttempted', unique: false },
        { name: 'examType', keyPath: 'examType', unique: false },
        { name: 'status', keyPath: 'status', unique: false },
        { name: 'totalScore', keyPath: 'totalScore', unique: false }
      ]
    },
    exam_responses: {
      keyPath: 'id', // Format: `${examId}_${questionId}`
      indexes: [
        { name: 'examId', keyPath: 'examId', unique: false },
        { name: 'questionId', keyPath: 'questionId', unique: false },
        { name: 'examQuestion', keyPath: ['examId', 'questionId'], unique: true },
        { name: 'exam_question', keyPath: ['examId', 'questionId'], unique: true },
        { name: 'subject', keyPath: 'subject', unique: false },
        { name: 'section', keyPath: 'section', unique: false },
        { name: 'state', keyPath: 'state', unique: false }
      ]
    },
    mistakes: {
      keyPath: 'mistakeId',
      indexes: [
        { name: 'questionId', keyPath: 'questionId', unique: false },
        { name: 'subject', keyPath: 'subject', unique: false },
        { name: 'chapter', keyPath: 'chapter', unique: false },
        { name: 'errorCategory', keyPath: 'errorCategory', unique: false },
        { name: 'intervalTier', keyPath: 'intervalTier', unique: false },
        { name: 'nextReviewDate', keyPath: 'nextReviewDate', unique: false },
        { name: 'resolvedCount', keyPath: 'resolvedCount', unique: false }
      ]
    },
    tasks: {
      keyPath: 'taskId',
      indexes: [
        { name: 'subject', keyPath: 'subject', unique: false },
        { name: 'priority', keyPath: 'priority', unique: false },
        { name: 'status', keyPath: 'status', unique: false },
        { name: 'createdAt', keyPath: 'createdAt', unique: false },
        { name: 'completedAt', keyPath: 'completedAt', unique: false }
      ]
    },
    coaching_tests: {
      keyPath: 'testId',
      indexes: [
        { name: 'institute', keyPath: 'institute', unique: false },
        { name: 'testCode', keyPath: 'testCode', unique: false },
        { name: 'testDate', keyPath: 'testDate', unique: false },
        { name: 'percentile', keyPath: 'percentile', unique: false },
        { name: 'totalMarks', keyPath: 'totalMarks', unique: false }
      ]
    },
    settings: {
      keyPath: 'key',
      indexes: []
    }
  };

  let dbInstance = null;
  let openPromise = null;

  function openDB() {
    if (dbInstance) return Promise.resolve(dbInstance);
    if (openPromise) return openPromise;

    openPromise = new Promise((resolve, reject) => {
      const idb = typeof indexedDB !== 'undefined'
        ? indexedDB
        : (typeof window !== 'undefined' ? window.indexedDB : null);

      if (!idb) {
        return reject(new Error('IndexedDB is unavailable in this environment.'));
      }

      const request = idb.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = function (event) {
        const db = event.target.result;
        const transaction = event.target.transaction;

        for (const [storeName, schema] of Object.entries(STORE_SCHEMAS)) {
          let store;
          if (!db.objectStoreNames.contains(storeName)) {
            store = db.createObjectStore(storeName, { keyPath: schema.keyPath });
          } else {
            store = transaction.objectStore(storeName);
          }

          if (schema.indexes && schema.indexes.length > 0) {
            for (const idx of schema.indexes) {
              if (!store.indexNames.contains(idx.name)) {
                try {
                  store.createIndex(idx.name, idx.keyPath, { unique: idx.unique || false });
                } catch (e) {
                  // Ignore redundant or unsupported index collisions
                }
              }
            }
          }
        }
      };

      request.onsuccess = function (event) {
        dbInstance = event.target.result;

        dbInstance.onversionchange = function () {
          dbInstance.close();
          dbInstance = null;
          openPromise = null;
        };

        resolve(dbInstance);
      };

      request.onerror = function (event) {
        openPromise = null;
        console.error('[ClockEEDB] Connection error:', event.target.error);
        reject(event.target.error);
      };
    });

    return openPromise;
  }

  function getStore(storeName, mode = 'readonly') {
    return openDB().then((db) => {
      const transaction = db.transaction([storeName], mode);
      return transaction.objectStore(storeName);
    });
  }

  // Reactive listeners map
  const listeners = new Map();
  function emitChange(storeName, detail) {
    if (listeners.has(storeName)) {
      for (const cb of listeners.get(storeName)) {
        try {
          cb(detail);
        } catch (e) {
          console.error(e);
        }
      }
    }
  }

  const client = {
    DB_NAME,
    DB_VERSION,
    STORE_SCHEMAS,
    open: openDB,

    /**
     * Retrieve single record by primary key
     */
    async get(storeName, key) {
      const store = await getStore(storeName, 'readonly');
      return new Promise((resolve, reject) => {
        const req = store.get(key);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Store/update a record (UPSERT)
     */
    async put(storeName, value) {
      const store = await getStore(storeName, 'readwrite');
      return new Promise((resolve, reject) => {
        const req = store.put(value);
        req.onsuccess = () => {
          emitChange(storeName, { type: 'put', key: req.result, value });
          resolve(req.result);
        };
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Alias for put()
     */
    async set(storeName, value) {
      return this.put(storeName, value);
    },

    /**
     * Add a record (fails if key already exists)
     */
    async add(storeName, value) {
      const store = await getStore(storeName, 'readwrite');
      return new Promise((resolve, reject) => {
        const req = store.add(value);
        req.onsuccess = () => {
          emitChange(storeName, { type: 'add', key: req.result, value });
          resolve(req.result);
        };
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Delete a single record by primary key
     */
    async delete(storeName, key) {
      const store = await getStore(storeName, 'readwrite');
      return new Promise((resolve, reject) => {
        const req = store.delete(key);
        req.onsuccess = () => {
          emitChange(storeName, { type: 'delete', key });
          resolve(true);
        };
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Retrieve all records from a store
     */
    async getAll(storeName) {
      const store = await getStore(storeName, 'readonly');
      return new Promise((resolve, reject) => {
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Query store using a secondary index
     */
    async getByIndex(storeName, indexName, query) {
      const store = await getStore(storeName, 'readonly');
      const index = store.index(indexName);
      return new Promise((resolve, reject) => {
        const req = index.getAll(query);
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Alias for getByIndex
     */
    async queryByIndex(storeName, indexName, query) {
      return this.getByIndex(storeName, indexName, query);
    },

    /**
     * Clear all records in a store
     */
    async clear(storeName) {
      const store = await getStore(storeName, 'readwrite');
      return new Promise((resolve, reject) => {
        const req = store.clear();
        req.onsuccess = () => {
          emitChange(storeName, { type: 'clear' });
          resolve(true);
        };
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Count records in a store
     */
    async count(storeName, keyOrRange) {
      const store = await getStore(storeName, 'readonly');
      return new Promise((resolve, reject) => {
        const req = keyOrRange ? store.count(keyOrRange) : store.count();
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
    },

    /**
     * Bulk put multiple records inside a single transaction
     */
    async bulkPut(storeName, items) {
      if (!Array.isArray(items) || items.length === 0) return 0;
      const db = await openDB();
      const tx = db.transaction([storeName], 'readwrite');
      const store = tx.objectStore(storeName);

      return new Promise((resolve, reject) => {
        let count = 0;
        for (let i = 0; i < items.length; i++) {
          const req = store.put(items[i]);
          req.onsuccess = () => count++;
        }
        tx.oncomplete = () => {
          emitChange(storeName, { type: 'bulkPut', count });
          resolve(count);
        };
        tx.onerror = () => reject(tx.error);
      });
    },

    // ==========================================
    // SPECIALIZED NTA CBT CRASH-RESILIENCE API
    // ==========================================

    /**
     * Persist single question response with atomic UPSERT & deterministic ID
     */
    async saveExamResponse(examId, questionId, responsePayload) {
      const id = `${examId}_${questionId}`;
      const record = {
        id,
        examId: String(examId),
        questionId: String(questionId),
        subject: responsePayload.subject || '',
        section: responsePayload.section || 'A',
        state: responsePayload.state || 1, // 1: Not Visited, 2: Not Answered, 3: Answered, 4: Marked Review, 5: Answered & Marked Review
        selectedOption: responsePayload.selectedOption !== undefined ? responsePayload.selectedOption : null,
        numericalValue: responsePayload.numericalValue !== undefined ? responsePayload.numericalValue : null,
        timeSpentSeconds: Number(responsePayload.timeSpentSeconds || 0),
        isCorrect: responsePayload.isCorrect !== undefined ? responsePayload.isCorrect : null,
        updatedAt: Date.now()
      };
      await this.put('exam_responses', record);
      return id;
    },

    /**
     * Retrieve all question responses for an exam
     */
    async getExamResponses(examId) {
      return this.getByIndex('exam_responses', 'examId', String(examId));
    },

    /**
     * Save active exam session metadata and countdown timer
     */
    async saveExamState(examId, examData) {
      const existing = (await this.get('exams', String(examId))) || {};
      const updated = {
        ...existing,
        ...examData,
        examId: String(examId),
        updatedAt: Date.now()
      };
      await this.put('exams', updated);
      return updated;
    },

    /**
     * Get active exam session metadata
     */
    async getExamState(examId) {
      return this.get('exams', String(examId));
    },

    /**
     * Subscribe to changes on a specific store
     */
    subscribe(storeName, callback) {
      if (!listeners.has(storeName)) {
        listeners.set(storeName, new Set());
      }
      listeners.get(storeName).add(callback);
      return () => {
        if (listeners.has(storeName)) {
          listeners.get(storeName).delete(callback);
        }
      };
    }
  };

  return client;
});
