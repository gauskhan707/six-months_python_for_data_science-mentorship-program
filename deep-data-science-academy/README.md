---
title: Deep Data Science & AI Academy
emoji: 📊
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: A 275-day interactive Data Science, ML, DL, GenAI & MLOps academy
---

# Deep Data Science & AI Academy

A complete **275-day learning platform** that takes you from Python beginner to job-ready data scientist
and AI engineer — deeper than the original course, faithful to it, and fully traceable.

This is a **working application**, not a roadmap: 275 built lessons, interactive quizzes, flashcards,
progress tracking, bookmarks, notes and an AI Tutor that knows the lesson you are reading.

```
275 days · 16 phases · 1,374 quiz items · 1,650 flashcards · 574 interview questions
806 code examples with expected output · 258 days linked to original recordings
```

---

## Quick start

```bash
cd deep-data-science-academy
python3 app.py                 # no dependencies to install
# open http://localhost:7860
```

Optional, to run the **lesson code** (not needed to browse the academy):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Rebuild content after authoring or editing lessons:

```bash
python3 tools/build_content.py     # regenerates all 275 lesson JSON files + indices
python3 tools/build_docs.py        # regenerates the traceability documentation
python3 tools/audit.py             # full quality-control audit -> docs/QC_REPORT.md
```

---

## What is inside

```
deep-data-science-academy/
├── app.py                     # zero-dependency HTTP server + JSON API
├── curriculum.json            # 275-day index (phases, titles, topics, keywords)
├── Dockerfile                 # Hugging Face Spaces (Docker SDK) ready
├── requirements.txt           # learner environment (the app itself needs nothing)
├── content/
│   └── day_001.json .. day_275.json      # one self-contained lesson per day
├── assets/
│   ├── index.html             # app shell
│   ├── style.css              # styling layer (responsive, dark/light, print)
│   ├── app.js                 # UI logic: routing, modes, quiz, search, progress
│   ├── visuals.js             # generated teaching diagrams (SVG, no downloads)
│   ├── tutor.js               # AI Tutor (offline engine + optional live model)
│   └── search_index.json      # light index used by search
├── quizzes/quiz_bank.json     # 1,374 items, every one linked to its day
├── flashcards/flashcard_bank.json
├── interview/interview_bank.json
├── projects/
│   ├── project_1_olist/       # Capstone 1: analytics + ML dashboard
│   └── project_2_document_rag/# Capstone 2: Document Intelligence RAG + MLOps
├── docs/                      # QC report, source mapping, gap analysis, curriculum
└── tools/                     # content pipeline (index, packs, engine, build, audit)
```

**Architecture rule:** content (JSON) / UI (HTML+JS) / styling (CSS) / logic (server + JS) are separate.
The browser never loads all 275 lessons: it fetches `content/day_NNN.json` on demand, and only keeps a light
index in memory. The whole academy is ~6 MB of JSON and runs on a free tier.

---

## Every day is a real lesson

Each of the 275 lessons contains 24 sections:

1. Learning objectives · 2. Prerequisites · 3. Why this matters · 4. Concept (what/why/how) ·
5. Simple explanation · 6. Intuition · 7. Real-world analogy · 8. Visual explanation ·
9. Internals · 10. Deep technical explanation (+ mathematics) · 11. Code examples · 12. Source traceability ·
13. Common mistakes · 14. Debugging examples · 15. Practice exercises · 16. Mini challenge ·
17. Interview questions with model answers · 18. Real-world application · 19. Production considerations ·
20. Recap · 21. Revision block · 22. Flashcards · 23. Checkpoint quiz · 24. Project connection.

Teaching flow used for hard topics: **WHAT → WHY → INTUITION → HOW → INTERNALS → CODE → VISUAL → EXAMPLE →
MISTAKES → PRACTICE → INTERVIEW → REAL WORLD → PRODUCTION.**

---

## Source fidelity and labelling

Content is labelled everywhere it appears:

| Label | Meaning |
|---|---|
| **[SOURCE]** | Directly supported by the original Codanics six-month recordings / repository |
| **[EXPLANATION]** | Academy rewritten teaching explanation |
| **[EXTENSION]** | Modern/deeper knowledge **not** covered in the original course |
| **[PRACTICE]** | Hands-on exercises |
| **[PROJECT]** | Project-based application |
| **[INTERVIEW]** | Interview preparation |
| **[PRODUCTION]** | Real-world production knowledge |

Source material actually ingested:

* **274 lecture transcripts** (`ALL_275_TRANSCRIPTS.zip`) — parsed into **193,909 timestamped segments**.
  A verified Urdu→Devanagari dictionary maps technical terms to how the mentor actually says them
  (`pandas → पांडा`, `machine learning → मशीन लर्निंग`), so **171 days deep-link to the exact
  timestamp** where the topic is taught, with a real quotation.
* **The course repository** — every `.ipynb` and `.py` file is parsed; **2,194 real code cells** are indexed and
  attached to lessons that match them, with the file path as citation.
* **The YouTube playlist** — lesson sequence and titles are used for ordering and gap detection. No video content
  is invented; where a transcript moment cannot be matched, the lesson says so explicitly.

Full per-day traceability: [`docs/SOURCE_MAPPING.md`](docs/SOURCE_MAPPING.md).

---

## Course gaps closed (see `docs/GAP_ANALYSIS.md`)

The original course is strong on Python, pandas, visualisation, maths, statistics, ML, deep learning,
time series, Streamlit/Flask and BI tools. It is **thin or silent** on the things employers now assume:

| Gap | Academy days |
|---|---|
| SQL (never taught in the recordings) | 135–150 |
| Excel analytics | 151–154 |
| Docker & containers | 262–263 |
| MLflow, testing, CI/CD | 264–265 |
| Monitoring, data drift, model drift | 266 |
| PySpark / distributed data | 267 |
| Cloud & ML system design | 268 |
| Attention, transformers, BERT/GPT internals | 238–242 |
| RAG evaluation, hallucination, grounding | 255 |
| Structured outputs, tools, agents | 250, 257 |
| PyTorch (recordings use TensorFlow only) | 219–222 |

---

## Interactive features

* **Navigation** — previous/next, day selector, jump-to-day, phase accordion, hash URLs (`#/day/137`).
* **Search** — server-side API with a client-side fallback over titles, topics, keywords and objectives.
* **Learning modes** — Beginner, Deep, Code, Interview, Project, Revision (keys `1`–`6`).
* **Quiz engine** — one attempt per question, immediate feedback, explanations, per-day score persisted locally.
* **Flashcards** — click to flip; 1,650 cards derived from the lessons.
* **Progress tracking** — completed days, progress bar, per-phase counts (localStorage).
* **Bookmarks & notes** — per-day bookmarking and a notes editor; both persist in your browser.
* **Copy-code buttons**, line-by-line code explanations, expected outputs, print/PDF lesson export.
* **Visual learning** — 20+ generated SVG diagrams (broadcasting, gradient descent, attention, RAG, joins,
  Docker layers, ML pipelines, confusion matrix…) plus a per-day pipeline diagram. No decorative graphics.
* **AI Tutor** — knows your current lesson and topic. Quick intents: explain simply / technically, give an
  example, give a coding problem, quiz me, interview me, why is my code wrong, beginner mode, real-world
  example, production use. It answers **offline** from the lesson's own materials, and optionally connects to
  any OpenAI-compatible endpoint (key stored only in your browser, sent directly to the endpoint you choose).
* **Responsive** — desktop, laptop, tablet and mobile layouts; dark/light theme; keyboard shortcuts.

---

## Deployment

**Hugging Face Spaces (Docker SDK):** push this folder; `app_port: 7860` and the `Dockerfile` are already set.
The container runs as a non-root user and has a healthcheck on `/api/health`.

**Any container host / VM:**

```bash
docker build -t dsacademy .
docker run -p 7860:7860 dsacademy
```

**Static hosting:** the front-end falls back to fetching `./content/day_NNN.json` and `./curriculum.json`
directly, so the whole academy can also be served as static files from any CDN.

---

## API

| Endpoint | Returns |
|---|---|
| `GET /api/health` | liveness + build statistics |
| `GET /api/curriculum` | light 275-day index |
| `GET /api/day/<n>` | full lesson JSON for a day |
| `GET /api/search?q=` | ranked search results |
| `GET /api/quiz?day=` · `/api/flashcards?day=` · `/api/interview?day=` | item banks |

---

## Content pipeline (how the 275 lessons are produced)

```
tools/index_data/phase_01.py .. phase_16.py   # authored 275-day index: title, topics, source mapping, difficulty
tools/content_packs/phase_XX*.py              # authored deep lessons (WHAT/WHY/INTUITION/CODE/QUIZ/...)
tools/source_extract.py                       # parses the transcript zip + repository notebooks
tools/lesson_engine.py                        # renders each day into the full 24-section lesson JSON
tools/build_content.py                        # writes content/, curriculum.json and the banks
tools/build_docs.py                           # writes docs/ (curriculum, source map, gap analysis)
tools/audit.py                                # quality-control audit -> docs/QC_REPORT.md
```

Lessons are produced in the batches defined by the build brief: 1–32, 33–66, 67–99, 100–102, 103–120,
121–128, 129–131, 132–134, 135–150, 151–164, 165–196, 197–212, 213–232, 233–246, 247–258, 259–268, 269–275.
Authored packs currently cover Phase 1 (Days 1–15); a lesson without an authored pack is served as a
**guided source lesson**: full objectives, prerequisites, visual, real repository code, real timestamped lecture
moments, definition/code/failure drills, mistakes, debugging help, self-check quiz and flashcards — explicitly
labelled, with nothing fabricated. `docs/QC_REPORT.md` tracks authored depth per phase.

---

## Quality control

`tools/audit.py` verifies, and `docs/QC_REPORT.md` reports:

* 275/275 days present, sequential, complete 24-section schema
* quiz (≥3), practice (≥2) and interview (≥2) coverage on every day
* code examples with expected output everywhere
* phase/topic coverage: SQL, Excel, Power BI, Tableau, ML, DL, NLP, Transformers, Hugging Face, GenAI, RAG,
  LangChain, FastAPI, Docker, MLflow, MLOps, PySpark, cloud, system design, interviews
* the complete canonical ML model collections (regression, classification, clustering, dimensionality reduction)
* source traceability and correct labelling of extensions
* all application assets and project folders present

Run it yourself: `python3 tools/audit.py`.

---

## Attribution

Source material: **Dr. Muhammad Aammar Tufail / Codanics** — the free *Six Months of AI and Data Science
Mentorship Program* (YouTube) and the accompanying repository
`gauskhan707/six-months_python_for_data_science-mentorship-program`.
The original lectures and code are and remain the foundation; this academy adds the rewritten explanations,
extensions, exercises, projects and interview preparation on top, and labels every addition as such.
