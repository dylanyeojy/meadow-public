"""Compare ways of chunking an entry and combining chunk probabilities into one top label.

Re-scores the saved MentalBERT runs without running the model again. Every rule takes
P(Suicidal) as the maximum across chunks, so the Crisis threshold check is identical under
all of them; only the top label differs.

  A  CP1 rule (REQ_F302): 126-token chunks, mean of Anxiety, Depression and Normal
  B  Priority: Suicidal if A says so, else Depression if any chunk's top class is
     Depression, else Anxiety if any chunk's is Anxiety, else Normal
  C  Maximum of every class across chunks, then the highest class
  D  Leave out chunks whose top class is Normal (unless every chunk is Normal), take the
     mean of the rest, then the highest class
  E  As A, but each chunk weighted by its length (Dylan's combine_chunks_weighted)
  F  As A, but chunks cut at sentence boundaries (trial_sentence_chunks.py)
  G  Sentence-boundary chunks and length weighting together

E and G wait for combine_chunks_weighted; F and G wait for the sentence-chunk run.

Run from the classifier folder, with the venv active:
    python evaluation/compare_aggregation.py
"""

import json
import sys
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score, recall_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so combine.py can be imported
from combine import combine_chunks, combine_chunks_weighted  # noqa: E402
from intervals import bootstrap_macro_f1, wilson  # noqa: E402

EVALUATION_DIR = Path(__file__).resolve().parent
RESULTS = EVALUATION_DIR / "results"
CLASSES = ["Anxiety", "Depression", "Normal", "Suicidal"]
ROOM = 126  # tokens of text per 126-token chunk


def top(probabilities):
    return max(probabilities, key=probabilities.get)


def rule_a(p):
    return top(combine_chunks(p["chunk_probabilities"]))


def rule_b(p):
    if rule_a(p) == "Suicidal":
        return "Suicidal"
    chunk_tops = {top(chunk) for chunk in p["chunk_probabilities"]}
    for label in ("Depression", "Anxiety"):
        if label in chunk_tops:
            return label
    return "Normal"


def rule_c(p):
    return top({c: max(chunk[c] for chunk in p["chunk_probabilities"]) for c in CLASSES})


def rule_d(p):
    chunks = p["chunk_probabilities"]
    kept = [chunk for chunk in chunks if top(chunk) != "Normal"] or chunks
    combined = combine_chunks(kept)
    combined["Suicidal"] = max(chunk["Suicidal"] for chunk in chunks)
    return top(combined)


def rule_weighted(p):
    return top(combine_chunks_weighted(p["chunk_probabilities"], p["chunk_lengths"]))


def score(intended, predicted):
    """Accuracy, macro F1 and per-class recall, each with its 95% interval (EV-8)."""
    labels = [c.lower() for c in CLASSES]
    recall = recall_score(intended, predicted, labels=labels, average=None, zero_division=0)
    correct = sum(i == p for i, p in zip(intended, predicted))
    recall_ci = {}
    for label in labels:
        in_class = [p for i, p in zip(intended, predicted) if i == label]
        recall_ci[label] = wilson(sum(p == label for p in in_class), len(in_class))
    return {
        "accuracy": round(accuracy_score(intended, predicted), 3),
        "accuracy_ci": wilson(correct, len(intended)),
        "macro_f1": round(f1_score(intended, predicted, labels=labels, average="macro", zero_division=0), 3),
        "macro_f1_ci": bootstrap_macro_f1(intended, predicted, labels),
        "recall": {label: round(r, 3) for label, r in zip(labels, recall)},
        "recall_ci": recall_ci,
    }


def load_token_run():
    """The main run, with each chunk's length worked out from the entry's token count."""
    run = json.loads((RESULTS / "mentalbert-predictions.json").read_text(encoding="utf-8"))
    tokens = {}
    for line in (EVALUATION_DIR / "dataset" / "dataset.jsonl").read_text(encoding="utf-8").splitlines():
        if line:
            entry = json.loads(line)
            tokens[entry["id"]] = entry["tokens"]
    for p in run["predictions"]:
        n = p["chunk_count"]
        p["chunk_lengths"] = [ROOM] * (n - 1) + [tokens[p["id"]] - ROOM * (n - 1)]
    return run["predictions"]


def weighted_is_written():
    try:
        combine_chunks_weighted([{c: 0.25 for c in CLASSES}], [1])
        return True
    except NotImplementedError:
        return False


def main():
    token_run = load_token_run()
    sentence_file = RESULTS / "mentalbert-predictions-sentences.json"
    sentence_run = json.loads(sentence_file.read_text(encoding="utf-8"))["predictions"] if sentence_file.exists() else None

    assert [rule_a(p).lower() for p in token_run] == [p["predicted"] for p in token_run], \
        "rule A must match the saved run"

    rules = {"A": (rule_a, token_run), "B": (rule_b, token_run), "C": (rule_c, token_run), "D": (rule_d, token_run)}
    if weighted_is_written():
        rules["E"] = (rule_weighted, token_run)
    if sentence_run:
        rules["F"] = (rule_a, sentence_run)
        if weighted_is_written():
            rules["G"] = (rule_weighted, sentence_run)
    waiting = [name for name in "EFG" if name not in rules]

    intended = [p["intended"] for p in token_run]
    baseline = [rule_a(p).lower() for p in token_run]
    report = {}
    def cell(value, ci):
        return f"{value:.2f} ({ci[0]:.2f}-{ci[1]:.2f})"

    print("95% intervals in brackets: Wilson for accuracy and recall, bootstrap for macro F1\n")
    print(f"{'rule':<5}{'accuracy':<19}{'macro F1':<19}{'anxiety':<19}{'depression':<19}{'normal':<19}suicidal")
    for name, (rule, run) in rules.items():
        assert [p["id"] for p in run] == [p["id"] for p in token_run]
        predicted = [rule(p).lower() for p in run]
        result = score(intended, predicted)
        # A working diagnostic, kept in the results file but not in the report table.
        result["changed_vs_a"] = sum(a != b for a, b in zip(baseline, predicted))
        report[name] = result
        r, rc = result["recall"], result["recall_ci"]
        print(f"{name:<5}{cell(result['accuracy'], result['accuracy_ci']):<19}"
              f"{cell(result['macro_f1'], result['macro_f1_ci']):<19}"
              + "".join(f"{cell(r[c], rc[c]):<19}" for c in ("anxiety", "depression", "normal"))
              + cell(r["suicidal"], rc["suicidal"]))
    if waiting:
        print(f"\nNot scored yet: {', '.join(waiting)} (see the note at the top of this file)")

    out = RESULTS / "aggregation-comparison.json"
    out.write_text(json.dumps({"rules": __doc__.split("\n\n")[2], "entries": len(token_run),
                               "results": report}, indent=2), encoding="utf-8")
    print(f"Saved to results/{out.name}")


if __name__ == "__main__":
    main()
