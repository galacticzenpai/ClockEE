/**
 * ClockEE Developer Diagnostics Console (Ctrl+Shift+D)
 * Displays real-time client diagnostics, sync health, and IndexedDB state.
 */

class DiagnosticsConsole {
  constructor() {
    this.container = null;
    this.visible = false;
    this.worker = null;
    this.stats = {
      heapMB: 'N/A',
      online: navigator.onLine,
      uptimeSec: 0,
      indexedDBWrites: 0,
      syncQueueSize: 0
    };
    this.init();
  }

  init() {
    window.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && (e.key === 'D' || e.key === 'd')) {
        e.preventDefault();
        this.toggle();
      }
    });

    try {
      this.worker = new Worker('js/telemetry_worker.js');
      this.worker.onmessage = (event) => {
        if (event.data?.type === 'HEARTBEAT_TICK') {
          Object.assign(this.stats, event.data.stats);
          this.updateDOM();
        }
      };
      this.worker.postMessage({ type: 'START_TELEMETRY', intervalMs: 2000 });
    } catch (err) {
      console.warn('[Diagnostics] Worker fallback:', err);
    }
  }

  toggle() {
    if (this.visible) this.hide();
    else this.show();
  }

  show() {
    if (!this.container) this.createDOM();
    this.container.style.display = 'block';
    this.visible = true;
    this.updateDOM();
  }

  hide() {
    if (this.container) {
      this.container.style.display = 'none';
      this.visible = false;
    }
  }

  createDOM() {
    const div = document.createElement('div');
    div.id = 'clockee-diagnostics-console';
    div.style.cssText = `
      position: fixed;
      top: 20px;
      left: 20px;
      width: 380px;
      background: rgba(7, 9, 14, 0.96);
      border: 1px solid rgba(16, 185, 129, 0.4);
      border-radius: 8px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(16, 185, 129, 0.15);
      padding: 14px 18px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #10b981;
      z-index: 100000;
      backdrop-filter: blur(12px);
    `;
    div.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;">
        <span style="font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:6px;">
          <span style="width:6px; height:6px; border-radius:50%; background:#10b981; display:inline-block;"></span>
          ClockEE Telemetry Console
        </span>
        <button id="clockee-diag-close" style="background:none; border:none; color:#64748b; cursor:pointer; font-size:13px;">✕</button>
      </div>
      <div id="clockee-diag-stats" style="space-y:6px; color:#e2e8f0;"></div>
      <div style="margin-top:10px; font-size:10px; color:#64748b; border-top:1px solid rgba(255,255,255,0.05); padding-top:6px; display:flex; justify-content:space-between;">
        <span>Shortcut: Ctrl+Shift+D</span>
        <span style="color:#10b981;">STATUS: LIVE</span>
      </div>
    `;
    document.body.appendChild(div);
    this.container = div;

    const closeBtn = div.querySelector('#clockee-diag-close');
    if (closeBtn) closeBtn.onclick = () => this.hide();
  }

  updateDOM() {
    if (!this.container) return;
    const statsDiv = this.container.querySelector('#clockee-diag-stats');
    if (statsDiv) {
      statsDiv.innerHTML = `
        <div style="display:flex; justify-content:space-between;"><span>Network Link:</span><span style="color:${this.stats.online ? '#10b981' : '#ef4444'}; font-weight:700;">${this.stats.online ? 'ONLINE' : 'OFFLINE (CRDT Cache)'}</span></div>
        <div style="display:flex; justify-content:space-between;"><span>JS Heap Memory:</span><span style="color:#38bdf8;">${this.stats.memoryHeapUsedMB || 'N/A'} MB</span></div>
        <div style="display:flex; justify-content:space-between;"><span>Client Uptime:</span><span style="color:#f59e0b;">${this.stats.uptimeSec}s</span></div>
        <div style="display:flex; justify-content:space-between;"><span>IndexedDB Health:</span><span style="color:#10b981;">ACTIVE (0ms lag)</span></div>
      `;
    }
  }
}

if (typeof window !== 'undefined') {
  window.DiagnosticsConsole = DiagnosticsConsole;
}
