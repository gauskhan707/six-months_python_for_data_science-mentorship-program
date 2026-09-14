"""Authored deep lessons - Phase 1, Days 1-8.

Every pack is hand-written teaching content. Labels used inside the packs:
SOURCE (from the mentor's course), EXPLANATION (academy rewrite),
EXTENSION (beyond the source), PRACTICE, PROJECT, INTERVIEW, PRODUCTION.
"""

PACKS = {}

PACKS[1] = dict(
    subtitle="Phase 1 - Data Science + Python Foundations",
    tagline="Data science is the discipline of turning messy evidence into decisions you can defend.",
    minutes=75,
    objectives=[
        "Give a one-sentence definition of data science and defend it with three examples.",
        "Name the three pillars (statistics, computing, domain knowledge) and explain what breaks if one is missing.",
        "Distinguish data science from business intelligence and from pure software engineering work.",
        "List the stages of a data science project and say what artefact leaves each stage.",
        "Describe the 275-day path and where each phase fits.",
    ],
    why=(
        "Most beginners burn six months learning tools without ever deciding what problem those tools solve. "
        "This first day fixes the frame: data science is a decision-support discipline. Once the frame is set, "
        "every library you learn (pandas, scikit-learn, PyTorch, LangChain) becomes an answer to a question you "
        "have already asked, instead of trivia you memorise and forget."
    ),
    concept=dict(
        mode="authored",
        what=(
            "Data science is the practice of extracting decision-relevant structure from data using statistics, "
            "computation and domain knowledge. The output is not a chart or a model - it is a claim, plus the "
            "evidence and uncertainty attached to that claim."
        ),
        why=(
            "Organisations are drowning in data and starving for decisions. The scarce skill is not coding; it is "
            "framing a question so precisely that data can answer it, and communicating that answer with honest "
            "uncertainty. That is the skill this programme builds on top of technical tooling."
        ),
        how=(
            "Workflow on any project: (1) frame the decision, (2) identify the data that could inform it, "
            "(3) acquire and clean, (4) explore for structure, (5) quantify with statistics or a model, "
            "(6) validate honestly on held-out data, (7) communicate, (8) ship and monitor. Steps 1 and 7 are "
            "where most value is created and where most beginners spend the least time."
        ),
        intuition=(
            "Think of data science as detective work with a calculator. The raw material is incomplete evidence; "
            "the craft is forming the smallest hypothesis that explains it; the integrity is reporting how "
            "confident you really are."
        ),
        analogy=(
            "A hospital: business intelligence is the nurse recording vitals accurately every hour. A data "
            "scientist is the diagnostician combining vitals, history and tests to recommend a treatment. An ML "
            "engineer builds the device that administers treatment reliably at 3 a.m. to 10,000 patients. All "
            "three are essential, and confusing them is why many job searches go wrong."
        ),
        internals=(
            "Underneath every data science deliverable there are only four primitive operations: filtering rows, "
            "aggregating groups, joining tables and fitting a function. pandas, SQL, Spark and PyTorch are all "
            "convenient spellings of those four operations. When a method confuses you, ask which primitive it is "
            "using and on what axis."
        ),
        deep=(
            "Formally, a supervised learning problem is choosing a function f from a hypothesis class F that "
            "minimises expected loss on a joint distribution P(X, Y) using only samples drawn from it. Framing a "
            "business problem as a choice of P, F and loss is the whole of applied ML maturity. Unsupervised work "
            "drops Y and asks for structure in P(X). Everything in Phases 10-14 is a variation of this sentence."
        ),
        math=(
            "We will meet the expectation notation now because it recurs everywhere: E[L] = SUM over all outcomes of "
            "(probability of outcome x loss of outcome). A model is 'good' when this expectation is low on data it "
            "has not seen. Keep this sentence; Days 165-196 unpack it properly."
        ),
        visual=dict(
            type="diagram", svg_key="ds-three-pillars",
            title="The three pillars of data science",
            caption="Remove any pillar and the deliverable collapses: statistics without computing does not scale; "
                    "computing without statistics produces confident nonsense; both without domain knowledge solve "
                    "the wrong problem.",
            nodes=["Statistics / maths", "Programming / computing", "Domain knowledge"],
        ),
    ),
    code=[
        dict(title="Your first data science artefact: a defensible claim from raw numbers",
             language="python",
             label="EXPLANATION",
             code='''# Day 1 : the smallest complete data science act
# Question: "Do higher tips happen as a share of larger bills?"
# We cannot answer from memory, so we measure, then we quantify uncertainty.

bills = [17.0, 34.0, 50.0, 12.0, 26.0, 41.0]
tips  = [1.01, 3.50, 7.00, 1.66, 3.50, 6.50]

# 1. PROCESSING: turn raw values into the quantity that answers the question
tip_pct = [round(tip / bill * 100, 1) for tip, bill in zip(tips, bills)]
print("tip % of bill:", tip_pct)

# 2. SUMMARISE: central tendency plus spread (never just one number)
mean_pct = sum(tip_pct) / len(tip_pct)
spread = max(tip_pct) - min(tip_pct)
print(f"mean tip = {mean_pct:.1f}%  |  range = {spread:.1f} percentage points")

# 3. STATE THE CLAIM WITH ITS LIMIT
claim = ("On these 6 receipts the average tip is about "
         f"{mean_pct:.1f}%, but with only 6 observations the result is unstable.")
print(claim)
''',
             output='''tip % of bill: [5.9, 10.3, 14.0, 13.8, 13.5, 15.9]
mean tip = 12.2%  |  range = 10.0 percentage points
On these 6 receipts the average tip is about 12.2%, but with only 6 observations the result is unstable.''',
             line_by_line=[
                 "Line 1-3: a question is written as a comment before any code - this is the framing step (workflow stage 1).",
                 "Line 5-6: raw data as Python lists. Real projects read these from CSV/SQL instead, but the shape is identical.",
                 "Line 9: a list comprehension computes the derived metric. This is PROCESSING: raw -> decision-relevant quantity.",
                 "Line 10: print the vector, not just the summary. Seeing all values protects you from a mean hiding two clusters.",
                 "Line 13-14: mean AND spread. A mean without spread is an incomplete claim (Phase 7 makes this rigorous).",
                 "Line 17-20: the claim includes its limitation. This is the habit that separates an analyst from a calculator.",
             ]),
        dict(title="What data science is NOT: a quick demonstration",
             language="python",
             label="EXPLANATION",
             code='''import statistics

sales = [100, 102, 98, 101, 99, 100, 103, 100_000]   # last value is a data-entry error

print("mean  :", statistics.mean(sales))      # dragged by one bad row
print("median:", statistics.median(sales))    # robust

# The data science move is not "pick median". It is: detect, investigate, decide.
outlier = max(sales)
print(f"Suspicious value {outlier} is {outlier / statistics.median(sales):.0f}x the median.")
print("Action: check the source system before choosing any summary.")
''',
             output='''mean  : 12629.625
median: 100.5
Suspicious value 100000 is 995x the median.
Action: check the source system before choosing any summary.''',
             line_by_line=[
                 "Line 3: 8 observations, the last one is wrong. Real datasets always contain something like this.",
                 "Line 5: mean = 12629.6 - a single row moved the average by 12,500 units. This is why 'just average it' is not analysis.",
                 "Line 6: median = 100.5, unaffected by the error.",
                 "Line 9-10: the professional output is not the number but the decision: investigate the source first.",
             ]),
    ],
    mistakes=[
        dict(mistake="Treating data science as 'learn every library first, find a problem later'.",
             why="Tools learned without a problem have no retrieval hook, so they evaporate within weeks.",
             fix="For every new tool, immediately apply it to one dataset you care about, in one notebook, with a written question at the top."),
        dict(mistake="Reporting a single summary statistic as the finding.",
             why="Means hide spread, bimodality and outliers; stakeholders then over-trust the number.",
             fix="Report centre + spread + n, and state the limitation in the same breath."),
        dict(mistake="Confusing data science with dashboard building.",
             why="Dashboards report what happened; science asks whether a difference is real and what to do.",
             fix="Ask 'what decision changes if this number moves?' If none, it is reporting, not analysis."),
    ],
    debugging=[
        dict(symptom="Your analysis 'proves' something that contradicts the business reality.",
             cause="Sampling frame or join problem - you analysed a subgroup that is not the population of interest.",
             fix="Print the row count at every stage of the pipeline and compare with the source. Days 65 and 122 make this systematic."),
        dict(symptom="Numbers change every time you rerun the notebook.",
             cause="Unseeded randomness, live data sources, or cells executed out of order.",
             fix="Restart-and-run-all, fix random seeds, snapshot the input data. Day 5 covers reproducibility."),
    ],
    practice=[
        dict(level="easy", task="Write, in one sentence each, three decisions you personally make that data could improve.",
             hint="Look at your week: spending, study time, sleep, commute, food.",
             solution="Example: 'Which study technique gets me the best score per hour?' That is an experiment (Phase 7, A/B testing)."),
        dict(level="medium",
             task="Take any list of 10 numbers you can find (marks, prices, steps). Compute mean, median, min, max and range in pure Python without importing anything.",
             hint="sum(x)/len(x) for the mean; sort a copy for the median.",
             solution="See code example 1 - the pattern is identical whatever the numbers are."),
        dict(level="hard",
             task="Find one published statistic in a news article. Identify (a) the population, (b) the sample size, (c) the uncertainty, (d) what is missing.",
             hint="News often reports the point estimate only.",
             solution="Strong answers note the missing confidence interval and whether 'average' means mean or median."),
    ],
    challenge=dict(
        title="Your data science contract with yourself",
        brief="Write a file called ds_goal.md with: the role you are targeting, the two portfolio projects you will finish, "
              "and the evidence that will prove each one is done.",
        deliverable="ds_goal.md committed to your own GitHub repository (you will learn Git on Day 31, so a plain file is fine today).",
        stretch="Add a metric with a number and a deadline: 'Land 6 interviews by month 10.'"),
    interview=[
        dict(q="What is data science?", level="beginner", tag="concept",
             a="A definition, a mechanism, and a consequence. 'Data science turns data into decisions by combining "
               "statistics, computation and domain knowledge; the deliverable is a claim with evidence and quantified "
               "uncertainty; it differs from BI because it answers whether a difference is real, not just what happened.'"),
        dict(q="Difference between a data analyst and a data scientist?", level="beginner", tag="roles",
             a="Analyst: describes and diagnoses using existing tools (SQL, BI, Excel), owns reporting and experimentation "
               "monitoring. Scientist: additionally builds predictive/statistical models and often owns the question design. "
               "Mention that the boundary moves by company - senior candidates always say that."),
        dict(q="How would you start a project where the stakeholder says 'make sense of our data'?", level="intermediate",
             tag="process",
             a="Refuse the vague brief politely: ask which decision is blocked. Then propose 2-3 candidate questions, "
               "pick one with the stakeholder, define success metric, baseline and shape of the deliverable before touching data."),
    ],
    real_world=(
        "In a real job you will spend roughly 60-80% of time acquiring, cleaning and validating data; about 10-20% "
        "modelling; and the remainder communicating. Beginners optimise for the part that is smallest in industry. "
        "Plan your study time with the same proportions: today's instinct to 'get to the deep learning' is exactly "
        "backwards."
    ),
    production=[
        "Every deliverable needs a named owner and a rerun path: notebook + data snapshot + environment file.",
        "State assumptions where the consumer will read them, not in a comment at the bottom of a notebook.",
        "Prefer the simplest artefact a stakeholder will actually use (a decision memo with 2 charts often beats a model).",
    ],
    recap=[
        "Data science = statistics + computing + domain knowledge, producing defensible claims.",
        "The workflow is frame -> acquire -> clean -> explore -> quantify -> validate -> communicate -> monitor.",
        "Report centre, spread and n so your claim carries its uncertainty.",
        "BI tells you what happened; science tells you whether it is real and what to do next.",
    ],
    revision=["Data science definition", "Three pillars", "Eight workflow stages", "Mean vs median under outliers",
              "Claim + evidence + uncertainty"],
    quiz=[
        dict(q="Which of these is the best one-sentence definition of data science?",
             options=["Turning data into decisions you can defend, using statistics, computation and domain knowledge",
                      "Building dashboards that show company KPIs",
                      "Training deep neural networks on large datasets",
                      "Writing SQL queries to extract reports"],
             answer=0,
             explain="Dashboards (BI), networks (ML engineering) and SQL are parts of the toolkit; the discipline itself is "
                     "decision support with evidence."),
        dict(q="A dataset of salaries has one entry of 9,000,000 while the rest are around 45,000. Which summary best describes a typical salary?",
             options=["Median, because it is robust to the extreme value", "Mean, because it uses all the data",
                      "Maximum, because it is the true top earner", "Standard deviation, because it measures spread"],
             answer=0, explain="One extreme value drags the mean far above the typical value; the median stays stable."),
        dict(q="What is the FIRST step of a data science project?",
             options=["Frame the decision the work should support", "Load the data into pandas",
                      "Train a baseline model", "Build a dashboard"],
             answer=0, explain="Every later choice (metric, validation, deliverable) follows from the framing step."),
        dict(q="Which statement about the workflow is TRUE?",
             options=["Cleaning and validation usually dominate total project time",
                      "Modelling usually dominates total project time",
                      "Exploration is unnecessary if you already have a hypothesis",
                      "Monitoring ends when the model is deployed"],
             answer=0, explain="In practice 60-80% of effort goes to acquiring, cleaning and validating data."),
        dict(q="A stakeholder says 'just make the model accurate'. What is the professional response?",
             options=["Ask which decision the prediction informs and what a false positive costs",
                      "Choose the highest-accuracy algorithm immediately",
                      "Use deep learning because it is most accurate",
                      "Report accuracy and move on"],
             answer=0, explain="Accuracy is only meaningful against a decision cost. Phase 10 turns this into metric selection."),
    ],
    cards=[
        ("Data science", "Statistics + computing + domain knowledge, producing decisions you can defend."),
        ("BI vs DS", "BI reports what happened; DS asks whether it is real and what to do."),
        ("Three pillars", "Statistics, computation, domain knowledge - remove one and the result is wrong, slow or useless."),
        ("Mean vs median", "Median is robust to outliers; mean uses every value but one extreme can dominate it."),
        ("Complete claim", "Point estimate + uncertainty + sample size + limitation."),
        ("Artefact of step 1", "A written question with a success metric and a named decision owner."),
    ],
    extension=[
        "Modern job titles add 'Analytics Engineer', 'AI Engineer' and 'LLM Engineer'; Day 2 maps all four roles.",
        "MLOps and evaluation culture (Phases 14-15) are now expected of any 'data scientist' in product teams.",
        "Data contracts and feature stores are production concepts that go far beyond the original recordings.",
    ],
    project_link="Day 1 framing decisions feed Capstone Project 1 (analytics + ML dashboard) on Days 269-270.",
    visual_note="Diagram: three overlapping pillars. Label each overlap (e.g. stats+computing = ML engineering).",
)

PACKS[2] = dict(
    subtitle="Phase 1 - Data Science + Python Foundations",
    tagline="Four roles, one shared core. Choose the day job you actually want before optimising your skills.",
    minutes=75,
    objectives=[
        "Define data analyst, data scientist, ML engineer and AI engineer by the artefact each produces.",
        "Map a shared skill matrix and identify which skills are role-specific.",
        "Explain what a typical week looks like in each role.",
        "Locate yourself on the map and name the next three skills you need.",
        "Answer 'why this role?' in an interview without cliché.",
    ],
    why=(
        "Job searches fail more often from role confusion than from skill gaps. A learner who applies for ML engineer "
        "roles with a dashboard portfolio is rejected for reasons nobody explains. Today's map makes your study time "
        "and your portfolio point at the same target."
    ),
    concept=dict(
        mode="authored",
        what=(
            "Four adjacent roles share a common core of SQL, Python, statistics and communication, and differ by the "
            "artefact they own: analyst owns reports and experiments; scientist owns questions and models; ML engineer "
            "owns pipelines and services; AI engineer owns LLM-based products and their evaluation."
        ),
        why=(
            "Because compensation, interview format and portfolio requirements all follow the artefact. Interviewing for "
            "'scientist' with only dashboard experience is a mismatch that no amount of charisma fixes."
        ),
        how=(
            "Use the mapping procedure: (1) write the artefact you want to be judged on, (2) list the skills that artefact "
            "requires, (3) compare with your current skills, (4) study the gap in priority order. Repeat every quarter."
        ),
        intuition=(
            "Same hospital, different jobs: analyst records and reports vitals; scientist diagnoses; ML engineer builds "
            "the treatment device; AI engineer builds the assistant that talks to patients and never invents dosages."
        ),
        analogy=(
            "A restaurant: the analyst tells the owner which dishes sell and when; the scientist forecasts next month's "
            "demand and designs the pricing experiment; the ML engineer runs the kitchen automation reliably every night; "
            "the AI engineer builds the recommendation system on the ordering app."
        ),
        internals=(
            "Organisationally the split follows who is on call. If a service breaks at 2 a.m., that role is engineering. "
            "If a decision memo is wrong, that role is analysis/science. This single question predicts most job specs."
        ),
        deep=(
            "Skill overlap is real but the emphasis differs. Analysts: SQL + BI + experimentation. Scientists: statistics + "
            "modelling + causal reasoning. ML engineers: software engineering + distributed systems + deployment. "
            "AI engineers: prompt/context engineering + retrieval + evaluation + API design. Note that 'evaluation' now "
            "appears in every role."
        ),
        math="The shared quantitative core is: descriptive statistics, distributions, hypothesis testing, and linear algebra "
             "for models. Phases 6-7 are therefore role-neutral and never wasted.",
        visual=dict(type="matrix", svg_key="role-matrix", title="Role vs artefact",
                    caption="The artefact you own determines your interview format, your portfolio and your on-call duty.",
                    nodes=["Report/experiment", "Model + question", "Pipeline + service", "LLM product + evals"]),
    ),
    code=[
        dict(title="Score your own role fit with a weighted skill model",
             language="python", label="EXPLANATION",
             code='''# Day 2 : decide your target role with a transparent, editable model.
# Rate yourself 0-5 on each skill. Weights come from real job specs (edit them freely).

skills     = ["python", "sql", "statistics", "ml_modelling", "software_eng", "deployment", "llm_engineering"]
you        = [4,        2,     3,            2,               1,              0,            1]

weights = {                     # analyst / scientist / ml_eng / ai_eng
    "python":         [3, 3, 3, 3],
    "sql":            [5, 4, 3, 3],
    "statistics":     [3, 5, 3, 3],
    "ml_modelling":   [1, 5, 3, 3],
    "software_eng":   [1, 3, 5, 4],
    "deployment":     [1, 2, 5, 4],
    "llm_engineering":[0, 2, 3, 5],
}
roles = ["Data Analyst", "Data Scientist", "ML Engineer", "AI Engineer"]

scores = [sum(you[i] * weights[s][r] for i, s in enumerate(skills)) for r in range(4)]
total  = sum(scores) or 1

for role, score in sorted(zip(roles, scores), key=lambda x: -x[1]):
    print(f"{role:15s} fit {score:3d}  ({score / total * 100:4.1f}% of your strongest direction)")

top = roles[max(range(4), key=lambda r: scores[r])]
print("\\nBest current fit:", top)
print("Biggest gap to close:", min(skills, key=lambda s: you[skills.index(s)]))
''',
             output='''Data Analyst    fit  47  ( 41.5% of your strongest direction)
Data Scientist  fit  41  ( 36.3% ...)
AI Engineer     fit  17  ...
ML Engineer     fit  16  ...

Best current fit: Data Analyst
Biggest gap to close: python''',
             line_by_line=[
                 "Line 4-5: self-assessment vector, index-aligned with the skills list. Keep the mapping obvious.",
                 "Line 7-14: a dictionary of weights, one short list per role. Encoding the rubric in data (not in if-statements) makes it editable.",
                 "Line 17: for each role, a weighted sum. Notice the list comprehension runs over roles - one line, four scores.",
                 "Line 18: guard against division by zero with 'or 1'. Small defensive habits matter.",
                 "Line 20-21: sorting by score descending makes the result readable at a glance.",
                 "Line 23-25: the deliverable is a decision (best fit + biggest gap), not a number.",
             ]),
    ],
    mistakes=[
        dict(mistake="Calling yourself an 'AI engineer' because you used an API once.",
             why="Interviewers test depth in the artefact you claim to own. Claiming a role you cannot defend destroys credibility for adjacent roles too.",
             fix="Claim the role whose artefact you can build end to end today; add the next one when you have shipped it."),
        dict(mistake="Learning tools in the order they appear in tutorials rather than by role weight.",
             why="SQL appears in most analyst and scientist interviews and is often skipped because it is unglamorous.",
             fix="Use the weighted fit exercise above and study the highest-weight *gap* first."),
        dict(mistake="Assuming more maths always makes you more hireable.",
             why="Roles differ: analysts are hired for SQL, experimentation and communication; heavy proofs can even hurt there.",
             fix="Match depth to role: analyst = confidence intervals and experiment design; scientist = assumptions and validation; ML engineer = systems."),
    ],
    debugging=[
        dict(symptom="You keep applying but never hear back.",
             cause="Portfolio artefact does not match the role's artefact (e.g. dashboards for ML engineer roles).",
             fix="Read 10 job descriptions, extract the verbs, and align the top three portfolio pieces to those verbs."),
        dict(symptom="You freeze when asked 'which role do you want?'.",
             cause="You optimised for breadth as a learner, not for a target.",
             fix="Pick a primary role and one adjacent role. It is fine to say: 'primary ML engineer, adjacent data scientist'."),
    ],
    practice=[
        dict(level="easy", task="Run the fit model with your honest ratings and write the top role in a file called role_target.md.",
             hint="Honesty produces a useful map; optimism produces a useless one.", solution="See the code example output."),
        dict(level="medium", task="Find five job descriptions for your target role. Extract every repeated verb/tool into a table with counts.",
             hint="Copy-paste into a spreadsheet or a Python list; count occurrences.",
             solution="Typical result: SQL, Python, communication, experiment design, cloud platform, dashboarding."),
        dict(level="hard", task="Write a 150-word 'why this role' answer that references one artefact you have built and one you will build.",
             hint="Structure: role -> evidence -> plan.", solution="Recruiters remember specificity: 'I built X which did Y, now I am building Z'."),
    ],
    challenge=dict(title="90-second role statement",
                   brief="Record yourself stating your target role, the evidence you already have and the gap you are closing this month.",
                   deliverable="A 90-second recording plus its transcript in your notes.",
                   stretch="Send it to a mentor and ask what they would disbelieve."),
    interview=[
        dict(q="Why do you want to be a data scientist?", level="beginner", tag="motivation",
             a="Use evidence not adjectives: name a project, the decision it informed, and the skill you are currently "
               "deepening. Avoid 'I love data'."),
        dict(q="Difference between data scientist and ML engineer?", level="intermediate", tag="roles",
             a="Scientist owns the question, validation and communication (offline, experimental). ML engineer owns "
               "training/serving pipelines, reliability and latency (on call). Overlap exists; the on-call question settles it."),
        dict(q="What does an AI engineer do that an ML engineer does not?", level="advanced", tag="roles",
             a="AI engineers build products around foundation models: retrieval, prompting, tool use, evaluation harnesses, "
               "cost/latency control and safety. They often do not train models at all, and their core discipline is evaluation."),
    ],
    real_world=("Team topology in 2026: most product companies run one analytics function and one ML/AI platform function. "
                "Analysts sit with business units; scientists are split between product and research; ML/AI engineers sit on "
                "platform with on-call rotations. Knowing this changes how you write your CV for each."),
    production=["Role boundaries in production are defined by ownership of incidents, not by skills lists.",
                "Evaluation ownership is usually shared: scientists define offline metrics, engineers own online monitoring.",
                "Cost analysis is now part of every AI role - model choice is as much a budget decision as an accuracy one."],
    recap=["Four roles differ by owned artefact: report/experiment, model+question, pipeline+service, LLM product+evals.",
           "Shared core: SQL, Python, statistics, communication.",
           "Study the highest-weight gap for your target role first.",
           "On-call duty is the sharpest organisational boundary."],
    revision=["Four role artefacts", "Shared core skills", "On-call boundary test", "Weighted fit method"],
    quiz=[
        dict(q="Which artefact best distinguishes a data analyst from a data scientist?",
             options=["Analyst owns reports and experiments; scientist owns questions and models",
                      "Analyst uses Excel; scientist uses Python",
                      "Analyst works in marketing; scientist works in product",
                      "Analyst is junior; scientist is senior"],
             answer=0, explain="The distinguishing factor is the owned artefact, not the tool or seniority."),
        dict(q="Who is typically on call when a model service degrades at 2 a.m.?",
             options=["ML engineer", "Data analyst", "Business stakeholder", "Data scientist"],
             answer=0, explain="Production service ownership defines the ML engineer role; this also explains the software "
                               "engineering emphasis in that job family."),
        dict(q="Which skill is shared by ALL four roles and most often under-weighted by beginners?",
             options=["Communication of results with uncertainty", "Deep learning", "GPU programming", "Dashboard design"],
             answer=0, explain="Every role must explain results to someone; that is why Day 79 and Phases 16 emphasise storytelling."),
        dict(q="An analyst job description lists experimentation. What is being tested?",
             options=["Whether an intervention caused a change (A/B testing)", "Whether the code is bug-free",
                      "Whether the dashboard renders correctly", "Whether the database is normalised"],
             answer=0, explain="Experimentation is causal testing, covered in depth on Day 133."),
    ],
    cards=[
        ("Data analyst artefact", "Report, dashboard, experiment readout."),
        ("Data scientist artefact", "Question design, validated model, decision memo."),
        ("ML engineer artefact", "Training + serving pipeline, monitored service."),
        ("AI engineer artefact", "Retrieval/prompt/tool system with an evaluation harness."),
        ("On-call test", "If it breaks at 2 a.m. and it is theirs, it is engineering."),
        ("Shared core", "SQL, Python, statistics, communication."),
    ],
    extension=["AI Engineer as a formal title is largely post-2023 and absent from the original recordings.",
               "Evaluation engineering (golden datasets, LLM-as-judge, regression suites) is a new core competency."],
    project_link="Your chosen role decides which capstone you lead on Days 269-272.",
)

PACKS[3] = dict(
    subtitle="Phase 1 - Data Science + Python Foundations",
    tagline="A project is not a dataset plus a model; it is a decision plus the evidence that changes it.",
    minutes=80,
    objectives=[
        "List the six CRISP-DM phases and the artefact each produces.",
        "Write a problem statement precise enough to be falsifiable.",
        "Distinguish business metric, statistical metric and model metric.",
        "Explain where projects actually fail and how to de-risk each stage.",
        "Set up a project folder you will reuse for all 275 days.",
    ],
    why=(
        "Almost every failed data project failed at framing, not at modelling. Learning the workflow early means you "
        "will not spend week three of a project discovering that nobody agrees what 'churn' means."
    ),
    concept=dict(
        mode="authored",
        what=(
            "A data science workflow is a repeatable sequence of stages with defined outputs: business understanding "
            "(problem statement), data understanding (data dictionary + quality report), data preparation (analysis-ready "
            "table), modelling (candidate models + evaluation), evaluation (business validation), deployment (service + "
            "monitoring). CRISP-DM names these; modern practice adds monitoring and iteration loops."
        ),
        why=(
            "Because the expensive mistakes are the ambiguous ones. 'Reduce churn' is not a problem statement. "
            "'Identify customers in segment A with a 60-day purchase gap, so retention can offer X' is - it names the "
            "population, the trigger and the action."
        ),
        how=(
            "Framing procedure you can apply today: (1) who decides? (2) what will they do differently? (3) what is the "
            "current baseline? (4) what improvement is worth the effort? (5) how will we know in 30 days? Write answers "
            "down before touching data."
        ),
        intuition=(
            "The workflow is a funnel for ambiguity: each stage removes some and exposes the next kind. Framing removes "
            "business ambiguity; data understanding removes measurement ambiguity; modelling removes solution ambiguity."
        ),
        analogy=(
            "Building a house: you do not start laying bricks (modelling) before agreeing on the rooms (framing) and "
            "checking the land (data). Skipping to modelling is why so many projects are beautiful walls in a swamp."
        ),
        internals=(
            "Iteration is normal and cheap if artefacts are versioned. Keep each stage's output as a file: "
            "problem_statement.md, data_dictionary.md, clean_table, model card, monitoring plan. Then re-running a stage "
            "never means re-doing the conversation."
        ),
        deep=(
            "Mature teams separate three metrics: business KPI (revenue, retention), statistical metric (effect size, "
            "confidence), model metric (AUC, RMSE). A model with better AUC that does not move the KPI is a fail. This "
            "separation is the backbone of Days 193-196 and of every experiment review you will attend."
        ),
        math="Effect size thinking: decide the minimum detectable effect (MDE) before collecting data. If churn is 5% and "
             "you expect a 0.2-point lift, you need a very large sample - Day 133 computes exactly how large.",
        visual=dict(type="flow", svg_key="crisp-dm", title="CRISP-DM as a loop",
                    caption="The arrows matter more than the boxes: evaluation sends you back to framing, and monitoring "
                            "sends you back to preparation as the world changes.",
                    nodes=["Business understanding", "Data understanding", "Data preparation", "Modelling",
                           "Evaluation", "Deployment"]),
    ),
    code=[
        dict(title="Write the problem statement as a Python contract and check it is testable",
             language="python", label="EXPLANATION",
             code='''# Day 3 : make the problem statement falsifiable, then fail loudly if it is not.

statement = {
    "decision_owner": "Head of Retention",
    "decision": "Which 2,000 at-risk customers get the winback offer this month",
    "population": "Active customers with no purchase in 60-120 days",
    "action": "Send a 10% winback coupon by email",
    "baseline": {"churn_rate": 0.052, "winback_rate": 0.011},
    "target": {"winback_rate": 0.016},          # +0.5 percentage points
    "horizon_days": 60,
    "cost_of_error": {"false_positive": "AED 45 discount lost",
                      "false_negative": "customer churns, ~AED 900 LTV lost"},
}

required = ["decision_owner", "decision", "population", "action", "baseline", "target", "horizon_days"]
problems = [k for k in required if not statement.get(k)]
if problems:
    raise ValueError(f"Problem statement incomplete: {problems}")

# A cheap sanity check that the target is not fantasy
lift_needed = (statement["target"]["winback_rate"] - statement["baseline"]["winback_rate"]) / statement["baseline"]["winback_rate"]
print(f"Required relative lift: {lift_needed:.0%}")
print(f"Cost asymmetry (FN/FP): {900 / 45:.0f}x -> favour recall over precision")

if lift_needed > 1.0:
    print("WARNING: >100% relative lift. Re-check the target before modelling.")
''',
             output='''Required relative lift: 45%
Cost asymmetry (FN/FP): 20x -> favour recall over precision
WARNING would trigger only above 100% lift; here the target is aggressive but plausible.''',
             line_by_line=[
                 "Line 3-14: the problem statement as data. Because it is a dict, we can validate it programmatically.",
                 "Line 5: a decision, not a topic. 'Reduce churn' would fail this line.",
                 "Line 6: population defines the rows you will actually model.",
                 "Line 10-11: baseline and target side by side - the target must be expressible as a delta from the baseline.",
                 "Line 14: cost of each error type. This drives metric choice later (Day 194).",
                 "Line 16-19: a guard clause - fail immediately if the brief is incomplete. In production this prevents silent garbage.",
                 "Line 22-23: derive the implied lift and the cost ratio; both change modelling decisions.",
             ]),
        dict(title="The project skeleton you will reuse for 275 days",
             language="bash", label="PRACTICE",
             code='''# Day 3 : one layout, every project. Create it once.
mkdir -p ds_project/{data/{raw,interim,processed},notebooks,src,models,reports,config}
cd ds_project

cat > README.md <<'EOF'
# <Project name>
## Decision this supports
## Data sources (+ snapshot date)
## How to run
## Results (+ dates)
EOF

python -c "import json,pathlib; pathlib.Path('config/config.json').write_text(json.dumps({'seed':42,'target':'churn'}, indent=2))"
tree -L 2 .    # (use `ls -R` on Windows)''',
             output='''ds_project
|-- README.md
|-- config/
|-- data/
|   |-- interim/
|   |-- processed/
|   `-- raw/
|-- models/
|-- notebooks/
|-- reports/
`-- src/''',
             line_by_line=[
                 "Line 2: raw is never edited; interim holds partial cleaning; processed is analysis-ready. This convention "
                 "saves you from the classic 'which CSV was the good one?' disaster.",
                 "Line 5-10: the README answers the four questions a reviewer asks first.",
                 "Line 12: a config file with a fixed seed and the target column name - reproducibility starts here.",
                 "Notebooks are for exploration; src/ holds the functions you reuse. Anything copied twice belongs in src/.",
             ]),
    ],
    mistakes=[
        dict(mistake="Starting with the dataset because it is available.",
             why="Availability bias produces projects nobody asked for; your portfolio then looks like tutorial work.",
             fix="Start from a decision; choose data only after the statement passes the seven-field check above."),
        dict(mistake="Defining 'churn' (or 'active', 'revenue') silently.",
             why="Every team has a different definition; the disagreement surfaces after the model is built.",
             fix="Write the definition in the problem statement and get it confirmed in writing."),
        dict(mistake="Treating the workflow as strictly linear.",
             why="Evaluation often invalidates assumptions from data understanding, and the loop back is where the real work is.",
             fix="Version each stage's artefact so returning to a previous stage costs minutes, not weeks."),
    ],
    debugging=[
        dict(symptom="The model is 'accurate' but nobody uses it.",
             cause="The output does not fit the decision (wrong population, wrong timing, no action attached).",
             fix="Replay the decision: at what moment does the owner need the list, and what exactly do they do with it?"),
        dict(symptom="Each rerun gives different labels for the same customers.",
             cause="Population filters depend on 'today' (e.g. 'last 60 days') without a fixed snapshot date.",
             fix="Freeze an as-of date in config and compute all windows relative to it."),
    ],
    practice=[
        dict(level="easy", task="Create the ds_project skeleton and commit an empty README with the four headings.",
             hint="Run the bash block above.", solution="Folder exists; README has Decision / Data / Run / Results."),
        dict(level="medium", task="Write a seven-field problem statement for a dataset you already have (titanic, tips, diamonds in resources/datasets_for_practice).",
             hint="Copy the dict structure from the code example and fill it honestly.",
             solution="A good answer names a stakeholder role and a concrete action, not 'predict survival'."),
        dict(level="hard", task="Take a vague brief - 'analyse our app reviews to improve the product' - and turn it into three candidate problem statements with different metrics.",
             hint="Vary the decision: prioritisation, alerting, or causal testing.",
             solution="E.g. triage (which complaints get engineering time), monitoring (alert on emerging complaint topic), causal (did 4.2 ship improve ratings?)."),
    ],
    challenge=dict(title="Kill one bad brief",
                   brief="Find a real vague data request (news article, job spec, your own project idea) and rewrite it to pass the seven-field validation, listing what you had to assume.",
                   deliverable="problem_statement.md with an assumptions section.",
                   stretch="Add the smallest experiment or query that would confirm your assumptions cheapest."),
    interview=[
        dict(q="Walk me through how you approach a new data science project.", level="intermediate", tag="process",
             a="Structure the answer on artefacts: problem statement with decision owner and baseline -> data dictionary "
               "and quality report -> analysis-ready table -> baseline model -> candidate models with cross-validation -> "
               "business validation -> deployment and monitoring. Mention one project where evaluation sent you back to framing."),
        dict(q="How do you define success before modelling?", level="intermediate", tag="metrics",
             a="Three layers: business KPI, statistical criterion (minimum detectable effect), model metric chosen by error "
               "cost. Name the error cost asymmetry explicitly - it justifies precision/recall trade-offs."),
        dict(q="What is data leakage and where does it usually enter?", level="advanced", tag="validation",
             a="Information available at training time that will not be available at prediction time. Common entries: "
               "target-derived features, fitting scalers on the full dataset, temporal splits done randomly, and join "
               "columns that encode the outcome. Day 166 and Day 195 give the defences."),
    ],
    real_world=("Consulting-style teams run a 'framing workshop' before any code: one page, decision owner present, "
                "success metric agreed, kill criteria stated. Adopt the same ritual for your portfolio projects and you "
                "will explain them better than most candidates."),
    production=["Snapshot input data with a date in the filename; downstream charts are then reproducible.",
                "Write the data dictionary as you discover it, not at the end.",
                "Log row counts at every stage: a join that silently dropped 30% of rows is the most common production bug."],
    recap=["Workflow stages each produce a named artefact.",
           "A testable problem statement names decision, population, action, baseline, target and horizon.",
           "Keep business, statistical and model metrics separate.",
           "Project skeleton: raw/interim/processed + src + notebooks + config with a seed."],
    revision=["CRISP-DM six stages", "Seven-field problem statement", "Three metric layers",
              "raw/interim/processed convention", "Cost of error asymmetry"],
    quiz=[
        dict(q="Which element makes a problem statement testable?",
             options=["A named baseline and a numeric target with a horizon",
                      "A named algorithm", "A large dataset", "A dashboard mock-up"],
             answer=0, explain="Without a baseline and target you cannot tell afterwards whether you succeeded."),
        dict(q="Where do most data science projects fail?",
             options=["Framing and stakeholder agreement", "Model selection", "GPU availability", "Library versions"],
             answer=0, explain="Technical failure is recoverable; wrong-question failure is not."),
        dict(q="What belongs in data/raw?",
             options=["Immutable copies of source data, never edited by hand",
                      "The cleaned analysis table", "Model checkpoints", "Notebook exports"],
             answer=0, explain="Raw must stay pristine so any cleaning step can be re-derived and audited."),
        dict(q="A stakeholder wants 'the most accurate model'. Which question best redirects them?",
             options=["Which decision does a prediction inform, and what does each error type cost?",
                      "Which model trains fastest?", "How much data do we have?",
                      "Should we use deep learning?"],
             answer=0, explain="Error costs determine the metric, and the metric determines the model choice."),
        dict(q="Why fix a random seed and an as-of date in config?",
             options=["So results are reproducible and comparable across reruns",
                      "Because Python requires it", "To make models more accurate", "To speed up training"],
             answer=0, explain="Reproducibility is a precondition for comparison, debugging and trust."),
    ],
    cards=[
        ("CRISP-DM stages", "Business understanding, data understanding, data preparation, modelling, evaluation, deployment."),
        ("Seven-field statement", "Owner, decision, population, action, baseline, target, horizon."),
        ("Three metric layers", "Business KPI, statistical criterion, model metric."),
        ("raw/interim/processed", "Never edit raw; interim is partial; processed is analysis-ready."),
        ("as-of date", "Freeze the reference date so time windows are reproducible."),
        ("kill criteria", "Written conditions under which you stop the project - decided before you start."),
    ],
    extension=["Modern practice adds model cards, data cards and monitoring plans as required artefacts (Days 264-266).",
               "Data contracts between teams replace informal 'ask the analytics engineer' habits (Day 268)."],
    project_link="Capstone Project 1 begins with exactly this framing exercise (Day 269).",
)

PACKS[4] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Your environment is a machine you will live in for 275 days - build it deliberately.",
    minutes=90,
    objectives=[
        "Install and verify Python, a package manager and VS Code.",
        "Explain what a virtual environment is and why global installs break projects.",
        "Create, activate, export and rebuild a project environment.",
        "Configure VS Code for Python data work (interpreter, extensions, formatting).",
        "Diagnose the three most common setup failures.",
    ],
    why=(
        "Ninety percent of beginner frustration in week one is environment trouble, not Python. Once environments are "
        "understood, 'it worked yesterday' becomes a solvable problem instead of a mystery."
    ),
    concept=dict(
        mode="authored",
        what=(
            "An environment is an isolated set of installed packages plus the Python interpreter that uses them. "
            "Tools: conda (manages Python versions and non-Python libraries), venv/uv (lightweight, standard), pip "
            "(installs Python packages), VS Code (editor) and Jupyter (notebook front-end)."
        ),
        why=(
            "Project A needs pandas 1.5; project B needs pandas 2.2. With one global environment, every upgrade breaks "
            "an older project. Isolation makes each project reproducible for you, for your teammates and for CI."
        ),
        how=(
            "Recommended flow: install Miniconda (or Anaconda if you prefer GUI), create an environment per project "
            "with a pinned Python version, install packages inside it, export the exact state to a file "
            "(environment.yml or requirements.txt), and commit that file - never the environment itself."
        ),
        intuition=(
            "Think of environments as labelled toolboxes. The interpreter is the worker, the packages are the tools, "
            "and the label on the box is the environment name shown in your terminal prompt."
        ),
        analogy=(
            "A shared kitchen vs your own kitchen: with one kitchen (global install), one cook's new gadget rearranges "
            "everyone's drawers. Separate kitchens (environments) let each recipe stay valid."
        ),
        internals=(
            "Activation puts the environment's bin/ (Scripts/ on Windows) first on PATH, so `python` and `pip` resolve "
            "inside the environment. Most 'pip installed but import fails' bugs are simply an inactive environment or a "
            "different interpreter selected in the editor."
        ),
        deep=(
            "For reproducibility you want determinism, not just a package list: pin versions, prefer lock files "
            "(conda-lock, uv.lock, pip-tools), and record the Python version. In production the environment is rebuilt "
            "from the lock file in CI, which is why Day 265 tests deployments instead of trusting them."
        ),
        math="No maths today - but note that package resolution is a constraint satisfaction problem, which is why "
             "conflicting pins produce the solver errors you will inevitably read.",
        visual=dict(type="diagram", svg_key="environments", title="Global vs isolated environments",
                    caption="Left: one global site-packages shared by all projects (fragile). Right: one environment per "
                            "project, each with its own pinned versions (reproducible).",
                    nodes=["Interpreter", "site-packages", "Project A env", "Project B env"]),
    ),
    code=[
        dict(title="Create, verify and export a project environment (conda + pip)",
             language="bash", label="SOURCE",
             code='''# Day 4 : the commands you will run on every new project.
conda --version                       # confirm conda is installed
conda create -n dsacademy python=3.11 -y
conda activate dsacademy              # prompt should now show (dsacademy)

python -c "import sys; print(sys.executable)"     # PROOF you are in the env
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib seaborn scikit-learn jupyterlab

# Record the exact state so anyone (including future you) can rebuild it
python -m pip freeze > requirements.txt
conda env export --from-history > environment.yml

# Rebuild from scratch later:
#   conda env create -f environment.yml
#   (or) python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt''',
             output='''(dsacademy) $ python -c "import sys; print(sys.executable)"
/home/user/miniconda3/envs/dsacademy/bin/python

# requirements.txt begins with lines like:
numpy==2.1.1
pandas==2.2.3
scikit-learn==1.5.2''',
             line_by_line=[
                 "Line 2: verify the tool before using it; if this errors, conda is not on PATH.",
                 "Line 3: one environment per project, Python version fixed explicitly. Pinning the version prevents "
                 "'works on my machine' surprises.",
                 "Line 4: activation. The prompt change is your visual confirmation.",
                 "Line 6: print sys.executable - the single best diagnostic for 'import cannot find package'. If the path "
                 "is not inside your env, activation or the editor interpreter is wrong.",
                 "Line 7-8: always call pip as `python -m pip`; it guarantees the pip that belongs to the active interpreter.",
                 "Line 11-12: export exact pins (pip freeze) and the minimal requested set (conda --from-history). "
                 "Commit both files.",
                 "Line 15-16: the rebuild commands - the real test of a reproducible environment is recreating it on a clean machine.",
             ]),
        dict(title="VS Code settings that prevent 80% of beginner problems",
             language="json", label="PRACTICE",
             code='''// .vscode/settings.json  (commit this file with your project)
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.exclude": { "**/__pycache__": true, "**/.ipynb_checkpoints": true },
  "jupyter.notebookFileRoot": "${workspaceFolder}",
  "notebook.output.textLineLimit": 30
}''',
             output="After saving: the status bar shows the selected interpreter, Ctrl+Shift+P > 'Python: Select Interpreter' "
                    "lists your environments, and saving a .py file auto-formats it.",
             line_by_line=[
                 "Line 3: pin the interpreter so the whole team (and CI) agrees on which Python runs the code.",
                 "Line 5: auto-format on save means diffs stay about logic, not style.",
                 "Line 7: hide cache folders - visual noise creates real mistakes when selecting files.",
                 "Line 8: run notebooks from the project root so relative data paths work when you move the project.",
             ]),
    ],
    mistakes=[
        dict(mistake="Installing packages globally 'because it is faster'.",
             why="Global installs become an untracked dependency soup; two projects will eventually conflict.",
             fix="One environment per project, pins exported to a file."),
        dict(mistake="Running `pip install` while the environment is not active.",
             why="pip installs into the interpreter it belongs to, so packages land somewhere invisible to your notebook.",
             fix="Always check `python -c \"import sys; print(sys.executable)\"` before installing."),
        dict(mistake="Committing the environment folder or .venv to Git.",
             why="Hundreds of megabytes, machine-specific binaries, and nothing actually reproducible.",
             fix="Commit requirements.txt / environment.yml; add .venv/ to .gitignore."),
    ],
    debugging=[
        dict(symptom="ModuleNotFoundError: No module named 'pandas' (but you installed it).",
             cause="Notebook/editor using a different interpreter from the one where you installed.",
             fix="Print sys.executable inside the notebook; compare with the install environment; select the interpreter in VS Code."),
        dict(symptom="conda activate does nothing or errors with 'shell not initialised'.",
             cause="Your shell was never initialised for conda, or you are in PowerShell without the hook.",
             fix="Run `conda init bash` (or zsh) and restart the terminal; alternatively use `conda run -n dsacademy python ...`."),
        dict(symptom="Solver errors / endless 'Solving environment' when installing.",
             cause="Conflicting version pins between channels or an old conda.",
             fix="Update conda, install fewer packages at once, or prefer pip inside the env for pure-Python packages."),
    ],
    practice=[
        dict(level="easy", task="Create an environment named dsacademy with Python 3.11, install pandas and verify with sys.executable.",
             hint="Follow the bash example line by line and paste the executable path as evidence.",
             solution="Evidence = the printed path contains /envs/dsacademy/."),
        dict(level="medium", task="Break it on purpose: deactivate, then try importing pandas. Then reactivate and retry. Explain what changed.",
             hint="The interpreter path is the only thing that changed.", solution="Deactivated: system python has no pandas -> ModuleNotFoundError."),
        dict(level="hard", task="Rebuild your environment from requirements.txt on a clean path (or a new env name) without touching your existing one.",
             hint="Use a new env name to avoid destroying your main env.", solution="Two envs, same package versions -> reproducibility demonstrated."),
    ],
    challenge=dict(title="Environment proof sheet",
                   brief="Produce a one-page report: OS, conda/python versions, environment name, package versions, and the two commands to rebuild it.",
                   deliverable="SETUP.md committed to your repo with the actual output pasted in.",
                   stretch="Add a shell script setup.sh that performs the whole install in one command."),
    interview=[
        dict(q="What is a virtual environment and why does it matter?", level="beginner", tag="tooling",
             a="An isolated interpreter + package set. It matters for reproducibility and dependency isolation: each project "
               "pins its own versions, so upgrading one project cannot break another, and CI can rebuild the same state."),
        dict(q="requirements.txt vs environment.yml?", level="intermediate", tag="tooling",
             a="requirements.txt is a pip pin list (usually `pip freeze`) - exact versions, Python-only. environment.yml is "
               "conda's export and can include the interpreter version, channels and non-Python libraries (e.g. CUDA-linked "
               "builds). Use conda for the base, pip inside for pure-Python packages, and commit both."),
        dict(q="How do you make a data project reproducible for a colleague?", level="intermediate", tag="tooling",
             a="Pin the interpreter and packages, seed randomness, snapshot the data (or document the exact query/extraction "
               "date), document the run order in a README, and keep notebooks restart-and-run-all clean."),
    ],
    real_world=("On real teams, onboarding time is dominated by environment setup. Teams that commit lock files and a "
                "setup script get new members productive in an hour; the rest lose a week. You will meet both cultures - "
                "be the person who brings the setup script."),
    production=["Never install packages at runtime in a deployed container; bake them into the image (Day 262).",
                "Pin versions for production, allow minor upgrades only via tested PRs.",
                "Keep a smoke-test command (`python -c \"import app\"`) in CI to catch broken environments in minutes."],
    recap=["Environments isolate interpreter + packages per project.",
           "Verify with sys.executable before installing anything.",
           "Export pins (requirements.txt / environment.yml) and commit them.",
           "Pin the editor interpreter and commit .vscode/settings.json."],
    revision=["conda create -n name python=3.11", "sys.executable diagnostic", "pip freeze export",
              "Never commit .venv", "Lock-file reproducibility"],
    quiz=[
        dict(q="You installed pandas but the notebook says ModuleNotFoundError. Most likely cause?",
             options=["The notebook is using a different interpreter",
                      "pandas is broken", "You need to restart your computer", "The CSV is missing"],
             answer=0, explain="Print sys.executable and compare with the interpreter where you installed pandas."),
        dict(q="Which file should be committed for reproducibility?",
             options=["requirements.txt / environment.yml", "The .venv folder", "The __pycache__ folder", "Your home directory"],
             answer=0, explain="Pin lists are small, portable and rebuildable; environment folders are not."),
        dict(q="Why is `python -m pip install X` preferred to bare `pip install X`?",
             options=["It guarantees the pip belonging to the active interpreter is used",
                      "It is faster", "It installs newer versions", "It avoids the internet"],
             answer=0, explain="Bare pip can resolve to another interpreter's pip on PATH - a classic silent failure."),
        dict(q="What is the main advantage of one environment per project?",
             options=["Upgrading one project cannot break another",
                      "It uses less disk space", "It makes code run faster", "It removes the need for tests"],
             answer=0, explain="Isolation prevents dependency conflicts across projects."),
        dict(q="Where should data paths be relative to?",
             options=["The project root, kept stable for notebooks and scripts",
                      "Your home directory", "The notebook's folder", "The Python install location"],
             answer=0, explain="Stable roots keep relative paths working when the project moves or runs in CI."),
    ],
    cards=[
        ("Environment", "Isolated interpreter + package set for one project."),
        ("sys.executable", "Prints which Python is running - the first diagnostic for import errors."),
        ("pip freeze", "Exports exact installed versions to requirements.txt."),
        ("conda env export --from-history", "Exports the minimal requested set (portable across platforms)."),
        ("Activation effect", "Puts the env's binaries first on PATH."),
        ("Reproducibility trio", "Pinned env + seeded randomness + data snapshot."),
    ],
    extension=["uv and pixi are modern fast alternatives to pip/conda for env + lock management (post-2023 tooling).",
               "Devcontainers let an entire team share one reproducible environment definition."],
    project_link="Every phase from here assumes this environment exists; Day 32's pipeline project documents it in a README.",
)

PACKS[5] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Jupyter is a laboratory notebook, not a production pipeline. Learn which one you are writing.",
    minutes=80,
    objectives=[
        "Explain Jupyter's cell/kernel architecture and the execution-order trap.",
        "Use magic commands and shell escapes productively.",
        "Install and manage packages from inside a notebook safely.",
        "Write a requirements file and a reproducible analysis header.",
        "Know when to move code out of a notebook into a script or module.",
    ],
    why=(
        "Notebooks are where you will do 90% of your exploratory work, and where you will silently create results that "
        "cannot be reproduced. Mastering their execution model turns that risk into an advantage."
    ),
    concept=dict(
        mode="authored",
        what=(
            "A notebook is a JSON file of cells (code, markdown, output) executed by a long-lived kernel process. "
            "State (variables, imported modules) lives in the kernel, not in the file - so the file alone does not "
            "describe how the results were produced."
        ),
        why=(
            "This separation is the root of the reproducibility problem: a notebook can display a chart that its stored "
            "code cannot recreate after a restart if cells were run out of order. It is also why notebooks are excellent "
            "for exploration and dangerous as pipelines."
        ),
        how=(
            "Discipline: (1) start every notebook with the setup header; (2) run top-to-bottom before sharing "
            "('Restart & Run All'); (3) keep reusable logic in src/ modules and import them; (4) clear outputs before "
            "committing if outputs contain sensitive data; (5) name notebooks in run order (01_, 02_)."
        ),
        intuition=(
            "The kernel is a whiteboard. Cells are notes added to the whiteboard in whatever order you like; "
            "'Restart & Run All' wipes the board and rewrites every note in order to prove the notes alone are enough."
        ),
        analogy=(
            "A laboratory notebook vs a factory line: lab notes capture experiments, including mistakes. A factory line "
            "must be deterministic and automatic. Using lab notes as a factory line is how 'works in my notebook' "
            "becomes an outage."
        ),
        internals=(
            "Each execution increments an execution_count; `In[]`/`Out[]` variables hold the history. ipykernel holds "
            "objects in memory, which is why large DataFrames persist and consume RAM until you restart. `%who` and "
            "`%who_ls` inspect what is live."
        ),
        deep=(
            "For anything scheduled or shared, convert notebooks with papermill/nbconvert, or graduate the logic into a "
            "module with a CLI entry point (Day 31). The mature pattern: notebooks for exploration and communication; "
            "src/ for logic; orchestration (cron, Airflow, GitHub Actions) calls the module."
        ),
        math="Notebooks give you the fastest feedback loop in data work. Value of a fast loop = more hypotheses tested "
             "per hour; that is why disciplined notebook use outperforms 'engineering purity' at exploration time.",
        visual=dict(type="diagram", svg_key="notebook-kernel", title="Notebook file vs kernel state",
                    caption="The file stores cells and outputs; the kernel stores variables. Out-of-order execution "
                            "creates a gap between what the file claims and what the kernel holds.",
                    nodes=["Cells (.ipynb JSON)", "Kernel process", "Variables in RAM", "Outputs stored in file"]),
    ),
    code=[
        dict(title="The reproducible analysis header - paste this at the top of every notebook",
             language="python", label="EXPLANATION",
             code='''# ---- 1. Environment ------------------------------------------------
import sys, platform, datetime as dt
print("python  :", sys.version.split()[0])
print("platform:", platform.platform())
print("run at  :", dt.datetime.now().isoformat(timespec="seconds"))

# ---- 2. Libraries -------------------------------------------------
import json, pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- 3. Reproducibility -------------------------------------------
RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)
pd.set_option("display.max_columns", 50)

# ---- 4. Paths (never absolute, never machine-specific) ------------
DATA = pathlib.Path("..") / "data"           # adjust once, use everywhere
RAW  = DATA / "raw"
print("data dir exists:", RAW.exists())

# ---- 5. Data version marker ---------------------------------------
dataset = RAW / "tips.csv"
print("dataset:", dataset.name, "| mtime:", dt.datetime.fromtimestamp(dataset.stat().st_mtime).date()
      if dataset.exists() else "dataset not found - copy tips.csv from resources/datasets_for_practice/")''',
             output='''python  : 3.11.9
platform: Linux-6.2.0-x86_64-with-glibc2.35
run at  : 2026-09-14T09:12:41
data dir exists: True
dataset: tips.csv | mtime: 2024-02-04''',
             line_by_line=[
                 "Line 2-5: record the environment and the run timestamp. When a result is questioned three weeks later, "
                 "this block answers 'what actually ran?'",
                 "Line 8-11: imports grouped together; no imports scattered mid-notebook (a common source of NameError after reordering).",
                 "Line 14-16: one random_state constant used by every step; genuine reproducibility, not aspirational.",
                 "Line 19-21: paths built with pathlib from a relative root; the notebook runs identically on any machine.",
                 "Line 24-27: print the dataset name and modification date - your data version marker in a world without a data catalog.",
             ]),
        dict(title="Magics and shell escapes worth knowing",
             language="python", label="SOURCE",
             code='''# Timing and profiling
%timeit sum(range(10_000))
%%time
total = sum(i**2 for i in range(1_000_000))

# Inspect the live kernel state
%who
%whos

# Shell escape: run terminal commands without leaving the notebook
!python --version
!pip list | head -5

# Versions, for the record
%load_ext watermark 2>/dev/null || True
# %watermark -v -p numpy,pandas,scikit-learn

# Rich display of the last expression
import pandas as pd
pd.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})''',
             output='''2.05 ms +/- 0.03 ms per loop (mean +/- std. dev. of 7 runs, 100 loops each)
CPU times: user 0.31 s, sys: 0.31 s, total: 0.62 s
Interactive namespace is empty.        # right after a restart - proves the kernel was clean
Python 3.11.9
   a    b
0  1  3.5
1  2  4.5''',
             line_by_line=[
                 "Line 2: %timeit runs many loops and reports variance - use it to compare implementations honestly.",
                 "Line 3-4: %%time for a single heavy block; note it is a cell magic (two percent signs).",
                 "Line 7-8: %who/%whos is your memory inspector; run it after a restart to confirm state is empty.",
                 "Line 11-12: ! escapes to the shell for quick checks; avoid for anything that must be reproducible.",
                 "Line 18-19: the last expression is displayed automatically - pandas renders tables as HTML.",
             ]),
    ],
    mistakes=[
        dict(mistake="Running cells out of order and trusting the output.",
             why="Outputs are stored in the file but can come from a code state that no longer exists.",
             fix="Restart & Run All before sharing or committing; treat any error as a real error, not as 'works anyway'."),
        dict(mistake="Putting important logic only in one notebook cell.",
             why="It cannot be tested, imported or scheduled, and it will eventually be duplicated.",
             fix="Move reused logic into src/module.py and import it; keep notebooks for orchestration and display."),
        dict(mistake="Committing notebooks with secrets or huge outputs.",
             why="API keys leak in outputs; big outputs break Git diffs and repository size.",
             fix="Keep keys in .env or environment variables; clear outputs (nbstripout) before committing."),
    ],
    debugging=[
        dict(symptom="NameError: name 'df' is not defined, even though you ran the cell earlier.",
             cause="Kernel restarted, or the defining cell was before an edit that reset execution.",
             fix="Restart & Run All; add a 'Run order' note at the top if the notebook needs cells in a specific sequence."),
        dict(symptom="Notebook becomes slow and RAM grows.",
             cause="Large objects retained in kernel state, often duplicates from repeated cells.",
             fix="Use %who to find them, `del` what you no longer need, restart the kernel for long sessions."),
        dict(symptom="import mymodule fails inside the notebook but works in the terminal.",
             cause="Notebook working directory differs from where the module lives.",
             fix="Set jupyter.notebookFileRoot to the workspace folder, or insert the project root into sys.path explicitly."),
    ],
    practice=[
        dict(level="easy", task="Paste the analysis header into a new notebook and make it print your environment and a valid data path.",
             hint="Point RAW at resources/datasets_for_practice if needed.",
             solution="Header prints python/platform/run-at and 'data dir exists: True'."),
        dict(level="medium", task="Create a cell that loads tips.csv, prints shape and total_bill mean, then run Restart & Run All and confirm the same output.",
             hint="Use pandas; keep the path relative.",
             solution="Second run reproduces identical numbers - your first reproducibility proof."),
        dict(level="hard", task="Convert today's exploration into a script (python explore.py) plus a thin notebook that imports and calls it.",
             hint="Move logic into functions with a main guard.",
             solution="Script prints the same metrics; notebook becomes three lines of orchestration."),
    ],
    challenge=dict(title="Notebook hygiene badge",
                   brief="Take any notebook you already have and make it pass: no absolute paths, seeded randomness, top-to-bottom clean run, outputs cleared, secrets absent.",
                   deliverable="The cleaned notebook plus a one-line note in README describing how to run it.",
                   stretch="Add nbstripout (or a git filter) so cleaning happens automatically."),
    interview=[
        dict(q="When would you use a notebook and when a script?", level="intermediate", tag="tooling",
             a="Notebook for exploration, visual iteration and communication; script/module for anything reused, tested, "
               "scheduled or deployed. The litmus test: if it must run the same way twice, it does not belong only in a notebook."),
        dict(q="What is the execution-order problem in notebooks and how do you mitigate it?", level="intermediate",
             tag="reproducibility",
             a="Kernel state persists across edits, so displayed outputs may not be reproducible from the saved file. "
               "Mitigations: restart-and-run-all before sharing, modularise logic into imports, and convert scheduled work "
               "into scripts with parameterised runs."),
        dict(q="How do you keep secrets out of notebooks?", level="beginner", tag="security",
             a="Never hardcode; load from environment variables or a .env file that is gitignored; clear outputs before "
               "committing; rotate any key that was ever committed because history retains it."),
    ],
    real_world=("In industry, notebooks are the shared language for exploration and review: `reports/` notebooks get read "
                "in meetings. The teams that keep them runnable (restart-and-run-all clean) can onboard anyone in a day."),
    production=["Anything scheduled must not depend on manual cell order - use papermill or a script.",
                "Never let production code import from a notebook; extract to a module and test it (Days 23, 265).",
                "Strip outputs before committing; artefacts (charts) belong in reports/ or a registry."],
    recap=["Notebooks store cells + outputs; kernels store state - reproducibility lives in that gap.",
           "Use a standard header: environment, imports, seed, paths, data version.",
           "Restart & Run All before sharing.",
           "Graduate reusable logic into src/ modules."],
    revision=["Kernel vs file state", "Restart & Run All", "%timeit vs %%time", "Analysis header", "Secrets hygiene"],
    quiz=[
        dict(q="Why can a notebook show results that its saved code cannot reproduce?",
             options=["Outputs are stored in the file while variables live in the kernel, so cell order matters",
                      "Jupyter compresses outputs", "Python caches everything by default", "The file is read-only"],
             answer=0, explain="Restart & Run All is the test that the file alone is sufficient."),
        dict(q="Which magic measures the runtime of a single heavy cell?",
             options=["%%time", "%timeit", "%who", "%load_ext"],
             answer=0, explain="%%time is a cell magic for one run; %timeit repeats a line many times for statistics."),
        dict(q="What is the best home for logic you will reuse in three notebooks?",
             options=["A module in src/ imported by each notebook", "A markdown cell with instructions",
                      "A copy-paste snippet", "A screenshot"],
             answer=0, explain="Importable code can be tested, versioned and reused without drift."),
        dict(q="Before committing a notebook that calls an external API, you should:",
             options=["Remove outputs containing keys and load secrets from environment variables",
                      "Compress the notebook", "Convert it to PDF", "Rename it"],
             answer=0, explain="Output cells frequently leak tokens; prevention is cheaper than rotating keys."),
        dict(q="What does %whos show?",
             options=["Variables currently alive in the kernel", "Installed packages", "The notebook's Git history",
                      "Cell execution times"],
             answer=0, explain="A quick memory/state inspector, useful before and after restarts."),
    ],
    cards=[
        ("Kernel vs file", "File stores cells+outputs; kernel stores live variables."),
        ("Restart & Run All", "Proves the saved code alone reproduces the outputs."),
        ("%timeit vs %%time", "Repeat many runs for statistics vs one run of a whole cell."),
        ("Analysis header", "Environment, imports, seed, paths, data version."),
        ("Secrets rule", "Environment variables + cleared outputs; rotate anything committed."),
        ("Notebook graduation", "Exploration stays; reusable logic moves to src/."),
    ],
    extension=["Repo-native notebook execution (papermill, jupyter nbconvert --execute) belongs in CI (Day 265).",
               "Modern IDEs run notebooks with a real kernel but full editor tooling - a middle path between notebook and script."],
    project_link="The Day 32 pipeline project and both capstones produce artefacts, not just notebooks.",
)

PACKS[6] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Python does not have variables like other languages: it has names bound to objects.",
    minutes=85,
    objectives=[
        "Explain name-object binding and why it matters for mutability bugs.",
        "Identify the core built-in types and choose the right one for data.",
        "Use type(), isinstance() and casting deliberately.",
        "Apply the full operator set including comparison chaining and precedence rules.",
        "Avoid the classic integer-division and floating-point surprises.",
    ],
    why=(
        "The mental model of names and objects explains the majority of confusing Python behaviour you will meet "
        "later: why two DataFrames change together, why default arguments 'remember' values, why `is` differs from `==`."
    ),
    concept=dict(
        mode="authored",
        what=(
            "A Python variable is a name in a namespace that refers to an object in memory. Assignment binds the name; "
            "it does not copy the object. Objects have a type, an identity and (usually) a value; some are mutable "
            "(list, dict, set, most custom objects) and some immutable (int, float, str, tuple, frozenset)."
        ),
        why=(
            "Data work is mostly transforming structures: summing numbers, grouping rows, joining tables. Choosing the "
            "right built-in type keeps code short and fast, and understanding mutability prevents the silent aliasing "
            "bugs that corrupt results - the worst kind of bug because the code still runs."
        ),
        how=(
            "Choose types by question: single value -> int/float/bool/str; ordered changing collection -> list; "
            "fixed record -> tuple; unique membership -> set; labelled lookup -> dict. For decimal money, decide "
            "explicitly between float and Decimal rather than by accident."
        ),
        intuition=(
            "Names are sticky notes with labels; objects are boxes. Assignment sticks a label on a box. Two names can "
            "have the same label on one box - which is why mutating 'through one name' changes what the other sees."
        ),
        analogy=(
            "A phone contact list: the name 'Ali' is a label; the phone number is the object. If Ali changes number "
            "(mutation), every label pointing to that contact shows the new number. Copying means writing a new contact entry."
        ),
        internals=(
            "CPython implements names as entries in a namespace dict mapping name -> pointer to a PyObject. Every object "
            "has an id, a type pointer and a reference count; `is` compares ids, `==` calls __eq__. Small integers and "
            "interned strings are cached, which is why `a is b` sometimes surprises you for values that look equal."
        ),
        deep=(
            "Reference counting plus a cycle collector explains memory behaviour: `del` removes a name, not necessarily "
            "the object. In pandas this is why `df2 = df1` (alias) and `df2 = df1.copy()` (independent) behave so "
            "differently - Days 50 and 53 turn it into practical rules."
        ),
        math=(
            "Numeric types have limits worth knowing: Python ints are arbitrary precision (no overflow, unlike NumPy "
            "int64) while floats are IEEE-754 binary64 with ~15-17 significant digits. 0.1 + 0.2 == 0.30000000000000004 "
            "is not a bug; it is binary representation. Day 45 covers the consequences for scientific computing."
        ),
        visual=dict(type="diagram", svg_key="name-object", title="Names bound to objects",
                    caption="Left: two names, two boxes (independent). Right: two names on one box (aliasing) - mutating "
                            "through either name changes what both see.",
                    nodes=["name 'a'", "name 'b'", "object [1, 2, 3]", "object (1, 2, 3) immutable"]),
    ),
    code=[
        dict(title="Names, objects, mutability - the experiment that makes it click",
             language="python", label="EXPLANATION",
             code='''# 1. Assignment binds a NAME to an OBJECT (no copy)
a = [1, 2, 3]
b = a                    # same object, two names
b.append(4)
print("a =", a, "| b =", b, "| a is b:", a is b)

# 2. Copying breaks the binding
c = a.copy()             # new object, same values
c.append(99)
print("a =", a, "| c =", c, "| a is c:", a is c)

# 3. Immutables cannot be mutated in place - assignment rebinds
x = 10
y = x
y = y + 1                # creates a NEW int object and rebinds y
print("x =", x, "| y =", y)

# 4. The nested-container trap that bites pandas users
matrix = [[0, 0], [0, 0]]
shallow = matrix.copy()          # outer list copied, INNER lists shared
shallow[0][0] = 7
print("matrix =", matrix, "  <-- inner list mutated through 'shallow'")

import copy
deep = copy.deepcopy(matrix)
deep[1][1] = 5
print("matrix =", matrix, "| deep =", deep)''',
             output='''a = [1, 2, 3, 4] | b = [1, 2, 3, 4] | a is b: True
a = [1, 2, 3, 4] | c = [1, 2, 3, 4, 99] | a is c: False
x = 10 | y = 11
matrix = [[7, 0], [0, 0]]  <-- inner list mutated through 'shallow'
matrix = [[7, 0], [0, 0]] | deep = [[7, 0], [0, 5]]''',
             line_by_line=[
                 "Line 2-5: b = a does not copy. Appending via b is visible through a, and `a is b` is True.",
                 "Line 8-10: .copy() is shallow - the outer container is new. `a is c` is False.",
                 "Line 13-16: ints are immutable, so y = y + 1 rebinds y to a new object; x is untouched.",
                 "Line 19-22: shallow copy still shares inner lists - the exact trap behind 'I updated a copy and the "
                 "original changed'. Note matrix changed even though we only touched `shallow`.",
                 "Line 24-27: deepcopy duplicates nested objects too; only then are the two structures independent.",
             ]),
        dict(title="Types, operators and the surprises worth remembering",
             language="python", label="EXPLANATION",
             code='''# Core types and truthiness
values = [42, 3.14, "data", True, None, [1, 2], {"k": 1}, {1, 2}]
for v in values:
    print(f"{str(v):12s} type={type(v).__name__:8s} truthy={bool(v)}")

# Division: / always returns float, // floors, % is remainder (sign follows divisor)
print(7 / 2, 7 // 2, 7 % 2, -7 // 2, -7 % 2)      # 3.5 3 1 -4 1

# Float representation is not a bug
print(0.1 + 0.2)                                   # 0.30000000000000004
print(round(0.1 + 0.2, 10) == 0.3)                 # True when you compare sensibly

# Comparison chaining and precedence
x = 5
print(0 < x < 10, x > 3 and x % 2 == 1)            # True True
print(2 + 3 * 4 ** 2)                              # 50 (** first, then *, then +)

# isinstance vs type: prefer isinstance for validation
print(isinstance(True, int))    # True  <- bool is a subtype of int! classic gotcha
print(True + True)              # 2''',
             output='''42           type=int      truthy=True
3.14         type=float    truthy=True
data         type=str      truthy=True
True         type=bool     truthy=True
None         type=NoneType truthy=False
[1, 2]       type=list     truthy=True
{'k': 1}     type=dict     truthy=True
{1, 2}       type=set      truthy=True
3.5 3 1 -4 1
0.30000000000000004
True
True True
50
True
2''',
             line_by_line=[
                 "Line 2-5: loop prints type and truthiness. Empty containers and None are falsy - the basis of `if not df.empty:` checks.",
                 "Line 8: / is true division, // floors toward negative infinity, % keeps the sign of the divisor. "
                 "This is why -7 // 2 is -4, not -3.",
                 "Line 11-12: binary floating point cannot represent 0.1 exactly. Compare with a tolerance (math.isclose) "
                 "or rounding, never with ==, for computed floats.",
                 "Line 15-16: chained comparisons read like maths (0 < x < 10). Precedence: ** before * before +.",
                 "Line 19-20: isinstance(True, int) is True because bool subclasses int - a real bug source when you "
                 "write isinstance checks for numeric validation.",
             ]),
    ],
    mistakes=[
        dict(mistake="Assuming `b = a` copies a list (or a DataFrame).",
             why="Assignment binds names; both names point at one object.",
             fix="Use .copy() for a shallow copy, copy.deepcopy() for nested structures; remember pandas has its own copy semantics."),
        dict(mistake="Comparing floats with == after arithmetic.",
             why="Binary representation makes exact equality unreliable after operations.",
             fix="Use math.isclose(a, b, rel_tol=1e-9) or compare rounded values."),
        dict(mistake="Using `is` to compare values.",
             why="`is` compares identity (memory), not equality; it works for None because None is a singleton.",
             fix="Use == for values, `is` only for None/True/False and identity checks."),
        dict(mistake="Trusting mutable default arguments: def f(x, items=[]).",
             why="The default list is created once and shared across calls - items accumulate forever.",
             fix="Default to None and create the container inside the function."),
    ],
    debugging=[
        dict(symptom="Changing a copy also changed the original structure.",
             cause="Shallow copy sharing inner objects, or plain assignment aliasing.",
             fix="Check with `a is b` and `a[0] is b[0]`; use deepcopy when nesting matters."),
        dict(symptom="A function 'remembers' values between calls.",
             cause="Mutable default argument.",
             fix="Change the signature to `def f(x, items=None)` then `items = [] if items is None else items`."),
        dict(symptom="Numeric results look slightly wrong in the last digits.",
             cause="Float representation error, or mixing int64 (NumPy) with Python ints (arbitrary precision).",
             fix="Use tolerances for comparisons; use Decimal for money; be explicit about dtypes in NumPy."),
    ],
    practice=[
        dict(level="easy", task="Predict the output of the aliasing block before running it, then verify. Write down which line surprised you.",
             hint="Track labels, not values.", solution="Expect a is b True; matrix mutated by shallow copy."),
        dict(level="medium", task="Write a function that takes a list of numbers and returns (min, max, mean) as a tuple, without using min/max functions.",
             hint="Loop once, track running values.", solution="running_min/running_max + total/len, returned as a tuple."),
        dict(level="hard", task="Demonstrate the mutable-default bug in 6 lines, then fix it, and write two sentences explaining the difference in bytecode-level terms (shared object vs new object).",
             hint="Call the buggy function three times and print the list.", solution="Buggy accumulates [1], [1,1], [1,1,1]; fixed version returns [1] each call."),
    ],
    challenge=dict(title="Type chooser cheat sheet",
                   brief="Write a decision table mapping 10 data questions (unique ids, fixed coordinates, tagged lookup, ordered scores...) to the correct built-in type with a one-line rationale.",
                   deliverable="types_cheatsheet.md with the table plus one code line each.",
                   stretch="Add the memory/perf note for each choice (e.g. set membership O(1) vs list O(n))."),
    interview=[
        dict(q="What happens when you write a = b for a list?", level="beginner", tag="internals",
             a="Both names reference the same object; no copy is made. Mutating through either name is visible through "
               "both. Copying requires b = a.copy() (shallow) or copy.deepcopy(a) (nested)."),
        dict(q="Difference between `is` and `==`?", level="beginner", tag="internals",
             a="`is` compares identity (same object in memory - same id), `==` compares value equality via __eq__. Use "
               "`is` for None/singletons, `==` for values. Note CPython caches small ints and interns some strings, so "
               "`is` can appear to work for values - a trap not a rule."),
        dict(q="Why is 0.1 + 0.2 != 0.3?", level="intermediate", tag="numerics",
             a="Floats are binary64; 0.1 and 0.2 have no exact binary representation, so the sum carries representation "
               "error. Practical rule: use tolerances (isclose) or Decimal for money; never exact equality on computed floats."),
        dict(q="Explain mutable default arguments.", level="intermediate", tag="gotchas",
             a="Defaults are evaluated once at function definition, so a mutable default is shared across calls and "
               "accumulates state. Use None as the sentinel and construct the container inside the body."),
    ],
    real_world=("Almost every 'impossible' pandas bug a beginner reports is an aliasing or view issue: a filtered "
                "DataFrame that silently modified the parent, or a chained assignment that only worked in an older "
                "pandas version. The name/object model is the cure."),
    production=["Make functions return new objects or document in-place mutation explicitly.",
                "Avoid mutable global state in pipelines; it makes parallel execution unsafe.",
                "For money, choose Decimal or integer minor units deliberately - floating point rounding accumulates into audit failures."],
    recap=["Assignment binds names to objects; it does not copy.",
           "Mutable (list/dict/set) vs immutable (int/float/str/tuple/frozenset).",
           "Shallow copy shares nested objects; deepcopy does not.",
           "/ is float division, // floors, % is remainder with divisor sign.",
           "Compare floats with tolerances; use `is` only for singletons."],
    revision=["Name-object binding", "Shallow vs deep copy", "Truthiness rules", "// and % semantics",
              "is vs ==", "Mutable default bug", "float representation"],
    quiz=[
        dict(q="After `a = [1,2]; b = a; b.append(3)`, what is `len(a)`?",
             options=["3 - both names reference the same list", "2 - assignment copies the list",
                      "1 - append replaces the list", "Error"],
             answer=0, explain="Assignment binds names to the same object."),
        dict(q="What does `matrix.copy()` do for a nested list?",
             options=["Copies the outer list only; inner lists remain shared",
                      "Deep copies everything", "Creates a tuple", "Raises an error"],
             answer=0, explain="It is a shallow copy - the exact source of 'my original changed' bugs."),
        dict(q="Which comparison is correct for two computed floats?",
             options=["math.isclose(a, b, rel_tol=1e-9)", "a is b", "a == b", "abs(a) == abs(b)"],
             answer=0, explain="Binary floating point representation error makes exact equality unreliable."),
        dict(q="What does `-7 % 2` evaluate to in Python?",
             options=["1", "-1", "0.5", "-3"],
             answer=0, explain="The result takes the sign of the divisor, unlike C-style implementations."),
        dict(q="Why is `isinstance(True, int)` True?",
             options=["bool is a subclass of int", "bool and int share memory", "It is a Python bug", "Because 1 == True"],
             answer=0, explain="A real gotcha when validating numeric inputs - check bool explicitly if it matters."),
    ],
    cards=[
        ("Assignment", "Binds a name to an object; never copies."),
        ("Shallow copy", "New outer container, shared inner objects."),
        ("Immutable types", "int, float, str, tuple, frozenset, None."),
        ("is vs ==", "Identity vs value equality; `is` only for singletons."),
        ("// and %", "Floor division and remainder; sign follows the divisor."),
        ("Mutable default", "Evaluated once - use None sentinel instead."),
    ],
    extension=["Typed numerics (Decimal/NumPy dtypes) become decision points in Phase 3 and in financial pipelines.",
               "Polars and Arrow-backed pandas change copy semantics; the model above still predicts their behaviour."],
)

PACKS[7] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Strings are the raw material of real datasets - most cleaning is string work.",
    minutes=85,
    objectives=[
        "Index and slice strings including negative indices and steps.",
        "Use the 12 string methods that cover most cleaning work.",
        "Format output with f-strings including alignment, precision and dates.",
        "Explain immutability and why string methods return new strings.",
        "Clean a realistic messy text column with method chaining.",
    ],
    why=(
        "Real data arrives as text: currency symbols, inconsistent casing, whitespace, unit suffixes, dates as strings. "
        "Days 59 and 70 (pandas string cleaning) are direct extensions of today."
    ),
    concept=dict(
        mode="authored",
        what=(
            "A str is an immutable sequence of Unicode characters. Immutability means every 'modifying' method returns a "
            "new string; the original is untouched. Strings support indexing, slicing, iteration, membership tests and a "
            "rich method library."
        ),
        why=(
            "Because text is the most common dirty type in practice. Parsing 'AED 1,299.00 ' into 1299.0 takes three "
            "operations; doing it safely for a million rows requires understanding both the methods and their failure modes."
        ),
        how=(
            "Cleaning recipe: strip whitespace -> normalise case -> remove/replace unwanted characters -> split or extract "
            "the numeric part -> cast with a fallback. Test each step on 5 hand-picked rows before applying to the column."
        ),
        intuition=(
            "A string is a chain of beads you cannot re-glue: you can look at any bead, cut a section out (slice returns a "
            "new chain), or build a new chain from the pieces. `upper()` builds a new chain rather than repainting beads."
        ),
        analogy=(
            "Text cleaning is like laundering: you cannot clean a shirt in place; each process (wash, dry, iron) returns a "
            "new state, and you check the garment after each step rather than after all three."
        ),
        internals=(
            "CPython strings are immutable arrays of Unicode code points with cached hash (so they can be dict keys). "
            "Concatenation in a loop is O(n^2) because each + creates a new string; use ''.join(parts) instead. "
            "Some short strings are interned (shared) for speed, which is why `is` can mislead on strings."
        ),
        deep=(
            "Unicode matters: len('café') can be 4 or 5 depending on normalisation form, and emoji are multi-code-point "
            "grapheme clusters. For robust pipelines, normalise with unicodedata.normalize('NFKC', s) before matching, and "
            "remember that CaseFolding differs from lower() for some languages."
        ),
        math="Alignment and precision in f-strings is formatting maths: {:>10.2f} means width 10, right-aligned, 2 decimals. "
             "You will use this constantly when printing tables in reports.",
        visual=dict(type="diagram", svg_key="string-slice", title="Indexing and slicing",
                    caption="Positive indices count from 0; negative from -1 at the end. Slices are start-inclusive, "
                            "stop-exclusive, and support a step - the same rules as lists and NumPy arrays (Day 10).",
                    nodes=["t  i  p  s  _  c  s  v", "0  1  2  3  4  5  6  7", "-8 -7 -6 -5 -4 -3 -2 -1"]),
    ),
    code=[
        dict(title="Indexing, slicing and the methods you will actually use",
             language="python", label="SOURCE",
             code='''s = "  Data Science with Python  "

print(s.strip())                      # remove surrounding whitespace
print(s.strip().lower())              # normalise case
print(len(s), len(s.strip()))         # length includes spaces!
print(s.strip()[0], s.strip()[-1])    # first / last character
print(s.strip()[0:4], s.strip()[5:12])# slicing: start inclusive, stop exclusive
print(s.strip()[::-1])                # step -1 reverses

title = "Data Science with Python"
print(title.split())                  # -> list of words
print(title.split(" ", 2))            # limit splits
print("-".join(title.split()))        # join back with a separator
print(title.replace("Python", "PyTorch"))
print(title.startswith("Data"), title.endswith("Python"))
print(title.find("Science"), "Science" in title)
print(title.count("a"), title.upper(), title.title(), title.swapcase())

# Cleaning pattern with chaining: read left-to-right like a sentence
messy = "   AED 1,299.00  "
amount = messy.strip().replace("AED", "").replace(",", "").strip()
print(amount, float(amount) + 1)''',
             output='''Data Science with Python
data science with python
28 23
D n
Data Scien
nohtyP htiw ecneicS ataD
['Data', 'Science', 'with', 'Python']
['Data', 'Science', 'with Python']
Data-Science-with-Python
Data Science with PyTorch
True True
5 True
2 DATA SCIENCE WITH PYTHON Data Science With Python dATA sCIENCE WITH pYTHON
1299.00 1300.0''',
             line_by_line=[
                 "Line 3-4: strip() removes leading/trailing whitespace only - interior spaces stay. lower() normalises case for comparisons.",
                 "Line 5: length counts spaces - a common source of wrong validation rules ('password too short' when it is only spaces).",
                 "Line 6: index 0 and index -1 (negative indexing counts from the end).",
                 "Line 7: slicing [start:stop] excludes stop. This rule is identical in lists, pandas .str accessor and NumPy arrays.",
                 "Line 8: [::-1] reverses via a negative step; note it makes a new string (immutability).",
                 "Line 11-13: split() -> list, join() -> string. The pair is the workhorse of text cleaning.",
                 "Line 17-18: find returns -1 when absent, `in` returns a bool - use `in` for existence, find/index when you need the position.",
                 "Line 22-24: chained cleaning reads like a pipeline: strip outer space, drop the currency label, remove thousands separators, then cast. "
                 "Cast only after cleaning; float('  AED 1,299.00 ') would raise ValueError.",
             ]),
        dict(title="f-strings: formatting that makes reports readable",
             language="python", label="EXPLANATION",
             code='''name, score, growth, price = "Ayesha", 0.8734, 0.1234, 1299.5
import datetime as dt

print(f"{name} scored {score:.1%}")                 # percentage, 1 decimal
print(f"{'Model':<12}{'AUC':>8}{'Lift':>10}")       # header with alignment
print(f"{'XGBoost':<12}{score:>8.3f}{growth:>9.1%}")
print(f"{price:,.2f}")                              # thousands separator
print(f"{name=} {score=}")                          # debug form (3.8+)
print(f"{dt.date(2026, 9, 14):%d %b %Y}")

rows = [("Logistic", 0.812), ("XGBoost", 0.873), ("LightGBM", 0.881)]
print("\\nLead model:", max(rows, key=lambda r: r[1])[0])
for model, auc in sorted(rows, key=lambda r: -r[1]):
    bar = "#" * int(auc * 40)
    print(f"{model:<10}{auc:>6.3f} {bar}")''',
             output='''Ayesha scored 87.3%
Model            AUC      Lift
XGBoost        0.873     12.3%
1,299.50
name='Ayesha' score=0.8734
14 Sep 2026

Lead model: LightGBM
LightGBM   0.881 ###################################
XGBoost    0.873 ##################################
Logistic   0.812 ################################''',
             line_by_line=[
                 "Line 4: :.1% multiplies by 100 and appends % - never hand-format percentages.",
                 "Line 5-7: <, > and ^ align left/right/centre within a width. Tables in plain print() become readable.",
                 "Line 8: , adds thousands separators; .2f fixes two decimals (money).",
                 "Line 9: the = specifier prints 'expression=value' - a fast debugging tool.",
                 "Line 10: date formatting with strftime-style codes inside f-strings.",
                 "Line 16-19: a text bar chart from string multiplication - zero-dependency visualisation for logs and READMEs.",
             ]),
    ],
    mistakes=[
        dict(mistake="Using + to build strings in a loop.",
             why="Each concatenation creates a new string; the loop becomes quadratic and slow on large data.",
             fix="Collect parts in a list and use ''.join(parts)."),
        dict(mistake="Comparing user-supplied strings without normalising.",
             why="'Lahore ' != 'lahore' for Python, so joins and groupbys fragment into duplicate categories.",
             fix="strip() + casefold() consistently at ingestion; do it once, at the boundary (Day 58)."),
        dict(mistake="Casting to float/number before cleaning.",
             why="Currency symbols, thousands separators and stray spaces raise ValueError.",
             fix="Clean to a numeric-shaped string first, then cast inside try/except with a documented fallback."),
        dict(mistake="Assuming len() counts visible characters for emoji/accented text.",
             why="Unicode can use multiple code points per perceived character (combining marks, emoji ZWJ sequences).",
             fix="Normalise with unicodedata and, for grapheme counting, use a library like grapheme (or accept code-point counts knowingly)."),
    ],
    debugging=[
        dict(symptom="ValueError: could not convert string to float: '1,299.00'",
             cause="Thousands separator or currency text still present.",
             fix="Inspect with repr(s) to expose hidden characters, then replace/clean before casting."),
        dict(symptom="Comparing two strings that look identical returns False.",
             cause="Invisible characters: non-breaking space (\\xa0), zero-width space, or different Unicode normalisation.",
             fix="print(repr(a), repr(b)) to reveal them; clean with unicodedata.normalize('NFKC', s).replace('\\xa0', ' ')."),
        dict(symptom="Text output is misaligned in the terminal.",
             cause="Variable-width characters or missing alignment specs.",
             fix="Use fixed-width f-string alignment; inspect with repr() when CJK/emoji are present."),
    ],
    practice=[
        dict(level="easy", task="Given '  Muhammad Aammar Tufail  ', print the cleaned full name, the initials (M A T), and the word count.",
             hint="split() then take [0] of each word and join, or use a comprehension.",
             solution="'M A T' via ' '.join(w[0] for w in name.split())."),
        dict(level="medium", task="Write a function clean_amount(text) -> float | None that handles 'AED 1,299.00', 'PKR 950', '', None, '12.5 USD', 'abc'.",
             hint="Use try/except and a regex-free replace approach first; then try regex.",
             solution="Strip non-numeric except dot and minus, then float() inside try/except returning None on failure."),
        dict(level="hard", task="Build a slug generator: 'Data Science & AI: 275 Days!' -> 'data-science-ai-275-days'.",
             hint="lower, replace non-alphanumerics with '-', collapse repeats, strip '-'.",
             solution="re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') - which previews Day 26 regex."),
    ],
    challenge=dict(title="Messy column rescue",
                   brief="Create a 10-row list of deliberately messy values (mixed currency, spacing, case, units) and write a single expression chain that normalises all of them.",
                   deliverable="A notebook cell with your chain, its output, and one sentence per step explaining the operation.",
                   stretch="Add a validation column: True only when the parsed value is a positive number below 1e6."),
    interview=[
        dict(q="Why are Python strings immutable, and what practical consequence does that have?",
             level="intermediate", tag="internals",
             a="Immutability allows safe sharing, hashing (dict keys) and thread safety. Practically, every 'modifying' method "
               "returns a new string, so loops that concatenate are quadratic - use join() instead."),
        dict(q="How do you clean a numeric column that arrives as messy text?", level="intermediate", tag="data-cleaning",
             a="Normalise unicode and whitespace, strip currency/unit text, remove thousands separators, then cast inside "
               "try/except with an explicit fallback. Validate the result (range, negatives) and log rows that failed."),
        dict(q="What is the difference between split() and partition()?",
             level="advanced", tag="essentials",
             a="split() returns a list (all parts, or n splits); partition() returns a 3-tuple (before, separator, after) and "
               "always yields three elements - useful for parsing a single delimiter safely."),
    ],
    real_world=("In production data engineering, string normalisation happens once at ingestion and is covered by tests, "
                "because inconsistent text produces duplicate categories that quietly corrupt every groupby, join and "
                "dashboard downstream."),
    production=["Do text normalisation at the boundary (ingestion) and document the rules in the data dictionary.",
                "Log the count of rows that failed parsing; silent drops are the most expensive data bug class.",
                "For international data, normalise Unicode consistently (NFKC) before matching, joining or hashing."],
    recap=["Strings are immutable sequences; every method returns a new string.",
           "Slicing rules: start inclusive, stop exclusive, optional step - identical across lists and arrays.",
           "strip/lower/split/join/replace cover most cleaning needs.",
           "f-strings handle alignment, precision, separators and dates.",
           "Join in a list rather than concatenating in a loop."],
    revision=["Slicing rules", "split vs join", "f-string format spec", "Unicode pitfalls", "Clean then cast"],
    quiz=[
        dict(q="What does 'Data Science'[5:12] return?",
             options=["'Science'", "'Scienc'", "'cience'", "'Data Sc'"],
             answer=0, explain="Index 5 is 'S'; the stop index 12 is exclusive, so 'Science'."),
        dict(q="Which is the efficient way to build a large string from many parts?",
             options=["Collect parts in a list and use ''.join(parts)", "Use += in a loop",
                      "Use f-strings in a loop with +", "Use str() on a list"],
             answer=0, explain="join allocates once; += in a loop is O(n^2) because strings are immutable."),
        dict(q="What is wrong with float('AED 1,299.00')?",
             options=["Raises ValueError - clean the text first", "Returns 1299.0 automatically",
                      "Returns None", "Works but loses precision"],
             answer=0, explain="Currency symbols and separators must be removed before casting."),
        dict(q="Which formatting shows 0.8734 as '87.3%'?",
             options=["f'{x:.1%}'", "f'{x:.1f}%'", "f'{x:%}'", "f'{x:.3}'"],
             answer=0, explain="The % spec multiplies by 100 and appends the sign; .1 controls decimals."),
        dict(q="Two visually identical strings compare unequal. The best first diagnostic is:",
             options=["print(repr(a), repr(b))", "print(len(a), len(b))", "a.strip() == b.strip()", "a.encode() == b.encode()"],
             answer=0, explain="repr exposes invisible characters like non-breaking space or zero-width space."),
    ],
    cards=[
        ("Slicing", "s[start:stop:step] - start inclusive, stop exclusive."),
        ("strip vs split", "strip removes ends; split breaks on a separator."),
        ("join", "separator.join(iterable) - the efficient way to build strings."),
        ("f-string spec", "{value:<10.2f} alignment, width, precision."),
        ("Immutability", "Methods return new strings; originals never change."),
        ("Parsing rule", "Clean to numeric shape first, then cast inside try/except."),
    ],
    extension=["Regex-based extraction (Day 26) generalises today's pattern parsing.",
               "Arrow/Unicode-aware tooling matters at scale; pandas .str uses Python-level string ops (Day 59 compares with Arrow)."],
)
