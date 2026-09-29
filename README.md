# The Unofficial Guide

<!-- Ashish city_guides -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:**
not set by a character count. Chunks are one ## section each, which lands them at 94 chunks averaging 319 characters (range 183–758). The corpus is 14 markdown guides where every section is already one self-contained topic — a character budget would cut across those boundaries for no benefit. The starter's 800-character window opened 35 of its 51 chunks mid-word.

**Overlap:**
0. Overlap exists to repair damage from cutting in the wrong place. Cutting on headings never cuts in the wrong place, and duplicated sentences would compete against each other for slots in the top-5.

**Context prefix** Nine of the fourteen documents are town guides sharing the identical seven headings, and 61 of their 63 sections never name their own town. Stored raw, there would be nine interchangeable "Getting there" chunks. Each chunk's text therefore opens with Town — Heading.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->
     

Printed by `python app.py chunks --indices 0,12,45,70,93`. All five come from
`chunker.py::split_documents`, which is what the pipeline actually calls.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

    Getting around the region with limited mobility — Overview

    An honest assessment rather than a promotional one. Some of these places are
    difficult and it is better to know in advance.

**Chunk 2** — source: `guide_brightwater.md#5` — produced by: `chunker.py::split_documents`

    Brightwater — Where to stay

    Accommodation is thin and expensive during graduation week and in early
    September. Outside those windows there is more supply than demand. The two
    hotels on the riverside are the obvious choice and the guesthouses on Corry
    Lane are better value.

**Chunk 3** — source: `guide_halden_bay.md#0` — produced by: `chunker.py::split_documents`

    Halden Bay — Overview

    Halden Bay is a working fishing port of 8,000 that has picked up a second
    life as a weekend destination. The two economies sit somewhat awkwardly
    beside each other and the town is candid about it.

**Chunk 4** — source: `guide_pellew_sands.md#1` — produced by: `chunker.py::split_documents`

    Pellew Sands — Getting there

    The branch line runs from the regional hub in 70 minutes, seven times a day,
    and the station is on the seafront, which is rare and pleasant. Driving is 50
    minutes from Brightwater. Seafront parking is metered and expensive; the free
    lot behind the station is a four-minute walk and almost always has space.

**Chunk 5** — source: `guide_walking.md#0` — produced by: `chunker.py::split_documents`

    Walking in the region — Easy, on good surfaces

    The **Brightwater river path** runs four miles upstream from the town to a
    weir, on a made surface, flat throughout. It is the most-walked route in the
    region and deservedly so. Continuing downstream from Givens Mill reaches
    Brightwater in about three hours.

Could someone answer a question from each of these alone? Chunks 2, 3 and 4 name
their town in the first line and answer one question completely, so yes. Chunk 1
is the weakest of the five: it is a preamble that says the guide is honest
without saying anything about any place, and it would be retrieved for questions
it cannot answer — which is exactly what happened to "which is one the easiest
town in the region" before unit 2's fix, where this chunk ranked first at 0.5335
while the chunk that held the answer ranked third.

Chunk 5 is a case the unit 2 fix created. `walking — Easy, on good surfaces` was
607 characters covering three separate routes; it is now one route per chunk,
which is why this one stops after the river path.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
How do I get to Corry Vale?

Gate: best distance 0.313, under the 0.67 cutoff

**Answer:**
A: According to guide_corry_vale.md, visitors drive from Brightwater (35 minutes on a good road to the valley mouth and another 20 on a poor one) or cycle in, though cycling is a serious undertaking with a 400-metre climb in the first four miles. There is also a school bus into the valley that will carry passengers if there is room, as there is no other public transport.

Sources retrieved: guide_corry_vale.md, guide_walking.md


**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

top_k = 8. Chosen by measuring where the chunk containing each answer actually ranks: 1, 1, 1, 3, and 8. At the starter's k=5, "How do I get to Corry Vale?" retrieved Where to stay, What to see, Getting around and When to go — every Corry Vale section except Getting there, which holds the answer. The gate passed at 0.3125, so the system would have answered confidently from the wrong section. k=8 is the smallest value that reaches every gold chunk; it costs about 640 tokens per call.

**THRESHOLD = 0.67.** Measured, not guessed. All ten questions, sorted by
distance:

| Question | In corpus? | Best distance |
|---|---|---|
| What is the population of Kestrelford | yes | 0.2689 |
| When did Kestrelford's Saturday market start | yes | 0.2748 |
| How do I get to Corry Vale | yes | 0.3125 |
| What is mobile coverage like in Corry Vale | yes | 0.3871 |
| Which is one the easiest town in the region | yes | 0.5335 |
| What is the capital of Mongolia | no | 0.8104 |
| What is the recommended dosage of ibuprofen for a headache | no | 0.8351 |
| How do I write a for loop in Rust | no | 0.8614 |
| How do I change the oil in a diesel engine | no | 0.8809 |
| Who won the 1994 World Cup | no | 0.9692 |

The two groups do not overlap. The worst in-corpus question is 0.5335 and the
best out-of-corpus one is 0.8104, so there is a 0.277-wide band with nothing in
it, and 0.67 is close to its midpoint (0.672) — about 0.137 of margin on each
side. The starter's 0.6 sat *below* my worst in-corpus question, so it would
have refused a question my documents answer; that was the error I found rather
than a number I inherited.

One of these five questions changed during Milestone 4. "Where is the best
mobile coverage" had no right answer — the sentence "mobile coverage is good in
the centre and patchy on the outskirts" appears verbatim in all ten town guides,
so any answer was both right and wrong and nothing could score it. I narrowed it
to Corry Vale, which has a specific answer in a specific file.


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I used Claude code for wirting the chunking function, it kept return fallback_split(documents) even though it was unnecessary. So, I removed it.
**2.**
Used Calude to fingure out the most ambiguous question with no unique answers, and then I decided to make that question ask something more specific.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2b. *(revised)* Every cited file supplied a fact | 5 of 5 | 5/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk under 40 or over 600 characters | all | 91/94 | 91/94 | 91/94 | MISSED |
| 5. 4 of 5 sampled chunks are complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Source: `results/run_2026-09-27_2355_before.md`, produced by `run_eval.py::main`
with `scorer.py::judge`. Criteria 4 and 5 are not measured by `run_eval.py` —
they come from `chunker.py::describe` via `python app.py index` and a seeded
5-chunk sample of `chunker.py::split_documents`. Chunking and the gate are both
deterministic, so their numbers are identical across the three columns.

**Criterion 1 — real output** (`run_eval.py::main`, run 1):

    Which is one the easiest town in the region
    Best distance: 0.5335 (passed the gate)
    Sources retrieved: guide_accessibility.md, guide_corry_vale.md, guide_walking.md

**Criterion 2b — the miss** (`run_eval.py::main`, run 2):

    Thornby Wells is the easiest town in the region.
    Source: guide_accessibility.md (and guide_walking.md)

`guide_walking.md` supplied nothing in that sentence.

**Criterion 3 — real output** (`run_eval.py::check_out_of_scope`, cutoff 0.67):

    refused  (best distance 0.810)  What is the capital of Mongolia?
    refused  (best distance 0.881)  How do I change the oil in a diesel engine?
    refused  (best distance 0.969)  Who won the 1994 World Cup?
    refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
    refused  (best distance 0.861)  How do I write a for loop in Rust?
    -> gate refused 5 of 5

**Criterion 4 — the miss** (`chunker.py::describe`):

    chunked  94 chunks, 319 characters on average (shortest 183, longest 758),
             produced by chunker.py::split_documents

    over 600: 3
       758  guide_accessibility.md :: Getting around the region with limited mobility — Straightforward
       661  guide_eating.md        :: Eating across the region — The pattern worth knowing
       607  guide_walking.md       :: Walking in the region — Easy, on good surfaces


<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | `scorer.py` has `REQUIRE_GROUNDING = True`, so a pass means the `expects` value was present in the retrieved chunks, not just in the answer. 5 of 5 on all three runs against a target of 4 of 5. |
| 2 | Every answer names a source | MET | As written, all 15 answers named at least one retrieved document; `scorer.py::_names_a_source` checks the cited file against what retrieval actually returned. It holds — but see 2b. |
| 2b | *(revised)* Every cited file supplied a fact | MISSED | Runs 2 and 3 of "easiest town" cited `guide_walking.md` alongside `guide_accessibility.md` while using only the latter. 4 of 5 against a target of 5 of 5, in two of three runs. A target that holds once is not met. |
| 3 | Gate stops out-of-corpus questions | MET | All 5 out-of-scope questions sat at 0.810–0.969, well clear of the 0.67 cutoff. One deterministic pass, so one number. |
| 4 | No chunk under 40 or over 600 characters | MISSED | 3 of 94 chunks were over 600 (758, 661, 607). The criterion says "no chunk," so three is a miss, not a rounding error. |
| 5 | 4 of 5 sampled chunks are complete thoughts | MET | A seeded random sample of 5 chunks; all 5 began with a capital or a bold marker and ended on terminal punctuation. 5 of 5 against a target of 4 of 5. |


## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

Criterion 4 — MISSED (91 of 94 chunks in bounds). Stage: chunking.

chunker.py::split_documents emitted one chunk per ## section and never checked length. Three chunks breached the 600-character bound: accessibility — Straightforward (758), eating — The pattern worth knowing (661), walking — Easy, on good surfaces (607).

These are not three separate problems. All three are thematic guides, and all three bundle a list under one heading — three towns, two paragraphs, three routes respectively. The nine town guides never breach the bound, because there every ## section is one paragraph about one topic. My Milestone 3 strategy assumed one section = one thought. That holds for town guides and fails for thematic ones.

The same assumption caused a separate problem I found in unit 1: accessibility — Practical packs hospital locations and mobile coverage under one heading, and it is the only place in the corpus stating that coverage is "genuinely absent in parts of Corry Vale." It ranks 14th of 94 at distance 0.798 for any coverage question — beyond any cutoff in my gap. Same root cause, different symptom.

### Criterion 2b — MISSED (4 of 5 in two of three runs). Stage: generation.

`GROUNDING_INSTRUCTION` in `generate.py` says "Name the document your answer
came from" and nothing about not naming others. The model had two chunks
mentioning Thornby Wells and no reason to prefer one: `accessibility —
Straightforward` at 0.5853 and `walking — Easy, on good surfaces` at 0.5962,
0.011 apart. Faced with near-identical evidence from two files, it hedged and
cited both, even when it used only one.

That distance gap is itself a chunking artefact. The accessibility chunk was
758 characters covering three different towns, so its Thornby Wells content was
diluted by Marchwood and Brightwater — which is the same defect criterion 4
names. **The two misses have one cause.**


## The Improvement

**What I changed:** two things, and they are not equal.

The measured fix: `MAX_CHUNK = 600` and a helper `chunker.py::_fit`. Sections
whose assembled chunk would exceed 600 characters are split again on blank
lines, each piece keeping its `Title — Heading` prefix. Sections at or under
the limit are untouched.

A second, smaller change: one rule added to `GROUNDING_INSTRUCTION` in
`generate.py` — "Name only the files whose text you actually used."

**Why I picked them:** my diagnosis named chunking, and I split the thematic
guides' lists at the boundary the author already wrote. I split only oversized
sections, so 91 of 94 chunks stayed byte-identical. The grounding rule was
written in unit 1 against the over-citation I had observed, and I intended to
defer it — but I applied it at 22:29:20, six minutes before the after-run at
22:35:16, alongside the chunker change at 22:29:46. So the after-run measures
both, which is the confound Milestone 4 warns about, and I caused it.


### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2b. *(revised)* Every cited file supplied a fact | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk under 40 or over 600 characters | all | 99/99 | 99/99 | 99/99 | MET |
| 5. 4 of 5 sampled chunks are complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Source: `results/run_2026-09-29_2235_after.md`.

    chunked  99 chunks, 306 characters on average (shortest 153, longest 566),
             produced by chunker.py::split_documents

**Did it help?** Yes. Criteria 4 and 2b both went from MISSED to MET. But my
after-run could not tell me *which change* did it, so I ran a controlled test
to find out.

Criterion 4 was the target and is unambiguous: 94 → 99 chunks, longest 758 →
566, nothing under 40 or over 600. Only the chunker touches chunk length.

Criterion 2b is the one the confound threatened, because the grounding rule
forbids exactly the over-citation it measures. I re-ran "which is the easiest
town in the region" three times against the **new chunks** with the **original**
instruction, bypassing the added rule:

    run 1: Thornby Wells is the easiest town in the region. Source: guide_accessibility.md
    run 2: Thornby Wells is the easiest town in the region. Source: `guide_accessibility.md`
    run 3: Thornby Wells is the easiest town in the region (guide_accessibility.md).

One source, three for three. So the chunking fix alone is sufficient, and the
grounding rule is a guard rather than the cause.

| | chunks | instruction | over-cites |
|---|---|---|---|
| Before-run | 94, oversized | original | yes, 2 of 3 runs |
| Isolation test | 99, split | original | no, 0 of 3 |
| After-run | 99, split | + citation rule | no, 0 of 3 |

The mechanism: the 758-character accessibility chunk became three paragraphs,
one per town, so Thornby Wells is now its own 322-character chunk at rank 1,
0.3557 — with a 0.079 margin over the runner-up, where before the two candidate
files sat 0.011 apart at 0.5853 and 0.5962. Given two near-tied sources the
model hedged and cited both; given a clear winner it cited one.

What did **not** move: gold-chunk containment. Ranks were 1, 1, 1, 3, 8 before
and 1, 2, 8, 1, 1 after — still 4 of 5 in the top three and 5 of 5 in the top
eight. The fix improved retrieval's margin, not its coverage.



## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

**Over-citation is fixed twice over, and guarded by accident.** Criterion 2b
passes, and the isolation test shows either change would have carried it alone.
That is more luck than design: I applied the grounding rule without meaning to
include it in this unit, and only found out by comparing file timestamps
against the run log. What is genuinely unresolved is that I have no measurement
of the grounding rule on its own — I know it is not *necessary* for this
question, not whether it helps on any other. Running a third eval with the
chunker fix reverted would settle it, and I did not do that.

**The thematic-guide retrieval gap.** Splitting oversized sections fixes chunk
size but not this. `accessibility — Practical` is 378 characters, so it was
never oversized and the fix never touched it — yet it is the only chunk in the
corpus stating that mobile coverage is "genuinely absent in parts of Corry
Vale," and it still ranks 15 of 99 at distance 0.798 for any coverage question.
That is beyond every cutoff in my gap, so the fact is unreachable no matter
where I put the threshold.

The cause is the title prefix I added in unit 1. For the nine town guides the
document title *is* the discriminating fact, and prefixing it is what made
"How do I get to Corry Vale?" work at all. For the thematic guides it misleads:
58 characters of "getting around the region with limited mobility" are glued to
a body about hospitals and phone signal, and the mobility framing dominates the
embedding. Fixing it means either dropping the prefix for thematic guides or
splitting on sentence groups rather than paragraphs. I could not justify either
as this unit's single measured change, and both would have re-indexed all 99
chunks and invalidated the comparison I had just made.


## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

**Criterion 1 was set too loose.** It asks whether the retrieved chunks contain
the answer, and `TOP_K = 8` means it asks about eight chunks. It scored 5 of 5
both before and after my fix, so it could not detect a real retrieval problem I
know exists: "How do I get to Corry Vale?" has its answer at rank 8 of 99 both
times. I would rewrite it as *"for at least 4 of 5 questions, the **top three**
results contain the answer."* That scores 4 of 5 today — it would still pass,
but it would fail the moment that question slipped one place, which is the
sensitivity I wanted and did not get.

**Criterion 3 was safe rather than easy.** A 0.277 gap between the worst
in-scope question (0.5335) and the best out-of-scope one (0.8104) means 4 of 5
was never in doubt. I would write it as 5 of 5 and add a second clause about
false refusals — no in-scope question refused — since that is the failure the
cutoff actually risks, and the starter's 0.6 would have tripped it.

**Criterion 4's bound was guessed, and it was right by accident.** I picked
600 in unit 1 while `fallback_split` was still producing 24–800 character
chunks, reasoning that 800 would span multiple town entries. That reasoning
turned out to describe the thematic guides exactly — the three chunks that
breached it were all multi-entry lists. I would keep the number and write down
the reason properly next time, because "no chunk covers more than one town or
route" is what I actually meant and is what I should have said.
