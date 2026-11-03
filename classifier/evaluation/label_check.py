"""Label-order check (CL-10).

The model's config.json names its four outputs LABEL_0 to LABEL_3. The model
card's example code says they mean 0 Anxiety, 1 Depression, 2 Normal,
3 Suicidal. This script runs a few obvious sentences through the model and
prints all four probabilities for each, so the mapping can be checked by eye
before any RQ1 result depends on it.

Write the sentences in evaluation/label-check-sentences.txt, one per line:
    anxiety | I keep worrying that I will fail tomorrow's exam.

Run from the classifier folder, with its .venv active:
    python evaluation/label_check.py
A different sentences file can be given as an argument.
"""

import sys
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

EVALUATION_DIR = Path(__file__).resolve().parent
MODEL_DIR = EVALUATION_DIR.parent / "models" / "mental-health-bert-finetuned"
SENTENCES_FILE = EVALUATION_DIR / "label-check-sentences.txt"

# The mapping being checked, from the model card. Position in the list = output number.
CARD_ORDER = ["anxiety", "depression", "normal", "suicidal"]

# The model was fine-tuned on 128-token inputs (CL-11).
MAX_TOKENS = 128


def read_sentences(path):
    """Return (expected class, sentence) pairs, skipping blank lines and # comments."""
    pairs = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        expected, _, sentence = line.partition("|")
        expected = expected.strip().lower()
        sentence = sentence.strip()
        if expected not in CARD_ORDER or not sentence:
            sys.exit(f"Line {line_number} should look like 'anxiety | a sentence': {line}")
        pairs.append((expected, sentence))
    return pairs


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else SENTENCES_FILE
    if not MODEL_DIR.exists():
        sys.exit(f"No model at {MODEL_DIR}. classifier/README.md says how to download it.")
    pairs = read_sentences(path)
    if not pairs:
        sys.exit(f"No sentences yet. Add some to {path.name}, one per line as 'class | sentence'.")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on {device}\n")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR).to(device)
    model.eval()

    matches = 0
    for expected, sentence in pairs:
        inputs = tokenizer(sentence, truncation=True, max_length=MAX_TOKENS, return_tensors="pt").to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=-1)[0].tolist()
        top = probabilities.index(max(probabilities))

        print(f"[you wrote it as {expected}] {sentence}")
        for index, probability in enumerate(probabilities):
            marker = "   <- top" if index == top else ""
            print(f"    output {index} (card says {CARD_ORDER[index]:<10}) {probability:.3f}{marker}")
        if CARD_ORDER[top] == expected:
            matches += 1
        print()

    print(f"{matches} of {len(pairs)} sentences: the top output is the one the card's mapping predicts.")


if __name__ == "__main__":
    main()
