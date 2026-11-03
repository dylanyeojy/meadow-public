# Classifier service

Runs the fine-tuned MentalBERT model, [`ourafla/mental-health-bert-finetuned`](https://huggingface.co/ourafla/mental-health-bert-finetuned), and returns the full probability distribution over its four classes: Normal, Anxiety, Depression, Suicidal. It is a separate program the backend calls over HTTP, never a module the backend imports, so it can move to a hosted platform by changing only its URL (proposal Section 3.3.3).

This folder also holds the RQ1 evaluation in [evaluation/](evaluation/README.md), which shares the service's code and environment so that the evaluation measures exactly what the app does.

## The rules it follows

From the proposal, Section 3.3.3 and requirement `REQ_F302`:

- `POST /classify` receives the journal text and nothing else: no mood values, no user id.
- It returns all four probabilities, the top label, and the per-chunk probabilities, never just a label.
- Entries longer than the model's 128-token window are split into chunks. **P(Suicidal) is the maximum across chunks; the other three are the mean** (`REQ_F302`). The result is not renormalised, since that would scale the Suicidal maximum back down.
- `GET /health` reports whether the model is loaded.

## Setup

Windows, from this folder, with Python 3.13 and an NVIDIA GPU:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -c "import torch; print(torch.cuda.is_available())"   # True means the GPU is in use
```

`requirements.txt` pulls PyTorch's CUDA build from PyTorch's own package index. Without an NVIDIA GPU, delete the `--extra-index-url` line and PyTorch falls back to running on the CPU, which is slower but fine for 100 entries.

## Two things the model does not tell you

**Its labels are unnamed.** The model's `config.json` calls the four outputs `LABEL_0` to `LABEL_3`. The mapping appears only in the example code of the [model card](https://huggingface.co/ourafla/mental-health-bert-finetuned), and it is alphabetical, not the order CP1 lists the classes in:

| Output | Class |
| --- | --- |
| 0 | Anxiety |
| 1 | Depression |
| 2 | Normal |
| 3 | Suicidal |

Every probability the router reads depends on it, so it was checked on 20 October 2026 with [evaluation/label_check.py](evaluation/label_check.py): 7 of 8 obvious sentences landed in the slot this table names, with no swap pattern (CL-10).

**Its tokenizer allows 512 tokens, but the model was fine-tuned at 128.** Nothing stops a longer input, so the 128-token limit and the chunking have to be applied by this service's own code.

## The model weights

A local copy lives in `models/`, which is not in git (837MB, since the model ships its weights in two formats). The proposal asks for one (Section 3.8.3), so the project does not depend on the model staying online. To download it again:

```powershell
python -c "from huggingface_hub import snapshot_download; snapshot_download('ourafla/mental-health-bert-finetuned', local_dir='models/mental-health-bert-finetuned')"
```

Keep a second copy outside this repo as well, such as in cloud storage.

## Secrets

Copy `.env.example` to `.env` and fill it in. `.env` is never committed.
