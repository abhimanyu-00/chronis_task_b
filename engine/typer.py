# Component 2 — Divergence Typing

from engine.keywords import GOAL_WORDS

# Decision boundaries
OVERSTATEMENT_THRESHOLD  = 0.30
UNDERSTATEMENT_THRESHOLD = -0.30
ASPIRATION_BEHAVIOR_MAX  = 0.35
BLIND_SPOT_NARRATIVE_MAX = 0.20   # narrative this low = blind spot
BLIND_SPOT_BEHAVIOR_MIN  = 0.60   # behavior this high = prominent domain


def has_goal_language(snippets):
    for snippet in snippets:
        snippet_lower = snippet.lower()
        for goal_word in GOAL_WORDS:
            if goal_word in snippet_lower:
                return True
    return False


def classify(behavioral_score, narrative_score, snippets):
    """
    Classify divergence into exactly one of four types.

    Decision boundaries:
    blind_spot:     behavior >= 0.60 AND narrative <= 0.20
                    domain prominent in behavior but
                    barely or never mentioned in self-talk

    aspiration_gap: goal language detected AND behavior <= 0.35
                    person states intentions, behavior flat

    overstatement:  gap > +0.30
                    narrative much higher than behavior

    understatement: gap < -0.30
                    behavior much higher than narrative

    aligned:        gap within -0.30 to +0.30
    """
    gap = narrative_score - behavioral_score

    # Check blind spot first
    # domain is behaviorally prominent but
    # self-talk is silent or near silent about it
    if behavioral_score >= BLIND_SPOT_BEHAVIOR_MIN and \
       narrative_score <= BLIND_SPOT_NARRATIVE_MAX:
        return "blind_spot", gap

    # Check aspiration gap
    # goal language present + behavior is flat or low
    if has_goal_language(snippets) and \
       behavioral_score <= ASPIRATION_BEHAVIOR_MAX:
        return "aspiration_gap", gap

    # Check overstatement
    if gap > OVERSTATEMENT_THRESHOLD:
        return "overstatement", gap

    # Check understatement
    if gap < UNDERSTATEMENT_THRESHOLD:
        return "understatement", gap

    # Within normal range
    return "aligned", gap