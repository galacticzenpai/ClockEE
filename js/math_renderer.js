/**
 * ClockEE OS 2.0 - Mathematical Pre-processor & LaTeX Sanitizer
 * Ensures all raw LaTeX commands are correctly wrapped in delimiters before KaTeX rendering.
 */
(function(window) {
  'use strict';

  function sanitizeMath(text) {
    if (!text || typeof text !== 'string') return '';

    // If text already has well-formed dollar delimiters, return as-is
    let processed = text;

    // Detect naked LaTeX blocks lacking delimiters (e.g. \begin{matrix} ... \end{matrix})
    processed = processed.replace(/\\begin\{([a-zA-Z]+)\}([\s\S]*?)\\end\{\1\}/g, function(match) {
      return `$$${match}$$`;
    });

    // Detect standalone unescaped mathematical fractions e.g. \frac{a}{b} not already inside $ or $$
    // If not enclosed in $, wrap it
    processed = processed.replace(/(?<!\$)\\(frac|sqrt|int|sum|prod|times|pm|le|ge|neq|alpha|beta|gamma|theta|mu|pi|lambda|sigma|omega|Delta|Omega)\{([^}]+)\}(?!\$)/g, function(match) {
      return `$${match}$`;
    });

    return processed;
  }

  function renderMathSafely(element, options) {
    if (!element || typeof renderMathInElement !== 'function') return;

    const defaultOpts = {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
        { left: '\\(', right: '\\)', display: false },
        { left: '\\[', right: '\\]', display: true }
      ],
      throwOnError: false,
      errorColor: '#ef4444'
    };

    const finalOpts = Object.assign({}, defaultOpts, options || {});
    try {
      renderMathInElement(element, finalOpts);
    } catch (e) {
      console.warn('[KaTeX Sanitizer] Math rendering encountered a non-fatal error:', e);
    }
  }

  window.ClockEEMath = {
    sanitize: sanitizeMath,
    render: renderMathSafely
  };
})(window);
