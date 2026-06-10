# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
it covers thing related to the dinning hall, from what options of food they have, accessblity and other basic queries
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Google Maps | review| CleveReviews.txt|
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
each review got one chunk 
**Overlap:**
None — reviews are self-contained units
**Why these choices fit your documents:**
because the data i have collected is small
**Final chunk count:**
7
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2
**Production tradeoff reflection:**
handles up to 256 tokens which is sufficient for individual reviews.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
I did not use any oustside sources to collect the reviews other than google maps, It was the reason that the MML is not able to answer clearly all the normal questions. It should answer things related to the car or the food types. 
**How source attribution is surfaced in the response:**
it takes from the dataset chunks and uses it directly to create response 
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Are there good vegetarian options? | Yes — multiple reviews mention vegetarian/vegan offerings, some highly recommend it with a large, clearly labeled selection. | Yes, there are good vegetarian options; cites Megan Harris and Mary Baker (large selection, clearly labeled) and notes Mariah Sprague only "somewhat" recommends. | Relevant | Accurate |
| 2 | How are the prices? | Reasonable; most reviewers report $10–20 per person, coffee-only visits $1–10. | Prices are reasonable, mostly $10–20 per person; Patti Magers paid $1–10 for coffee; "All The Way" called them reasonable. | Relevant | Accurate |
| 3 | Do they accept cash? | No — card only, per Mariah Sprague's review. | No, per Mariah Sprague they do not take cash, so bring a card. | Relevant | Accurate |
| 4 | How is the breakfast, especially the pancakes? | Poor — Shael warns pancakes were undercooked and berry sauce tasted defrosted (Food: 1), though yogurt is decent. | Not recommended; pancakes "super undercooked," defrosted-tasting berry sauce, rated 1/5, but yogurt is decent. | Relevant | Accurate |
| 5 | What are the parking and hours like? | Parking is somewhat hard, free street parking available; hours are not covered in the reviews. | "I don't have enough information on the hours." Parking can be hard to find with free street parking; one older review mentions easy parking. | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What are the parking and hours like?" (Question 5)

**What the system returned:** It answered the parking half correctly but said "I don't have enough information on the hours." It also pulled a parking detail from a two-year-old review that partly contradicts the newer ones.

**Root cause (tied to a specific pipeline stage):** This is a data/ingestion-stage gap, not a retrieval or generation bug. The source file (`documents/CleveReviews.txt`) is scraped Google Maps reviews, and none of them mention opening hours — so no chunk containing hours exists to embed or retrieve. The grounding instruction in the system prompt then correctly forced the model to refuse rather than invent hours. The contradictory parking detail surfaced because chunking is one-review-per-chunk with no timestamp weighting, so an outdated review is retrieved with equal priority to recent ones.

**What you would change to fix it:** Feed it more data — collect more reviews and add a source that actually contains hours (e.g. the dining hall's official page), and store the data in a tighter, more structured frame (e.g. tag each review with its date) so the retriever can prefer recent information over stale reviews.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Architecture diagram and the per-milestone AI Tool Plan in planning.md gave me concrete inputs to hand to Claude for each stage instead of vague requests. Because I had already decided "1 review = 1 chunk, no overlap, all-MiniLM-L6-v2, top-k=4," the generated `ingest.py`, `embed.py`, and `query.py` lined up with my design on the first pass and I mostly had to verify rather than redesign. Having the grounding rule written down in advance is also why `query.py` correctly refuses to answer about hours instead of hallucinating.

**One way your implementation diverged from the spec, and why:** My Chunking Strategy section said I would split reviews using a `-Name` regex pattern, but the actual `ingest.py` just checks `line.startswith("-")` line by line — a simpler scan that was easier to debug and handled the file fine, so a full regex was unnecessary. I also revised my Evaluation Plan: my planned expected answers (e.g. "$20–30 per person," "plenty of parking," "4.3 stars") turned out not to match the real Google Maps data, which says $10–20 and "somewhat difficult to find parking" and has no overall star rating. I updated the expected answers to reflect what the reviews actually contain, since the point of evaluation is to test against the corpus, not my initial guesses.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md (reviews separated by a `-Name` pattern, no fixed size, no overlap) and asked Claude to implement `load_and_chunk()` in `ingest.py`.
- *What it produced:* A function that read the file and grouped lines into one chunk per review, attaching the filepath as the source.
- *What I changed or overrode:* The plan called for a regex split, but I kept the simpler `line.startswith("-")` scan it produced because it was easier to read and worked on my file; I verified it by printing chunks and checking each started with a name.

**Instance 2**

- *What I gave the AI:* My running app threw `Error code: 401 - Invalid API Key` and returned nothing. I gave Claude `app.py`, `query.py`, and my `.env` setup and asked why the app would not answer.
- *What it produced:* It traced the failure to a placeholder key (`your_key_here`) still sitting in `.env`, noticed I had pasted my real key into `.env.example` (which is tracked by git) by mistake, and added a `try/except` around `ask()` in `app.py` so API errors show in the UI instead of failing silently.
- *What I changed or overrode:* I accepted the error-handling change and moved my key into the correct `.env` file. I directed it to also restore the placeholder in `.env.example` so my key would not be committed.
