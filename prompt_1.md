The cleanest design separates concerns at the tool boundary, then lets the agent orchestrate. A few key choices matter.

**Tool surface**

Don't expose just one tool. Your current `query(query, doc_ids)` is the "depth" tool. Add at least:

- `find_documents(query, k)` → returns candidate `doc_ids` with title and a one-paragraph summary, retrieved over the full 1M corpus
- `query_documents(query, doc_ids)` → your existing pipeline
- Optionally `get_document_outline(doc_id)` → returns section headers / TOC

The reason: with 1M docs at ~100 pages each, the agent cannot reason about *which* docs to query without a discovery step, and forcing it to call your existing pipeline over the full corpus is wasteful (10k chunks out of ~100M pages is 0.01% recall — fine within a known doc set, useless as discovery). Build a document-level index (one embedding per doc summary, optionally hierarchical: summary index + chunk index), so `find_documents` is cheap and discriminating. This is the same separation Chen et al. and HippoRAG exploit — coarse selection over fine retrieval.

**Decomposition strategy**

The agent should classify the incoming query into one of three regimes:

1. *Single-hop*: just call `query_documents` with discovered docs.
2. *Independent multi-hop* (e.g., "Compare X across companies A, B, C") → decompose into a fixed set of sub-queries, fan out in parallel, synthesize at the end.
3. *Dependent multi-hop* (e.g., "Who was CEO of X when Y was acquired?") → cannot plan all hops upfront; hop N+1 is constructed from hop N's answer.

A static planner that emits a DAG of sub-queries with explicit dependencies handles all three uniformly. Independent edges run in parallel; dependent edges block until predecessors resolve. Concretely:

```
plan = planner_llm(query) 
     → [(node_id, subquery_template, depends_on, candidate_docs_hint)]
```

Templates contain placeholders like `{node_3.answer}` so the executor fills them in at runtime. This gives you parallel speedup where the structure allows it, without giving up iterative behavior on the truly sequential parts.

**Iterative replanning**

Pure plan-and-execute breaks when a later hop reveals that an earlier hop's assumption was wrong. Allow controlled replanning: after each completed node, the agent can continue, append nodes, or rewrite pending ones. A ReAct-style loop wrapped around the DAG executor is enough. Cap at ~5 hops; that covers the long tail of real questions, and the failure mode beyond that is usually decomposition error rather than depth.

**Cross-hop state**

This is where most multi-hop RAG implementations leak quality:

- **Evidence memory**: union of reranked top-50 chunks from each hop, keyed by chunk_id with provenance (which sub-query retrieved them). Deduplicate across hops. The final synthesizer sees the accumulated pool, not just the last hop's chunks.
- **Active doc set**: starts empty, expanded by `find_documents` calls or by entities surfaced in intermediate answers, narrowed when the agent gains confidence. Passed as the `doc_ids` filter to subsequent `query_documents` calls.
- **Sub-Q/A log**: short answers per sub-question, used both as substitutions for dependent placeholders and as inputs to the final synthesis prompt.

**Reranking under multi-hop**

Your current reranker scores chunks individually against one query. At synthesis time what you actually want is *coverage*: does the chunk set collectively answer all sub-questions? This is exactly the LANCER formulation. Two practical levels:

- Per-hop reranking as today + cross-hop dedup. Adequate for most cases.
- A final coverage-aware rerank over the accumulated evidence pool against the full set of decomposed sub-questions, before synthesis. This is where coverage-based scoring substantially beats marginal relevance, because individually-relevant chunks frequently cluster on the same sub-question and leave others unsupported.

**Implementation notes worth flagging**

- HyDE on each sub-query, especially dependent ones — they tend to be abstract/anaphoric ("the company mentioned above") and embed poorly without expansion.
- Standalone-rewrite the original query against conversation history before decomposition; conversational follow-ups otherwise propagate ambiguity into every sub-query.
- Verification pass after synthesis: prompt the LLM to check each claim against evidence memory, flag unsupported claims for one extra retrieval round. Cheap, large quality win on factuality.
- Budgets: max hops (5), max docs per `find_documents` (~50–100), max unique chunks in evidence memory (~200). These prevent runaway costs without hurting recall on realistic queries.
- Aggressive sub-query caching. Embed each sub-query and skip near-duplicates — agents reformulate the same question constantly.

**Frameworks**

LlamaIndex has `SubQuestionQueryEngine` and `RouterQueryEngine` that prototype this fast, and LangGraph is good for the DAG/replan loop. But for your stack (Qwen3-Embedding-8B + BM25 + RRF + Qdrant + cross-encoder), I'd build the orchestration directly — the frameworks add latency, constrain the planner/executor wiring, and obscure where to plug in coverage reranking. Borrow the patterns, not the code.

Want me to sketch the DAG executor + evidence-memory contract as a concrete diagram or pseudocode skeleton?
