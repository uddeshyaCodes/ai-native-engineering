# Lecture 01: Search Foundations, Embeddings and Retrieval Strategy

**Course:** AI-Enabled Software Engineering · **Module 3:** Retrieval, Context Engineering and Evaluation
**Instructor:** Prof. Sandeep Chakraborty, Department of CSE, IIT Kharagpur
**TAs:** Srijit (assisting with the course) and Rudro (technical aspects and runtime support)
**Running example:** A fintech support assistant for an Indian lending app (loans, KYC, refunds), built on an 8-FAQ knowledge base in the labs. The second use case is a coding assistant on a 2-million-line repository.
**Labs:** Google Colab. Lab 1 BM25, Lab 2 semantic search, Lab 3 hybrid search with RRF, Lab 4 cross-encoder re-ranking, Lab 5 dimensionality reduction with OpenAI Matryoshka embeddings.
**Next lecture:** RAG end to end, chunking strategies, grounding and citations.

> **Transcript note:** The source is an auto-captioned transcript with many mis-hearings. Read "Oregon" as **search**, "I product" as **AI product**, "Cola" as **Colab**, "Lap" as **lab**, "Cormac" as **Cormack** (the RRF paper), "phases" as **FAISS**, "BM 2.5" and "BM 25" as **BM25**, "HN SW" as **HNSW**, "TS NE" as **t-SNE**, "Mississippi macro" as **MS MARCO**, "busy re ranker" as **BGE reranker**, "Qualicet" as **COALESCE**, and "Matriosca" as **Matryoshka**. Where a number is garbled (for example the golden-set size, some OpenAI prices and the 3072-dimension model size) the notes say so and use the figure that is consistent with the rest of the lecture.

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Explain why **retrieval quality** caps answer quality, and why adding more context is not the fix.
- Define **corpus, chunk, query, top-K, relevance** and the **offline versus online** phases of a search system.
- Compute **precision@K, recall@K, MRR** and explain why **NDCG** is used for graded relevance.
- Explain **TF, IDF, TF-IDF** and the two problems that **BM25** fixes (term-frequency saturation and length bias), including the roles of `k1` and `b`.
- Explain what an **embedding** is, how **contrastive learning** trains it, and why the **same model** must embed both documents and queries.
- Compare **cosine similarity, dot product and Euclidean distance**, and explain when they give the same ranking.
- Explain why **chunking** is needed and choose a sensible size and overlap.
- Explain **approximate nearest neighbour (ANN)** search and the **HNSW** graph with its `M` and `efSearch` knobs.
- Explain **hybrid search**, the score-scale problem, **weighted min-max fusion** and **Reciprocal Rank Fusion (RRF)**, and compute an RRF score by hand.
- Distinguish a **bi-encoder** (retriever) from a **cross-encoder** (re-ranker) and place both in a retrieval funnel.
- Choose an embedding model and dimension using six criteria, a golden set and the cost and privacy trade-offs.
- Apply **Matryoshka** dimension reduction and quantisation, and estimate storage with `N × D × 4 bytes`.

---

## Session map

| Block | Topic | Lab |
|-------|-------|-----|
| **Intro** | Why retrieval decides LLM quality; the three pillars; failure modes | None |
| **Part 1 - Foundations** | Vocabulary (corpus, chunk, query, top-K, relevance); offline and online phases; metrics | None |
| **Part 2 - Lexical search** | Tokenisation, inverted index, TF-IDF, BM25, strengths and weaknesses, Indian-language issues | **Lab 1:** BM25 on 8 FAQs with a score threshold |
| **Break** | | |
| **Part 3 - Semantic search** | Embeddings, contrastive learning, similarity measures, bi-encoders, chunking, ANN, HNSW, pgvector | **Lab 2:** MiniLM embeddings, cosine search, multilingual comparison |
| **Part 4 - Hybrid search** | Parallel retrieval, fusion problem, weighted fusion, RRF, SQL RRF | **Lab 3:** BM25 plus vector fused with RRF |
| **Part 5 - Re-ranking** | Retrieval funnel, cross-encoder, re-ranker options, latency, thresholding | **Lab 4:** MS MARCO cross-encoder re-ranks 4 candidates |
| **Part 6 - Choosing a model** | Six selection factors, MTEB caveat, OpenAI and Sentence Transformers options, cost, dimensions | **Lab 5:** Matryoshka dimension cut (1536 down to 4) |
| **Wrap-up** | Decision framework, model migration, DPDP and vectors | Take-home: build a v1 portal search with a golden set |

---

## Part 1: Why retrieval decides answer quality

### Three pillars and the LLM in the middle

Traditional software is deterministic: the same input gives the same output, and tests check exact answers. AI-native software adds an LLM whose output depends on its context, so the lecturer frames quality around three pillars:

| Pillar | Question it answers |
|--------|---------------------|
| **Retrieval** | Which few facts should be found from the data? |
| **Context** | What exactly does the model see, and in what order? |
| **Evaluation** | How do we measure whether the output is good, and improve it over time? |

The LLM is the generation step. The lecturer's claim: **the model is only as good as its context**, and most of the quality comes from the other three pillars. Industry practice he cites: with the same model, improving retrieval and context often gives a bigger quality jump than upgrading to a more expensive model.

### Why an LLM needs retrieved context

- An LLM has never seen your refund policy, codebase or customer tickets, and its knowledge stops at its training cut-off.
- If the wrong document is in the context, the model still writes a fluent, confident and **wrong** answer. This is the hallucination risk the lecturer links back to Module 1.
- Pasting every document into the prompt is not an option. The lecturer's example: a corpus of 100,000 documents cannot fit, and even a large window costs tokens and time.

### Why more context is not better

Stuffing 30 or 50 documents into every prompt causes three problems:

1. **Cost** rises (the lecturer's example: the monthly bill roughly triples).
2. **Latency** rises (roughly doubles in his example).
3. **Accuracy can fall.** Models miss facts "buried in the middle" of a long context, so precision suffers even when the right document is present.

The fix is to retrieve the **top few** relevant chunks and let the LLM write from those. This pattern is **Retrieval-Augmented Generation (RAG)**: find the facts first, then let the LLM write the answer.

### Three failure modes

| Failure | Example from the lecture | Why it is dangerous |
|---------|--------------------------|---------------------|
| **Bad retrieval** | Refund policy for business accounts is returned for a personal account | The LLM writes a perfect paragraph with the wrong refund timeline |
| **Bad context** | 30 documents stuffed in "to be safe" | Cost, latency and confusion all rise |
| **No evaluation** | Queries tested only in English; real users write Hinglish | The model silently breaks on real traffic |

**Key point:** in classical software a fixed test suite is enough. Here the output depends on context, so you need a **golden set of real queries** and statistical measurement.

### Use case 1: Fintech support assistant

- A lending app answers questions on loans, KYC and refunds.
- Scale: around 10,000 policy pages.
- Queries mix English, Hindi, Hinglish and other Indian languages, for example "EMI bounce charge" typed in a mixed script.
- Data contains personal information. Under the DPDP Act, processing needs consent, so the pipeline must mask PII and stay within budget.
- A good system means fewer escalations, correct policy answers and DPDP compliance.

### Use case 2: Coding assistant on a large repository

- A tool like Cursor or Claude Code must find the **relevant files, function signatures, documents and tests**, and their **order** matters.
- The repository (2 million lines) cannot fit in the window, so agentic tools read in a loop: read, decide what else to fetch, read again.
- Evaluation signal: does the generated change **compile and pass the tests**? Public benchmarks such as SWE-bench use this idea. Teams build internal versions on their own repositories.

### The same pattern everywhere

| Domain | Query example | What is retrieved |
|--------|---------------|-------------------|
| Enterprise knowledge | "What is our leave policy for ...?" | HR documents, wikis |
| E-commerce | "Cotton shirt for office under 1500" | Products among millions |
| Legal and compliance | "Which GST circular applies here?" | Circulars, contract clauses |
| Healthcare | Summarise a patient's history | Records (sensitive; DPDP applies strictly) |
| Education | Tutor that answers only from course material | Course sections |
| Agents | Which tool, memory or data to load at each step | Tools and memory items |

---

## Part 2: Vocabulary and evaluation metrics

### Six terms used throughout

| Term | Meaning |
|------|---------|
| **Corpus** | The whole collection of chunks (the lab has 8 FAQ entries; production has many thousands of chunks) |
| **Document or chunk** | One unit the system can return. Long PDFs are split so the user gets the exact paragraph, not a 40-page file |
| **Query** | What the user types. Usually short (about 3 to 8 words); documents are long, and this mismatch is part of why search is hard |
| **Index** | A structure, like the index at the back of a textbook, so you do not scan every chunk for every query |
| **Relevance** | How well a chunk answers a query. This is a human judgement; the system approximates it |
| **Top-K** | Return only the best K results (typically 5 or 10) |

### Two-phase architecture

| Phase | Steps | Frequency | Speed requirement |
|-------|-------|-----------|-------------------|
| **Offline** | Ingest, clean, chunk, embed, build the index | Once, or when documents change | Can be slow (minutes on GPU or API; longer on CPU) |
| **Online** | Embed the query, compare with the index, score, rank, return top-K | Every user query | Must be fast (milliseconds) |

**Rule:** documents and queries must be processed the same way. If you embed documents with model A and queries with model B, results become meaningless.

### The four standard metrics

A **golden set** is a set of real queries, each marked with the chunks that are correct. Run the search, then compare the results with the marks. The lecturer suggested a few hundred real queries (the exact figure is garbled in the transcript).

| Metric | Definition | Use |
|--------|-----------|-----|
| **Precision@K** | Fraction of the top K results that are correct | Fewer wrong results shown |
| **Recall@K** | Fraction of all correct chunks that appear in the top K | **Most important for RAG**: if the right chunk is not in the top K, the LLM never sees it |
| **MRR** (Mean Reciprocal Rank) | Average of 1/rank of the first correct result | How quickly the right answer appears |
| **NDCG@K** (Normalised Discounted Cumulative Gain) | Rewards correct results near the top and allows graded relevance (very relevant versus somewhat relevant) | Widely used; libraries compute it |

The lecture focuses on **Recall@K** and **MRR**.

**Worked example (from the lecture, 4 queries, correct chunk ranks shown):**

| Query | Rank of correct chunk | In top 5? | Reciprocal rank |
|-------|----------------------|-----------|-----------------|
| Money back | 1 | Yes (1) | 1.00 |
| GSTIN invalid | 3 | Yes (1) | 0.33 |
| KYC documents | 7 | No (0) | 0.14 |
| Refund kabayega | 2 | Yes (1) | 0.50 |

- **Recall@5** = 3 / 4 = **0.75**
- **MRR** = (1 + 0.33 + 0.14 + 0.50) / 4 = **0.49**
- Precision@5 example from the lecture: 2 correct out of 5 shown gives 2/5 = **0.4**.

### Caution: two different "recalls"

- **Retrieval recall@K** asks whether the correct answer was found.
- **ANN recall** (Part 3) asks whether an approximate index found the same neighbours that exact search would have found. Typical ANN recall is 95 to 99 percent. Do not confuse the two.

---

## Part 3: Lexical search (classical keyword search)

Lexical search checks which words of the query appear in the document. It is about 30 years old and still valid. Its advantages are that it is fast, explainable and needs no ML model. Its main weakness is that it misses synonyms.

### Text preprocessing

Apply the same steps to documents and queries:

1. **Lowercase** the text.
2. **Tokenise**: split on delimiters into tokens.
3. **Remove stop words** (words such as "the", "is", "in") that carry little meaning.
4. **Stem** each token to a root form (for example "refunds" to "refund").

Stop-word lists and stemmers are English-only. They do not work well for Hinglish or transliterated Indian languages (see the Indian-context section below).

### Inverted index

A normal index goes from document to words. An **inverted index** goes from **word to the list of documents** containing it, like a textbook index. Example from the lecture:

| Word | Documents |
|------|-----------|
| refund | D1, D3 |
| KYC | D2, D3 |
| wallet | D2 |
| delay | D1 |

This is the most important data structure in keyword search. Looking up query words gives candidate documents directly.

### Term frequency (TF)

TF counts how many times a query term appears in a document. A document that mentions "refund" five times ranks above one that mentions it once.

**Problem:** common words ("order", "account") appear in almost every document and add noise.

### Inverse document frequency (IDF)

IDF gives rare words more weight:

```
IDF(word) = log(N / n)
```

- N = total number of documents
- n = number of documents that contain the word

Lecture examples (natural log):

- A word in 40,000 of 50,000 documents: log(50,000 / 40,000) = log(1.25) ≈ **0.22**. Low information.
- GSTIN in 500 of 50,000 documents: log(50,000 / 500) = log(100) ≈ **4.6**. High information.

The logarithm stops rare words from dominating too strongly.

### TF-IDF

TF-IDF = TF × IDF. It scores terms that are frequent in this document but rare in the corpus.

**Two flaws of plain TF-IDF:**

1. **No saturation.** Score grows linearly with term frequency. A page that repeats "refund" 50 times is probably spam but gets 50 times the score of a single mention.
2. **Length bias.** A long document contains more words and repeats more by chance, so it beats a short FAQ that answers the question directly.

### BM25 (Best Match 25)

BM25 fixes both flaws with two tuning parameters. The lecturer described the components; the standard form is:

```
score(D, Q) = Σ IDF(q) × [ f(q, D) × (k1 + 1) ] / [ f(q, D) + k1 × (1 - b + b × |D| / avgdl) ]
```

| Symbol | Meaning | Typical value |
|--------|---------|---------------|
| `f(q, D)` | Term frequency of query term q in document D | Counted |
| `k1` | **Saturation knob**: how fast the TF contribution flattens | 1.2 to 2.0 (default 1.2) |
| `b` | **Length normalisation**: 0 ignores length, 1 fully normalises | 0.75 |
| `\|D\|` / `avgdl` | Document length relative to the average | Computed |

**Saturation.** The TF contribution rises for the first few mentions and then levels off. With `k1 = 1.2` it approaches `k1 + 1 = 2.2`. Repeated spam stops helping.

**Length.** A document longer than average is penalised, so a short direct answer can win.

**Practice:** the defaults `k1 = 1.2` and `b = 0.75` are almost never changed. Know what they do so you can tune them for unusual documents.

**Note on IDF:** the lecture uses `log(N / n)`. Production libraries use a smoothed variant of the same idea.

### Worked BM25 example (lecture)

Query: "refund delay". Three documents, default parameters.

| Doc | Content | Matches | BM25 |
|-----|---------|---------|------|
| D1 | "refund process takes seven days" | refund (2 times) | ≈ 0.61 |
| D2 | "KYC needs PAN and other documents" | none | 0.00 |
| D3 | "refund delayed due to KYC pending" | refund and delay (1 each) | ≈ 1.45 |

Lesson: D3 wins because it matches **two different query words**, one of them rare ("delay"). Matching several distinct rare terms beats repeating one common term.

### Lab 1: BM25 on the 8-FAQ knowledge base

The lab ran three queries against eight FAQ sentences:

| Query | Top result | BM25 score | Note |
|-------|-----------|-----------|------|
| "refund delay KYC" | Refund is delayed if KYC verification is pending | 1.88 | Correct |
| "GSTIN error" | Invalid GSTIN error. Check the 15-character format | 3.17 | Exact identifier match; higher score because GSTIN is a rare term |
| "how do I get my money back" | Reset your password from the login page | **0.00** | No word overlap, so the top result is meaningless |

**Lesson:** an argmax always returns something. The fix is a **score threshold**: below it, return "Sorry, I could not find this." The lecturer used 0.5 for illustration only. BM25 scores are **not on a fixed scale** (they depend on query length and corpus), so any threshold must be calibrated on your own golden set.

### Where BM25 is strong

- **Exact identifiers**: GSTIN, PAN, order ID, account numbers.
- **Rare jargon**: product names, legal clause numbers such as "Section 80C", drug names.
- **No training needed**: works on day one.
- **Explainable**: you can show exactly which words matched.

### Where BM25 fails

- **Vocabulary mismatch**: "money back" does not match "refund".
- **Paraphrase**: "can't log in" versus "authentication failure".
- **Cross-language**: a Hindi query does not match an English document.
- **Negation and near-synonyms**: "eligible" and "not eligible" share most words.

### Indian-context challenges

- **Code-mixing**: Hindi and English in one sentence.
- **Transliteration**: Hindi or Bengali written in Roman script, with several spellings of one word (the lecturer's example: three spellings of Aadhaar).
- **Multiple scripts**: Devanagari, Bengali, Tamil and others.
- **English stop words and stemmers** break on all of the above.

**Conclusion:** for Indian users, pure keyword search is fragile. Plan for **multilingual retrieval from day one**.

---

## Part 4: Semantic search (embeddings)

Semantic search matches **meaning**. The query "money back" should retrieve a refund policy even with no shared words.

### What an embedding is

An **embedding** is a fixed-length list of numbers (a vector) produced by a neural network, the **embedding model**, that captures the meaning of a piece of text. Typical lengths are 384, 768, 1024, 1536 or 3072 numbers. The length is the **dimension**.

**GPS analogy (from the lecture):** Kharagpur and Midnapore are close because their GPS coordinates are close. Kharagpur and Bangalore are far apart. Embeddings are coordinates in a high-dimensional "meaning space".

Important caveats:

- **An individual number has no human meaning.** Only the overall **direction** of the vector matters.
- The lecturer's 2-D picture is for intuition only. Real embeddings have hundreds of dimensions, and visualisations such as t-SNE distort distances.
- Similar texts form **clusters**: "return payment", "money back" and "refund policy" sit together; "KYC", "PAN card" and "verify" sit together; "reset password" and "login failed" sit together.

### Contrastive learning (how the model learns)

Embedding models are typically trained with **contrastive learning**:

1. Collect millions of **positive pairs** of text that belong together: a question and its answer, a title and its article, a search query and the page that was clicked, a sentence and its translation.
2. Encode both sides with the network.
3. Adjust the weights so **positive pairs move closer** (pull together) and **negative pairs move apart** (push apart).

**Consequences the lecturer draws:**

- A model trained mostly on English pairs is weak on other languages.
- A model trained on web data may not know your internal product vocabulary.
- A model trained with translation pairs can match a Hindi query to an English document.

So check what a model was trained on before you rely on it.

### Similarity measures

| Measure | What it uses | Notes |
|---------|--------------|-------|
| **Cosine similarity** | The **angle** between vectors: `cos θ = (a · b) / (‖a‖ ‖b‖)` | 1 means same direction; 0 means orthogonal (unrelated). Ignores length |
| **Dot product** | Multiplies matching numbers and sums them; depends on **angle and length** | Cheapest to compute |
| **Euclidean (L2) distance** | Straight-line distance; smaller means more similar | Standard in many indexes |

**Normalisation trick:** if every vector is scaled to length 1, all three give the **same ranking**. Cosine equals the dot product, and Euclidean distance is a simple function of cosine. So you can normalise and then use the dot product, which is cheapest.

- OpenAI embeddings come already normalised to length 1.
- For Sentence Transformers, pass `normalize_embeddings=True`.
- **Rule of thumb:** use the metric the model card recommends, and use the **same metric** in your vector index. A mismatch silently hurts quality.

**Scores are model-specific.** A cosine of 0.8 may mean "very similar" for one model, while unrelated text scores 0.7 with another. Never hard-code a threshold without testing it on your golden set for that model. Perfect matches are rare; even "cancel an order" and "money back" will not score exactly 1.

### Bi-encoder (the retrieval architecture)

```
Offline:  every chunk  ──encoder──>  vector  ──store──>  index
Online:   query        ──encoder──>  vector  ──nearest neighbours──>  top-K
```

- Query and documents are encoded **separately** by the same encoder.
- Document vectors are **precomputed**, so query-time cost does not depend on document length.
- This scales to millions of documents. The price is precision, because query and document never interact directly.
- **The query must use the exact same model and version** as the documents. If you upgrade the model, you must **re-embed the whole corpus**.

### Lab 2: semantic search with MiniLM

- Model: `all-MiniLM-L6-v2`, **384 dimensions**, about 90 MB, runs on CPU.
- Steps: encode the 8 FAQs; encode each query; `normalize_embeddings=True`; cosine similarity; take top 2.

Observations from the lab:

| Query | Result | What it shows |
|-------|--------|---------------|
| "how do I get my money back" | "Refunds are processed within 7 working days" first | Meaning match with no shared words, which BM25 could not do |
| "GSTIN error" | "Invalid GSTIN error" scores 0.84 and the second result 0.26 | Large score gap = high confidence |
| "refund delay KYC" | Top two results score 0.84 and 0.54 (the lecturer called these close) | Smaller gap = the ranking is less certain |

**Hinglish test.** The query "mirror refund kabayega" returns a relevant but not best answer with this English model. Switching to a **multilingual** model (the lecturer used a small multilingual Sentence Transformer on CPU, and recommended a larger one on a GPU) gives better answers for Hindi in Devanagari and Bengali typed in Roman script.

**Lesson:** the English-only model handles English well. Multilingual queries need a multilingual model, and this must be tested on real user input.

### Failure cases of semantic search

| Weakness | Example |
|----------|---------|
| **Exact codes** | GSTIN numbers that differ by one character look almost identical in embedding space |
| **Negation** | "Refund allowed" and "refund not allowed" are close |
| **New jargon** | An internal product name such as "SuperCoin" that the model has never seen |
| **Always returns K** | Nearest-neighbour search returns K results even when none is relevant, so you need a threshold or a re-ranker |

**Recap question from the lecture:** a user searches "order 1843 not delivered". Which method reliably finds the ticket with that exact order ID? **BM25**, because it matches the identifier word for word.

---

## Part 5: Chunking

### Why chunk

1. **Length limit.** Models accept a maximum input (512 tokens for many open models; about 8,000 for OpenAI models, as stated in the lecture).
2. **Blurred meaning.** One vector for a 40-page PDF averages many topics into a single blurry point.
3. **Precision.** The user and the LLM need the exact paragraph.

### Size and overlap

- **Typical starting size:** 200 to 500 tokens per chunk.
- **Too small:** context is lost. "It takes seven days" means nothing without "refund".
- **Too large:** topics mix and the vector becomes blurry.
- **Overlap:** repeat about 10 to 20 percent between neighbouring chunks, so a sentence at a boundary appears complete in at least one chunk.
- **Respect structure** where you can: split at headings, FAQ boundaries or table rows. Prepend the document title to each chunk so it knows it belongs to "Refund Policy".

Chunking is a topic of its own. The next lecture covers it in depth with RAG.

---

## Part 6: Vector indexes and storage

### Exact versus approximate search

- **Exact (brute force)** compares the query with every vector. It is 100 percent accurate, fine up to about 100K vectors, and very slow above about 10 million.
- **Approximate nearest neighbour (ANN)** checks only a small fraction of vectors. It may occasionally miss a true neighbour, but it answers in milliseconds at millions of vectors, at the cost of memory and tuning. Typical ANN recall is 95 to 99 percent.

### HNSW (Hierarchical Navigable Small World)

HNSW is the most popular ANN index. It builds a **multi-layer graph**:

- The **top layer** has few points with long-distance links, like a national highway.
- **Lower layers** have more points and shorter links, like state roads.
- The **bottom layer** contains every point, like city streets.

A search starts at the top, greedily moves towards the query, drops a layer, and repeats. It visits only a few hundred points out of a million.

| Knob | Meaning | Effect |
|------|---------|--------|
| **M** | Number of links per point | More links = better recall, more memory |
| **efSearch** | Candidates explored during search | Higher = better recall, slower |

**Cost:** the graph lives in memory, so RAM grows with the number and dimension of vectors.

### pgvector in PostgreSQL

pgvector is the lecture's default starting point for vector search:

```sql
CREATE EXTENSION vector;
ALTER TABLE chunks ADD COLUMN embedding vector(384);   -- must match the model's dimension
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
-- query: ORDER BY embedding <=> $1 LIMIT 50    (<=> is pgvector's cosine distance operator)
```

- The vectors sit **next to relational data**, so you get transactions, joins, backups and access control in one place.
- You can filter by customer ID, language or date in the same query.
- Good for up to a few million vectors.

**Practical limits:**

- The `vector` type supports HNSW indexing up to **2,000 dimensions**. OpenAI's 3072-dimension model cannot be indexed directly.
- The `halfvec` type (half precision) raises the limit to about **4,000 dimensions**.
- Or reduce the dimension (Part 9).

### Other options

| Option | Notes |
|--------|-------|
| **pgvector** | Default. Keeps vectors with relational data |
| **Qdrant, Weaviate, Milvus** | Dedicated vector databases for hundreds of millions of vectors, advanced filtering and horizontal scaling. Open source and self-hostable |
| **Pinecone and cloud vector features** | Managed. Removes operations work, but the vendor holds the bill and your data leaves your infrastructure |
| **FAISS** (the transcript says "phases") | A library, not a database. Good for experiments and offline jobs; you handle persistence and updates |

**Rule of thumb:** start with pgvector and move only when measurements show you need to.

---

## Part 7: Hybrid search

### Why combine

| Query type | BM25 | Semantic |
|-----------|------|----------|
| "money back" (synonym) | Fails | Wins |
| Order ID or GSTIN (exact identifier) | Wins | Weak |
| Rare section or clause number | Wins | Can fail |
| "Why am I charged twice?" (natural question) | OK | Better |
| Mixed Hinglish | Unreliable | Depends on model |

Modern systems combine both, taking the best of the lexical and semantic worlds.

### Hybrid architecture

```
             ┌── BM25 ───────────> top 50 (keyword) ──┐
query ──────┤                                          ├── fuse ── re-rank ── top 5-10
             └── vector search ──> top 50 (meaning) ──┘
```

- Both retrievers run **in parallel**, so latency is set by the slower one.
- Each returns **top 50**, not top 10. At this stage we want **high recall** and do not want to lose anything.
- Fusion and re-ranking then choose the final top 5 to 10.

### The fusion problem: scores are not comparable

| Retriever | Score range | Depends on |
|-----------|-------------|-----------|
| BM25 | Unbounded (0 to 25 or more) | Query length and corpus |
| Cosine similarity | Compressed (roughly 0.2 to 0.9) | The embedding model |

If you add raw scores, BM25 dominates because its numbers are bigger.

### Option 1: weighted min-max fusion

1. Normalise each list to 0 to 1 with **min-max**: `(x − min) / (max − min)`.
2. Combine with a weight, typically **alpha = 0.7** on the semantic score.
3. **Tune alpha** by choosing the value that maximises **recall@K on your golden set**.

**Weakness:** min-max is sensitive to **outliers**. One very high BM25 score squashes all the others towards 0.

**Correction:** the lecturer said "subtract the mean" when describing this step. Min-max subtracts the **minimum**, not the mean.

### Option 2: Reciprocal Rank Fusion (RRF)

RRF **ignores scores and uses only ranks**:

```
RRF(d) = Σ over each list containing d:   1 / (k + rank(d))      with k = 60
```

- `k = 60` comes from the original 2009 paper by Cormack and colleagues.
- A document ranked high in **both** lists gets two good contributions. A document ranked high in only one list gets one.
- It rewards **agreement** between the two retrievers.

**Worked example (from the lecture):**

| Document | BM25 rank | Vector rank | RRF score |
|----------|-----------|-------------|-----------|
| A | 1 | 3 | 1/61 + 1/63 ≈ **0.0323** |
| B | 4 | 1 | 1/64 + 1/61 ≈ **0.0320** |
| C | 2 | not in top list | 1/62 ≈ **0.0161** |
| D | not in top list | 2 | 1/62 ≈ **0.0161** |

A, ranked well by both retrievers, comes first.

### Lab 3: hybrid search with RRF

- Combines the BM25 ranks from Lab 1 with the vector ranks from Lab 2.
- "GSTIN error" returns "Invalid GSTIN error" at the top (BM25 contributes the exact match).
- "How do I get my money back" returns "Refunds are processed within 7 working days" at the top. The lecturer said the fused results were better than either retriever alone when he compared them. This is an observation from one small run, so confirm it on your own golden set.

### Hybrid search in PostgreSQL

The lecturer showed RRF in one SQL query: take the rank from each retriever, use `COALESCE` so a missing rank contributes **0**, add the two RRF terms, and `ORDER BY` the total. The spoken form was garbled, so the exact SQL is not reproduced here.

### Practical tips

1. Start with **RRF with k = 60**, and take the **top 50 per retriever**.
2. **Apply filters first** (for example customer ID, language, date) in both retrievers.
3. Choose the embedding model for your language and data.
4. Only tune weights later, once you have a golden set.
5. **Measure** BM25, vector and hybrid on the golden set and compare them.

---

## Part 8: Re-ranking

### The retrieval funnel

```
Whole corpus (e.g. 500K chunks)
    │  Stage 1: hybrid retrieval (about 20 ms), optimised for RECALL
    ▼
~50 to 100 candidates
    │  Stage 2: re-ranker (cross-encoder), optimised for PRECISION
    ▼
Top 3 to 5 chunks  ──>  LLM
```

- Stage 1 must make sure the right answer is **somewhere** in the candidate set.
- Stage 2 looks deeply at a few candidates. Running an expensive model on the whole corpus would be far too slow.
- This funnel gives the accuracy of the expensive model at the cost of the cheap one.

### Bi-encoder versus cross-encoder

| | Bi-encoder (retriever) | Cross-encoder (re-ranker) |
|--|------------------------|---------------------------|
| Input | Query and document **encoded separately** | Query and document **read together** in one pass |
| Interaction | None at the word level | Word-level interaction between query and document |
| Speed | Fast; document vectors precomputed | Slow; one pass per query-document pair |
| Accuracy | Lower | Higher; gives a relevance score |
| Role | Retrieval over the full corpus | Re-ordering a short list |

### Re-ranker options

| Option | Type | Notes |
|--------|------|-------|
| **Cohere Rerank** (version garbled; likely 3.5) | API | Easy to implement. Supports 100+ languages including Indian languages. Priced per search. Data leaves your domain |
| **BGE reranker (multilingual)** | Open source, self-hosted on GPU | Good for Indian languages; data stays in-house |
| **MS MARCO MiniLM cross-encoder** | Open source, English | Tiny and fast, runs on CPU. Used in Lab 4 |
| **LLM as re-ranker** | Prompted model | Most flexible (describe relevance in natural language). Slowest and most expensive per query |

### Lab 4: cross-encoder re-ranking

- Model: MS MARCO MiniLM cross-encoder.
- Query: "refund not allowed after shipping".
- Four candidates from the hybrid search.
- Result: "Cancel an order before it is shipped for full refund" ranks first, which is the right answer, with **clearly separated** scores.
- The bi-encoder ordering of the same four candidates looked similar, with scores close together. The cross-encoder's scores were more spread out, so it was more confident.

### Costs and when to skip re-ranking

- Re-ranking adds about **100 to 300 ms** for 50 to 100 pairs (lecturer's figure). You can reduce the number of pairs, but there is always some latency.
- Self-hosting keeps data in-house but needs GPU capacity. An LLM-based re-ranker sends data to a provider.
- **Skip it** when the corpus is tiny, when hybrid results are already good, or when the latency budget is strict.

### Threshold the re-ranker score

If the best re-ranker score is below a threshold, nothing in the corpus answers the query well. Return "I could not find this" or escalate to a human instead of forcing an answer.

---

## Part 9: Choosing an embedding model

### Six selection factors

1. **Quality on your data.** Test on your language mix: English only, Hindi, Bengali, or Hinglish.
2. **Maximum input length.** 512 tokens versus about 8,000 tokens per chunk.
3. **Dimension.** From 384 to 3072. Trades storage, RAM and speed against quality.
4. **Cost model.** Per-token API price versus the GPU and operations cost of self-hosting.
5. **Data residency.** An API sends data outside your domain (a DPDP concern). Self-hosting keeps data in-house.
6. **Latency budget.** Chat tolerates 1 to 2 seconds. Instant search may need under 100 ms.

### The MTEB leaderboard (use with care)

The **Massive Text Embedding Benchmark** on Hugging Face averages many tasks: classification, clustering, pair classification, retrieval and more. A model can rank high on average and still be mediocre at **retrieval**.

**Method:** use MTEB's **retrieval column** to shortlist three models, then choose the final model with your **golden set**.

### OpenAI embedding models

| Model | Notes |
|-------|-------|
| `text-embedding-3-small` | Default dimension 1536; cheapest; good for scale or tight budgets |
| `text-embedding-3-large` | Default dimension 3072; better quality; higher price |
| `text-embedding-ada-002` | Legacy; generally avoid |

The lecturer's prices are "2026 prices" but were read out with garbled conversions. Check current pricing before you budget.

**Code pattern from the lecture:**

```python
from openai import OpenAI
client = OpenAI()                                   # reads OPENAI_API_KEY from the environment
resp = client.embeddings.create(model="text-embedding-3-small", input=["refund policy", "KYC documents"])
vectors = [d.embedding for d in resp.data]          # same order as the input
tokens = resp.usage.total_tokens                    # log this for cost tracking, as in Lecture 05
```

**Production tips:**

- **Batch** many texts per call (up to about 2,000 inputs, within the per-request token limit), instead of one call per chunk.
- Wrap calls with **timeouts, retries and a circuit breaker** for HTTP 429 (rate limit) and other errors.

### Sentence Transformers (open source, self-hosted)

- Choose from English-only models (fast) and multilingual models (larger, better for Indian languages). The lecturer's multilingual example set `device="cuda"`, because large multilingual models need a GPU.
- Pass `normalize_embeddings=True`.
- Accepts queries in different languages and scripts (for example Devanagari).

**Trade-off:**

| Advantages | Costs |
|-----------|-------|
| Data never leaves your server (DPDP-friendly) | GPU server and MLOps effort |
| No per-token price and no rate limits | You own scaling, uptime and security |
| Fine-tunable on your domain | Large models are heavy to run |
| No vendor lock-in or model retirement | Keeping up with model updates is your job |

### Cohere multilingual embeddings

Known for strong multilingual retrieval. The query can be sent in Devanagari, so it does not need to be in Latin script. Test with native Hindi, Hinglish, code-mixed Bengali, and real user input.

### Cost in context

The lecturer's worked example: a knowledge base of about 400-token chunks, 1,00,000 queries per day with about 20 tokens each.

- Monthly **query-embedding** cost was about **INR 114** with the small model and about **INR 741** with the large model (figures as read in class; the transcript is partly garbled).
- Indexing cost is a one-off cost and was quoted as small (about INR 38 for the embedding API in the example).
- The lecturer's point: **the embedding API cost is tiny**. Storage, RAM and **re-indexing** dominate.

---

## Part 10: Dimensions, storage and quantisation

### Storage formula

```
storage bytes = number of chunks × dimension × bytes per number
```

For float32 (4 bytes per number):

| Chunks | Dimension | Storage |
|--------|-----------|---------|
| 1,000,000 | 384 | 1.536 GB (about 1.5 GB) |
| 1,000,000 | 1536 | about 6.1 GB |
| 1,000,000 | 3072 | about 12.3 GB |

The lecturer's "37 two" is read as **3072** because the storage figure he gave (12.3 GB) matches 3072 dimensions.

Dimension also drives **RAM** (HNSW lives in memory), **query latency** (more multiplications per comparison) and **index build time**.

### Matryoshka embeddings

Matryoshka embeddings (used by OpenAI's text-embedding-3 models) are trained so that the **first k numbers** form a usable smaller embedding. You can keep, for example, the first 256 or 512 dimensions.

**Lab 5 results** (the lecturer's golden set, MRR):

| Dimension | Bytes per vector (float32) | MRR |
|-----------|----------------------------|-----|
| 1536 | 6144 | 1.00 |
| 512 | 2048 | 1.00 |
| 128 | 512 | 0.89 |
| very small (4) | 16 | close to random |

Lesson: 512 dimensions gave the same MRR at about one third of the storage.

**Note on the dimensions:** the spoken list of very small dimensions was garbled. The MRR values above are the ones stated in the lecture.

### Quantisation

Reducing the number of **bits per dimension** also cuts storage. Quality figures from the lecturer's slide (as a percentage of the float32 baseline):

| Data type | Quality retained |
|-----------|------------------|
| float32 | 100% |
| int8 | about 97 to 99% |
| binary | about 90 to 96% |

### Rules of thumb for dimension and data type

| Corpus size | Suggested dimension | Data type | Why |
|-------------|--------------------|-----------|-----|
| Under 100K chunks | Full (for example 1536 or 3072) | Full precision | Storage is trivial, so maximise quality |
| 100K to 10M | 512 to 1024 | float16 | Fits in RAM on one server |
| Over 10M | 256 to 512 | int8 or binary | Memory dominates cost |
| Edge or mobile devices | 128 to 384 | Reduced | Memory and CPU bound |

---

## Part 11: Decision framework and model migration

### Decision flow from the lecture

1. **Must the data stay on your servers?** Yes: self-host, for example a multilingual BGE-M3-style model.
2. **Do you need Indian languages or mixed-script queries?** Yes: use a **multilingual** model.
3. **Do you need huge scale or a very tight budget?** Yes: use OpenAI `text-embedding-3-small` with a lower dimension.
4. **Otherwise:** the default is OpenAI `text-embedding-3-large` at **1024 dimensions**.

Always confirm the choice with your golden set.

### Worked scenarios (from the lecture)

| Scenario | Suggested approach |
|----------|--------------------|
| English SaaS help centre, about 5K documents | Hybrid retrieval with RRF; OpenAI small or a Sentence Transformers model |
| E-commerce, 50 million products in 12 languages | Hybrid with a multilingual vector model (for example Cohere multilingual) |
| 30 million Hindi and English chunks, cloud vendor | Multilingual Matryoshka model at **512 dimensions**, with hybrid search |

### Migrating to a new model

- **Tag every vector** with the model name and version.
- **Never mix** vectors from two models in one index. They are not comparable.
- To upgrade, **re-embed in the background**, then switch over. This lets you start with a smaller model and move up later.

---

## Part 12: Privacy note (DPDP and vectors)

- **Vectors are not privacy-preserving.** Research has shown that original text can be recovered from embeddings. Treat vectors like the text they come from.
- Do not reason that "I only send the embedding, so it is safe" to a public model.
- Mask PII (phone numbers, PAN, Aadhaar) before embedding, and keep embedding providers within the DPDP obligations.
- A managed cloud vector store moves your data outside your infrastructure. Check that against DPDP.

---

## Key takeaways

1. **Retrieval sets the ceiling.** If the right chunk is not retrieved, no LLM can fix it. Improve retrieval before buying a bigger model.
2. **BM25 is a strong, cheap baseline.** It wins on IDs, rare terms and exact matches, and needs no training.
3. **Embeddings win on meaning.** They handle synonyms and paraphrase, but miss exact codes and negation.
4. **Hybrid search is the default.** Run BM25 and vector search in parallel, fuse with **RRF (k = 60)**, and refine with a re-ranker.
5. **Re-ranking adds precision at a latency cost.** Use a cross-encoder on the top 50 to 100 candidates, and threshold its score.
6. **Measure everything on a golden set** of real queries, including mixed-language and ID-based queries. Track **recall@K** and **MRR**.
7. **Use the same model for documents and queries.** Tag vectors with the model version, and plan re-embedding for upgrades.
8. **Choose dimensions by corpus size.** Matryoshka cuts storage with little loss. Vectors are personal data for DPDP purposes.
