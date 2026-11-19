-- ==============================================================================
-- ⚡ ClockEE — Reel #5: SQLite-VSS Local Vector Similarity Search Schema
-- Upstream: asg017/sqlite-vss
-- Domain: Local-First Vector Search for Offline Question Bank Similarity
-- ==============================================================================

-- 1. Question Vector Embeddings Table
CREATE TABLE IF NOT EXISTS question_embeddings (
    question_id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    chapter TEXT NOT NULL,
    difficulty TEXT DEFAULT 'moderate',
    content_snippet TEXT NOT NULL,
    embedding_dim INTEGER DEFAULT 64,
    embedding_json TEXT NOT NULL,       -- JSON array of floats (normalized)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Fast Lookup Indexes
CREATE INDEX IF NOT EXISTS idx_vss_subject ON question_embeddings(subject);
CREATE INDEX IF NOT EXISTS idx_vss_topic ON question_embeddings(topic);
CREATE INDEX IF NOT EXISTS idx_vss_difficulty ON question_embeddings(difficulty);

-- 3. Virtual VSS Index Metadata (Tracks index builds & latency metrics)
CREATE TABLE IF NOT EXISTS vss_index_meta (
    index_id TEXT PRIMARY KEY,
    total_vectors INTEGER NOT NULL,
    dimension INTEGER NOT NULL,
    metric TEXT DEFAULT 'cosine',       -- 'cosine' | 'l2' | 'inner_product'
    avg_query_latency_ms REAL DEFAULT 0.0,
    last_indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
