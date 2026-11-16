---
name: mcq_distractor_engine
description: Heuristic analyzer mapping incorrect MCQ distractor options to specific conceptual traps and mathematical miscalculations.
domain: Adaptive CBT Exam Engine
upstream: question-bank-distractors
reel_id: reel_012
---

# ⚡ MCQ Distractor & Misconception Analyzer (Reel #12)

Diagnostic engine classifying student mistakes into actionable cognitive traps rather than generic errors.

## Capabilities
1. **Trap Taxonomy**: Categorizes errors into Sign Inversion, Missing Factor of 2, Inverted Fraction, Formula Mismatch, and Dimensional Failure.
2. **Pedagogical Feedback**: Explains why a decoy option was attractive and how to spot it during tests.
3. **CBT Review Integration**: Powers post-exam error autopsy cards in `cbt_analysis.html`.

## CLI Usage
```bash
python integrations/distractor_engine/misconception_map.py
```
