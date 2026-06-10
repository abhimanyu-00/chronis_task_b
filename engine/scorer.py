# Component 1 — Scoring
# Converts behavioral sentences and self-talk
# into scores between 0 and 1
# No matching step needed — self-talk is already
# grouped by domain in data.json

from engine.keywords import POSITIVE_WORDS, NEGATIVE_WORDS


def score_sentence(sentence):
    """
    Score a single sentence as 0, 0.5, or 1.
    0   = negative behavior found
    1   = positive behavior found
    0.5 = no signal found
    """
    sentence = sentence.lower()

    # Check for negative words first
    for word in NEGATIVE_WORDS:
        if word in sentence:
            return 0

    # Check for positive words
    for word in POSITIVE_WORDS:
        if word in sentence:
            return 1

    # No signal found
    return 0.5


def get_behavioral_score(daily_sentences):
    """
    Score all days and average them.
    daily_sentences is a dict like:
    {"day_1": "skipped gym", "day_2": "went for walk"}
    Returns a single score between 0 and 1.
    """
    scores = []
    for day, sentence in daily_sentences.items():
        score = score_sentence(sentence)
        scores.append(score)

    return sum(scores) / len(scores)


def get_narrative_score(snippets):
    """
    Score all self-talk snippets and average them.
    snippets is a list like:
    ["I have been active", "feeling very fit lately"]
    Returns a single score between 0 and 1.
    """
    if not snippets:
        return 0.0

    scores = []
    for snippet in snippets:
        score = score_sentence(snippet)
        scores.append(score)

    return sum(scores) / len(scores)