#!/usr/bin/env python3
"""
ClockEE Package: Agent Memory Vault (Claude-Mem / Mem0 Equivalent)
Provides persistent, categorized long-term memory across sessions using SQLite.
Stores user learning habits, exam targets, recurring mistake archetypes, and developer notes.
"""

import os
import sys
import json
import sqlite3
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = ROOT_DIR / "integrations" / "agent_memory" / "agent_memory.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                importance INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON memory_nodes(category)")
    return conn

class AgentMemory:
    def __init__(self):
        self.conn = get_db()

    def remember(self, key: str, value: any, category: str = "general", importance: int = 1):
        """Store or update a memory node."""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        with self.conn:
            self.conn.execute("""
                INSERT INTO memory_nodes (category, key, value, importance, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    category = excluded.category,
                    importance = excluded.importance,
                    updated_at = CURRENT_TIMESTAMP
            """, (category, key, serialized, importance))
        return True

    def recall(self, key: str):
        """Recall a specific memory by key."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM memory_nodes WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            try:
                return json.loads(row["value"])
            except Exception:
                return row["value"]
        return None

    def list_memories(self, category: str = None):
        """List all memories, optionally filtered by category."""
        cursor = self.conn.cursor()
        if category:
            cursor.execute("SELECT category, key, value, importance, updated_at FROM memory_nodes WHERE category = ? ORDER BY importance DESC", (category,))
        else:
            cursor.execute("SELECT category, key, value, importance, updated_at FROM memory_nodes ORDER BY importance DESC")
        
        results = []
        for r in cursor.fetchall():
            try:
                v = json.loads(r["value"])
            except Exception:
                v = r["value"]
            results.append({
                "category": r["category"],
                "key": r["key"],
                "value": v,
                "importance": r["importance"],
                "updated_at": r["updated_at"]
            })
        return results

if __name__ == "__main__":
    mem = AgentMemory()
    mem.remember("aspirant_goal", "JEE Advanced 2028 - Top 100 AIR", category="aspirant_profile", importance=5)
    mem.remember("weak_topic", "Rotational Mechanics - Moment of Inertia", category="mistake_patterns", importance=4)
    print("Agent Memory Initialized. Current Nodes:")
    print(json.dumps(mem.list_memories(), indent=2))
