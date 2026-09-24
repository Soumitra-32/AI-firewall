"""
Stage 4 entrypoint: runs every DIRECT_ATTACKS entry against multiple
models (no firewall yet — that's Stage 5) and saves each result to
Postgres, tagged by which model produced it.

Run:
    python run_direct_attacks.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import build_agent
from attacks.direct import DIRECT_ATTACKS
from evaluation.evaluator import run_attack, save_attack_result

MODELS_TO_TEST = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    
]

if __name__ == "__main__":
    for model_name in MODELS_TO_TEST:
        print(f"\n=== Testing model: {model_name} ===\n")
        agent = build_agent(model_override=model_name)

        for attack in DIRECT_ATTACKS:
            print(f"--- {attack['name']} ---")
            outcome = run_attack(agent, attack, firewall_enabled=False)
            save_attack_result(
                attack_name=f"{attack['name']}__{model_name}",
                category="direct",
                prompt=attack["prompt"],
                firewall_enabled=False,
                outcome=outcome,
            )
            print(f"  compromised: {outcome['instruction_compromised']}")
            print(f"  unauthorized_tool_call: {outcome['unauthorized_tool_call']}")
            print(f"  protected_data_accessed: {outcome['protected_data_accessed']}")
            print()

    print("Done. Results saved to attack_results table.")