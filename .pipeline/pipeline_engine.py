#!/usr/bin/env python3
"""
ClockEE Autonomous Pipeline Engine
Daemon runner invoked on scheduled intervals and by the mesh poller.
Executes the unified ClockEE Mesh Orchestrator.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINE_DIR = ROOT_DIR / ".pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mesh_orchestrator import run_mesh_process

if __name__ == "__main__":
    run_mesh_process()
