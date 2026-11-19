/**
 * ⚡ ClockEE — Reel #9: Client-Side KaTeX Render Helper (js/katex_render_helper.js)
 * Automatically scans elements and renders inline ($...$) and block ($$...$$) KaTeX math.
 */

(function(window) {
  'use strict';

  function renderMathInElement(elem) {
    if (!elem || typeof window.katex === 'undefined') return;

    const html = elem.innerHTML;
    // Replace block formulas $$...$$
    let processed = html.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
      try {
        return window.katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
      } catch (e) {
        return match;
      }
    });

    // Replace inline formulas $...$
    processed = processed.replace(/\$([^\$\n]+?)\$/g, (match, formula) => {
      try {
        return window.katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {
        return match;
      }
    });

    if (processed !== html) {
      elem.innerHTML = processed;
    }
  }

  function autoRenderAllMath(selector = '.math-renderable, .question-text, .option-text, .solution-content') {
    document.querySelectorAll(selector).forEach(renderMathInElement);
  }

  // Auto-initialize when KaTeX is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => autoRenderAllMath());
  } else {
    autoRenderAllMath();
  }

  window.ClockEEMath = {
    render: renderMathInElement,
    autoRender: autoRenderAllMath
  };

})(typeof window !== 'undefined' ? window : this);
