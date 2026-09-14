"""Extract real source assets from the mentor's materials.

Two sources are read directly (never invented):

1. The 274 lecture transcripts archived in ALL_275_TRANSCRIPTS.zip. Every
   transcript contains timestamped lines such as ``[12:34] text``. We index
   those lines so a lesson can deep-link to the exact moment a topic is taught.

2. The course repository itself: every .ipynb notebook and .py file. Real code
   cells are pulled out and attached to lessons, with the file path as citation.

Nothing here fabricates content. If a match is not found, the lesson simply has
no source citation for that item.
"""
from __future__ import annotations

import json
import os
import re
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ACADEMY = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(ACADEMY)
TRANSCRIPT_ZIP = os.path.join(REPO_ROOT, "ALL_275_TRANSCRIPTS.zip")
CACHE_DIR = os.path.join(HERE, "cache")
TRANSCRIPT_CACHE = os.path.join(CACHE_DIR, "transcripts.json")
CODE_CACHE = os.path.join(CACHE_DIR, "code_assets.json")

SKIP_DIR_PARTS = (".git", "__pycache__", "node_modules", ".vscode")

STOPWORDS = set("""a an and or the of to in is are was were for with on at by from as it its this that these those
you your we our they their he she his her not no but if then else when while do does did done have has had can could
will would should may might must be been being i me my mine us them there here what which who whom whose how why
than too very s t just don now use used using into over under again further once only own same so than both each
few more most other some such any all about above after before below between during out off up down part series
complete course data science ai learning learn lecture day days video please watch like share subscribe channel""".split())


def _tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z][a-z0-9+#_.\-]{2,}", text.lower()) if w not in STOPWORDS]


# --------------------------------------------------------------------------- #
# Transcripts
# --------------------------------------------------------------------------- #
TS_LINE = re.compile(r"^\[(\d{1,2}):(\d{2})(?::(\d{2}))?\]\s*(.*)$")


def _parse_transcript(body: str) -> list[tuple[int, str]]:
    segs: list[tuple[int, str]] = []
    for line in body.splitlines():
        m = TS_LINE.match(line.strip())
        if not m:
            continue
        a, b, c, text = m.groups()
        secs = int(a) * 3600 + int(b) * 60 + int(c) if c else int(a) * 60 + int(b)
        text = text.strip()
        if len(text) >= 8:
            segs.append((secs, text))
    # de-duplicate consecutive repeats produced by the ASR export
    out, seen = [], set()
    for secs, text in segs:
        key = text[:60]
        if key in seen:
            continue
        seen.add(key)
        out.append((secs, text))
    return out


def build_transcript_cache(force: bool = False) -> dict:
    if os.path.exists(TRANSCRIPT_CACHE) and not force:
        with open(TRANSCRIPT_CACHE, encoding="utf-8") as fh:
            return json.load(fh)

    os.makedirs(CACHE_DIR, exist_ok=True)
    index = json.load(open(os.path.join(HERE, "source_transcripts.json"), encoding="utf-8"))
    by_name = {rec["fn"].split("/")[-1]: rec for rec in index}

    result: dict[str, dict] = {}
    with zipfile.ZipFile(TRANSCRIPT_ZIP) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as fh:
            raw = fh.read().decode("utf-8", errors="replace")

    parts = re.split(r"^===== <ZipInfo filename='([^']+)'[^>]*> =====$", raw, flags=re.M)
    for i in range(1, len(parts), 2):
        fname = parts[i].split("/")[-1]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        rec = by_name.get(fname, {})
        segs = _parse_transcript(body)
        result[str(rec.get("idx", fname))] = {
            "idx": rec.get("idx"),
            "date": rec.get("date"),
            "title": rec.get("title"),
            "video_id": rec.get("video_id"),
            "segments": segs,
        }

    with open(TRANSCRIPT_CACHE, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False)
    return result


def search_terms(keywords: list[str], phrases: list[str] | None = None) -> list[tuple[str, float]]:
    """Expand English keywords into searchable terms, including the Devanagari
    forms the ASR produced for the same technical terms. Returns (term, weight)."""
    terms: dict[str, float] = {}

    def add(term: str, weight: float) -> None:
        term = term.strip().lower()
        if len(term) < 3:
            return
        terms[term] = max(terms.get(term, 0.0), weight)

    all_words: list[str] = []
    for kw in list(keywords) + list(phrases or []):
        w = kw.strip().lower().strip("(),.:;'\"")
        if len(w) > 2:
            all_words.append(w)
            add(w, 1.0)                                  # match the English word itself
            if w.endswith("s") and len(w) > 4:
                add(w[:-1], 0.9)                         # joins -> join
    # multi-word phrases first (more distinctive)
    for i in range(len(all_words) - 1):
        pair = f"{all_words[i]} {all_words[i + 1]}"
        add(pair, 1.4)
    for w in all_words:
        if w in TRANSLIT:
            for form in TRANSLIT[w]:
                add(form, 1.6)
    return sorted(terms.items(), key=lambda kv: -kv[1])


def match_transcript_segments(transcripts: dict, video_idxs: list[str], keywords: list[str],
                              phrases: list[str] | None = None, limit: int = 4) -> list[dict]:
    """Return the best timestamped moments for a lesson, as genuine quotations."""
    if not video_idxs:
        return []
    terms = search_terms(keywords, phrases)
    if not terms:
        return []
    scored: list[tuple[float, str, int, str, list[str]]] = []
    for idx in video_idxs:
        rec = transcripts.get(str(idx))
        if not rec:
            continue
        for secs, text in rec["segments"]:
            low = text.lower()
            matched = [t for t, _w in terms if t in low]
            if not matched:
                continue
            weight = sum(w for t, w in terms if t in low)
            score = weight / (1 + len(text) / 130)
            scored.append((score, idx, secs, text, matched))
    scored.sort(key=lambda x: -x[0])
    out, per_video = [], defaultdict(int)
    for score, idx, secs, text, matched in scored:
        if per_video[idx] >= 2:
            continue
        if any(text[:50] == o["quote"][:50] for o in out):
            continue
        per_video[idx] += 1
        rec = transcripts[idx]
        ts = (f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}" if secs >= 3600
              else f"{secs // 60:02d}:{secs % 60:02d}")
        out.append({
            "video_idx": int(idx),
            "video_title": rec["title"],
            "date": rec["date"],
            "video_url": f"https://www.youtube.com/watch?v={rec['video_id']}",
            "timestamp": ts,
            "seconds": secs,
            "deep_link": f"https://www.youtube.com/watch?v={rec['video_id']}&t={secs}s",
            "quote": text[:400],
            "matched_terms": matched[:6],
            "match_score": round(float(score), 4),
        })
        if len(out) >= limit:
            break
    if not out:
        # Honest fallback: no keyword hit, so point at the opening explanation of the
        # mapped lecture and label it as an intro, not as a topic match.
        for idx in video_idxs:
            rec = transcripts.get(str(idx))
            if not rec:
                continue
            for secs, text in rec["segments"]:
                if 60 <= secs <= 900 and len(text) > 40:
                    ts = (f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}" if secs >= 3600
                          else f"{secs // 60:02d}:{secs % 60:02d}")
                    out.append({
                        "video_idx": int(idx), "video_title": rec["title"], "date": rec["date"],
                        "video_url": f"https://www.youtube.com/watch?v={rec['video_id']}",
                        "timestamp": ts, "seconds": secs,
                        "deep_link": f"https://www.youtube.com/watch?v={rec['video_id']}&t={secs}s",
                        "quote": text[:400], "matched_terms": [], "fallback": True,
                        "match_score": 0.0,
                    })
                    break
            if out:
                break
    return out


# --------------------------------------------------------------------------- #
# Transcript matching dictionary
# The mentor teaches in Urdu/Hindi while saying English technical terms, and the
# ASR engine writes those terms in Devanagari script (e.g. "pandas" -> "पांडा").
# These spellings were verified against the real transcript corpus, so a lesson's
# "source moments" are genuine quotations with working deep links.
# --------------------------------------------------------------------------- #
TRANSLIT: dict[str, list[str]] = {
    "pandas": ["पांडा"], "numpy": ["नम पाई", "नमपाई"], "python": ["पाइथन"],
    "data": ["डाटा", "डेटा"], "dataframe": ["डाटाफ्रेम", "डेटा फ्रेम"],
    "machine": ["मशीन"], "learning": ["लर्निंग"], "deep": ["डीप"],
    "statistics": ["स्टेटिस्टिक्स", "स्टेटिस्टिक"], "probability": ["प्रोबेबिलिटी"],
    "distribution": ["डिस्ट्रिब्यूशन", "डिस्ट्रीब्यूशन"], "normal": ["नॉर्मल"],
    "hypothesis": ["हाइपोथेसिस", "हाइपोथीसिस"], "value": ["वैल्यू", "वैलू"],
    "correlation": ["कोरिलेशन", "कोरलेशन"], "regression": ["रिग्रेशन"],
    "classification": ["क्लासिफिकेशन", "क्लैसिफिकेशन"], "clustering": ["क्लस्टरिंग"],
    "decision": ["डिसीजन", "डिसिजन"], "tree": ["ट्री"], "random": ["रैंडम", "रेंडम"],
    "forest": ["फॉरेस्ट", "फारेस्ट"], "gradient": ["ग्रेडिएंट"], "descent": ["डिसेंट"],
    "activation": ["एक्टिवेशन", "एक्टिवेसन"], "dropout": ["ड्रॉप आउट"],
    "convolution": ["कन्वोल्यूशन", "कॉन्वोल्यूशन"], "vision": ["विजन"],
    "transfer": ["ट्रांसफर"], "time": ["टाइम"], "series": ["सीरीज", "सीरिज"],
    "sentiment": ["सेंटिमेंट"], "hierarchical": ["हायरार्किकल", "हाइरार्किकल"],
    "optics": ["ऑप्टिक्स"], "gmm": ["जीएमएम"], "svd": ["एसवीडी"], "tsne": ["टी एस एन ई"],
    "anomaly": ["एनोमली", "अनोमली"], "sarima": ["सारिमा", "सरिमा"],
    "arima": ["अरीमा"], "prophet": ["प्रोफेट", "प्रॉफेट"],
    "calculate": ["कैलकुलेट", "कैल्कुलेट"], "dax": ["डेक्स", "डैक्स"],
    "power": ["पावर", "पॉवर"], "tableau": ["टेबलो", "टेबलाउ"], "excel": ["एक्सेल", "एक्सल"],
    "streamlit": ["स्ट्रीमलिट", "स्ट्रीमलाइट"], "flask": ["फ्लास्क"],
    "fastapi": ["फास्ट एपीआई"], "langchain": ["लैंग चेन", "लैंगचेन"], "rag": ["रैग"],
    "llm": ["एलएलएम"], "prompt": ["प्रॉम्प्ट", "प्रांप्ट"], "cloud": ["क्लाउड"],
    "deployment": ["डेप्लॉयमेंट", "डिप्लॉयमेंट"], "mlops": ["एमएल ऑप्स", "एमएलऑप्स"],
    "engineer": ["इंजीनियरिंग", "इंजीनियर"], "feature": ["फीचर", "फ़ीचर"],
    "hyperparameter": ["हाइपर पैरामीटर", "हाइपरपैरामीटर"],
    "cross": ["क्रॉस"], "validation": ["वैलिडेशन", "वेलिडेशन"],
    "ensemble": ["एंसेंबल", "एन्सेम्बल"], "boosting": ["बूस्टिंग"], "boost": ["बूस्ट"],
    "overfitting": ["ओवरफिटिंग", "ओवर फिटिंग"], "underfitting": ["अंडरफिटिंग"],
    "confusion": ["कंफ्यूजन", "कन्फ्यूजन"], "matrix": ["मैट्रिक्स", "मेट्रिक्स"],
    "accuracy": ["एक्यूरेसी"], "recall": ["रिकॉल"], "precision": ["प्रिसिजन"],
    "pipeline": ["पाइपलाइन"], "scaling": ["स्केलिंग", "स्केलिं"],
    "missing": ["मिसिंग"], "outlier": ["आउटलायर", "आउट लायर"],
    "vector": ["वेक्टर"], "derivative": ["डेरिवेटिव", "डेरीवेटिव"],
    "integral": ["इंटीग्रल"], "sampling": ["सैंपलिंग", "सैम्पलिंग", "सैंपल"],
    "bootstrap": ["बूटस्ट्रैप"], "neural": ["न्यूरल"], "network": ["नेटवर्क"],
    "transformer": ["ट्रांसफॉर्मर", "ट्रांसफार्मर"], "embedding": ["एंबेडिंग", "एम्बेडिंग"],
    "attention": ["अटेंशन", "अटेन्शन"], "token": ["टोकन"], "tokenizer": ["टोकनाइजर"],
    "git": ["गिट"], "github": ["गिट हब"], "api": ["एपीआई"], "json": ["जेसन"],
    "nlp": ["एनएलपी"], "cnn": ["सीएनएन"], "rnn": ["आरएनएन"], "lstm": ["एलएसटीएम"],
    "gru": ["जी आर यू"], "bert": ["बर्ट"], "gpt": ["जीपीटी"], "pca": ["पीसीए"],
    "knn": ["के एन एन", "केएनएन"], "svm": ["एसवीएम"], "xgboost": ["एक्सजीबूस्ट"],
    "catboost": ["कैट बूस्ट", "कैटबूस्ट"], "lightgbm": ["लाइट जीबीएम", "लाइटजीबीएम"],
    "jupyter": ["जुपिटर"], "colab": ["कोलैब"], "kaggle": ["कैगल"],
    "dashboard": ["डैशबोर्ड"], "sql": ["एसक्यूएल"], "spark": ["स्पार्क"],
    "visualization": ["विजुअलाइजेशन", "विजुअलाइज़ेशन"], "plotting": ["प्लॉटिंग"],
    "plotly": ["प्लॉटली"], "seaborn": ["सीबोर्न", "सीबॉर्न"],
    "matplotlib": ["मैटप्लॉटलिब", "मेटप्लॉटलिब", "मैटप्लॉट"],
    "kmeans": ["के मीन"], "mean": ["मीन"], "median": ["मीडियन"],
    "variance": ["वेरिएंस", "वैरिएंस"], "deviation": ["डेविएशन", "डिविएशन"],
    "percentile": ["परसेंटाइल"], "anova": ["एनोवा"], "manova": ["मैनोवा"],
    "chisquare": ["काई स्क्वायर", "ची स्क्वायर"], "inference": ["इन्फरेंस"],
    "testing": ["टेस्टिंग"], "array": ["अरे", "ऐरे"], "reshape": ["रीशेप"],
    "index": ["इंडेक्स"], "slicing": ["स्लाइसिंग"], "join": ["जॉइन", "ज्वाइन"],
    "merge": ["मर्ज"], "groupby": ["ग्रुप बाय", "ग्रुपबाय"], "filter": ["फिल्टर"],
    "imputation": ["इम्प्यूटेशन"], "encoding": ["एनकोडिंग"], "cleaning": ["क्लीनिंग"],
    "preprocessing": ["प्रीप्रोसेसिंग"],
}

# --------------------------------------------------------------------------- #
# Repository code assets
# --------------------------------------------------------------------------- #
def _iter_repo_files() -> list[str]:
    paths = []
    self_dir = os.path.basename(ACADEMY)
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d != self_dir]   # never cite the academy's own tools
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
        for f in files:
            if f.endswith((".ipynb", ".py")):
                paths.append(os.path.join(root, f))
    return sorted(paths)


def _clean_cell(src: str, max_lines: int = 45) -> str:
    lines = [ln.rstrip() for ln in src.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 2:
        return ""
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["# ... (truncated)"]
    return "\n".join(lines)


def build_code_cache(force: bool = False) -> dict:
    if os.path.exists(CODE_CACHE) and not force:
        with open(CODE_CACHE, encoding="utf-8") as fh:
            return json.load(fh)

    os.makedirs(CACHE_DIR, exist_ok=True)
    assets: list[dict] = []
    for path in _iter_repo_files():
        rel = os.path.relpath(path, REPO_ROOT)
        try:
            if rel.endswith(".ipynb"):
                with open(path, encoding="utf-8", errors="replace") as fh:
                    nb = json.load(fh)
                cells = nb.get("cells", [])
                heading = ""
                for cell in cells:
                    src = "".join(cell.get("source", []))
                    if cell.get("cell_type") == "markdown":
                        first = next((ln.strip("# ").strip() for ln in src.splitlines() if ln.strip()), "")
                        if first:
                            heading = first[:120]
                        continue
                    if cell.get("cell_type") != "code":
                        continue
                    code = _clean_cell(src)
                    if not code or code.lstrip().startswith(("%", "!")):
                        continue
                    if any(bad in code for bad in ("plt.show()",)) and len(code.splitlines()) < 3:
                        continue
                    assets.append({
                        "path": rel,
                        "kind": "notebook",
                        "heading": heading,
                        "code": code,
                        "tokens": sorted(set(_tokens(heading + " " + code)))[:60],
                    })
            else:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    code = _clean_cell(fh.read())
                if code:
                    assets.append({
                        "path": rel,
                        "kind": "script",
                        "heading": rel.split("/")[-1],
                        "code": code,
                        "tokens": sorted(set(_tokens(rel + " " + code)))[:60],
                    })
        except Exception as exc:  # pragma: no cover - defensive
            print(f"  ! skipped {rel}: {exc}")

    payload = {"generated_from": "repository source files", "assets": assets}
    with open(CODE_CACHE, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return payload


# Words too generic to prove a topical match on their own. Without this filter,
# every lesson would "match" the first notebook that mentions data and columns.
MATCH_STOPWORDS = {
    "data", "rows", "row", "columns", "column", "table", "tables", "value", "values", "code", "using", "used",
    "use", "with", "from", "into", "basic", "basics", "example", "examples", "types", "type", "work", "works",
    "working", "learn", "learning", "case", "study", "part", "parts", "section", "sections", "steps", "step",
    "practice", "project", "projects", "analysis", "complete", "first", "second", "final", "python", "notebook",
    "handling", "function", "functions", "different", "common", "other", "more", "most", "best", "good",
}


def match_code_assets(assets: list[dict], keywords: list[str], repo_hints: list[str],
                      limit: int = 3) -> list[dict]:
    wanted = [w.lower() for w in keywords if len(w) > 2 and w.lower() not in MATCH_STOPWORDS]
    specific = set(wanted)
    hints = [h for h in repo_hints if h and not h.startswith("http")]
    scored: list[tuple[float, dict]] = []
    for asset in assets:
        path_low = asset["path"].lower()
        if any(part in path_low for part in ("/cursor", ".git/", "site-packages")):
            continue
        path_score, keyword_score = 0.0, 0.0
        for hint in hints:
            h = hint.lower().strip("/")
            if h and h in path_low:
                path_score += 3.0
        tok_set = set(asset.get("tokens", []))
        keyword_score += 0.6 * sum(1 for w in wanted if w in tok_set)
        text_low = (asset["heading"] + " " + asset["code"]).lower()
        keyword_score += 0.3 * sum(1 for w in wanted if w in text_low)
        score = path_score + keyword_score
        # require either a path hint from the curriculum, or at least one SPECIFIC
        # topical match; attaching unrelated code to a lesson is worse than none.
        if path_score == 0:
            specific_hits = sum(1 for w in wanted if w in tok_set or w in text_low)
            if specific_hits == 0 or keyword_score < 1.2:
                continue
        if score > 1.2:
            scored.append((score, asset))
    scored.sort(key=lambda x: -x[0])
    out = []
    for score, asset in scored[:limit]:
        out.append({
            "path": asset["path"],
            "kind": asset["kind"],
            "heading": asset["heading"],
            "code": asset["code"],
            "score": round(score, 3),
        })
    return out
