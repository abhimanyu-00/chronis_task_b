# Test suite
# PDF requirement: "pytest suite covering type boundary
# logic and abstention behavior"

import pytest
from engine.evidence import check_evidence
from engine.scorer import score_sentence, get_behavioral_score
from engine.typer import classify
from engine.output import make_result, make_abstention


# ── Evidence tests ──────────────────────────────────────

def test_abstention_when_less_than_3_days():
    days = {"day_1": "went to gym"}
    snippets = ["I have been active"]
    result = check_evidence("fitness", days, snippets)
    assert result["status"] == "insufficient_evidence"


def test_pass_when_3_or_more_days():
    days = {
        "day_1": "went to gym",
        "day_2": "went for walk",
        "day_3": "completed workout"
    }
    snippets = ["I have been active"]
    result = check_evidence("fitness", days, snippets)
    assert result["status"] == "ok"


def test_abstention_when_no_snippets():
    days = {
        "day_1": "went to gym",
        "day_2": "went for walk",
        "day_3": "completed workout"
    }
    result = check_evidence("fitness", days, [])
    assert result["status"] == "insufficient_evidence"


# ── Scorer tests ─────────────────────────────────────────

def test_negative_sentence_scores_zero():
    score = score_sentence("skipped planned workout session")
    assert score == 0


def test_positive_sentence_scores_one():
    score = score_sentence("went to gym and completed workout")
    assert score == 1


def test_neutral_sentence_scores_half():
    score = score_sentence("today was an ordinary day")
    assert score == 0.5


# ── Typer tests ───────────────────────────────────────────

def test_overstatement_detected():
    div_type, gap = classify(0.0, 1.0, ["I have been very active"])
    assert div_type == "overstatement"


def test_understatement_detected():
    # narrative 0.3 = low but above blind_spot threshold 0.20
    # behavior 1.0 = very high
    # gap = 0.3 - 1.0 = -0.7 → understatement
    div_type, gap = classify(1.0, 0.3, ["work has been slow"])
    assert div_type == "understatement"


def test_aspiration_gap_detected():
    div_type, gap = classify(
        0.1, 0.5,
        ["I really want to start eating healthy soon"]
    )
    assert div_type == "aspiration_gap"


def test_blind_spot_detected():
    # high behavior, very low narrative = blind spot
    div_type, gap = classify(1.0, 0.0, ["focusing on other things"])
    assert div_type == "blind_spot"


# ── Output safety tests ───────────────────────────────────

def test_no_characterological_fields_in_output():
    result = make_result(
        domain="fitness",
        divergence_type="overstatement",
        gap=0.8,
        behavioral_score=0.1,
        narrative_score=0.9,
        behavioral_summary="low activity",
        narrative_summary="high claims",
        evidence_note="5 days, 1 snippet"
    )
    forbidden = [
        "diagnosis", "personality", "character",
        "lazy", "undisciplined", "medical"
    ]
    result_str = str(result).lower()
    for word in forbidden:
        assert word not in result_str


def test_abstention_has_no_divergence_type():
    result = make_abstention("sleep", "only 1 day of data")
    assert "divergence_type" not in result
    assert result["status"] == "insufficient_evidence"