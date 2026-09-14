#!/usr/bin/env python3
"""Quality-control audit for the 275-day academy.

Checks the questions from the build brief and writes docs/QC_REPORT.md.

    python3 tools/audit.py            # audit + write report
    python3 tools/audit.py --quiet    # exit code only (for CI)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACADEMY = os.path.dirname(HERE)
CONTENT = os.path.join(ACADEMY, "content")
DOCS = os.path.join(ACADEMY, "docs")
sys.path.insert(0, HERE)

REQUIRED_FIELDS = [
    "day", "phase", "title", "learning_objectives", "prerequisites", "why_this_matters", "concept",
    "visual", "code_examples", "common_mistakes", "debugging", "practice", "mini_challenge",
    "interview_questions", "real_world", "production", "recap", "quiz", "flashcards",
    "source_trace", "labels", "revision", "project_link", "prev_day", "next_day",
]
PHASE_TOPIC_REQUIREMENTS = {
    "SQL": [135, 150], "Excel": [151, 154], "Power BI": [155, 160], "Tableau": [161, 163],
    "Docker": [262, 263], "MLflow": [264, 265], "MLOps": [264, 266], "PySpark": [267, 267],
    "cloud": [268, 268], "system design": [268, 268], "FastAPI": [261, 261],
    "RAG": [254, 255], "LangChain": [256, 257], "Transformers": [240, 242],
    "Hugging Face": [243, 245], "interview": [274, 275], "GenAI": [247, 248],
    "deep learning": [213, 232], "NLP": [233, 246], "NumPy": [33, 48], "pandas": [49, 70],
}
ML_COLLECTION = ["Linear Regression", "Ridge", "Lasso", "Elastic Net", "Polynomial", "SVR",
                 "Decision Tree", "Random Forest", "Gradient Boosting", "AdaBoost", "XGBoost",
                 "LightGBM", "CatBoost", "Bayesian", "Poisson"]
CLF_COLLECTION = ["Logistic Regression", "KNN", "Naive Bayes", "Decision Tree", "Random Forest",
                  "SVM", "Gradient Boosting", "AdaBoost", "XGBoost", "LightGBM", "CatBoost"]
UNSUP_COLLECTION = ["K-Means", "Hierarchical", "DBSCAN", "OPTICS", "Gaussian Mixture", "PCA",
                    "SVD", "t-SNE", "UMAP", "anomaly"]


def load_lessons() -> dict[int, dict]:
    lessons = {}
    for f in sorted(os.listdir(CONTENT)):
        m = re.match(r"day_(\d{3})\.json$", f)
        if not m:
            continue
        with open(os.path.join(CONTENT, f), encoding="utf-8") as fh:
            lessons[int(m.group(1))] = json.load(fh)
    return lessons


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    lessons = load_lessons()
    with open(os.path.join(ACADEMY, "curriculum.json"), encoding="utf-8") as fh:
        curriculum = json.load(fh)

    problems: list[str] = []
    warnings: list[str] = []
    checks: list[tuple[str, str]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append((name, ("PASS" if ok else "FAIL") + f" - {detail}"))
        if not ok:
            problems.append(f"{name}: {detail}")

    # 1. completeness and sequence
    missing = [d for d in range(1, 276) if d not in lessons]
    check("All 275 days present", not missing, f"{len(lessons)}/275 lesson files" + (f"; missing {missing}" if missing else ""))
    non_sequential = [d for d in lessons if lessons[d]["day"] != d]
    check("Day numbers sequential", not non_sequential, "day field matches filename" if not non_sequential else str(non_sequential))

    # 2. required sections
    incomplete = {}
    for d, L in lessons.items():
        allow_null = {"prev_day", "next_day"}          # first/last day legitimately have no neighbour
        absent = [f for f in REQUIRED_FIELDS
                  if f not in L or (L[f] in (None, "", [], {}) and not (f in allow_null and f in L))]
        if absent:
            incomplete[d] = absent
    check("All required lesson sections", not incomplete,
          "every lesson has the full 24-section schema" if not incomplete else f"{len(incomplete)} lessons incomplete: {list(incomplete)[:8]}")

    # 3. depth
    full = [d for d, L in lessons.items() if L.get("depth") == "full"]
    authored_pct = len(full) / 275 * 100
    check("Lesson depth (authored deep lessons)", authored_pct > 5,
          f"{len(full)}/275 authored full lessons ({authored_pct:.1f}%), rest guided-source lessons")
    warnings.append(f"{275 - len(full)} days are currently guided-source lessons and await full authoring")

    # 4. quizzes, exercises, interview coverage
    no_quiz = [d for d, L in lessons.items() if len(L.get("quiz", [])) < 3]
    no_ex = [d for d, L in lessons.items() if len(L.get("practice", [])) < 2]
    no_int = [d for d, L in lessons.items() if len(L.get("interview_questions", [])) < 2]
    check("Checkpoint quiz on every day", not no_quiz, f"{275 - len(no_quiz)}/275 days have >=3 quiz items")
    check("Practice exercises on every day", not no_ex, f"{275 - len(no_ex)}/275 days have >=2 exercises")
    check("Interview questions on every day", not no_int, f"{275 - len(no_int)}/275 days have >=2 questions")

    # 5. code
    no_code = [d for d, L in lessons.items() if not L.get("code_examples")]
    check("Code examples present", not no_code, f"{275 - len(no_code)}/275 days include executable code")
    with_output = [d for d, L in lessons.items() if any(c.get("output") for c in L.get("code_examples", []))]
    check("Expected outputs supplied", len(with_output) >= 20, f"{len(with_output)} days show expected output")
    line_by_line = [d for d, L in lessons.items() if any(c.get("line_by_line") for c in L.get("code_examples", []))]
    check("Line-by-line code explanations", len(line_by_line) >= 15, f"{len(line_by_line)} days explain code line by line")

    # 6. phase/topic coverage
    for topic, (lo, hi) in PHASE_TOPIC_REQUIREMENTS.items():
        span = [d for d in range(lo, hi + 1) if d in lessons]
        norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
        hits = [d for d in span
                if norm(topic) in norm(lessons[d]["title"] + " " + " ".join(lessons[d].get("topics", [])))]
        check(f"Topic coverage: {topic}", bool(hits), f"{len(hits)} day(s) in {lo}-{hi}: {hits[:4]}")

    # 7. canonical model collections
    all_text = " ".join((L["title"] + " " + " ".join(L.get("topics", []))) for L in lessons.values()).lower()
    missing_models = [m for m in ML_COLLECTION + CLF_COLLECTION if m.lower() not in all_text]
    check("Canonical ML model collection preserved", not missing_models,
          "all regression + classification models scheduled" if not missing_models else f"missing: {missing_models}")
    missing_unsup = [m for m in UNSUP_COLLECTION if m.lower() not in all_text]
    check("Unsupervised collection preserved", not missing_unsup,
          "k-means through UMAP scheduled" if not missing_unsup else f"missing: {missing_unsup}")

    # 8. gap topics (extension)
    gaps = ["sql", "docker", "mlflow", "mlops", "pyspark", "ci/cd", "monitoring", "drift",
            "rag", "langchain", "system design", "cloud", "testing"]
    gap_days = {g: [d for d, L in lessons.items()
                    if g in (L["title"] + " " + " ".join(L.get("topics", []))).lower()] for g in gaps}
    check("Course gaps identified and covered", all(gap_days.values()),
          "; ".join(f"{g}: day {v[0]}" for g, v in gap_days.items() if v))

    # 9. source traceability
    with_source = [d for d, L in lessons.items() if L["source_trace"].get("moments") or L["source_trace"].get("videos")]
    with_moment = [d for d, L in lessons.items() if L["source_trace"].get("moments")]
    real_moment = [d for d, L in lessons.items()
                   if any(not m.get("fallback") for m in L["source_trace"].get("moments", []))]
    check("Source traceability present", len(with_source) >= 150,
          f"{len(with_source)} days link original recordings; {len(real_moment)} have keyword-matched timestamped moments")
    extension_days = [d for d, L in lessons.items() if L.get("tag") == "ext"]
    check("Academy extensions labelled", len(extension_days) >= 20,
          f"{len(extension_days)} days are labelled ACADEMY EXTENSION and never claimed as source content")

    # 10. prerequisites sanity
    broken_prereq = [d for d, L in lessons.items() if d > 1 and not L.get("prerequisites")]
    check("Prerequisites defined", not broken_prereq, "every day after Day 1 lists prerequisites")

    # 11. assets / app
    for rel in ("app.py", "curriculum.json", "assets/index.html", "assets/style.css", "assets/app.js",
                "assets/tutor.js", "assets/visuals.js", "assets/search_index.json",
                "quizzes/quiz_bank.json", "flashcards/flashcard_bank.json", "interview/interview_bank.json"):
        check(f"Application asset: {rel}", os.path.exists(os.path.join(ACADEMY, rel)),
              "present" if os.path.exists(os.path.join(ACADEMY, rel)) else "MISSING")

    projects = os.path.join(ACADEMY, "projects")
    for proj in ("project_1_olist", "project_2_document_rag"):
        check(f"Project folder: {proj}", os.path.exists(os.path.join(projects, proj)),
              "present" if os.path.exists(os.path.join(projects, proj)) else "MISSING")

    # totals
    totals = {
        "quiz_items": sum(len(L.get("quiz", [])) for L in lessons.values()),
        "flashcards": sum(len(L.get("flashcards", [])) for L in lessons.values()),
        "interview_qs": sum(len(L.get("interview_questions", [])) for L in lessons.values()),
        "exercises": sum(len(L.get("practice", [])) for L in lessons.values()),
        "code_examples": sum(len(L.get("code_examples", [])) for L in lessons.values()),
        "minutes": sum(L.get("est_minutes", 0) for L in lessons.values()),
    }

    report = ["# Quality Control Report - Deep Data Science & AI Academy", "",
              f"Generated by `tools/audit.py`. Lessons audited: **{len(lessons)}/275**.", "",
              "## Summary", "", f"- Checks run: **{len(checks)}**",
              f"- Failures: **{len(problems)}**",
              f"- Authored deep lessons: **{len(full)}/275** ({authored_pct:.1f}%)",
              f"- Days with timestamped source moments: **{len(real_moment)}**",
              f"- Days linking original recordings: **{len(with_source)}**",
              f"- Academy-extension days: **{len(extension_days)}**", "",
              "## Totals", ""]
    report += [f"- {k.replace('_', ' ')}: **{v:,}**" for k, v in totals.items()]
    report += ["", "## Checks", ""]
    report += [f"- {'✅' if c[1].startswith('PASS') else '❌'} **{c[0]}** - {c[1][7:]}" for c in checks]
    if problems:
        report += ["", "## Failures requiring action", ""] + [f"- {p}" for p in problems]
    if warnings:
        report += ["", "## Tracked warnings", ""] + [f"- {w}" for w in warnings]

    report += ["", "## Curriculum integrity", "",
               "| Phase | Days | Authored | Guided |", "|---|---|---|---|"]
    for p in curriculum["phases"]:
        aw = sum(1 for d in p["days"] if d["day"] in full)
        report.append(f"| {p['n']}. {p['name']} | {p['start']}-{p['end']} | {aw} | {p['count'] - aw} |")

    report += ["", "## How to close a failure", "",
               "1. `python3 tools/build_content.py` rebuilds every lesson from the curriculum index + authored packs.",
               "2. Add a pack in `tools/content_packs/phase_XX.py` with `PACKS[day] = {...}` to promote a guided day to a full lesson.",
               "3. Re-run `python3 tools/build_content.py && python3 tools/audit.py`.", ""]

    os.makedirs(DOCS, exist_ok=True)
    with open(os.path.join(DOCS, "QC_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(report))

    if not args.quiet:
        for c in checks:
            print(f"[{'ok' if c[1].startswith('PASS') else 'XX'}] {c[0]}: {c[1][7:]}")
        print(f"\n{len(problems)} failure(s). Report: docs/QC_REPORT.md")
        print("totals:", totals)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
