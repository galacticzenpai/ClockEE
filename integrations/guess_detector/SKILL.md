---
name: guess-detector
description: Statistical fluke and lucky guess detection engine distinguishing genuine cognitive mastery from blind rapid guesses based on difficulty, response latency, and option selection entropy.
---

# Blind Guess & Statistical Fluke Detection Engine

Reel: #23 (https://www.instagram.com/p/DfIijXSzzaO/)
Package: `integrations/guess_detector/`

## Capabilities
- Computes mastery confidence scores (0.0 to 1.0) for every correct answer.
- Flags suspicious correct answers answered in <12 seconds on Tough/Advanced multi-step problems.
- Provides a calibrated 'True Skill Score' free of lucky random guessing artifacts.
- Benchmarked at <5µs per question assessment.
