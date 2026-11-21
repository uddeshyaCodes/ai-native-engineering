# Lecture 01: In-Lecture Quizzes

Live polls ran through Mentimeter in several blocks, mostly after the semantic search and vector index parts. Stems follow the instructor's readout. The transcript is auto-captioned and some stems and options were lost, so items marked **reconstructed** are inferred from the lecture content around them.

---

## Quiz 1 - After semantic search (Lab 2)

### Q1. What does cosine similarity measure between two embedding vectors?

| | |
|---|---|
| **Correct ✓** | **The angle between the two vectors** (their direction, not their length) |

**Live note:** Most students answered correctly.

**Explanation:** Cosine similarity is 1 when the vectors point the same way and 0 when they are orthogonal (unrelated). It ignores magnitude.

---

### Q2. Which similarity measure combines both vector direction and magnitude?

| | |
|---|---|
| **Correct ✓** | **Dot product** |

**Live note:** Most students picked the dot product, with some choosing cosine similarity.

**Explanation:** Cosine similarity uses only the angle. The dot product multiplies matching components and sums them, so it depends on both angle and length.

---

### Q3. What is an embedding mismatch in a retrieval system?

| | |
|---|---|
| **Correct ✓** | **Queries are embedded with a different model than the documents** |

**Live note:** Most students answered correctly.

**Explanation:** Vectors from two different models live in different spaces, so their similarity is meaningless. Use the same model, and the same version, for documents and queries. If you upgrade, re-embed the whole corpus.

---

## Quiz 2 - After the RAG and retrieval block

### Q4. What is the main process in a retrieval-augmented generation (RAG) pipeline?

| | |
|---|---|
| **Correct ✓** | **Retrieve relevant passages and use them as evidence for the answer** |

**Live note:** Most students answered correctly.

---

### Q5. What does recall@K measure? (Reconstructed: the stem and options were not captured in the transcript.)

| | |
|---|---|
| **Correct concept ✓** | The **fraction of all correct chunks** that appear in the top K results |

**Explanation:** Recall@K asks whether the right chunks were found at all. It is the most important metric for RAG, because a chunk outside the top K never reaches the LLM. Precision@K asks how many of the top K are correct.

---

### Q6. What is hybrid search in information retrieval?

| | |
|---|---|
| **Correct ✓** | **Combining keyword (lexical) search and vector (semantic) search** |

**Live note:** The lecturer gave the answer after the poll was slow to fill, so it was not tallied.

---

## Quiz 3 - After vector indexes and ANN (Part 6)

### Q7. What does a vector database typically store to enable similarity search?

| | |
|---|---|
| **Correct ✓** | **Numerical embeddings and metadata** |

**Live note:** Most students answered correctly.

**Explanation:** The embeddings are used for the similarity comparison. The metadata (for example customer ID, language, date) is used for filtering.

---

### Q8. Why are approximate nearest neighbour (ANN) indexes used in vector search?

| | |
|---|---|
| **Correct ✓** | **They speed up search with minimal loss of accuracy** |

**Live note:** Most students answered correctly.

**Explanation:** Exact search compares the query with every vector, which becomes too slow beyond about 10 million vectors. ANN checks only a small fraction and typically reaches 95 to 99 percent ANN recall.

---

### Q9. What is HNSW in the context of vector databases?

| | |
|---|---|
| **Correct ✓** | **A graph-based ANN index with hierarchical layers** |

**Live note:** Most students answered correctly.

---

## Quiz 4 - After re-ranking (Lab 4) and the closing blocks

### Q10. A user searches for "order 1843 not delivered". Which method reliably finds the ticket with that exact order ID? (Recap question asked verbally, not a Mentimeter poll.)

| | |
|---|---|
| **Correct ✓** | **BM25 (lexical search)** |

**Explanation:** BM25 matches the identifier word for word. A semantic model breaks the identifier into sub-pieces that carry little meaning, so exact codes can return a different document.

---

### Q11. Which configuration did the lecturer recommend for 30 million Hindi and English chunks on a cloud vendor? (Reconstructed: the option text was partly lost. The lecturer confirmed the answer was option C.)

| | |
|---|---|
| **Correct ✓** | **A multilingual Matryoshka model at 512 dimensions, with a hybrid retrieval approach** |

**Explanation:** Hindi plus English needs a multilingual model. Matryoshka at 512 dimensions keeps storage and memory manageable at this scale. A hybrid approach covers exact identifiers as well as meaning. The cloud vendor makes the privacy and DPDP check important before you use it.

---

## Quick self-check

| Claim | True / False |
|-------|----------------|
| Cosine similarity of 0.8 means "very similar" for every embedding model | **False**. Scores are model-specific; test the threshold on your golden set |
| If every vector is normalised to length 1, cosine, dot product and Euclidean distance give the same ranking | **True** |
| The same embedding model must be used for documents and for queries | **True** |
| BM25 scores are on a fixed 0 to 1 scale | **False**. BM25 is unbounded and depends on query length and corpus |
| Recall@K is the most important retrieval metric for RAG | **True** |
| An ANN index always returns the exact nearest neighbours | **False**. ANN trades a small amount of recall for speed |
| Min-max normalisation is robust to one very high BM25 score | **False**. One outlier squashes the others towards 0 |
| RRF uses the raw BM25 and cosine scores | **False**. RRF uses only the ranks, with `k = 60` |
| A cross-encoder is used for the first retrieval over millions of chunks | **False**. It is too slow for the full corpus, so it re-ranks a short candidate list |
| Vector embeddings are privacy-preserving, so DPDP does not apply to them | **False**. Vectors should be treated like the text they came from |
| Adding more chunks to the LLM always improves the answer | **False**. More context raises cost and latency and can hurt accuracy |
| Upgrading to a bigger LLM is usually the best first fix for poor answers | **False**. Improving retrieval and context often gives a larger gain |
