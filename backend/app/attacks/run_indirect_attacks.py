"""
Stage 6: runs indirect injection attacks against a model, both WITH and
WITHOUT the firewall, mirroring the direct-attack comparison in Stage 5.

Run:
    python run_indirect_attacks.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import build_agent
from attacks.indirect import INDIRECT_ATTACKS
from evaluation.evaluator import run_attack_trials, save_attack_result

#MODEL = "openai/gpt-oss-20b"         # None = use whatever LLM_PROVIDER/model .env points at
MODEL = None
N_TRIALS = 1         # keep low to respect free-tier rate limits

if __name__ == "__main__":
    for use_firewall in [False, True]:
        label = "WITH firewall" if use_firewall else "WITHOUT firewall"
        print(f"\n=== {label}, {N_TRIALS} trials per attack ===\n")

        agent = build_agent(model_override=MODEL, use_firewall=use_firewall)

        for attack in INDIRECT_ATTACKS:
            outcomes = run_attack_trials(agent, attack, firewall_enabled=use_firewall, n_trials=N_TRIALS)

            compromised = sum(1 for o in outcomes if o["instruction_compromised"] == "yes")
            unauthorized = sum(1 for o in outcomes if o["unauthorized_tool_call"] == "yes")
            accessed = sum(1 for o in outcomes if o["protected_data_accessed"] == "yes")

            print(f"--- {attack['name']} ---")
            print(f"  compromised: {compromised}/{N_TRIALS}")
            print(f"  unauthorized_tool_call: {unauthorized}/{N_TRIALS}")
            print(f"  protected_data_accessed: {accessed}/{N_TRIALS}")
            print()

            for i, outcome in enumerate(outcomes):
                save_attack_result(
                    attack_name=f"{attack['name']}__fw={use_firewall}__trial{i}",
                    category="indirect",
                    prompt=attack["prompt"],
                    firewall_enabled=use_firewall,
                    outcome=outcome,
                )

    print("Done. Results saved to attack_results table.")