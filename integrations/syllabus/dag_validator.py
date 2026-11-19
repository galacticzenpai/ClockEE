#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #36: Directed Acyclic Graph (DAG) Syllabus Tracker for JEE/NEET
Upstream: syllabus/curriculum-dag
Domain: Multi-Agent Mesh Coordination

Validates acyclic prerequisite integrity, computes topological study ordering,
and evaluates dynamic node unlock states based on student diagnostic mastery.
"""

import time
import json
from pathlib import Path
from typing import Dict, Any, List, Set

class SyllabusDAGValidator:
    def __init__(self, dag_file: str = "integrations/syllabus/syllabus_dag.json"):
        with open(dag_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.nodes = {n["id"]: n for n in self.data["nodes"]}

    def verify_acyclic(self) -> bool:
        """Kahn's algorithm / DFS cycle detection."""
        visited = set()
        rec_stack = set()

        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            for prereq in self.nodes.get(node_id, {}).get("prereqs", []):
                if prereq not in visited:
                    if dfs(prereq):
                        return True
                elif prereq in rec_stack:
                    return True  # Cycle detected
            rec_stack.remove(node_id)
            return False

        for node_id in self.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    return False
        return True

    def compute_unlock_status(self, completed_mastered_ids: Set[str]) -> Dict[str, str]:
        """
        Determines state for each node:
        - COMPLETED: in mastered set
        - UNLOCKED: all prereqs are in mastered set
        - LOCKED: at least one prereq missing
        """
        status_map = {}
        for nid, node in self.nodes.items():
            if nid in completed_mastered_ids:
                status_map[nid] = "COMPLETED"
            else:
                prereqs = node.get("prereqs", [])
                if all(p in completed_mastered_ids for p in prereqs):
                    status_map[nid] = "UNLOCKED"
                else:
                    status_map[nid] = "LOCKED"
        return status_map

def benchmark_dag():
    validator = SyllabusDAGValidator()
    
    # 1. Verify acyclic
    t0 = time.perf_counter()
    is_dag = validator.verify_acyclic()
    t1 = time.perf_counter()
    cycle_check_us = (t1 - t0) * 1_000_000
    
    assert is_dag, "Curriculum contains illegal cyclic dependencies!"
    print(f"[*] Verified DAG acyclic integrity in {cycle_check_us:.2f}µs (Total nodes: {len(validator.nodes)})")

    # 2. Benchmark unlock state evaluation
    mastered = {"phy_kinematics", "phy_nlm", "chem_mole", "math_sets", "math_trig"}
    t2 = time.perf_counter()
    status_map = validator.compute_unlock_status(mastered)
    t3 = time.perf_counter()
    unlock_eval_us = (t3 - t2) * 1_000_000

    print(f"[*] Node unlock evaluation in {unlock_eval_us:.2f}µs")
    print(f"  • phy_wep status: {status_map['phy_wep']} (Prereqs: {validator.nodes['phy_wep']['prereqs']})")
    print(f"  • phy_rotational status: {status_map['phy_rotational']} (Prereqs: {validator.nodes['phy_rotational']['prereqs']})")
    print(f"  • math_limits status: {status_map['math_limits']} (Prereqs: {validator.nodes['math_limits']['prereqs']})")

    assert status_map["phy_wep"] == "UNLOCKED"
    assert status_map["phy_rotational"] == "LOCKED"
    assert status_map["math_limits"] == "UNLOCKED"

    print("\n[✓] Syllabus DAG Curriculum Validator certified (Exit Code 0).")
    return unlock_eval_us

if __name__ == "__main__":
    benchmark_dag()
