/**
 * ClockEE Lightweight Subject Mastery Radar Chart
 * Canvas-based hexagon / triangle radar plotter for STEM competency.
 */

class SubjectRadarChart {
  constructor(canvasElement, options = {}) {
    this.canvas = canvasElement;
    this.ctx = canvasElement.getContext('2d');
    this.options = Object.assign({
      labels: ['Physics', 'Chemistry', 'Mathematics'],
      fillColor: 'rgba(16, 185, 129, 0.2)',
      strokeColor: '#10b981',
      gridColor: 'rgba(255, 255, 255, 0.1)',
      textColor: '#94a3b8'
    }, options);
    this.resize();
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = (rect.width || 300) * dpr;
    this.canvas.height = (rect.height || 300) * dpr;
    this.ctx.scale(dpr, dpr);
    this.size = Math.min(rect.width || 300, rect.height || 300);
  }

  render(values = [80, 75, 90]) {
    const ctx = this.ctx;
    const center = this.size / 2;
    const radius = center * 0.75;
    const totalSides = this.options.labels.length;

    ctx.clearRect(0, 0, this.size, this.size);

    // Draw concentric grids
    for (let level = 1; level <= 3; level++) {
      const r = radius * (level / 3);
      ctx.beginPath();
      for (let i = 0; i < totalSides; i++) {
        const angle = (Math.PI * 2 / totalSides) * i - Math.PI / 2;
        const x = center + Math.cos(angle) * r;
        const y = center + Math.sin(angle) * r;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = this.options.gridColor;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Draw value polygon
    ctx.beginPath();
    const points = [];
    for (let i = 0; i < totalSides; i++) {
      const val = Math.min(100, Math.max(0, values[i] || 0));
      const r = radius * (val / 100);
      const angle = (Math.PI * 2 / totalSides) * i - Math.PI / 2;
      const x = center + Math.cos(angle) * r;
      const y = center + Math.sin(angle) * r;
      points.push({ x, y });
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = this.options.fillColor;
    ctx.fill();
    ctx.strokeStyle = this.options.strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw Labels
    ctx.font = '11px "JetBrains Mono", monospace';
    ctx.fillStyle = this.options.textColor;
    ctx.textAlign = 'center';
    for (let i = 0; i < totalSides; i++) {
      const angle = (Math.PI * 2 / totalSides) * i - Math.PI / 2;
      const labelX = center + Math.cos(angle) * (radius + 20);
      const labelY = center + Math.sin(angle) * (radius + 20) + 4;
      ctx.fillText(`${this.options.labels[i]}: ${values[i]}%`, labelX, labelY);
    }
  }
}

if (typeof window !== 'undefined') {
  window.SubjectRadarChart = SubjectRadarChart;
}
