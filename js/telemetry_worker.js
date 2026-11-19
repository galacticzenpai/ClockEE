/**
 * ClockEE Telemetry Background Heartbeat Worker
 * Samples client health, memory usage, and broadcast heartbeats without main thread load.
 */

self.onmessage = function(e) {
  if (e.data && e.data.type === 'START_TELEMETRY') {
    const intervalMs = e.data.intervalMs || 3000;
    setInterval(() => {
      const stats = {
        timestamp: Date.now(),
        memoryHeapUsedMB: (performance && performance.memory) ? Math.round(performance.memory.usedJSHeapSize / (1024 * 1024)) : 'N/A',
        online: navigator.onLine,
        uptimeSec: Math.round(performance.now() / 1000)
      };
      self.postMessage({ type: 'HEARTBEAT_TICK', stats });
    }, intervalMs);
  }
};
