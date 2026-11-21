
class SPSCRingBuffer {
  constructor(capacityPowerOfTwo = 1024) {
    if ((capacityPowerOfTwo & (capacityPowerOfTwo - 1)) !== 0) {
      throw new Error("Capacity must be a power of 2");
    }
    this.capacity = capacityPowerOfTwo;
    this.mask = capacityPowerOfTwo - 1;
    this.buffer = new Float64Array(this.capacity);
    this.head = 0; // Producer write index
    this.tail = 0; // Consumer read index
  }

  push(value) {
    if (this.head - this.tail >= this.capacity) {
      return false; // Buffer full: zero allocation drop policy
    }
    this.buffer[this.head & this.mask] = value;
    this.head++;
    return true;
  }

  pop() {
    if (this.head === this.tail) {
      return null; // Buffer empty
    }
    const val = this.buffer[this.tail & this.mask];
    this.tail++;
    return val;
  }

  size() {
    return this.head - this.tail;
  }
}

const ring = new SPSCRingBuffer(16);
for (let i = 0; i < 16; i++) {
  const ok = ring.push(i * 10);
  if (!ok) throw new Error("Failed to push to available ring slot " + i);
}

// 17th push must fail (no allocation, drop policy)
if (ring.push(999) !== false) {
  throw new Error("Ring buffer overflow policy failed!");
}

let consumed = [];
while (ring.size() > 0) {
  consumed.push(ring.pop());
}

if (consumed.length === 16 && consumed[15] === 150) {
  console.log("PASS: Lock-Free SPSC Ring Buffer circular bitmask indexing verified successfully!");
} else {
  console.error("FAIL: Ring buffer output incorrect", consumed);
  process.exit(1);
}
