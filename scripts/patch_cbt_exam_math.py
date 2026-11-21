with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate question text rendering
target_str = "textContainer.innerHTML = activeQuestion.text;"
if target_str in text:
    replacement = """const sanitizedText = window.ClockEEMath ? ClockEEMath.sanitize(activeQuestion.text) : activeQuestion.text;
      textContainer.innerHTML = sanitizedText;"""
    text = text.replace(target_str, replacement)
    print("Replaced question text container assignment with sanitizedText")

# Add script tag in head
if '<script src="js/math_renderer.js"></script>' not in text:
    text = text.replace('</head>', '  <script src="js/math_renderer.js"></script>\n</head>')
    print("Added math_renderer.js script tag to head")

with open('cbt_exam.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated cbt_exam.html successfully")
