# Lecture 01: Important Exam Q&A

Practice questions aligned with lecture emphasis and the in-class quizzes. Answers are concise for revision.

---

## Foundations and evaluation

### Q1. Why does retrieval quality set the ceiling for an LLM application?

**A.** The LLM only knows what is in its context. If the right chunk is not retrieved, the model cannot use it, and if a wrong chunk is retrieved, the model writes a confident wrong answer (hallucination). Better retrieval and context often gives a bigger quality gain than a more expensive model.

### Q2. Why is "more context" not the fix for poor answers?

**A.** More context raises token cost and latency, and models can miss facts buried in the middle of a long context. Retrieve the top few relevant chunks instead. This pattern is RAG.

### Q3. Define corpus, chunk, query and top-K.

**A.** The **corpus** is the full collection of chunks. A **chunk** is one unit that can be returned. A **query** is what the user types, usually short. **Top-K** means returning only the best K results, usually 5 or 10.

### Q4. What is the difference between the offline and online phases of a search system?

**A.** **Offline:** ingest, clean, chunk, embed and build the index. This happens once or when documents change, and can be slow. **Online:** embed the query, compare it with the index, score, rank and return the top K. This must be fast, because it runs on every query.

### Q5. Why must documents and queries be processed the same way?

**A.** Scores are only comparable when both sides use the same process. Embedding documents with one model and queries with another gives meaningless similarity. For BM25, the same tokenisation and stemming must apply to both.

### Q6. Define precision@K and recall@K. Which matters more for RAG, and why?

**A.** **Precision@K** is the fraction of the top K results that are correct. **Recall@K** is the fraction of all correct chunks found in the top K. Recall@K matters more for RAG, because a relevant chunk outside the top K never reaches the LLM.

### Q7. Compute recall@5 and MRR for these queries: correct chunk at rank 1, rank 3, rank 7 and rank 2.

**A.** Recall@5 counts how many queries have their correct chunk in the top 5: ranks 1, 3 and 2 are in, rank 7 is out, so recall@5 = 3/4 = **0.75**. The reciprocal ranks are 1, 1/3, 1/7 and 1/2. MRR = (1 + 0.33 + 0.14 + 0.50) / 4 ≈ **0.49**.

### Q8. When would you use NDCG instead of MRR or recall?

**A.** NDCG rewards correct results near the top and supports **graded relevance** (very relevant versus somewhat relevant). Use it when relevance is not just yes or no.

### Q9. Why is a golden set needed, and how is it built?

**A.** Classical tests check exact outputs. Retrieval output depends on context and user phrasing, so you need real queries, each marked with the chunks that are correct. Running a few test queries by hand does not show how a model behaves across real traffic. Include mixed-language and ID-based queries.

---

## Lexical search

### Q10. What is an inverted index?

**A.** A map from each **word** to the list of **documents** containing it, like a book index. It lets you find candidate documents for a query without scanning every document.

### Q11. Explain TF, IDF and TF-IDF.

**A.** **TF** counts how often a query term appears in a document. **IDF** = log(N / n), where N is the number of documents and n is the number containing the term, so rare words weigh more. **TF-IDF** multiplies them: frequent in this document but rare in the corpus scores highest.

### Q12. What two problems does BM25 fix in TF-IDF?

**A.** **Term-frequency saturation:** the score flattens after a few mentions, so keyword spam stops helping. **Length normalisation:** long documents are penalised so they do not win by chance.

### Q13. What do k1 and b control in BM25?

**A.** **k1** (typically 1.2 to 2.0) controls how quickly term-frequency contribution saturates. **b** (typically 0.75) controls how strongly length is penalised: 0 ignores length, 1 fully normalises it. The defaults are rarely changed.

### Q14. In the BM25 worked example, why does D3 beat D1 for the query "refund delay"?

**A.** D3 matches **two different query terms**, including the rare term "delay", and BM25 rewards distinct rare matches more than repeating one common word. D1 matches only "refund", twice.

### Q15. Why did the BM25 lab return a non-answer for "how do I get my money back"?

**A.** The query shares no words with any FAQ, so every score is 0. An argmax still returns the first document. The fix is a **score threshold**, calibrated on your golden set, below which the system says it could not find an answer.

### Q16. Where does BM25 fail, and where does it win?

**A.** It **fails** on synonyms ("money back" versus "refund"), paraphrase, cross-language queries and negation. It **wins** on exact identifiers (GSTIN, PAN, order ID), rare jargon and clause numbers, works without training, and is explainable.

### Q17. What makes keyword search fragile for Indian users?

**A.** Code-mixing (Hindi and English in one sentence), transliteration with several spellings of one word, multiple scripts (Devanagari, Bengali, Tamil), and English-only stop-word lists and stemmers that do not handle them.

---

## Semantic search and embeddings

### Q18. What is an embedding, and what is the dimension?

**A.** An embedding is a fixed-length vector of numbers produced by a neural network (the embedding model) that captures the meaning of a text. The **dimension** is the length of that vector (for example 384 or 1536).

### Q19. How does contrastive learning train an embedding model?

**A.** It uses positive pairs of texts that belong together (question and answer, title and article, query and clicked page, sentence and translation). The network pulls positive pairs together in the vector space and pushes negatives apart.

### Q20. Why does the training data matter for an embedding model?

**A.** A model trained mostly on English will be weak on other languages. A model trained on web data may not know internal product vocabulary. A model trained on translation pairs can match a Hindi query to an English document.

### Q21. Compare cosine similarity, dot product and Euclidean distance.

**A.** **Cosine** uses only the angle between vectors. **Dot product** uses angle and magnitude and is the cheapest to compute. **Euclidean (L2)** uses the straight-line distance, where smaller means more similar. When every vector is normalised to length 1, all three give the same ranking.

### Q22. Why should you not hard-code a cosine threshold such as 0.8?

**A.** Scores depend on the model. For one model 0.8 may mean very similar, while unrelated text scores around 0.7 with another. Find the threshold on your own golden set for that specific model.

### Q23. Explain the bi-encoder architecture and its trade-off.

**A.** Query and documents are encoded separately by the same encoder. Document vectors are precomputed offline, so query-time cost does not depend on document length, and the design scales to millions of documents. The trade-off is lower precision, because query and document never interact directly.

### Q24. What is the "same model" rule, and what happens when you upgrade a model?

**A.** Query and document vectors must come from the same model and version. After an upgrade you must **re-embed the whole corpus**. Tag every vector with the model name and version, and never mix vectors from two models in one index.

### Q25. What are the semantic search failure cases?

**A.** Exact codes (GSTIN or order IDs split into meaningless sub-pieces), negation ("refund allowed" versus "refund not allowed"), new internal jargon the model has not seen, and always returning K results even when nothing is relevant.

---

## Chunking, indexing and storage

### Q26. Why is chunking needed, and what size and overlap should you start with?

**A.** Models have maximum input lengths, and one vector for a long document blurs many topics into one point. Users need the exact paragraph. Start with about **200 to 500 tokens** per chunk and about **10 to 20 percent overlap** so boundary sentences appear whole in at least one chunk. Prefer splitting on headings and FAQ boundaries, and prepend the document title.

### Q27. What is ANN, and what is the trade-off?

**A.** Approximate nearest-neighbour search checks only a small fraction of vectors instead of all of them. It answers in milliseconds at millions of vectors, at the cost of occasionally missing a true neighbour (typical ANN recall 95 to 99 percent), plus memory and tuning.

### Q28. What is HNSW, and what do M and efSearch control?

**A.** HNSW (Hierarchical Navigable Small World) is a multi-layer graph index. The top layer has long-range links and the bottom layer has every point, so search descends layer by layer and visits only a few hundred points. **M** is the number of links per point (more means better recall and more memory). **efSearch** is the number of candidates explored (more means better recall and slower queries).

### Q29. Why does vector dimension affect more than storage?

**A.** Storage is `chunks × dimension × bytes per number`. HNSW lives in memory, so RAM grows with dimension. Each comparison costs more multiplications, so latency rises, and index builds slow down. pgvector's HNSW index also has a dimension limit (2,000 for `vector`, about 4,000 for `halfvec`).

### Q30. Why start with pgvector?

**A.** It keeps vectors next to relational data, so you get transactions, joins, backups and access control in one place, and you can filter on metadata in the same query. It is good for up to a few million vectors. Move to a dedicated vector database only when measurements show a need.

---

## Hybrid search and re-ranking

### Q31. Why run BM25 and vector search in parallel and take the top 50 from each?

**A.** The two retrievers are independent, so running them in parallel makes latency that of the slower one. Taking 50 from each keeps **recall** high, so the fusion and re-ranking steps can choose the final top 5 to 10 from a wide set.

### Q32. Why can't you add BM25 and cosine scores directly?

**A.** BM25 is unbounded (roughly 0 to 25 or more) and depends on query length and corpus, while cosine sits in a narrow band (roughly 0.2 to 0.9) and depends on the model. Raw addition lets BM25 dominate.

### Q33. What is weighted min-max fusion, and what is its weakness?

**A.** Each list is normalised to 0 to 1 with min-max, then combined with a weight such as alpha = 0.7 on the semantic score. Tune alpha by maximising recall@K on the golden set. Weakness: min-max is sensitive to outliers, because one very high BM25 score squashes the rest towards 0.

### Q34. How does Reciprocal Rank Fusion work?

**A.** RRF ignores scores and uses ranks only: for each document, sum `1 / (k + rank)` across each list it appears in, with `k = 60`. A document ranked well in both lists gets two good contributions, so RRF rewards agreement between retrievers.

### Q35. Compute the RRF score for a document ranked 1 in BM25 and 3 in vector search.

**A.** `1/(60+1) + 1/(60+3) = 1/61 + 1/63 ≈ 0.0164 + 0.0159 = 0.0323`.

### Q36. What are the two-stage retrieval funnel and the difference between a bi-encoder and a cross-encoder?

**A.** Stage 1 is hybrid retrieval over the full corpus, optimised for recall, bringing it to about 50 to 100 candidates. Stage 2 is a re-ranker, optimised for precision, that scores the candidates and keeps the top 3 to 5. A **bi-encoder** encodes query and document separately and can be precomputed, so it is fast and less precise. A **cross-encoder** reads query and document together in one pass, so it is more accurate and slow, which is why it runs only on the short list.

### Q37. Name the re-ranker options and their trade-offs.

**A.** **Cohere Rerank** is an API that supports many languages, priced per search, with data leaving your domain. **BGE reranker (multilingual)** is open source and self-hosted on a GPU, which keeps data in-house. **MS MARCO MiniLM** is a tiny English cross-encoder that runs on CPU. An **LLM as re-ranker** is the most flexible and the slowest and most expensive per query.

### Q38. When should you skip re-ranking?

**A.** When the corpus is tiny, when hybrid results are already good, or when the latency budget is strict. Re-ranking adds about 100 to 300 ms for 50 to 100 pairs in the lecturer's example.

### Q39. Why use a re-ranker score threshold?

**A.** If no candidate scores above the threshold, nothing in the corpus answers the query well. Returning "I could not find this" or escalating is better than forcing a weak answer into the LLM.

---

## Choosing a model and dimension

### Q40. What are the six factors for choosing an embedding model?

**A.** Quality on your own data and language mix, maximum input length, dimension, cost model (per-token API versus self-hosted GPU), data residency (DPDP), and latency budget.

### Q41. How should you use the MTEB leaderboard?

**A.** Use the **retrieval** column, not the overall average. A model can rank high on average through clustering and still be mediocre at retrieval. Use MTEB to shortlist about three models, then choose using your golden set.

### Q42. Why is the Matryoshka property useful?

**A.** The first k dimensions of a Matryoshka embedding form a usable smaller embedding, so you can truncate it (for example 1536 to 512) and save storage and memory with little quality loss. In the lecture's Lab 5, 512 dimensions kept MRR at 1.00 with about one third of the storage, while 128 dimensions dropped to 0.89.

### Q43. Calculate the storage for 1 million chunks at 384 dimensions in float32.

**A.** `1,000,000 × 384 × 4 bytes = 1.536 GB`, about 1.5 GB.

### Q44. What does quantisation do, and what is the quality cost?

**A.** It reduces bits per dimension, for example to int8 or binary, which cuts storage. The lecturer's figures put int8 at about 97 to 99 percent of baseline quality and binary at about 90 to 96 percent, so you choose the accuracy you can accept.

### Q45. What is the decision flow for picking a model in the lecture?

**A.** First, must the data stay on your servers? If yes, self-host (for example a multilingual BGE-M3-style model). Second, do you need Indian languages or mixed scripts? If yes, use a multilingual model. Third, do you need huge scale or a tight budget? If yes, use a small OpenAI model at a lower dimension. Otherwise, default to `text-embedding-3-large` at 1024 dimensions. Always confirm on the golden set.

### Q46. Why are embedding vectors personal data for DPDP purposes?

**A.** Vectors are not privacy-preserving. Research has shown that the original text can be recovered from embeddings, so a vector should be treated like the text it came from. Do not send vectors to a public model on the assumption that they are anonymous.

### Q47. What does "measure first" mean in the take-home problem?

**A.** Build a version-one search, then compare BM25, vector and hybrid retrieval on a golden set of about 30 queries, including Hinglish or Bengali queries and ID-based queries. Report recall@K, MRR, latency and price, then justify the model and dimension you choose.
