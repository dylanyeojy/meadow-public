"""Trial (21 October 2026): chunk at sentence boundaries instead of every 126 tokens.

Same model, same classify() and the same combine_chunks; only the chunking differs.
Each chunk is filled with whole sentences up to 126 tokens of text. A single sentence
longer than that is the only thing ever cut mid-sentence.

If the trial is adopted, this chunking moves into classify.py; until then the service
and the main run keep the 126-token chunking.

Run from the classifier folder, with the venv active:
    python evaluation/trial_sentence_chunks.py
"""

import json
import re
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so classify.py can be imported
from classify import WINDOW, Classifier  # noqa: E402

EVALUATION_DIR = Path(__file__).resolve().parent
DATASET = EVALUATION_DIR / "dataset" / "dataset.jsonl"
RESULT = EVALUATION_DIR / "results" / "mentalbert-predictions-sentences.json"

ROOM = WINDOW - 2  # tokens of text per chunk, after [CLS] and [SEP]

# A sentence ends at . ! or ? followed by a space, or at a line break.
SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+|\n+")


class SentenceClassifier(Classifier):
    """The usual Classifier, with chunk() replaced by sentence-boundary chunking."""

    def chunk_token_lists(self, text):
        """Return the chunks as lists of token ids, without [CLS] and [SEP]."""
        sentences = [s for s in SENTENCE_BREAK.split(text) if s.strip()]
        chunks, current = [], []
        for sentence in sentences:
            ids = self.tokenizer(sentence, add_special_tokens=False)["input_ids"]
            while len(ids) > ROOM:  # a sentence longer than a whole chunk
                if current:
                    chunks.append(current)
                    current = []
                chunks.append(ids[:ROOM])
                ids = ids[ROOM:]
            if len(current) + len(ids) > ROOM:  # this sentence would not fit
                chunks.append(current)
                current = []
            current = current + ids
        if current or not chunks:
            chunks.append(current)
        return chunks

    def chunk(self, text):
        """Same output shape as Classifier.chunk, so classify() works unchanged."""
        chunks = self.chunk_token_lists(text)
        cls, sep, pad = self.tokenizer.cls_token_id, self.tokenizer.sep_token_id, self.tokenizer.pad_token_id
        rows = [[cls] + ids + [sep] for ids in chunks]
        longest = max(len(row) for row in rows)
        return {
            "input_ids": torch.tensor([row + [pad] * (longest - len(row)) for row in rows]),
            "attention_mask": torch.tensor([[1] * len(row) + [0] * (longest - len(row)) for row in rows]),
        }


def main():
    entries = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line]
    classifier = SentenceClassifier()
    print(f"Classifying {len(entries)} entries on {classifier.device}, sentence-boundary chunks")

    predictions = []
    for entry in entries:
        result = classifier.classify(entry["text"])
        token_lists = classifier.chunk_token_lists(entry["text"])
        predictions.append({
            "id": entry["id"],
            "intended": entry["label"],
            "predicted": result["top_label"].lower(),
            "probabilities": result["probabilities"],
            "chunk_count": result["chunk_count"],
            "chunk_lengths": [len(ids) for ids in token_lists],
            "chunk_probabilities": result["chunk_probabilities"],
        })

    RESULT.write_text(json.dumps({"chunking": "sentence boundaries, up to 126 tokens of text per chunk",
                                  "entries": len(predictions),
                                  "chunked_entries": sum(p["chunk_count"] > 1 for p in predictions),
                                  "predictions": predictions}, indent=2), encoding="utf-8")
    print(f"Saved to results/{RESULT.name}")


if __name__ == "__main__":
    main()
