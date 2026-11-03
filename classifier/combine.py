"""Combining each chunk's probabilities into one result (REQ_F302, CL-5).

Written by Dylan. The tests are in tests/test_combine.py.
"""


def combine_chunks(chunk_probabilities):
    """Combine every chunk's four probabilities into one set of four.

    chunk_probabilities is a list with one dict per chunk, for example:
        [
            {"Anxiety": 0.10, "Depression": 0.20, "Normal": 0.65, "Suicidal": 0.05},
            {"Anxiety": 0.05, "Depression": 0.30, "Normal": 0.15, "Suicidal": 0.50},
        ]

    Return one dict with the same four keys, where:
    - "Suicidal" is the highest Suicidal value of any chunk,
    - the other three are each the mean (average) across the chunks,
    - and the result is never rescaled to add up to 1 (never renormalised).
    """

    if not chunk_probabilities:
        raise ValueError("No chunk probabilities passed.")

    max_suicidal = total_anxiety = total_depression = total_normal = 0
    length = len(chunk_probabilities)

    for chunk in chunk_probabilities:
        max_suicidal = max(max_suicidal, chunk["Suicidal"])
        total_anxiety += chunk["Anxiety"]
        total_depression += chunk["Depression"]
        total_normal += chunk["Normal"]

    return {
        "Anxiety": total_anxiety / length,
        "Depression": total_depression / length,
        "Normal": total_normal / length,
        "Suicidal": max_suicidal,
    }


def combine_chunks_weighted(chunk_probabilities, chunk_lengths):
    """Like combine_chunks, but a longer chunk counts for more in the averages.

    Used only by the RQ1 aggregation comparison (rules E and G, CL-12). The
    classifier service uses combine_chunks.

    chunk_lengths is a list of whole numbers, one per chunk, giving how many tokens
    of text that chunk holds. For example, a 140-token entry has two chunks with
    lengths [126, 14], so the first chunk should count 126/140 of each average and
    the second only 14/140.

    Return one dict with the same four keys, where:
    - "Suicidal" is still the highest Suicidal value of any chunk (length does not matter),
    - the other three are each the length-weighted mean across the chunks,
    - and the result is never renormalised.
    Raise a ValueError if there are no chunks, or if the two lists differ in length.
    """
    if not chunk_probabilities:
        raise ValueError("No chunk probabilities passed.")

    if not chunk_lengths:
        raise ValueError("No chunk lengths passed.")

    length_chunk_probabilities = len(chunk_probabilities)
    length_chunk_count = len(chunk_lengths)
    total_tokens = sum(chunk_lengths)

    if length_chunk_probabilities != length_chunk_count:
        raise ValueError("Chunk list in different lengths")

    max_suicidal = total_anxiety = total_depression = total_normal = 0

    for index, chunk in enumerate(chunk_probabilities):
        max_suicidal = max(max_suicidal, chunk["Suicidal"])
        total_anxiety += chunk["Anxiety"] * chunk_lengths[index]
        total_depression += chunk["Depression"] * chunk_lengths[index]
        total_normal += chunk["Normal"] * chunk_lengths[index]

    return {
        "Anxiety": total_anxiety / total_tokens,
        "Depression": total_depression / total_tokens,
        "Normal": total_normal / total_tokens,
        "Suicidal": max_suicidal,
    }
