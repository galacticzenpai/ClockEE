---
name: cbt_exam_timer
description: High-precision crash-resilient Web Worker countdown timer with IndexedDB/LocalStorage timestamp anchoring.
domain: Adaptive CBT Exam Engine
upstream: clockee/cbt-timer
reel_id: reel_010
---

# ⚡ Crash-Resilient Web Worker CBT Timer (Reel #10)

High-precision 180-minute countdown timer executing in a dedicated Web Worker thread, immune to main-thread UI rendering lag and tab throttling.

## Capabilities
1. **Zero-Drift Web Worker**: Background thread ticks on wall-clock anchoring (`Date.now()`).
2. **Crash & Tab Hibernate Recovery**: Anchors target timestamp to persistent storage so tab reload recovers exact remaining seconds without timer reset.
3. **Paced Warning Cadence**: Automatically fires urgent warning pulse at T-minus 15 minutes and critical alert at T-minus 5 minutes.
4. **Auto-Submit on Zero**: Broadcasts `clockee:timer-expired` custom event for clean test submission.

## Usage in CBT Pages
```html
<script src="js/cbt_timer_manager.js"></script>
<script>
  ClockEETimer.start(180 * 60); // 3-hour exam
  ClockEETimer.onTick((data) => {
    console.log(data.formattedTime, data.progressPercentage);
  });
</script>
```
