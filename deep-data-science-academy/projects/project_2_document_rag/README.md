# Capstone Project 2 — Document Intelligence RAG + MLOps & Production System

**Days 271–272.** An end-to-end generative-AI product: ingest documents → chunk → embed → retrieve → generate
grounded answers with citations → serve via FastAPI → ship in Docker → track with MLflow → monitor drift,
cost and quality in production.

## System question

> Given a folder of business documents, answer questions **with citations**, refuse when the answer is not in the
> corpus, and prove the answers are faithful.

The refusal and the proof are the parts that separate a demo from a product.

## Architecture

```
                    ┌──────────────── INGESTION (offline, batch) ────────────────┐
  PDFs / DOCX / HTML│ extract text+layout → clean → chunk (semantic) → embed     │
   / CSV / markdown │ → upsert into vector store (metadata: source, page, date)  │
                    └───────────────────────────────────────────────────────────┘
                                              │
   question ──► API (FastAPI) ──► retriever (hybrid: BM25 + dense) ──► reranker (cross-encoder)
                                      │                                        │
                                      └──────► prompt assembly (context + citations + refusal rule)
                                                              │
                                                        LLM (any provider)
                                                              │
                                    answer + citations ──► validator (schema + faithfulness check)
                                                              │
                        Streamlit UI ◄──────────────────────────┘
                                              │
                    observability: latency, token cost, retrieval hit-rate, groundedness, drift
```

## Deliverable checklist

| # | Artefact | Where | Days |
|---|---|---|---|
| 1 | Requirements + SLAs (latency, cost/query, quality target) | `docs/requirements.md` | 271 |
| 2 | Ingestion pipeline with layout-aware extraction and page metadata | `src/ingest.py` | 253 |
| 3 | Chunking strategy with measured trade-offs (size/overlap) | `src/chunk.py` | 253 |
| 4 | Embedding + vector index (FAISS/Chroma) with metadata filtering | `src/index.py` | 251–252 |
| 5 | Hybrid retrieval + reranking | `src/retrieve.py` | 254 |
| 6 | Grounded generation with citation enforcement and refusal | `src/generate.py` | 254–255 |
| 7 | FastAPI service with Pydantic schemas + Swagger docs | `src/api.py` | 261 |
| 8 | Streamlit UI (upload, ask, see citations, thumbs-up/down) | `app/streamlit_app.py` | 259 |
| 9 | Evaluation harness: golden set of 50 Q/A + RAGAS-style metrics | `eval/run_eval.py` | 255 |
| 10 | MLflow tracking of index/prompt/model versions and eval scores | `mlops/track.py` | 264–265 |
| 11 | Monitoring dashboard: latency, cost, refusal rate, groundedness, retrieval drift | `mlops/monitor.py` | 266 |
| 12 | Dockerfile + docker-compose (api, ui, vector store) | `Dockerfile`, `docker-compose.yml` | 262–263 |
| 13 | Architecture review + cost model | `docs/architecture_review.md` | 272 |

## Evaluation must be first-class

Build a golden set of **50 questions** with known correct answers *and* 10 questions whose answers are **not** in
the corpus (to test refusal). Report:

| Metric | Definition | Target |
|---|---|---|
| Context precision | share of retrieved chunks that are relevant | ≥ 0.7 |
| Context recall | share of needed evidence retrieved | ≥ 0.8 |
| Faithfulness | share of answer claims supported by retrieved context | ≥ 0.9 |
| Answer relevance | answers actually address the question | ≥ 0.85 |
| Refusal accuracy | correctly refuses unanswerable questions | ≥ 0.9 |
| p95 latency | end-to-end response time | < 4 s |
| Cost per query | embedding + LLM tokens | < $0.01 |

Run the harness on every prompt/index change (regression testing for LLM systems) and log every run to MLflow.

## Production concerns to address explicitly

1. **Prompt injection**: documents are untrusted input; never let retrieved text override system instructions.
2. **PII**: redact before embedding; keep the vector store inside your trust boundary.
3. **Caching**: exact-match cache plus semantic cache to control cost and latency.
4. **Failure modes**: retrieval miss → refusal; LLM timeout → fallback model or cached answer; store outage → degrade to keyword search.
5. **Drift**: monitor query distribution and retrieval hit-rate; alert when quality metrics drop.
6. **Cost model**: tokens per query, embedding refresh costs, storage growth per month.
7. **Security**: API keys in secrets/env only; never in the repository; rate limiting per client.

## Run it

```bash
python -m pip install -r ../../requirements.txt
python src/ingest.py --docs ./corpus --out ./data/chunks.jsonl
python src/index.py  --chunks ./data/chunks.jsonl --store ./data/index
python eval/run_eval.py --index ./data/index --golden eval/golden_set.jsonl
uvicorn src.api:app --host 0.0.0.0 --port 8000     # Swagger at /docs
streamlit run app/streamlit_app.py                 # UI
docker compose up --build                          # full stack
```

## Grading rubric (100 points)

| Criterion | Points |
|---|---|
| Ingestion + chunking quality (layout, tables, metadata) | 10 |
| Retrieval quality with measured hybrid + rerank gains | 15 |
| Grounding: citations, refusal behaviour, no hallucinated policy | 15 |
| Evaluation harness with golden set, reported honestly | 15 |
| API design: Pydantic schemas, status codes, error handling | 10 |
| Deployment: Docker/Compose, configurable, runs from a clean clone | 10 |
| MLOps: tracking, versioning, monitoring, drift alerts | 15 |
| Architecture review + cost model + trade-off justification | 10 |
