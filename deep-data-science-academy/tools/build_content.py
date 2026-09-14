#!/usr/bin/env python3
"""Build the academy content: curriculum index, 275 lesson files, and the
aggregate quiz / flashcard / interview / search indices.

Usage:
    python3 tools/build_content.py            # full build
    python3 tools/build_content.py --days 1 32   # rebuild a range only

Content is NEVER loaded into the browser in bulk: the UI fetches
content/day_NNN.json on demand and only holds this light index in memory.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACADEMY = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import lesson_engine as engine  # noqa: E402
import source_extract as se  # noqa: E402

CONTENT_DIR = os.path.join(ACADEMY, "content")
ASSETS_DIR = os.path.join(ACADEMY, "assets")


def write_json(path: str, payload: dict | list) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
    return os.path.getsize(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", nargs=2, type=int, default=None, help="rebuild only this inclusive range")
    args = ap.parse_args()

    rows = engine.load_index()
    packs = engine.load_packs()
    transcripts = se.build_transcript_cache()
    code_assets = se.build_code_cache()["assets"]

    print(f"index rows: {len(rows)} | authored packs: {len(packs)}")

    days = range(1, 276)
    if args.days:
        days = range(args.days[0], args.days[1] + 1)

    quizzes, flashcards, interview, search = [], [], [], []
    for day in days:
        lesson = engine.render_lesson(rows[day], packs.get(day), transcripts, code_assets)
        size = write_json(os.path.join(CONTENT_DIR, f"day_{day:03d}.json"), lesson)
        if day == 1 or not args.days:
            pass
        for i, q in enumerate(lesson["quiz"]):
            quizzes.append({"id": f"d{day}q{i+1}", "day": day, "phase": lesson["phase"]["n"],
                            "title": lesson["title"], "q": q["q"], "options": q["options"],
                            "answer": q["answer"], "explain": q.get("explain", ""),
                            "difficulty": lesson["difficulty"], "type": q.get("type", "mcq")})
        for i, c in enumerate(lesson["flashcards"]):
            flashcards.append({"id": f"d{day}f{i+1}", "day": day, "phase": lesson["phase"]["n"],
                               "title": lesson["title"], "front": c["front"], "back": c["back"],
                               "tag": c.get("tag", "recall")})
        for i, q in enumerate(lesson["interview_questions"]):
            interview.append({"id": f"d{day}i{i+1}", "day": day, "phase": lesson["phase"]["n"],
                              "domain": lesson["phase"]["name"], "title": lesson["title"],
                              "q": q["q"], "a": q["a"], "level": q.get("level", lesson["difficulty"]),
                              "tag": q.get("tag", "concept")})
        if not args.days or day % 25 == 0:
            search.append({
                "day": day, "title": lesson["title"], "phase": lesson["phase"]["n"],
                "phase_name": lesson["phase"]["name"], "difficulty": lesson["difficulty"],
                "depth": lesson["depth"], "tag": lesson["tag"], "topics": lesson["topics"],
                "keywords": lesson["keywords"][:12],
            })
        print(f"  day {day:3d} -> {size/1024:5.1f} KB  [{lesson['depth']:7s}] {lesson['title'][:58]}")

    if not args.days:
        write_json(os.path.join(ACADEMY, "curriculum.json"), engine.render_curriculum(rows))
        # rebuild the full search index from every written lesson
        search = []
        for day in range(1, 276):
            with open(os.path.join(CONTENT_DIR, f"day_{day:03d}.json"), encoding="utf-8") as fh:
                lesson = json.load(fh)
            search.append({
                "day": day, "title": lesson["title"], "phase": lesson["phase"]["n"],
                "phase_name": lesson["phase"]["name"], "difficulty": lesson["difficulty"],
                "depth": lesson["depth"], "tag": lesson["tag"], "topics": lesson["topics"],
                "keywords": lesson["keywords"][:14],
                "objectives": lesson["learning_objectives"][:3],
            })
        print(f"quiz items: {len(quizzes)} | flashcards: {len(flashcards)} | interview Qs: {len(interview)}")
        print(f"curriculum.json {os.path.getsize(os.path.join(ACADEMY, 'curriculum.json'))/1024:.1f} KB")

    write_json(os.path.join(ACADEMY, "quizzes", "quiz_bank.json"), quizzes)
    write_json(os.path.join(ACADEMY, "flashcards", "flashcard_bank.json"), flashcards)
    write_json(os.path.join(ACADEMY, "interview", "interview_bank.json"), interview)
    write_json(os.path.join(ASSETS_DIR, "search_index.json"), search)
    print("build complete")


if __name__ == "__main__":
    main()
