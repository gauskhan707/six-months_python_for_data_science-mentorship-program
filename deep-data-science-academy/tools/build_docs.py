#!/usr/bin/env python3
"""Generate the traceability documentation from the curriculum index.

Writes
    docs/SOURCE_MAPPING.md   day -> original recordings -> repository material -> labels
    docs/GAP_ANALYSIS.md     where the original course is thin, and which days fill it
    docs/CURRICULUM.md       the full 275-day table (phase, day, title, difficulty, tag)
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACADEMY = os.path.dirname(HERE)
DOCS = os.path.join(ACADEMY, "docs")
sys.path.insert(0, HERE)

import lesson_engine as engine  # noqa: E402
import phases as phase_mod  # noqa: E402

TAG_LABEL = {"src": "SOURCE", "mix": "SOURCE + EXTENSION", "ext": "ACADEMY EXTENSION"}


def main() -> None:
    rows = engine.load_index()
    with open(os.path.join(HERE, "source_transcripts.json"), encoding="utf-8") as fh:
        transcripts = {str(t["idx"]): t for t in json.load(fh)}
    os.makedirs(DOCS, exist_ok=True)

    # ---------------- CURRICULUM.md ---------------- #
    lines = ["# The 275-day curriculum", "",
             "Generated from `tools/index_data/phase_*.py` by `tools/build_docs.py`.", "",
             "Tags: **SOURCE** = taught in the original recordings, **SOURCE + EXT** = covered partially then "
             "extended, **EXT** = academy extension (not in the original recordings).", ""]
    for p in phase_mod.PHASES:
        lines += [f"## Phase {p['n']} - {p['name']} (Days {p['start']}-{p['end']})", "",
                  f"*Goal:* {p['goal']}", "", f"*Source status:* {p['source_note']}", "",
                  "| Day | Title | Difficulty | Source tag | Key topics |", "|---|---|---|---|---|"]
        for d in range(p["start"], p["end"] + 1):
            r = rows[d]
            label = {1: "beginner", 2: "intermediate", 3: "advanced"}[r["difficulty_num"]]
            topics = ", ".join(r["topics"][:3])
            lines.append(f"| {d} | {r['title']} | {label} | {TAG_LABEL[r['tag']]} | {topics} |")
        lines.append("")
    open(os.path.join(DOCS, "CURRICULUM.md"), "w", encoding="utf-8").write("\n".join(lines))

    # ---------------- SOURCE_MAPPING.md ---------------- #
    lines = ["# Source traceability map", "",
             "For every academy day: which original lecture(s) it derives from, which repository material is used, and "
             "how the content is labelled. This map is generated from the real transcript index "
             "(`tools/source_transcripts.json`, 274 recordings) and the repository file paths in `tools/index_data/`.", "",
             "`EXT` days are explicitly academy extensions: SQL, Docker, MLflow, MLOps, PySpark, CI/CD, monitoring, drift "
             "and system design were **not** taught in the original six-month recordings.", "",
             "| Day | Academy title | Original recording(s) | Repository material | Label |", "|---|---|---|---|---|"]
    for d in range(1, 276):
        r = rows[d]
        vids = []
        for v in r["videos"]:
            m = transcripts.get(v)
            if m:
                vids.append(f"_{m['date']}_ {m['title'][:70]}")
        vid_txt = "<br>".join(vids[:3]) if vids else "-"
        repo = "<br>".join(f"`{x}`" for x in r["repo"]) if r["repo"] else "-"
        lines.append(f"| {d} | {r['title']} | {vid_txt} | {repo} | {TAG_LABEL[r['tag']]} |")
    open(os.path.join(DOCS, "SOURCE_MAPPING.md"), "w", encoding="utf-8").write("\n".join(lines))

    # ---------------- GAP_ANALYSIS.md ---------------- #
    audio_topics = set()
    for r in rows.values():
        audio_topics.update(t.lower() for t in r["topics"])
    gaps = [
        ("SQL and relational databases", 135, 150,
         "The six-month recordings never teach SQL - Codanics delivers it as a separate playlist. For data roles, SQL is "
         "non-negotiable (most analyst interviews are SQL-heavy).",
         "16 days from relational modelling to window functions, query plans and an interview sprint, using the practice "
         "database shipped in `resources/datasets_for_practice/database.sqlite.zip`."),
        ("Excel analytics", 151, 154,
         "The recordings cover Tableau and Power BI but not Excel-based analysis, which is still the most common "
         "reporting surface in industry.",
         "Four days: cleaning and formulas, SUMIFS/XLOOKUP/INDEX-MATCH, PivotTables and Power Query, plus a dashboard case study."),
        ("Docker and containers", 262, 263,
         "Deployment in the recordings stops at an AWS EC2 walkthrough; containers are how everything ships today.",
         "Dockerfile construction, image slimming, Compose for multi-service apps, registries and container debugging."),
        ("MLflow, experiment tracking and model registry", 264, 265,
         "Not covered in the recordings; models were saved as .pkl/.h5 files without tracking or versioning.",
         "Tracking server, run comparison, autologging, registry stages, plus testing and CI/CD with GitHub Actions."),
        ("Monitoring, data drift and model drift", 266, 266,
         "Not covered. The course stops at deployment, which is where production work actually begins.",
         "Monitoring layers (system, data, model, business), PSI/KS drift detection, alerting, retraining triggers, "
         "shadow and canary releases."),
        ("PySpark and distributed processing", 267, 267,
         "Not covered: all data work in the recordings assumes a single machine.",
         "Spark architecture, lazy evaluation, DataFrame transformations, joins and aggregations at scale, Spark ML."),
        ("Cloud architecture and ML system design", 268, 268,
         "Only an EC2 deployment demo; no service mapping, autoscaling, cost or architecture design.",
         "Compute/storage/network mental model, AWS-GCP-Azure service mapping, batch vs online vs streaming inference, "
         "feature stores, data contracts and a full system-design walkthrough."),
        ("Attention, transformers and modern NLP", 238, 242,
         "The recordings teach NLP with bag-of-words, embeddings and LSTM/GRU, then jump to Hugging Face usage; the "
         "attention mechanism and transformer internals are not derived.",
         "Five days deriving attention, self-attention maths, the full transformer architecture, encoders (BERT) and "
         "decoders (GPT) before touching the Hugging Face API."),
        ("RAG evaluation, hallucination and grounding", 255, 255,
         "The recordings build chat-with-PDF apps but never measure whether the answers are correct.",
         "Faithfulness/relevance/context metrics, golden datasets, regression testing, hallucination taxonomy and "
         "grounding-with-citations patterns."),
        ("Structured outputs, function calling and agents", 250, 257,
         "Prompt engineering is covered; schema-constrained outputs, tool calling and agent loops are not.",
         "JSON-schema and Pydantic validation of model output, retry/repair loops, tool definitions, ReAct agent loop "
         "and when an agent is worse than a pipeline."),
        ("Fine-tuning transformers", 245, 245,
         "Transfer learning is shown conceptually; supervised fine-tuning of a transformer with the Trainer API is not.",
         "Full fine-tuning walkthrough: label mapping, Trainer vs custom loop, warmup/weight decay, checkpointing and serving."),
        ("Testing, typing and code quality in data code", 22, 23,
         "The recordings use notebooks; tests, type hints, linters and CI are absent.",
         "Type hints, pytest for data pipelines, logging, ruff/mypy and a CI workflow that runs them."),
        ("Time-series depth (stationarity diagnostics, SARIMAX, backtesting)", 209, 212,
         "ARIMA/SARIMA/Prophet are demonstrated but diagnostics, exogenous variables and rolling-origin backtesting "
         "are not developed.",
         "Stationarity tests, ACF/PACF reading, seasonal orders and rolling-origin evaluation for credible forecasts."),
        ("Deep learning in PyTorch", 219, 222,
         "The recordings teach deep learning with TensorFlow/Keras only.",
         "Four days of PyTorch: tensors, autograd, nn.Module training loops, Dataset/DataLoader, GPU and checkpoints - "
         "the framework most hiring loops ask about."),
        ("System design for ML interviews", 268, 274,
         "No interview preparation exists in the recordings beyond best-model presentations.",
         "Structured interview bank (574 questions), mock interview with a scoring rubric, 100-question final assessment "
         "and a job-readiness checklist."),
    ]
    lines = ["# Gap analysis: where the original course is thin, and how the academy closes it", "",
             "This is the honest audit the learner needs. Each row states what the original six-month recordings cover, "
             "what is missing, and which academy days fill the gap. Nothing here claims an academy extension was taught "
             "in the source.", "",
             "| Area | Academy days | Why it is a gap | What the academy adds |", "|---|---|---|---|"]
    for area, lo, hi, why, adds in gaps:
        lines.append(f"| {area} | {lo}-{hi} | {why} | {adds} |")

    # areas present in source, for contrast
    lines += ["", "## What the original course covers well (and the academy preserves)", "",
              "| Area | Original coverage | Academy days |", "|---|---|---|",
              "| Python programming | Days 1-7, plus the Python chilaa playlist | 1-32 |",
              "| pandas + EDA | Days 8-20 (parts 1-8, outliers, EDA case studies) | 49-70 |",
              "| Data visualization | Days 21-26 (matplotlib, seaborn, plotly, animated plots) | 71-88 |",
              "| Mathematics | Zero-to-Math series + linear algebra parts 1-8 | 89-112 |",
              "| Statistics | ABC of Statistics days 1-13 + 7 notebooks | 113-134 |",
              "| Machine learning | ML-101 days 1-21 + 28 notebooks | 165-196 |",
              "| Unsupervised ML | k-means, hierarchical, DBSCAN/OPTICS, GMM, PCA, SVD, t-SNE | 197-208 |",
              "| Deep learning | DL-101 days 1-8 (MLP, CNN, CV, RNN, LSTM/GRU, TensorFlow) | 213-232 |",
              "| Time series | ARIMA, SARIMA, Prophet, weather-forecasting project | 209-212 |",
              "| NLP basics | Sentiment analysis, LSTM/GRU text models | 233-237 |",
              "| GenAI tooling | Prompt engineering, Hugging Face, OpenAI APIs, LangChain, Streamlit chat-with-PDF | 243-257 |",
              "| Web apps | Streamlit (19 projects), Flask (9 apps), FastAPI (7 lessons), EC2 deployment | 259-261 |",
              "| BI tools | Tableau Public series (20 lessons), Power BI for Beginners (35 lessons) | 155-164 |",
              "| Projects | Heart disease, Titanic, bank churn (36 student notebooks), model comparisons | 269-272 |", "",
              "## Source-to-academy principle", "",
              "1. **Preserve sequence where it is pedagogically sound** - Python before pandas before ML is the original order and stays.",
              "2. **Move where the original order hurts** - the original course taught pandas (Days 8-20) before NumPy (Days 28-32); "
              "the academy puts NumPy first (33-48) because pandas is built on it, while keeping the traceability links intact.",
              "3. **Label everything** - [SOURCE], [EXPLANATION], [EXTENSION], [PRACTICE], [PROJECT], [INTERVIEW], [PRODUCTION].",
              "4. **Never claim source for an extension** - SQL, Docker, MLflow, MLOps, PySpark, CI/CD, monitoring, drift and system "
              "design are marked as academy extensions throughout.", ""]
    open(os.path.join(DOCS, "GAP_ANALYSIS.md"), "w", encoding="utf-8").write("\n".join(lines))

    print("docs written: CURRICULUM.md, SOURCE_MAPPING.md, GAP_ANALYSIS.md")
    print("audio topics tracked:", len(audio_topics))


if __name__ == "__main__":
    main()
