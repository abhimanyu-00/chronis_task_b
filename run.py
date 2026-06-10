# run.py — single command execution

import json
import os
import subprocess

from engine.evidence import check_evidence
from engine.scorer import (
    get_behavioral_score,
    get_narrative_score
)
from engine.typer import classify
from engine.output import make_result, make_abstention
import sys

def load_data():
    # accept optional file argument
    # default to data/data.json if none provided
    filepath = sys.argv[1] if len(sys.argv) > 1 else "data/data.json"
    print(f"Loading data from: {filepath}")
    with open(filepath) as f:
        return json.load(f)

def run_pipeline(data):
    results = []

    for domain, content in data.items():
        behavior = content["behavior"]
        selftalk = content["selftalk"]

        # Step 1 — evidence check first
        evidence = check_evidence(domain, behavior, selftalk)

        if evidence["status"] == "insufficient_evidence":
            results.append(make_abstention(domain, evidence["reason"]))
            continue

        # Step 2 — score both sides
        b_score = get_behavioral_score(behavior)
        n_score = get_narrative_score(selftalk)

        # Step 3 — classify
        div_type, gap = classify(b_score, n_score, selftalk)

        # Step 4 — safe output
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
        print(f"Domain:   {r['domain'].upper()}")
        print(f"Status:   {r['status']}")

        if r["status"] == "insufficient_evidence":
            print(f"Reason:   {r['reason']}")
        else:
            print(f"Type:     {r['divergence_type']}")
            print(f"Gap:      {r['gap_score']}")
            print(f"Behavior: {r['behavioral_score']}")
            print(f"Narrative:{r['narrative_score']}")
            print(f"Note:     {r['evidence_note']}")

        print("-" * 50)


def run_tests():
    print("\n" + "="*50)
    print("CHRONIS TASK B — TEST RESULTS")
    print("="*50 + "\n")

    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode == 0:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
        print(result.stderr)

    print("="*50)


if __name__ == "__main__":
    data = load_data()
    results = run_pipeline(data)
    print_results(results)
    save_results(results)
    run_tests()