"""Authored deep lessons - Phase 1, Days 12-15."""

PACKS = {}

PACKS[12] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Loops are for algorithms; vectorisation is for data. Learn loops properly to know when to leave them.",
    minutes=85,
    objectives=[
        "Write for and while loops with correct termination conditions.",
        "Use range, enumerate and zip to avoid index bookkeeping bugs.",
        "Control loops with break, continue and the often-forgotten for/else.",
        "Recognise when a loop over rows is the wrong tool.",
        "Bound nested-loop complexity and choose the right data structure to fix it.",
    ],
    why=(
        "Loops are how you write algorithms - and also how you accidentally write an O(n^2) pipeline over a million rows. "
        "Learning them well includes learning when to hand the work to NumPy or pandas instead."
    ),
    concept=dict(
        mode="authored",
        what=("A for loop iterates over any iterable (list, tuple, dict, string, file, generator, DataFrame column). "
              "A while loop repeats while a condition holds and must be made to terminate. Both support break (exit now), "
              "continue (skip to next iteration) and an else clause that runs only if the loop finished without break."),
        why=("Grouping, filtering and accumulating are loops underneath. Writing them explicitly teaches the mechanics; "
             "recognising the vectorised equivalent is what makes code fast enough for real data."),
        how=("Prefer `for item in iterable` over index arithmetic; add enumerate() when you need the index, zip() to walk "
              "two sequences together, and items() for dictionaries. Use while for unknown-iteration problems (convergence, "
              "retry, queue drain) with an explicit guard to avoid infinite loops."),
        intuition=("A loop is a conveyor belt: the body does one operation per item. The cost of the whole belt is "
                   "(work per item) x (number of items), so improving either factor improves everything."),
        analogy=("Tuning a radio: a for loop scans a known list of stations; a while loop keeps turning until the signal "
                 "matches (unknown number of turns) - and you need a maximum-turn guard so you do not burn out the dial."),
        internals=("for loop calls iter(obj) then next() until StopIteration. Each iteration in CPython is interpreted "
                   "bytecode, which is why a Python-level loop costs roughly 50-100 ns per simple iteration while a NumPy "
                   "array operation runs in compiled C over contiguous memory - often 20-100x faster."),
        deep=("Nested loops multiply: two loops over 10^4 items is 10^8 operations. The fix is structural, not stylistic - "
              "build a dict/set for lookup (Day 9), sort-and-sweep, or vectorise. Also note loop-carried dependencies "
              "prevent vectorisation; if each step needs the previous result, you must loop (or use cumulative functions "
              "like np.cumsum)."),
        math="Total work = iterations x cost per iteration. Estimating this before writing code is a professional habit: "
             "1e6 rows x 1e3 comparisons is a thousand million operations, which no amount of syntax sugar fixes - only a "
             "boundary change (hash lookup, vectorisation, database index) will.",
        visual=dict(type="flow", svg_key="pipeline", title="Loop cost = items x per-item work",
                    caption="Improving either factor improves throughput: reduce per-item work (vectorise, avoid lookups) or "
                            "reduce items (filter early, sample, aggregate at source).",
                    nodes=["Iterable", "Per-item work", "Accumulator", "Result"]),
    ),
    code=[
        dict(title="The four idioms that replace index bookkeeping",
             language="python", label="SOURCE",
             code='''sales = [220, 340, 180, 500]

# 1. Direct iteration (never use range(len(x)) unless you truly need the index)
total = 0
for amount in sales:
    total += amount
print("total:", total)

# 2. enumerate when you need position + value
for i, amount in enumerate(sales, start=1):
    print(f"row {i}: {amount}")

# 3. zip to walk two sequences together (stops at the shortest)
targets = [200, 300, 200, 450]
for amount, target in zip(sales, targets):
    status = "hit" if amount >= target else "miss"
    print(f"{amount} vs {target}: {status}")

# 4. dict iteration with .items()
regions = {"north": 120, "south": 90}
for name, amount in regions.items():
    print(name, amount)

# Accumulating into a dict (the most common analytics loop)
by_parity = {"even": 0, "odd": 0}
for amount in sales:
    by_parity["even" if amount % 2 == 0 else "odd"] += amount
print(by_parity)

# The vectorised equivalent - learn to see this
import numpy as np
arr = np.array(sales)
print("numpy sum:", arr.sum(), "| mean:", arr.mean(), "| >=200:", (arr >= 200).sum())''',
             output='''total: 1240
row 1: 220
row 2: 340
row 3: 180
row 4: 500
220 vs 200: hit
340 vs 300: hit
180 vs 200: miss
500 vs 450: hit
north 120
south 90
{'even': 720, 'odd': 520}
numpy sum: 1240 | mean: 310.0 | >=200: 3''',
             line_by_line=[
                 "Line 4-6: iterating the values directly is the clearest form; no indexes to get wrong.",
                 "Line 9-10: enumerate gives a counter; start=1 is handy for human-readable output (Excel-like row numbers).",
                 "Line 13-16: zip pairs two sequences; if lengths differ it silently stops at the shortest, so assert lengths first.",
                 "Line 19-20: iterating .items() yields (key, value) pairs - the standard pattern for configuration and lookups.",
                 "Line 23-25: building aggregates in a loop is the core of grouping; note how quickly this becomes a groupby in pandas (Day 62).",
                 "Line 28-29: the vectorised equivalents express the same intent without a loop - the mindset shift that Phase 3 formalises.",
             ]),
        dict(title="while loops, loop control, and the for/else that surprises everyone",
             language="python", label="EXPLANATION",
             code='''import time

# while: for convergence/retry problems where the count is unknown
balance, rate, years = 1000.0, 0.05, 0
while balance < 2000 and years < 40:      # ALWAYS include a second guard
    balance *= (1 + rate)
    years += 1
print(f"doubled after {years} years -> {balance:.2f}")

# break and continue
numbers = [4, -1, 7, 0, 12, -5]
for n in numbers:
    if n < 0:
        continue          # skip negatives
    if n > 10:
        break             # stop at the first value above 10
    print("processing", n)

# for/else: else runs only when no break occurred (search pattern)
def find_first_negative(values):
    for i, v in enumerate(values):
        if v < 0:
            print("found at index", i)
            break
    else:
        print("no negatives found")

find_first_negative(numbers)
find_first_negative([1, 2, 3])

# Retry loop with a hard limit - the production pattern
attempts = 0
while attempts < 3:
    attempts += 1
    ok = attempts == 2          # simulate: succeeds on the second try
    print(f"attempt {attempts} ok={ok}")
    if ok:
        break
else:
    print("all attempts failed - raise/alert")

# Nested loop with a cheap early exit: break the inner loop, guard the outer
pairs = 0
for a in range(50):
    for b in range(50):
        if a == b:
            break
        pairs += 1
print("pairs checked:", pairs, " (naive would be", 50*50, ")")''',
             output='''doubled after 15 years -> 2078.93
processing 4
found at index 1
no negatives found
attempt 1 ok=False
attempt 2 ok=True
pairs checked: 1225  (naive would be 2500)''',
             line_by_line=[
                 "Line 4-7: while with a compound condition includes a safety bound (years < 40) so a logic error cannot hang the process.",
                 "Line 10-16: continue skips the rest of the iteration; break exits the loop entirely. Order matters: check skip conditions before early exits.",
                 "Line 19-27: for/else separates 'found' from 'exhausted'. It is clearer than a found flag and shows up in binary search and validation code.",
                 "Line 30-38: the retry-with-limit pattern is exactly how production API calls are written (Day 27). The else clause is the alert path.",
                 "Line 41-46: nested loops can be pruned with early exits, but the structural fix for big data is a hash lookup or vectorisation - not more breaks.",
             ]),
    ],
    mistakes=[
        dict(mistake="Using range(len(x)) by reflex.",
             why="It adds index arithmetic, hurts readability and invites off-by-one errors.",
             fix="Iterate directly; add enumerate() when you need the index."),
        dict(mistake="Writing a while loop without a guaranteed exit.",
             why="A logic error hangs the process (or the notebook kernel) and burns time.",
             fix="Always include a bound (`while cond and attempts < MAX`) and log the iterations."),
        dict(mistake="Modifying a list while iterating over it.",
             why="Indexes shift, so elements are skipped silently.",
             fix="Iterate over a copy or build a new list with a comprehension."),
        dict(mistake="Looping over DataFrame rows with iterrows() for aggregation.",
             why="It is 100-1000x slower than the vectorised equivalent and loses dtypes.",
             fix="Use groupby/vectorised operations; if you must loop, use itertuples() and only on small slices."),
    ],
    debugging=[
        dict(symptom="The loop runs forever with no output.",
             cause="The condition never becomes false (missing increment, or comparing incompatible types).",
             fix="Add a counter and print it every N iterations; add a hard iteration cap while debugging."),
        dict(symptom="Results are correct but the script takes hours.",
             cause="Nested loop with a membership test (O(n^2)).",
             fix="Build a set/dict for O(1) lookups; measure before and after with time.perf_counter."),
        dict(symptom="for/else prints 'not found' even though it was found.",
             cause="Using `return` or a flag inside the loop instead of break, so else still runs.",
             fix="Use break for the found case; the else clause triggers only on exhaustion."),
    ],
    practice=[
        dict(level="easy", task="Sum all even numbers between 1 and 100 using a loop, then verify with sum(range(2, 101, 2)).",
             hint="Accumulator plus a condition, or a step in range.", solution="Both give 2550."),
        dict(level="medium", task="Given two lists of customer ids, print the ids present in both using ONE loop and set membership.",
             hint="Build a set from one list, then loop the other.", solution="O(n) instead of O(n^2) - the standard interview framing."),
        dict(level="hard", task="Implement a retry loop that calls a function returning random success/failure, retries up to 5 times with increasing sleep, and raises a clear error if all attempts fail.",
             hint="while/else plus exponential backoff (0.1 * 2**attempt).", solution="Prints attempts, sleeps between them, raises RuntimeError with the last error."),
    ],
    challenge=dict(title="Loop versus vector: measured",
                   brief="Compute the mean, median and count above threshold for 1e6 random numbers twice: once with a Python loop and once with NumPy. Report both timings and the speed-up.",
                   deliverable="A notebook cell with both implementations, timings, and identical results asserted.",
                   stretch="Extend to grouping by a category column and compare with pandas groupby."),
    interview=[
        dict(q="When would you use a while loop instead of a for loop?", level="beginner", tag="control-flow",
             a="When the number of iterations is unknown: convergence, retry with backoff, draining a queue, reading a stream. "
               "Always add an upper bound so a logic error cannot hang the process."),
        dict(q="What does the else clause on a for loop do?", level="intermediate", tag="gotchas",
             a="It runs only if the loop completed without break - the idiom for 'not found' branches in search algorithms."),
        dict(q="How do you speed up a nested loop in a data pipeline?", level="intermediate", tag="performance",
             a="First remove the quadratic behaviour: build a dict/set for O(1) lookups, or join in SQL/pandas. Then vectorise "
               "with NumPy/pandas if the operation is elementwise. Measure both versions to prove the gain."),
        dict(q="Why is iterating pandas rows considered bad practice?", level="advanced", tag="performance",
             a="iterrows boxes each value into Python objects and rebuilds a Series per row, losing dtype efficiency; it is "
               "100-1000x slower than vectorised ops. Use itertuples or, better, a vectorised/grouped formulation."),
    ],
    real_world=("Batch jobs that 'work on the sample, fail on production' are usually loops whose per-iteration cost was fine "
                "for 1,000 rows and fatal for 50 million. Estimating work before coding is a senior habit you can start today."),
    production=["Always bound loops in production code (max iterations, timeouts) and log progress for long jobs.",
                "Prefer chunked processing with progress logging over one giant loop that gives no feedback.",
                "If a job takes longer than expected, profile before optimising syntax: the problem is usually algorithmic."],
    recap=["Iterate iterables directly; use enumerate and zip to avoid index bookkeeping.",
           "while loops need an explicit termination guard.",
           "break exits, continue skips, for/else handles the exhausted case.",
           "Loop cost = items x per-item work; fix the bigger factor first.",
           "Avoid row-wise loops on DataFrames - vectorise or group instead."],
    revision=["enumerate/zip", "break/continue/else", "bounded while", "O(n^2) detection", "vectorised equivalent"],
    quiz=[
        dict(q="Which loop form gives both index and value?",
             options=["for i, v in enumerate(items)", "for i in range(len(items))", "for v in items", "while items"],
             answer=0, explain="enumerate yields (index, value) pairs; you can set start=1 for human numbering."),
        dict(q="When does a for loop's else block execute?",
             options=["When the loop finishes without hitting break", "Always after the loop",
                      "Only when the loop body raises", "Never in Python 3"],
             answer=0, explain="It is the 'not found' branch in search loops."),
        dict(q="What is the complexity problem with `for a in list_a: if a in list_b:` for large lists?",
             options=["It is O(n*m) - use a set for O(n+m)", "It is O(1)", "It is fine because Python is fast",
                      "It only affects memory"],
             answer=0, explain="Membership on a list is O(n); with a set it becomes O(1) per lookup."),
        dict(q="`zip(a, b)` with len(a)=5 and len(b)=3 yields:",
             options=["3 pairs - it stops at the shortest", "5 pairs with padding", "Error", "8 pairs"],
             answer=0, explain="Zip truncates silently; assert equal lengths when that would be a data error."),
        dict(q="Which is the production-safe retry pattern?",
             options=["while attempts < MAX with backoff and an alert on exhaustion",
                      "while True until it works", "Recursive retry without a base case", "for _ in range(inf)"],
             answer=0, explain="Bounded retries with backoff prevent infinite loops and thundering-herd behaviour."),
    ],
    cards=[
        ("enumerate", "Index plus value without index bookkeeping."),
        ("zip", "Walk two sequences together; truncates to the shortest."),
        ("for/else", "Executes only when no break occurred."),
        ("Bounded while", "Always include a maximum iteration guard."),
        ("Loop cost", "items x per-item work - optimise the dominant factor."),
        ("Vectorise instead", "NumPy/pandas replace row loops at 20-100x speed."),
    ],
    extension=["itertools (chain, product, combinations, groupby) replaces many hand-written loops (Day 19).",
               "Cython/Numba compile hot loops when a genuine loop-carried dependency blocks vectorisation (Day 46)."],
)

PACKS[13] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="A function is a contract: given these inputs, I promise this output and this behaviour.",
    minutes=90,
    objectives=[
        "Define functions with clear names, parameters and return values.",
        "Use positional, keyword, default and variadic arguments correctly.",
        "Avoid mutable default arguments and understand why they break.",
        "Apply LEGB scope rules and avoid accidental global state.",
        "Write docstrings that make a function usable without reading its body.",
    ],
    why=(
        "Functions are the unit of reuse and the unit of testing. Code that cannot be extracted into a testable function "
        "cannot be trusted in a pipeline - and every professional habit from here (modules, tests, pipelines) builds on them."
    ),
    concept=dict(
        mode="authored",
        what=("A function is a named, reusable block that takes inputs (arguments), performs work, and returns a value "
              "(None if no return statement runs). Python functions are first-class objects: they can be assigned, passed "
              "and returned - the property that makes decorators, map/filter and pipelines possible."),
        why=("Duplication is where bugs breed: fix one copy, forget the other. Functions also create the boundary needed for "
             "testing, documentation and profiling. A data pipeline is best understood as a series of small functions."),
        how=("Definition: def name(params) -> return_type with a docstring. Arguments: positional, keyword with defaults, "
             "*args (extra positional tuple), **kwargs (extra keyword dict), and keyword-only parameters after *. Return "
             "early; return multiple values as a tuple. Keep one responsibility per function (do one thing)."),
        intuition=("A function is a machine with an input hopper and an output chute. Parameters are the hopper design; the "
                   "return value is the chute. If a function both cleans and trains a model, the machine has two chutes and "
                   "you can never test either properly."),
        analogy=("A recipe card: the ingredients list is the signature, the method is the body, and the dish is the return "
                 "value. A good card lets another cook produce the same dish without asking you questions - that is what a "
                 "docstring achieves."),
        internals=("Calling a function creates a frame containing local names, arguments and the return address; names resolve "
                   "by LEGB: Local, Enclosing, Global, Built-in. Default values are evaluated once at definition time and "
                   "stored on the function object (__defaults__), which is exactly why mutable defaults break. Recursion depth "
                   "is limited (~1000) because each call adds a frame."),
        deep=("Closures let an inner function capture enclosing variables - the mechanism behind decorators (Day 20) and "
              "partial application (functools.partial). For data code, the highest-value patterns are: pure functions "
              "(no hidden state) for transforms, factory functions that return configured objects, and generators (Day 19) "
              "when returning a whole list would waste memory."),
        math="A pure function is a mathematical function: same input always yields the same output with no side effects. "
             "Purity is what makes caching (lru_cache) and parallel execution safe - both appear in production ML code.",
        visual=dict(type="diagram", svg_key="pipeline", title="Function as a contract",
                    caption="Inputs -> documented behaviour -> returned value. Documented exceptions are part of the contract: "
                            "callers must know what failure looks like.",
                    nodes=["arguments (typed)", "function body (one job)", "return value", "documented exceptions"]),
    ),
    code=[
        dict(title="Arguments in all their forms, with the traps made explicit",
             language="python", label="SOURCE",
             code='''def clean_amount(text: str, currency: str = "AED", *, strip_commas: bool = True) -> float | None:
    """Parse a money string.

    Args:
        text: raw value, e.g. 'AED 1,299.00'
        currency: label to remove before parsing
        strip_commas: remove thousands separators (keyword-only)
    Returns:
        float value, or None when parsing fails.
    """
    if text is None:
        return None
    cleaned = str(text).replace(currency, "").strip()
    if strip_commas:
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None

print(clean_amount("AED 1,299.00"))
print(clean_amount("PKR 950", currency="PKR"))
print(clean_amount(" 2,500 ", strip_commas=True))
print(clean_amount("abc"))
print(clean_amount(None))

# *args and **kwargs: forwarding without knowing the shape
def summarise(*values, label="values", **options):
    total = sum(values)
    return {"label": label, "n": len(values), "sum": total, "mean": total / len(values) if values else 0.0,
            "options": options}

print(summarise(1, 2, 3, label="sales", precision=2))

# THE TRAP: mutable default arguments
def add_item_bad(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add_item_bad("a"), add_item_bad("b"), add_item_bad("c"))    # accumulates!

def add_item_good(item, bucket=None):
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket

print(add_item_good("a"), add_item_good("b"), add_item_good("c"))''',
             output='''1299.0
950.0
2500.0
None
None
{'label': 'sales', 'n': 3, 'sum': 6, 'mean': 2.0, 'options': {'precision': 2}}
['a'] ['a', 'b'] ['a', 'b', 'c']
['a'] ['b'] ['c']''',
             line_by_line=[
                 "Line 1: the signature documents types and intent. `*` makes strip_commas keyword-only, preventing a call "
                 "like clean_amount('1,299', 'AED', False) that reads as noise.",
                 "Line 2-11: a docstring that states the contract - arguments, return, and the None-on-failure behaviour.",
                 "Line 15-23: defensive parsing: handle None, clean, then cast inside try/except. Returning None rather than "
                 "raising keeps a whole column parseable while flagging failures (Day 59 expands this in pandas).",
                 "Line 30-37: *values collects positionals as a tuple, **options collects the rest as a dict - the pattern "
                 "behind wrappers and decorators.",
                 "Line 40-44: the mutable default trap. The list lives on the function object, so it is shared across calls - "
                 "a bug that hides until production data volume changes call ordering.",
                 "Line 46-52: the canonical fix: default to None, create the container inside the body.",
             ]),
        dict(title="Scope (LEGB), side effects and turning a script into a pipeline of functions",
             language="python", label="EXPLANATION",
             code='''counter = 0                 # global

def bump_bad():
    counter += 1            # UnboundLocalError: Python sees a local assignment
    return counter

def bump_good():
    global counter          # explicit, but avoid this in data code
    counter += 1
    return counter

try:
    bump_bad()
except UnboundLocalError as e:
    print("scope error:", e)
print("global counter after explicit mutation:", bump_good())

# Closures: an inner function remembers enclosing state (no globals needed)
def make_threshold_filter(min_value):
    def keep(records):
        return [r for r in records if r["amount"] >= min_value]
    return keep

high_value = make_threshold_filter(1000)
print(high_value([{"amount": 1200}, {"amount": 300}]))

# Refactor a script into pure functions: testable, reusable, composable
def parse_records(raw_rows):
    return [{"name": r[0].strip().title(), "amount": float(r[1])} for r in raw_rows]

def filter_records(records, min_amount=0.0):
    return [r for r in records if r["amount"] >= min_amount]

def total_by_name(records):
    totals = {}
    for r in records:
        totals[r["name"]] = totals.get(r["name"], 0) + r["amount"]
    return totals

raw = [(" ali ", "1200"), ("sara", "300"), ("ALI", "800")]
pipeline_result = total_by_name(filter_records(parse_records(raw), 500))
print(pipeline_result)''',
             output='''scope error: cannot access local variable 'counter' where it is not associated with a value
global counter after explicit mutation: 1
[{'amount': 1200}]
{'Ali': 2000}''',
             line_by_line=[
                 "Line 3-5: assigning to a global inside a function without `global` makes Python treat it as local, so the "
                 "read fails. This is the most common scope error and it looks like a bug in the wrong line.",
                 "Line 7-9: `global` fixes it but couples the function to module state - hostile to testing and parallelism.",
                 "Line 18-22: closure: keep() remembers min_value from the enclosing scope. The returned function is "
                 "self-contained and safe to pass around - the basis of decorators and config factories.",
                 "Line 25-35: the same logic as small pure functions. Each can be unit-tested independently, and the pipeline "
                 "reads top-to-bottom like a sentence (Day 32 formalises this as a project).",
                 "Line 38-39: composition with no globals, no side effects, deterministic output - exactly what a data pipeline needs.",
             ]),
    ],
    mistakes=[
        dict(mistake="Using a mutable default argument (bucket=[]).",
             why="The default object is created once and shared across calls, so state leaks between invocations.",
             fix="Default to None and construct inside the body."),
        dict(mistake="A function that both computes and prints.",
             why="You cannot reuse the value, test it, or suppress output.",
             fix="Return the value; print in the caller (notebooks) or log it (production)."),
        dict(mistake="Functions that do three jobs: load + clean + model.",
             why="Untestable, unprofiled, and impossible to re-run partially when the last step fails.",
             fix="One job per function; compose them in a pipeline or a pipeline class (Day 169)."),
        dict(mistake="Silently swallowing exceptions with bare `except:`.",
             why="Real errors (typos, schema changes) disappear and debugging starts from zero.",
             fix="Catch specific exceptions, log the context, and decide explicitly whether to raise or return a sentinel."),
    ],
    debugging=[
        dict(symptom="UnboundLocalError inside a function even though the variable exists at module level.",
             cause="An assignment somewhere in the function makes that name local for the whole scope.",
             fix="Inspect for accidental assignment; pass the value as a parameter instead of mutating a global."),
        dict(symptom="A function returns different results for identical inputs.",
             cause="Hidden state: mutable default, global counter, random seed, or time-dependence.",
             fix="Make it pure; pass a seeded rng or a snapshot timestamp as parameters (Day 5 reproducibility)."),
        dict(symptom="TypeError: got an unexpected keyword argument.",
             cause="Signature drift - the function was renamed/changed but a caller was not updated.",
             fix="Greppable names + tests that call the public API catch this in CI (Day 23/265)."),
    ],
    practice=[
        dict(level="easy", task="Write convert_temp(celsius, unit='C') returning Fahrenheit or Kelvin based on unit, with a clear ValueError for unknown units.",
             hint="Keyword argument plus explicit validation.", solution="Return the converted float; raise ValueError('unit must be C/F/K')."),
        dict(level="medium", task="Refactor yesterday's script into three pure functions: parse, filter, aggregate. Call them in a pipeline and verify the output is unchanged.",
             hint="Extract each loop; pass data in, return data out.", solution="Each function testable with a two-line assert."),
        dict(level="hard", task="Write a factory function that returns a configured validator with a closure over min/max, then use it on three columns with different bounds and report failing rows.",
             hint="Closures (make_validator(lo, hi)) plus a list of (column, validator).", solution="Failing rows reported per column with the invalid value and the bound it broke."),
    ],
    challenge=dict(title="Signature design review",
                   brief="Take any 30-line script you have written and redesign its function signatures: type hints, docstrings, keyword-only flags, and explicit failure behaviour.",
                   deliverable="Before/after code plus a paragraph on what changed and why.",
                   stretch="Add a `verbose: bool = False` pattern where logging replaces prints entirely (Day 24)."),
    interview=[
        dict(q="What is the difference between arguments and parameters?", level="beginner", tag="functions",
             a="Parameters are the names in the definition; arguments are the actual values supplied at call time. "
               "Positional arguments map by order, keyword arguments by name, and defaults fill the gaps."),
        dict(q="Why is `def f(items=[]):` dangerous?", level="intermediate", tag="gotchas",
             a="Defaults are evaluated once at definition and stored on the function object, so the same list is reused and "
               "accumulates across calls. Default to None and construct inside."),
        dict(q="Explain LEGB scope.", level="intermediate", tag="internals",
             a="Name resolution order: Local, Enclosing, Global, Built-in. Assignments inside a function create locals, which "
               "is why reading an outer variable then assigning to it raises UnboundLocalError unless declared global/nonlocal."),
        dict(q="What makes a function 'pure' and why does it matter for data pipelines?",
             level="advanced", tag="design",
             a="Purity = same inputs produce the same output with no side effects. Pure functions are trivially testable, safe "
               "to parallelise, cacheable and reproducible - all requirements for reliable ML pipelines."),
    ],
    real_world=("Production ML code is a chain of small pure functions (load_raw, clean, featurise, split, train, evaluate) "
                "wrapped by orchestration. The functions are unit-tested; the orchestration is integration-tested. Teams that "
                "skip the function boundary end up with one 400-line notebook nobody can modify."),
    production=["Type-hint and document public functions; they are the API of your pipeline.",
                "Return values instead of printing; let the caller decide presentation.",
                "Fail loudly with specific exceptions at boundaries and log the context needed to reproduce."],
    recap=["Functions are contracts: inputs, behaviour, outputs, documented failures.",
           "Positional, keyword, default, *args, **kwargs, and keyword-only parameters.",
           "Never use mutable defaults; default to None.",
           "LEGB governs name resolution; avoid globals in data code.",
           "One job per function - pure where possible."],
    revision=["signature forms", "mutable default trap", "LEGB", "closure", "pure function"],
    quiz=[
        dict(q="What does `def f(x, bucket=[]):` cause across repeated calls?",
             options=["The same list is reused and accumulates values", "A new list each call",
                      "A TypeError on the second call", "Nothing unusual"],
             answer=0, explain="Defaults are evaluated once and stored on the function object."),
        dict(q="Which call is valid for `def f(a, b=2, *, c=3)`?",
             options=["f(1, c=4)", "f(1, 2, 3)", "f(1, c=3, b=2) is invalid", "f(a=1, 3)"],
             answer=0, explain="c is keyword-only (after *), so it must be passed by name; b can be positional or keyword."),
        dict(q="What is UnboundLocalError usually a symptom of?",
             options=["Assigning to a name inside a function that was intended to be global",
                      "A missing import", "A syntax error", "Too many arguments"],
             answer=0, explain="Assignment makes the name local for the whole function scope."),
        dict(q="Why prefer returning values over printing inside functions?",
             options=["Returned values can be tested, reused and logged; prints cannot",
                      "Printing is slower and always wrong", "Return consumes less memory", "Printing requires imports"],
             answer=0, explain="Separation of computation from presentation is fundamental to testability."),
        dict(q="A closure is:",
             options=["An inner function that captures variables from its enclosing scope",
                      "A function with no arguments", "A recursive function", "A generator"],
             answer=0, explain="Closures enable decorators, factories and configuration without global state."),
    ],
    cards=[
        ("Pure function", "Same inputs, same output, no side effects."),
        ("Mutable default", "Evaluated once and shared - use None instead."),
        ("Keyword-only", "Parameters after * must be passed by name."),
        ("LEGB", "Local, Enclosing, Global, Built-in resolution order."),
        ("Closure", "Inner function remembering enclosing state."),
        ("One job", "A function that cleans and trains cannot be tested."),
    ],
    extension=["functools.partial, lru_cache and singledispatch are stdlib tools that turn plain functions into production components.",
               "Type hints checked by mypy catch signature drift before it reaches production (Day 22)."],
)

PACKS[14] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Lambda, map and filter are vocabulary; modules and packages are architecture.",
    minutes=85,
    objectives=[
        "Use lambda for short throwaway callables without abusing it.",
        "Apply map and filter, and know when a comprehension is better.",
        "Explain the memory difference between a comprehension and a generator expression.",
        "Import modules in all four forms and use __name__ == '__main__' correctly.",
        "Structure code as your own importable module and reuse it across notebooks.",
    ],
    why=(
        "You will write more preprocessing functions than models. Lambdas, comprehensions and modules are the vocabulary "
        "that keeps preprocessing readable; the module layout is what makes it reusable instead of copy-pasted."
    ),
    concept=dict(
        mode="authored",
        what=("A lambda is an anonymous single-expression function: lambda x: x*2. map(func, iterable) applies a function to "
              "every element lazily; filter(func, iterable) keeps elements where the function is truthy. A module is a .py "
              "file that can be imported; a package is a directory of modules (with __init__.py optionally). "
              "__name__ is '__main__' only when the file is executed directly."),
        why=("These are the tools that let you express 'apply this rule to every row' and 'use this helper from any notebook'. "
             "Without them, analytics code degenerates into copy-paste, and every fix has to be applied in five places."),
        how=("Lambdas: pass short keys to sorted(key=...), map/filter/pandas .apply, or a callback. map/filter: prefer "
             "comprehensions unless the function already exists (e.g. sum(map(int, strings))). Modules: import module, "
             "from module import name, import module as alias, from module import *. Guard executable code with "
             "if __name__ == '__main__': to keep imports side-effect free."),
        intuition=("A lambda is a sticky note with one expression on it - useful, and useless for anything long. A module is a "
                   "toolbox: importing it should give you tools, not start a project. That is why the __main__ guard exists."),
        analogy=("map/filter are assembly-line machines: map transforms, filter sorts out rejects. A comprehension is a worker "
                 "who does both in one walk past the belt - fewer machines, less coordination, usually clearer."),
        internals=("map and filter return iterators (lazy): nothing is computed until iterated, which is why list(map(f, xs)) "
                   "materialises results and map(f, xs) alone does not. A list comprehension builds the entire list in memory; "
                   "a generator expression (same syntax with parentheses) yields lazily. Importing a module executes it once "
                   "and caches it in sys.modules, so top-level side effects happen exactly once - and at an unpredictable time."),
        deep=("Package design for data work: keep pure transforms in src/transforms.py, I/O in src/io.py, and configuration in "
              "config.py. Then orchestration (notebooks, scripts, CLI) imports them. This layout survives the move from "
              "exploration to production, and it is what makes unit tests possible without touching a database."),
        math="Lazy versus eager is a memory-complexity decision: eager costs O(n) memory, lazy costs O(1) plus the current "
             "element. For a 10 GB file you cannot afford eager; for a 1,000-row table eager is simpler and faster.",
        visual=dict(type="flow", svg_key="pipeline", title="map, filter and comprehension",
                    caption="All three express 'transform each element'. Comprehensions usually read best; map/filter win when "
                            "the function already exists; generators win when memory matters.",
                    nodes=["iterable", "transform (map)", "keep condition (filter)", "materialise or stream"]),
    ),
    code=[
        dict(title="Lambda, map, filter - and when the comprehension wins",
             language="python", label="SOURCE",
             code='''records = [{"name": "ali", "amount": 1200}, {"name": "SARA", "amount": 300}, {"name": "Bilal", "amount": 900}]

# lambda as a sort key - its most justified use
print(sorted(records, key=lambda r: r["amount"], reverse=True)[0])
print(sorted(records, key=lambda r: r["name"].lower()))

# map: use when the function already exists
str_amounts = ["1200", "300", "900"]
print("sum:", sum(map(float, str_amounts)))          # no lambda needed
print("lengths:", list(map(len, ["a", "bb", "ccc"])))

# filter
high = list(filter(lambda r: r["amount"] >= 900, records))
print("high:", [r["name"] for r in high])

# The comprehension equivalent - usually clearer
high2 = [r for r in records if r["amount"] >= 900]
print("same:", [r["name"] for r in high2])

# Comprehension forms beyond lists
squares = {n: n ** 2 for n in range(1, 5)}       # dict comprehension
unique_lengths = {len(r["name"]) for r in records}   # set comprehension
gen = (r["amount"] for r in records)             # generator expression: lazy
print("dict comp:", squares, "| set comp:", unique_lengths, "| gen sum:", sum(gen))

# Anti-pattern: lambda with side effects - do not do this
messy = [(lambda r: print("processing", r["name"]))(r) for r in records]

# Functions assigned to names beat lambdas when logic grows
def amount_of(record):
    """Named function: documents intent, reusable, testable."""
    return record["amount"]

print("named function:", sum(map(amount_of, records)))''',
             output='''{'name': 'ali', 'amount': 1200}
[{'name': 'ali', 'amount': 1200}, {'name': 'Bilal', 'amount': 900}, {'name': 'SARA', 'amount': 300}]
sum: 2400.0
lengths: [1, 2, 3]
high: ['ali', 'Bilal']
same: ['ali', 'Bilal']
dict comp: {1: 1, 2: 4, 3: 9, 4: 16} | set comp: {3, 4, 5} | gen sum: 2400
processing ali
processing SARA
processing Bilal
named function: 2400''',
             line_by_line=[
                 "Line 4-5: lambdas shine as sort keys - short, obvious, used once. Note the second sort lowercases for a case-insensitive name order.",
                 "Line 8-9: when the function already exists (float, len), map is concise and avoids a pointless lambda.",
                 "Line 12-13: filter with a lambda is valid but the list comprehension on line 16 says the same thing more directly.",
                 "Line 19-22: comprehension variants cover dicts, sets and generators. The generator expression is lazy: sum() consumes it without building a list.",
                 "Line 25-26: a comprehension used purely for side effects is an anti-pattern - use a plain for loop; comprehensions should build values.",
                 "Line 28-33: when logic outgrows an expression, name it. Named functions get docstrings, tests and tracebacks that point at the right line.",
             ]),
        dict(title="Build your own module and use the __main__ guard",
             language="python", label="PRACTICE",
             code='''# ---------------- src/transforms.py -------------------------------
"""Reusable cleaning transforms for any notebook or pipeline."""
from __future__ import annotations

DEFAULT_CURRENCY = "AED"

def clean_amount(text: str, currency: str = DEFAULT_CURRENCY) -> float | None:
    """Return a float for a money string, or None when unparseable."""
    if text is None:
        return None
    cleaned = str(text).replace(currency, "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None

def normalise_name(name: str) -> str:
    """Trim, collapse whitespace and title-case a person name."""
    return " ".join(name.split()).title()

def main() -> None:
    samples = ["AED 1,299.00", " 2,500 ", "abc", None]
    for s in samples:
        print(f"{str(s):>16} -> {clean_amount(s)}")

# ---------------- guard: only run when executed directly -------------
if __name__ == "__main__":
    main()

# ---------------- usage from a notebook or another module ------------
# import sys; sys.path.append("src")      # or install the package (Day 31)
# from transforms import clean_amount, normalise_name
# print(clean_amount("AED 950"), normalise_name("  ali   raza "))''',
             output='''$ python src/transforms.py
      AED 1,299.00 -> 1299.0
             2,500  -> 2500.0
                 abc -> None
                None -> None

$ python -c "from transforms import normalise_name; print(normalise_name('  ali   raza '))"
Ali Raza''',
             line_by_line=[
                 "Line 1-2: a module docstring states the purpose - it is what `help(transforms)` shows.",
                 "Line 5: a module-level constant makes intent explicit and is easy to change in one place.",
                 "Line 7-16: two small pure functions. Because they are pure, they can be unit-tested and reused in pandas .apply later.",
                 "Line 18-21: main() holds the executable demo, so the module stays importable and side-effect free.",
                 "Line 24-25: the __main__ guard means importing the module never prints or runs work - the rule that keeps pipelines deterministic.",
                 "Line 28-30: the notebook usage pattern. Day 31 replaces the sys.path hack with a proper package and CLI.",
             ]),
    ],
    mistakes=[
        dict(mistake="Assigning a lambda to a name (f = lambda x: ...).",
             why="PEP 8 discourages it; you lose a docstring, a clear traceback name and readability.",
             fix="Use def; keep lambdas for inline single-use callables."),
        dict(mistake="Using a comprehension for side effects (prints, writes, appends).",
             why="It builds a useless list and hides the intent.",
             fix="Use a for loop when the purpose is an action, a comprehension when the purpose is a value."),
        dict(mistake="Putting executable code at module top level without the __main__ guard.",
             why="Importing the module runs the work - surprising, slow, and it breaks tests.",
             fix="Wrap in main() and guard with if __name__ == '__main__':."),
        dict(mistake="Using `from module import *`.",
             why="It hides where names came from and can silently shadow built-ins.",
             fix="Import explicitly, or import the module and use module.name."),
    ],
    debugging=[
        dict(symptom="ModuleNotFoundError when importing your own helper from a notebook.",
             cause="The notebook's working directory is not on sys.path.",
             fix="Run from the project root, or add the package properly (pip install -e .) as on Day 31."),
        dict(symptom="Edits to a module do not take effect in the notebook.",
             cause="Python caches imported modules in sys.modules.",
             fix="Restart the kernel, or use importlib.reload(module) during development."),
        dict(symptom="map() returns something that prints as <map object at 0x...>.",
             cause="map is lazy; it returns an iterator, not a list.",
             fix="Wrap with list(), or consume it once (sum, join, any) deliberately."),
    ],
    practice=[
        dict(level="easy", task="Sort a list of (name, score) tuples by score descending using a lambda key, then by name for ties.",
             hint="Two sorts (stable) or key=lambda t: (-t[1], t[0]).", solution="key=lambda t: (-t[1], t[0]) sorts in one pass."),
        dict(level="medium", task="Write your own module with three pure functions (clean text, parse number, validate range) and use it from a notebook via an import.",
             hint="Follow the transforms.py template.", solution="Notebook imports and calls all three; no copy-paste."),
        dict(level="hard", task="Rewrite a 6-line map/filter chain as a comprehension, as a generator pipeline, and as a single pandas-free reduce; compare memory behaviour with sys.getsizeof and tracemalloc.",
             hint="tracemalloc for peak memory.", solution="Generator uses O(1) extra memory; list builds everything eagerly."),
    ],
    challenge=dict(title="Personal utility module",
                   brief="Create src/mytools.py with at least five functions you will genuinely reuse (parsing, cleaning, timing, seeding, path building), a docstring per function, and a __main__ demo.",
                   deliverable="The module plus a notebook that imports it and calls each function once.",
                   stretch="Add a simple test file (test_mytools.py) with asserts for the edge cases - previewing Day 23."),
    interview=[
        dict(q="When should you use a lambda versus a def?", level="beginner", tag="functions",
             a="Lambda for a short, single-use expression where the function is obvious in place (sort keys, small callbacks). "
               "def when it needs a name, a docstring, multiple statements, testing or a meaningful traceback."),
        dict(q="Difference between a list comprehension and a generator expression?", level="intermediate", tag="performance",
             a="Comprehensions build the whole list in memory (O(n)); generator expressions yield lazily (O(1) extra memory). "
               "Generators can only be consumed once, which is the trade-off."),
        dict(q="What does `if __name__ == '__main__':` do?", level="beginner", tag="packaging",
             a="It separates library behaviour from script behaviour: the block runs only when the file is executed directly, "
               "not when it is imported. It keeps imports side-effect free, which tests and pipelines depend on."),
        dict(q="How would you organise reusable data code across ten notebooks?", level="advanced", tag="architecture",
             a="A package (src/) with pure transform functions, an io module for loading, and configuration; notebooks import it. "
               "Version it in Git, test it in CI, and expose a CLI entry point for scheduled runs (Days 31-32, 265)."),
    ],
    real_world=("The move from 'notebook hero' to 'team member' is mostly this day: extract logic into importable, tested "
                "functions. Interviewers frequently ask you to describe a shared utility package you built - this is that story."),
    production=["Every module import must be side-effect free; do work in functions called explicitly.",
                "Keep pure transforms separate from I/O so the transforms are testable without data access.",
                "Version internal packages and pin them in requirements, like any third-party dependency."],
    recap=["lambdas: one expression, best as an inline key or callback.",
           "map/filter are lazy; comprehensions and generators cover most cases more readably.",
           "Modules are importable toolboxes; packages group them.",
           "The __main__ guard separates script from library behaviour.",
           "Extract reusable logic into src/ - the first step toward production code."],
    revision=["lambda vs def", "map/filter laziness", "comprehension forms", "__main__ guard", "import forms"],
    quiz=[
        dict(q="What does `list(map(str, [1, 2]))` return?",
             options=["['1', '2']", "[1, 2]", "<map object>", "Error"], answer=0, explain="map applies str to each element; list() materialises the lazily produced results."),
        dict(q="Why is `f = lambda x: x + 1` discouraged?",
             options=["Named lambdas lose docstrings and readable tracebacks", "It is a syntax error",
                      "It is slower", "Lambdas cannot do arithmetic"],
             answer=0, explain="PEP 8 prefers def for anything that deserves a name."),
        dict(q="What runs when you `import mycars` (a module with a demo print at top level)?",
             options=["The top-level code executes once, including the print", "Nothing - imports are inert",
                      "Only functions run", "The __main__ block runs"],
             answer=0, explain="Module top-level code runs once per process on first import; the __main__ block does not."),
        dict(q="Which is lazy?",
             options=["(x**2 for x in range(10))", "[x**2 for x in range(10)]", "{x**2 for x in range(10)}", "list(map(...))"],
             answer=0, explain="Generator expressions and map/filter return iterators; the others materialise containers."),
        dict(q="Best reason to move a repeated cleaning step into src/transforms.py?",
             options=["One definition to fix, test and reuse everywhere", "It runs faster automatically",
                      "Notebooks cannot contain loops", "It reduces imports"],
             answer=0, explain="Single source of truth is the core argument for modularising data code."),
    ],
    cards=[
        ("lambda", "Single-expression anonymous function; best for sort keys."),
        ("Lazy map/filter", "Return iterators; nothing computes until consumed."),
        ("Comprehension forms", "List [], set {}, dict {k: v}, generator ()."),
        ("__main__ guard", "Run code only when executed directly, not on import."),
        ("Package layout", "src/ for pure functions and I/O; notebooks import them."),
        ("Side-effect-free import", "Importing must never do work."),
    ],
    extension=["Modern projects use pyproject.toml + editable installs (pip install -e .) instead of sys.path hacks (Day 31).",
               "Type checkers and linters (mypy, ruff) enforce module hygiene automatically in CI (Day 265)."],
)
