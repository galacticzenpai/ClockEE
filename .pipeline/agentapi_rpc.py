import os
import subprocess
import time
from typing import Dict, Any, Optional

AGENTAPI_BIN = r"C:\Users\Kunal\.gemini\antigravity\bin\agentapi.bat"

class AgentAPIRPCClient:
    """
    Sub-5ms non-blocking inter-conversation RPC client for ClockEE mesh.
    Dispatches prompts asynchronously via subprocess.Popen.
    """
    def __init__(self, bin_path: str = AGENTAPI_BIN):
        self.bin_path = bin_path

    def send_async(self, recipient_id: str, content: str, title: Optional[str] = None) -> float:
        """
        Dispatches message non-blockingly. Returns caller dispatch latency in milliseconds.
        """
        t0 = time.perf_counter()
        cmd = [self.bin_path, "send-message"]
        if title:
            cmd.append(f"--title={title}")
        cmd.extend([recipient_id, content])

        try:
            # Popen returns immediately without waiting for child exit
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
        except Exception as e:
            print(f"[AgentAPIRPC] Error launching subprocess: {e}")

        t1 = time.perf_counter()
        return (t1 - t0) * 1000

def benchmark_rpc():
    client = AgentAPIRPCClient()
    # Test dispatch latency against SIMULATION conversation ID
    latencies = []
    for _ in range(5):
        lat = client.send_async(
            recipient_id="62adc180-be21-4671-848c-c8df59e2c202",
            content="PING: AgentAPI RPC latency check",
            title="Heartbeat RPC"
        )
        latencies.append(lat)
        time.sleep(0.01)

    avg_ms = sum(latencies) / len(latencies)
    print(f"[BENCHMARK] Non-blocking AgentAPI RPC caller dispatch latency: {avg_ms:.3f}ms (Target: <5ms SLA)")
    return avg_ms

if __name__ == "__main__":
    benchmark_rpc()
