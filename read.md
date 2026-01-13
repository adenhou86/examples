┌─────────────────────────────────────────────────────────────────────┐
│                            USER INPUT QUERY                          │
│                               (query)                                │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    get_multihop_rag_answer(query, llm)                │
│  - init current_query = query                                          │
│  - init all_retrieved_docs = []                                        │
│  - init reasoning_trace = {hops: [], summary: ""}                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MULTI-HOP LOOP (for hop in 1..max_hops)            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                ┌──────────────────────────────────────┐
                │  Q_hop = current_query                │
                │  (Q1 = original, Q2.. = sub-questions)│
                └──────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│               Retrieve docs: _retrieve_documents_simple(Q_hop)         │
│               (Vector DB similarity_search, top_k=docs_per_hop)        │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│         Truncate + tag: _truncate_documents(docs, word_limit, hop)     │
│  - doc.page_content truncated to N words                               │
│  - doc.metadata["hop"] = hop                                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│           Structured reasoning: _generate_structured_reasoning(...)    │
│  Inputs:                                                               │
│   - original query                                                     │
│   - current sub-question Q_hop                                         │
│   - retrieved docs A_hop                                               │
│   - previous reasoning_trace (Q/A/R from earlier hops)                 │
│  LLM outputs:                                                          │
│   INSIGHTS / REASONING / MISSING_INFO                                  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│     Append to reasoning_trace["hops"]:                                 │
│       {hop, question, retrieved_docs, insights, reasoning, missing}    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│            Stop-or-continue decision (no_missing detection)            │
│  if missing_info indicates "no missing info" → BREAK early             │
│  else → generate next sub-question                                     │
└─────────────────────────────────────────────────────────────────────┘
                     │                               │
                     │ BREAK                         │ CONTINUE
                     ▼                               ▼
      ┌───────────────────────────┐   ┌──────────────────────────────────────┐
      │ Exit multi-hop loop        │   │ Next sub-question generation          │
      └───────────────────────────┘   │ _generate_next_subquestion_from_missing│
                                      │  Inputs: original query + missing_info │
                                      │  Output: Q_(hop+1)                     │
                                      └──────────────────────────────────────┘
                                                   │
                                                   ▼
                                      ┌───────────────────────────┐
                                      │ current_query = Q_(hop+1)  │
                                      └───────────────────────────┘
                                                   │
                                                   ▼
                                      (loop back to retrieval step)


AFTER LOOP COMPLETES (either reached max_hops or broke early)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│    Deduplicate: unique_docs = _remove_duplicates_with_metadata(...)    │
│    (remove repeated docs across hops)                                  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Final synthesis: _generate_final_answer_structured(query, unique_docs) │
│  LLM sees:                                                             │
│   - ORIGINAL QUESTION                                                  │
│   - FULL MULTI-HOP TRACE (Q1/A1/R1 ... Qn/An/Rn)                        │
│   - ALL UNIQUE DOCS WITH METADATA                                      │
│  Produces:                                                             │
│   - Synthesized answer                                                  │
│   - Formatted reasoning trace                                           │
│   - Document sources section                                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FINAL OUTPUT TO USER                           │
│  🔍 MULTI-HOP REASONING TRACE                                           │
│  🎯 SYNTHESIZED ANSWER                                                  │
│  📄 DOCUMENT SOURCES                                                    │
└─────────────────────────────────────────────────────────────────────┘
