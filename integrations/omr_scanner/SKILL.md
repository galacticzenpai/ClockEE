---
name: omr-scanner
description: High-accuracy optical mark recognition (OMR) scanner for physical answer sheet digitization with sub-millisecond grading latency.
---

# Physical OMR Bubble Sheet Optical Scanner

Reel: #13 (https://www.instagram.com/p/DerbBtfzj8p/)
Package: `integrations/omr_scanner/`

## Capabilities
- Detects marked bubbles across standard 4-option MCQs (A, B, C, D).
- Distinguishes between valid single marks, unattempted questions, and invalid double-marks.
- Sub-millisecond execution (<1ms per 10 questions) for zero-lag offline grading.
- Compatible with ClockEE hybrid offline-to-digital practice workflow.

## Usage
```python
from integrations.omr_scanner.scanner import OMRScanner

scanner = OMRScanner(num_questions=10)
# Grade bubble intensity matrix
results = scanner.grade(intensity_matrix, answer_key)
print(results)
```
