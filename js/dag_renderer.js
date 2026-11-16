/**
 * ClockEE Syllabus DAG Knowledge Graph Renderer
 * Interactive hierarchical node graph with Hallmark dark styling.
 */

class SyllabusDAGRenderer {
  constructor(containerElement, dagData) {
    this.container = typeof containerElement === 'string' ? document.querySelector(containerElement) : containerElement;
    this.data = dagData;
    this.completedNodes = new Set(JSON.parse(localStorage.getItem('clockee_completed_nodes') || '["phy_kinematics", "chem_mole", "math_sets"]'));
  }

  render() {
    if (!this.container || !this.data) return;
    this.container.innerHTML = '';

    const subjects = ['Physics', 'Chemistry', 'Mathematics'];
    subjects.forEach(sub => {
      const subNodes = this.data.nodes.filter(n => n.subject === sub);
      const section = document.createElement('div');
      section.style.cssText = 'margin-bottom: 24px; background: rgba(13, 17, 26, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 18px;';
      
      const title = document.createElement('h3');
      title.textContent = sub;
      title.style.cssText = 'font-size: 14px; font-weight: 700; color: #f59e0b; font-family: "JetBrains Mono", monospace; text-transform: uppercase; margin-bottom: 14px; display:flex; align-items:center; gap:8px;';
      title.innerHTML = `<span style="width:8px; height:8px; border-radius:50%; background:#f59e0b;"></span> \${sub} Mastery Tree`;
      section.appendChild(title);

      const grid = document.createElement('div');
      grid.style.cssText = 'display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px;';

      subNodes.forEach(node => {
        const isCompleted = this.completedNodes.has(node.id);
        const prereqsMet = node.prereqs.every(p => this.completedNodes.has(p));
        const status = isCompleted ? 'COMPLETED' : (prereqsMet ? 'UNLOCKED' : 'LOCKED');

        const card = document.createElement('div');
        card.style.cssText = `
          padding: 12px 14px;
          border-radius: 8px;
          border: 1px solid \${isCompleted ? 'rgba(16, 185, 129, 0.4)' : (prereqsMet ? 'rgba(56, 189, 248, 0.4)' : 'rgba(255, 255, 255, 0.05)')};
          background: \${isCompleted ? 'rgba(16, 185, 129, 0.08)' : (prereqsMet ? 'rgba(56, 189, 248, 0.08)' : 'rgba(255, 255, 255, 0.02)')};
          color: \${prereqsMet || isCompleted ? '#f8fafc' : '#64748b'};
          font-family: 'Inter', sans-serif;
          font-size: 12px;
          cursor: \${prereqsMet ? 'pointer' : 'not-allowed'};
          transition: transform 0.15s ease;
        `;
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-family:'JetBrains Mono', monospace; font-size:10px; color:\${isCompleted ? '#10b981' : (prereqsMet ? '#38bdf8' : '#64748b')}; font-weight:700;">\${status}</span>
            <span style="font-size:10px; color:#64748b;">Tier \${node.level}</span>
          </div>
          <div style="font-weight:600; font-size:13px;">\${node.name}</div>
          \${node.prereqs.length > 0 ? `<div style="font-size:10px; color:#94a3b8; margin-top:4px;">Requires: \${node.prereqs.join(', ')}</div>` : ''}
        `;
        grid.appendChild(card);
      });

      section.appendChild(grid);
      this.container.appendChild(section);
    });
  }
}

if (typeof window !== 'undefined') {
  window.SyllabusDAGRenderer = SyllabusDAGRenderer;
}
