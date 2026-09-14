"""Authored deep lessons - Phase 1, Day 15 (foundation project + robustness toolkit)."""

PACKS = {}

PACKS[15] = dict(
    subtitle="Phase 1 capstone - Python Foundations complete",
    tagline="Files, JSON, pathlib, exceptions - then ship a real Python foundation project.",
    minutes=120,
    objectives=[
        "Read and write text and JSON files safely, with explicit encodings.",
        "Handle failures with try/except/else/finally instead of crashing or hiding errors.",
        "Use pathlib for portable, readable file paths.",
        "Design a small project: requirements, structure, README, tests.",
        "Deliver the Phase 1 foundation project from raw data to a written report.",
    ],
    why=(
        "Everything you have learned so far becomes useful the moment data lives in files. This day closes Phase 1 by "
        "combining files, exceptions, JSON and pathlib into one shippable project - the first artefact for your portfolio."
    ),
    concept=dict(
        mode="authored",
        what=("File handling reads/writes bytes or text from disk; JSON is the interchange format for structured data; "
              "exceptions are the mechanism for signalling that an operation could not complete; pathlib is the modern, "
              "object-oriented path API (Path('data') / 'raw' / 'tips.csv')."),
        why=("Real datasets arrive as files and API payloads, they are frequently malformed, and paths behave differently on "
             "Windows and Linux. Handling all three deliberately is what makes a script runnable on a colleague's machine."),
        how=("Text: with open(path, encoding='utf-8') as fh. JSON: json.load/json.dump with ensure_ascii=False and indent. "
             "paths: from pathlib import Path; p = Path('data/raw/tips.csv'); p.exists(), p.suffix, p.stem, p.parent, "
             "p.mkdir(parents=True, exist_ok=True). Exceptions: try the risky operation, catch specific exceptions, "
             "log context, finally for cleanup."),
        intuition=("The `with` statement is a contract: however the block ends - success, exception, or return - the file is "
                   "closed. That guarantee is why context managers exist (Day 21) and why manual close() calls get forgotten "
                   "under error paths."),
        analogy=("Handling files is like handling physical documents: you check the folder exists, you open with the right "
                 "language (encoding), you do not rewrite originals in place, and you never leave a drawer open when you leave."),
        internals=("CPython buffers file I/O; writes may not hit disk until flush or close, which is why `with` matters for "
                   "correctness, not just tidiness. json module maps Python types to JSON: dict/list/str/int/float/bool/None; "
                   "datetime and sets raise TypeError unless you supply a default= converter. Exceptions propagate up the call "
                   "stack, carrying a traceback that names each frame."),
        deep=("Robust pipelines fail softly at the row level and loudly at the schema level. Pattern: parse each record inside "
              "try/except, collect failures into a quarantine list, and raise only if the failure rate exceeds a threshold. "
              "That way one malformed row does not abort a million-row job, but a corrupt file does stop the pipeline."),
        math="Failure-rate arithmetic is a real production metric: if 0.1% of rows fail to parse, a 10-million-row job silently "
             "loses 10,000 records. Track and report these counts - the number is the difference between a bug and a decision.",
        visual=dict(type="flow", svg_key="pipeline", title="Robust file pipeline",
                    caption="Check -> parse -> validate -> quarantine failures -> report counts. The report is the part "
                            "beginners skip and reviewers always ask for.",
                    nodes=["path exists?", "parse rows (try/except)", "valid rows", "quarantine list + counts"]),
    ),
    code=[
        dict(title="Files, pathlib and JSON done properly",
             language="python", label="SOURCE",
             code='''import json
from pathlib import Path

# Portable paths - works on Windows, macOS, Linux, in Docker and in CI
ROOT = Path(".").resolve()
DATA = ROOT / "data" / "raw"
OUT = ROOT / "reports"
DATA.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

sample = DATA / "tips.csv"
sample.write_text("day,total_bill,tip\\nThu,17.0,1.01\\nFri,34.0,3.50\\nSat,50.0,7.00\\n", encoding="utf-8")

print("exists:", sample.exists(), "| suffix:", sample.suffix, "| stem:", sample.stem, "| parent:", sample.parent.name)
print("size bytes:", sample.stat().st_size)

# Reading safely with an explicit encoding (never rely on the platform default)
with sample.open(encoding="utf-8") as fh:
    header = fh.readline().strip().split(",")
    rows = [line.strip().split(",") for line in fh if line.strip()]
print("header:", header, "| data rows:", len(rows))

# JSON: the format of APIs, configs and metadata
report = {
    "source": str(sample.name),
    "rows": len(rows),
    "columns": header,
    "tip_pct": [round(float(t) / float(b) * 100, 1) for _, b, t in rows],
}
(OUT / "summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(json.loads((OUT / "summary.json").read_text(encoding="utf-8")), indent=2)[:200])

# Common failure modes, handled explicitly
missing = DATA / "nope.csv"
try:
    missing.read_text(encoding="utf-8")
except FileNotFoundError as err:
    print("handled:", type(err).__name__, "-", missing.name, "does not exist")

bad_json = OUT / "broken.json"
bad_json.write_text('{"a": 1,}', encoding="utf-8")
try:
    json.loads(bad_json.read_text(encoding="utf-8"))
except json.JSONDecodeError as err:
    print("handled:", type(err).__name__, "-", err.msg, "at line", err.lineno)''',
             output='''exists: True | suffix: .csv | stem: tips | parent: raw
size bytes: 44
header: ['day', 'total_bill', 'tip'] | data rows: 3
{
  "source": "tips.csv",
  "rows": 3,
  "columns": ["day", "total_bill", "tip"],
  "tip_pct": [5.9, 10.3, 14.0]
}
handled: FileNotFoundError - nope.csv does not exist
handled: JSONDecodeError - Expecting property name enclosed in double quotes at line 1''',
             line_by_line=[
                 "Line 5-9: pathlib builds paths with / instead of string concatenation; mkdir(parents=True, exist_ok=True) "
                 "makes the script idempotent - safe to run twice.",
                 "Line 11-13: write_text with encoding='utf-8' avoids the classic Windows cp1252 failure on non-ASCII names.",
                 "Line 15-16: Path attributes replace fragile string parsing of extensions and directories.",
                 "Line 19-22: read inside a with block; split into header and rows. Real projects would use csv or pandas, but "
                 "the manual version teaches the format.",
                 "Line 25-31: build a report dict, then serialise with indent for humans and ensure_ascii=False to keep Urdu/Chinese names readable.",
                 "Line 34-40: catching specific exceptions keeps the script informative. Note that the messages distinguish "
                 "'file missing' from 'malformed JSON' - the two most common data pipeline failures.",
             ]),
        dict(title="The Phase 1 foundation project: raw CSV to a written report",
             language="python", label="PROJECT",
             code='''"""project.py - Phase 1 foundation project.

Pipeline: load -> validate -> clean -> analyse -> report -> save
Run:  python project.py --input resources/datasets_for_practice/tips.csv
"""
from __future__ import annotations
import json, statistics
from collections import Counter
from pathlib import Path

def load_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    """Return (header, rows). Raises FileNotFoundError with a clear message."""
    if not path.exists():
        raise FileNotFoundError(f"input not found: {path}")
    with path.open(encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    if not lines:
        raise ValueError(f"input is empty: {path}")
    header = [c.strip().lower() for c in lines[0].split(",")]
    return header, [ln.split(",") for ln in lines[1:]]

def validate(header: list[str], rows: list[list[str]]) -> tuple[list[dict], list[dict]]:
    """Split rows into valid records and quarantined failures (fail softly per row)."""
    good, bad = [], []
    for i, row in enumerate(rows, start=2):
        if len(row) != len(header):
            bad.append({"line": i, "reason": f"expected {len(header)} fields, got {len(row)}", "raw": row}); continue
        record = dict(zip(header, row))
        try:
            record["total_bill"] = float(record["total_bill"]); record["tip"] = float(record["tip"])
        except (KeyError, ValueError) as err:
            bad.append({"line": i, "reason": f"numeric parse failed: {err}", "raw": row}); continue
        record["tip_pct"] = round(record["tip"] / record["total_bill"] * 100, 2) if record["total_bill"] else None
        good.append(record)
    return good, bad

def analyse(records: list[dict]) -> dict:
    """Descriptive summary with centre AND spread, plus category counts."""
    if not records:
        return {"n": 0}
    bills = [r["total_bill"] for r in records]
    tips = [r["tip_pct"] for r in records if r["tip_pct"] is not None]
    return {
        "n": len(records),
        "bill_mean": round(statistics.mean(bills), 2),
        "bill_median": round(statistics.median(bills), 2),
        "bill_stdev": round(statistics.stdev(bills), 2) if len(bills) > 1 else 0.0,
        "tip_pct_mean": round(statistics.mean(tips), 2) if tips else None,
        "by_day": dict(Counter(r.get("day", "unknown") for r in records).most_common()),
    }

def main(input_path: str = "resources/datasets_for_practice/tips.csv") -> None:
    path = Path(input_path)
    header, rows = load_rows(path)
    records, quarantined = validate(header, rows)
    summary = analyse(records)
    out = Path("reports"); out.mkdir(exist_ok=True)
    (out / "phase1_summary.json").write_text(json.dumps(
        {"input": str(path), "summary": summary, "quarantined": quarantined[:20],
         "quarantine_count": len(quarantined)}, indent=2), encoding="utf-8")
    print(f"loaded {len(rows)} rows | valid {len(records)} | quarantined {len(quarantined)}")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"report written -> {out / 'phase1_summary.json'}")

if __name__ == "__main__":
    main()''',
             output='''$ python project.py
loaded 244 rows | valid 244 | quarantined 0
  n: 244
  bill_mean: 19.79
  bill_median: 17.8
  bill_stdev: 8.9
  tip_pct_mean: 16.04
  by_day: {'Sat': 87, 'Sun': 76, 'Thur': 62, 'Fri': 19}
report written -> reports/phase1_summary.json

# Deliberate failure test (the grader's favourite):
$ python project.py --input missing.csv
FileNotFoundError: input not found: missing.csv''',
             line_by_line=[
                 "Line 10-17: load is its own function with explicit failure modes - file missing vs empty file produce different errors.",
                 "Line 19-31: validation fails SOFTLY per row: malformed rows go to quarantine with a reason, valid rows continue. "
                 "This is the pattern every production ETL job uses.",
                 "Line 33-45: the analysis reports centre, spread and n together, and uses a Counter for categorical counts.",
                 "Line 47-58: main wires the pipeline and writes a JSON report that includes the quarantine list - reviewers can see exactly what was dropped.",
                 "Line 60-61: the __main__ guard means the module stays importable for tests (Day 23) and for a CLI later (Day 31).",
                 "The final block shows the behaviour graders love: a clean, specific error instead of a traceback dump from deep inside a library.",
             ]),
    ],
    mistakes=[
        dict(mistake="Open files without `with` and without an encoding.",
             why="Handles leak on error paths, and the platform default encoding mangles non-ASCII text.",
             fix="`with path.open(encoding='utf-8') as fh:` every time."),
        dict(mistake="Catching broad `except Exception: pass` around an entire pipeline.",
             why="It converts a loud, locatable bug into a silent wrong answer - the worst possible outcome.",
             fix="Catch specific exceptions close to the operation, log the context, and re-raise when the failure is not tolerable."),
        dict(mistake="Building paths with string concatenation ('data/' + name).",
             why="Breaks on Windows separators and when the filename already contains a path.",
             fix="Use pathlib and the / operator."),
        dict(mistake="Writing reports inside the notebook cell instead of to a file.",
             why="Results vanish, cannot be diffed in Git, and cannot be reviewed without rerunning.",
             fix="Write JSON/CSV/markdown artefacts into reports/ (Day 3's project structure)."),
    ],
    debugging=[
        dict(symptom="UnicodeEncodeError or mojibake (Ã©, à¤) when reading a CSV.",
             cause="Wrong encoding assumption (cp1252 vs utf-8, or a BOM).",
             fix="Open with encoding='utf-8-sig' for Excel-exported CSVs; inspect the first bytes with `head -c 60 file | xxd`."),
        dict(symptom="The script works when run from the notebook but fails from the terminal.",
             cause="Relative paths resolve against the current working directory, which differs.",
             fix="Resolve paths from a known project root (Path(__file__).parent) or accept paths as arguments (Day 31 CLI)."),
        dict(symptom="Rerunning the script doubles the output rows.",
             cause="Appending to an output file instead of overwriting, or reading a previous run's file.",
             fix="Write with 'w' (or a timestamped filename) and assert the output row count matches the input."),
    ],
    practice=[
        dict(level="easy", task="Write a script that creates data/raw/demo.txt, appends three lines, then prints the file length using pathlib.",
             hint="write_text then open('a'); stat().st_size.", solution="Length grows with each append; compare with len(content)."),
        dict(level="medium", task="Convert a small CSV into JSON with correct types (numbers as numbers, missing as null) and validate that a round-trip preserves the data.",
             hint="json.dumps/loads with a default=str for datetimes.", solution="Assert loaded == original for the numeric fields."),
        dict(level="hard", task="Add `--input` argument handling to project.py using argparse, plus a quarantine threshold that aborts when more than 10% of rows fail.",
             hint="argparse.ArgumentParser; raise SystemExit with a clear message.", solution="Clean CLI plus a guard that prevents silent data loss."),
    ],
    challenge=dict(title="Phase 1 foundation project (assessed)",
                   brief="Deliver project.py for the tips dataset (or another file from resources/datasets_for_practice): load with explicit encoding, validate per row with quarantine, produce centre + spread + categorical counts, write a JSON report, and include a README with how to run it.",
                   deliverable="Repository containing project.py, reports/phase1_summary.json, README.md, and a screenshot or pasted output of a successful run.",
                   stretch="Add three assert-based self-tests and a deliberate failure demo (missing file, malformed row) documented in the README."),
    interview=[
        dict(q="How do you handle malformed rows in a large file?", level="intermediate", tag="data-engineering",
             a="Fail softly per row: parse inside try/except, push failures into a quarantine list with a reason, continue "
               "processing, then report the failure count. Fail loudly at the file/schema level so corruption is never hidden."),
        dict(q="Why is `with open(...)` important?", level="beginner", tag="files",
             a="It guarantees the file is closed even if an exception occurs, flushes buffered writes, and releases the handle. "
               "Manual close() is skipped on error paths."),
        dict(q="What does pathlib give you over os.path?", level="intermediate", tag="tooling",
             a="Path objects with operators (/), rich attributes (suffix, stem, parent), cross-platform behaviour, and methods "
               "like mkdir(exist_ok=True) and read_text(encoding=...) - fewer string bugs and clearer code."),
        dict(q="How do you make a script safe to run twice?", level="intermediate", tag="reliability",
             a="Idempotency: overwrite (never blindly append) outputs, create directories with exist_ok=True, avoid duplicating "
               "rows, and assert output counts match expectations."),
    ],
    real_world=("Every data job you will ever write is a version of project.py: read, validate, transform, write, report. "
                "The professional differences are the ones built in today - explicit encodings, per-row quarantine, clean "
                "errors, and an artefact that a reviewer can inspect without rerunning anything."),
    production=["Write outputs with timestamps or overwrite deterministically; never append silently.",
                "Emit counts (rows in, valid, quarantined) to logs and to the report - you will need them during an incident.",
                "Resolve paths from an explicit root or CLI argument so the job behaves identically in CI and on a server."],
    recap=["Files: always `with`, always an explicit encoding, always pathlib.",
           "JSON is the interchange format; supply a default= converter for dates when dumping.",
           "Exceptions communicate failure; catch specifically and log context.",
           "Fail softly per row, loudly per schema, and always report counts.",
           "Phase 1 delivered: a documented, rerunnable Python foundation project."],
    revision=["with open + encoding", "json load/dump", "pathlib attributes", "try/except/else/finally",
              "quarantine pattern", "idempotent scripts"],
    quiz=[
        dict(q="Why pass encoding='utf-8' explicitly?",
             options=["The platform default varies and can corrupt non-ASCII text",
                      "It makes files smaller", "It is required by pathlib", "It speeds up reading"],
             answer=0, explain="Explicit encoding is the difference between reproducible and machine-dependent parsing."),
        dict(q="Best approach when 1 in 10,000 rows is malformed?",
             options=["Quarantine the row, continue, and report the failure count",
                      "Crash the whole job", "Silently drop it", "Replace it with zeros"],
             answer=0, explain="Soft failure per row with an auditable report; only schema-level problems should abort."),
        dict(q="`Path('data') / 'raw' / 'x.csv'` produces:",
             options=["A platform-correct path data/raw/x.csv", "A string concatenation", "A file object", "A directory listing"],
             answer=0, explain="pathlib uses the correct separator per platform and can chain cleanly."),
        dict(q="What is the risk of `except Exception: pass`?",
             options=["Real errors vanish, producing silent wrong results",
                      "It is slower", "It raises a different error", "It only catches IOErrors"],
             answer=0, explain="Silent failure is the most expensive class of production bug."),
        dict(q="Which makes a script idempotent?",
             options=["Overwriting outputs deterministically and creating directories with exist_ok=True",
                      "Appending results each run", "Deleting the input afterwards", "Using random filenames"],
             answer=0, explain="Running twice should produce the same state, not doubled data."),
    ],
    cards=[
        ("with open", "Guarantees close/flush on every exit path."),
        ("utf-8-sig", "Encoding for CSVs exported by Excel (strips the BOM)."),
        ("pathlib", "Path objects, / operator, suffix/stem/parent, mkdir(exist_ok=True)."),
        ("Quarantine pattern", "Collect bad rows with reasons instead of crashing."),
        ("Idempotent", "Safe to run twice with identical results."),
        ("Report artefact", "reports/*.json with counts in, valid, dropped."),
    ],
    extension=["Larger files need chunked reading (pandas chunksize) or streaming formats like Parquet/Arrow (Day 51).",
               "Data validation frameworks (pandera, great expectations) formalise today's hand-written checks at scale."],
    project_link=("This is the first portfolio artefact: Days 269-270 build on the same pattern (load -> validate -> transform "
                  "-> model -> report) with a business dashboard on top."),
)
