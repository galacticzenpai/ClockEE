#!/usr/bin/env python3
"""
⚡ ClockEE — Autonomous Simulation & Error Diagnostics Runner
Runs JEE Exam Simulations, evaluates answers, autopsies errors, and sends telemetry to Main Control.
"""

import os
import sys
import json
import time
import random
import sqlite3
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "clockee.db"
AUTH_DB_PATH = ROOT_DIR / "clockee_auth.db"
QUESTION_BANK_PATH = ROOT_DIR / "cbt_question_bank.json"
REPORT_OUTPUT_PATH = ROOT_DIR / "simulation_error_report.json"

# ANSI Terminal Styling
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner():
    banner = f"""
{CYAN}{BOLD}========================================================================
   ⚡ CLOCKEE TACTICAL SIMULATION ENGINE & ERROR RADAR DISPATCHER
========================================================================{RESET}
 {DIM}Autonomous JEE Advanced Cockpit • Real-Time Error Checking & Telemetry{RESET}
"""
    print(banner)


def audit_question_bank(bank_path=QUESTION_BANK_PATH):
    """
    Checks the entire question bank for syntax, missing fields, or data errors.
    """
    print(f"\n{BOLD}[*] Auditing Question Bank Data Integrity:{RESET} {bank_path.name}")
    if not bank_path.is_file():
        print(f"{RED}[!] Question bank file not found: {bank_path}{RESET}")
        return []

    try:
        with open(bank_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
    except Exception as e:
        print(f"{RED}[!] Failed to parse JSON question bank: {e}{RESET}")
        return []

    print(f"[*] Scanning {len(questions):,} question records across Physics, Chemistry, and Mathematics...")

    errors = []
    subject_counts = {"Physics": 0, "Chemistry": 0, "Maths": 0, "Other": 0}
    type_counts = {"single": 0, "numerical": 0, "other": 0}

    for idx, q in enumerate(questions):
        sub = q.get("subject", "Other")
        if sub in subject_counts:
            subject_counts[sub] += 1
        else:
            subject_counts["Other"] += 1

        q_type = q.get("type", "single")
        if q_type in type_counts:
            type_counts[q_type] += 1
        else:
            type_counts["other"] += 1

        # Error checks
        q_text = q.get("text", "")
        if not q_text or len(q_text.strip()) == 0:
            errors.append({"qNum": idx + 1, "id": q.get("id"), "error": "Empty question statement"})

        # Check options for single choice
        if q_type == "single":
            opts = q.get("options", [])
            if not opts or len(opts) < 2:
                errors.append({"qNum": idx + 1, "id": q.get("id"), "error": "Missing or fewer than 2 option choices"})
            if q.get("correct") is None:
                errors.append({"qNum": idx + 1, "id": q.get("id"), "error": "Missing correct option index"})
        elif q_type == "numerical":
            if q.get("correctNum") is None and q.get("correct") is None:
                errors.append({"qNum": idx + 1, "id": q.get("id"), "error": "Missing numerical correct answer key"})

        # Check for unclosed KaTeX math blocks
        if q_text:
            single_dollars = q_text.count("$") - (q_text.count("$$") * 2)
            if single_dollars % 2 != 0:
                errors.append({"qNum": idx + 1, "id": q.get("id"), "error": "Unclosed inline LaTeX math ($)"})

    print(f"\n{GREEN}[✓] Audit Completed:{RESET}")
    print(f"  • Physics:   {subject_counts['Physics']:,} Qs")
    print(f"  • Chemistry: {subject_counts['Chemistry']:,} Qs")
    print(f"  • Maths:     {subject_counts['Maths']:,} Qs")
    print(f"  • Total Evaluated: {len(questions):,} questions")
    print(f"  • Data Formatting Errors Detected: {RED if errors else GREEN}{len(errors)}{RESET}")

    if errors:
        print(f"\n{YELLOW}[!] Sample Errors Found ({min(5, len(errors))} of {len(errors)}):{RESET}")
        for err in errors[:5]:
            print(f"    - Q#{err['qNum']} ({err.get('id', 'N/A')}): {err['error']}")
    else:
        print(f"  • {GREEN}100% of question bank conforms to ClockEE LaTeX & scoring standards.{RESET}")

    return errors


def load_question_pool(subject="Full", count=75, target_latency=75):
    """
    Retrieves real questions from cbt_question_bank.json or creates realistic mock questions.
    """
    pool = []
    if QUESTION_BANK_PATH.is_file():
        try:
            with open(QUESTION_BANK_PATH, "r", encoding="utf-8") as f:
                bank = json.load(f)

            if subject == "Full":
                per_sub = count // 3
                rem = count - (per_sub * 2)
                p_pool = [q for q in bank if q.get("subject") == "Physics"]
                c_pool = [q for q in bank if q.get("subject") == "Chemistry"]
                m_pool = [q for q in bank if q.get("subject") in ["Maths", "Mathematics"]]

                random.shuffle(p_pool)
                random.shuffle(c_pool)
                random.shuffle(m_pool)

                selected = p_pool[:per_sub] + c_pool[:per_sub] + m_pool[:rem]
                pool = selected
            else:
                norm_sub = "Maths" if subject in ["Maths", "Mathematics"] else subject
                sub_pool = [q for q in bank if q.get("subject") == norm_sub]
                random.shuffle(sub_pool)
                pool = sub_pool[:count]
        except Exception as e:
            print(f"{YELLOW}[!] Notice reading question bank ({e}), generating calibrated questions.{RESET}")

    # Fallback synthesizer if not enough questions in bank
    if len(pool) < count:
        needed = count - len(pool)
        for i in range(1, needed + 1):
            is_num = (i % 5 == 0)
            cur_sub = subject
            if subject == "Full":
                cur_sub = "Physics" if i <= needed // 3 else ("Chemistry" if i <= (needed * 2) // 3 else "Maths")

            pool.append({
                "id": f"synth_{cur_sub.lower()[:3]}_{Date_stamp()}_{i}",
                "num": len(pool) + 1,
                "type": "numerical" if is_num else "single",
                "subject": cur_sub,
                "chapter": f"{cur_sub} Core Domain",
                "topic": f"High-Yield Concept #{i}",
                "difficulty": "Tough" if i % 3 == 0 else "Moderate",
                "idealTimeSec": target_latency,
                "text": f"Simulation test problem for {cur_sub} #{i}: Determine the critical threshold value.",
                "options": None if is_num else ["Option (A)", "Option (B)", "Option (C)", "Option (D)"],
                "correct": i % 4,
                "correctNum": round(12.5 + (i * 1.5), 1),
                "marking": {"correct": 4, "wrong": -1}
            })

    # Number sequentially
    for idx, q in enumerate(pool[:count]):
        q["num"] = idx + 1
        q["idealTimeSec"] = target_latency

    return pool[:count]


def Date_stamp():
    return int(time.time() * 1000)


def run_simulation(subject="Full", count=75, profile="balanced", target_latency=75):
    """
    Executes a simulated test run, evaluates questions, and categorizes all errors.
    """
    print(f"\n{BOLD}[*] Running Exam Simulation:{RESET}")
    print(f"  • Target Domain: {CYAN}{subject} Syllabus{RESET}")
    print(f"  • Question Count: {count} Questions")
    print(f"  • Target Latency: {target_latency}s / Question")
    print(f"  • Candidate Profile: {MAGENTA}{profile.upper()}{RESET}")

    questions = load_question_pool(subject=subject, count=count, target_latency=target_latency)
    user_responses = []

    # Simulation Skill Settings
    skill_accuracy = 0.90 if profile == "topper" else (0.74 if profile == "balanced" else 0.52)
    attempt_rate = 0.96 if profile == "topper" else (0.92 if profile == "balanced" else 0.85)

    print(f"\n[*] Simulating real candidate latency & response attempts across {len(questions)} problems...")

    for q in questions:
        is_attempted = random.random() < attempt_rate
        if not is_attempted:
            user_responses.append({
                "status": "not_attempted",
                "selectedOption": None,
                "enteredValue": None,
                "timeSpent": random.randint(15, 45)
            })
            continue

        q_acc = skill_accuracy - (0.10 if q.get("type") == "numerical" else 0.0)
        is_correct = random.random() < q_acc

        ideal = q.get("idealTimeSec", target_latency)
        # Latency delta with Gaussian spread
        time_factor = random.uniform(0.65, 1.45)
        time_spent = max(18, int(ideal * time_factor))

        if q.get("type") == "single":
            corr = q.get("correct", 0)
            if is_correct:
                sel = corr
            else:
                distractors = [d for d in [0, 1, 2, 3] if d != corr]
                sel = random.choice(distractors)
            user_responses.append({
                "status": "answered",
                "selectedOption": sel,
                "enteredValue": None,
                "timeSpent": time_spent
            })
        else:
            exp = float(q.get("correctNum", q.get("correct", 25.0)))
            if is_correct:
                val = exp
            else:
                # Common errors: sign inversion or arithmetic drift
                err_choice = random.choice(["sign", "calc", "off_by_one"])
                if err_choice == "sign" and exp != 0:
                    val = -exp
                elif err_choice == "off_by_one":
                    val = exp + random.choice([-1.0, 1.0])
                else:
                    val = round(exp * random.uniform(0.7, 1.3), 1)

            user_responses.append({
                "status": "answered",
                "selectedOption": None,
                "enteredValue": str(val),
                "timeSpent": time_spent
            })

    # Evaluate responses and check for errors
    test_meta = {
        "id": f"sim_py_{Date_stamp()}",
        "title": f"Autonomous {subject} Mock Simulation",
        "targetLatencySec": target_latency
    }

    eval_result = evaluate_and_check_errors(questions, user_responses, test_meta)
    return eval_result


def evaluate_and_check_errors(questions, user_responses, test_meta):
    """
    Pure evaluation and autopsy extraction function.
    """
    total_score = 0
    correct_count = 0
    wrong_count = 0
    attempted_count = 0
    positive_marks = 0
    negative_marks = 0
    mistakes = []
    latencies = []

    sub_breakdown = {}

    for idx, q in enumerate(questions):
        resp = user_responses[idx]
        sub = q.get("subject", "Physics")
        if sub not in sub_breakdown:
            sub_breakdown[sub] = {"attempted": 0, "correct": 0, "wrong": 0, "score": 0, "time_sec": 0}

        is_eval = resp.get("status") == "answered"
        ideal = q.get("idealTimeSec", 75)
        time_spent = resp.get("timeSpent", 0)
        sub_breakdown[sub]["time_sec"] += time_spent

        is_correct = False
        score_delta = 0

        if is_eval:
            attempted_count += 1
            sub_breakdown[sub]["attempted"] += 1

            if q.get("type") == "single":
                is_correct = (resp.get("selectedOption") == q.get("correct"))
            else:
                try:
                    entered = float(resp.get("enteredValue", 0))
                    expected = float(q.get("correctNum", q.get("correct", 0)))
                    is_correct = abs(entered - expected) <= 0.05
                except (ValueError, TypeError):
                    is_correct = False

            if is_correct:
                correct_count += 1
                positive_marks += 4
                total_score += 4
                score_delta = 4
                sub_breakdown[sub]["correct"] += 1
                sub_breakdown[sub]["score"] += 4
            else:
                wrong_count += 1
                negative_marks += 1
                total_score -= 1
                score_delta = -1
                sub_breakdown[sub]["wrong"] += 1
                sub_breakdown[sub]["score"] -= 1

                # Categorize Root Cause
                if q.get("type") == "single":
                    if time_spent < ideal * 0.45:
                        cat = "Silly / Rushed Mistake"
                        detail = f"Answered in only {time_spent}s (< 45% of ideal time). Rushed reading problem statement."
                    elif time_spent > ideal * 1.35:
                        cat = "Concept Gap"
                        detail = f"Spent {time_spent}s struggling with formula derivation. Theory revision required."
                    else:
                        cat = "Calculation Mistake" if (idx % 2 == 0) else "Concept Gap"
                        detail = f"Selected Option ({chr(65 + (resp.get('selectedOption') or 0))}) instead of ({chr(65 + (q.get('correct') or 0))})."
                else:
                    try:
                        ent = float(resp.get("enteredValue", 0))
                        exp = float(q.get("correctNum", q.get("correct", 0)))
                        if ent == -exp and exp != 0:
                            cat = "Sign / Inversion Error"
                            detail = f"Sign inversion error: entered {ent} vs expected {exp}. Verify direction vector."
                        elif time_spent < ideal * 0.45:
                            cat = "Silly / Rushed Mistake"
                            detail = f"Rushed arithmetic in {time_spent}s."
                        else:
                            cat = "Calculation Mistake"
                            detail = f"Calculated value {ent} deviates from ground truth {exp}."
                    except Exception:
                        cat = "Calculation Mistake"
                        detail = f"Value {resp.get('enteredValue')} failed numerical match."

                mistake_record = {
                    "id": f"mistake_{test_meta['id']}_{idx + 1}",
                    "testId": test_meta["id"],
                    "testTitle": test_meta["title"],
                    "qNum": idx + 1,
                    "subject": sub,
                    "chapter": q.get("chapter", f"{sub} Core Domain"),
                    "topic": q.get("topic", f"{sub} Concept #{idx + 1}"),
                    "questionText": q.get("text", f"Question #{idx + 1}"),
                    "markedOption": f"Option ({chr(65 + resp['selectedOption'])})" if q.get("type") == "single" else str(resp.get("enteredValue")),
                    "correctOption": f"Option ({chr(65 + q['correct'])})" if q.get("type") == "single" else str(q.get("correctNum", q.get("correct"))),
                    "errorCategory": cat,
                    "reason": cat,
                    "reasonDetail": detail,
                    "idealTimeSec": ideal,
                    "timeSpentSec": time_spent,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "important": True,
                    "bookmarked": True,
                    "status": "unresolved"
                }
                mistakes.append(mistake_record)

        latencies.append({
            "qNum": idx + 1,
            "subject": sub,
            "timeSec": time_spent,
            "targetLatencySec": ideal,
            "status": "correct" if is_correct else ("wrong" if is_eval else "unattempted"),
            "scoreDelta": score_delta
        })

    accuracy = round((correct_count / attempted_count) * 100, 2) if attempted_count > 0 else 0.0
    total_time_sec = sum(r.get("timeSpent", 0) for r in user_responses)
    avg_latency = round(total_time_sec / max(1, attempted_count))

    return {
        "testId": test_meta["id"],
        "title": test_meta["title"],
        "totalQs": len(questions),
        "attempted": attempted_count,
        "correctCount": correct_count,
        "wrongCount": wrong_count,
        "score": max(0, total_score),
        "maxScore": len(questions) * 4,
        "positiveMarks": positiveMarks if 'positiveMarks' in locals() else positive_marks,
        "negativeMarks": negativeMarks if 'negativeMarks' in locals() else negative_marks,
        "accuracy": accuracy,
        "timeTakenMin": max(1, round(total_time_sec / 60)),
        "avgLatencySec": avg_latency,
        "mistakes": mistakes,
        "questionLatencies": latencies,
        "subjectBreakdown": sub_breakdown,
        "questions": questions,
        "userResponses": user_responses
    }


def send_to_main_control(eval_result, host="127.0.0.1", port=8000):
    """
    Dispatches simulation results and error autopsies to Main Control:
    1. Local database persistence (clockee.db & clockee_auth.db)
    2. HTTP POST to server.py endpoint /api/simulations/report
    3. Output JSON artifact simulation_error_report.json
    """
    print(f"\n{BOLD}[*] Dispatching Simulation & Errors to Main Control:{RESET}")

    # 1. Save Report JSON Artifact
    try:
        report_data = {
            "simulationId": eval_result["testId"],
            "title": eval_result["title"],
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "score": eval_result["score"],
                "maxScore": eval_result["maxScore"],
                "accuracy": eval_result["accuracy"],
                "attempted": eval_result["attempted"],
                "totalQs": eval_result["totalQs"],
                "avgLatencySec": eval_result["avgLatencySec"],
                "timeTakenMin": eval_result["timeTakenMin"]
            },
            "errorCount": len(eval_result["mistakes"]),
            "mistakes": eval_result["mistakes"],
            "subjectBreakdown": eval_result["subjectBreakdown"]
        }
        with open(REPORT_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"  • {GREEN}[✓] Simulation error report generated:{RESET} {REPORT_OUTPUT_PATH.name}")
    except Exception as e:
        print(f"  • {RED}[!] Failed writing report file: {e}{RESET}")

    # 2. Persist in Local SQLite Database
    db_updated = False
    for db_file in [DB_PATH, AUTH_DB_PATH]:
        if db_file.is_file():
            try:
                conn = sqlite3.connect(db_file)
                cur = conn.cursor()

                # Insert into cbt_exams if table exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS cbt_exams (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        test_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        mode TEXT DEFAULT 'simulation',
                        subject TEXT NOT NULL,
                        chapter TEXT DEFAULT '',
                        total_questions INTEGER DEFAULT 25,
                        time_spent_seconds INTEGER DEFAULT 0,
                        score INTEGER DEFAULT 0,
                        max_score INTEGER DEFAULT 100,
                        accuracy REAL DEFAULT 0.0,
                        status TEXT DEFAULT 'completed',
                        responses_json TEXT DEFAULT '[]',
                        analytics_json TEXT DEFAULT '{}',
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("""
                    INSERT OR REPLACE INTO cbt_exams (
                        id, user_id, test_id, title, mode, subject, chapter, total_questions,
                        time_spent_seconds, score, max_score, accuracy, status, responses_json, analytics_json, completed_at
                    ) VALUES (?, 'user_alpha', ?, ?, 'simulation', 'Full', 'Main Control Simulation', ?, ?, ?, ?, ?, 'completed', ?, ?, CURRENT_TIMESTAMP)
                """, (
                    eval_result["testId"], eval_result["testId"], eval_result["title"],
                    eval_result["totalQs"], eval_result["timeTakenMin"] * 60,
                    eval_result["score"], eval_result["maxScore"], eval_result["accuracy"],
                    json.dumps(eval_result["mistakes"]), json.dumps(eval_result["subjectBreakdown"])
                ))

                # Insert tasks into tasks table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        subject TEXT DEFAULT 'General',
                        priority TEXT DEFAULT 'medium',
                        completed INTEGER DEFAULT 0,
                        due_date TEXT DEFAULT '',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                for m in eval_result["mistakes"]:
                    task_id = f"task_{m['id']}"
                    cur.execute("""
                        INSERT OR REPLACE INTO tasks (id, user_id, title, subject, priority, completed, due_date)
                        VALUES (?, 'user_alpha', ?, ?, 'high', 0, CURRENT_DATE)
                    """, (task_id, f"[Autopsy] Master Error Q#{m['qNum']}: {m['topic']}", m['subject']))

                conn.commit()
                conn.close()
                print(f"  • {GREEN}[✓] Telemetry persisted in SQLite database:{RESET} {db_file.name}")
                db_updated = True
            except Exception as e:
                print(f"  • {YELLOW}[!] DB persist note ({db_file.name}): {e}{RESET}")

    # 3. HTTP Dispatch to server.py API
    endpoint = f"http://{host}:{port}/api/simulations/report"
    try:
        payload = json.dumps({
            "user_id": "user_alpha",
            "test_id": eval_result["testId"],
            "title": eval_result["title"],
            "subject": "Full",
            "score": eval_result["score"],
            "max_score": eval_result["maxScore"],
            "accuracy": eval_result["accuracy"],
            "total_questions": eval_result["totalQs"],
            "mistakes": eval_result["mistakes"],
            "analytics": {
                "avgLatencySec": eval_result["avgLatencySec"],
                "subjectBreakdown": eval_result["subjectBreakdown"]
            }
        }).encode("utf-8")

        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  • {GREEN}[✓] Live API Handshake Success:{RESET} {endpoint}")
            print(f"    - Main Control Server acknowledged {data.get('errors_logged', len(eval_result['mistakes']))} errors.")
            print(f"    - Queued {data.get('tasks_created', len(eval_result['mistakes']))} autopsy tasks in Task Flow.")
    except urllib.error.URLError:
        print(f"  • {YELLOW}[i] Server at {endpoint} not running (safe offline mode active).{RESET}")
        print(f"    - Report stored locally and ready for automatic browser pickup.")
    except Exception as e:
        print(f"  • {YELLOW}[!] Handshake notice: {e}{RESET}")


def display_cockpit_summary(res):
    """
    Renders terminal summary table and mistake autopsies.
    """
    print(f"\n{CYAN}{BOLD}========================================================================{RESET}")
    print(f"{BOLD}                EXAMINATION SIMULATION SCORECARD                        {RESET}")
    print(f"{CYAN}{BOLD}========================================================================{RESET}")

    score_pct = (res['score'] / res['maxScore']) * 100
    perf_color = GREEN if score_pct >= 75 else (YELLOW if score_pct >= 50 else RED)

    print(f"  Test Session:     {BOLD}{res['title']}{RESET}")
    print(f"  Total Score:      {perf_color}{BOLD}{res['score']} / {res['maxScore']}{RESET} ({score_pct:.1f}%)")
    print(f"  Accuracy:         {perf_color}{BOLD}{res['accuracy']}%{RESET}")
    print(f"  Attempt Rate:     {res['attempted']} / {res['totalQs']} Qs ({(res['attempted']/res['totalQs'])*100:.1f}%)")
    print(f"  Pacing Latency:   {CYAN}{res['avgLatencySec']}s / Question{RESET} (Time: {res['timeTakenMin']} min)")
    print(f"  Errors Detected:  {RED if res['wrongCount'] > 0 else GREEN}{BOLD}{res['wrongCount']} Incorrect Autopsies{RESET}")
    print(f"{CYAN}------------------------------------------------------------------------{RESET}")

    print(f"{BOLD}Subject Breakdown:{RESET}")
    for sub, stats in res['subjectBreakdown'].items():
        sub_acc = round((stats['correct'] / max(1, stats['attempted'])) * 100, 1)
        sub_col = GREEN if sub_acc >= 75 else (YELLOW if sub_acc >= 50 else RED)
        print(f"  • {sub:12} Score: {stats['score']:>3} pts | Acc: {sub_col}{sub_acc:>5}%{RESET} | Correct: {stats['correct']:>2} | Wrong: {stats['wrong']:>2}")

    print(f"{CYAN}------------------------------------------------------------------------{RESET}")
    print(f"{BOLD}Detected Error Autopsies ({min(4, len(res['mistakes']))} of {len(res['mistakes'])}):{RESET}")

    for idx, m in enumerate(res['mistakes'][:4]):
        cat_badge = f"{RED}[{m['errorCategory']}]{RESET}"
        print(f"  {BOLD}Q#{m['qNum']:02d}{RESET} {cat_badge} {m['subject']} ({m['chapter']})")
        print(f"     Marked: {RED}{m['markedOption']}{RESET}  ->  Correct: {GREEN}{m['correctOption']}{RESET}  ({m['timeSpentSec']}s)")
        print(f"     {DIM}{m['reasonDetail']}{RESET}")

    if len(res['mistakes']) > 4:
        print(f"  {DIM}... plus {len(res['mistakes']) - 4} more autopsies queued in Task Kanban.{RESET}")

    print(f"{CYAN}{BOLD}========================================================================{RESET}\n")


def interactive_menu():
    print_banner()
    print("Select an operation mode:")
    print("  [1] Run Full 75-Q JEE Main Simulation & Check for Errors")
    print("  [2] Run Physics 25-Q Speed & Latency Drill")
    print("  [3] Run Chemistry 25-Q Accuracy Drill")
    print("  [4] Run Mathematics 25-Q Advanced Drill")
    print("  [5] Run Stress Test (High Error & Trap Misconception Rate)")
    print("  [6] Audit Master Question Bank Integrity & LaTeX Consistency")
    print("  [Q] Exit")

    choice = input("\nEnter choice [1-6, Q]: ").strip().upper()

    if choice == "1":
        res = run_simulation(subject="Full", count=75, profile="balanced", target_latency=75)
        display_cockpit_summary(res)
        send_to_main_control(res)
    elif choice == "2":
        res = run_simulation(subject="Physics", count=25, profile="balanced", target_latency=75)
        display_cockpit_summary(res)
        send_to_main_control(res)
    elif choice == "3":
        res = run_simulation(subject="Chemistry", count=25, profile="balanced", target_latency=60)
        display_cockpit_summary(res)
        send_to_main_control(res)
    elif choice == "4":
        res = run_simulation(subject="Maths", count=25, profile="balanced", target_latency=120)
        display_cockpit_summary(res)
        send_to_main_control(res)
    elif choice == "5":
        res = run_simulation(subject="Full", count=75, profile="stress", target_latency=60)
        display_cockpit_summary(res)
        send_to_main_control(res)
    elif choice == "6":
        audit_question_bank()
    elif choice == "Q":
        print("[*] Exiting ClockEE Simulation Engine.")
        sys.exit(0)
    else:
        print("[!] Invalid option. Running default Full 75-Q Simulation...")
        res = run_simulation(subject="Full", count=75, profile="balanced")
        display_cockpit_summary(res)
        send_to_main_control(res)


def main():
    parser = argparse.ArgumentParser(description="ClockEE Autonomous Simulation Engine & Error Dispatcher")
    parser.add_argument("--subject", choices=["Physics", "Chemistry", "Maths", "Full"], default="Full", help="Subject domain")
    parser.add_argument("--count", type=int, default=75, help="Number of questions to simulate")
    parser.add_argument("--profile", choices=["topper", "balanced", "stress"], default="balanced", help="Candidate skill profile")
    parser.add_argument("--latency", type=int, default=75, help="Target latency in seconds per question")
    parser.add_argument("--audit-bank", action="store_true", help="Audit question bank integrity without running simulation")
    parser.add_argument("--no-send", action="store_true", help="Do not send report to Main Control API or DB")
    parser.add_argument("--host", default="127.0.0.1", help="Main Control server host")
    parser.add_argument("--port", type=int, default=8000, help="Main Control server port")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive cockpit menu")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Default to running full simulation directly
        print_banner()
        res = run_simulation(subject="Full", count=75, profile="balanced", target_latency=75)
        display_cockpit_summary(res)
        send_to_main_control(res, host=args.host, port=args.port)
        return

    print_banner()

    if args.interactive:
        interactive_menu()
        return

    if args.audit_bank:
        audit_question_bank()
        return

    res = run_simulation(
        subject=args.subject,
        count=args.count,
        profile=args.profile,
        target_latency=args.latency
    )

    display_cockpit_summary(res)

    if not args.no_send:
        send_to_main_control(res, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
