import os, json, re

p = r'C:\Users\Kunal\.gemini\antigravity\brain\9b7f2b93-6e46-4371-91ca-186d7a6dc5b4\browser_sandbox\outputs'

step_files = [
    (1, [47]),
    (2, [49]), (3, [49]),
    (4, [51]), (5, [51]),
    (6, [53]), (7, [53]),
    (8, [55]), (9, [55]),
    (10, [57]), (11, [57]),
    (12, [59]), (13, [59]),
    (14, [61]), (15, [61]),
    (16, [63]), (17, [63]),
    (18, [65]), (19, [65]),
    (20, [67]), (21, [67]),
    (22, [69]), (23, [69]),
    (24, [71]), (25, [71]),
    (26, [184, 80]),
    (27, [186, 80]),
    (28, [88]), (29, [88]),
    (30, [100]), (31, [100]),
    (32, [168]),
    (33, [170]),
    (34, [110]),
    (35, [112]), (36, [112]),
    (37, [114]), (38, [114]),
    (39, [116]), (40, [116]),
    (41, [118]), (42, [118]),
    (43, [123]), (44, [123]),
    (45, [125]), (46, [125]),
    (47, [127]), (48, [127]),
    (49, [129]), (50, [129]),
    (51, [131]), (52, [131]),
    (53, [133]), (54, [133]),
    (55, [135]), (56, [135]),
    (57, [137]), (58, [137]),
    (59, [139]), (60, [139]),
    (61, [141]), (62, [141]),
    (63, [145])
]

# Check existing files
found_steps = set()
for f in os.listdir(p):
    if f.endswith('.json'):
        m = re.match(r'step_(\d+)\.json', f)
        if m:
            found_steps.add(int(m.group(1)))

print(f"Total json files found in outputs: {len(found_steps)}")
missing = []
for q, steps in step_files:
    if not any(s in found_steps for s in steps):
        missing.append((q, steps))

print(f"Missing question steps: {missing}")
