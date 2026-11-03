"""The second-rater check on the RQ1 dataset labels (proposal Section 3.7.2, figure 3.32).

An independent person labels a 20% sample, 5 entries per class, without seeing the original
labels. Cohen's Kappa then measures how far the two sets of labels agree beyond chance.

Each rater gets their own sample, sheet and result, so no rating is ever overwritten:
  rater 1: second-rater/rating-sheet.xlsx, sample.json, results/second-rater-agreement.json
  rater 2: second-rater/rating-sheet-2.xlsx, sample-2.json, results/second-rater-2-agreement.json
Rater 2's sample leaves out every entry rater 1 saw, so the two ratings cover different entries.

Commands, run from the classifier folder with the venv active:
  python evaluation/second_rater.py calibration           write the calibration pack (pilot entries)
  python evaluation/second_rater.py sheet --rater 2       write rater 2's blind rating sheet
  python evaluation/second_rater.py kappa --rater 2 --threshold 0.6
                                                          measure agreement against the bar set beforehand

Give a rater only their own rating sheet (and the calibration pack). Never a sample file,
dataset/, results/ or generation/: those hold the original labels.
"""

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation
from sklearn.metrics import cohen_kappa_score, confusion_matrix

SEEDS = {1: 20261019, 2: 20261021}
PER_CLASS = 5
CLASSES = ["normal", "anxiety", "depression", "suicidal"]

# What a rater is told about each class. Plain descriptions of the labels, written for a
# reader rather than a model, and deliberately not the generation prompts.
DESCRIPTIONS = {
    "normal": "Everyday ups and downs. The writer may be tired, annoyed or have a bad moment, "
              "but is coping, and any worry is proportionate and passes.",
    "anxiety": "Worry or dread dominates, usually about what might go wrong. Racing thoughts, "
               "restlessness, trouble switching off, or physical signs such as a racing heart.",
    "depression": "A low mood that has lasted: flatness, emptiness, tiredness, withdrawing from "
                  "people and being hard on oneself. No thoughts of death.",
    "suicidal": "Thoughts that life is not worth living, of wishing not to be here, or of ending "
                "one's life, said directly or indirectly.",
}

# The distinctions raters most often get wrong, for the calibration session.
DISTINCTIONS = [
    "Depression or anxiety? Ask which feeling leads. Anxiety looks forward: what might go wrong, "
    "dread, a mind that will not switch off. Depression is heavy and flat: things have stopped "
    "mattering, energy is gone, the writer is hard on themselves.",
    "Depression or a normal bad day? Ask how long and how deep. A normal entry can be sad or fed up, "
    "but the writer is still coping and the feeling passes. Depression has lasted, and even good "
    "news barely registers.",
    "Suicidal or depression? Ask whether the writer questions being alive at all: wishing not to "
    "wake up, wanting to disappear, feeling others would be better off without them. Depression "
    "without those thoughts stays depression.",
    "Read the whole entry before deciding. A good event (a prize, a new friend) does not make an "
    "entry normal if the writer feels nothing about it.",
]

CONTENT_NOTE = ("Content note: some entries describe thoughts of not wanting to live. If reading them affects "
                "you, stop at any time. Support is free, confidential and open 24 hours: MIASA Crisis Helpline "
                "1800-180-066, Befrienders KL 03-7627 2929. In an emergency, call 999.")

HERE = Path(__file__).resolve().parent
CLASSIFIER = HERE.parent
DATASET = HERE / "dataset" / "dataset.jsonl"
PILOT = HERE / "generation" / "work" / "pilot" / "entries.jsonl"
FOLDER = HERE / "second-rater"
RESULTS = HERE / "results"


def files(rater):
    suffix = "" if rater == 1 else f"-{rater}"
    return {
        "sheet": FOLDER / f"rating-sheet{suffix}.xlsx",
        "sample": FOLDER / f"sample{suffix}.json",
        "result": RESULTS / ("second-rater-agreement.json" if rater == 1 else f"second-rater-{rater}-agreement.json"),
    }


def show(path):
    return path.relative_to(CLASSIFIER)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_jsonl(path):
    if not path.exists():
        sys.exit(f"{show(path)} is missing.")
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def label_of(entry):
    return entry.get("label") or entry["class"]


def guide_tab(wb, lines):
    guide = wb.active
    guide.title = "read me first"
    for row, text in enumerate(lines, start=1):
        guide.cell(row=row, column=1, value=text).alignment = Alignment(wrap_text=True, vertical="top")
    guide["A1"].font = Font(bold=True)
    guide.column_dimensions["A"].width = 110


def calibration():
    path = FOLDER / "calibration-pack.xlsx"
    entries = load_jsonl(PILOT)
    order = random.Random(SEEDS[2] + 100).sample(entries, len(entries))
    wb = Workbook()
    guide_tab(wb, [
        "Calibration: practice before rating",
        "",
        "These 8 practice entries are not part of the study. They are here so that you and the "
        "researcher read the four labels the same way before you rate the real entries.",
        "1. Read the four labels below.",
        "2. On the 'practice' sheet, label each entry yourself.",
        "3. Only then open the 'answers' sheet, compare, and talk through any differences with the "
        "researcher.",
        "4. Then rate the real entries on your own rating sheet, alone, without discussing them.",
        "",
        "The four labels:",
        *[f"{c}: {d}" for c, d in DESCRIPTIONS.items()],
        "",
        "Where raters most often disagree:",
        *DISTINCTIONS,
        "",
        CONTENT_NOTE,
    ])
    practice = wb.create_sheet("practice")
    answers = wb.create_sheet("answers")
    for ws, headings in ((practice, ["item", "entry", "your label"]), (answers, ["item", "intended label"])):
        for col, heading in enumerate(headings, start=1):
            ws.cell(row=1, column=col, value=heading).font = Font(bold=True)
    practice.column_dimensions["B"].width = 100
    practice.column_dimensions["C"].width = 14
    answers.column_dimensions["B"].width = 16
    for row, e in enumerate(order, start=2):
        item = f"P{row - 1}"
        practice.cell(row=row, column=1, value=item).alignment = Alignment(vertical="top")
        practice.cell(row=row, column=2, value=e["text"]).alignment = Alignment(wrap_text=True, vertical="top")
        answers.cell(row=row, column=1, value=item)
        answers.cell(row=row, column=2, value=label_of(e))
    dropdown = DataValidation(type="list", formula1='"' + ",".join(CLASSES) + '"', allow_blank=True)
    practice.add_data_validation(dropdown)
    dropdown.add(f"C2:C{len(order) + 1}")
    practice.freeze_panes = "A2"
    FOLDER.mkdir(exist_ok=True)
    wb.save(path)
    print(f"Wrote {show(path)}: {len(order)} practice entries, labels on a separate 'answers' sheet.")


def sheet(rater):
    f = files(rater)
    if f["sheet"].exists():
        sys.exit(f"{show(f['sheet'])} already exists. Delete it and {show(f['sample'])} only if you mean "
                 "to draw a new sample; never do so after the rater has started.")
    entries = load_jsonl(DATASET)
    seen = set()
    for other in range(1, rater):
        if files(other)["sample"].exists():
            seen |= {k["id"] for k in json.loads(files(other)["sample"].read_text(encoding="utf-8"))["items"]}
    rng = random.Random(SEEDS[rater])
    sample = []
    for cls in CLASSES:
        pool = [e for e in entries if label_of(e) == cls and e["id"] not in seen]
        sample += rng.sample(pool, PER_CLASS)
    rng.shuffle(sample)

    key = [{"item": f"R{i:02d}", "id": e["id"], "label": label_of(e)} for i, e in enumerate(sample, start=1)]
    FOLDER.mkdir(exist_ok=True)
    f["sample"].write_text(json.dumps({"rater": rater, "seed": SEEDS[rater], "excludes_earlier_samples": sorted(seen),
                                       "made": now(), "items": key}, indent=2), encoding="utf-8")

    wb = Workbook()
    guide_tab(wb, [
        "Thank you for helping with this research.",
        "",
        "Each entry on the 'entries' sheet is a short, fictional journal entry written for a study of a "
        "mental health text classifier. None of them is about a real person.",
        "For each one, choose the single label that fits best from the dropdown. If you are unsure, pick "
        "your best judgement and say why in the comment column.",
        "Please work on your own, and do not discuss the entries with anyone until you have finished.",
        "",
        "The four labels:",
        *[f"{c}: {d}" for c, d in DESCRIPTIONS.items()],
        "",
        CONTENT_NOTE,
    ])
    ws = wb.create_sheet("entries")
    for col, (heading, width) in enumerate([("item", 8), ("entry", 100), ("label", 14), ("comment", 40)], start=1):
        ws.cell(row=1, column=col, value=heading).font = Font(bold=True)
        ws.column_dimensions["ABCD"[col - 1]].width = width
    for row, (k, e) in enumerate(zip(key, sample), start=2):
        ws.cell(row=row, column=1, value=k["item"]).alignment = Alignment(vertical="top")
        ws.cell(row=row, column=2, value=e["text"]).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=4).alignment = Alignment(wrap_text=True, vertical="top")
    dropdown = DataValidation(type="list", formula1='"' + ",".join(CLASSES) + '"', allow_blank=True)
    ws.add_data_validation(dropdown)
    dropdown.add(f"C2:C{len(key) + 1}")
    ws.freeze_panes = "A2"
    wb.save(f["sheet"])

    print(f"Wrote {show(f['sheet'])}: {len(key)} entries, {PER_CLASS} per class, shuffled, with no labels shown"
          + (f", none of the {len(seen)} entries earlier raters saw." if seen else "."))
    print(f"The key is in {show(f['sample'])}. Send the rater the sheet only.")


def kappa(rater, threshold, overwrite):
    f = files(rater)
    if not f["sample"].exists() or not f["sheet"].exists():
        sys.exit("No rating sheet for this rater yet. Run the sheet command first.")
    if f["result"].exists() and not overwrite:
        sys.exit(f"{show(f['result'])} already holds this rater's result. It is never replaced silently; "
                 "pass --overwrite only if the same rater's sheet has genuinely been corrected.")
    key = {k["item"]: k for k in json.loads(f["sample"].read_text(encoding="utf-8"))["items"]}
    try:
        ws = load_workbook(f["sheet"])["entries"]
    except PermissionError:
        sys.exit(f"{show(f['sheet'])} is open in Excel. Save and close it, then run kappa again.")

    yours, theirs, rows, missing = [], [], [], []
    for item, _, label, comment in ws.iter_rows(min_row=2, max_col=4, values_only=True):
        if item is None:
            continue
        label = (label or "").strip().lower()
        if label not in CLASSES:
            missing.append(item)
            continue
        yours.append(key[item]["label"])
        theirs.append(label)
        rows.append({"item": item, "id": key[item]["id"], "yours": key[item]["label"],
                     "theirs": label, "comment": comment or ""})
    if missing:
        sys.exit(f"These items have no valid label yet: {', '.join(missing)}. Ask the rater to finish them.")

    k = cohen_kappa_score(yours, theirs, labels=CLASSES)
    agreed = sum(a == b for a, b in zip(yours, theirs))
    matrix = confusion_matrix(yours, theirs, labels=CLASSES).tolist()
    disagreements = [r for r in rows if r["yours"] != r["theirs"]]

    print(f"Rater {rater}. Cohen's Kappa: {k:.3f}")
    print(f"Raw agreement: {agreed} of {len(rows)} ({agreed / len(rows):.0%})")
    print("\nConfusion matrix (rows: original labels, columns: the rater's):")
    print(" " * 12 + "".join(f"{c:>12}" for c in CLASSES))
    for cls, counts in zip(CLASSES, matrix):
        print(f"{cls:<12}" + "".join(f"{n:>12}" for n in counts))
    if disagreements:
        print("\nDisagreements, to look at again:")
        for r in disagreements:
            print(f"  {r['item']} ({r['id']}): original {r['yours']}, rater {r['theirs']}"
                  + (f". Rater's comment: {r['comment']}" if r["comment"] else ""))
    if threshold is not None:
        print(f"\nKappa {'reaches' if k >= threshold else 'does not reach'} the agreed bar of {threshold}.")

    RESULTS.mkdir(exist_ok=True)
    f["result"].write_text(json.dumps({
        "rater": rater,
        "kappa": round(k, 4),
        "agreement": agreed,
        "rated": len(rows),
        "threshold": threshold,
        "labels": CLASSES,
        "confusion_matrix_rows_original_cols_rater": matrix,
        "disagreements": disagreements,
        "seed": SEEDS[rater],
        "computed": now(),
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved to {show(f['result'])}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["calibration", "sheet", "kappa"])
    parser.add_argument("--rater", type=int, choices=sorted(SEEDS), default=1)
    parser.add_argument("--threshold", type=float, help="the agreement bar, decided before looking")
    parser.add_argument("--overwrite", action="store_true", help="replace this rater's saved result")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.command == "calibration":
        calibration()
    elif args.command == "sheet":
        sheet(args.rater)
    else:
        kappa(args.rater, args.threshold, args.overwrite)


if __name__ == "__main__":
    main()
