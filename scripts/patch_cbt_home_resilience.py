with open('cbt_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Quizrr with ClockEE CBT
text = text.replace('Quizrr', 'ClockEE CBT')

# Enhance question bank initialization to fall back to window.CBT_MASTER_BANK or window.CBT_QUESTIONS
start_marker = "// Try loading live cbt_question_bank.json if available"
end_marker = "updateVitals();"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_init = """// Populate from window.CBT_MASTER_BANK or fetch live cbt_question_bank.json
      function ingestBankData(data) {
        if (Array.isArray(data) && data.length > 0) {
          console.log(`✓ Ingested ${data.length} authentic questions into CBT Home`);
          data.forEach(q => {
            const sub = q.subject || "Physics";
            const ch = q.chapter || "General";
            if (!masterChaptersMap[sub]) masterChaptersMap[sub] = {};
            if (!masterChaptersMap[sub][ch]) masterChaptersMap[sub][ch] = [];
            masterChaptersMap[sub][ch].push(q);
            if (sub === "Mathematics") {
              if (!masterChaptersMap["Maths"]) masterChaptersMap["Maths"] = {};
              if (!masterChaptersMap["Maths"][ch]) masterChaptersMap["Maths"][ch] = [];
              masterChaptersMap["Maths"][ch].push(q);
            } else if (sub === "Maths") {
              if (!masterChaptersMap["Mathematics"]) masterChaptersMap["Mathematics"] = {};
              if (!masterChaptersMap["Mathematics"][ch]) masterChaptersMap["Mathematics"][ch] = [];
              masterChaptersMap["Mathematics"][ch].push(q);
            }
          });
        }
      }

      if (window.CBT_MASTER_BANK && Array.isArray(window.CBT_MASTER_BANK) && window.CBT_MASTER_BANK.length > 0) {
        ingestBankData(window.CBT_MASTER_BANK);
        renderAccordions();
      }

      fetch('cbt_question_bank.json')
        .then(res => res.json())
        .then(data => {
          ingestBankData(data);
          renderAccordions();
        })
        .catch(err => {
          console.warn("Live fetch bypassed, using local memory bank / matrix:", err);
          renderAccordions();
        });

      """
    text = text[:idx_start] + new_init + text[idx_end:]
    print("Successfully replaced question bank initialization in cbt_home.html")
else:
    print(f"Markers not found: start={idx_start}, end={idx_end}")

with open('cbt_home.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved cbt_home.html successfully.")
