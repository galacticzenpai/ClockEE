/**
 * ⚡ ClockEE — Reel #10: Web Worker Precision Countdown Timer (js/workers/cbt_timer_worker.js)
 * Isolated background thread timer immune to main-thread DOM freezes, tab backgrounding, and throttling.
 */

let timerInterval = null;
let endTime = 0;
let totalDurationSeconds = 180 * 60; // 3 hours default
let isPaused = false;
let pauseOffset = 0;

self.onmessage = function(e) {
  const { command, durationSeconds, targetTimestamp } = e.data || {};

  switch (command) {
    case 'START':
      totalDurationSeconds = durationSeconds || (180 * 60);
      endTime = targetTimestamp || (Date.now() + totalDurationSeconds * 1000);
      isPaused = false;
      startTicking();
      break;

    case 'PAUSE':
      isPaused = true;
      pauseOffset = Math.max(0, endTime - Date.now());
      if (timerInterval) clearInterval(timerInterval);
      self.postMessage({ type: 'PAUSED', remainingSeconds: Math.ceil(pauseOffset / 1000) });
      break;

    case 'RESUME':
      if (isPaused) {
        endTime = Date.now() + pauseOffset;
        isPaused = false;
        startTicking();
      }
      break;

    case 'STOP':
      if (timerInterval) clearInterval(timerInterval);
      isPaused = false;
      self.postMessage({ type: 'STOPPED' });
      break;

    case 'PING':
      const rem = Math.max(0, Math.ceil((endTime - Date.now()) / 1000));
      self.postMessage({ type: 'PONG', remainingSeconds: rem });
      break;
  }
};

function startTicking() {
  if (timerInterval) clearInterval(timerInterval);

  // Immediate initial tick
  emitTick();

  // Tick every 250ms for wall-clock alignment
  timerInterval = setInterval(() => {
    emitTick();
  }, 250);
}

function emitTick() {
  const now = Date.now();
  const diffMs = endTime - now;
  const remainingSeconds = Math.max(0, Math.ceil(diffMs / 1000));
  const elapsedSeconds = totalDurationSeconds - remainingSeconds;
  const progressPct = Math.min(100, Math.max(0, (elapsedSeconds / totalDurationSeconds) * 100));

  self.postMessage({
    type: 'TICK',
    remainingSeconds: remainingSeconds,
    elapsedSeconds: elapsedSeconds,
    progressPercentage: Math.round(progressPct * 10) / 10,
    isUrgent: remainingSeconds <= (15 * 60), // Warning under 15m
    isCritical: remainingSeconds <= (5 * 60), // Critical pulse under 5m
    formattedTime: formatTime(remainingSeconds)
  });

  if (remainingSeconds <= 0) {
    if (timerInterval) clearInterval(timerInterval);
    self.postMessage({ type: 'EXPIRED' });
  }
}

function formatTime(sec) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}
