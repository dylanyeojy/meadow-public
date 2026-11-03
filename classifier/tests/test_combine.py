"""Tests for combine_chunks and combine_chunks_weighted (REQ_F302, CL-5)."""

from pytest import approx, raises

from combine import combine_chunks, combine_chunks_weighted

# Three chunks of one long entry: the first reads as anxiety, the second as
# depression, and only the third as suicidal.
THREE_CHUNKS = [
    {"Anxiety": 0.70, "Depression": 0.20, "Normal": 0.08, "Suicidal": 0.02},
    {"Anxiety": 0.10, "Depression": 0.80, "Normal": 0.07, "Suicidal": 0.03},
    {"Anxiety": 0.02, "Depression": 0.05, "Normal": 0.03, "Suicidal": 0.90},
]


def test_req_f302_returns_all_four_classes():
    result = combine_chunks(THREE_CHUNKS)
    assert set(result) == {"Anxiety", "Depression", "Normal", "Suicidal"}


def test_req_f302_one_chunk_comes_back_unchanged():
    one_chunk = [
        {"Anxiety": 0.10, "Depression": 0.20, "Normal": 0.65, "Suicidal": 0.05}
    ]
    assert combine_chunks(one_chunk) == approx(one_chunk[0])


def test_req_f302_suicidal_is_the_highest_chunk_not_the_mean():
    # The mean would be 0.32, which only reaches Heightened-caution.
    # The highest chunk, 0.90, is what the router must see.
    assert combine_chunks(THREE_CHUNKS)["Suicidal"] == approx(0.90)


def test_req_f302_other_classes_are_the_mean_across_chunks():
    result = combine_chunks(THREE_CHUNKS)
    assert result["Anxiety"] == approx((0.70 + 0.10 + 0.02) / 3)
    assert result["Depression"] == approx((0.20 + 0.80 + 0.05) / 3)
    assert result["Normal"] == approx((0.08 + 0.07 + 0.03) / 3)


def test_req_f302_result_is_never_renormalised():
    # Taking the highest Suicidal pushes the total past 1. Rescaling it back
    # to 1 would shrink P(Suicidal), so the total must stay as it is.
    total = sum(combine_chunks(THREE_CHUNKS).values())
    assert total == approx(0.82 / 3 + 1.05 / 3 + 0.18 / 3 + 0.90)
    assert total > 1


def test_req_f302_does_not_change_the_chunks_it_was_given():
    chunks = [dict(chunk) for chunk in THREE_CHUNKS]
    combine_chunks(chunks)
    assert chunks == THREE_CHUNKS


def test_req_f302_empty_list_is_an_error():
    with raises(ValueError):
        combine_chunks([])


# combine_chunks_weighted, on trial (21 October 2026)

TWO_CHUNKS = [
    {"Anxiety": 0.90, "Depression": 0.05, "Normal": 0.03, "Suicidal": 0.02},
    {"Anxiety": 0.10, "Depression": 0.05, "Normal": 0.25, "Suicidal": 0.60},
]


def test_req_f302_weighted_equal_lengths_match_the_plain_mean():
    result = combine_chunks_weighted(THREE_CHUNKS, [126, 126, 126])
    assert result == approx(combine_chunks(THREE_CHUNKS))


def test_req_f302_weighted_longer_chunk_counts_for_more():
    # 126 tokens and 14 tokens: the first chunk carries 126/140 of the average.
    result = combine_chunks_weighted(TWO_CHUNKS, [126, 14])
    assert result["Anxiety"] == approx((0.90 * 126 + 0.10 * 14) / 140)
    assert result["Normal"] == approx((0.03 * 126 + 0.25 * 14) / 140)


def test_req_f302_weighted_suicidal_is_still_the_highest_chunk():
    # The short chunk holds the suicidal passage; its length must not water it down.
    assert combine_chunks_weighted(TWO_CHUNKS, [126, 14])["Suicidal"] == approx(0.60)


def test_req_f302_weighted_empty_list_is_an_error():
    with raises(ValueError):
        combine_chunks_weighted([], [])


def test_req_f302_weighted_lengths_must_match_the_chunks():
    with raises(ValueError):
        combine_chunks_weighted(TWO_CHUNKS, [126])
