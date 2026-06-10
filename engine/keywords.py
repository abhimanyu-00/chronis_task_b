# Keyword lists built from domain knowledge first,
# supplemented by dataset specific terms.
#
# Design decision:
# Layer 1 — domain knowledge words → general, work for any sentence
# Layer 2 — dataset specific words → work for this dataset only
#
# Both layers documented separately as required by PDF.
# Assumption and failure modes stated in decisions.md


# Positive words — person IS actively doing the behavior
# Layer 1: domain knowledge
POSITIVE_WORDS = [

    # fitness — general signals of physical activity
    "active", "exercise", "workout", "gym",
    "walked", "ran", "jogged", "cycled",
    "training", "fitness", "physical",

    # work — general signals of productive work
    "worked", "completed", "attended", "finished",
    "achieved", "productive", "meetings",
    "delivered", "submitted", "focused",

    # social — general signals of social engagement
    "met", "visited", "joined", "attended",
    "called", "connected", "socialised",
    "friends", "family", "colleagues",

    # diet — general signals of healthy eating
    "cooked", "healthy", "nutritious",
    "homemade", "vegetables", "fruits",

    # sleep — general signals of good sleep
    "slept", "rested", "early", "refreshed",
    "good sleep", "full night",

    # Layer 2: dataset specific positive words
    "crushing", "energetic", "consistent",
    "routine", "stayed", "went"
]


# Negative words — person is NOT doing the behavior
# Layer 1: domain knowledge
NEGATIVE_WORDS = [

    # fitness — general signals of physical inactivity
    "skipped", "cancelled", "avoided", "missed",
    "sedentary", "inactive", "lazy",
    "elevator", "no exercise",

    # work — general signals of low work activity
    "slow", "relaxed", "free time",
    "chill", "easy", "nothing much",
    "unproductive", "idle",

    # diet — general signals of unhealthy eating
    "junk", "unhealthy", "takeaway",
    "processed", "skipped meal",
    "did not cook", "ordered food",

    # social — general signals of social avoidance
    "stayed home", "alone", "isolated",
    "did not go out", "keeping to myself",
    "cancelled plans",

    # sleep — general signals of poor sleep
    "late", "sleepless", "tired",
    "no sleep", "restless", "awake",

    # Layer 2: dataset specific negative words
    "pizza", "chips", "biscuits",
    "fast food", "delivery", "watching tv",
    "sedentary", "midnight"
]


# Goal words — person WANTS to do but has not done it
# These are universal across all domains
# Used to detect aspiration gap type
GOAL_WORDS = [

    # Layer 1: domain knowledge goal signals
    "want to",
    "need to",
    "planning to",
    "going to",
    "will start",
    "trying to",
    "hope to",
    "plan to",
    "soon",
    "someday",
    "eventually",
    "next week",
    "from tomorrow",
    "have to",

    # Layer 2: dataset specific goal signals
    "start eating",
    "stop eating",
    "work on",
    "start a proper"
]