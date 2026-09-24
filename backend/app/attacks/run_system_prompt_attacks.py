"""
Stage 6b: runs SYSTEM_PROMPT_ATTACKS against a model, WITH and WITHOUT
the firewall (the firewall isn't expected to help here — it protects
tool execution, not the model's own text output — but we test both
conditions for completeness and to confirm that assumption).

Run:
    python run_system_prompt_attacks.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import build_agent, SYSTEM_PROMPT
from attacks.system_prompt import SYSTEM_PROMPT_ATTACKS
from evaluation.evaluator import run_system_prompt_attack, save_attack_result

MODEL = "openai/gpt-oss-20b"      # None = use whatever LLM_PROVIDER/model .env points at
N_TRIALS = 1

if __name__ == "__main__":
    for use_firewall in [False, True]:
        label = "WITH firewall" if use_firewall else "WITHOUT firewall"
        print(f"\n=== {label}, {N_TRIALS} trials per attack ===\n")

        agent = build_agent(model_override=MODEL, use_firewall=use_firewall)

        for attack in SYSTEM_PROMPT_ATTACKS:
            compromised_count = 0
            for trial in range(N_TRIALS):
                outcome = run_system_prompt_attack(
                    agent, attack, SYSTEM_PROMPT, firewall_enabled=use_firewall
                )
                if outcome["instruction_compromised"] == "yes":
                    compromised_count += 1

                save_attack_result(
                    attack_name=f"{attack['name']}__fw={use_firewall}__trial{trial}",
                    category="system_prompt",
                    prompt=attack["prompt"],
                    firewall_enabled=use_firewall,
                    outcome=outcome,
                )

            print(f"--- {attack['name']} ---")
            print(f"  compromised (prompt leaked or unauthorized action): {compromised_count}/{N_TRIALS}")
            print()

    print("Done. Results saved to attack_results table.")