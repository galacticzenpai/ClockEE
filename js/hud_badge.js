/**
 * ClockEE Floating Cockpit Telemetry Badge
 * Persistent, non-intrusive status pill in lower-left corner.
 */

class CockpitHUDBadge {
  constructor() {
    this.badge = null;
    this.init();
  }

  init() {
    if (document.getElementById('clockee-hud-badge')) return;
    const pill = document.createElement('div');
    pill.id = 'clockee-hud-badge';
    pill.style.cssText = `
      position: fixed;
      bottom: 16px;
      left: 16px;
      background: rgba(7, 9, 14, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 9999px;
      padding: 6px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #94a3b8;
      z-index: 9999;
      cursor: pointer;
      backdrop-filter: blur(8px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
      transition: border-color 0.2s ease, transform 0.2s ease;
      user-select: none;
    `;
    pill.innerHTML = `
      <span class="tabular-nums" id="clockee-hud-pulse" style="width:7px; height:7px; border-radius:50%; background:#10b981; display:inline-block; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);"></span>
      <span style="font-weight:600; color:#f8fafc;">ClockEE OS</span>
      <span style="color:#64748b;">|</span>
      <span class="tabular-nums" id="clockee-hud-state" style="color:#10b981;">SYNCED</span>
    `;

    pill.onmouseenter = () => {
      pill.style.borderColor = 'rgba(245, 158, 11, 0.4)';
      pill.style.transform = 'translateY(-2px)';
    };
    pill.onmouseleave = () => {
      pill.style.borderColor = 'rgba(255, 255, 255, 0.1)';
      pill.style.transform = 'translateY(0)';
    };

    pill.onclick = () => {
      if (window.DiagnosticsConsole) {
        if (!window.__clockeeDiagInstance) {
          window.__clockeeDiagInstance = new window.DiagnosticsConsole();
        }
        window.__clockeeDiagInstance.toggle();
      }
    };

    document.body.appendChild(pill);
    this.badge = pill;

    // Listen for offline/online transitions
    window.addEventListener('online', () => this.updateStatus(true));
    window.addEventListener('offline', () => this.updateStatus(false));
  }

  updateStatus(isOnline) {
    const stateEl = document.getElementById('clockee-hud-state');
    const pulseEl = document.getElementById('clockee-hud-pulse');
    if (!stateEl || !pulseEl) return;
    if (isOnline) {
      stateEl.textContent = 'SYNCED';
      stateEl.style.color = '#10b981';
      pulseEl.style.background = '#10b981';
      pulseEl.style.boxShadow = '0 0 8px #10b981';
    } else {
      stateEl.textContent = 'OFFLINE (IDB)';
      stateEl.style.color = '#f59e0b';
      pulseEl.style.background = '#f59e0b';
      pulseEl.style.boxShadow = '0 0 8px #f59e0b';
    }
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', () => {
    window.CockpitHUDBadge = new CockpitHUDBadge();
  });
}
