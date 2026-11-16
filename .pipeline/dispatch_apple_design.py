import json
import os
import sys
from agentapi_rpc import AgentAPIRPCClient

QUEUE_PATH = os.path.join(os.path.dirname(__file__), "queue.json")

def dispatch_apple_design():
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)

    active_convs = queue.get("active_conversations", {})
    client = AgentAPIRPCClient()

    # 1. Dispatch to SIMULATION
    sim_id = active_convs.get("simulation", {}).get("id")
    if sim_id:
        content = (
            "=== SPRINT DIRECTIVE: APPLE DESIGN LANGUAGE & MULTI-DEVICE RESPONSIVENESS AUDIT ===\n"
            "Target: SIMULATION (62adc180)\n"
            "Action Required:\n"
            "1. Run full responsiveness tests across all 24 HTML surfaces using scripts/verify_responsiveness.py.\n"
            "2. Audit against the 7 canonical Apple viewport specifications: iPhone SE (375px), iPhone 16 (390px), "
            "iPhone 16 Pro Max (430px), iPad Mini (768px), iPad Air (820px), iPad Pro (1024px), MacBook Pro (1440px).\n"
            "3. Verify zero horizontal overflow, touch target accessibility (min 44x44px), and proper safe-area padding.\n"
            "4. Verify Hallmark Anti-AI-Slop Linter maintains 100.0/100.\n"
            "5. Emit structured responsive audit report to BUG FIXES if any viewport clipping is observed."
        )
        lat = client.send_async(recipient_id=sim_id, content=content, title="[P0] Apple Design & Multi-Device Responsive Audit")
        print(f"✔ Dispatched to SIMULATION ({sim_id[:8]}...) in {lat:.2f}ms")

    # 2. Dispatch to BUG FIXES
    bf_id = active_convs.get("bug_fixes", {}).get("id")
    if bf_id:
        content = (
            "=== SPRINT DIRECTIVE: APPLE DESIGN POLISH & RESPONSIVE HOTFIXES ===\n"
            "Target: BUG FIXES (c05ee59e)\n"
            "Action Required:\n"
            "1. Receive responsive simulation feedback from SIMULATION.\n"
            "2. Surgically address any clipping or fixed width bottlenecks on compact mobile viewports (<480px).\n"
            "3. Ensure all cards and interactive controls use Apple Human Interface Guidelines: SF Pro font stack, "
            "hairline retina borders, subtle squircle corner radii (12px/16px/22px), and smooth cubic-bezier transitions.\n"
            "4. Eliminate any residual neon cyber glows, aggressive gradients, or gimmicky AI badges."
        )
        lat = client.send_async(recipient_id=bf_id, content=content, title="[P0] Apple Design Polish & Responsive Remediation")
        print(f"✔ Dispatched to BUG FIXES ({bf_id[:8]}...) in {lat:.2f}ms")

    # 3. Dispatch to UI / UX
    ui_id = active_convs.get("ui_ux", {}).get("id")
    if ui_id:
        content = (
            "=== SPRINT DIRECTIVE: APPLE HUMAN INTERFACE DESIGN SYSTEM CONVERGENCE ===\n"
            "Target: UI / UX (06a7d47b)\n"
            "Action Required:\n"
            "1. Standardize all 24 application views onto the Apple Design Language.\n"
            "2. Remove all gimmicky AI aesthetics, retro terminal styling, and cyan/purple glowing neon elements.\n"
            "3. Align interface typography to Apple SF Pro, frosted glass materials (backdrop-filter: blur(25px) saturate(190%)), "
            "and clean Apple System Blue (#0a84ff) accents.\n"
            "4. Maintain reference data catalog at data/clockee_master_data_catalog.json."
        )
        lat = client.send_async(recipient_id=ui_id, content=content, title="[P0] Apple HIG Convergence")
        print(f"✔ Dispatched to UI/UX ({ui_id[:8]}...) in {lat:.2f}ms")

    # 4. Dispatch to MAIN FEATURE
    mf_id = active_convs.get("untitled_conversation", {}).get("id")
    if mf_id:
        content = (
            "=== SPRINT DIRECTIVE: APPLE-GRADE APPLICATION WORKFLOWS & COPY CLEANUP ===\n"
            "Target: MAIN FEATURE (6371cba6)\n"
            "Action Required:\n"
            "1. Clean up application copy and interactive modal flows to feel like a high-caliber professional Apple tool.\n"
            "2. Strip out gimmicky AI buzzwords and futuristic hype phrasing across all pages.\n"
            "3. Ensure the 6,326 authentic question items (Physics: 2,671, Chemistry: 1,819, Maths: 1,836) render "
            "with clean KaTeX formulas, crisp diagrams, and zero visual stutter."
        )
        lat = client.send_async(recipient_id=mf_id, content=content, title="[P0] Apple-Grade Professional UX & Copy")
        print(f"✔ Dispatched to MAIN FEATURE ({mf_id[:8]}...) in {lat:.2f}ms")

if __name__ == "__main__":
    dispatch_apple_design()
