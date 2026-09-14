# The 275-day curriculum

Generated from `tools/index_data/phase_*.py` by `tools/build_docs.py`.

Tags: **SOURCE** = taught in the original recordings, **SOURCE + EXT** = covered partially then extended, **EXT** = academy extension (not in the original recordings).

## Phase 1 - Data Science + Python Foundations (Days 1-15)

*Goal:* Understand the field and become fluent in core Python.

*Source status:* Original course days 1-7 (intro, installation, Python programming).

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 1 | What is Data Science? | beginner | SOURCE | Definition of data science, The three pillars: statistics, computing, domain, Data science vs BI vs data analytics |
| 2 | Data Analyst vs Data Scientist vs ML Engineer vs AI Engineer | beginner | SOURCE | Four roles compared, Skill matrix and overlap, What each role does daily |
| 3 | The Data Science Workflow | beginner | SOURCE | CRISP-DM and its six phases, Problem framing before code, Data acquisition to deployment |
| 4 | Setting Up Your Python Environment | beginner | SOURCE | Installing Python and Anaconda, Conda environments explained, VS Code setup and extensions |
| 5 | Jupyter, Colab, Packages and Reproducibility | beginner | SOURCE | Notebook anatomy, cells and kernels, Jupyter vs Colab vs VS Code, Installing and managing packages |
| 6 | Variables, Data Types and Operators | beginner | SOURCE | Variables as names bound to objects, Core types: int, float, str, bool, NoneType, type(), isinstance(), casting |
| 7 | Strings in Depth | beginner | SOURCE | String literals and escapes, Indexing and slicing strings, Immutability |
| 8 | Lists and Tuples | beginner | SOURCE | List creation and mutability, append, extend, insert, pop, remove, Nested lists |
| 9 | Sets and Dictionaries | beginner | SOURCE | Set uniqueness and hash semantics, Union, intersection, difference, Dictionary as key-value store |
| 10 | Indexing and Slicing Mastery | beginner | SOURCE | Zero-based indexing, Negative indices, Slicing with start, stop, step |
| 11 | Conditions and Branching Logic | beginner | SOURCE | Boolean expressions and truthiness, if / elif / else, Ternary expressions |
| 12 | Loops and Iteration Tools | beginner | SOURCE | for loops over sequences, while loops and loop control, range, enumerate, zip |
| 13 | Functions, Arguments and Scope | beginner | SOURCE | Defining and calling functions, Positional, keyword, default, *args, **kwargs, Return values vs printing |
| 14 | Lambda, map, filter, Modules and Packages | intermediate | SOURCE | Anonymous functions, map and filter mental model, List vs generator expression |
| 15 | Exceptions, Debugging, Files, JSON and pathlib + Foundation Project | intermediate | SOURCE | try / except / else / finally, Reading and writing files safely, JSON serialisation |

## Phase 2 - Python for Data Work (Days 16-32)

*Goal:* Write professional, testable Python that handles real data files, APIs and repos.

*Source status:* Original course touched functions/modules and Git; testing, typing, logging, regex and packaging are academy extensions.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 16 | Object-Oriented Programming I: Classes and Objects | intermediate | SOURCE | Why OOP matters for data code, class, __init__, self, Instance vs class attributes |
| 17 | OOP II: Inheritance, Polymorphism and Dataclasses | intermediate | SOURCE | Inheritance and super(), Method overriding and polymorphism, Dunder methods: __repr__, __len__, __eq__ |
| 18 | Iterators and the Iteration Protocol | intermediate | SOURCE | Iterable vs iterator, __iter__ and __next__, StopIteration and loops |
| 19 | Generators and Lazy Evaluation | intermediate | SOURCE | yield and generator functions, Generator expressions, Streaming big files without loading RAM |
| 20 | Decorators | advanced | SOURCE | Functions as first-class objects, Closures and nonlocal, Writing your own decorator |
| 21 | Context Managers | advanced | SOURCE | with statement and resource safety, __enter__ / __exit__, contextlib.contextmanager |
| 22 | Type Hints and Modern Typing | advanced | ACADEMY EXTENSION | Why annotate code, Built-in generics: list[int], dict[str, float], Optional, Union, Literal |
| 23 | Testing Your Data Code with pytest | advanced | ACADEMY EXTENSION | Why tests save data pipelines, assert-based sanity checks, Writing your first pytest test |
| 24 | Logging Instead of Printing | advanced | ACADEMY EXTENSION | Why print() fails in production, logging levels and handlers, Formatting log records |
| 25 | Debugging Like a Professional | intermediate | SOURCE | Reading a traceback bottom-up, print-debugging discipline, breakpoint() and pdb commands |
| 26 | Regular Expressions for Data Cleaning | advanced | ACADEMY EXTENSION | Regex mental model: pattern -> match, Character classes and quantifiers, Groups, alternation and anchors |
| 27 | HTTP, APIs and requests | intermediate | SOURCE | Client-server model, HTTP verbs, status codes, headers, GET with query parameters |
| 28 | Web Data: JSON, HTML and Scraping with Pandas | intermediate | SOURCE | JSON structures and parsing, Nested JSON to DataFrame, HTML tables with pandas.read_html |
| 29 | datetime, timedelta and Time Zones | intermediate | SOURCE | datetime, date, time objects, Parsing strings into dates, Arithmetic with timedelta |
| 30 | Performance, Profiling and Refactoring | advanced | ACADEMY EXTENSION | Complexity intuition for data code, timeit and %timeit, Profiling with cProfile |
| 31 | Git, GitHub, Project Structure, CLI and Automation | intermediate | SOURCE | Git mental model and the three trees, commit, branch, merge, merge conflicts, Pushing to GitHub and pull requests |
| 32 | Python Data Pipeline Project and Mastery Assessment | advanced | SOURCE | Pipeline design: extract -> transform -> load, Config files and logging in a real project, Code review checklist |

## Phase 3 - NumPy + Scientific Computing (Days 33-48)

*Goal:* Manipulate n-dimensional arrays fast, and understand the maths they implement.

*Source status:* Original course days 28-32 (NumPy parts 1-3) plus linear algebra in Python.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 33 | Why NumPy and the ndarray | intermediate | SOURCE | The speed problem with Python lists, ndarray: contiguous typed memory, Creating arrays: array, zeros, ones, arange, linspace |
| 34 | Dimensions, Shape and Axes | intermediate | SOURCE | 0D to 3D+ arrays, shape, ndim, size, nbytes, Axis numbering and intuition |
| 35 | Data Types, Memory and Precision | advanced | SOURCE | dtype system: int8-64, float16-64, bool, unicode, Memory footprint calculation, Casting and astype |
| 36 | Indexing, Slicing and Views vs Copies | intermediate | SOURCE | Basic indexing and slices, Negative and step slicing, Views share memory, copies do not |
| 37 | Boolean Masking and Conditional Selection | intermediate | SOURCE | Comparison operators return boolean arrays, Mask-based filtering, np.where and np.select |
| 38 | Reshape, Flatten, Transpose and Concatenate | intermediate | SOURCE | reshape and -1 inference, flatten vs ravel (copy vs view), transpose and .T |
| 39 | Vectorisation: Thinking Without Loops | advanced | ACADEMY EXTENSION | What vectorisation really means at CPU level, Replacing loops with array expressions, Element-wise vs reduction operations |
| 40 | Broadcasting Rules | advanced | SOURCE | Broadcasting in three rules, Scalar and row/column broadcasting, Shape mismatch errors and how to read them |
| 41 | Aggregations and Axis Semantics | intermediate | SOURCE | sum, mean, std, min, max, argmin/argmax, axis=0 vs axis=1 demystified, keepdims and NaN-aware functions |
| 42 | Linear Algebra I: Vectors, Matrices and Products | advanced | SOURCE | Vector and matrix representation, Element-wise vs matrix product, np.dot vs @ operator |
| 43 | Linear Algebra II: Inverse, Solve and Determinant | advanced | SOURCE | Identity and inverse, np.linalg.inv and np.linalg.solve, Singular matrices and conditioning |
| 44 | Random Numbers and Simulation | advanced | ACADEMY EXTENSION | Why pseudo-randomness is reproducible, np.random.default_rng and Generator, Distributions: uniform, normal, binomial, poisson |
| 45 | Numerical Stability and Precision | advanced | ACADEMY EXTENSION | Floating point is not real arithmetic, Catastrophic cancellation, Log-sum-exp trick |
| 46 | Performance: Strides, Memory Layout and Speed Tricks | advanced | ACADEMY EXTENSION | C vs Fortran order and strides, Cache-friendly iteration, In-place operations |
| 47 | Scientific Computing Workflow + NumPy Project | advanced | SOURCE | Simulation project: physics-style data generation, Building a mini statistics engine with NumPy, Reproducible random seeds |
| 48 | NumPy Assessment and Consolidation | advanced | SOURCE | 40-question assessment, Five coding katas: masking, broadcasting, aggregation, linalg, simulation, Common errors recap |

## Phase 4 - Pandas + Data Cleaning + EDA (Days 49-70)

*Goal:* Load, clean, reshape and explore any tabular dataset with confidence.

*Source status:* Original course days 8-20 (Pandas parts 1-8, outliers, EDA) plus the pandas tips & tricks notebooks.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 49 | Series: The One-Dimensional Workhorse | intermediate | SOURCE | Series anatomy: values + index, Creating Series from lists and dicts, Alignment on index |
| 50 | DataFrame Anatomy | intermediate | SOURCE | Rows, columns and index, Building DataFrames from dicts and arrays, dtypes per column |
| 51 | Reading Data: CSV, Excel, JSON and SQL | intermediate | SOURCE | read_csv arguments you actually need, read_excel and sheet selection, read_json and normalisation |
| 52 | First Look: Profiling a Dataset | intermediate | SOURCE | head, tail, sample, info and describe, shape, columns, dtypes, memory_usage |
| 53 | Selection: loc, iloc, at, iat | intermediate | SOURCE | Label vs position based indexing, loc with slices and conditions, iloc with integers only |
| 54 | Filtering, Query and Sorting | intermediate | SOURCE | Boolean masks and &, ~, isin, between, str.contains |
| 55 | Sorting, Ranking and Ordering Business Data | intermediate | SOURCE | sort_values with na_position, rank methods: average, min, max, dense, Ties and business meaning |
| 56 | Missing Values: Detection and Strategy | intermediate | SOURCE | Why missingness is information, isna, notna, isna().sum(), MCAR, MAR, MNAR intuition |
| 57 | Imputation in Depth | advanced | SOURCE | Mean, median, mode imputation, Forward and backward fill for time series, Group-wise imputation |
| 58 | Duplicates and Inconsistent Values | intermediate | SOURCE | duplicated and drop_duplicates, Subset keys and keep strategies, Fuzzy near-duplicates |
| 59 | String Cleaning with the .str Accessor | advanced | SOURCE | Vectorised string methods, split, extract with regex, replace, contains, startswith |
| 60 | Categorical Data and dtype Optimisation | advanced | ACADEMY EXTENSION | Object vs category dtype, Memory savings measurement, Ordered categories |
| 61 | Datetime Handling in Pandas | advanced | SOURCE | to_datetime and errors='coerce', dt accessor: year, month, weekday, hour, date_range, Period, resample |
| 62 | GroupBy Fundamentals | advanced | SOURCE | Split-apply-combine, groupby on one and many keys, Iterating groups |
| 63 | Aggregation, Transform and Filter | advanced | SOURCE | agg with dicts and named aggregation, transform for shape-preserving ops, filter for group-level selection |
| 64 | apply, map, applymap and pipe | advanced | SOURCE | When to use map vs apply vs applymap, Row-wise apply and its cost, Vectorised alternatives to apply |
| 65 | Merge and Join | advanced | SOURCE | Relational thinking: keys, Inner, left, right, outer joins, Many-to-one and many-to-many |
| 66 | Concat and Combining DataFrames | advanced | SOURCE | Vertical vs horizontal concatenation, Index handling and ignore_index, Mismatched columns |
| 67 | Pivot and pivot_table | advanced | SOURCE | Long vs wide format, pivot vs pivot_table semantics, Aggregation functions in pivot_table |
| 68 | Melt, Stack, Unstack and Crosstab | advanced | ACADEMY EXTENSION | melt for tidying data, stack and unstack mechanics, Crosstab for frequency analysis |
| 69 | Rolling Windows, Shifts and Lag Features | advanced | SOURCE | rolling with window and min_periods, expanding and ewm, shift, diff, pct_change |
| 70 | Feature Engineering + Complete EDA Case Study | advanced | SOURCE | Feature types: numeric, categorical, datetime, text, Creating ratios, aggregates, flags, Encoding domain knowledge |

## Phase 5 - Data Visualization + Storytelling (Days 71-88)

*Goal:* Turn data into charts that change decisions, in matplotlib, seaborn and plotly.

*Source status:* Original course days 21-26 (visualization parts 1-2, plotly, animated plots, quiz).

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 71 | Visualization Principles and Chart Selection | intermediate | SOURCE | Purpose first: explore vs explain, Perceptual accuracy of encodings, Choosing chart type for the question |
| 72 | Matplotlib Anatomy: Figure and Axes | intermediate | SOURCE | Figure, Axes, Axis objects, pyplot vs object-oriented API, subplots and gridspec |
| 73 | Line, Bar and Scatter Plots | intermediate | SOURCE | plot(), bar(), scatter() mechanics, Line styles, markers, widths, Bar plot ordering and baselines |
| 74 | Histograms and Distribution Analysis | intermediate | SOURCE | Binning and bin width choice, hist, kde, ecdf, Comparing distributions across groups |
| 75 | Boxplots, Violin Plots and Outlier Communication | intermediate | SOURCE | Five-number summary visualised, IQR fences on the plot, Violin plots and density shapes |
| 76 | Scatterplots, Relationships and Bubble Charts | intermediate | SOURCE | Correlation visually, Overplotting and transparency, Bubble size encoding |
| 77 | Categorical Charts: Bars, Counts and Heatmaps | intermediate | SOURCE | Countplots and barplots, Stacked vs grouped bars, Ordering by value, not alphabet |
| 78 | Time Series Plots and Annotations | advanced | SOURCE | Datetime axis handling, Trend, seasonality and holiday bands, Annotating events on a chart |
| 79 | Storytelling with Data | advanced | SOURCE | Audience and decision framing, Headline, subtitle, caption structure, Annotation as narrative |
| 80 | Seaborn I: Relational Plots | intermediate | SOURCE | relplot and figure-level vs axes-level, Hue, size, style semantics, Faceting with col and row |
| 81 | Seaborn II: Distribution and Regression Plots | advanced | SOURCE | displot with multiple kinds, kdeplot bandwidth effects, histplot with hue and multiple |
| 82 | Seaborn III: Categorical Plots | advanced | SOURCE | boxplot, violinplot, boxenplot, barplot vs countplot, pointplot and catplot |
| 83 | Correlation and Heatmaps | advanced | SOURCE | Pearson vs Spearman vs Kendall, corr() and method selection, Masking the upper triangle |
| 84 | Pairplots and Multivariate Exploration | advanced | SOURCE | pairplot for quick multivariate scan, pairplot performance limits, jointplot with marginals |
| 85 | Plotly I: Interactive Charts | advanced | SOURCE | Why interactivity changes analysis, graph_objects vs express, Hover, zoom, legend interactions |
| 86 | Plotly II: Animated, Geo and Hierarchical Charts | advanced | SOURCE | Animation frames over time, Choropleth and scatter geo maps, Sunburst and treemap hierarchies |
| 87 | Interactive Dashboards with Plotly and Streamlit | advanced | SOURCE + EXTENSION | Dashboard layout thinking, Filters and cross-filtering, KPI tiles and drill-down |
| 88 | Visualization Project and Critique | advanced | SOURCE | Brief: executive dashboard for a retail dataset, Chart-by-chart justification, Before/after redesign exercise |

## Phase 6 - Mathematics for Data Science (Days 89-112)

*Goal:* Build the maths foundation (algebra, linear algebra, calculus, probability) needed by ML.

*Source status:* Original course Zero-to-Math series (number theory, pre-algebra, linear algebra parts 1-8) plus 05_mathematics notebook.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 89 | Why Mathematics and Number Sense | beginner | SOURCE | Math as the language of models, Arithmetic proficiency checks, Order of operations and percentages |
| 90 | Fractions, Ratios, Proportions and Percentages | beginner | SOURCE | Fractions and decimal equivalence, Ratios and rates, Percentage change, points and growth |
| 91 | Number Theory Essentials | intermediate | SOURCE | Natural, integer, rational, real, complex, Primes and factorisation, GCD and LCM |
| 92 | Pre-Algebra and Algebraic Manipulation | intermediate | SOURCE | Variables and expressions, Expanding and factorising, Solving linear equations |
| 93 | Equations, Inequalities and Linear Systems | intermediate | SOURCE | Linear equations in two variables, Inequalities and interval notation, Systems of equations: substitution and elimination |
| 94 | Functions and Graphs | intermediate | SOURCE | Function as a mapping, Domain, range, inverse, Linear, quadratic, exponential, sigmoid, ReLU |
| 95 | Exponents and Logarithms | intermediate | SOURCE | Exponent laws, Log as inverse of exponent, Log base e, 2 and 10 |
| 96 | Sequences, Series and Summation Notation | advanced | SOURCE | Arithmetic and geometric sequences, Sigma notation reading, Sum formulas and intuitions |
| 97 | Coordinate Geometry and Distances | intermediate | SOURCE | Cartesian plane and points, Slope, intercept and line equation, Euclidean and Manhattan distance |
| 98 | Vectors: Operations and Norms | advanced | SOURCE | Vector as ordered list and as arrow, Addition, subtraction, scalar multiplication, L1, L2, L-infinity norms |
| 99 | Dot Product, Angles and Projections | advanced | SOURCE | Dot product algebra and geometry, Cosine similarity, Orthogonality and correlation link |
| 100 | Matrices: Representation and Operations | advanced | SOURCE | Matrix notation and shapes, Addition, scalar multiplication, Transpose and symmetric matrices |
| 101 | Matrix Multiplication and Its Meaning | advanced | SOURCE | Inner-dimension rule, Manual multiplication walkthrough, Matrix x vector as transformation |
| 102 | Linear Transformations and Geometry | advanced | SOURCE | Transformation view: rotate, scale, shear, project, Basis vectors and how they move, Composition of transformations |
| 103 | Determinants and Volume | advanced | SOURCE | 2x2 determinant formula and geometry, 3x3 determinant and cofactor expansion, Determinant as area/volume scale factor |
| 104 | Matrix Inverse and Solving Linear Systems | advanced | SOURCE | Identity check for inverses, 2x2 inverse derivation, Gaussian elimination preview |
| 105 | Eigenvalues and Eigenvectors | advanced | SOURCE | Definition: Av = lambda v, Finding eigenvalues via characteristic polynomial, Eigenvectors as invariant directions |
| 106 | Eigen-Decomposition and Applications | advanced | SOURCE | Diagonalisation A = P D P^-1, Matrix powers and PageRank idea, Covariance eigen-structure -> PCA |
| 107 | Derivatives: Definition, Rules and Intuition | advanced | ACADEMY EXTENSION | Slope as instantaneous rate of change, Limit definition, Power, product, quotient and chain rules |
| 108 | Partial Derivatives and Gradients | advanced | ACADEMY EXTENSION | Functions of many variables, Partial derivative notation, Gradient as a vector of steepest ascent |
| 109 | Chain Rule and Backpropagation Preview | advanced | ACADEMY EXTENSION | Composition of functions, Chain rule single and multi variable, Computational graph intuition |
| 110 | Optimisation and Gradient Descent Mathematics | advanced | SOURCE | Minima, maxima, saddle points, Convexity and local minima, Gradient descent update rule |
| 111 | Probability Foundations | advanced | SOURCE | Sample space, events, axioms, Combining events: union, intersection, Conditional probability |
| 112 | Bayes, Random Variables and Distributions + Math for ML Capstone | advanced | SOURCE | Bayes theorem derivation and intuition, Random variables discrete and continuous, PMF, PDF, CDF |

## Phase 7 - Statistics (Days 113-134)

*Goal:* Describe data, quantify uncertainty and test hypotheses correctly.

*Source status:* Original course ABC of Statistics days 1-13 plus the 06_statistics notebooks (central tendency, distributions, tests, ANOVA, MANOVA, correlation, case study).

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 113 | What Statistics Is and Types of Data | beginner | SOURCE | Descriptive vs inferential statistics, Population vs sample, Nominal, ordinal, interval, ratio scales |
| 114 | Descriptive Statistics: Central Tendency | intermediate | SOURCE | Mean and its sensitivity to outliers, Median and robust centre, Mode for categorical data |
| 115 | Spread: Range, Variance and Standard Deviation | intermediate | SOURCE | Range and IQR, Variance formula and degrees of freedom, Population vs sample SD |
| 116 | Percentiles, Quartiles and the IQR | intermediate | SOURCE | Percentile definition and interpolation, Quartiles and five-number summary, IQR outlier rule |
| 117 | Skewness and Kurtosis | advanced | SOURCE | Symmetry detection, Positive and negative skew, Kurtosis and tail heaviness |
| 118 | Probability Distributions Overview | advanced | SOURCE | Discrete vs continuous distributions, PMF, PDF and CDF reading, Uniform, Bernoulli, binomial, Poisson, normal, exponential |
| 119 | The Normal Distribution and z-scores | advanced | SOURCE | Bell curve parameters mu and sigma, Empirical 68-95-99.7 rule, z-scores and standard normal table |
| 120 | Binomial and Bernoulli Distributions | advanced | SOURCE | Bernoulli trial, Binomial PMF and parameters, Mean and variance formulas |
| 121 | Poisson and Other Discrete Distributions | advanced | SOURCE | Poisson process assumptions, PMF and rate parameter lambda, Mean equals variance property |
| 122 | Sampling Methods and Bias | advanced | SOURCE | Why we sample, Simple random, systematic, stratified, cluster, Convenience and survivorship bias |
| 123 | Sampling Distributions | advanced | SOURCE | Statistic as a random variable, Distribution of the sample mean, Standard error and the sqrt(n) law |
| 124 | The Central Limit Theorem | advanced | SOURCE | Statement and conditions, CLT for means, proportions and sums, Simulation experiments with skew and small n |
| 125 | Standard Error and Confidence Intervals | advanced | SOURCE | Point estimate vs interval, SE formula for mean and proportion, 95 percent CI construction and interpretation |
| 126 | Hypothesis Testing Logic | advanced | SOURCE | Null and alternative hypotheses, One-tailed vs two-tailed, Test statistic and decision rule |
| 127 | p-values: What They Are and Are Not | advanced | SOURCE | Definition: probability of data given H0, Simulation-built intuition, p > 0.05 is not proof of no effect |
| 128 | Type I and Type II Errors, Power and Effect Size | advanced | ACADEMY EXTENSION | Error table, alpha, beta and power, Effect size: Cohen's d, eta squared |
| 129 | z-tests and t-tests | advanced | SOURCE | When to use z vs t, One-sample t-test, Independent two-sample t-test (Welch) |
| 130 | Paired Tests and Analysis of Variance (ANOVA) | advanced | SOURCE | Paired t-test and repeated measures, One-way ANOVA logic, F-statistic and between/within variance |
| 131 | Chi-Square Tests and MANOVA | advanced | SOURCE | Chi-square goodness of fit, Test of independence and contingency tables, Expected vs observed counts |
| 132 | Covariance and Correlation Deep Dive | advanced | SOURCE | Covariance and its units problem, Pearson r and its assumptions, Spearman and Kendall for ranks |
| 133 | A/B Testing in Practice | advanced | ACADEMY EXTENSION | Experiment design: hypothesis, metric, MDE, Randomisation and assignment, Sample size and duration calculation |
| 134 | Statistics Case Study and Assessment | advanced | SOURCE | Full case study on real data, Choosing tests defensibly, Reporting statistical findings |

## Phase 8 - SQL + Databases (Days 135-150)

*Goal:* Query relational databases fluently and pass SQL interviews.

*Source status:* ACADEMY EXTENSION. The original six-month recordings do not teach SQL; Codanics delivers it as a separate playlist. Practice database provided in resources/datasets_for_practice/database.sqlite.zip.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 135 | Databases and the Relational Model | intermediate | ACADEMY EXTENSION | Why SQL is non-negotiable for data roles, Tables, rows, columns, schema, Primary keys, foreign keys, constraints |
| 136 | SELECT, WHERE and ORDER BY | intermediate | ACADEMY EXTENSION | SELECT clause and projections, Aliases, WHERE with comparison and logical operators |
| 137 | Expressions, CASE and NULL Handling | intermediate | ACADEMY EXTENSION | Arithmetic and string expressions, CASE WHEN for conditional logic, Binning with CASE |
| 138 | Aggregate Functions, GROUP BY and HAVING | advanced | ACADEMY EXTENSION | COUNT, COUNT(*), COUNT(DISTINCT), SUM, AVG, MIN, MAX, GROUP BY rules |
| 139 | Joins I: Inner, Left, Right | advanced | ACADEMY EXTENSION | Join as key matching, INNER JOIN mechanics, LEFT JOIN and NULL rows |
| 140 | Joins II: Full, Cross, Self and Anti-Joins | advanced | ACADEMY EXTENSION | FULL OUTER JOIN, CROSS JOIN for combinations, SELF JOIN for hierarchies and comparisons |
| 141 | Subqueries: Scalar, Derived and Correlated | advanced | ACADEMY EXTENSION | Scalar subqueries in SELECT and WHERE, IN and EXISTS, Derived tables in FROM |
| 142 | CTEs and Modular SQL | advanced | ACADEMY EXTENSION | WITH clause syntax, Chaining multiple CTEs, Readable analytical pipelines |
| 143 | Window Functions I: Ranking | advanced | ACADEMY EXTENSION | OVER() and PARTITION BY, ROW_NUMBER, RANK, DENSE_RANK, NTILE, Top-N per group pattern |
| 144 | Window Functions II: Aggregates, Lags and Leads | advanced | ACADEMY EXTENSION | Running totals and moving averages, LAG and LEAD for trend analysis, FIRST_VALUE, LAST_VALUE, NTH_VALUE |
| 145 | Date and String Functions for Analytics | advanced | ACADEMY EXTENSION | Date parsing, truncation, difference, EXTRACT and date arithmetic, String concatenation, SUBSTRING, TRIM, REPLACE |
| 146 | Data Cleaning in SQL | advanced | ACADEMY EXTENSION | Detecting duplicates with window functions, Standardising categories with CASE and mapping, Trimming and casing text |
| 147 | Analytical SQL Patterns | advanced | ACADEMY EXTENSION | Cohort analysis with retention grids, Funnel analysis with CTEs, Customer segmentation queries |
| 148 | Indexes, Query Plans and Optimisation | advanced | ACADEMY EXTENSION | How indexes work (B-tree intuition), Composite indexes and column order, SARGable predicates |
| 149 | Normalisation, Transactions and ACID | advanced | ACADEMY EXTENSION | 1NF, 2NF, 3NF with examples, When to denormalise (warehouse star schema), Transactions and BEGIN/COMMIT/ROLLBACK |
| 150 | SQL Interview Sprint and Case Study | advanced | ACADEMY EXTENSION | 12 classic interview questions solved live, Query optimisation interview scenarios, Window function interview patterns |

## Phase 9 - Excel + Power BI + Tableau (Days 151-164)

*Goal:* Be dangerous in the BI stack that most employers actually use.

*Source status:* Original course Tableau series (Mar-Apr 2024) and Power BI for Beginners series (Apr-May 2024). Excel analytics is an academy extension.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 151 | Excel for Data Analysts: Structure, Cleaning and Formulas | intermediate | SOURCE | Workbook anatomy: sheets, cells, ranges, Named ranges and structured tables, Absolute vs relative references |
| 152 | Excel Formulas That Get You Hired | advanced | SOURCE | IF and nested IF vs IFS, SUMIFS and COUNTIFS with criteria, XLOOKUP vs VLOOKUP |
| 153 | Excel Text, Date Functions and PivotTables | advanced | SOURCE | TEXT, LEFT, RIGHT, MID, TRIM, CONCAT/TEXTJOIN, Date functions and date arithmetic, PivotTable fields, values, filters |
| 154 | Excel Power Query and Dashboard Case Study | advanced | SOURCE | Power Query as ETL: append, merge, unpivot, Refreshable data pipelines in Excel, Conditional formatting and KPI tiles |
| 155 | Power BI Fundamentals and Interface | intermediate | SOURCE | BI vs BI-adjacent tools, Install, update and settings, Report view, data view, model view |
| 156 | Power Query ETL in Power BI | advanced | SOURCE | Get Data and query steps, Promote headers, change types, remove errors, Append and merge queries |
| 157 | Data Modelling and Star Schema | advanced | ACADEMY EXTENSION | Fact vs dimension tables, Relationships, cardinality and direction, Star vs snowflake schema |
| 158 | DAX I: Calculated Columns and Measures | advanced | SOURCE | Row context vs filter context, Calculated column vs measure decision rule, Basic aggregations in DAX |
| 159 | DAX II: CALCULATE, FILTER and Time Intelligence | advanced | ACADEMY EXTENSION | CALCULATE as the heart of DAX, FILTER and ALL/REMOVEFILTERS, Time intelligence: YTD, MTD, SAMEPERIODLASTYEAR |
| 160 | Power BI Visuals, KPIs and Dashboard Design | advanced | SOURCE | Chart selection inside Power BI, KPI cards, gauges, matrix visuals, Slicers, drill-through, bookmarks |
| 161 | Tableau Fundamentals | intermediate | SOURCE | Tableau Public install and interface, Dimensions vs measures, Discrete vs continuous (green vs blue) |
| 162 | Tableau Calculated Fields, Filters and Sorting | advanced | SOURCE | Calculated field basics, Filters and context filters, Sorting, groups and sets |
| 163 | Tableau Charts, Dashboards and Stories | advanced | SOURCE | Bar, line, scatter, area, map, treemap, Dual axis and combined charts, Dashboard layout and device preview |
| 164 | BI Capstone: End-to-End Dashboard and Business Storytelling | advanced | SOURCE | Choose a business question and dataset, Model the data, Build the dashboard in Power BI or Tableau |

## Phase 10 - Machine Learning (Days 165-196)

*Goal:* Train, tune, evaluate and explain supervised models from first principles.

*Source status:* Original course Machine Learning-101 days 1-21 plus the 07_machine_learning notebooks and the bank-churn / diamond model comparisons.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 165 | What Machine Learning Actually Is | intermediate | SOURCE | Programs that learn from data, Supervised, unsupervised, self-supervised, reinforcement, Parametric vs non-parametric |
| 166 | The Supervised Learning Workflow and Data Leakage | advanced | SOURCE | Framing: X and y, Train, validation, test splits, Cross-validation preview |
| 167 | Preprocessing: Scaling and Encoding | advanced | SOURCE | Standardisation vs normalisation vs robust scaling, When distance-based models need scaling, One-hot, ordinal, target and binary encoding |
| 168 | Feature Engineering and Feature Selection | advanced | SOURCE | Feature creation from domain knowledge, Interaction and polynomial features, Binning and discretisation |
| 169 | Pipelines and ColumnTransformer | advanced | SOURCE | Why pipelines prevent leakage, Pipeline steps and naming, ColumnTransformer for mixed dtypes |
| 170 | Linear Regression I: Model and Mathematics | advanced | SOURCE | The line equation for many features, Ordinary least squares objective, Normal equation vs gradient descent |
| 171 | Linear Regression II: Assumptions and Diagnostics | advanced | ACADEMY EXTENSION | Linearity, independence, homoscedasticity, Normality of residuals, Multicollinearity and VIF |
| 172 | Gradient Descent in Machine Learning | advanced | SOURCE | Batch, stochastic, mini-batch, Learning rate schedules, Convergence diagnostics |
| 173 | Polynomial Regression | advanced | SOURCE | Capturing non-linearity by basis expansion, Degree selection and overfitting, Interaction terms |
| 174 | Regularisation: Ridge, Lasso and Elastic Net | advanced | SOURCE | Why regularisation works (bias-variance), L2 penalty and coefficient shrinkage, L1 penalty and sparsity |
| 175 | Beyond Least Squares: Robust, Bayesian, Quantile and Poisson Regression | advanced | ACADEMY EXTENSION | Huber and RANSAC for outliers, Bayesian linear regression and posterior coefficients, Quantile regression for prediction intervals |
| 176 | KNN Regression and Support Vector Regression | advanced | SOURCE | KNN: distance-based prediction, Choosing k and distance metric, Curse of dimensionality |
| 177 | Decision Tree Regression | advanced | SOURCE | Recursive binary splitting, Variance reduction criterion, Depth, min_samples and pruning |
| 178 | Random Forest Regression | advanced | SOURCE | Bagging and random feature subsets, Why averaging reduces variance, OOB score and feature importance |
| 179 | Bagging, Extra Trees and AdaBoost Regression | advanced | SOURCE | Bootstrap aggregation recap, Extra Trees randomness, Adaptive boosting: reweighting errors |
| 180 | Gradient Boosting Regression | advanced | SOURCE | Boosting as functional gradient descent, Residual fitting intuition, Shrinkage, subsample and depth |
| 181 | XGBoost Regression | advanced | SOURCE | Regularised objective and second-order approximation, Handling missing values natively, Key parameters: eta, gamma, lambda, alpha |
| 182 | LightGBM Regression | advanced | SOURCE | Histogram-based splitting, Leaf-wise growth vs level-wise, Leaf count and min_child_samples |
| 183 | CatBoost Regression | advanced | SOURCE | Ordered boosting and target leakage in categoricals, Oblivious trees, Native categorical handling |
| 184 | Regression Capstone: The Complete Model Bake-Off | advanced | SOURCE | Same data, ranking 16+ regression models, Leak-free preprocessing pipeline, Cross-validated comparison table |
| 185 | Classification: Logistic Regression | advanced | SOURCE | Why linear regression fails for classes, Sigmoid and log-odds, Maximum likelihood and log loss |
| 186 | KNN and Naive Bayes Classifiers | advanced | SOURCE | KNN classification and decision boundaries, Curse of dimensionality and scaling, Naive Bayes assumption and why it works |
| 187 | Decision Tree Classification and Interpretation | advanced | SOURCE | Gini and entropy criteria, Information gain computation, Tree depth and pruning strategies |
| 188 | Random Forest Classification and Feature Importance | advanced | SOURCE | Ensemble of trees for classification, Voting and probability averaging, Impurity vs permutation importance |
| 189 | Support Vector Machines | advanced | SOURCE | Maximum margin classifier, Support vectors and slack variables, C parameter and the margin trade-off |
| 190 | Gradient Boosting Classification | advanced | SOURCE | Log loss optimisation with trees, Binary and multiclass strategies, Early stopping and shrinkage |
| 191 | AdaBoost and XGBoost Classification | advanced | SOURCE | Adaptive reweighting for classifiers, SAMME algorithm intuition, XGBoost classifier specifics: scale_pos_weight |
| 192 | LightGBM and CatBoost Classification | advanced | SOURCE | LightGBM for imbalanced classification, CatBoost ordered boosting for categoricals, GPU training and prediction |
| 193 | Regression Metrics: MAE, MSE, RMSE and R2 | advanced | SOURCE | Absolute vs squared error trade-offs, RMSE units and interpretability, R2 definition and pitfalls |
| 194 | Classification Metrics and the Confusion Matrix | advanced | SOURCE | Confusion matrix layout and derived metrics, Accuracy paradox with imbalance, Precision, recall, F1 and F-beta |
| 195 | Cross-Validation, Tuning and Imbalanced Data | advanced | SOURCE | K-fold, stratified, grouped and time-series CV, GridSearchCV and RandomizedSearchCV, Halving search and nested CV |
| 196 | Explainability, Error Analysis and Model Comparison | advanced | SOURCE + EXTENSION | Global vs local explanation, Permutation importance and partial dependence, SHAP values intuition and plots |

## Phase 11 - Unsupervised ML + Time Series (Days 197-212)

*Goal:* Find structure without labels and forecast time series properly.

*Source status:* Original course unsupervised ML series (k-means, hierarchical, DBSCAN/OPTICS, GMM, PCA, SVD, t-SNE) and the time series / ARIMA / SARIMA / Prophet recordings.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 197 | Unsupervised Learning Landscape and Distance Metrics | advanced | SOURCE | Supervised vs unsupervised objectives, Similarity and distance families, Euclidean, manhattan, cosine, jaccard |
| 198 | K-Means Clustering: Theory and Mathematics | advanced | SOURCE | Objective: within-cluster sum of squares, Lloyd's algorithm steps, Convergence and local minima |
| 199 | K-Means in Practice: Choosing K | advanced | SOURCE | Elbow method and its weaknesses, Silhouette, Calinski-Harabasz, Davies-Bouldin, Inertia curve interpretation |
| 200 | Hierarchical Clustering | advanced | SOURCE | Agglomerative vs divisive, Linkage criteria: single, complete, average, ward, Dendrograms and cutting height |
| 201 | DBSCAN and OPTICS | advanced | SOURCE | Density-based clustering idea, Core, border and noise points, eps and min_samples selection |
| 202 | Gaussian Mixture Models, EM and Cluster Evaluation | advanced | SOURCE | Mixture of Gaussians model, Expectation-Maximisation walkthrough, Covariance types and model selection with BIC/AIC |
| 203 | Dimensionality Reduction and PCA Theory | advanced | SOURCE | Why reduce dimensions, Curse of dimensionality, Variance maximisation derivation |
| 204 | PCA in Practice | advanced | SOURCE | Scaling before PCA, Choosing components: scree plot and explained variance, Biplots and loadings interpretation |
| 205 | Singular Value Decomposition and Matrix Factorisation | advanced | SOURCE | A = U S V^T interpretation, Relationship between SVD and PCA, Low-rank approximation and Eckart-Young |
| 206 | t-SNE and UMAP | advanced | SOURCE | Manifold learning motivation, t-SNE perplexity and neighbourhood preservation, Why t-SNE distances are not global |
| 207 | Anomaly Detection | advanced | SOURCE + EXTENSION | Supervised vs unsupervised anomaly detection, Z-score and IQR baselines, Isolation Forest mechanics |
| 208 | Cluster Interpretation and Unsupervised Project | advanced | SOURCE | Naming and profiling clusters, Cluster-level statistics and personas, Business storytelling with clusters |
| 209 | Time Series Fundamentals and Components | advanced | SOURCE | Time series vs cross-sectional data, Trend, seasonality, cycle, irregular, Additive vs multiplicative decomposition |
| 210 | Time Series EDA, Stationarity and Autocorrelation | advanced | SOURCE | Datetime index and resampling, Rolling statistics and decomposition, Stationarity definition and tests (ADF, KPSS) |
| 211 | ARIMA and SARIMA | advanced | SOURCE | AR, MA, ARMA model intuition, ARIMA(p,d,q) parameters, Seasonal orders (P,D,Q,m) |
| 212 | SARIMAX, Prophet, Forecast Evaluation and Project | advanced | SOURCE | Exogenous variables in SARIMAX, Prophet components: trend, seasonality, holidays, Backtesting and rolling-origin evaluation |

## Phase 12 - Deep Learning + Computer Vision (Days 213-232)

*Goal:* Understand neural networks from a single neuron to a trained CNN.

*Source status:* Original course Deep Learning-101 days 1-8 (MLP, activations, CNN, computer vision, rice disease project, RNN) with PyTorch added as an extension.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 213 | Neural Networks from Zero: The Perceptron | advanced | SOURCE | Biological to artificial neuron analogy, Weighted sum and threshold, Perceptron learning rule |
| 214 | Neurons, Weights, Bias and Activation Functions | advanced | SOURCE | Linear layer mathematics, Bias as a shift, Step, sigmoid, tanh, ReLU, Leaky ReLU, softmax |
| 215 | Loss Functions | advanced | SOURCE | MSE and MAE for regression, Binary cross-entropy derivation, Categorical cross-entropy and softmax |
| 216 | Gradient Descent and Backpropagation | advanced | SOURCE | Computational graph of a network, Forward pass, Backward pass by hand for a 2-layer net |
| 217 | Network Architecture: Depth, Width and Capacity | advanced | SOURCE | Hidden layers and representation power, How many neurons per layer, Parameter counting |
| 218 | Overfitting, Regularisation, Dropout and Batch Norm | advanced | SOURCE | Underfitting vs overfitting learning curves, L1/L2 weight decay, Dropout mechanics and inference behaviour |
| 219 | PyTorch I: Tensors | advanced | SOURCE + EXTENSION | Tensor creation and dtypes, Devices: CPU vs CUDA, Broadcasting and operations |
| 220 | PyTorch II: Autograd | advanced | SOURCE + EXTENSION | requires_grad and computational graph, backward() and gradient accumulation, Detaching and no_grad |
| 221 | PyTorch III: nn.Module and the Training Loop | advanced | SOURCE + EXTENSION | Defining models with nn.Module, Layers: Linear, ReLU, Sequential, Loss functions and optimisers |
| 222 | PyTorch IV: Datasets, DataLoader, GPU and Checkpoints | advanced | SOURCE + EXTENSION | Custom Dataset class, DataLoader batching and shuffling, Moving data to GPU |
| 223 | Training Best Practices, Schedules and Monitoring | advanced | SOURCE | Learning rate finder and schedulers, Weight initialisation strategies, Tracking metrics with TensorBoard |
| 224 | Convolution: Filters, Stride, Padding and Feature Maps | advanced | SOURCE | Why convolution for images, Kernel as learned pattern detector, Stride, padding, dilation |
| 225 | Pooling, CNN Architectures and Design | advanced | SOURCE | Max and average pooling, Translation invariance, LeNet to ResNet evolution |
| 226 | Image Classification with PyTorch CNNs | advanced | SOURCE | Loading image datasets, Building a CNN in PyTorch, Training and validating |
| 227 | Data Augmentation | advanced | ACADEMY EXTENSION | Augmentation as regularisation, Geometric and photometric transforms, Augmentation pipelines in torchvision |
| 228 | Transfer Learning and Fine-Tuning | advanced | SOURCE | Feature extraction vs fine-tuning, Frozen layers and new heads, Learning rate strategies for fine-tuning |
| 229 | CNN Evaluation and Error Analysis | advanced | ACADEMY EXTENSION | Beyond accuracy: per-class precision/recall, Confusion matrix analysis, Grad-CAM visualisation |
| 230 | Recurrent Neural Networks | advanced | SOURCE | Sequential data and memory, RNN cell equations, BPTT and vanishing gradients |
| 231 | LSTM and GRU | advanced | SOURCE | Gates: forget, input, output, Cell state as long-term memory, GRU simplification |
| 232 | Sequence Modelling in PyTorch + Deep Learning Capstone | advanced | SOURCE | Embedding layers, Packing and padding sequences, Text and time-series RNNs in PyTorch |

## Phase 13 - NLP + Transformers + Hugging Face (Days 233-246)

*Goal:* Process text, then understand and fine-tune transformer models.

*Source status:* Original course covered NLP basics, sentiment analysis, LSTM/GRU and an intro to Hugging Face. Attention maths and transformer internals are academy extensions.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 233 | The NLP Pipeline and Text Preprocessing | intermediate | SOURCE | NLP task taxonomy, Corpus, documents, tokens, Cleaning: HTML, URLs, unicode, emoji |
| 234 | Tokenization: From Words to Subwords | advanced | SOURCE | Word, character and subword tokenization, Vocabulary size trade-offs, Byte-pair encoding (BPE) |
| 235 | Bag of Words and TF-IDF | advanced | SOURCE | Document-term matrix, CountVectorizer in sklearn, TF-IDF weighting and intuition |
| 236 | Word Embeddings | advanced | SOURCE | One-hot limits, Distributional hypothesis, Word2Vec CBOW and skip-gram |
| 237 | Sequence Models for Text | advanced | SOURCE | RNN/LSTM text classification end to end, Padding, masking and variable length, Bidirectional layers |
| 238 | The Attention Mechanism | advanced | ACADEMY EXTENSION | Bottleneck of fixed-size context vectors, Query, key, value formulation, Attention weights as soft alignment |
| 239 | Self-Attention and Multi-Head Attention | advanced | ACADEMY EXTENSION | Scaled dot-product attention maths, Why divide by sqrt(d_k), Multi-head attention |
| 240 | The Transformer Architecture | advanced | ACADEMY EXTENSION | Encoder-decoder structure, Positional encoding: sinusoidal and learned, Residual connections and layer norm |
| 241 | BERT and Encoder-Only Models | advanced | SOURCE | Masked language modelling, Next sentence prediction and its removal, BERT variants: RoBERTa, DistilBERT, DeBERTa |
| 242 | Generative Transformers and Decoding Strategies | advanced | ACADEMY EXTENSION | Decoder-only architecture and causal masking, GPT family scaling laws intuition, Greedy, beam, top-k, top-p sampling |
| 243 | Hugging Face: The Transformers Library | advanced | SOURCE | Hub, models and model cards, pipeline() for quick inference, AutoTokenizer and AutoModel classes |
| 244 | Hugging Face: Tokenizers and Datasets Libraries | advanced | ACADEMY EXTENSION | Fast tokenizers and offset mapping, Padding, truncation, attention masks, Loading and streaming datasets |
| 245 | Fine-Tuning a Transformer Classifier | advanced | SOURCE | Task setup and label mapping, Trainer API vs custom PyTorch loop, Learning rate, warmup, weight decay |
| 246 | NLP Evaluation, Error Analysis and Capstone | advanced | SOURCE + EXTENSION | Metrics per task: F1, EM, BLEU, ROUGE, perplexity, Confusion analysis for text, Slice analysis by length, domain, language |

## Phase 14 - Generative AI + LLMs + RAG (Days 247-258)

*Goal:* Engineer reliable LLM applications with retrieval, tools and evaluation.

*Source status:* Original course covered prompt engineering, Hugging Face, OpenAI APIs, LangChain and Streamlit chat-with-PDF apps. RAG evaluation, structured outputs and agent architecture are academy extensions.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 247 | Generative AI and LLM Fundamentals | advanced | SOURCE | GenAI: what generative AI means, LLM training stages: pretraining, SFT, RLHF/DPO, Model families and sizes |
| 248 | Tokens, Context Windows and Sampling Parameters | advanced | SOURCE | Tokenization effects on cost and behaviour, Context window budgets, Temperature, top-p, top-k, seed |
| 249 | Prompt Engineering | advanced | SOURCE | Prompt anatomy: role, task, context, format, constraints, System vs user vs assistant messages, Zero-shot, few-shot, chain-of-thought |
| 250 | Structured Outputs and Function Calling | advanced | ACADEMY EXTENSION | Why free text breaks pipelines, JSON schema and Pydantic validation, Function/tool calling flow |
| 251 | Embeddings and Semantic Search | advanced | SOURCE | Embedding space intuition, Sentence-transformer models, Cosine similarity retrieval |
| 252 | Vector Databases and Indexing | advanced | ACADEMY EXTENSION | Why vector databases exist, Flat, IVF, HNSW, PQ indexes, FAISS, Chroma, Pinecone, pgvector |
| 253 | Chunking and Document Processing | advanced | SOURCE | PDF and DOCX extraction, Fixed, recursive, semantic chunking, Chunk size and overlap trade-offs |
| 254 | RAG Architecture End to End | advanced | SOURCE | Why RAG instead of fine-tuning, Indexing pipeline vs query pipeline, Retriever + reranker + generator |
| 255 | RAG Evaluation, Hallucination and Grounding | advanced | ACADEMY EXTENSION | Faithfulness, answer relevance, context precision/recall, RAGAS-style evaluation, Golden datasets and regression testing |
| 256 | LangChain: Chains, LCEL and Memory | advanced | SOURCE | LangChain building blocks, Prompt templates and output parsers, LCEL composition with pipes |
| 257 | LangChain: Tools, Agents and Application Architecture | advanced | SOURCE | Tools as callable functions, ReAct agent loop, Agent executors and error handling |
| 258 | Safety, Reliability and the Document Intelligence Project Brief | advanced | SOURCE + EXTENSION | Prompt injection and jailbreaks, PII handling and data governance, Guardrails, moderation and allow-lists |

## Phase 15 - Deployment + MLOps + Data Engineering (Days 259-268)

*Goal:* Ship models as services and keep them healthy in production.

*Source status:* Original course covered Streamlit, Flask, FastAPI and an AWS EC2 deployment walkthrough. Docker, MLflow, CI/CD, monitoring, drift and PySpark are academy extensions.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 259 | Streamlit: Build and Deploy Data Apps | advanced | SOURCE | Streamlit execution model, Widgets, layout and state, Caching with st.cache_data |
| 260 | Flask and REST Fundamentals | advanced | SOURCE | WSGI and the request-response cycle, Routes, templates and static files, Form handling and JSON APIs |
| 261 | FastAPI and Pydantic | advanced | SOURCE | ASGI vs WSGI, Path, query and body parameters, Pydantic models and validation |
| 262 | Docker: Images, Containers and Dockerfiles | advanced | ACADEMY EXTENSION | Containers vs virtual machines, Dockerfile instructions, Building, tagging and running images |
| 263 | Docker Compose, Registries and Deployment | advanced | ACADEMY EXTENSION | Multi-service apps with Compose, Networking and service discovery, Pushing to a registry |
| 264 | MLflow: Experiment Tracking | advanced | ACADEMY EXTENSION | Reproducibility problem in ML, MLflow tracking server and runs, Logging params, metrics, artefacts and models |
| 265 | MLflow Registry, Testing and CI/CD | advanced | ACADEMY EXTENSION | MLOps: model registry stages and versions, Managing model lifecycle, Unit and integration tests for ML code |
| 266 | Monitoring, Logging, Data Drift and Model Drift | advanced | ACADEMY EXTENSION | MLOps monitoring: system, data, model, business, Data drift detection (PSI, KS, KL), Concept drift and delayed labels |
| 267 | PySpark and Distributed Data Processing | advanced | ACADEMY EXTENSION | When pandas stops scaling, Spark architecture: driver, executors, cluster, DataFrames, lazy evaluation, actions |
| 268 | Cloud and Production ML System Design | advanced | ACADEMY EXTENSION | Cloud mental model: compute, storage, network, AWS, GCP and Azure service mapping, Batch vs online vs streaming inference |

## Phase 16 - Capstone + Portfolio + Interview (Days 269-275)

*Goal:* Turn 268 days of skill into two portfolio projects and interview performance.

*Source status:* Original course included portfolio building (day 22), best-model presentations and Q&A sessions; this phase structures that into a job-readiness program.

| Day | Title | Difficulty | Source tag | Key topics |
|---|---|---|---|---|
| 269 | Capstone Project 1: Analytics + ML Dashboard (Architecture) | advanced | SOURCE + EXTENSION | Project brief: Olist e-commerce analytics, Architecture and folder structure, Data acquisition and SQL layer |
| 270 | Capstone Project 1: Build, Evaluate and Tell the Story | advanced | SOURCE + EXTENSION | Training and comparing models, Selecting the final model with business metrics, Building the dashboard (Power BI/Tableau/Streamlit) |
| 271 | Capstone Project 2: Document Intelligence RAG (Architecture) | advanced | SOURCE + EXTENSION | System requirements and SLAs, Architecture: ingestion, index, retrieval, generation, Technology choices and trade-offs |
| 272 | Capstone Project 2: Build, Evaluate, Deploy and Monitor | advanced | SOURCE + EXTENSION | Building the ingestion and indexing pipeline, Hybrid retrieval and reranking, FastAPI service + Streamlit UI |
| 273 | Portfolio, Resume and GitHub Presentation | advanced | SOURCE | Project selection and ordering, Resume bullets with impact metrics, GitHub profile and repository polish |
| 274 | Interview Marathon: SQL, Python, Statistics, ML, DL, NLP, RAG, MLOps, System Design | advanced | SOURCE + EXTENSION | Rapid-fire question banks per domain, Whiteboard coding patterns, Case interview frameworks |
| 275 | Mock Interview, Final Assessment and Job Readiness | advanced | SOURCE + EXTENSION | Full mock interview with scoring rubric, Final 100-question assessment, Job readiness checklist |
