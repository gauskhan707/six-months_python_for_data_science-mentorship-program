"""Phase definitions for the 275-day Deep Data Science & AI Academy.

The phase map is the spine of the curriculum: it fixes the day ranges, the
learning arc, and how much of each phase is source-backed (taught in the
original Codanics mentorship recordings) versus an academy EXTENSION.
"""

PHASES = [
    dict(n=1, name="Data Science + Python Foundations", start=1, end=15,
         goal="Understand the field and become fluent in core Python.",
         source_level="high",
         source_note="Original course days 1-7 (intro, installation, Python programming)."),
    dict(n=2, name="Python for Data Work", start=16, end=32,
         goal="Write professional, testable Python that handles real data files, APIs and repos.",
         source_level="medium",
         source_note="Original course touched functions/modules and Git; testing, typing, logging, regex and packaging are academy extensions."),
    dict(n=3, name="NumPy + Scientific Computing", start=33, end=48,
         goal="Manipulate n-dimensional arrays fast, and understand the maths they implement.",
         source_level="high",
         source_note="Original course days 28-32 (NumPy parts 1-3) plus linear algebra in Python."),
    dict(n=4, name="Pandas + Data Cleaning + EDA", start=49, end=70,
         goal="Load, clean, reshape and explore any tabular dataset with confidence.",
         source_level="high",
         source_note="Original course days 8-20 (Pandas parts 1-8, outliers, EDA) plus the pandas tips & tricks notebooks."),
    dict(n=5, name="Data Visualization + Storytelling", start=71, end=88,
         goal="Turn data into charts that change decisions, in matplotlib, seaborn and plotly.",
         source_level="high",
         source_note="Original course days 21-26 (visualization parts 1-2, plotly, animated plots, quiz)."),
    dict(n=6, name="Mathematics for Data Science", start=89, end=112,
         goal="Build the maths foundation (algebra, linear algebra, calculus, probability) needed by ML.",
         source_level="high",
         source_note="Original course Zero-to-Math series (number theory, pre-algebra, linear algebra parts 1-8) plus 05_mathematics notebook."),
    dict(n=7, name="Statistics", start=113, end=134,
         goal="Describe data, quantify uncertainty and test hypotheses correctly.",
         source_level="high",
         source_note="Original course ABC of Statistics days 1-13 plus the 06_statistics notebooks (central tendency, distributions, tests, ANOVA, MANOVA, correlation, case study)."),
    dict(n=8, name="SQL + Databases", start=135, end=150,
         goal="Query relational databases fluently and pass SQL interviews.",
         source_level="low",
         source_note="ACADEMY EXTENSION. The original six-month recordings do not teach SQL; Codanics delivers it as a separate playlist. Practice database provided in resources/datasets_for_practice/database.sqlite.zip."),
    dict(n=9, name="Excel + Power BI + Tableau", start=151, end=164,
         goal="Be dangerous in the BI stack that most employers actually use.",
         source_level="high",
         source_note="Original course Tableau series (Mar-Apr 2024) and Power BI for Beginners series (Apr-May 2024). Excel analytics is an academy extension."),
    dict(n=10, name="Machine Learning", start=165, end=196,
         goal="Train, tune, evaluate and explain supervised models from first principles.",
         source_level="high",
         source_note="Original course Machine Learning-101 days 1-21 plus the 07_machine_learning notebooks and the bank-churn / diamond model comparisons."),
    dict(n=11, name="Unsupervised ML + Time Series", start=197, end=212,
         goal="Find structure without labels and forecast time series properly.",
         source_level="high",
         source_note="Original course unsupervised ML series (k-means, hierarchical, DBSCAN/OPTICS, GMM, PCA, SVD, t-SNE) and the time series / ARIMA / SARIMA / Prophet recordings."),
    dict(n=12, name="Deep Learning + Computer Vision", start=213, end=232,
         goal="Understand neural networks from a single neuron to a trained CNN.",
         source_level="high",
         source_note="Original course Deep Learning-101 days 1-8 (MLP, activations, CNN, computer vision, rice disease project, RNN) with PyTorch added as an extension."),
    dict(n=13, name="NLP + Transformers + Hugging Face", start=233, end=246,
         goal="Process text, then understand and fine-tune transformer models.",
         source_level="medium",
         source_note="Original course covered NLP basics, sentiment analysis, LSTM/GRU and an intro to Hugging Face. Attention maths and transformer internals are academy extensions."),
    dict(n=14, name="Generative AI + LLMs + RAG", start=247, end=258,
         goal="Engineer reliable LLM applications with retrieval, tools and evaluation.",
         source_level="medium",
         source_note="Original course covered prompt engineering, Hugging Face, OpenAI APIs, LangChain and Streamlit chat-with-PDF apps. RAG evaluation, structured outputs and agent architecture are academy extensions."),
    dict(n=15, name="Deployment + MLOps + Data Engineering", start=259, end=268,
         goal="Ship models as services and keep them healthy in production.",
         source_level="medium",
         source_note="Original course covered Streamlit, Flask, FastAPI and an AWS EC2 deployment walkthrough. Docker, MLflow, CI/CD, monitoring, drift and PySpark are academy extensions."),
    dict(n=16, name="Capstone + Portfolio + Interview", start=269, end=275,
         goal="Turn 268 days of skill into two portfolio projects and interview performance.",
         source_level="medium",
         source_note="Original course included portfolio building (day 22), best-model presentations and Q&A sessions; this phase structures that into a job-readiness program."),
]


def phase_for_day(day: int) -> dict:
    for p in PHASES:
        if p["start"] <= day <= p["end"]:
            return p
    raise ValueError(f"day {day} outside 1-275")


PHASE_DAY_COUNT = sum(p["end"] - p["start"] + 1 for p in PHASES)
assert PHASE_DAY_COUNT == 275, PHASE_DAY_COUNT
