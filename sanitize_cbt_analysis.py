with open('cbt_analysis.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add escapeHtml helper
escape_fn = '''    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
'''

if 'function escapeHtml(' not in content:
    content = content.replace('<script>', '<script>\n' + escape_fn, 1)
    print("Added escapeHtml to cbt_analysis.html")

# Sanitize learnings item
content = content.replace('<span>${item}</span>', '<span>${escapeHtml(item)}</span>')

# Sanitize subject / chapter / topic in modal-sol-body
content = content.replace('${subject}</span>', '${escapeHtml(subject)}</span>')
content = content.replace('${chapter} • ${topic}</span>', '${escapeHtml(chapter)} • ${escapeHtml(topic)}</span>')

# Sanitize table row q.subject
content = content.replace('<td class="p-3 font-semibold text-gray-300">${q.subject}</td>', '<td class="p-3 font-semibold text-gray-300">${escapeHtml(q.subject)}</td>')

with open('cbt_analysis.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated cbt_analysis.html with XSS escaping")
