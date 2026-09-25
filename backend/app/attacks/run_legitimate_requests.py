"""
Stage 7: runs legitimate (non-malicious) requests under the firewall to
measure the False Positive Rate. Also saves a firewall_enabled='no'
baseline pass for completeness, though false-positive rate only makes
sense WITH the firewall on.

Run:
    python run_legitimate_requests.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import build_agent
from attacks.legitimate import LEGITIMATE_REQUESTS
from evaluation.evaluator import run_attack, save_attack_result

MODEL = None   # uses whatever LLM_PROVIDER/model .env points at

if __name__ == "__main__":
    for use_firewall in [True, False]:
        label = "WITH firewall" if use_firewall else "WITHOUT firewall"
        print(f"\n=== {label} ===\n")

        agent = build_agent(model_override=MODEL, use_firewall=use_firewall)

        for req in LEGITIMATE_REQUESTS:
            outcome = run_attack(agent, req, firewall_enabled=use_firewall)
            save_attack_result(
                attack_name=f"{req['name']}__fw={use_firewall}",
                category="legitimate",
                prompt=req["prompt"],
                firewall_enabled=use_firewall,
                outcome=outcome,
            )
            print(f"--- {req['name']} ---")
            print(f"  response: {outcome['agent_final_response'][:150]}")
            print()

    print("Done.")