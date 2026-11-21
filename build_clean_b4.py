import json, re

steps = [859, 861, 863, 865, 867, 869, 871, 873, 875, 877, 879, 886, 892, 894, 896]
step_data = {}

with open(r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        s = obj.get('step_index')
        if s in steps:
            c = obj.get('content', '')
            pos = c.find(f'[Browser Step {s}]\n')
            if pos != -1:
                pos += len(f'[Browser Step {s}]\n')
                end = c.find('\n\n[WEBVIEW_BROWSER_HUD]', pos)
                if end == -1: end = len(c)
                raw = c[pos:end].strip()
                d = json.loads(raw, strict=False)
                step_data[s] = d.get('value')

# Collect all extracted items with their question number
# Steps:
# 859 -> Q61, Q62
# 861 -> Q63, Q64
# 863 -> Q65, Q66
# 865 -> Q67, Q68
# 867 -> Q69, Q70
# 869 -> Q71, Q72
# 871 -> Q73, Q74
# 873 -> Q75, Q76
# 875 -> Q77, Q78
# 877 -> Q79, Q80
# 879 -> Q81, Q82
# 886 -> Q83
# [HUD from 888] -> Q84
# 892 -> Q85 (q85Data), Q86 (q86Data)
# 894 -> Q87, Q88
# 896 -> Q89 (q89Data), Q90 (q90Data)

extracted_by_num = {}

def add_item(qnum, item):
    extracted_by_num[qnum] = item

# 859
add_item(61, step_data[859][0])
add_item(62, step_data[859][1])
# 861
add_item(63, step_data[861][0])
add_item(64, step_data[861][1])
# 863
add_item(65, step_data[863][0])
add_item(66, step_data[863][1])
# 865
add_item(67, step_data[865][0])
add_item(68, step_data[865][1])
# 867
add_item(69, step_data[867][0])
add_item(70, step_data[867][1])
# 869
add_item(71, step_data[869][0])
add_item(72, step_data[869][1])
# 871
add_item(73, step_data[871][0])
add_item(74, step_data[871][1])
# 873
add_item(75, step_data[873][0])
add_item(76, step_data[873][1])
# 875
add_item(77, step_data[875][0])
add_item(78, step_data[875][1])
# 877
add_item(79, step_data[877][0])
add_item(80, step_data[877][1])
# 879
add_item(81, step_data[879][0])
add_item(82, step_data[879][1])
# 886
add_item(83, step_data[886])

# Q84 manually synthesized from HUD in step 888:
add_item(84, {
    "correctOpt": 4,
    "iframeSrc": "",
    "images": [],
    "options": [
        {"is_correct": False, "option_index": 1, "percentage": "14.62% Marked this option", "text": "4 N"},
        {"is_correct": False, "option_index": 2, "percentage": "33.78% Marked this option", "text": "3 N"},
        {"is_correct": False, "option_index": 3, "percentage": "14.52% Marked this option", "text": "5 N"},
        {"is_correct": True, "option_index": 4, "percentage": "36.97% Marked this option", "text": "1 N"}
    ],
    "solutionText": ["Two blocks of masses 2 kg and 1 kg in contact. Horizontal force F = 3.0 N applied to 2 kg block. Common acceleration a = F / (m1 + m2) = 3.0 / (2 + 1) = 1.0 m/s^2. Contact force on 1 kg block = m2 * a = 1 kg * 1.0 m/s^2 = 1.0 N."],
    "statement": "Two blocks of masses 2 kg and 1 kg are in contact with each other on a frictionless table. When a horizontal force of 3.0 N is applied to the block of mass 2 kg, the value of the force of contact between the two blocks is:"
})

# 892
add_item(85, step_data[892]["q85Data"])
add_item(86, step_data[892]["q86Data"])
# 894
add_item(87, step_data[894][0])
add_item(88, step_data[894][1])
# 896
add_item(89, step_data[896]["q89Data"])
add_item(90, step_data[896]["q90Data"])

print(f"Total mapped questions 61 to 90: {len(extracted_by_num)}")
print("Keys present:", sorted(extracted_by_num.keys()))

with open('b4_extracted_clean.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_by_num, f, indent=2, ensure_ascii=False)
print("Saved b4_extracted_clean.json successfully!")
