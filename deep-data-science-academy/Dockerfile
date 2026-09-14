# Hugging Face Spaces (Docker SDK) / any container host.
# Zero third-party Python dependencies: the app is standard library only, so the
# image stays small and the Space stays free-tier friendly.
FROM python:3.11-slim

# HF Spaces runs containers as a non-root user by convention
RUN useradd -m -u 1000 academy
WORKDIR /app

# Content is copied before the app so layer caching works when only code changes
COPY --chown=academy:academy content/ ./content/
COPY --chown=academy:academy curriculum.json ./
COPY --chown=academy:academy quizzes/ ./quizzes/
COPY --chown=academy:academy flashcards/ ./flashcards/
COPY --chown=academy:academy interview/ ./interview/
COPY --chown=academy:academy assets/ ./assets/
COPY --chown=academy:academy projects/ ./projects/
COPY --chown=academy:academy docs/ ./docs/
COPY --chown=academy:academy app.py README.md requirements.txt ./

USER academy
ENV PORT=7860 HOST=0.0.0.0 PYTHONUNBUFFERED=1
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:7860/api/health').read()" || exit 1

CMD ["python", "app.py"]
