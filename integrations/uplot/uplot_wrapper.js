/**
 * ClockEE 60FPS Retina Canvas Chart Engine
 * Lightweight, zero-dependency time-series renderer for CBT telemetry.
 */

class RetinaChartEngine {
  constructor(canvasElement, options = {}) {
    this.canvas = canvasElement;
    this.ctx = canvasElement.getContext('2d');
    this.options = Object.assign({
      lineColor: '#f59e0b',
      fillColor: 'rgba(245, 158, 11, 0.08)',
      gridColor: 'rgba(255, 255, 255, 0.05)',
      textColor: '#94a3b8',
      pointColor: '#fbbf24',
      padding: { top: 20, right: 20, bottom: 30, left: 40 }
    }, options);
    this.resize();
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = (rect.width || 600) * dpr;
    this.canvas.height = (rect.height || 260) * dpr;
    this.ctx.scale(dpr, dpr);
    this.width = rect.width || 600;
    this.height = rect.height || 260;
  }

  render(xData, yData, yLabel = '') {
    if (!xData || !yData || xData.length === 0) return;
    const ctx = this.ctx;
    const { top, right, bottom, left } = this.options.padding;
    const w = this.width - left - right;
    const h = this.height - top - bottom;

    ctx.clearRect(0, 0, this.width, this.height);

    // Compute min / max
    const minY = 0;
    const maxY = Math.max(...yData, 100);

    // Grid lines
    ctx.strokeStyle = this.options.gridColor;
    ctx.lineWidth = 1;
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillStyle = this.options.textColor;
    ctx.textAlign = 'right';

    const steps = 4;
    for (let i = 0; i <= steps; i++) {
      const val = Math.round(minY + (maxY - minY) * (i / steps));
      const y = top + h - (i / steps) * h;
      ctx.beginPath();
      ctx.moveTo(left, y);
      ctx.lineTo(left + w, y);
      ctx.stroke();
      ctx.fillText(`${val}`, left - 8, y + 3);
    }

    // Line Path
    ctx.beginPath();
    const points = [];
    for (let i = 0; i < xData.length; i++) {
      const x = left + (i / (xData.length - 1 || 1)) * w;
      const y = top + h - ((yData[i] - minY) / (maxY - minY)) * h;
      points.push({ x, y });
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    // Stroke
    ctx.strokeStyle = this.options.lineColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Fill gradient
    if (points.length > 0) {
      const grad = ctx.createLinearGradient(0, top, 0, top + h);
      grad.addColorStop(0, this.options.fillColor);
      grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let pt of points) ctx.lineTo(pt.x, pt.y);
      ctx.lineTo(points[points.length - 1].x, top + h);
      ctx.lineTo(points[0].x, top + h);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
    }

    // Draw last point pulse
    if (points.length > 0) {
      const last = points[points.length - 1];
      ctx.fillStyle = this.options.pointColor;
      ctx.beginPath();
      ctx.arc(last.x, last.y, 4, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

if (typeof window !== 'undefined') {
  window.RetinaChartEngine = RetinaChartEngine;
}
