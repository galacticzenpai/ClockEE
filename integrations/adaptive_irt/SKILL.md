---
name: irt_adaptive_sequencer
description: Item Response Theory (IRT) 3PL adaptive question sequencer dynamically adjusting exam difficulty based on student ability.
domain: Adaptive CBT Exam Engine
upstream: item-response-theory/engine
reel_id: reel_011
---

# ⚡ Item Response Theory (IRT) Adaptive Sequencer (Reel #11)

Adaptive testing engine evaluating latent ability ($\theta$) in real-time to pinpoint student mastery in 30 questions rather than 180.

## Capabilities
1. **3PL IRT Model**: Accounts for discrimination ($a$), difficulty ($b$), and guessing ($c=0.25$).
2. **Maximum Information Selection**: Dynamically selects questions that maximize Fisher Information.
3. **Bayesian EAP Theta Convergence**: Accurately estimates ability across $[-3.0, +3.0]$.
4. **Client & Server Equivalence**: Identical scoring in `integrations/adaptive_irt/irt_engine.py` and `js/adaptive_sequencer.js`.

## CLI Usage
```bash
python integrations/adaptive_irt/irt_engine.py
```
