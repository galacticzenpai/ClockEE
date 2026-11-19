---
name: perceptual-contrast-guard
description: Accessible Perceptual Contrast Algorithm (APCA / W3C Silver) validator ensuring dark-mode question text satisfies minimum Lc 75 contrast for 3-hour marathon exams.
---

# APCA Perceptual Contrast Validator for High-Stakes Exams

Reel: #20 (https://www.instagram.com/p/DfRBJe5R0jV/)
Package: `integrations/contrast_guard/`

## Capabilities
- Implements the Accessible Perceptual Contrast Algorithm (APCA) contrast formula.
- Verifies readability of text on dark backgrounds (#07090e, #0d111a).
- Rejects any low-contrast muted grays (< Lc 60) that cause eye fatigue during 3-hour tests.
- Benchmarked at <10µs per color pair.
