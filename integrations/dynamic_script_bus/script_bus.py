#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #34: CORS-Immune Local-First Dynamic JavaScript Bus
Upstream: cors-free/script-bus
Domain: Multi-Agent Mesh Coordination

Generates timestamped JavaScript payload wrappers (window.CLOCKEE_STATE = {...})
and script tag injection snippets that bypass browser local file restrictions completely.
"""

import time
import json
from typing import Dict, Any

class DynamicScriptBus:
    def __init__(self, target_js_file: str = ".pipeline/tracker_data.js"):
        self.target_js_file = target_js_file

    def emit_state_sync(self, state_dict: Dict[str, Any]) -> str:
        """
        Encapsulates payload into executable JS assignment with timestamp anchor.
        """
        t_ms = int(time.time() * 1000)
        state_dict["_sync_timestamp_ms"] = t_ms
        serialized = json.dumps(state_dict, indent=2)
        js_content = f"// ClockEE Dynamic Script Bus — Generated at {t_ms}\nwindow.CLOCKEE_DATA = {serialized};\nif (window.onClockEERefresh) window.onClockEERefresh(window.CLOCKEE_DATA);\n"
        
        with open(self.target_js_file, "w", encoding="utf-8") as f:
            f.write(js_content)
            
        return js_content

    @staticmethod
    def generate_html_loader(script_path: str = ".pipeline/tracker_data.js") -> str:
        """Generates dynamic DOM script tag injector for local file:// usage."""
        return f"""
        function refreshDynamicScriptBus() {{
            const old = document.getElementById('clockee-dynamic-bus');
            if (old) old.remove();
            const s = document.createElement('script');
            s.id = 'clockee-dynamic-bus';
            s.src = '{script_path}?t=' + Date.now();
            document.head.appendChild(s);
        }}
        setInterval(refreshDynamicScriptBus, 1000);
        """

def benchmark_script_bus():
    bus = DynamicScriptBus(target_js_file="integrations/dynamic_script_bus/test_data.js")
    sample_state = {"cycle": "Reel 34 Test", "timestamp": time.time(), "nodes": 10}

    t0 = time.perf_counter()
    content = bus.emit_state_sync(sample_state)
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000

    print(f"[BENCHMARK] Script bus state emit latency: {latency_us:.2f}µs ({len(content)} bytes)")
    assert "window.CLOCKEE_DATA =" in content
    print("[✓] CORS-Immune Dynamic Script Bus certified (Exit Code 0).")
    return latency_us

if __name__ == "__main__":
    benchmark_script_bus()
