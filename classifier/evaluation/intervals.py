"""95% confidence intervals for the RQ1 metrics (EV-8).

Accuracy, precision and recall are proportions (so many right out of so many), so they get
Wilson score intervals, which stay sensible for small samples and values near 0 or 1.
Macro F1 is not a single proportion, so it gets a percentile bootstrap: the 100 entries are
resampled with replacement many times and the middle 95% of the resulting scores is kept.
"""

import math

import numpy as np
from sklearn.metrics import f1_score

Z = 1.96  # 95%
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_SEED = 20261022


def wilson(successes, total):
    """Return (low, high) for a proportion of successes out of total."""
    if total == 0:
        return (0.0, 1.0)
    p = successes / total
    centre = (p + Z**2 / (2 * total)) / (1 + Z**2 / total)
    half = Z * math.sqrt(p * (1 - p) / total + Z**2 / (4 * total**2)) / (1 + Z**2 / total)
    return (round(centre - half, 3), round(centre + half, 3))


def bootstrap_macro_f1(intended, predicted, labels):
    """Return (low, high) for macro F1 by percentile bootstrap over the entries."""
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    intended, predicted = np.array(intended), np.array(predicted)
    scores = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        pick = rng.integers(0, len(intended), len(intended))
        scores.append(f1_score(intended[pick], predicted[pick], labels=labels, average="macro", zero_division=0))
    low, high = np.percentile(scores, [2.5, 97.5])
    return (round(float(low), 3), round(float(high), 3))
