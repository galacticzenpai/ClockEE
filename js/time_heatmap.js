/**
 * ClockEE Cognitive Load Time Heatmap
 * Visualizes student dwell time vs ideal question allocation.
 */

class CognitiveTimeHeatmap {
  constructor(targetElement, questionsData = []) {
    this.target = typeof targetElement === 'string' ? document.querySelector(targetElement) : targetElement;
    this.data = questionsData;
  }

  classifyPace(spentSec, idealSec = 120) {
    const ratio = spentSec / idealSec;
    if (ratio < 0.3) return { label: 'Rushed', color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.15)', border: '#0284c7' };
    if (ratio <= 1.25) return { label: 'Optimal', color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)', border: '#059669' };
    if (ratio <= 2.0) return { label: 'Slow', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)', border: '#d97706' };
    return { label: 'Stuck', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.18)', border: '#dc2626' };
  }

  render() {
    if (!this.target) return;
    this.target.innerHTML = '';
    
    const container = document.createElement('div');
    container.style.cssText = 'display:grid; grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); gap: 8px; font-family: "JetBrains Mono", monospace;';

    this.data.forEach((q, idx) => {
      const pace = this.classifyPace(q.spentSec || 0, q.idealSec || 120);
      const card = document.createElement('div');
      card.style.cssText = `
        padding: 8px 4px;
        border-radius: 6px;
        background: \${pace.bg};
        border: 1px solid \${pace.border};
        text-align: center;
        cursor: pointer;
        transition: transform 0.15s ease;
      `;
      card.title = `Q#\${idx + 1}: \${q.spentSec || 0}s (Ideal: \${q.idealSec || 120}s) - \${pace.label}`;
      card.innerHTML = `
        <div style="font-size: 11px; color: #94a3b8;">Q\${idx + 1}</div>
        <div style="font-size: 13px; font-weight: 700; color: \${pace.color};">\${q.spentSec || 0}s</div>
      `;
      card.onmouseenter = () => card.style.transform = 'translateY(-2px)';
      card.onmouseleave = () => card.style.transform = 'translateY(0)';
      container.appendChild(card);
    });

    this.target.appendChild(container);
  }
}

if (typeof window !== 'undefined') {
  window.CognitiveTimeHeatmap = CognitiveTimeHeatmap;
}
