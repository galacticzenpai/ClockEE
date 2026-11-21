with open('components/navbar.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Add data-nav attributes to primary navigation links
text = text.replace('href="index.html" class="nav-btn', 'href="index.html" data-nav="home" class="nav-btn')
text = text.replace('href="task.html" class="nav-btn', 'href="task.html" data-nav="task" class="nav-btn')
text = text.replace('href="today.html" class="nav-btn', 'href="today.html" data-nav="today" class="nav-btn')
text = text.replace('href="cbt_home.html" class="nav-btn', 'href="cbt_home.html" data-nav="cbt" class="nav-btn')

dock_code = """
  // Mount Universal Bottom Floating Controls Dock for UI/UX Design System
  function ensureFloatingDock() {
    if (document.getElementById('clockee-floating-dock')) return;
    const dock = document.createElement('aside');
    dock.id = 'clockee-floating-dock';
    dock.className = 'clockee-dock fixed bottom-5 right-5 z-40 flex items-center gap-2 p-1.5 rounded-full bg-slate-900/90 backdrop-blur-md border border-slate-700/60 shadow-2xl transition-all';
    dock.setAttribute('data-dock', 'bottom-right');
    dock.setAttribute('aria-label', 'System Quick Controls');
    dock.innerHTML = `
      <button id="dock-btn-palette" data-dock-action="palette" class="dock-btn flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition" title="Command Palette">
        <span class="text-[10px] opacity-60">⌘K</span>
        <span>Palette</span>
      </button>
      <button id="dock-btn-aitutor" data-dock-action="aitutor" class="dock-btn flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold text-cyan-400 hover:text-cyan-300 hover:bg-cyan-950/40 border border-cyan-500/20 transition" title="AI Tutor Assistance">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
        <span>AI Tutor</span>
      </button>
    `;
    document.body.appendChild(dock);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureFloatingDock);
  } else {
    ensureFloatingDock();
  }
"""

if 'clockee-floating-dock' not in text:
    last_brace = text.rfind('})();')
    if last_brace != -1:
        text = text[:last_brace] + dock_code + '\n' + text[last_brace:]
        print("Injected ensureFloatingDock into components/navbar.js")

with open('components/navbar.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved components/navbar.js successfully")
