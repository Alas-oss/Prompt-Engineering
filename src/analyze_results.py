import json
from collections import defaultdict

def load_results():
    with open("data/results.json", "r", encoding="utf-8") as f:
        return json.load(f)

def compute_averages(results):
    scores_by_technique = defaultdict(lambda: {
        "accuracy": [],
        "conciseness": [],
        "consistency": []
    })

    for entry in results:
        technique = entry["technique"]
        scores = entry["scores"]

        if scores["accuracy"] is not None:
            scores_by_technique[technique]["accuracy"].append(scores["accuracy"])
        if scores["conciseness"] is not None:
            scores_by_technique[technique]["conciseness"].append(scores["conciseness"])
        if scores["consistency"] is not None:
            scores_by_technique[technique]["consistency"].append(scores["consistency"])

    averages = {}
    for technique, dims in scores_by_technique.items():
        acc = dims["accuracy"]
        con = dims["conciseness"]
        cst = dims["consistency"]

        averages[technique] = {
            "accuracy":    round(sum(acc) / len(acc), 2) if acc else None,
            "conciseness": round(sum(con) / len(con), 2) if con else None,
            "consistency": round(sum(cst) / len(cst), 2) if cst else None,
            "overall":     round(
                (sum(acc + con + cst)) / (len(acc + con + cst)), 2
            ) if acc else None
        }

    return averages

def print_table(averages):
    print("\n── Results Summary ──────────────────────────────────────────")
    print(f"{'Technique':<20} {'Accuracy':>10} {'Conciseness':>12} {'Consistency':>12} {'Overall':>10}")
    print("─" * 68)

    sorted_techniques = sorted(
        averages.items(),
        key=lambda x: x[1]["overall"] or 0,
        reverse=True
    )

    for technique, scores in sorted_techniques:
        print(
            f"{technique:<20} "
            f"{str(scores['accuracy']):>10} "
            f"{str(scores['conciseness']):>12} "
            f"{str(scores['consistency']):>12} "
            f"{str(scores['overall']):>10}"
        )

    print("─" * 68)
    winner = sorted_techniques[0][0]
    print(f"\n Optimal performing technique: {winner} (overall average: {sorted_techniques[0][1]['overall']})")

if __name__ == "__main__":
    results = load_results()
    averages = compute_averages(results)
    print_table(averages)
