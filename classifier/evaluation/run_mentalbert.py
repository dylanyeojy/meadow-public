"""Run MentalBERT over the frozen RQ1 dataset (proposal Section 3.7).

Every entry goes through classify.py, the same code the classifier service uses,
chunking included (EV-5). The predictions are saved for the metrics script; this
script computes no metrics itself.

Run from the classifier folder, with the venv active:
    python evaluation/run_mentalbert.py
A saved run is never replaced unless --overwrite is given.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
import transformers

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so classify.py can be imported
from classify import MODEL_DIR, WINDOW, Classifier  # noqa: E402

EVALUATION_DIR = Path(__file__).resolve().parent
DATASET = EVALUATION_DIR / "dataset" / "dataset.jsonl"
RESULT = EVALUATION_DIR / "results" / "mentalbert-predictions.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--overwrite", action="store_true", help="replace the saved run")
    args = parser.parse_args()
    if RESULT.exists() and not args.overwrite:
        sys.exit(f"{RESULT.name} already exists. Pass --overwrite only to deliberately rerun.")

    entries = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line]
    classifier = Classifier()
    print(f"Classifying {len(entries)} entries on {classifier.device}")

    predictions = []
    for entry in entries:
        result = classifier.classify(entry["text"])
        predictions.append({
            "id": entry["id"],
            "intended": entry["label"],
            "predicted": result["top_label"].lower(),
            "probabilities": result["probabilities"],
            "chunk_count": result["chunk_count"],
            "chunk_probabilities": result["chunk_probabilities"],
        })

    run = {
        "model": MODEL_DIR.name,
        "window": WINDOW,
        "device": classifier.device,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "dataset": DATASET.name,
        "entries": len(predictions),
        "chunked_entries": sum(p["chunk_count"] > 1 for p in predictions),
        "ran": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "predictions": predictions,
    }
    RESULT.write_text(json.dumps(run, indent=2), encoding="utf-8")
    print(f"Saved {len(predictions)} predictions ({run['chunked_entries']} chunked) to results/{RESULT.name}")


if __name__ == "__main__":
    main()
