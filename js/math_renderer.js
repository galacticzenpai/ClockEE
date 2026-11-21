/**
 * ClockEE OS 2.0 - Mathematical Pre-processor & LaTeX Sanitizer
 * Ensures all raw LaTeX commands are correctly wrapped in delimiters before KaTeX rendering.
 */
(function(window) {
  'use strict';

  function sanitizeMath(text) {
    if (!text || typeof text !== 'string') return '';

    let processed = text;

    // Detect naked LaTeX blocks lacking delimiters (e.g. \begin{matrix} ... \end{matrix})
    processed = processed.replace(/\\begin\{([a-zA-Z]+)\}([\s\S]*?)\\end\{\1\}/g, function(match) {
      return `$$${match}$$`;
    });

    // Detect Greek symbols & mathematical operators lacking $ delimiters
    // e.g., \rho, \int, \frac, \sqrt, \alpha, \theta, \circ
    processed = processed.replace(/(?<!\$)\\(rho|int|frac|sqrt|sum|prod|times|pm|le|ge|neq|alpha|beta|gamma|theta|mu|pi|lambda|sigma|omega|Delta|Omega|circ|oint)(?:\b|\{)([\s\S]*?)(?!\$)/g, function(match) {
      if (match.startsWith('$')) return match;
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
