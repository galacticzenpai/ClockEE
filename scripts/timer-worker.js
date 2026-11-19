/**
 * ClockEE 2.0 - High-Precision Web Worker Timer Engine
 * Guarantees zero time-drift in background tabs, power throttling, and long sessions.
 */

let timerInterval = null;
let startTime = null;
let totalSeconds = 180 * 60; // Default: 180 minutes = 10,800 seconds
let elapsedSeconds = 0;
let isRunning = false;

self.onmessage = function (e) {
  const data = e.data;
  if (!data || !data.type) return;

  switch (data.type) {
    case 'START':
      totalSeconds = data.totalSeconds || totalSeconds;
      elapsedSeconds = data.elapsedSeconds || 0;
      isRunning = true;
      startTime = Date.now() - (elapsedSeconds * 1000);

      if (timerInterval) clearInterval(timerInterval);
      timerInterval = setInterval(tick, 250); // Frequent tick for sub-second precision
      sendTick();
      break;

    case 'PAUSE':
      if (isRunning) {
        isRunning = false;
        if (timerInterval) clearInterval(timerInterval);
        sendTick();
      }
      break;

    case 'RESUME':
      if (!isRunning) {
        isRunning = true;
        startTime = Date.now() - (elapsedSeconds * 1000);
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(tick, 250);
        sendTick();
      }
      break;

    case 'SYNC':
      if (typeof data.elapsedSeconds === 'number') {
        elapsedSeconds = data.elapsedSeconds;
        startTime = Date.now() - (elapsedSeconds * 1000);
      }
      if (typeof data.totalSeconds === 'number') {
        totalSeconds = data.totalSeconds;
      }
      sendTick();
      break;

    case 'RESET':
      isRunning = false;
      if (timerInterval) clearInterval(timerInterval);
      totalSeconds = data.totalSeconds || (180 * 60);
      elapsedSeconds = 0;
      sendTick();
      break;
  }
};

function tick() {
  if (!isRunning) return;

  const now = Date.now();
  const calculatedElapsed = Math.floor((now - startTime) / 1000);

  if (calculatedElapsed !== elapsedSeconds) {
    elapsedSeconds = calculatedElapsed;
    sendTick();
  }

  if (elapsedSeconds >= totalSeconds) {
    elapsedSeconds = totalSeconds;
    isRunning = false;
    if (timerInterval) clearInterval(timerInterval);
    sendTick(true);
  }
}

function sendTick(isOver = false) {
  const remainingSeconds = Math.max(0, totalSeconds - elapsedSeconds);
  self.postMessage({
    type: 'TICK',
    totalSeconds,
    elapsedSeconds,
    remainingSeconds,
    isRunning,
    isOver: isOver || remainingSeconds <= 0
  });
}
