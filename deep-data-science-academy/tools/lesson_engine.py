"""Lesson engine: turns curriculum rows + authored packs + source material into
the full 24-section lesson JSON that the academy UI renders.

Every lesson carries explicit content labels so the learner always knows what is
source-backed and what the academy added:

    SOURCE       - directly supported by the original Codanics recordings/repo
    EXPLANATION  - academy rewritten teaching explanation
    EXTENSION    - modern/deeper knowledge not adequately covered in the source
    PRACTICE     - hands-on exercises
    PROJECT      - project-based application
    INTERVIEW    - interview preparation
    PRODUCTION   - real-world production knowledge
"""
from __future__ import annotations

import importlib
import os
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)

import phases as phase_mod  # noqa: E402
import source_extract as se  # noqa: E402

DIFFICULTY = {1: "beginner", 2: "intermediate", 3: "advanced"}

# Study prompts used to turn a topic into a real study card when a topic has not
# yet been expanded into an authored deep-dive. These are questions, not claims,
# so nothing is fabricated about the source material.
STUDY_LENSES = [
    ("definition", "Write the one-sentence definition in your own words."),
    ("purpose", "Why does this exist? What breaks without it?"),
    ("inputs/outputs", "What goes in, what comes out, and what type is each?"),
    ("mechanics", "Walk through the steps the computer performs."),
    ("failure modes", "Name two ways this goes wrong and how you would detect it."),
    ("code", "Find the linked repository notebook and run the relevant cell."),
    ("exam-readiness", "Answer aloud: how would you explain this in an interview?"),
]


def load_index() -> dict[int, dict]:
    rows: dict[int, dict] = {}
    for i in range(1, 17):
        mod = importlib.import_module(f"index_data.phase_{i:02d}")
        for row in mod.DAYS:
            day, title, topics, vids, repo, diff, tag = row
            rows[day] = dict(
                day=day,
                title=title,
                topics=[t.strip() for t in topics.split("|") if t.strip()],
                videos=[v.strip() for v in vids.split(",") if v.strip()],
                repo=[r.strip() for r in repo.split(";") if r.strip()],
                difficulty_num=diff,
                tag=tag,
            )
    missing = [d for d in range(1, 276) if d not in rows]
    if missing:
        raise SystemExit(f"curriculum index is missing days: {missing}")
    return rows


def load_packs() -> dict[int, dict]:
    packs: dict[int, dict] = {}
    pack_dir = os.path.join(HERE, "content_packs")
    for fname in sorted(os.listdir(pack_dir)):
        if not fname.endswith(".py") or fname.startswith("_"):
            continue
        mod = importlib.import_module(f"content_packs.{fname[:-3]}")
        for day, pack in getattr(mod, "PACKS", {}).items():
            packs[day] = pack
    return packs


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _keywords(row: dict) -> list[str]:
    words: list[str] = []
    for topic in row["topics"]:
        words.extend([w for w in topic.lower().replace("/", " ").split() if len(w) > 3])
    words.extend([w for w in row["title"].lower().replace("/", " ").split() if len(w) > 3])
    seen, out = set(), []
    for w in words:
        w = w.strip("(),.:;")
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out[:18]


def _short_topics(row: dict) -> list[str]:
    """Topic list used for keyword matching against source material."""
    return [t.split(":")[0].strip() for t in row["topics"]]


def _prereqs(day: int, rows: dict[int, dict]) -> list[str]:
    if day == 1:
        return ["No prior experience required - start here.",
                "A computer with 8 GB RAM (16 GB preferred) and internet access."]
    prev = rows[day - 1]
    phase = phase_mod.phase_for_day(day)
    out = [f"Day {day - 1}: {prev['title']}",
           f"Comfort with the earlier topics of {phase['name']}."]
    if day <= 15:
        out.append("Python installed and a working notebook environment (see Days 4-5).")
    elif day <= 32:
        out.append("Python fundamentals: variables, loops, functions, files (Days 6-15).")
    elif day <= 48:
        out.append("Python + pandas-free array thinking; maths at high-school algebra level.")
    elif day <= 70:
        out.append("NumPy array fundamentals (Days 33-48).")
    elif day <= 88:
        out.append("pandas data wrangling fluency (Days 49-70).")
    elif day <= 134:
        out.append("Comfort reading formulas and graphs; Python + NumPy available.")
    elif day <= 150:
        out.append("Datasets loaded in a warehouse/SQL engine of your choice (SQLite is fine).")
    elif day <= 196:
        out.append("Statistics and linear algebra from Phases 6-7 still fresh.")
    elif day <= 212:
        out.append("Supervised ML workflow, metrics and pipelines (Phase 10).")
    elif day <= 232:
        out.append("Gradient descent, loss functions and vector/matrix maths.")
    elif day <= 258:
        out.append("Deep learning fundamentals and Python packaging basics.")
    elif day <= 268:
        out.append("A trained model or LLM app you want to ship.")
    else:
        out.append("All previous phases - capstones integrate everything.")
    return out


def _why_this_matters(day: int, row: dict, phase: dict) -> str:
    nxt = ", ".join(row["topics"][:3])
    return (
        f"Day {day} sits in Phase {phase['n']} ({phase['name']}), whose goal is: {phase['goal']} "
        f"Today's core material - {nxt} - is the vocabulary the rest of the phase is built on. "
        "Learners who skip the concept and jump to copying code usually stall two weeks later; "
        "the goal here is that you can explain what you did, not just that it ran."
    )


def _labels(row: dict, pack: dict | None) -> dict:
    tag = row["tag"]
    src = ["Course repository notebooks and datasets linked below.",
           "Original lecture recordings linked below (Urdu/Hindi, timestamped)."]
    if tag == "ext":
        src = ["This topic is an ACADEMY EXTENSION: it was not taught in the original six-month recordings.",
               "Where an original recording touches it partially, the closest moment is still linked."]
    elif tag == "mix":
        src = ["Partially covered in the original recordings; the academy adds the missing depth.",
               "Repository notebooks linked below are the original code where available."]
    explanation = [f"Day {row['day']} written walkthrough: concept, intuition, analogy, internals and deep dive."]
    extension = []
    if pack and pack.get("extension"):
        extension = pack["extension"]
    elif tag != "src":
        extension = [
            "Modern practice beyond the original recordings (2024-2026 tooling and conventions).",
            "Production and interview framing for this topic.",
        ]
    return {
        "SOURCE": src,
        "EXPLANATION": explanation,
        "EXTENSION": extension,
        "PRACTICE": ["Exercises, mini challenge and self-check quiz at the end of this lesson."],
        "PROJECT": pack.get("project", ["See the project phase: this lesson feeds Capstone Project 1 and 2."]) if pack else
                   ["This skill is consumed by Capstone Project 1 and 2 (Days 269-272)."],
        "INTERVIEW": ["Interview questions with model answers are listed later in this lesson."],
        "PRODUCTION": ["Production considerations are listed later in this lesson."],
    }


def _guided_concept(row: dict) -> dict:
    topic_cards = []
    for topic in row["topics"]:
        topic_cards.append({
            "topic": topic,
            "prompts": [f"{label}: {question}" for label, question in STUDY_LENSES],
        })
    return {
        "mode": "guided",
        "what": f"{row['title']} - a guided source lesson. The topic list below is the exact scope "
                f"covered by the original recordings and repository notebooks linked in this lesson.",
        "why": f"Because every downstream day assumes this vocabulary. Skipping it creates silent gaps "
               f"that surface later as 'my model does not work and I do not know why'.",
        "how": "Work through the topic cards in order: read the linked source moment, run the linked "
               "repository code, then answer the reflection prompts in your own words before moving on.",
        "intuition": "Treat each topic as a question the instructor was answering. Find the question, "
                     "then the answer becomes memorable.",
        "analogy": "Building this phase is like learning to drive: watching is not enough, and neither is "
                   "memorising the manual. You need wheel time on real datasets.",
        "internals": "Use the linked notebooks to see real implementations, then step one level deeper: "
                     "for each library call, ask what data structure and loops it replaces.",
        "visual": "Sketch the pipeline of today's topic yourself: inputs -> processing -> outputs. "
                  "The diagram section contains a generated structure you can copy.",
        "deep": "Advanced learners: implement the smallest possible version of today's topic from scratch "
                "(no library) before using the library version.",
        "math": "Identify which quantity in today's topic is being summed, averaged, or maximised. "
                "That quantity is the maths to understand first.",
        "topic_cards": topic_cards,
    }


def _guided_quiz(row: dict) -> list[dict]:
    """Topic-scoped self-check. These are recall/verification items, not invented facts."""
    items = []
    for topic in row["topics"][:4]:
        items.append({
            "q": f"Before moving on, can you do all three for '{topic}'? (a) define it in one sentence, "
                 f"(b) write or run code that demonstrates it, (c) name one way it fails.",
            "options": ["Yes - all three confidently", "Yes to (a) and (b), shaky on (c)",
                        "Only (a) definition", "Not yet - I will rewatch the linked moment"],
            "answer": 0,
            "explain": "Mastery check for this topic. If you are not at the first option, revisit the linked "
                       "timestamped lecture segment and the repository notebook before continuing.",
            "type": "self-check",
        })
    items.append({
        "q": f"What is the correct label for today's core content?",
        "options": [
            "SOURCE + EXPLANATION: taught in the original course, rewritten here" if row["tag"] == "src"
            else "EXTENSION: added by the academy because the original course was thin here" if row["tag"] == "ext"
            else "MIXED: partially in the original course, extended by the academy",
            "All of it is brand-new academy invention",
            "None of it relates to the original course",
            "It is only an interview question bank",
        ],
        "answer": 0,
        "explain": "Traceability matters: you should always know what came from your mentor's course and what "
                   "the academy added.",
        "type": "traceability",
    })
    return items


def _guided_flashcards(row: dict) -> list[dict]:
    cards = []
    for topic in row["topics"][:5]:
        cards.append({"front": f"Define: {topic}", "back": "One-sentence definition + one real use case, in your own words.", "tag": "recall"})
    cards.append({"front": f"Day {row['day']} in one line", "back": row["title"], "tag": "context"})
    return cards




def _starter_example(row: dict) -> dict:
    """Runnable lab harness for a lesson with no matching repository code."""
    topics = "".join(f'    "{t}",\n' for t in row["topics"][:4])
    code = (
        f'"""Lab starter for Day {row["day"]}: {row["title"]}\n\n'
        'No original notebook matched this lesson closely enough to quote, so work\n'
        'through the source links in this lesson using this harness.\n"""\n'
        'import platform, sys\n'
        'import numpy as np\n\n'
        'print("python :", sys.version.split()[0], "|", platform.system())\n'
        'print("numpy  :", np.__version__)\n\n'
        'RANDOM_STATE = 42\n'
        'rng = np.random.default_rng(RANDOM_STATE)     # reproducible experiments\n\n'
        'checklist = [\n' + topics + ']\n'
        'for i, item in enumerate(checklist, start=1):\n'
        '    print(f"todo {i}: {item}")\n\n'
        '# Keep raw inputs immutable - work on a copy (Day 3 project structure)\n'
        'raw = np.arange(10)\n'
        'work = raw.copy()\n'
        'work[0] = -1\n'
        'print("raw untouched:", raw[0], "| working copy:", work[0])\n'
    )
    return {
        "title": "Lab starter - set up today's practice in a clean environment",
        "language": "python", "code": code,
        "output": "Prints the python/numpy versions, the seeded RNG and today's topic checklist.",
        "line_by_line": [
            "Line 5-6: record the environment so your notes say exactly what produced the outputs.",
            "Line 9-10: seed the RNG - reproducibility is a precondition for comparing your work with the lecture.",
            "Line 12-14: the checklist turns today's topics into explicit, tickable tasks.",
            "Line 16-19: keep raw inputs immutable and work on a copy - the habit from Day 3's structure.",
        ],
        "label": "PRACTICE",
        "notes": ("No repository notebook matched this lesson closely enough to quote, so nothing unrelated is "
                  "attached: use this harness with the source links above."),
    }


def _guided_practice(row: dict) -> list[dict]:
    """Actionable study tasks for a guided lesson. These are instructions to DO
    something with the source material, never invented claims about it."""
    tasks = []
    for topic in row["topics"][:3]:
        tasks.append({
            "level": "easy" if not tasks else "medium",
            "task": f"Definition drill - {topic}. Write a one-sentence definition in your own words, then a second "
                    f"sentence naming what goes in and what comes out.",
            "hint": "If you cannot name the input and the output, rewatch the linked moment before continuing.",
            "solution": "Aim for the shape: '<topic> takes <input>, produces <output>, and exists because <reason>.'",
        })
    repo = (row["repo"] or ["the repository"])[0]
    tasks.append({
        "level": "hard",
        "task": f"Code drill - {repo}. Open it in Jupyter and re-implement the section covering "
                f"{row['topics'][0]} in a fresh notebook without looking at the original, then compare outputs.",
        "hint": "Work cell by cell; when you get stuck, read the original for 20 seconds and close it again.",
        "solution": "You are done when your notebook runs top-to-bottom and reproduces the original's numbers.",
    })
    tasks.append({
        "level": "medium",
        "task": f"Failure drill - {row['topics'][-1]}. Deliberately break the example (wrong dtype, wrong axis, "
                f"duplicate keys or missing values) and record the exact error message and what it teaches you.",
        "hint": "Break one thing at a time so you know which change caused the error.",
        "solution": "Every error you can provoke and explain is one you will recognise in production.",
    })
    return tasks


def _guided_mistakes(row: dict) -> list[dict]:
    return [
        {"mistake": "Watching the lecture without running the repository notebook.",
         "why": "Recognition is not recall: code that looked obvious fails the moment you type it yourself.",
         "fix": "For every topic today, run the linked notebook cell, then retype it from memory in your own file."},
        {"mistake": f"Using {row['topics'][0]} on data whose types or shape you have not printed.",
         "why": "Most failures in this topic are input problems (dtype, shape, missing values) rather than logic errors.",
         "fix": "Print type and shape immediately before the operation; keep that habit for all 275 days."},
    ]


def _guided_debugging(row: dict) -> list[dict]:
    return [
        {"symptom": "The linked notebook cell raises ModuleNotFoundError or ImportError.",
         "cause": "Wrong kernel/environment selected, or the library is not installed in the active environment.",
         "fix": "Print sys.executable in the notebook and install into that environment (Day 4)."},
        {"symptom": "Your output differs from the recording even though the code looks identical.",
         "cause": "Library version differences, a changed default argument, or unseeded randomness.",
         "fix": "Pin versions (requirements.txt), set a random seed, and compare dtypes and shapes, not just values (Day 5)."},
    ]


# --------------------------------------------------------------------------- #
# Main renderer
# --------------------------------------------------------------------------- #
def render_lesson(row: dict, pack: dict | None, transcripts: dict, code_assets: list[dict]) -> dict:
    day = row["day"]
    phase = phase_mod.phase_for_day(day)
    keywords = _keywords(row)
    video_idxs = [v for v in row["videos"] if v.isdigit()]
    source_videos = se.match_transcript_segments(transcripts, video_idxs, keywords, limit=4)
    source_code = se.match_code_assets(code_assets, keywords, row["repo"], limit=3)

    # video metadata even when no segment matched
    video_meta = []
    for idx in video_idxs[:6]:
        rec = transcripts.get(str(idx))
        if rec:
            video_meta.append({
                "video_idx": rec["idx"], "title": rec["title"], "date": rec["date"],
                "url": f"https://www.youtube.com/watch?v={rec['video_id']}",
            })

    authored = pack is not None
    concept = pack["concept"] if authored and "concept" in pack else _guided_concept(row)

    def _cards(items: list) -> list[dict]:
        out = []
        for c in items:
            if isinstance(c, (list, tuple)):
                out.append({"front": c[0], "back": c[1], "tag": c[2] if len(c) > 2 else "recall"})
            else:
                out.append({"front": c.get("front", ""), "back": c.get("back", ""), "tag": c.get("tag", "recall")})
        return out

    def _practice(items: list) -> list[dict]:
        out = []
        for p in items:
            if isinstance(p, (list, tuple)):
                p = dict(zip(("level", "task", "hint", "solution"), p))
            out.append({"level": p.get("level", "medium"), "task": p.get("task", ""),
                        "hint": p.get("hint", ""), "solution": p.get("solution", "")})
        return out

    if pack and pack.get("code"):
        code_examples = pack["code"]
    elif source_code:
        code_examples = [
            {"title": f"Reference implementation - {a['path'].split('/')[-1]}",
             "language": "python", "code": a["code"],
             "output": "Run the cell to reproduce this notebook's own output.",
             "line_by_line": [], "label": "SOURCE",
             "notes": f"Real code from your repository: {a['path']} (heading: {a['heading'][:80]})"}
            for a in source_code
        ]
    else:
        code_examples = [_starter_example(row)]

    lesson: dict[str, Any] = {
        "day": day,
        "phase": {"n": phase["n"], "name": phase["name"], "start": phase["start"], "end": phase["end"],
                  "goal": phase["goal"], "source_level": phase["source_level"], "source_note": phase["source_note"]},
        "title": row["title"],
        "subtitle": (pack or {}).get("subtitle", f"{phase['name']} - Day {day} of 275"),
        "tagline": (pack or {}).get("tagline", ""),
        "difficulty": DIFFICULTY[row["difficulty_num"]],
        "est_minutes": (pack or {}).get("minutes", 60 + 15 * row["difficulty_num"]),
        "depth": "full" if authored else "guided",
        "tag": row["tag"],
        "keywords": keywords,
        "topics": row["topics"],
        "prerequisites": (pack or {}).get("prerequisites", _prereqs(day, load_index())),
        "learning_objectives": (pack or {}).get("objectives", [
            f"Explain {t} without notes." for t in row["topics"][:3]
        ] + [
            f"Apply {row['topics'][0]} to a small dataset in code.",
            "List the common mistakes for today's topics and how to detect them.",
        ]),
        "why_this_matters": (pack or {}).get("why", _why_this_matters(day, row, phase)),
        "concept": concept,
        "labels": _labels(row, pack),
        "source_trace": {
            "phase_note": phase["source_note"],
            "videos": video_meta,
            "moments": source_videos,
            "code": source_code,
            "repo_paths": row["repo"],
            "traceability": ("Every claim about the original course in this lesson is traceable to a linked "
                             "recording or repository file. Academy extensions are labelled EXTENSION."),
        },
        "visual": (pack or {}).get("visual", {
            "type": "pipeline",
            "title": f"Day {day} pipeline",
            "caption": "INPUT -> PROCESSING -> OUTPUT is the universal shape of the work in this phase.",
            "svg_key": "pipeline",
            "nodes": ["Raw data", row["title"], "Verified result", "Notes for revision"],
        }),
        "code_examples": code_examples,
        "common_mistakes": (pack or {}).get("mistakes", []) or _guided_mistakes(row),
        "debugging": (pack or {}).get("debugging", []) or _guided_debugging(row),
        "practice": _practice((pack or {}).get("practice", [])) or _guided_practice(row),
        "mini_challenge": (pack or {}).get("challenge", {
            "title": f"Day {day} mini challenge",
            "brief": f"Rebuild the core idea of '{row['topics'][0]}' on a dataset of your own choice and write "
                     f"five lines explaining what you did and why.",
            "deliverable": "A notebook cell (or script) + a 5-line markdown explanation committed to your repo.",
            "stretch": "Explain it to a non-technical friend in under 90 seconds.",
        }),
        "interview_questions": (pack or {}).get("interview", [
            {"q": f"What is {row['topics'][0]}, and where would you use it in a real project?",
             "a": "Answer using: definition -> why it exists -> one concrete project example -> one limitation. "
                  "The limitation is what separates senior answers.",
             "level": DIFFICULTY[row["difficulty_num"]], "tag": "concept"},
            {"q": f"Describe a bug you would expect when misusing {row['topics'][-1]}.",
             "a": "Name the symptom, the underlying cause, and the check you would run to confirm it.",
             "level": "intermediate", "tag": "debugging"},
        ]),
        "real_world": (pack or {}).get("real_world",
            f"Roles that use {row['topics'][0]} daily: data analyst, data scientist and ML engineer. "
            f"In industry the tool matters less than the judgement about when to use it - that judgement is what "
            f"interviews and performance reviews reward."),
        "production": (pack or {}).get("production", [
            "Version the inputs and the code, not just the output.",
            "Make the step rerunnable: a script you are afraid to re-run is a liability.",
            "Log what happened (counts in, counts out) so failures are detectable.",
        ]),
        "recap": (pack or {}).get("recap", [f"Today covered: {', '.join(row['topics'])}.",
                                            "You should be able to explain each topic in one sentence and show one code example."]),
        "quiz": (pack or {}).get("quiz", []) or _guided_quiz(row),
        "flashcards": _cards((pack or {}).get("cards", [])) or _guided_flashcards(row),
        "revision_points": (pack or {}).get("revision", []),
        "revision": {
            "one_liner": (pack or {}).get("tagline", row["title"]),
            "must_remember": (pack or {}).get("revision", [t for t in row["topics"][:3]]),
            "code_recall": "Type today's key code from memory, then compare with the lesson.",
            "teach_back": f"Explain {row['title']} to an imaginary junior in 3 minutes.",
        },
        "project_link": (pack or {}).get("project_link",
            "Capstone Project 1 (analytics + ML dashboard) and Project 2 (Document Intelligence RAG) reuse this skill."),
        "prev_day": day - 1 if day > 1 else None,
        "next_day": day + 1 if day < 275 else None,
        "nav": {"phase_first": phase["start"], "phase_last": phase["end"]},
    }
    return lesson


def render_curriculum(rows: dict[int, dict]) -> dict:
    phases = []
    for p in phase_mod.PHASES:
        pdays = [rows[d] for d in range(p["start"], p["end"] + 1)]
        phases.append({
            **{k: v for k, v in p.items()},
            "count": len(pdays),
            "days": [{
                "day": r["day"], "title": r["title"], "difficulty": DIFFICULTY[r["difficulty_num"]],
                "topics": r["topics"], "tag": r["tag"],
            } for r in pdays],
        })
    return {
        "title": "Deep Data Science & AI Academy",
        "total_days": 275,
        "phases": phases,
        "generated_by": "tools/build_content.py",
        "source_legend": {
            "SOURCE": "Directly supported by the original Codanics six-month mentorship recordings/repository.",
            "EXPLANATION": "Academy rewritten teaching explanation.",
            "EXTENSION": "Modern/deeper knowledge not adequately covered in the original course.",
            "PRACTICE": "Hands-on exercises.",
            "PROJECT": "Project-based application.",
            "INTERVIEW": "Interview preparation.",
            "PRODUCTION": "Real-world production knowledge.",
        },
    }
