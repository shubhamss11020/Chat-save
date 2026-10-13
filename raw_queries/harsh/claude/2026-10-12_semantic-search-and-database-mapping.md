---
conversation_id: 927df246-8470-4dbb-abb3-f0cc926c54af
platform: claude
username: "harsh"
title: "Semantic search and database mapping"
created_at: "2026-10-12 15:05:03 EDT"
updated_at: "2026-10-13 08:33:07 EDT"
---

# Semantic search and database mapping

## User (2026-10-13 08:33:07 EDT)

Give me details about semantic search how it basically mapping with the db

## Claude (2026-10-13 08:33:07 EDT)

> *Thinking:*
>

Semantic search finds records by meaning rather than exact keywords, and it maps back to your database by storing a vector for each piece of text next to the row it came from.

## The core idea

An embedding model turns text into a list of numbers (a vector, typically 768 to 3072 dimensions). Texts with similar meaning end up close together in that vector space. "Invoice mismatch on coil order" and "billing discrepancy for steel shipment" share almost no keywords, but their vectors are near each other. A keyword search (`ILIKE`, `tsvector`) would miss that match.

## How it maps to the database

**1. Chunk the source rows.** Long content (emails, call transcripts, wiki pages) is split into chunks of roughly 200 to 500 tokens, usually with some overlap. One embedding for a whole transcript is too blurry, so each chunk gets its own.

**2. Embed each chunk and store it with a pointer back to the source.** With Postgres and pgvector, it looks like this:

```sql
CREATE EXTENSION vector;

CREATE TABLE chunks (
  id          bigserial PRIMARY KEY,
  source_table text,        -- 'emails', 'calls', 'wiki_pages'
  source_id    bigint,      -- id of the original row
  client_id    bigint,      -- metadata for filtering
  chunk_index  int,
  content      text,        -- the chunk's text
  embedding    vector(1536) -- the embedding
);
```

The `source_table` and `source_id` columns are the mapping. A vector hit is just a chunk, and those two columns take you back to the original email, call or page.

**3. Build a vector index.** Without one, every query compares against every row.

```sql
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
```

HNSW is fast and accurate but uses more memory. IVFFlat is lighter and needs tuning. Both are approximate nearest-neighbor indexes, so they trade a little recall for a lot of speed.

**4. At query time, embed the question and find the nearest chunks.** You must use the same model that embedded the chunks.

```sql
SELECT source_table, source_id, content,
       embedding <=> $1 AS distance   -- $1 = query embedding
FROM chunks
WHERE client_id = 42                   -- ordinary SQL filter
ORDER BY embedding <=> $1
LIMIT 10;
```

`<=>` is cosine distance, where smaller means more similar.

**5. Join back to the real data.** Take the `source_id` values from the top chunks and fetch the full email, call or page. You can also pass the top chunks to an LLM as context (RAG).

## The flow

```
Ingest:  row → chunk → embed → store (vector + source_id + metadata)
Query:   question → embed → nearest vectors → source_id → full row → answer
```

## Practical points

- **Hybrid search is usually best.** Combine vector similarity with keyword search (`tsvector`) and merge the rankings, for example with Reciprocal Rank Fusion. Vectors handle meaning, while keywords handle exact terms such as part numbers, client names and PO numbers.
- **Use metadata filters.** Filters like `client_id`, date or source type narrow the search before or during the vector lookup, and they improve both speed and relevance.
- **Re-embed when the model changes.** Vectors from different models aren't comparable, so changing models means re-embedding everything.
- **Keep it in sync.** New or edited rows need re-chunking and re-embedding, usually through a trigger, a queue or a periodic sweep. Mark each chunk with a content hash so you only re-embed what changed.
- **Pick the dimension and cost deliberately.** More dimensions mean more storage and slower search. The practical ceiling for pgvector's HNSW index is 2000 dimensions for the `vector` type. Higher-dimension embeddings need `halfvec` or reduced dimensions.
- **Distance is not confidence.** A nearest result is always returned even if nothing is truly relevant, so set a distance threshold or add a reranker.

If you're asking about the AskCruz connector specifically, the same pattern applies. The existing tables (emails, calls, wiki pages, implementation tasks) would each feed a shared `chunks` table keyed by `source_table` and `source_id`, and the search tools would run the vector query and return the same ids the `get_*` tools already accept. I can sketch that schema or the ingestion pipeline for it if that's useful.

One note: I couldn't archive this conversation. The Threads-OV save tool isn't connected in this session, so `save_chat_transcript` wasn't available. Reconnecting it in Settings → Connectors will restore archiving.
