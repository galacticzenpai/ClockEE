/**
 * ClockEE Physics-Based Split Drawer for Question Palette
 * Smooth sliding drawer with frosted glass styling and gesture swipe handling.
 */

class SplitDrawer {
  constructor(containerSelector, options = {}) {
    this.container = typeof containerSelector === 'string' ? document.querySelector(containerSelector) : containerSelector;
    this.options = Object.assign({
      openWidth: '340px',
      closedWidth: '0px',
      direction: 'right',
      onToggle: null
    }, options);
    this.isOpen = false;
    this.init();
  }

  init() {
    if (!this.container) return;
    this.container.style.transition = 'transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease';
    this.container.style.transform = 'translateX(100%)';
    this.container.style.backdropFilter = 'blur(16px)';
    this.container.style.backgroundColor = 'rgba(7, 9, 14, 0.92)';
    this.container.style.borderLeft = '1px solid rgba(255, 255, 255, 0.08)';
    this.container.style.boxShadow = '-8px 0 32px rgba(0, 0, 0, 0.5)';
  }

  toggle() {
    if (this.isOpen) this.close();
    else this.open();
  }

  open() {
    if (!this.container) return;
    this.container.style.transform = 'translateX(0)';
    this.container.style.opacity = '1';
    this.isOpen = true;
    if (this.options.onToggle) this.options.onToggle(true);
  }

  close() {
    if (!this.container) return;
    this.container.style.transform = 'translateX(100%)';
    this.isOpen = false;
    if (this.options.onToggle) this.options.onToggle(false);
  }

  renderQuestionGrid(totalQuestions, stateMap, onSelectQuestion) {
    if (!this.container) return;
    let grid = this.container.querySelector('.clockee-drawer-grid');
    if (!grid) {
      grid = document.createElement('div');
      grid.className = 'clockee-drawer-grid';
      grid.style.cssText = 'display:grid; grid-template-columns: repeat(5, 1fr); gap: 8px; padding: 16px; overflow-y:auto; max-height: calc(100vh - 120px);';
      this.container.appendChild(grid);
    }
    grid.innerHTML = '';

    for (let i = 1; i <= totalQuestions; i++) {
      const btn = document.createElement('button');
      btn.textContent = i;
      btn.style.cssText = `
        height: 38px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.1s ease, filter 0.1s ease;
      `;

      const status = (stateMap && stateMap[i]) || 'NOT_VISITED';
      if (status === 'ANSWERED') {
        btn.style.background = '#10b981';
        btn.style.color = '#ffffff';
      } else if (status === 'MARKED_REVIEW') {
        btn.style.background = '#8b5cf6';
        btn.style.color = '#ffffff';
      } else if (status === 'NOT_ANSWERED') {
        btn.style.background = '#ef4444';
        btn.style.color = '#ffffff';
      } else {
        btn.style.background = 'rgba(255, 255, 255, 0.04)';
        btn.style.color = '#94a3b8';
      }

      btn.onclick = () => {
        if (onSelectQuestion) onSelectQuestion(i);
      };
      grid.appendChild(btn);
    }
  }
}

if (typeof window !== 'undefined') {
  window.SplitDrawer = SplitDrawer;
}
