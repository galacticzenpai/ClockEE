# Hands-on Engineering Labs: Mentor-Inspired Building Blocks
*Inspired by Codecrafters, Protohackers, roadmap.sh, and our 100 System Mentors*

This guide and test suite provide beginner-to-advanced developers with runnable, self-contained implementations of four foundational distributed and backend systems primitives.

---

## Lab Overview Matrix

| Lab # | System Component | Primary Mentor / Inspiration | Key Architectural Patterns Demonstrated |
| :--- | :--- | :--- | :--- |
| **Lab 1** | **MiniRedis (In-Memory K/V Store)** | Salvatore Sanfilippo (`antirez`) | O(1) Dictionary Lookup, Millisecond TTL, Passive (Lazy) Eviction on Access, Active Probabilistic Eviction Cycle. |
| **Lab 2** | **Token Bucket Rate Limiter** | Alex Xu (`System Design Interview`) | Burst Capacity, Non-blocking Fractional Refill Calculation based on $\Delta t$, Thread-Safe Token Depletion. |
| **Lab 3** | **Zero-Dependency Raw Socket HTTP Server** | Matteo Collina & Ryan Dahl (`Protohackers`) | Raw TCP Socket I/O, RFC-Compliant HTTP/1.1 Framing, Radix/Trie Parametric Routing (`:id` match). |
| **Lab 4** | **Idempotency Key Middleware Engine** | Stripe Engineering Architecture | `Idempotency-Key` deduplication, Atomic in-flight request lock, Cached replay response, 422 Payload Conflict detection. |

---

## 1. Lab Specifications & Deep-Dive

### Lab 1: MiniRedis (Salvatore Sanfilippo / antirez)
- **Concept**: A high-performance in-memory key-value engine cannot afford a timer thread for every key. Instead, Redis uses two complementary eviction mechanisms:
  1. **Passive Eviction**: When a key is requested (`GET`), check if `time.time() >= expires[key]`. If expired, delete it and return `None`.
  2. **Active Eviction**: Periodically run a random sampling sweep (`active_expire_cycle`) over keys with expiration deadlines, deleting expired keys to prevent memory leaks from keys that are never queried again.

### Lab 2: Token Bucket Rate Limiter (Alex Xu)
- **Concept**: Rate limiting without background timer overhead. When a request arrives:
  $$\Delta t = \text{now} - \text{last\_refill\_time}$$
  $$\text{tokens} = \min(\text{capacity}, \text{current\_tokens} + \Delta t \times \text{refill\_rate})$$
  If $\text{tokens} \ge \text{required}$, decrement tokens and allow request; otherwise return HTTP 429 Too Many Requests.

### Lab 3: Raw Socket HTTP/1.1 & Radix Trie Router (Protohackers / Matteo Collina)
- **Concept**: Building an HTTP server from scratch using raw OS TCP sockets (`socket.socket(AF_INET, SOCK_STREAM)`):
  - Parsing the HTTP request line: `METHOD /path HTTP/1.1`
  - Parsing HTTP headers and body delimiter (`\r\n\r\n`)
  - Route resolution using a **Trie (Prefix Tree)** with support for dynamic URL parameters (`/users/:id` -> `params = {"id": "42"}`)
  - Formatting RFC-compliant responses with `Content-Length`, `Content-Type`, and `Connection: close`.

### Lab 4: Stripe-Style Idempotency Engine
- **Concept**: Guaranteeing at-most-once execution of mutating operations (e.g. payment transactions) despite network disconnects and retries:
  - If a key has never been seen: store `IN_PROGRESS` record and execute transaction.
  - If a key is currently `IN_PROGRESS`: subsequent concurrent requests wait on a thread event (atomic mutex) until the primary request finishes, preventing duplicate work.
  - If a key has completed: immediately replay the cached status code and payload without re-running the underlying operation.
  - If a key is re-used with an altered payload: immediately reject with `422 Unprocessable Entity` (payload mismatch error).

---

## 2. How to Run the Demonstration and Tests

The test suite is completely self-contained in Python 3 standard library with **zero external dependencies**.

### Execution Command:
```bash
python hands_on_engineering_labs.py
```

### Expected Output:
```text
======================================================================
RUNNING HANDS-ON ENGINEERING LAB AUTOMATED TESTS
======================================================================

[LAB 1] Testing MiniRedis (TTL & Eviction)...
  -> MiniRedis passed all tests: O(1) ops, TTL tracking, passive & active eviction.

[LAB 2] Testing TokenBucketRateLimiter (Alex Xu)...
  -> TokenBucketRateLimiter passed: Burst control and fractional refill verified.

[LAB 3] Testing Raw Socket HTTP Server & Radix Trie Router...
  -> Raw Socket HTTP Server passed: Trie resolution, param extraction & HTTP/1.1 framing.

[LAB 4] Testing IdempotencyEngine (Stripe-Inspired)...
  -> IdempotencyEngine passed: Replay cache, deduplication, and payload mismatch rejection.

======================================================================
ALL 4 HANDS-ON ENGINEERING LABS PASSED VERIFICATION ACCURATELY!
======================================================================
```

---

## 3. Recommended Student Next Steps & Extensions
1. **Lab 1 Extension**: Implement Redis RESP2 protocol parser over TCP sockets and test with the official `redis-cli`.
2. **Lab 2 Extension**: Implement Sliding Window Counter or Leaky Bucket with Redis-backed distributed atomics (`INCRBY` + `EXPIRE`).
3. **Lab 3 Extension**: Add keep-alive persistent connections (`Connection: keep-alive`) with HTTP pipeline parsing.
4. **Lab 4 Extension**: Back the idempotency engine with PostgreSQL using `INSERT INTO idempotency_keys ... ON CONFLICT DO NOTHING`.
