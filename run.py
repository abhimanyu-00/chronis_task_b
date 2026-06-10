# run.py — single command execution
# PDF requirement: "single-command runnable script"
# Usage: python run.py

import json
import os
from engine.evidence import check_evidence
from engine.scorer import (
    get_behavioral_score,
    get_narrative_score
)
from engine.typer import classify
from engine.output import make_result, make_abstention


def load_data():
    with open("data/data.json") as f:
        return json.load(f)

def run_pipeline(data):
    results = []

    for domain, content in data.items():
        behavior = content["behavior"]
        selftalk = content["selftalk"]

        # evidence check
        evidence = check_evidence(domain, behavior, selftalk)

        if evidence["status"] == "insufficient_evidence":
            results.append(make_abstention(domain, evidence["reason"]))
            continue

        # scoring
        b_score = get_behavioral_score(behavior)
        n_score = get_narrative_score(selftalk)

        # classify
        div_type, gap = classify(b_score, n_score, selftalk)

        # output
        result = make_result(
            domain=domain,
            divergence_type=div_type,
            gap=gap,
            behavioral_score=b_score,
            narrative_score=n_score,
            behavioral_summary=f"behavioral score {round(b_score,2)} across {len(behavior)} days",
            narrative_summary=f"narrative score {round(n_score,2)} from {len(selftalk)} snippet(s)",
            evidence_note=f"{len(behavior)} days of data, {len(selftalk)} snippet(s)"
        )
        results.append(result)

    return results


def save_results(results):
    os.makedirs("results", exist_ok=True)
    with open("results/output.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to results/output.json")


def print_results(results):
    print("\n" + "="*50)
    print("CHRONIS TASK B — DIVERGENCE SCORING RESULTS")
    print("="*50 + "\n")

    for r in results:
        print(f"Domain:  {r['domain'].upper()}")
        print(f"Status:  {r['status']}")

        if r["status"] == "insufficient_evidence":
            print(f"Reason:  {r['reason']}")
        else:
            print(f"Type:    {r['divergence_type']}")
            print(f"Gap:     {r['gap_score']}")
            print(f"Behavior:{r['behavioral_score']}")
            print(f"Narrative:{r['narrative_score']}")
            print(f"Note:    {r['evidence_note']}")

        print("-" * 50)


if __name__ == "__main__":
    data = load_data()
    results = run_pipeline(data)
    print_results(results)
    save_results(results)