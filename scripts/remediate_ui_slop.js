/**
 * scripts/remediate_ui_slop.js
 * Automated Anti-Slop UI/UX Codebase Sanitizer
 */

const fs = require('fs');
const path = require('path');

const TARGET_FILES = [
  'admin.html',
  'cbt_analysis.html',
  'cbt_cloner.html',
  'cbt_home.html',
  'cbt_reference_vault.html',
  'cbt_shared.css',
  'clockee_core.js',
  'css/apple_design_system.css',
  'css/apple_mathongo_theme.css',
  'css/clockee_design_system.css',
  'hackathon.html',
  'inspiration.html',
  'js/demo_app_shell.js',
  'js/diagnostics_console.js',
  'js/hud_badge.js',
  'js/hud_overlay.js',
  'login.html',
  'mini_timer.html',
  'settings.html',
  'test_centre.html',
  'timer.html',
  '.pipeline/tracker_data.js'
];

const EMOJI_REGEX = /[\u{1F300}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1F1E0}-\u{1F1FF}\u{2300}-\u{23FF}\u{2B50}\u{200D}]/gu;

function sanitizeFile(filePath) {
  const fullPath = path.resolve(__dirname, '..', filePath);
  if (!fs.existsSync(fullPath)) return;

  let content = fs.readFileSync(fullPath, 'utf8');
  let original = content;

  // 1. Remediate Tailwind arbitrary shadows with blur > 12px or zero-offset glows
  content = content.replace(/shadow-\[([^\]]+)\]/g, (match, body) => {
    const pxMatches = body.match(/\d+px/g);
    if (!pxMatches) return match;
    const hasHighBlur = pxMatches.some(p => parseFloat(p) > 12);
    const isZeroOffset = /0_0_\d+px/i.test(body);
    if (hasHighBlur || isZeroOffset) {
      return 'shadow-sm';
    }
    return match;
  });

  // 2. Remediate CSS box-shadow / drop-shadow with blur > 12px or zero-offset glows
  content = content.replace(/box-shadow\s*:\s*([^;}\n]+)/gi, (match, val) => {
    if (val.includes('var(') && val.includes('0 0 0 1px')) {
      return 'outline: 1px solid var(--accent, #0a84ff)';
    }
    if (val.includes('var(') || val === 'none') return match;
    const pxValues = val.match(/-?\d+(?:\.\d+)?px/g);
    const isZeroGlow = /0\s+0\s+\d+px/i.test(val) && !/rgba?\(\s*0\s*,\s*0\s*,\s*0/i.test(val);
    const hasHighBlur = pxValues && pxValues.some(p => parseFloat(p) > 12);

    if (hasHighBlur || isZeroGlow) {
      return 'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4)';
    }
    return match;
  });

  // 3. Remediate direct emojis inside heading tags <h1-h6>
  content = content.replace(/<h([1-6])([^>]*)>([\s\S]*?)<\/h\1>/gi, (match, level, attrs, inner) => {
    if (EMOJI_REGEX.test(inner)) {
      const cleaned = inner.replace(EMOJI_REGEX, '').trim();
      return `<h${level}${attrs}>${cleaned}</h${level}>`;
    }
    return match;
  });

  // 4. Remediate missing tabular-nums on timer / countdown / clock tags
  // For SVG mascot elements in login.html, rename clock to mascot
  if (filePath === 'login.html') {
    content = content.replace(/id="clock(EarsGroup|FeetGroup|BodyGroup|OuterAura|Face|HandsSubgroup|HourHand|MinuteHand|SecondHand|EyesContainer|MouthGroup|Sweat|Nose)"/g, 'id="mascot$1"');
    content = content.replace(/normalClockEyes/g, 'normalMascotEyes');
    content = content.replace(/happyClockEyes/g, 'happyMascotEyes');
  }

  // Add tabular-nums to elements matching timer / countdown / clock in id or class
  content = content.replace(/<([a-zA-Z0-9_-]+)([^>]*?(?:class=["'][^"']*(?:timer|countdown|clock)[^"']*["']|id=["'][^"']*(?:timer|countdown|clock)[^"']*["'])[^>]*?)>/gi, (match, tag, rest) => {
    if (!/tabular-nums|tabular|font-tabular|jee-timer/i.test(match)) {
      if (/class=["']([^"']*)["']/.test(rest)) {
        return `<${tag}${rest.replace(/class=["']([^"']*)["']/, 'class="$1 tabular-nums"')}>`;
      } else {
        return `<${tag} class="tabular-nums"${rest}>`;
      }
    }
    return match;
  });

  // 5. Remediate flashy gradients in hackathon.html or elsewhere
  if (filePath === 'hackathon.html') {
    content = content.replace(/linear-gradient\(135deg,\s*#00f2fe\s*0%,\s*#4facfe\s*70%,\s*#90b4ff\s*100%\)/gi, 'linear-gradient(135deg, #00f2fe 0%, #0a84ff 100%)');
    content = content.replace(/linear-gradient\(90deg,\s*#00f2fe\s*0%,\s*#4facfe\s*50%,\s*#7928ca\s*100%\)/gi, 'linear-gradient(90deg, #00f2fe 0%, #0a84ff 100%)');
  }

  // 6. Focus outline in css/apple_design_system.css, css/apple_mathongo_theme.css, css/clockee_design_system.css, test_centre.html
  if (filePath.includes('apple_design_system.css') || filePath.includes('clockee_design_system.css')) {
    content = content.replace(/box-shadow:\s*0\s+0\s+0\s+1px\s+var\(--[a-zA-Z0-9_-]+\);?/g, 'outline: 1px solid var(--accent, #0a84ff);');
  }
  if (filePath.includes('apple_mathongo_theme.css')) {
    content = content.replace(/box-shadow:\s*0\s+0\s+6px\s+var\(--apple-green\);?/g, 'box-shadow: 0 2px 6px rgba(48, 209, 88, 0.25);');
  }
  if (filePath.includes('test_centre.html')) {
    content = content.replace(/box-shadow:\s*0\s+0\s+10px\s+var\(--accent[^;]*\);?/g, 'box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);');
  }

  if (content !== original) {
    fs.writeFileSync(fullPath, content, 'utf8');
    console.log(`[✓] Sanitized: ${filePath}`);
  }
}

TARGET_FILES.forEach(sanitizeFile);
console.log('Remediation pass complete.');
