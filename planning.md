# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I have taken Cleveland Dinning hall review of my school Whitman College, the reviews are important because each was experincing different food reviews, and by knowing those information we can make search engine easier of the students opinion to this side of campus.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->
     CleveReviews.txt have been taken from Google maps reviews panel

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Google Maps | a reliable source open to interputation by the studnets | https://www.google.com/maps/place/Cleveland+Commons+Dining+Hall/@46.0689996,-118.3308477,17z/data=!4m8!3m7!1s0x54a26b36c0d9b3cd:0x2cf21989562b9260!8m2!3d46.0689996!4d-118.3282728!9m1!1b1!16s%2Fg%2F11fmyr96sh?entry=ttu&g_ep=EgoyMDI2MDYwMy4xIKXMDSoASAFQAw%3D%3D
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
the documents have varitiy of infomration, like they have when the year it was sent, what is the experince, each section of the dinning hall, and some small review. each is splitted using -theNameOfThePerson then the other details of their review 
**Chunk size:**
-name
No fixed character limit
**Overlap:**
Overlap is not needed; 
**Reasoning:**
 reviews are self-contained
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
Embedding model: all-MiniLM-L6-v2
**Top-k:**
4
**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Is there any the vegterian options? | there is a good varity of options to choose.
| 2 | What is the average price per person?| 20-30$ for a good set of meal|
| 3 |How is the customer servies? | Very good, the staff are nice|
| 4 | what is the overall rating? |4.3 starts out of 5 |
| 5 | is there any parking spaces for cars?|Yes there is plantey of spaces |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The information is not consistant, some of them mention things others do not, through that the answer will be formated using only one opinion even though the review might be old or solved

2.The Reviews might be faked, it does not actually show how the dinning hall is right now since most of them are outdated

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Document Ingestion          Chunking               Embedding + Vector Store
──────────────────         ──────────────         ────────────────────────
CleveReviews.txt     →     Split on -Name   →     all-MiniLM-L6-v2
(plain text file)          pattern (regex)         (sentence-transformers)
                           1 review = 1 chunk              ↓
                                                    ChromaDB (local)

        Retrieval                        Generation
        ─────────                        ──────────
  User query → embed query   →   Top-4 chunks as context
  → cosine similarity search  →   Groq llama-3.3-70b-versatile
  → return top-4 chunks       →   Gradio web UI displays
  (with source metadata)          answer + source citations
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I'll use Claude. Input: my Documents section (one .txt file, reviews separated by -Name pattern) and my Chunking Strategy section (split per review, no fixed character limit). Expected output: a working ingest.py with a load_and_chunk() function. I'll verify by running it and printing 5 chunks — each should start with a name, contain the full review text and metadata, and have no empty or malformed entries.
**Milestone 4 — Embedding and retrieval:**
I'll use Claude. Input: my Retrieval Approach section (all-MiniLM-L6-v2, ChromaDB, top-k=4) and the Architecture diagram above. Expected output: an embed.py that embeds all chunks and stores them in ChromaDB with source metadata, and a retrieve() function that takes a query string and returns top-4 chunks with their source. I'll verify by running 3 of my evaluation questions and checking that returned chunks visibly relate to each question.
**Milestone 5 — Generation and interface:**
I'll use Claude. Input: my grounding requirement (answer from retrieved context only, cite sources), the output format (answer + source list), and the Gradio skeleton from the project spec. Expected output: a query.py with an ask() function that calls Groq and enforces grounding, and an app.py with a working Gradio UI. I'll verify by asking a question my documents don't cover and confirming the system says it doesn't know rather than hallucinating.