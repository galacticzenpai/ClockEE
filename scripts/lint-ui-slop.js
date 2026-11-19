#!/usr/bin/env node

/**
 * JEE Educational Platform - Anti-Slop UI/UX Static Analysis Linter
 * Enforces zero-distraction, authentic NTA exam standards, and cognitive ergonomics.
 *
 * Rules Enforced:
 * 1. [BOX_SHADOW_SLOP]: Box-shadow blur > 12px or neon glow spread is forbidden.
 * 2. [GRADIENT_SLOP]: Multi-hue flashy / web3 gradients are forbidden.
 * 3. [EMOJI_HEADING_SLOP]: Emojis inside headings (h1-h6) are strictly forbidden.
 * 4. [TIMER_TABULAR_NUMS]: All countdowns/timers must enforce `tabular-nums`.
 */

const fs = require('fs');
const path = require('path');

const IGNORED_DIRS = new Set([
  'node_modules',
  '.git',
  '.next',
  'dist',
  'build',
  '.turbo',
  '.system_generated',
  'brain',
  'mesh',
  'scripts',
  'test',
  'tests',
  '__tests__'
]);

const SUPPORTED_EXTENSIONS = new Set([
  '.css',
  '.scss',
  '.less',
  '.html',
  '.htm',
  '.js',
  '.jsx',
  '.ts',
  '.tsx',
  '.vue',
  '.svelte'
]);

// ANSI styling for CLI output
const ANSI = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  dim: '\x1b[2m'
};

const violations = [];

/**
 * Recursively scans directory for target files
 */
function walkDirectory(targetPath, fileList = []) {
  if (!fs.existsSync(targetPath)) return fileList;

  const stat = fs.statSync(targetPath);
  if (stat.isFile()) {
    if (SUPPORTED_EXTENSIONS.has(path.extname(targetPath).toLowerCase())) {
      fileList.push(targetPath);
    }
    return fileList;
  }

  const entries = fs.readdirSync(targetPath, { withFileTypes: true });
  for (const entry of entries) {
    if (IGNORED_DIRS.has(entry.name)) continue;

    const fullPath = path.join(targetPath, entry.name);
    if (entry.isDirectory()) {
      walkDirectory(fullPath, fileList);
    } else if (entry.isFile() && SUPPORTED_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

/**
 * Strips comments from content while preserving line breaks to keep line numbers accurate
 */
function stripComments(content, ext) {
  if (['.html', '.htm'].includes(ext)) {
    return content.replace(/<!--[\s\S]*?-->/g, match => '\n'.repeat((match.match(/\n/g) || []).length));
  }
  // For CSS, JS, TS, etc.
  return content
    .replace(/\/\*[\s\S]*?\*\//g, match => '\n'.repeat((match.match(/\n/g) || []).length))
    .replace(/(^|[^:])\/\/[^\n]*/g, '$1');
}

/**
 * Splits top-level commas outside of parentheses
 */
function splitTopLevelCommas(str) {
  const parts = [];
  let current = '';
  let parenDepth = 0;

  for (let i = 0; i < str.length; i++) {
    const char = str[i];
    if (char === '(') parenDepth++;
    else if (char === ')') parenDepth = Math.max(0, parenDepth - 1);

    if (char === ',' && parenDepth === 0) {
      parts.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  if (current.trim().length > 0) {
    parts.push(current.trim());
  }
  return parts;
}

/**
 * Rule 1: Box-shadow blur > 12px or neon glow spread
 */
function checkShadowSlop(filePath, cleanContent, rawContent) {
  const shadowRegex = /(?:box-shadow|drop-shadow)\s*:\s*([^;}\n]+)/gi;
  let match;

  while ((match = shadowRegex.exec(cleanContent)) !== null) {
    const rawVal = match[1].trim();
    if (rawVal === 'none' || rawVal === 'inherit' || rawVal === 'initial' || rawVal.startsWith('var(')) continue;

    // Check pixel blur values
    const pxValues = rawVal.match(/-?\d+(?:\.\d+)?px/g);
    if (pxValues) {
      for (const val of pxValues) {
        const num = parseFloat(val);
        if (num > 12) {
          const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
          violations.push({
            file: filePath,
            line: lineIndex,
            rule: 'BOX_SHADOW_SLOP',
            severity: 'ERROR',
            snippet: match[0].trim(),
            message: `Box-shadow blur radius (${val}) exceeds the 12px maximum limit. High blur creates distracting visual mud. Use crisp, high-focus borders instead.`
          });
          break;
        }
      }
    }

    // Neon zero-offset glow check: e.g., 0 0 [num]px [vibrant color]
    if (/0\s+0\s+\d+px/i.test(rawVal) && !/rgba?\(\s*0\s*,\s*0\s*,\s*0/i.test(rawVal)) {
      const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
      violations.push({
        file: filePath,
        line: lineIndex,
        rule: 'NEON_GLOW_SLOP',
        severity: 'ERROR',
        snippet: match[0].trim(),
        message: 'Zero-offset neon glow spread detected. The JEE platform mandates zero-glare, eye-strain-free dark matte surfaces.'
      });
    }
  }

  // Tailwind arbitrary shadow detection: e.g., shadow-[0_0_20px_...]
  const tailwindShadowRegex = /shadow-\[([^\]]+)\]/g;
  while ((match = tailwindShadowRegex.exec(cleanContent)) !== null) {
    const body = match[1];
    const pxValues = body.match(/\d+px/g);
    if (pxValues) {
      for (const val of pxValues) {
        if (parseFloat(val) > 12) {
          const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
          violations.push({
            file: filePath,
            line: lineIndex,
            rule: 'BOX_SHADOW_SLOP',
            severity: 'ERROR',
            snippet: match[0],
            message: `Tailwind arbitrary shadow (${match[0]}) has blur > 12px (${val}). Enforce standard crisp elevation tokens.`
          });
          break;
        }
      }
    }
  }
}

/**
 * Rule 2: Multi-hue flashy / rainbow / web3 gradients
 */
function checkGradientSlop(filePath, cleanContent) {
  const gradientRegex = /(?:linear|radial|conic)-gradient\s*\(([\s\S]*?)\)/gi;
  let match;

  const flashyKeywords = ['#ff00', '#00ff', '#f0f', '#0ff', 'magenta', 'cyan', 'lime', 'deeppink', 'fuchsia', 'violet'];

  while ((match = gradientRegex.exec(cleanContent)) !== null) {
    const body = match[1].toLowerCase().replace(/\s+/g, ' ');
    const stops = splitTopLevelCommas(body);

    // If gradient is simply a grid background e.g. radial-gradient(rgba(...) 1px, transparent 1px), skip
    if (stops.length <= 2 && (body.includes('transparent') || body.includes('1px'))) {
      continue;
    }

    const hasVibrantContrast = flashyKeywords.filter(k => body.includes(k)).length >= 2;
    // More than 3 color stops (rainbow gradient slop)
    if (stops.length > 3 || hasVibrantContrast) {
      const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
      violations.push({
        file: filePath,
        line: lineIndex,
        rule: 'GRADIENT_SLOP',
        severity: 'ERROR',
        snippet: match[0].slice(0, 60) + '...',
        message: 'Flashy multi-hue / vibrant gradient detected. The JEE UI requires distraction-free matte solids or subtle monochromatic tone shifts.'
      });
    }
  }
}

/**
 * Rule 3: Emojis directly inside HTML headings
 */
function checkEmojiInHeadings(filePath, cleanContent, lines) {
  const emojiRegex = /[\u{1F300}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1F1E0}-\u{1F1FF}]/u;

  // HTML & JSX heading tags: <h1>...</h1> through <h6>...</h6>
  const headingTagRegex = /<h([1-6])(?:\s+[^>]*)?>([\s\S]*?)<\/h\1>/gi;
  let match;

  while ((match = headingTagRegex.exec(cleanContent)) !== null) {
    const headingContent = match[2];
    if (emojiRegex.test(headingContent)) {
      const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
      violations.push({
        file: filePath,
        line: lineIndex,
        rule: 'EMOJI_HEADING_SLOP',
        severity: 'ERROR',
        snippet: match[0].replace(/\s+/g, ' ').slice(0, 60),
        message: 'Direct emoji found inside heading tag (<h' + match[1] + '>). Keep academic headings serious and uncluttered; use semantic SVG icons or badges if necessary.'
      });
    }
  }

  // Markdown headings: # Heading with emoji
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^#{1,6}\s+/.test(line) && emojiRegex.test(line)) {
      violations.push({
        file: filePath,
        line: i + 1,
        rule: 'EMOJI_HEADING_SLOP',
        severity: 'ERROR',
        snippet: line.trim(),
        message: 'Markdown heading contains an emoji. Headings must remain professional and distraction-free.'
      });
    }
  }
}

/**
 * Rule 4: Countdown timers missing tabular-nums
 */
function checkTimerTabularNums(filePath, cleanContent) {
  const ext = path.extname(filePath).toLowerCase();

  // In CSS files: check selectors that style timers or countdowns
  if (['.css', '.scss', '.less'].includes(ext)) {
    const timerBlockRegex = /([^{}]*(?:timer|countdown|clock)[^{}]*)\{([^}]+)\}/gi;
    let match;
    while ((match = timerBlockRegex.exec(cleanContent)) !== null) {
      const selector = match[1].trim();
      const body = match[2];

      if (selector.includes('@keyframes') || selector.includes('animation') || selector.includes('transition')) continue;

      const hasTabularNums = /tabular-nums/i.test(body) || /"tnum"/i.test(body);
      if (!hasTabularNums) {
        const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
        violations.push({
          file: filePath,
          line: lineIndex,
          rule: 'TIMER_TABULAR_NUMS',
          severity: 'ERROR',
          snippet: `${selector} { ... }`,
          message: `Timer selector "${selector}" is missing "font-variant-numeric: tabular-nums;". Numbers will shift and cause layout jitter as the countdown runs.`
        });
      }
    }
  }

  // In HTML / JSX / TSX / Vue / Svelte: check elements with timer / countdown in class or id
  if (['.html', '.htm', '.jsx', '.tsx', '.vue', '.svelte'].includes(ext)) {
    const timerElemRegex = /<([a-zA-Z0-9_-]+)[^>]*(?:class(?:Name)?=["'][^"']*(?:timer|countdown|clock)[^"']*["']|id=["'][^"']*(?:timer|countdown|clock)[^"']*["'])[^>]*>/gi;
    let match;
    while ((match = timerElemRegex.exec(cleanContent)) !== null) {
      const tagStr = match[0];
      const hasTabularClass = /tabular-nums|font-tabular|jee-timer/i.test(tagStr);
      const hasTabularStyle = /tabular-nums/i.test(tagStr);

      if (!hasTabularClass && !hasTabularStyle) {
        const lineIndex = cleanContent.slice(0, match.index).split('\n').length;
        violations.push({
          file: filePath,
          line: lineIndex,
          rule: 'TIMER_TABULAR_NUMS',
          severity: 'WARNING',
          snippet: tagStr.replace(/\s+/g, ' ').slice(0, 70),
          message: 'Timer / Countdown component element is missing tabular-nums utility class or inline styling. Ensure monospace or tabular-nums is applied.'
        });
      }
    }
  }
}

/**
 * Main execution
 */
function runLinter() {
  const targetPath = process.argv[2] ? path.resolve(process.argv[2]) : process.cwd();

  console.log(`\n${ANSI.bold}${ANSI.cyan}=== JEE Educational Platform: Anti-Slop UI/UX Linter ===${ANSI.reset}`);
  console.log(`${ANSI.dim}Scanning target: ${targetPath}${ANSI.reset}\n`);

  const files = walkDirectory(targetPath);

  if (files.length === 0) {
    console.log(`${ANSI.yellow}No supported UI files found in target path.${ANSI.reset}\n`);
    process.exit(0);
  }

  let errorCount = 0;
  let warningCount = 0;

  for (const file of files) {
    const rawContent = fs.readFileSync(file, 'utf8');
    const ext = path.extname(file).toLowerCase();
    const cleanContent = stripComments(rawContent, ext);
    const lines = cleanContent.split('\n');

    checkShadowSlop(file, cleanContent, rawContent);
    checkGradientSlop(file, cleanContent);
    checkEmojiInHeadings(file, cleanContent, lines);
    checkTimerTabularNums(file, cleanContent);
  }

  // Report results
  if (violations.length === 0) {
    console.log(`${ANSI.bold}${ANSI.green}✓ [PASS] All ${files.length} UI files adhere strictly to the Anti-Slop Design Rubric.${ANSI.reset}`);
    console.log(`${ANSI.dim}  • Zero neon glow spreads detected.`);
    console.log(`  • Zero multi-hue flashy gradients.`);
    console.log(`  • Zero emoji slop in academic headings.`);
    console.log(`  • Tabular alignment verified for countdowns.${ANSI.reset}\n`);
    process.exit(0);
  } else {
    console.log(`${ANSI.bold}${ANSI.red}✗ [FAIL] Found ${violations.length} UI/UX violation(s) across ${files.length} files:${ANSI.reset}\n`);

    violations.forEach((v, idx) => {
      const relPath = path.relative(process.cwd(), v.file);
      const isErr = v.severity === 'ERROR';
      if (isErr) errorCount++; else warningCount++;

      console.log(`${idx + 1}. [${isErr ? ANSI.red : ANSI.yellow}${v.rule}${ANSI.reset}] ${ANSI.bold}${relPath}:${v.line}${ANSI.reset}`);
      console.log(`   ${ANSI.dim}Snippet: ${v.snippet}${ANSI.reset}`);
      console.log(`   ${v.message}\n`);
    });

    console.log(`${ANSI.bold}Summary:${ANSI.reset} ${errorCount} Errors, ${warningCount} Warnings.\n`);
    process.exit(errorCount > 0 ? 1 : 0);
  }
}

runLinter();
