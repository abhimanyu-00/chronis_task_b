# Decisions — Chronis Task B
## Behavioral–Narrative Divergence Scoring

---

## 1. Problem Understanding

Chronis captures continuous real world behavioral signals
through the locket device — voice, video, motion, and
heart rate. From these signals the system infers behavioral
facts about the person automatically, without any manual
input.

Self-talk is extracted separately from the same voice
signal — specifically when the person speaks first-person
statements about themselves.

The gap between what a person does and what they say about
themselves is the primary signal this system measures.
This gap is not an error to be reconciled — it is the
core signal to be characterized and typed.

---

## 2. Input Design

### Why text sentences for behavioral input

In the real Chronis world, behavioral data does not arrive
as clean numeric arrays like step counts or hours logged.
The locket infers behavioral facts from sensor signals
and expresses them as structured observations:
"skipped planned workout session"
"worked past midnight to meet deadline"
"met friends for dinner in the evening"


This is more faithful to how Chronis actually operates
than using numeric arrays. The device captures voice,
video, motion, and heart rate — and derives meaning
from those signals as text observations.

### Why text sentences for self-talk input

Self-talk is captured directly from voice when the person
speaks first-person statements about themselves. It
arrives as plain sentences with no preprocessing needed.
"I have been staying very active lately"
"Work has been pretty slow this week"


### Why behavior and self-talk are kept separate

The PDF requires per-domain divergence scoring. Divergence
means the distance between two things. If behavior and
self-talk are merged into one signal, the gap disappears
and classification becomes impossible.

Both sides are scored independently and then compared.

### Dataset structure

Data is organized in a single file per person with
behavior and self-talk grouped by domain:
Domains: fitness, work, diet, social, sleep
Behavior: 5 days per domain (except sleep — 1 day)
Self-talk: 3 snippets per domain


Sleep has only 1 day deliberately to demonstrate the
abstention case required by the assessment brief.

5 behavioral days satisfies "a few days" from the brief.
3 self-talk snippets satisfies "a small set" from the brief.

---

## 3. Alignment Method — Lexical Keyword Matching

### Method chosen

Lexical keyword matching with two layers:
- Layer 1: domain knowledge words — general vocabulary
  that works for any sentence about this domain
- Layer 2: dataset specific words — vocabulary unique
  to this synthetic dataset, documented separately

### How it works

Three word lists are defined:

Positive words — person IS actively doing the behavior
→ sentence scores 1

Negative words — person is NOT doing the behavior
→ sentence scores 0

Goal words — person WANTS to do but has not done it
→ used to detect aspiration gap type only

Each sentence is scanned for these words. Negative list
is checked first. If a negative word is found, score = 0.
If a positive word is found, score = 1. If nothing is
found, score = 0.5 (neutral, no signal).

All behavioral day scores are averaged into one
behavioral score between 0 and 1.

All self-talk snippet scores are averaged into one
narrative score between 0 and 1.

Gap = narrative score minus behavioral score.

### Why lexical over embedding

The assessment brief states:

> "A simple, well-explained solution is preferred over
> an unnecessarily complex one"

> "We value clarity, reasoning, explainability"

Lexical keyword matching is the simplest approach where
every scoring decision is fully traceable to a specific
word in the input. No external model, no library, no
GPU needed. Anyone can read the code and understand
exactly what it is doing and why.

Embedding based approaches understand meaning more
accurately but are harder to explain, require external
libraries, and add complexity without adding value
for this assessment scope.

### Why two layer keyword design

Keywords derived only from the dataset are overfitted —
they only work for sentences already seen. Keywords
derived only from domain knowledge may miss dataset
specific vocabulary.

Two layers solve this:
- Layer 1 generalizes to new sentences
- Layer 2 handles dataset specific vocabulary
- Both layers documented separately for transparency

### Assumptions

1. Layer 1 domain knowledge keywords cover primary
   vocabulary and generalize beyond this dataset

2. Layer 2 dataset specific keywords supplement layer 1
   for words unique to this synthetic dataset and are
   documented separately

3. First matching word determines sentence score

4. Negative list checked before positive list

### Failure modes

1. Complex negation not handled —
   "I would not say I was inactive" would score wrongly
   because "inactive" triggers negative score

2. Synonyms outside keyword lists are missed entirely —
   new food names, regional language, informal slang
   give neutral score 0.5

3. Sarcasm not detected

4. Dataset specific terms will not generalize to new
   data — real world deployment needs expanded lists

5. Single matching word determines entire sentence score —
   mixed sentences like "went to gym but skipped cardio"
   score based on whichever word appears first in scan

---

## 4. Evidence Sufficiency — Component 3

### Rules

- Minimum 3 days of behavioral data per domain
- Minimum 1 self-talk snippet per domain

### Why these thresholds

3 days is the minimum to establish a behavioral pattern.
1 day could be an outlier. 2 days is insufficient for
pattern confidence. 3 days gives a reasonable baseline
for a short assessment synthetic dataset.

1 self-talk snippet is the minimum to produce any
narrative score. Zero snippets means the domain is
completely absent from self-talk — which is handled
separately as blind spot classification.

### Behavior when evidence is insufficient

Evidence check runs before any scoring or classification.
If evidence check fails, the system returns immediately:

```json
{
  "domain": "sleep",
  "status": "insufficient_evidence",
  "reason": "only 1 day(s) of data, need at least 3"
}
```

No score is calculated. No type is assigned. The
classification function is never called. This is
structurally enforced — not just a warning.

---

## 5. Divergence Type Boundaries — Component 2

All four types have explicit numeric decision boundaries
documented here and in the code comments.
blind_spot:
behavioral_score >= 0.60
AND narrative_score <= 0.20
Domain is behaviorally prominent but self-talk
is silent or near silent about it.
Person does not acknowledge this domain exists
in their life narrative.

aspiration_gap:
goal language detected in self-talk
AND behavioral_score <= 0.35
Person repeatedly states intentions or wishes
but behavior shows flat or absent progress.
"want to", "planning to", "need to" + low behavior.

overstatement:
gap > +0.30
Narrative score much higher than behavioral score.
Person claims more than behavior supports.

understatement:
gap < -0.30
Behavioral score much higher than narrative score.
Person enacts more than they acknowledge.

aligned:
gap within -0.30 to +0.30
Narrative and behavior broadly consistent.


### Why this order of checks

Blind spot is checked first because a very low narrative
score could also satisfy understatement. Blind spot
requires both high behavior AND low narrative — checking
it first prevents misclassification.

Aspiration gap is checked before overstatement because
goal language changes the interpretation of a high
narrative score. The person is not claiming to do
something — they are expressing a wish to do it. These
are fundamentally different divergence types.

### Why blind_spot uses threshold not exact zero

Initial implementation used narrative == 0.0 for blind
spot. This caused misclassification when sentences scored
0.5 (neutral) pulling the average slightly above zero.

Changed to narrative <= 0.20 to handle sentences that
give weak or neutral signal — which is more honest about
how lexical scoring works in practice.

---

## 6. Output Safety — Component 4

### Structural prevention

The output schema contains only these fixed fields:
domain
status
divergence_type
gap_score
behavioral_score
narrative_score
behavioral_summary
narrative_summary
evidence_note


There is no free text field describing the person.
There is no field for diagnosis, personality assessment,
character judgment, or medical evaluation.

Medical and characterological statements are impossible
by construction — not by wording choice — because there
is no field in the output schema where such statements
could ever appear.

### What this system refuses to claim

- No medical diagnoses of any kind
- No personality assessments
- No character judgments such as lazy or undisciplined
- No causal explanations about why a person behaves
  a certain way
- No comparisons to population norms or averages
- No recommendations to seek professional help
- No predictions about future behavior

The system only characterizes a measured gap between
two signals. Nothing more.

---

## 7. What This System Does Not Do

This system does not explain why a gap exists.
This system does not judge the person.
This system does not make predictions about future behavior.
This system does not compare one person to another.
This system does not produce any output that could be
mistaken for a clinical or psychological assessment.
This system does not assign meaning to the gap beyond
its measured type and direction.

---

## 8. Known Limitations

1. Keyword lists are manually defined and may not cover
   all vocabulary variations in real world data

2. Lexical scoring does not understand sentence structure —
   word order and context are ignored

3. Three self-talk snippets per domain capture a pattern
   but remain a limited narrative signal — real world
   Chronis data would have far more self-talk observations

4. Synthetic dataset does not capture the full complexity
   of real Chronis locket data — real data would include
   mixed signals, ambiguous sentences, and cross-domain
   observations

5. Thresholds are set empirically for this synthetic
   dataset and would need recalibration for real world data

6. Single sentence per behavioral day is a simplification —
   real Chronis data would have multiple observations
   per day requiring aggregation logic

7. Cross-domain sentences are not handled —
   "skipped lunch to finish work" belongs to both
   work and diet but is scored for only one domain