/**
 * ClockEE Tactile HUD Overlay
 * Displays a floating tactile shortcut reference legend with retro terminal amber accents.
 */

class CBTHUDOverlay {
  constructor() {
    this.container = null;
    this.visible = false;
    this.createDOM();
  }

  createDOM() {
    if (document.getElementById('clockee-hud-overlay')) {
      this.container = document.getElementById('clockee-hud-overlay');
      return;
    }
    const div = document.createElement('div');
    div.id = 'clockee-hud-overlay';
    div.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(13, 17, 26, 0.95);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 16px rgba(245, 158, 11, 0.15);
      padding: 16px 20px;
      font-family: 'JetBrains Mono', monospace;
      color: #f8fafc;
      font-size: 12px;
      z-index: 99999;
      display: none;
      backdrop-filter: blur(8px);
      max-width: 320px;
      transition: opacity 0.2s ease, transform 0.2s ease;
    `;
    div.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:6px;">
        <span style="font-weight:700; color:#f59e0b; text-transform:uppercase; letter-spacing:0.05em; display:flex; align-items:center; gap:6px;">
          <span style="width:6px; height:6px; border-radius:50%; background:#f59e0b; display:inline-block;"></span>
          Cockpit Keymap
        </span>
        <button id="clockee-hud-close" style="background:none; border:none; color:#64748b; cursor:pointer; font-size:14px; padding:2px;">✕</button>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px 12px;">
        <div><kbd style="background:#1e293b; color:#38bdf8; padding:2px 6px; border-radius:4px; font-weight:600;">1 - 4</kbd> <span style="color:#94a3b8;">Select Opt</span></div>
        <div><kbd style="background:#1e293b; color:#10b981; padding:2px 6px; border-radius:4px; font-weight:600;">S / ↵</kbd> <span style="color:#94a3b8;">Save & Next</span></div>
        <div><kbd style="background:#1e293b; color:#a855f7; padding:2px 6px; border-radius:4px; font-weight:600;">M / R</kbd> <span style="color:#94a3b8;">Review</span></div>
        <div><kbd style="background:#1e293b; color:#ef4444; padding:2px 6px; border-radius:4px; font-weight:600;">C / ⌫</kbd> <span style="color:#94a3b8;">Clear</span></div>
        <div><kbd style="background:#1e293b; color:#e2e8f0; padding:2px 6px; border-radius:4px; font-weight:600;">← / P</kbd> <span style="color:#94a3b8;">Previous</span></div>
        <div><kbd style="background:#1e293b; color:#e2e8f0; padding:2px 6px; border-radius:4px; font-weight:600;">→ / N</kbd> <span style="color:#94a3b8;">Next</span></div>
      </div>
      <div style="margin-top:10px; font-size:10px; color:#64748b; text-align:right;">
        Press <kbd style="background:#07090e; color:#f59e0b; padding:1px 4px; border-radius:3px;">?</kbd> to toggle
      </div>
    `;
    document.body.appendChild(div);
    this.container = div;

    const closeBtn = div.querySelector('#clockee-hud-close');
    if (closeBtn) {
      closeBtn.onclick = () => this.hide();
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
  }

  hide() {
    if (this.container) {
      this.container.style.display = 'none';
      this.visible = false;
    }
  }
}

if (typeof window !== 'undefined') {
  window.CBTHUDOverlay = CBTHUDOverlay;
}
