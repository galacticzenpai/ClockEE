/**
 * ClockEE OS 2.0 - Mathematical Pre-processor & LaTeX Sanitizer
 * Ensures all raw LaTeX commands are correctly wrapped in delimiters before KaTeX rendering.
 */
(function(window) {
  'use strict';

  function sanitizeMath(text) {
    if (!text || typeof text !== 'string') return '';

    // Split text into tokens: math blocks ($$...$$, $...$, \(...\), \[...\]) and non-math segments.
    // We only sanitize/wrap naked LaTeX commands that exist outside existing math delimiters!
    const mathPattern = /(\$\$[\s\S]*?\$\$|\$[^\$]+?\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g;
    const parts = text.split(mathPattern);

    return parts.map(part => {
      if (!part) return '';
      // If this part is already a delimited math block, preserve it intact without touching inner commands
      if (
        (part.startsWith('$$') && part.endsWith('$$')) ||
        (part.startsWith('$') && part.endsWith('$')) ||
        (part.startsWith('\\[') && part.endsWith('\\]')) ||
        (part.startsWith('\\(') && part.endsWith('\\)'))
      ) {
        return part;
      }

      let processed = part;

      // Detect naked LaTeX environments lacking delimiters (e.g. \begin{matrix} ... \end{matrix})
      processed = processed.replace(/\\begin\{([a-zA-Z]+)\}([\s\S]*?)\\end\{\1\}/g, function(match) {
        return `$$${match}$$`;
      });

      // Detect naked Greek symbols & mathematical operators lacking $ delimiters in plain text
      // e.g., \rho, \int, \frac{a}{b}, \sqrt{x}, \alpha, \theta, \circ
      processed = processed.replace(/\\(rho|int|frac|sqrt|sum|prod|times|pm|le|ge|neq|alpha|beta|gamma|theta|mu|pi|lambda|sigma|omega|Delta|Omega|circ|oint)(?:\b|\{)([\s\S]*?)(?=[,\s\.\?!]|$)/g, function(match) {
        return `$${match}$`;
      });

      return processed;
    }).join('');
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
