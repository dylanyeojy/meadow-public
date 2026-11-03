"""Classify a journal entry with MentalBERT, chunking long entries (REQ_F302).

The RQ1 evaluation and the classifier service both use this file, so the
evaluation measures exactly what the app does (EV-5).
"""

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from combine import combine_chunks

MODEL_DIR = Path(__file__).resolve().parent / "models" / "mental-health-bert-finetuned"

# The model's output order, from its model card, checked on 20 October 2026 (CL-10).
LABELS = ("Anxiety", "Depression", "Normal", "Suicidal")

# The model was fine-tuned on 128-token inputs (CL-11). Two of the 128 are the
# special tokens [CLS] and [SEP], so each chunk holds up to 126 tokens of text.
WINDOW = 128


class Classifier:
    """Loads the model once, then classifies as many entries as needed."""

    def __init__(self, model_dir=MODEL_DIR):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir).to(self.device)
        self.model.eval()

    def chunk(self, text):
        """Split the text into 128-token chunks, each with its own [CLS] and [SEP]."""
        return self.tokenizer(
            text,
            truncation=True,
            max_length=WINDOW,
            return_overflowing_tokens=True,
            padding=True,
            return_tensors="pt",
        )

    def classify(self, text):
        """Return the combined probabilities, the top label and every chunk's probabilities."""
        chunks = self.chunk(text)
        with torch.no_grad():
            logits = self.model(
                input_ids=chunks["input_ids"].to(self.device),
                attention_mask=chunks["attention_mask"].to(self.device),
            ).logits
        rows = torch.softmax(logits, dim=-1).tolist()
        chunk_probabilities = [dict(zip(LABELS, row)) for row in rows]

        probabilities = combine_chunks(chunk_probabilities)
        top_label = max(probabilities, key=probabilities.get)
        return {
            "probabilities": probabilities,
            "top_label": top_label,
            "chunked": len(chunk_probabilities) > 1,
            "chunk_count": len(chunk_probabilities),
            "chunk_probabilities": chunk_probabilities,
        }
