#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #29: Concurrent SQLite Multi-Process Transaction Arbiter
Upstream: sqlite/deadlock-preventer
Domain: Self-Healing & Defect Detection

WAL-mode connection coordinator with exponential backoff and busy-timeout handlers
eliminating 'database is locked' errors under high-concurrency background writes.
"""

import sqlite3
import time
import random
import threading
import os
from contextlib import contextmanager
from typing import Generator

DEFAULT_BUSY_TIMEOUT_MS = 5000
MAX_RETRIES = 5
INITIAL_BACKOFF_SEC = 0.02

class SQLiteArbiter:
    def __init__(self, db_path: str = "clockee_test_wal.db", busy_timeout_ms: int = DEFAULT_BUSY_TIMEOUT_MS):
        self.db_path = db_path
        self.busy_timeout_ms = busy_timeout_ms
        self._init_wal()

    def _init_wal(self):
        """Initializes Write-Ahead Logging (WAL) and synchronous optimization."""
        conn = sqlite3.connect(self.db_path, timeout=self.busy_timeout_ms / 1000.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms};")
        conn.execute("CREATE TABLE IF NOT EXISTS arbiter_telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INT, payload TEXT, timestamp REAL);")
        conn.commit()
        conn.close()

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """Provides a managed transaction with exponential backoff retry on database locks."""
        conn = None
        retries = 0
        backoff = INITIAL_BACKOFF_SEC

        while retries <= MAX_RETRIES:
            try:
                conn = sqlite3.connect(self.db_path, timeout=self.busy_timeout_ms / 1000.0)
                conn.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms};")
                conn.execute("BEGIN IMMEDIATE;")
                yield conn
                conn.commit()
                break
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    retries += 1
                    if retries > MAX_RETRIES:
                        if conn:
                            conn.rollback()
                        raise
                    time.sleep(backoff + random.uniform(0.005, 0.02))
                    backoff *= 1.5
                else:
                    if conn:
                        conn.rollback()
                    raise
            except Exception:
                if conn:
                    conn.rollback()
                raise
            finally:
                if conn:
                    conn.close()

def worker_task(arbiter: SQLiteArbiter, thread_id: int, records_per_thread: int, results: list):
    try:
        for i in range(records_per_thread):
            with arbiter.transaction() as conn:
                conn.execute(
                    "INSERT INTO arbiter_telemetry (thread_id, payload, timestamp) VALUES (?, ?, ?)",
                    (thread_id, f"payload_{thread_id}_{i}", time.time())
                )
        results.append(True)
    except Exception as e:
        results.append(e)

def benchmark_deadlock_arbiter():
    test_db = "integrations/deadlock_resolver/test_wal.db"
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass

    arbiter = SQLiteArbiter(db_path=test_db)

    # Launch 50 concurrent writer threads
    num_threads = 50
    records_per_thread = 5
    expected_records = num_threads * records_per_thread
    threads = []
    results = []

    print(f"[*] Stress testing SQLite WAL Arbiter: {num_threads} concurrent threads ({expected_records} total writes)...")
    t0 = time.perf_counter()

    for tid in range(num_threads):
        t = threading.Thread(target=worker_task, args=(arbiter, tid, records_per_thread, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.perf_counter() - t0
    
    # Verify records in database
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM arbiter_telemetry")
    count = cursor.fetchone()[0]
    conn.close()

    # Clean up test DB
    try:
        if os.path.exists(test_db):
            os.remove(test_db)
    except Exception:
        pass

    errors = [r for r in results if r is not True]
    print(f"[BENCHMARK] Executed {count}/{expected_records} writes across {num_threads} threads in {duration*1000:.2f}ms")
    print(f"Errors / Deadlocks encountered: {len(errors)}")

    assert count == expected_records, f"Expected {expected_records} rows, found {count}"
    assert len(errors) == 0, f"Encountered concurrency errors: {errors}"
    print("[✓] Concurrent SQLite WAL Transaction Arbiter certified (Exit Code 0).")

if __name__ == "__main__":
    benchmark_deadlock_arbiter()
