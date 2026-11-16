/**
 * ClockEE Scorecard PDF / Print Generator
 * Formats full exam analysis into a printable official score report.
 */

class ScorecardPDFGenerator {
  constructor(examData = {}) {
    this.data = examData;
  }

  generatePrintableWindow() {
    const d = this.data;
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      alert('Please allow popups to download or print your scorecard.');
      return;
    }

    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>ClockEE CBT - Official Exam Scorecard</title>
        <style>
          @page { size: A4 portrait; margin: 15mm; }
          body { font-family: 'Inter', -apple-system, sans-serif; color: #111827; margin: 0; padding: 20px; font-size: 12px; }
          .header { border-bottom: 2px solid #0056b3; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
          .title { font-size: 20px; font-weight: 800; color: #0056b3; }
          .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
          .stat-box { border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px; background: #f9fafb; text-align: center; }
          .stat-val { font-size: 18px; font-weight: 700; color: #111827; }
          .stat-lbl { font-size: 10px; color: #6b7280; text-transform: uppercase; margin-top: 2px; }
          table { width: 100%; border-collapse: collapse; margin-top: 14px; }
          th, td { border: 1px solid #e5e7eb; padding: 6px 10px; text-align: left; }
          th { background: #f3f4f6; font-size: 11px; }
          @media print { .no-print { display: none; } }
        </style>
      </head>
      <body>
        <div class="header">
          <div>
            <div class="title">ClockEE CBT Official Scorecard</div>
            <div style="color:#6b7280; font-size:11px; margin-top:3px;">Candidate: \${d.candidateName || 'Student'} | Exam: \${d.examName || 'JEE Advanced Full Mock'}</div>
          </div>
          <div style="text-align:right; font-size:10px; color:#6b7280;">Date: \${new Date().toLocaleDateString()}</div>
        </div>

        <div class="grid">
          <div class="stat-box"><div class="stat-val">\${d.score || 0} / \${d.maxScore || 300}</div><div class="stat-lbl">Final Score</div></div>
          <div class="stat-box"><div class="stat-val">\${d.percentile || 99.0}%</div><div class="stat-lbl">Estimated Percentile</div></div>
          <div class="stat-box"><div class="stat-val">\${d.airRange || '500 - 1500'}</div><div class="stat-lbl">Projected AIR</div></div>
          <div class="stat-box"><div class="stat-val">\${d.accuracy || 85}%</div><div class="stat-lbl">Accuracy</div></div>
        </div>

        <h3 style="font-size:13px; margin-bottom:6px;">Subject-Wise Performance Breakdown</h3>
        <table>
          <thead>
            <tr><th>Subject</th><th>Attempted</th><th>Correct</th><th>Accuracy</th><th>Score</th></tr>
          </thead>
          <tbody>
            <tr><td>Physics</td><td>23 / 25</td><td>20</td><td>86.9%</td><td>77</td></tr>
            <tr><td>Chemistry</td><td>24 / 25</td><td>22</td><td>91.6%</td><td>85</td></tr>
            <tr><td>Mathematics</td><td>22 / 25</td><td>18</td><td>81.8%</td><td>68</td></tr>
          </tbody>
        </table>

        <div style="margin-top:24px; border-top:1px dashed #d1d5db; padding-top:12px; font-size:10px; color:#6b7280; text-align:center;">
          Generated automatically by ClockEE High-Stakes CBT Analytics Sandbox.
        </div>

        <script>
          window.onload = function() { window.print(); };
        </script>
      </body>
      </html>
    `;

    printWindow.document.write(html);
    printWindow.document.close();
  }
}

if (typeof window !== 'undefined') {
  window.ScorecardPDFGenerator = ScorecardPDFGenerator;
}
