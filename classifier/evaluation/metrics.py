"""RQ1 metrics for MentalBERT and the GPT-5.4 baseline (proposal Section 3.7, EV-3, EV-8).

Scores every saved run the same way:
  - accuracy and macro F1;
  - precision and recall per class, Suicidal reported first;
  - the confusion matrix;
  - 95% intervals (Wilson for proportions, bootstrap for macro F1);
  - the Suicidal check at the routing thresholds, held fixed at their CP1 values: how many
    entries would reach Crisis (top label Suicidal, or P(Suicidal) at least 0.35) or at
    least Heightened-caution (P(Suicidal) at least 0.15) from the classifier alone. Mood
    ratings, which can also escalate a route in the app, are not part of this dataset.

An entry a model gave no answer for counts as wrong. This script interprets nothing.

Run from the classifier folder, with the venv active:
    python evaluation/metrics.py
"""

import json
import sys
from pathlib import Path

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intervals import bootstrap_macro_f1, wilson  # noqa: E402

RESULTS = Path(__file__).resolve().parent / "results"
RUNS = {
    "MentalBERT": "mentalbert-predictions.json",
    "GPT-5.4 (defined prompt, primary)": "baseline-predictions-defined.json",
    "GPT-5.4 (bare prompt, secondary)": "baseline-predictions-bare.json",
}
LABELS = ["suicidal", "anxiety", "depression", "normal"]  # Suicidal first: the priority metric
CRISIS, HEIGHTENED = 0.35, 0.15


def p_suicidal(prediction):
    probabilities = prediction.get("probabilities") or {}
    return {key.lower(): value for key, value in probabilities.items()}.get("suicidal")


def routing_check(predictions):
    """Classifier-only route reached by each entry, counted for suicidal and other entries."""
    counts = {"suicidal_entries": 0, "crisis": 0, "at_least_heightened": 0,
              "other_entries": 0, "other_crisis": 0, "other_at_least_heightened": 0}
    for p in predictions:
        score = p_suicidal(p)
        crisis = p["predicted"] == "suicidal" or (score is not None and score >= CRISIS)
        heightened = crisis or (score is not None and score >= HEIGHTENED)
        if p["intended"] == "suicidal":
            counts["suicidal_entries"] += 1
            counts["crisis"] += crisis
            counts["at_least_heightened"] += heightened
        else:
            counts["other_entries"] += 1
            counts["other_crisis"] += crisis
            counts["other_at_least_heightened"] += heightened
    for key in ("crisis", "at_least_heightened"):
        counts[key + "_ci"] = wilson(counts[key], counts["suicidal_entries"])
        counts["other_" + key + "_ci"] = wilson(counts["other_" + key], counts["other_entries"])
    return counts


def per_class(intended, predicted):
    precision = precision_score(intended, predicted, labels=LABELS, average=None, zero_division=0)
    recall = recall_score(intended, predicted, labels=LABELS, average=None, zero_division=0)
    out = {}
    for label, prec, rec in zip(LABELS, precision, recall):
        called = sum(p == label for p in predicted)
        actual = sum(i == label for i in intended)
        hits = sum(i == p == label for i, p in zip(intended, predicted))
        out[label] = {
            "precision": round(prec, 3), "precision_ci": wilson(hits, called),
            "recall": round(rec, 3), "recall_ci": wilson(hits, actual),
        }
    return out


def score(predictions):
    intended = [p["intended"] for p in predictions]
    predicted = [p["predicted"] or "no answer" for p in predictions]
    correct = sum(i == p for i, p in zip(intended, predicted))
    return {
        "entries": len(predictions),
        "no_answer": sum(p["predicted"] is None for p in predictions),
        "accuracy": round(accuracy_score(intended, predicted), 3),
        "accuracy_ci": wilson(correct, len(predictions)),
        "macro_f1": round(f1_score(intended, predicted, labels=LABELS, average="macro", zero_division=0), 3),
        "macro_f1_ci": bootstrap_macro_f1(intended, predicted, LABELS),
        "per_class": per_class(intended, predicted),
        "confusion_matrix": {
            "rows_intended_columns_predicted": LABELS,
            "counts": confusion_matrix(intended, predicted, labels=LABELS).tolist(),
        },
        "routing_check": routing_check(predictions),
    }


def show(name, result):
    def ci(value, interval):
        return f"{value:.2f} ({interval[0]:.2f}-{interval[1]:.2f})"

    print(f"\n{name}   ({result['no_answer']} without an answer)")
    print(f"  accuracy {ci(result['accuracy'], result['accuracy_ci'])}   "
          f"macro F1 {ci(result['macro_f1'], result['macro_f1_ci'])}")
    print(f"  {'class':<12}{'precision':<20}recall")
    for label, m in result["per_class"].items():
        print(f"  {label:<12}{ci(m['precision'], m['precision_ci']):<20}{ci(m['recall'], m['recall_ci'])}")
    r = result["routing_check"]
    print(f"  suicidal entries reaching Crisis: {r['crisis']}/{r['suicidal_entries']}, "
          f"at least Heightened: {r['at_least_heightened']}/{r['suicidal_entries']}")
    print(f"  other entries reaching Crisis: {r['other_crisis']}/{r['other_entries']}, "
          f"at least Heightened: {r['other_at_least_heightened']}/{r['other_entries']}")
    print(f"  confusion matrix (rows intended, columns predicted: {', '.join(LABELS)})")
    for label, row in zip(LABELS, result["confusion_matrix"]["counts"]):
        print(f"    {label:<12}{row}")


def main():
    report = {}
    for name, file in RUNS.items():
        path = RESULTS / file
        if not path.exists():
            print(f"\n{name}: no saved run yet ({file})")
            continue
        report[name] = score(json.loads(path.read_text(encoding="utf-8"))["predictions"])
        show(name, report[name])
    out = RESULTS / "metrics.json"
    out.write_text(json.dumps({"thresholds": {"crisis": CRISIS, "heightened": HEIGHTENED},
                               "results": report}, indent=2), encoding="utf-8")
    print(f"\nSaved to results/{out.name}")


if __name__ == "__main__":
    main()
