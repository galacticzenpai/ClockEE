---
name: hallmark-design
description: Anti-AI-slop design skill and aesthetic linter adapted from Together AI's Hallmark (nutlope/hallmark). Enforces human-crafted UI layouts, responsive breakpoints, theme materials, and flags generic AI design clichés.
---

# Hallmark: Anti-AI-Slop Design Skill for ClockEE

Adapted from Together AI's open-source **Hallmark** (`nutlope/hallmark`, MIT License) by Hassan El Mghari.

## Overview
Coding assistants frequently default to an identifiable "AI slop" aesthetic:
1. Centered hero sections with glowing purple/violet gradients.
2. A single brightly colored word inside the main headline (`<span>`).
3. Three identical glassmorphism cards with generic SVG icons.
4. Uppercase tracked-out "eyebrow" labels (`text-xs font-mono uppercase tracking-widest`) above every heading.
5. Email collection boxes at the footer that display "Thanks!" without an active backend handler.
6. Fake metrics counters ("10,000+ Happy Students", "99.9% Uptime").

Hallmark replaces these predictable crutches with **purpose-driven macrostructures**, a **50-theme material catalog**, **multi-viewport responsive verification**, and an automated **slop linter (`sloplint.py`)**.

---

## The Three Quality Gates

### 1. Floor Gates (Mandatory / Blocking)
- **Viewport Meta**: Every entry point must include `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
- **Responsive Layout**: Zero horizontal overflow at any of the 8 canonical viewports:
  `[320px, 375px, 414px, 768px, 1024px, 1280px, 1440px, 1920px]`.
- **Functional Forms**: Any input/form must have a verified submit handler or local storage persistence; no dead `alert('Thanks!')` placeholders.
- **Accessible Interactive Targets**: Minimum touch target size of 44x44px on mobile devices.

### 2. Reflex Gates (Aesthetic Cliché Filters)
- **Gradient Monoculture**: Disallow cliché purple/violet/indigo radial background blobs unless explicitly specified by a chosen theme.
- **Headline Tinting**: Do not highlight a single token inside an `<h1>` with an arbitrary gradient or color span.
- **Card Grids**: Prohibit mindless 3-card layouts (`grid-cols-1 md:grid-cols-3`) when an asymmetric layout, timeline, or list conveys information better.
- **Eyebrow Inflation**: Never place an uppercase micro-label above more than one primary hero element per viewport.

### 3. Finish Checks (Advisory Polish)
- **Typography Pairing**: Contrast heading display fonts with legible body typefaces (e.g., Space Grotesk + Inter, Playfair + Newsreader, JetBrains Mono + Geist).
- **Surface Depth**: Use authentic border contrast, physical paper textures, or crisp editorial rules rather than blurry backdrop filters.
- **Data Authenticity**: Replace placeholder metrics with real domain data (e.g. JEE/NEET timing metrics, actual revision cycles, question banks).

---

## The Hallmark Workflow in ClockEE

### Mode 1: Audit an Existing Page
Run the Hallmark linter against any ClockEE page:
```powershell
python integrations/hallmark_design/hallmark_cli.py audit index.html
python integrations/hallmark_design/hallmark_cli.py audit --all
```

### Mode 2: Browse Themes
Inspect curated aesthetic themes to apply to ClockEE features (CBT Exam, Focus Timer, Mistake Notebook, Coaching Dashboard):
```powershell
python integrations/hallmark_design/hallmark_cli.py themes
```

### Mode 3: Safe Redesign (`--kept` Contract)
When redesigning a page:
1. Extract all interactive IDs, input names, form actions, and script references.
2. Select a material theme from `themes_catalog.json`.
3. Apply structural macrostructures (editorial split, asymmetric sidebar, technical workbench).
4. Verify that all functional handlers and data attributes remain 100% intact.
