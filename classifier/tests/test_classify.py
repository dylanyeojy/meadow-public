"""Tests for the chunking in classify.py (REQ_F302, CL-11).

They need the local model in models/ and are skipped without it.
"""

import pytest

from classify import MODEL_DIR, WINDOW, Classifier

pytestmark = pytest.mark.skipif(not MODEL_DIR.exists(), reason="model not downloaded")

SENTENCE = "I stayed up late again finishing the group report and barely slept. "


@pytest.fixture(scope="module")
def classifier():
    return Classifier()


def text_tokens(classifier, text):
    return classifier.tokenizer(text, add_special_tokens=False)["input_ids"]


def test_req_f302_short_entry_is_one_chunk(classifier):
    chunks = classifier.chunk("Today was a pretty normal day.")
    assert chunks["input_ids"].shape[0] == 1


def test_req_f302_long_entry_is_split_into_128_token_chunks(classifier):
    text = SENTENCE * 20
    tokens = len(text_tokens(classifier, text))
    expected_chunks = -(-tokens // (WINDOW - 2))  # rounds up
    chunks = classifier.chunk(text)
    assert tokens > WINDOW
    assert chunks["input_ids"].shape == (expected_chunks, WINDOW)


def test_req_f302_every_chunk_has_its_own_special_tokens(classifier):
    tokenizer = classifier.tokenizer
    chunks = classifier.chunk(SENTENCE * 20)
    for row, mask in zip(chunks["input_ids"], chunks["attention_mask"]):
        real = row[mask.bool()].tolist()  # the chunk without its padding
        assert real[0] == tokenizer.cls_token_id
        assert real[-1] == tokenizer.sep_token_id


def test_req_f302_no_text_is_lost_or_repeated_between_chunks(classifier):
    text = SENTENCE * 20
    tokenizer = classifier.tokenizer
    chunks = classifier.chunk(text)
    joined = []
    for row, mask in zip(chunks["input_ids"], chunks["attention_mask"]):
        joined += row[mask.bool()].tolist()[1:-1]  # drop [CLS] and [SEP]
    assert joined == text_tokens(classifier, text)
    assert tokenizer.cls_token_id not in joined
