"""
Hands-On Engineering Labs - Master Test & Execution Suite
Inspired by:
- Codecrafters & Protohackers
- antirez (Redis - In-Memory Key-Value Store with TTL & Dict Rehashing)
- Alex Xu (Token Bucket & Leaky Bucket Rate Limiters)
- Matteo Collina / Ryan Dahl (Zero-Dependency HTTP/1.1 Server with Radix/Trie Routing)
- Stripe Engineering (Idempotency Key Middleware with Replay Cache & In-Flight Mutex)
"""

import sys
import os
import time
import socket
import threading
import json
import uuid
import re
from typing import Dict, Any, Optional, Tuple, Callable

# ==============================================================================
# LAB 1: In-Memory Key-Value Store with TTL & Active/Passive Eviction (antirez/Redis)
# ==============================================================================
class MiniRedis:
    """
    In-memory key-value store with:
    - O(1) SET, GET, DEL
    - EXPIRE / TTL support
    - Passive eviction (on GET)
    - Active eviction (probabilistic random sampling cycle like Redis dict eviction)
    """
    def __init__(self):
        self._db: Dict[str, Any] = {}
        self._expires: Dict[str, float] = {}
        self._lock = threading.Lock()

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> bool:
        with self._lock:
            self._db[key] = value
            if ttl_seconds is not None:
                self._expires[key] = time.time() + ttl_seconds
            elif key in self._expires:
                del self._expires[key]
            return True

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            # Passive expiration check (lazy eviction)
            if key in self._expires and time.time() >= self._expires[key]:
                self._delete_key(key)
                return None
            return self._db.get(key, None)

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._delete_key(key)

    def ttl(self, key: str) -> Optional[float]:
        with self._lock:
            if key not in self._db:
                return None
            if key not in self._expires:
                return -1  # Persists indefinitely
            remaining = self._expires[key] - time.time()
            if remaining <= 0:
                self._delete_key(key)
                return None
            return remaining

    def active_expire_cycle(self, sample_size: int = 10) -> int:
        """
        Active random sampling eviction loop:
        Sample N keys with expires, delete expired ones.
        """
        with self._lock:
            keys_with_expiry = list(self._expires.keys())
            if not keys_with_expiry:
                return 0
            
            sample = keys_with_expiry[:sample_size]
            now = time.time()
            evicted = 0
            for k in sample:
                if now >= self._expires[k]:
                    self._delete_key(k)
                    evicted += 1
            return evicted

    def _delete_key(self, key: str) -> bool:
        existed = False
        if key in self._db:
            del self._db[key]
            existed = True
        if key in self._expires:
            del self._expires[key]
        return existed

    def size(self) -> int:
        with self._lock:
            return len(self._db)


# ==============================================================================
# LAB 2: Token Bucket & Sliding Window Rate Limiter (Alex Xu / Stripe API)
# ==============================================================================
class TokenBucketRateLimiter:
    """
    Token Bucket Algorithm:
    - capacity: maximum burst allowed
    - refill_rate: tokens added per second
    Smoothly refills based on elapsed time without background timer threads.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._buckets: Dict[str, Tuple[float, float]] = {}  # key -> (tokens, last_refill_time)
        self._lock = threading.Lock()

    def allow_request(self, key: str, tokens: int = 1) -> bool:
        with self._lock:
            now = time.time()
            if key not in self._buckets:
                self._buckets[key] = (self.capacity, now)

            current_tokens, last_time = self._buckets[key]
            # Refill tokens based on delta time
            elapsed = now - last_time
            current_tokens = min(self.capacity, current_tokens + (elapsed * self.refill_rate))

            if current_tokens >= tokens:
                self._buckets[key] = (current_tokens - tokens, now)
                return True
            else:
                self._buckets[key] = (current_tokens, now)
                return False


# ==============================================================================
# LAB 3: Zero-Dependency Raw Socket HTTP/1.1 Server with Trie/Radix Router
# (Matteo Collina / Ryan Dahl / Protohackers style)
# ==============================================================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.handler: Optional[Callable[[Dict[str, Any]], Tuple[int, Dict[str, str], str]]] = None
        self.param_name: Optional[str] = None


class HTTPRouter:
    """
    Trie-based parameterized HTTP URL router supporting :param matching.
    """
    def __init__(self):
        self.root = TrieNode()

    def add_route(self, method: str, path: str, handler: Callable):
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.root
        method_key = f"__METHOD_{method.upper()}__"
        if method_key not in curr.children:
            curr.children[method_key] = TrieNode()
        curr = curr.children[method_key]

        for part in parts:
            if part.startswith(":"):
                # Parametric node
                param_key = ":param"
                if param_key not in curr.children:
                    node = TrieNode()
                    node.param_name = part[1:]
                    curr.children[param_key] = node
                curr = curr.children[param_key]
            else:
                if part not in curr.children:
                    curr.children[part] = TrieNode()
                curr = curr.children[part]
        curr.handler = handler

    def resolve(self, method: str, path: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        parts = [p for p in path.strip("/").split("/") if p]
        curr = self.root
        method_key = f"__METHOD_{method.upper()}__"
        if method_key not in curr.children:
            return None, {}
        curr = curr.children[method_key]

        params = {}
        for part in parts:
            if part in curr.children:
                curr = curr.children[part]
            elif ":param" in curr.children:
                curr = curr.children[":param"]
                if curr.param_name:
                    params[curr.param_name] = part
            else:
                return None, {}
        return curr.handler, params


class RawHTTPServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self.router = HTTPRouter()
        self.server_socket: Optional[socket.socket] = None
        self._is_running = False
        self._thread: Optional[threading.Thread] = None

    def route(self, method: str, path: str):
        def decorator(handler):
            self.router.add_route(method, path, handler)
            return handler
        return decorator

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen(128)
        self._is_running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self):
        self._is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join(timeout=1.0)

    def _serve(self):
        while self._is_running:
            try:
                client_sock, _ = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True).start()
            except Exception:
                break

    def _handle_client(self, client_sock: socket.socket):
        with client_sock:
            try:
                raw_data = client_sock.recv(4096).decode("utf-8", errors="replace")
                if not raw_data:
                    return

                lines = raw_data.split("\r\n")
                request_line = lines[0].split(" ")
                if len(request_line) < 2:
                    return
                method, full_path = request_line[0], request_line[1]

                path = full_path.split("?")[0]
                handler, params = self.router.resolve(method, path)

                headers = {}
                idx = 1
                while idx < len(lines) and lines[idx]:
                    header_line = lines[idx]
                    if ": " in header_line:
                        k, v = header_line.split(": ", 1)
                        headers[k.lower()] = v
                    idx += 1

                body = "\r\n".join(lines[idx + 1:]) if idx + 1 < len(lines) else ""
                req = {"method": method, "path": path, "params": params, "headers": headers, "body": body}

                if handler:
                    status_code, resp_headers, resp_body = handler(req)
                else:
                    status_code, resp_headers, resp_body = 404, {"Content-Type": "application/json"}, json.dumps({"error": "Not Found"})

                status_text = {200: "OK", 201: "Created", 400: "Bad Request", 404: "Not Found", 409: "Conflict", 429: "Too Many Requests"}.get(status_code, "OK")
                resp_bytes = resp_body.encode("utf-8")
                resp_headers["Content-Length"] = str(len(resp_bytes))
                resp_headers["Connection"] = "close"

                head = f"HTTP/1.1 {status_code} {status_text}\r\n"
                for hk, hv in resp_headers.items():
                    head += f"{hk}: {hv}\r\n"
                head += "\r\n"

                client_sock.sendall(head.encode("utf-8") + resp_bytes)
            except Exception:
                pass


# ==============================================================================
# LAB 4: Idempotency Key Middleware with Replay Cache & In-Flight Lock (Stripe)
# ==============================================================================
class IdempotencyRecord:
    def __init__(self, status: str = "IN_PROGRESS"):
        self.status = status  # IN_PROGRESS, COMPLETED, FAILED
        self.status_code: Optional[int] = None
        self.response_body: Optional[str] = None
        self.event = threading.Event()


class IdempotencyEngine:
    """
    Stripe-inspired Idempotency Middleware engine.
    Ensures that retried POST requests:
    1. Replay cached result if previous request succeeded.
    2. Block and wait if an identical idempotency key is actively being processed.
    3. Detect payload hash mismatch if identical key is used with conflicting parameters.
    """
    def __init__(self, lock_timeout: float = 3.0):
        self.lock_timeout = lock_timeout
        self.cache: Dict[str, IdempotencyRecord] = {}
        self.payload_hashes: Dict[str, str] = {}
        self._lock = threading.Lock()

    def process(self, idempotency_key: str, payload_str: str, execute_fn: Callable[[], Tuple[int, str]]) -> Tuple[int, str, bool]:
        """
        Returns: (status_code, response_body, is_cached_replay)
        """
        with self._lock:
            # Check existing
            if idempotency_key in self.cache:
                record = self.cache[idempotency_key]
                if self.payload_hashes.get(idempotency_key) != payload_str:
                    return 422, json.dumps({"error": "Idempotency key payload mismatch"}), False
                
                if record.status == "COMPLETED":
                    return record.status_code or 200, record.response_body or "", True
                elif record.status == "FAILED":
                    return record.status_code or 500, record.response_body or "", True
                
                is_in_progress = True
            else:
                record = IdempotencyRecord("IN_PROGRESS")
                self.cache[idempotency_key] = record
                self.payload_hashes[idempotency_key] = payload_str
                is_in_progress = False

        if is_in_progress:
            # Wait for leader to finish
            finished = record.event.wait(timeout=self.lock_timeout)
            if not finished:
                return 409, json.dumps({"error": "Concurrent request in-flight timeout"}), False
            return record.status_code or 500, record.response_body or "", True

        # First caller executes
        try:
            status_code, resp_body = execute_fn()
            record.status_code = status_code
            record.response_body = resp_body
            record.status = "COMPLETED"
            return status_code, resp_body, False
        except Exception as e:
            record.status = "FAILED"
            record.status_code = 500
            record.response_body = json.dumps({"error": str(e)})
            raise
        finally:
            record.event.set()


# ==============================================================================
# AUTOMATED LAB TEST SUITE
# ==============================================================================
def run_all_lab_tests():
    print("=" * 70)
    print("RUNNING HANDS-ON ENGINEERING LAB AUTOMATED TESTS")
    print("=" * 70)

    # -------------------------------------------------------------
    # Test 1: Redis Key-Value Store & TTL Eviction
    # -------------------------------------------------------------
    print("\n[LAB 1] Testing MiniRedis (TTL & Eviction)...")
    store = MiniRedis()
    store.set("user:1", {"name": "Alice"})
    assert store.get("user:1") == {"name": "Alice"}

    # TTL test with passive expiration
    store.set("temp_token", "secret123", ttl_seconds=0.2)
    assert store.get("temp_token") == "secret123"
    assert store.ttl("temp_token") > 0
    time.sleep(0.25)
    assert store.get("temp_token") is None, "Failed: Key should have passively expired"
    assert store.ttl("temp_token") is None

    # Active expiration test
    store.set("batch:1", "val1", ttl_seconds=0.1)
    store.set("batch:2", "val2", ttl_seconds=0.1)
    time.sleep(0.15)
    evicted_count = store.active_expire_cycle(sample_size=10)
    assert evicted_count >= 2, f"Failed: Expected at least 2 evicted keys, got {evicted_count}"
    assert store.size() == 1  # Only user:1 remains
    print("  -> MiniRedis passed all tests: O(1) ops, TTL tracking, passive & active eviction.")

    # -------------------------------------------------------------
    # Test 2: Token Bucket Rate Limiter
    # -------------------------------------------------------------
    print("\n[LAB 2] Testing TokenBucketRateLimiter (Alex Xu)...")
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate=2.0)  # 3 tokens max, refills 2 per sec
    client_ip = "192.168.1.10"

    assert limiter.allow_request(client_ip), "Request 1 should pass"
    assert limiter.allow_request(client_ip), "Request 2 should pass"
    assert limiter.allow_request(client_ip), "Request 3 should pass"
    assert not limiter.allow_request(client_ip), "Request 4 should be rate limited"

    # Refill test
    time.sleep(0.55)  # Refills ~1.1 tokens
    assert limiter.allow_request(client_ip), "Request 5 after refill should pass"
    assert not limiter.allow_request(client_ip), "Exceeded available refilled token"
    print("  -> TokenBucketRateLimiter passed: Burst control and fractional refill verified.")

    # -------------------------------------------------------------
    # Test 3: Zero-Dependency Raw Socket HTTP Server with Trie Routing
    # -------------------------------------------------------------
    print("\n[LAB 3] Testing Raw Socket HTTP Server & Radix Trie Router...")
    server = RawHTTPServer(host="127.0.0.1", port=0)

    @server.route("GET", "/health")
    def health_handler(req):
        return 200, {"Content-Type": "application/json"}, json.dumps({"status": "healthy"})

    @server.route("GET", "/users/:id")
    def user_handler(req):
        uid = req["params"].get("id")
        return 200, {"Content-Type": "application/json"}, json.dumps({"userId": uid, "user": f"User_{uid}"})

    server.start()
    try:
        # Client request 1: static route
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect(("127.0.0.1", server.port))
        s1.sendall(b"GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n")
        resp1 = s1.recv(4096).decode()
        s1.close()
        assert "200 OK" in resp1
        assert '"status": "healthy"' in resp1

        # Client request 2: parameterized route /users/42
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect(("127.0.0.1", server.port))
        s2.sendall(b"GET /users/42 HTTP/1.1\r\nHost: localhost\r\n\r\n")
        resp2 = s2.recv(4096).decode()
        s2.close()
        assert "200 OK" in resp2
        assert '"userId": "42"' in resp2

        # Client request 3: 404 route
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.connect(("127.0.0.1", server.port))
        s3.sendall(b"GET /nonexistent HTTP/1.1\r\nHost: localhost\r\n\r\n")
        resp3 = s3.recv(4096).decode()
        s3.close()
        assert "404 Not Found" in resp3
        print("  -> Raw Socket HTTP Server passed: Trie resolution, param extraction & HTTP/1.1 framing.")
    finally:
        server.stop()

    # -------------------------------------------------------------
    # Test 4: Stripe-Inspired Idempotency Middleware
    # -------------------------------------------------------------
    print("\n[LAB 4] Testing IdempotencyEngine (Stripe-Inspired)...")
    idempotency = IdempotencyEngine()
    charge_count = [0]

    def mock_charge_payment():
        time.sleep(0.05)  # Simulate payment gateway call
        charge_count[0] += 1
        return 200, json.dumps({"charge_id": f"ch_{charge_count[0]}", "amount": 5000})

    idem_key = "idem_tx_998877"
    payload = json.dumps({"amount": 5000, "currency": "usd"})

    # Primary execution
    code1, resp1, is_cached1 = idempotency.process(idem_key, payload, mock_charge_payment)
    assert code1 == 200
    assert not is_cached1
    assert charge_count[0] == 1

    # Retry with same key and same payload -> MUST replay cached response, zero duplicate charge
    code2, resp2, is_cached2 = idempotency.process(idem_key, payload, mock_charge_payment)
    assert code2 == 200
    assert is_cached2, "Subsequent identical request must be served from idempotency replay cache"
    assert resp2 == resp1
    assert charge_count[0] == 1, "Duplicate payment was triggered!"

    # Conflict test: same idempotency key with different payload
    different_payload = json.dumps({"amount": 9000, "currency": "usd"})
    code3, resp3, is_cached3 = idempotency.process(idem_key, different_payload, mock_charge_payment)
    assert code3 == 422, "Conflicting payload with identical idempotency key must return 422 Unprocessable"
    print("  -> IdempotencyEngine passed: Replay cache, deduplication, and payload mismatch rejection.")

    print("\n" + "=" * 70)
    print("ALL 4 HANDS-ON ENGINEERING LABS PASSED VERIFICATION ACCURATELY!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_lab_tests()
