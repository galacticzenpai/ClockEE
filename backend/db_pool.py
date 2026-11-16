import os
import sqlite3
import time
from contextlib import contextmanager
from typing import Generator

class DeadlockFreeDBPool:
    """
    High-concurrency SQLite connection arbiter.
    Enforces WAL mode, busy timeouts, and backoff retries.
    """
    def __init__(self, db_path: str = "clockee.db", timeout_sec: float = 5.0, max_retries: int = 5):
        self.db_path = db_path
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries
        self._init_wal()

    def _init_wal(self):
        try:
            conn = sqlite3.connect(self.db_path, timeout=self.timeout_sec)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute(f"PRAGMA busy_timeout={int(self.timeout_sec * 1000)};")
            conn.close()
        except Exception as e:
            print(f"[DBPool] WAL setup warning: {e}")

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path, timeout=self.timeout_sec)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                # Backoff retry
                for attempt in range(1, self.max_retries + 1):
                    time.sleep(0.05 * (2 ** attempt))
                    try:
                        conn.commit()
                        break
                    except Exception:
                        if attempt == self.max_retries:
                            conn.rollback()
                            raise
            else:
                conn.rollback()
                raise
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def benchmark_db_pool():
    pool = DeadlockFreeDBPool("clockee_benchmark.db")
    with pool.get_connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS test_wal (id INTEGER PRIMARY KEY, val TEXT, ts REAL);")

    # Simulate 50 sequential rapid writes
    t0 = time.perf_counter()
    for i in range(50):
        with pool.get_connection() as conn:
            conn.execute("INSERT INTO test_wal (val, ts) VALUES (?, ?);", (f"item_{i}", time.time()))
    t1 = time.perf_counter()
    latency_ms = ((t1 - t0) / 50) * 1000
    print(f"[BENCHMARK] WAL transaction write latency: {latency_ms:.3f}ms per write (50 writes completed)")
    
    # Cleanup test db
    try:
        os.remove("clockee_benchmark.db")
        if os.path.exists("clockee_benchmark.db-wal"):
            os.remove("clockee_benchmark.db-wal")
        if os.path.exists("clockee_benchmark.db-shm"):
            os.remove("clockee_benchmark.db-shm")
    except Exception:
        pass
    return latency_ms

if __name__ == "__main__":
    benchmark_db_pool()
