"""
Deciding whether an answer was right.

`run_eval.py` finds `judge` here automatically and fills the Run columns with
pass/fail instead of leaving them blank.

An answer passes three checks, and all three have to hold:

  1. It isn't a refusal. The gate refusing a question I wrote on purpose is a
     failure of the system, not a neutral outcome.
  2. It names a source (criterion 2). Checked against what retrieval actually
     returned, so an answer citing a document that wasn't retrieved doesn't
     count as cited.
  3. It contains what `expects` names — AND so do the retrieved chunks
     (criterion 1). An answer that's right but isn't in the chunks it was given
     came from the model's own memory, not from my corpus, and for a retrieval
     system that's a failure dressed as a pass.

Why the matching is fuzzy rather than `expects in answer`: my `expects` values
were written in unit 1 as "a word or short phrase a correct answer contains",
not as literal substrings. "School bus or Car" names two acceptable answers;
"Mobile coverage is good in the town centres" is a sentence the model
paraphrases every run ("good in the centre (or town centres)"). A literal
substring test would have failed four of my five questions while the system was
answering them correctly, which would make the scorer measure phrasing rather
than correctness.

So: `or` and `/` in `expects` mean alternatives, any one of which is enough,
and a multi-word phrase matches when all of its content words are present
regardless of order or wording in between. That is deliberately looser than
exact match and it is the trade I'm making — it can't catch an answer that uses
all the right words to say the wrong thing.
"""

import re

# Mirrors gate.REFUSAL. Kept as a list of markers rather than importing gate,
# so this file stays cheap to import and still catches near-misses where the
# model hedges in its own words instead of the gate refusing outright.
REFUSAL_MARKERS = (
    "don t have enough information",
    "do not have enough information",
    "cannot answer",
    "can t answer",
    "no information about that",
)

# Flip to False to score correctness alone and measure criterion 2 separately.
REQUIRE_SOURCE = True

# Flip to False to accept a right answer that wasn't in the retrieved chunks.
REQUIRE_GROUNDING = True

# Words too common to carry meaning — dropped before the all-words-present test,
# or "Mobile coverage is good in the town centres" would fail on "the".
STOPWORDS = frozenset(
    """a an the is are was were be been do does did of in on at to for from by
    with and it its this that there here what when where which who how you your
    i my as or not no if then than so about into over under""".split()
)


def judge(question: str, expects: str, answer: str, results: list) -> bool:
    """Did this answer get the question right?

    `question` isn't used to decide — it's in the signature because a judge
    that needed to (one calling a model, say) would need it, and because a
    verdict you can't trace back to its question is hard to debug.
    """
    return not reasons_to_fail(question, expects, answer, results)


def reasons_to_fail(question: str, expects: str, answer: str, results: list) -> list[str]:
    """Same decision as `judge`, but says why. Empty list means pass.

    Use this when a verdict in the run log surprises you: the reason is the
    difference between fixing the system and fixing the scorer.
    """
    failures = []
    answer_text = _normalize(answer or "")

    if not answer_text.strip():
        return ["empty answer"]

    if any(marker in answer_text for marker in REFUSAL_MARKERS):
        return ["refused — the gate or the model declined to answer"]

    if REQUIRE_SOURCE and not _names_a_source(answer_text, results):
        failures.append("names no source that retrieval actually returned")

    if not expects.strip():
        # Nothing was written down in unit 1 to check against, so correctness
        # can't be judged here. Says so rather than passing quietly.
        failures.append("questions.py has no `expects` for this question")
        return failures

    matched = _match(expects, answer_text)
    if matched is None:
        failures.append(f"answer doesn't contain what `expects` names ({expects.strip()!r})")
    elif REQUIRE_GROUNDING:
        chunks = _normalize(" ".join(getattr(r, "text", "") for r in results or []))
        if _match(matched, chunks) is None:
            failures.append(f"{matched!r} isn't in the retrieved chunks — not grounded")

    return failures


# ─── The matching, such as it is ─────────────────────────────────────────────


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation and markdown, pad with spaces.

    The padding is what makes `" word " in text` a whole-word test: every token
    in the result is surrounded by exactly one space on each side.

    Digit-group commas go first, so `12,000` and `12000` are the same number.
    Everything else non-alphanumeric becomes a space, which also flattens
    `` `guide_kestrelford.md` `` to `guide kestrelford md` — the same shape the
    source name gets, so the two still compare.
    """
    text = re.sub(r"(?<=\d),(?=\d)", "", text.lower())
    return " " + " ".join(re.sub(r"[^a-z0-9]+", " ", text).split()) + " "


def _alternatives(expects: str) -> list[str]:
    """`"School bus or Car"` -> `["school bus", "car"]`. Any one is enough."""
    parts = re.split(r"\s+or\s+|/", _normalize(expects).strip())
    return [p.strip() for p in parts if p.strip()]


def _match(expects: str, text: str) -> str | None:
    """Return the alternative that matched, or None. Truthy is a match.

    Returns *which* one matched so the grounding check can look for the same
    alternative in the chunks, rather than passing because the answer said
    "school bus" and the chunks happened to mention a car.
    """
    for variant in _alternatives(expects):
        if f" {variant} " in text:
            return variant  # said it outright

        words = [w for w in variant.split() if w not in STOPWORDS]
        if len(words) > 1 and all(f" {w} " in text for w in words):
            return variant  # said it in its own words, in some other order

    return None


def _names_a_source(answer_text: str, results: list) -> bool:
    """Does the answer cite a document that retrieval actually handed it?

    Matches the stem too (`guide_kestrelford` for `guide_kestrelford.md`),
    because the model drops the extension about as often as it keeps it.
    """
    for result in results or []:
        source = _normalize(getattr(result, "source", "")).strip()
        if not source:
            continue
        stem = source.rsplit(" ", 1)[0] if " " in source else source
        if f" {source} " in answer_text or f" {stem} " in answer_text:
            return True
    return False


# ─── A check on the checker ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Real answers from results/run_2026-09-23_1924_before.md, hand-labelled.
    # If the scorer disagrees with me here, the scorer is wrong.
    class _R:
        def __init__(self, text, source):
            self.text, self.source = text, source

    coverage = [_R("Mobile coverage is good in the town centres and patchy on "
                   "the outskirts", "guide_accessibility.md")]
    corry = [_R("There is no public transport into the valley beyond a school "
                "bus that will carry passengers if there is room.", "guide_corry_vale.md")]
    pop = [_R("Kestrelford is a hill town of 12,000, an hour inland.",
              "guide_kestrelford.md")]

    cases = [
        ("What is the population of Kestrelford", "12,000",
         "Kestrelford has a population of 12,000 (from guide_kestrelford.md).", pop, True),
        ("Where is the best mobile coverage", "Mobile coverage is good in the town centres ",
         "Based on the provided documents, mobile coverage is good in the centre "
         "(or town centres) and patchy on the outskirts.\n\nSources:\n- "
         "`guide_accessibility.md`", coverage, True),
        ("How do I get to Corry Vale ?", "School bus or Car",
         "There is also a school bus that will carry passengers if there is room.\n\n"
         "Source: `guide_corry_vale.md`", corry, True),
        # Right answer, no source named — fails criterion 2.
        ("What is the population of Kestrelford", "12,000",
         "Kestrelford has a population of 12,000.", pop, False),
        # Right answer, wrong number.
        ("What is the population of Kestrelford", "12,000",
         "Kestrelford has a population of 30,000, per guide_kestrelford.md.", pop, False),
        # Refused.
        ("What is the population of Kestrelford", "12,000",
         "I don't have enough information about that.", pop, False),
        # Cites a document retrieval never returned.
        ("What is the population of Kestrelford", "12,000",
         "Kestrelford has 12,000 people (guide_brightwater.md).", pop, False),
    ]

    failed = 0
    for question, expects, answer, results, want in cases:
        got = judge(question, expects, answer, results)
        if got != want:
            failed += 1
            why = reasons_to_fail(question, expects, answer, results)
            print(f"MISMATCH want {want} got {got}: {answer[:60]}...\n  {why}")

    print(f"{len(cases) - failed} of {len(cases)} self-tests passed.")
