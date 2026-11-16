---
name: auto-repair-dom
description: MutationObserver-based runtime protector catching missing DOM targets, detached buttons, or unhandled events and healing them gracefully during CBT testing.
---

# Self-Healing DOM Selector & Missing Attribute Guardrail

Reel: #27 (https://www.instagram.com/p/DfWwN89hmY1/)
Package: `integrations/auto_repair/`

## Capabilities
- Protects against UI crashes caused by missing containers, dynamic DOM re-renders, or missing attributes.
- Self-heals question options, save buttons, and palette containers dynamically.
- Catches unhandled JavaScript runtime rejections without interrupting active timer countdowns.
