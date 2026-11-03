# RQ1 evaluation

How well does the fine-tuned MentalBERT classify private, student-style journal entries? The protocol is Section 3.7 of the project proposal. This folder holds the dataset, how it was made and checked, and the results that go into the report.

| Folder | Holds |
| --- | --- |
| [dataset/](dataset/README.md) | **The frozen dataset**: `dataset.jsonl`, 100 entries, 25 per class, and its dataset card. Never edited |
| `generation/` | How the entries were made: the matrix (`matrix.json`), the prompts (`prompts/`), `generate.py`, and `work/`, the record of the run: the plan, every generation in `state.json`, the blind review sheets and the pilot |
| `second-rater/` | The rating sheets, their answer keys (`sample*.json`) and the calibration pack |
| `results/` | Agreement results now; the classifier and baseline metrics for Chapter 4 next |

## Making the dataset (done, frozen 20 October 2026)

From `classifier/`, with the venv active. Add `--pilot` to run the 8-entry pilot, kept in `generation/work/pilot/`.

1. `python evaluation/generation/generate.py submit` sends one batch request per entry that still needs one.
2. `python evaluation/generation/generate.py collect`, once the batch has finished (usually within an hour), writes a **blind** review sheet, `generation/work/blind-review-N.xlsx`: entry text only, shuffled, under anonymous item numbers.
3. In the sheet, choose the **label** for each entry, an **issue** if it reads as implausible or its class could be guessed from one word, and a **note** for any issue or doubt. Save and close it.
4. `python evaluation/generation/generate.py apply` reads the labels. An entry passes when the label matches its intended class and the issue is "none". Then `submit` again regenerates the rejects, until every class has 25.
5. `python evaluation/generation/generate.py freeze` writes `dataset/dataset.jsonl`, and never overwrites it with anything different.

`status` shows where every entry stands and the cost so far.

## The second raters

An independent person labels 20 entries, 5 per class, without seeing the original labels, and Cohen's Kappa measures the agreement against a bar set beforehand, κ ≥ 0.60. Each rater has their own sample, sheet and result file, and a saved result is never overwritten.

**Rater 1** is done: κ = 0.67, 15 of 20 (`results/second-rater-agreement.json`).

**Rater 2** is done: κ = 0.87, 18 of 20 (`results/second-rater-2-agreement.json`). Calibration and rating took about 3 minutes together; the rater scanned for cue phrases rather than reading every entry in full (CP-35). The steps they followed:

1. Run the calibration with `second-rater/calibration-pack.xlsx`: 8 pilot entries, which are not part of the dataset. The rater labels them on the "practice" sheet first, then compares with the "answers" sheet and talks through the differences with the researcher.
2. Then send `second-rater/rating-sheet-2.xlsx`, **that file only**. It holds 20 entries none of which rater 1 saw. The rater works alone, without discussing them.
3. When it comes back, put it in the same place and run `python evaluation/second_rater.py kappa --rater 2 --threshold 0.6`. The result goes to `results/second-rater-2-agreement.json`.

## Rules from the protocol

- Entries pass through **the same classification code as the live service**, chunking included, so the evaluation measures what the app does.
- The routing thresholds (0.35, 0.15, 4.0) are **held fixed** during the evaluation.
- **Suicidal recall is the priority metric.** Report it first.
- The published 89.72% accuracy is the model author's claim, never this project's finding.
