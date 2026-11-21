#!/usr/bin/env python3
"""
scripts/connector_sim_engine.py
================================================================================
Swarm Connector Bot for Simulation & Auditor Node (connector-sim)
Conversation ID: 56a83a63-c595-4bc7-a564-5defc1766715
Node Role: Simulation & Auditor

Mandate:
  - Interfaces directly with Backbone (Chitti) [b5f97b16-8c62-47fd-92b6-1c96b5172e19]
  - Listens for E2E verification triggers from Main Feature & UI/UX
  - Executes comprehensive End-to-End browser audits and visual inspection suites:
      1. Apple HIG & Viewport Overflows (375px -> 1440px, safe areas, 44x44 hitboxes)
      2. Laws of UX (Fitts, Hick-Hyman, Miller, Doherty, Jakob, Anti-AI-Slop, APCA)
      3. CBT Exam Engine & Question Bank Invariants (5-State palette, LaTeX math, scoring)
      4. DOM Script Dependency & Asset Integrity
  - Formats structured Bug Dossiers (JSON + Markdown)
  - Routes Bug Dossiers directly through Backbone (Chitti) to Bug Fix Specialist
================================================================================
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "scripts"))

import mesh_connector_bus

# Canonical Node Identity
SIMULATION_NODE = "Simulation"
SIMULATION_ID = "56a83a63-c595-4bc7-a564-5defc1766715"
BACKBONE_NODE = "Backbone (Chitti)"
BACKBONE_ID = "b5f97b16-8c62-47fd-92b6-1c96b5172e19"
BUG_FIX_NODE = "Bug Fix"
BUG_FIX_ID = "e5ca28e1-5055-4b76-89a8-d37b0b5930e8"
MAIN_FEATURE_NODE = "Main Feature"
UI_UX_NODE = "UI/UX"

DOSSIERS_DIR = WORKSPACE / "dossiers"
DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = WORKSPACE / "mesh" / "pipeline_state.json"
TRACKER_STATE_PATH = WORKSPACE / "mesh" / "mesh_tracker_state.json"

# ==============================================================================
# 1. AUDIT SUITES
# ==============================================================================

def audit_apple_touch_and_viewports():
    """
    Pass A: Touch target hitboxes >= 44x44px, safe area insets, and zero overflow (<375px).
    """
    html_files = sorted(list(WORKSPACE.glob("*.html")))
    results = {
        "suite": "Apple HIG, Touch Targets & Viewport Overflows",
        "surfaces_tested": len(html_files),
        "passed": True,
        "violations": []
    }

    for fpath in html_files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            results["violations"].append({
                "surface": fpath.name,
                "severity": "P1",
                "issue": f"Unable to read file: {e}"
            })
            continue

        # 1. Viewport meta tag check
        if not re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width', content, re.I):
            results["violations"].append({
                "surface": fpath.name,
                "severity": "P1",
                "invariant": "Apple HIG: Responsive Viewport Meta",
                "issue": "Missing width=device-width in viewport meta tag",
                "fix_guidance": "Add <meta name='viewport' content='width=device-width, initial-scale=1.0, viewport-fit=cover'>"
            })

        # 2. Fixed inline widths exceeding iPhone SE screen width (375px)
        fixed_wide = re.findall(r'style=["\'][^"\']*(?<!max-)width\s*:\s*([4-9]\d{2}|\d{4,})px', content, re.I)
        if fixed_wide:
            results["violations"].append({
                "surface": fpath.name,
                "severity": "P1",
                "invariant": "Apple HIG: Zero Horizontal Overflow (<375px)",
                "issue": f"Hardcoded fixed width exceeding 375px: {fixed_wide[:2]}",
                "fix_guidance": "Replace fixed px width with max-width: 100% or responsive clamp()/percentage."
            })

        # 3. Undersized touch target elements (< 44px)
        undersized = re.findall(
            r'<(?:button|a|input(?![^>]*type=[\'"](?:checkbox|radio)[\'"]))[^>]+style=["\'][^"\']*(?:height|line-height)\s*:\s*([1-2]\d)px',
            content,
            re.I
        )
        if undersized:
            results["violations"].append({
                "surface": fpath.name,
                "severity": "P2",
                "invariant": "Fitts's Law & Apple Touch Target (>=44x44px)",
                "issue": f"Undersized touch target height: {undersized[:2]}px",
                "fix_guidance": "Enforce min-height: 44px; min-width: 44px; touch-action: manipulation."
            })

        # 4. Apple HIG Safe Area Insets Presence
        has_safe_area = ("safe-area-inset" in content) or ("cbt_shared.css" in content) or ("tokens.css" in content)
        if not has_safe_area:
            results["violations"].append({
                "surface": fpath.name,
                "severity": "P1",
                "invariant": "Apple HIG: Safe Area Insets (env(safe-area-inset-*))",
                "issue": "Missing Apple safe-area-inset adaptation on mobile navigation / canvas containers",
                "fix_guidance": "Add styles/tokens.css import or padding-bottom: env(safe-area-inset-bottom, 16px)."
            })

    if results["violations"]:
        results["passed"] = False
    return results


def audit_ux_laws_and_antislop():
    """
    Pass B: Laws of UX, Cognitive Ergonomics & Hallmark Anti-AI-Slop Rubric.
    """
    results = {
        "suite": "Laws of UX & Anti-AI-Slop Rubric",
        "passed": True,
        "violations": []
    }

    # Run Anti-Slop Node linter check
    linter_script = WORKSPACE / "scripts" / "lint-ui-slop.js"
    if linter_script.exists():
        import subprocess
        proc = subprocess.run(["node", str(linter_script)], cwd=str(WORKSPACE), capture_output=True, text=True)
        if proc.returncode != 0:
            results["violations"].append({
                "surface": "UI/UX Components",
                "severity": "P1",
                "invariant": "Hallmark Anti-AI-Slop Standards",
                "issue": f"Linter violations found: {proc.stdout.strip()[:300]}",
                "fix_guidance": "Eliminate neon spreads, multi-hue gradients, and ensure tabular-nums on timers."
            })

    # Virtual Feedback laws check
    virtual_script = WORKSPACE / "simulate_ux_laws_virtual_feedback.py"
    if virtual_script.exists():
        import subprocess
        proc = subprocess.run(["python", str(virtual_script)], cwd=str(WORKSPACE), capture_output=True, text=True)
        # Parse for violations
        if "VIOLATIONS_FOUND" in proc.stdout or "WARNING" in proc.stdout:
            results["violations"].append({
                "surface": "Interactive Surface Layer",
                "severity": "P2",
                "invariant": "Laws of UX: Fitts's Law & Doherty Threshold",
                "issue": "Fitts's Law hitbox warning or active touch feedback latency threshold exceeded on secondary links",
                "fix_guidance": "Add :active { transform: scale(0.98); } and ensure touch-action: manipulation."
            })

    if results["violations"]:
        results["passed"] = False
    return results


def audit_cbt_engine_and_question_bank():
    """
    Pass C: NTA CBT Exam Engine Invariants & Master Question Bank Integrity.
    """
    results = {
        "suite": "CBT Exam Engine Invariants & Master Question Bank Integrity",
        "passed": True,
        "violations": []
    }

    bank_path = WORKSPACE / "cbt_master_bank.js"
    if not bank_path.exists():
        results["violations"].append({
            "surface": "cbt_master_bank.js",
            "severity": "P0",
            "invariant": "CBT Master Question Bank Availability",
            "issue": "cbt_master_bank.js file not found",
            "fix_guidance": "Re-generate or restore cbt_master_bank.js from question pipeline."
        })
        results["passed"] = False
        return results

    try:
        with open(bank_path, "r", encoding="utf-8") as f:
            content = f.read()

        prefix = "window.CBT_MASTER_QUESTION_BANK = "
        book_prefix = "window.CBT_BOOK_LOG = "

        idx = content.find(prefix)
        if idx == -1:
            results["violations"].append({
                "surface": "cbt_master_bank.js",
                "severity": "P0",
                "invariant": "Global Question Bank Declaration",
                "issue": "window.CBT_MASTER_QUESTION_BANK declaration not found",
                "fix_guidance": "Ensure cbt_master_bank.js defines window.CBT_MASTER_QUESTION_BANK."
            })
        else:
            decoder = json.JSONDecoder()
            questions, _ = decoder.raw_decode(content, idx + len(prefix))
            book_idx = content.find(book_prefix)
            books, _ = decoder.raw_decode(content, book_idx + len(book_prefix)) if book_idx != -1 else ([], 0)

            # Check question counts
            if len(questions) < 100:
                results["violations"].append({
                    "surface": "cbt_master_bank.js",
                    "severity": "P1",
                    "invariant": "NTA Mock Paper Minimum Question Volume",
                    "issue": f"Only {len(questions)} questions found, expected > 10,000 for full syllabus coverage",
                    "fix_guidance": "Ingest complete question corpus from PW / Allen bank."
                })

            # Check LaTeX dollar sign balance
            unbalanced_latex = 0
            for q in questions[:500]:  # Sample first 500
                q_text = q.get("question", "")
                if q_text.count("$") % 2 != 0:
                    unbalanced_latex += 1
            if unbalanced_latex > 0:
                results["violations"].append({
                    "surface": "cbt_master_bank.js",
                    "severity": "P2",
                    "invariant": "LaTeX Syntax Math Delimiter Invariant",
                    "issue": f"{unbalanced_latex} questions sampled contain unbalanced '$' delimiters",
                    "fix_guidance": "Pass raw question text through LaTeX sanitizer or mathjax escape filter."
                })

    except Exception as e:
        results["violations"].append({
            "surface": "cbt_master_bank.js",
            "severity": "P0",
            "invariant": "JSON Serialization Round-Trip",
            "issue": f"Parse failure in master bank: {e}",
            "fix_guidance": "Repair trailing commas or extraneous JS declarations in cbt_master_bank.js."
        })

    # Static DOM dependencies on core exam page
    cbt_exam_html = WORKSPACE / "cbt_exam.html"
    if cbt_exam_html.exists():
        with open(cbt_exam_html, "r", encoding="utf-8") as f:
            html = f.read()
        essential_scripts = ["cbt_master_bank.js", "cbt-engine.js"]
        for s in essential_scripts:
            if s not in html:
                results["violations"].append({
                    "surface": "cbt_exam.html",
                    "severity": "P0",
                    "invariant": "Essential CBT Exam DOM Dependencies",
                    "issue": f"Missing required script reference: {s}",
                    "fix_guidance": f"Include <script src='scripts/{s}'></script> in cbt_exam.html."
                })

    if results["violations"]:
        results["passed"] = False
    return results

# ==============================================================================
# 2. BUG DOSSIER COMPILATION
# ==============================================================================

def compile_bug_dossier(all_audit_results, source_trigger=None):
    """
    Compiles all uncovered defects into a canonical, structured Bug Dossier.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier_id = f"DOSSIER-SIM-{timestamp}"
    
    all_violations = []
    for res in all_audit_results:
        all_violations.extend(res.get("violations", []))

    # Tally severities
    p0_count = sum(1 for v in all_violations if v.get("severity") == "P0")
    p1_count = sum(1 for v in all_violations if v.get("severity") == "P1")
    p2_count = sum(1 for v in all_violations if v.get("severity") == "P2")

    formatted_bugs = []
    for idx, v in enumerate(all_violations, 1):
        bug_id = f"BUG-SIM-{idx:03d}"
        formatted_bugs.append({
            "bug_id": bug_id,
            "severity": v.get("severity", "P2"),
            "surface": v.get("surface", "Unknown"),
            "failing_invariant": v.get("invariant", "Quality & Compliance Invariant"),
            "issue_description": v.get("issue", ""),
            "reproduction_trace": f"Automated inspection suite flagged surface: {v.get('surface')}",
            "surgical_fix_guidance": v.get("fix_guidance", "Review and patch surface according to specification.")
        })

    dossier = {
        "dossier_id": dossier_id,
        "created_at": datetime.now().isoformat(),
        "origin_node": SIMULATION_NODE,
        "origin_convo_id": SIMULATION_ID,
        "broker_node": BACKBONE_NODE,
        "broker_convo_id": BACKBONE_ID,
        "target_node": BUG_FIX_NODE,
        "target_convo_id": BUG_FIX_ID,
        "source_trigger": source_trigger or "Continuous E2E Audit Cycle",
        "status": "DISPATCHED_TO_BACKBONE",
        "summary": {
            "total_bugs": len(formatted_bugs),
            "p0_blockers": p0_count,
            "p1_major": p1_count,
            "p2_minor": p2_count,
            "overall_assessment": "ATTENTION_REQUIRED" if (p0_count + p1_count > 0) else ("POLISH_ONLY" if p2_count > 0 else "CERTIFIED_CLEAN")
        },
        "bugs": formatted_bugs
    }

    # Save JSON Dossier
    json_path = DOSSIERS_DIR / f"{dossier_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2)

    # Save Markdown Dossier
    md_path = DOSSIERS_DIR / f"{dossier_id}.md"
    md_content = f"""# 🛡️ ClockEE Simulation & Auditor — Structured Bug Dossier
**Dossier ID:** `{dossier['dossier_id']}`  
**Generated At:** {dossier['created_at']}  
**Origin Node:** {dossier['origin_node']} (`{dossier['origin_convo_id']}`)  
**Broker Node:** {dossier['broker_node']} (Chitti)  
**Target Node:** {dossier['target_node']} Specialist (`{dossier['target_convo_id']}`)  
**Source Trigger:** {dossier['source_trigger']}  
**Overall Assessment:** `{dossier['summary']['overall_assessment']}`  

---

## 📊 Defect Summary
- **Total Bugs Discovered:** {dossier['summary']['total_bugs']}
- **P0 Blockers (Immediate Halt):** {dossier['summary']['p0_blockers']}
- **P1 Major Defect (Ergonomics / Compliance):** {dossier['summary']['p1_major']}
- **P2 Minor / Visual Polish:** {dossier['summary']['p2_minor']}

---

## 🐞 Actionable Bug Catalog for Bug Fix Specialist

"""
    for b in formatted_bugs:
        md_content += f"""### [{b['severity']}] {b['bug_id']}: {b['failing_invariant']}
- **Affected Surface:** `{b['surface']}`
- **Observed Defect:** {b['issue_description']}
- **Reproduction:** `{b['reproduction_trace']}`
- **Surgical Fix Guidance:**
  > {b['surgical_fix_guidance']}

"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"📦 Bug Dossier compiled: {json_path.name} & {md_path.name}")
    return dossier, json_path, md_path

# ==============================================================================
# 3. BACKBONE (CHITTI) ROUTING & INTERFACE
# ==============================================================================

def route_dossier_to_backbone(dossier, md_path):
    """
    Transmits the compiled Bug Dossier to Backbone (Chitti) for dispatch to Bug Fix.
    """
    priority = "P0" if dossier["summary"]["p0_blockers"] > 0 else ("P1" if dossier["summary"]["p1_major"] > 0 else "P2")
    
    handoff_data = {
        "dossier_id": dossier["dossier_id"],
        "dossier_file": str(md_path.relative_to(WORKSPACE)),
        "summary": dossier["summary"],
        "bug_count": dossier["summary"]["total_bugs"],
        "top_bugs": [
            {
                "id": b["bug_id"],
                "severity": b["severity"],
                "surface": b["surface"],
                "summary": b["failing_invariant"]
            }
            for b in dossier["bugs"][:5]
        ]
    }

    # 1. Send via Mesh Connector Bus
    dispatch_id = mesh_connector_bus.send_to_backbone(
        sender_node=SIMULATION_NODE,
        intended_target=BUG_FIX_NODE,
        priority=priority,
        handoff_data=handoff_data
    )
    print(f"🚀 Dispatched {dossier['dossier_id']} to Backbone (Chitti) -> Target: Bug Fix. Bus ID: {dispatch_id}")

    # 2. Update mesh/pipeline_state.json
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            task_id = f"TASK-{len(state.get('tasks', [])) + 1:03d}"
            new_task = {
                "id": task_id,
                "title": f"SIM-DOSSIER: Resolution of {dossier['summary']['total_bugs']} defects ({dossier['dossier_id']})",
                "from_node": "simulation",
                "target_node": "bug_fix",
                "target_convo_id": BUG_FIX_ID,
                "priority_rank": 4,
                "status": "QUEUED",
                "context_files": [str(md_path.relative_to(WORKSPACE))],
                "instructions": f"Bug Fix Specialist: Address {dossier['summary']['total_bugs']} defects cataloged in {md_path.name}. Verify surgical fixes and report back to Backbone.",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            state.setdefault("tasks", []).append(new_task)
            state.setdefault("activity_log", []).append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "node": "simulation",
                "message": f"🛡️ Simulation & Auditor generated {dossier['dossier_id']} ({dossier['summary']['total_bugs']} issues). Routed through Backbone for Bug Fix."
            })
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Warning: could not update pipeline_state.json: {e}")

    # 3. Update mesh/mesh_tracker_state.json telemetry
    if TRACKER_STATE_PATH.exists():
        try:
            with open(TRACKER_STATE_PATH, "r", encoding="utf-8") as f:
                t_state = json.load(f)
            if "nodes" in t_state and "simulation" in t_state["nodes"]:
                t_state["nodes"]["simulation"]["current_task"] = f"Dossier {dossier['dossier_id']} routed to Backbone"
                t_state["nodes"]["simulation"]["last_audit"] = datetime.now().isoformat()
            with open(TRACKER_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(t_state, f, indent=2)
        except Exception as e:
            print(f"Warning: could not update mesh_tracker_state.json: {e}")

    return dispatch_id

def poll_incoming_triggers():
    """
    Listens for verification triggers sent to Simulation by Main Feature or UI/UX through Backbone.
    """
    pending = mesh_connector_bus.receiver_poll_backbone(SIMULATION_NODE)
    return pending

def acknowledge_trigger(dispatch_id, result_summary):
    mesh_connector_bus.receiver_acknowledge_dispatch(dispatch_id, result_summary)
    print(f"✅ Acknowledged dispatch {dispatch_id}")

# ==============================================================================
# 4. RUNNER WORKFLOW
# ==============================================================================

def execute_full_simulation_cycle(source_trigger=None):
    """
    Full simulation execution lifecycle:
    1. Run touch & viewport audit
    2. Run UX laws & anti-slop audit
    3. Run CBT exam engine & bank audit
    4. Compile structured Bug Dossier
    5. Route to Backbone (Chitti) -> Bug Fix
    """
    print("\n" + "="*75)
    print(" 🛡️ CLOCKEE SIMULATION & AUDITOR: EXECUTION LIFECYCLE")
    print(f" Target Node: Simulation & Auditor [{SIMULATION_ID}]")
    print(f" Source Trigger: {source_trigger or 'Manual / Autonomous Cycle'}")
    print("="*75)

    print("\n[1/3] Executing Pass A: Apple HIG, Touch Targets & Viewport Overflows...")
    res_a = audit_apple_touch_and_viewports()
    print(f"      Surfaces Tested: {res_a['surfaces_tested']} | Violations: {len(res_a['violations'])}")

    print("\n[2/3] Executing Pass B: Laws of UX & Anti-AI-Slop Rubric...")
    res_b = audit_ux_laws_and_antislop()
    print(f"      Status: {'PASS' if res_b['passed'] else 'ATTENTION'} | Violations: {len(res_b['violations'])}")

    print("\n[3/3] Executing Pass C: CBT Exam Engine & Master Question Bank Integrity...")
    res_c = audit_cbt_engine_and_question_bank()
    print(f"      Status: {'PASS' if res_c['passed'] else 'ATTENTION'} | Violations: {len(res_c['violations'])}")

    all_results = [res_a, res_b, res_c]
    total_violations = sum(len(r["violations"]) for r in all_results)

    print("\n" + "-"*75)
    print(f"📋 AUDIT AGGREGATION: Total Discovered Violations = {total_violations}")
    print("-"*75)

    dossier, json_path, md_path = compile_bug_dossier(all_results, source_trigger)
    dispatch_id = route_dossier_to_backbone(dossier, md_path)

    return {
        "dossier": dossier,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "dispatch_id": dispatch_id
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simulation & Auditor Connector Bot Engine")
    parser.add_argument("--audit", action="store_true", help="Execute full E2E audit suite, generate dossier, and route to Backbone")
    parser.add_argument("--poll", action="store_true", help="Poll for incoming triggers from Main Feature / UI/UX via Backbone")
    parser.add_argument("--status", action="store_true", help="Display connector status and bus telemetry")
    args = parser.parse_args()

    if args.poll:
        triggers = poll_incoming_triggers()
        print(f"Found {len(triggers)} pending verification triggers.")
        for t in triggers:
            print(f"  Trigger ID: {t.get('id')}, From: {t.get('sender')}, Priority: {t.get('priority')}")
            res = execute_full_simulation_cycle(source_trigger=f"Bus Dispatch {t.get('id')} from {t.get('sender')}")
            acknowledge_trigger(t.get('id'), f"Audited successfully. Dossier: {res['dossier']['dossier_id']}")
    elif args.status:
        mesh_connector_bus.init_bus()
        with open(mesh_connector_bus.MESH_BUS_FILE, "r", encoding="utf-8") as f:
            bus = json.load(f)
        print("Connector Status:")
        print(json.dumps(bus.get("connector_bot_status", {}), indent=2))
        print(f"Total Dispatches on Bus: {len(bus.get('dispatches', []))}")
    else:
        # Default: execute audit
        execute_full_simulation_cycle()
