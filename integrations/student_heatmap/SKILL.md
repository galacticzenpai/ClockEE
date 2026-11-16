---
name: student-heatmap
description: Time-spent-per-question cognitive load heatmap generator identifying time sink questions, careless rushes, and balanced pace.
---

# Time-Spent-Per-Question Cognitive Load Heatmap

Reel: #22 (https://www.instagram.com/p/DfNSFM9S38J/)
Package: `integrations/student_heatmap/`

## Capabilities
- Categorizes student question dwell time into 4 cognitive speed zones:
  - **RUSHED** (<25% of ideal time): Careless mistake risk
  - **OPTIMAL** (75% - 125% of ideal time): Sweet spot
  - **CAUTION** (125% - 200% of ideal time): Slight hesitation
  - **STUCK / TIME-SINK** (>200% of ideal time): Dangerous time loss
- Renders an interactive 2D color-coded grid for exam autopsy.
