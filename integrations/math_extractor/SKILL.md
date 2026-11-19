---
name: latex_math_extractor
description: Deterministic STEM parser extracting and validating LaTeX formulas and organic chemistry equations with KaTeX compatibility.
domain: STEM Question Extraction
upstream: KaTeX/math-extractor
reel_id: reel_009
---

# ⚡ KaTeX LaTeX Math & Chemical Formula Parser (Reel #9)

High-fidelity STEM formula extractor and KaTeX rendering helper for JEE Advanced test questions.

## Capabilities
1. **Formula Tokenization**: Accurately isolates inline math (`$...$`, `\(...\)`) and display blocks (`$$...$$`, `\[...\]`).
2. **Syntax Validation**: Ensures balanced brackets and symbol hygiene before sending to browser rendering.
3. **KaTeX Helper**: Auto-renders formulas in `.question-text`, `.option-text`, and solution blocks via `js/katex_render_helper.js`.
4. **NTA-Style Symbol Support**: Full support for calculus, linear algebra, electromagnetism, and organic chemistry notation.

## CLI Usage
```bash
python integrations/math_extractor/formula_parser.py
```
