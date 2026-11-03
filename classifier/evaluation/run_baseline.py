"""Run the zero-shot GPT-5.4 baseline over the frozen RQ1 dataset (EV-4, EV-9).

Two prompts, both fixed before any result was seen:
  defined  baseline/system-prompt.txt       the primary baseline (label definitions)
  bare     baseline/system-prompt-bare.txt  the secondary check (label names only)

Each entry is sent whole, with no examples, and the reply is restricted to one of the
four labels. The probability of each label is read from the logprobs at the token where
the label starts; the four labels start with different letters, so every alternative
token belongs to exactly one label. The predictions are saved for the metrics script.

Run from the classifier folder, with the venv active:
    python evaluation/run_baseline.py defined
    python evaluation/run_baseline.py bare
A saved run is never replaced unless --overwrite is given.
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from dotenv import load_dotenv
from openai import OpenAI

CLASSIFIER_DIR = Path(__file__).resolve().parent.parent
EVALUATION_DIR = CLASSIFIER_DIR / "evaluation"
DATASET = EVALUATION_DIR / "dataset" / "dataset.jsonl"
PROMPTS = {
    "defined": EVALUATION_DIR / "baseline" / "system-prompt.txt",
    "bare": EVALUATION_DIR / "baseline" / "system-prompt-bare.txt",
}
LABELS = ["anxiety", "depression", "normal", "suicidal"]

MODEL = "gpt-5.4"
SETTINGS = {"reasoning_effort": "none", "temperature": 0, "logprobs": True, "top_logprobs": 5}
RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "journal_label",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"label": {"type": "string", "enum": LABELS}},
            "required": ["label"],
            "additionalProperties": False,
        },
    },
}


def label_for(token):
    """The label an alternative token starts, or None (each label starts with its own letter)."""
    piece = token.strip().lower()
    matches = [label for label in LABELS if piece and label.startswith(piece)]
    return matches[0] if len(matches) == 1 else None


def label_probabilities(logprobs):
    """Probability of each label, from the alternatives at the token where the label starts."""
    text = ""
    for token in logprobs:
        if text.replace(" ", "").endswith('"label":"'):
            probabilities = dict.fromkeys(LABELS, 0.0)
            for alternative in token.top_logprobs:
                label = label_for(alternative.token)
                if label:
                    probabilities[label] += math.exp(alternative.logprob)
            return probabilities
        text += token.token
    return None


def classify(client, system_prompt, text):
    """One API call for one entry. Errors and refusals are recorded, never retried with another prompt."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text}],
            response_format=RESPONSE_FORMAT,
            **SETTINGS,
        )
    except openai.APIError as error:
        return {"predicted": None, "error": f"{type(error).__name__}: {error}"}, None

    choice = response.choices[0]
    if choice.message.refusal or not choice.message.content:
        return {"predicted": None, "error": f"refusal: {choice.message.refusal}"}, response.model
    return {
        "predicted": json.loads(choice.message.content)["label"],
        "probabilities": label_probabilities(choice.logprobs.content),
    }, response.model


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("prompt", choices=PROMPTS)
    parser.add_argument("--overwrite", action="store_true", help="replace the saved run")
    args = parser.parse_args()

    result_file = EVALUATION_DIR / "results" / f"baseline-predictions-{args.prompt}.json"
    if result_file.exists() and not args.overwrite:
        sys.exit(f"{result_file.name} already exists. Pass --overwrite only to deliberately rerun.")

    # override=True: the key in classifier/.env wins over any OPENAI_API_KEY set in Windows.
    load_dotenv(CLASSIFIER_DIR / ".env", override=True)
    client = OpenAI()
    system_prompt = PROMPTS[args.prompt].read_text(encoding="utf-8")
    entries = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line]
    print(f"Classifying {len(entries)} entries with {MODEL}, {args.prompt} prompt")

    predictions, snapshots = [], set()
    for number, entry in enumerate(entries, start=1):
        outcome, snapshot = classify(client, system_prompt, entry["text"])
        snapshots.add(snapshot)
        predictions.append({"id": entry["id"], "intended": entry["label"], **outcome})
        if number % 10 == 0:
            print(f"  {number} done")

    run = {
        "model": MODEL,
        "snapshots": sorted(s for s in snapshots if s),
        "settings": SETTINGS,
        "prompt": args.prompt,
        "prompt_file": PROMPTS[args.prompt].name,
        "system_prompt": system_prompt,
        "entries": len(predictions),
        "no_answer": sum(p["predicted"] is None for p in predictions),
        "ran": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "predictions": predictions,
    }
    result_file.write_text(json.dumps(run, indent=2), encoding="utf-8")
    print(f"Saved to results/{result_file.name} ({run['no_answer']} without an answer)")


if __name__ == "__main__":
    main()
