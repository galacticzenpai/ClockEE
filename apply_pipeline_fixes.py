import re

# 1. Update index.html line 663: replace w-[420px] max-w-[95vw] with responsive w-full sm:w-[420px] max-w-full sm:max-w-[95vw]
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

old_drawer = 'class="fixed top-0 right-0 h-full w-[420px] max-w-[95vw]'
new_drawer = 'class="fixed top-0 right-0 h-full w-full sm:w-[420px] max-w-full sm:max-w-[95vw]'

if old_drawer in index_html:
    index_html = index_html.replace(old_drawer, new_drawer)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("Fixed mobile floor width in index.html")
else:
    print("Could not find drawer class in index.html")

# 2. Update today.html timeline rendering: escape subject and chapter
with open('today.html', 'r', encoding='utf-8') as f:
    today_html = f.read()

# Add escapeHtml helper if not present
escape_helper = '''    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
'''

if 'function escapeHtml(' not in today_html:
    today_html = today_html.replace('function renderTodayTimeline() {', escape_helper + '    function renderTodayTimeline() {')

# Sanitize l.subject and l.chapter
old_timeline_item = '<div class="text-xs font-bold text-white">${l.subject} • ${l.chapter || \'Practice\'}</div>'
new_timeline_item = '<div class="text-xs font-bold text-white">${escapeHtml(l.subject)} • ${escapeHtml(l.chapter || \'Practice\')}</div>'

if old_timeline_item in today_html:
    today_html = today_html.replace(old_timeline_item, new_timeline_item)
    with open('today.html', 'w', encoding='utf-8') as f:
        f.write(today_html)
    print("Sanitized today.html timeline entries")
else:
    print("Could not find old_timeline_item in today.html")

# 3. Update admin.html: sanitize user email, role, etc. in users.map and logs.map
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

if 'function escapeHtml(' not in admin_html:
    # insert near start of <script>
    admin_html = admin_html.replace('<script>', '<script>\n    function escapeHtml(str) {\n      if (str === null || str === undefined) return "";\n      return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/\'/g, "&#39;");\n    }\n')

# Replace u.email with escapeHtml(u.email), u.role with escapeHtml(u.role), etc.
admin_html = admin_html.replace('${u.email}', '${escapeHtml(u.email)}')
admin_html = admin_html.replace('${u.role}', '${escapeHtml(u.role)}')
admin_html = admin_html.replace('${u.id}', '${escapeHtml(u.id)}')
admin_html = admin_html.replace('${l.userEmail || l.email || "Unknown"}', '${escapeHtml(l.userEmail || l.email || "Unknown")}')
admin_html = admin_html.replace('${l.action}', '${escapeHtml(l.action)}')
admin_html = admin_html.replace('${l.details}', '${escapeHtml(l.details)}')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)
print("Sanitized admin.html users and logs dynamic rendering")
