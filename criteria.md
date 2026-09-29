# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

> **Revised in unit 2:** Every source document an answer cites supplied at
> least one fact used in that answer.
>
> **Why revised:** the original measured presence, not correctness. In the
> before-run, two of three runs of "which is the easiest town in the region"
> cited `guide_accessibility.md` *and* `guide_walking.md`; run 2's entire
> answer was "Thornby Wells is the easiest town in the region," a single fact
> from the first file, with the second named anyway. The original criterion
> passed that. It could be measured consistently — it just measured the wrong
> thing, so a system that invents citations would clear it.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. Something about your chunks

No chunk is under 40 characters or over 600 characters, checked across all chunks generated from the test corpus.
<!-- .

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**
This run measured shortest = 24, longest = 800 — both outside the bound I'm setting. I'm setting it anyway, tighter than what came out: a 24-char chunk in this corpus is almost certainly a heading with the body split into the next chunk (there's no way to answer anything from 24 characters of Markdown), and an 800-char chunk is long enough to span two or three of the short town entries this guide uses, which would hurt retrieval precision by making one chunk "about" multiple places at once. Since the current run fails this on both ends, this criterion is telling me fallback_split needs a real fix, not just a passing grade — that's the target doing its job.


---

## 5. Your choice

In a random sample of 5 chunks, at least 4 read as a complete thought — no chunk starts or ends mid-sentence.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**

Chunk 1 above cuts off after "The station is a 15-" — a sentence severed mid-word, not mid-idea, which is worse: a reader can't even guess what the missing word says. This is the exact failure mode retrieval-based QA can't route around: if the retrieved chunk is incomplete, a correct retrieval still produces a wrong or unanswerable response. I set it at 4 of 5, not 5 of 5, because with a 650-char average budget and prose that doesn't chunk on clean paragraph breaks, occasional boundary spillover is likely structural to fallback_split rather than something I can eliminate without switching splitting strategies — so 5/5 would be a target I can't hit without more work than this milestone calls for, and 4/5 still catches the case I actually saw.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
