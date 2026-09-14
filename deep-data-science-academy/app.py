#!/usr/bin/env python3
"""Deep Data Science & AI Academy - application server.

Zero third-party dependencies: standard library only, so it runs anywhere
(local machine, Docker, Hugging Face Spaces, any PaaS) and stays cheap to host.

Endpoints
    GET /                       -> the single-page app (assets/index.html)
    GET /api/health             -> liveness probe + content stats
    GET /api/curriculum         -> light 275-day index (phases, titles, keywords)
    GET /api/day/<n>            -> full lesson JSON for day n (loaded on demand)
    GET /api/search?q=...       -> server-side search over the light index
    GET /api/quiz?day=          -> quiz bank (all, or one day)
    GET /api/flashcards?day=    -> flashcard bank (all, or one day)
    GET /api/interview?day=     -> interview bank (all, or one day)
    GET /assets/*               -> static files (css, js, images, svg)

Design notes
    * Lessons are fetched one at a time, never as a 275-day bundle.
    * Static mode: if the app is hosted without Python (e.g. HF static Space),
      assets/app.js falls back to reading ./content/day_NNN.json directly.
    * Binds 0.0.0.0 and honours $PORT so it works behind container proxies.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
ASSETS_DIR = os.path.join(ROOT, "assets")

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
}

_cache: dict[str, object] = {}


def load_json(rel_path: str):
    """Load a JSON file from the academy root with a tiny in-process cache."""
    if rel_path in _cache:
        return _cache[rel_path]
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    _cache[rel_path] = payload
    return payload


def content_stats() -> dict:
    days = sorted(f for f in os.listdir(CONTENT_DIR) if f.startswith("day_")) if os.path.isdir(CONTENT_DIR) else []
    curriculum = load_json("curriculum.json") or {}
    return {
        "status": "ok",
        "lessons": len(days),
        "phases": len(curriculum.get("phases", [])),
        "total_days": curriculum.get("total_days", 275),
        "first": days[0] if days else None,
        "last": days[-1] if days else None,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "DDSAAcademy/1.0"

    # -- helpers --------------------------------------------------------- #
    def _send(self, body: bytes, ctype: str, status: int = 200, cache: str = "no-cache") -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        # allow embedding in the preview iframe / HF Spaces
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, payload, status: int = 200) -> None:
        self._send(json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8", status)

    def _error(self, status: int, message: str) -> None:
        self._json({"error": message, "status": status}, status)

    def log_message(self, fmt, *args):  # quieter logs
        if os.environ.get("ACADEMY_VERBOSE"):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # -- routing --------------------------------------------------------- #
    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ("/", "/index.html", "/academy"):
            return self._serve_static("index.html")
        if path == "/api/health":
            return self._json(content_stats())
        if path == "/api/curriculum":
            payload = load_json("curriculum.json")
            return self._json(payload) if payload else self._error(503, "curriculum.json not built yet - run tools/build_content.py")
        if path.startswith("/api/day/"):
            day = path.rsplit("/", 1)[-1]
            if not day.isdigit() or not (1 <= int(day) <= 275):
                return self._error(400, "day must be an integer between 1 and 275")
            payload = load_json(f"content/day_{int(day):03d}.json")
            return self._json(payload) if payload else self._error(404, f"day {day} content not built yet")
        if path == "/api/search":
            return self._search(query.get("q", [""])[0])
        if path in ("/api/quiz", "/api/quizzes"):
            return self._bank("quizzes/quiz_bank.json", query)
        if path == "/api/flashcards":
            return self._bank("flashcards/flashcard_bank.json", query)
        if path == "/api/interview":
            return self._bank("interview/interview_bank.json", query)

        # static assets
        rel = path.lstrip("/")
        if rel.startswith("assets/"):
            return self._serve_static(rel[len("assets/"):])
        # allow direct access to content JSON and other built files (static-host parity)
        if rel.startswith(("content/", "quizzes/", "flashcards/", "interview/")):
            full = os.path.normpath(os.path.join(ROOT, rel))
            if full.startswith(ROOT) and os.path.isfile(full):
                with open(full, "rb") as fh:
                    return self._send(fh.read(), MIME.get(os.path.splitext(full)[1], "application/octet-stream"))
        return self._error(404, f"not found: {path}")

    do_HEAD = do_GET

    # -- handlers -------------------------------------------------------- #
    def _serve_static(self, rel: str):
        full = os.path.normpath(os.path.join(ASSETS_DIR, rel))
        if not full.startswith(ASSETS_DIR) or not os.path.isfile(full):
            return self._error(404, f"asset not found: {rel}")
        ext = os.path.splitext(full)[1].lower()
        cache = "max-age=3600" if ext in (".css", ".js", ".svg", ".png", ".jpg", ".webp", ".ico") else "no-cache"
        with open(full, "rb") as fh:
            self._send(fh.read(), MIME.get(ext, "application/octet-stream"), cache=cache)

    def _bank(self, rel: str, query: dict):
        payload = load_json(rel)
        if payload is None:
            return self._error(503, f"{rel} not built yet")
        day = query.get("day", [None])[0]
        if day and day.isdigit():
            payload = [item for item in payload if item.get("day") == int(day)]
        limit = query.get("limit", [None])[0]
        if limit and limit.isdigit():
            payload = payload[: int(limit)]
        return self._json(payload)

    def _search(self, q: str):
        index = load_json("assets/search_index.json") or []
        q = (q or "").strip().lower()
        if not q:
            return self._json([])
        terms = [t for t in q.split() if t]
        results = []
        for item in index:
            haystack = " ".join([
                item.get("title", ""), item.get("phase_name", ""),
                " ".join(item.get("topics", [])), " ".join(item.get("keywords", [])),
                " ".join(item.get("objectives", [])),
            ]).lower()
            score = 0
            for term in terms:
                if term in item.get("title", "").lower():
                    score += 6
                score += 2 * haystack.count(term)
            if score:
                results.append({**{k: item[k] for k in ("day", "title", "phase", "phase_name", "difficulty", "depth", "tag")},
                                "score": score})
        results.sort(key=lambda r: -r["score"])
        return self._json(results[:40])


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> None:
    port = int(os.environ.get("PORT", os.environ.get("ACADEMY_PORT", 7860)))
    host = os.environ.get("HOST", "0.0.0.0")
    if not os.path.isdir(CONTENT_DIR) or not os.listdir(CONTENT_DIR):
        print("! content/ is empty - run: python3 tools/build_content.py", file=sys.stderr)
    stats = content_stats()
    print(f"Deep Data Science & AI Academy")
    print(f"  lessons built : {stats['lessons']}/275")
    print(f"  serving       : http://{host}:{port}")
    httpd = Server((host, port), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
