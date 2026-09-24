"""
Stage 5: re-runs the same DIRECT_ATTACKS against gpt-oss-20b both WITH
and WITHOUT the firewall, multiple trials per attack, since LLM outputs
aren't perfectly deterministic even at temperature=0.

Run:
    python run_firewall_comparison.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import build_agent
from attacks.direct import DIRECT_ATTACKS
from evaluation.evaluator import run_attack_trials, save_attack_result

#MODEL = "openai/gpt-oss-20b"
MODEL = "liquid/lfm-2.5-2.6b:free"
N_TRIALS = 1

if __name__ == "__main__":
    for use_firewall in [False, True]:
        label = "WITH firewall" if use_firewall else "WITHOUT firewall"
        print(f"\n=== {label} ({MODEL}), {N_TRIALS} trials per attack ===\n")

        agent = build_agent(model_override=MODEL, use_firewall=use_firewall)

        for attack in DIRECT_ATTACKS:
            outcomes = run_attack_trials(agent, attack, firewall_enabled=use_firewall, n_trials=N_TRIALS)

            compromised_count = sum(1 for o in outcomes if o["instruction_compromised"] == "yes")
            unauthorized_count = sum(1 for o in outcomes if o["unauthorized_tool_call"] == "yes")
            accessed_count = sum(1 for o in outcomes if o["protected_data_accessed"] == "yes")

            print(f"--- {attack['name']} ---")
            print(f"  compromised: {compromised_count}/{N_TRIALS}")
            print(f"  unauthorized_tool_call: {unauthorized_count}/{N_TRIALS}")
            print(f"  protected_data_accessed: {accessed_count}/{N_TRIALS}")
            print()

            for i, outcome in enumerate(outcomes):
                save_attack_result(
                    attack_name=f"{attack['name']}__{MODEL}__fw={use_firewall}__trial{i}",
                    category="direct",
                    prompt=attack["prompt"],
                    firewall_enabled=use_firewall,
                    outcome=outcome,
                )

    print("Done. Results saved to attack_results table.")