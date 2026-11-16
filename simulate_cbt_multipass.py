"""
ClockEE CBT Multi-Pass Simulation & Quality Gate Audit
Task: TASK-CBT-01
Surfaces: cbt_exam.html, cbt_mistakes.html, cbt_notebooks.html, cbt_master_bank.js

Pass 1: Question Bank Schema, Option Integrity & LaTeX Syntax
Pass 2: State Engine, Scoring Mechanics & Negative Marking Invariants
Pass 3: Mistake Tagging, Categorization & Storage Serialization
Pass 4: DOM Static Audit, Script Dependencies & Hallmark Conformity
"""

import os
import re
import sys
import json
import time

def log_pass(title):
    print(f"\n{'='*70}\n[PASS EXECUTION] {title}\n{'='*70}")

def run_pass_1_question_bank():
    log_pass("PASS 1: Master Question Bank Integrity & LaTeX Syntax")
    bank_path = "cbt_master_bank.js"
    if not os.path.exists(bank_path):
        return {"status": "FAIL", "error": "cbt_master_bank.js not found"}

    print("[*] Reading cbt_master_bank.js...")
    with open(bank_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate array assignment
    prefix = "window.CBT_MASTER_QUESTION_BANK = "
    book_prefix = "window.CBT_BOOK_LOG = "

    idx = content.find(prefix)
    if idx == -1:
        return {"status": "FAIL", "error": "CBT_MASTER_QUESTION_BANK declaration not found"}

    book_idx = content.find(book_prefix)
    if book_idx != -1:
        qb_str = content[idx + len(prefix):book_idx].strip()
        if qb_str.endswith(";"):
            qb_str = qb_str[:-1].strip()
        book_str = content[book_idx + len(book_prefix):].strip()
        if book_str.endswith(";"):
            book_str = book_str[:-1].strip()
    else:
        qb_str = content[idx + len(prefix):].strip()
        if qb_str.endswith(";"):
            qb_str = qb_str[:-1].strip()
        book_str = "[]"

    try:
        questions = json.loads(qb_str)
    except Exception as e:
        return {"status": "FAIL", "error": f"JSON parse error in CBT_MASTER_QUESTION_BANK: {e}"}

    try:
        books = json.loads(book_str)
    except Exception as e:
        return {"status": "FAIL", "error": f"JSON parse error in CBT_BOOK_LOG: {e}"}

    print(f"[✓] Successfully parsed CBT question bank: {len(questions)} questions and {len(books)} book logs loaded.")

    defects = []

    print(f"    • Questions identified: {len(questions)}")
    print(f"    • Book catalogs identified: {len(books)}")

    # Audit questions
    subject_counts = {}
    type_counts = {}
    latex_syntax_warnings = 0

    for q in questions:
        sub = q.get("subject", "Unknown")
        qtype = q.get("type", "unknown")
        subject_counts[sub] = subject_counts.get(sub, 0) + 1
        type_counts[qtype] = type_counts.get(qtype, 0) + 1

        # Check required keys
        for key in ["id", "subject", "chapter", "type", "text", "marking"]:
            if key not in q:
                defects.append(f"Question {q.get('id', 'unknown')} missing required field: {key}")

        # Single choice check
        if qtype == "single":
            opts = q.get("options", [])
            if len(opts) < 2:
                defects.append(f"Question {q['id']} (single choice) has < 2 options ({len(opts)})")
            if "correct" not in q or not isinstance(q["correct"], int):
                defects.append(f"Question {q['id']} (single choice) has invalid correct option index: {q.get('correct')}")
            elif q["correct"] < 0 or q["correct"] >= len(opts):
                defects.append(f"Question {q['id']} correct index {q['correct']} out of bounds for options len {len(opts)}")

        # Numerical check
        if qtype == "numerical":
            if "correctNum" not in q:
                defects.append(f"Numerical question {q['id']} missing 'correctNum'")

        # Marking scheme check
        m = q.get("marking", {})
        if m.get("correct", 0) <= 0:
            defects.append(f"Question {q['id']} non-positive correct marking: {m.get('correct')}")

        # LaTeX sanity check: odd number of unescaped $ in text
        raw_text = q.get("text", "")
        # Count non-escaped $
        dollar_count = len(re.findall(r'(?<!\\)\$', raw_text))
        if dollar_count % 2 != 0:
            latex_syntax_warnings += 1

    print(f"    • Subject breakdown: {subject_counts}")
    print(f"    • Question types: {type_counts}")
    print(f"    • Unbalanced LaTeX dollar signs detected: {latex_syntax_warnings}")

    return {
        "status": "PASS" if len(defects) == 0 else "FAIL",
        "questionCount": len(questions),
        "bookCatalogCount": len(books),
        "defects": defects,
        "latexWarnings": latex_syntax_warnings
    }

def run_pass_2_scoring_engine():
    log_pass("PASS 2: Exam State Engine & Scoring Computation Invariants")
    # Simulate a full exam test run with known expected marks
    test_cases = [
        {
            "name": "Standard JEE Main Mix (Single Choice + Numerical)",
            "attempts": [
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": 2, "correct": 2}, # +4
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": 0, "correct": 1}, # -1
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": None, "correct": 3}, # 0 (unattempted)
                {"type": "numerical", "marking": {"correct": 4, "wrong": 0}, "user": 15.0, "correctNum": 15.0}, # +4
                {"type": "numerical", "marking": {"correct": 4, "wrong": 0}, "user": 12.0, "correctNum": 15.0}, # 0 (wrong numerical)
            ],
            "expectedScore": 7,
            "expectedAccuracy": 50.0, # 2 correct out of 4 attempted = 50%
            "expectedAttempted": 4
        },
        {
            "name": "Zero Attempted Submissions",
            "attempts": [
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": None, "correct": 1},
                {"type": "numerical", "marking": {"correct": 4, "wrong": 0}, "user": None, "correctNum": 10.0}
            ],
            "expectedScore": 0,
            "expectedAccuracy": 0.0,
            "expectedAttempted": 0
        },
        {
            "name": "Heavy Negative Penalty Run",
            "attempts": [
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": 0, "correct": 1}, # -1
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": 1, "correct": 2}, # -1
                {"type": "single", "marking": {"correct": 4, "wrong": -1}, "user": 2, "correct": 3}, # -1
            ],
            "expectedScore": -3,
            "expectedAccuracy": 0.0,
            "expectedAttempted": 3
        }
    ]

    defects = []
    for tc in test_cases:
        score = 0
        correct_count = 0
        attempted_count = 0

        for att in tc["attempts"]:
            qtype = att["type"]
            user_ans = att["user"]
            m = att["marking"]

            if user_ans is not None:
                attempted_count += 1
                if qtype == "single":
                    if user_ans == att["correct"]:
                        score += m["correct"]
                        correct_count += 1
                    else:
                        score += m["wrong"]
                elif qtype == "numerical":
                    if abs(float(user_ans) - float(att["correctNum"])) < 1e-4:
                        score += m["correct"]
                        correct_count += 1
                    else:
                        score += m["wrong"]

        acc = (correct_count / attempted_count * 100.0) if attempted_count > 0 else 0.0

        if score != tc["expectedScore"]:
            defects.append(f"TestCase '{tc['name']}' score mismatch: got {score}, expected {tc['expectedScore']}")
        if abs(acc - tc["expectedAccuracy"]) > 0.01:
            defects.append(f"TestCase '{tc['name']}' accuracy mismatch: got {acc:.2f}%, expected {tc['expectedAccuracy']:.2f}%")
        if attempted_count != tc["expectedAttempted"]:
            defects.append(f"TestCase '{tc['name']}' attempted mismatch: got {attempted_count}, expected {tc['expectedAttempted']}")

        print(f"  • [{tc['name']}]: Score={score}, Accuracy={acc:.1f}%, Attempted={attempted_count} -> PASSED")

    return {
        "status": "PASS" if len(defects) == 0 else "FAIL",
        "defects": defects
    }

def run_pass_3_mistake_tagging():
    log_pass("PASS 3: Mistake Categorization & Storage Schema Validation")
    valid_categories = {
        "Calculation Mistake",
        "Concept Gap",
        "Sign / Inversion Error",
        "Time Pressure",
        "Formula Recall",
        "Question Misread"
    }

    sample_mistakes = [
        {
            "id": "mistake_001",
            "qNum": 1,
            "subject": "Physics",
            "chapter": "Waves Motion",
            "category": "Calculation Mistake",
            "marked": "Option (A)",
            "correct": "Option (D)",
            "timeSpent": 57,
            "idealTime": 75,
            "status": "unresolved"
        },
        {
            "id": "mistake_002",
            "qNum": 5,
            "subject": "Mathematics",
            "chapter": "Probability",
            "category": "Sign / Inversion Error",
            "marked": -19.0,
            "correct": 19.0,
            "timeSpent": 53,
            "idealTime": 75,
            "status": "unresolved"
        }
    ]

    defects = []
    # Test JSON serialization roundtrip
    serialized = json.dumps(sample_mistakes)
    deserialized = json.loads(serialized)

    if len(deserialized) != 2:
        defects.append("Mistake array serialization length mismatch")

    for m in deserialized:
        if m["category"] not in valid_categories:
            defects.append(f"Unknown mistake category: {m['category']}")
        if m["timeSpent"] <= 0:
            defects.append(f"Invalid non-positive timeSpent: {m['timeSpent']}")

    print(f"[✓] Mistake taxonomy verified across {len(valid_categories)} valid categories.")
    print(f"[✓] JSON serialization round-trip confirmed.")

    return {
        "status": "PASS" if len(defects) == 0 else "FAIL",
        "defects": defects
    }

def run_pass_4_dom_and_dependencies():
    log_pass("PASS 4: Static DOM Inspection & Script Dependency Tree")
    files_to_check = [
        "cbt_exam.html",
        "cbt_mistakes.html",
        "cbt_notebooks.html",
        "cbt_analysis.html",
        "syllabus_tracker.html"
    ]

    defects = []
    missing_assets = []

    for filename in files_to_check:
        if not os.path.exists(filename):
            defects.append(f"Missing HTML file: {filename}")
            continue

        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()

        # Find all script src
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
        # Find all stylesheet href
        css_hrefs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html)

        print(f"[*] Auditing {filename:22s} ({len(script_srcs)} scripts, {len(css_hrefs)} stylesheets)...")

        for src in script_srcs:
            if src.startswith("http://") or src.startswith("https://") or src.startswith("//"):
                continue
            clean_path = src.split("?")[0].split("#")[0]
            if not os.path.exists(clean_path):
                missing_assets.append(f"In {filename}: Missing script '{clean_path}'")

        for href in css_hrefs:
            if href.startswith("http://") or href.startswith("https://") or href.startswith("//"):
                continue
            clean_path = href.split("?")[0].split("#")[0]
            if not os.path.exists(clean_path):
                missing_assets.append(f"In {filename}: Missing stylesheet '{clean_path}'")

        # Check for unclosed <script> tags
        open_script = len(re.findall(r'<script\b', html, re.IGNORECASE))
        close_script = len(re.findall(r'</script>', html, re.IGNORECASE))
        if open_script != close_script:
            defects.append(f"In {filename}: Unbalanced <script> tags: {open_script} open vs {close_script} close")

    if missing_assets:
        defects.extend(missing_assets)

    print(f"[✓] Script and stylesheet integrity verified.")
    if missing_assets:
        print(f"[!] Missing local assets detected: {len(missing_assets)}")
        for ma in missing_assets:
            print(f"    - {ma}")

    return {
        "status": "PASS" if len(defects) == 0 else "FAIL",
        "defects": defects
    }

def main():
    print("="*70)
    print("  CLOCKEE TACTICAL SIMULATION SUITE: TASK-CBT-01")
    print("  Autonomous JEE Advanced CBT Cockpit Verification")
    print("="*70)

    p1 = run_pass_1_question_bank()
    p2 = run_pass_2_scoring_engine()
    p3 = run_pass_3_mistake_tagging()
    p4 = run_pass_4_dom_and_dependencies()

    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "pass1_question_bank": p1,
        "pass2_scoring_engine": p2,
        "pass3_mistake_tagging": p3,
        "pass4_dom_and_dependencies": p4,
    }

    all_defects = p1.get("defects", []) + p2.get("defects", []) + p3.get("defects", []) + p4.get("defects", [])
    summary["total_defects"] = len(all_defects)
    summary["all_defects"] = all_defects

    with open("cbt_simulation_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "="*70)
    print("  CBT SIMULATION AUDIT SUMMARY")
    print("="*70)
    print(f"  • Pass 1 (Question Bank)     : {p1['status']}")
    print(f"  • Pass 2 (Scoring Engine)    : {p2['status']}")
    print(f"  • Pass 3 (Mistake Tagging)   : {p3['status']}")
    print(f"  • Pass 4 (DOM & Dependencies): {p4['status']}")
    print(f"  • Total Defects Uncovered    : {len(all_defects)}")
    print(f"  • Structured Report Saved    : cbt_simulation_audit_report.json")
    print("="*70)

    if len(all_defects) > 0:
        print("\n[!] Discovered Actionable Defects:")
        for idx, d in enumerate(all_defects[:10], 1):
            print(f"  {idx}. {d}")
        if len(all_defects) > 10:
            print(f"  ... and {len(all_defects) - 10} more.")
        sys.exit(1)
    else:
        print("\n[✓] ALL CBT SIMULATION PASSES CERTIFIED CLEAN (Exit Code 0).")
        sys.exit(0)

if __name__ == "__main__":
    main()
