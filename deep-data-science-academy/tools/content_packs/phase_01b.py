"""Authored deep lessons - Phase 1, Days 8-11."""

PACKS = {}

PACKS[8] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Lists are ordered and mutable; tuples are fixed records. Choosing wrongly costs you bugs later.",
    minutes=85,
    objectives=[
        "Create, index, slice and iterate lists correctly.",
        "Use append/extend/insert/pop/remove/sort with confidence about what each mutates.",
        "Explain when a tuple is the right structure and why it is hashable.",
        "Avoid the aliasing and nested-mutation traps with lists.",
        "Choose between list, tuple, set and dict by intent, not habit.",
    ],
    why=(
        "Almost every dataset starts life as lists of rows before it becomes an array or DataFrame. Sloppy list handling "
        "is the origin of a surprising number of 'wrong numbers' bugs - especially aliasing and accidental in-place sorting."
    ),
    concept=dict(
        mode="authored",
        what=("A list is an ordered, mutable, heterogeneous sequence: one object holding references to other objects, "
              "addressable by position. A tuple is an ordered, immutable sequence, usually meaning 'this group of values "
              "belongs together and must not change', e.g. a coordinate or a database row."),
        why=("Order matters for data (rows have positions), mutation matters for in-place algorithms (sorting, appending), "
             "and immutability matters for safety (keys in dictionaries, function arguments that must not be altered)."),
        how=("Creating: [1,2,3], list(range(5)), [x*2 for x in range(5)]. Adding: append (single item), extend (many), "
             "insert (at position). Removing: pop (by index, returns it), remove (by value), del, clear. Ordering: sort() "
             "in place, sorted() returns new. Copying: lst.copy() is shallow - reach for copy.deepcopy for nesting."),
        intuition=("A list is a numbered row of lockers holding objects. Append adds a locker at the end; insert squeezes "
                   "a new locker in and renumbers everything after it (which is why inserting at the front of a large list "
                   "is slow). A tuple is a sealed box of lockers whose addresses can never change."),
        analogy=("A shopping list you can edit (list) versus the printed receipt of that trip (tuple). You keep editing "
                 "the list; the receipt is evidence and should not be rewritten."),
        internals=("CPython lists are dynamic arrays of pointers with over-allocation: appending is amortised O(1) because "
                   "capacity grows geometrically. Index access is O(1); membership testing is O(n); insert/delete in the "
                   "middle is O(n). Tuples allocate once, are smaller and slightly faster."),
        deep=("Because a list stores references, a list of lists does not own its inner lists. Sort stability is guaranteed "
              "(Timsort): equal keys keep original order, which is why you can sort by a primary key then a secondary key "
              "with two successive sort calls. In pandas and NumPy the same reference semantics reappear as views and copies."),
        math=("Complexity is the maths you need today: list append O(1) amortised, membership 'x in lst' O(n), sort O(n log n). "
              "If you find yourself testing membership inside a loop over 10^6 items, the correct fix is a set (O(1) lookup)."),
        visual=dict(type="diagram", svg_key="list-tuple", title="List vs tuple in memory",
                    caption="A list is a resizable array of references (new items can be appended). A tuple is fixed at "
                            "creation, so it can be hashed and used as a dictionary key.",
                    nodes=["list [a, b, c] resizable", "tuple (a, b, c) immutable & hashable"]),
    ),
    code=[
        dict(title="Every list operation you need, with what it mutates",
             language="python", label="SOURCE",
             code='''rows = ["Ali", 34, "Lahore"]
print(rows[0], rows[-1], len(rows))

rows.append("analyst")          # add ONE item at the end (in place)
rows.extend(["python", "sql"])  # add MANY items (in place)
rows.insert(1, "Mr")            # insert at index 1, shifting the rest
print(rows)

last = rows.pop()               # remove and RETURN the last item
rows.remove("Mr")               # remove by VALUE (first match)
print("popped:", last, "| now:", rows)

nums = [5, 1, 3, 2]
nums.sort()                      # IN PLACE, returns None
print("sorted in place:", nums)
other = sorted(nums, reverse=True)   # new list, original untouched
print("new list:", other, "| original:", nums)

# Slicing returns a NEW list; slice assignment mutates in place
part = nums[1:3]
nums[0] = 99
print("slice copy:", part, "| mutated:", nums)

# Nested lists: the aliasing trap
matrix = [[1, 2], [3, 4]]
row = matrix[0]                 # NOT a copy
row.append(99)
print("matrix after appending through 'row':", matrix)''',
             output='''Ali Lahore 3
['Ali', 'Mr', 34, 'Lahore', 'analyst', 'python', 'sql']
popped: sql | now: ['Ali', 34, 'Lahore', 'analyst', 'python']
sorted in place: [1, 2, 3, 5]
new list: [5, 3, 2, 1] | original: [1, 2, 3, 5]
slice copy: [2, 3] | mutated: [99, 2, 3, 5]
matrix after appending through 'row': [[1, 2, 99], [3, 4]]''',
             line_by_line=[
                 "Line 2: index 0 is the first element, -1 the last. len() counts top-level elements only.",
                 "Line 5-7: append adds one item, extend adds each item of an iterable, insert places at a position. "
                 "All three mutate in place and return None - never write `rows = rows.append(x)`.",
                 "Line 10-11: pop returns the removed item (useful); remove deletes by value and returns nothing.",
                 "Line 14-16: sort() mutates and returns None; sorted() returns a new list. Mixing them up is the single "
                 "most common beginner bug here.",
                 "Line 19-21: slicing copies references into a new list. Changing nums[0] afterwards does not affect part.",
                 "Line 24-27: matrix[0] is a reference to the inner list, so appending through 'row' is visible in matrix.",
             ]),
        dict(title="Tuples: fixed records, unpacking, and why they can be dictionary keys",
             language="python", label="EXPLANATION",
             code='''point = (12.97, 77.59)                 # (latitude, longitude) - a fixed record
row_from_db = (1001, "Ayesha", "Data Scientist", 145000)

lat, lon = point                          # unpacking
id_, name, title, salary = row_from_db
print(f"{name} ({title}) earns {salary:,} at {lat:.2f},{lon:.2f}")

# Tuples are hashable -> usable as dict keys and set members
grid = {(0, 0): "origin", (1, 2): "cell"}
print(grid[(1, 2)])

# A list is NOT hashable -> this raises TypeError
try:
    bad = {[1, 2]: "x"}
except TypeError as e:
    print("list as key ->", e)

# Returning multiple values is really returning one tuple
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([4, 9, 1, 7])
print("range:", lo, hi)

# Immutability is shallow: a tuple can contain a mutable list
t = (1, [2, 3])
t[1].append(4)
print("tuple with mutated list inside:", t)   # legal, but a design smell''',
             output='''Ayesha (Data Scientist) earns 145,000 at 12.97,77.59
cell
list as key -> unhashable type: 'list'
range: 1 9
tuple with mutated list inside: (1, [2, 3, 4])''',
             line_by_line=[
                 "Line 1-2: tuples express 'these belong together'. The database row is a classic case - the shape is fixed.",
                 "Line 4-5: unpacking assigns each element to a name; the number of names must match the tuple length.",
                 "Line 9-10: because a tuple cannot change, Python can hash it, so it works as a dict key or set member. "
                 "The spatial grid uses this to key cells by coordinates.",
                 "Line 13-16: putting a list where a hashable is required raises TypeError - the practical reason tuples exist.",
                 "Line 19-20: returning 'multiple values' actually returns a tuple; unpack at the call site.",
                 "Line 24-26: immutability is shallow - the tuple's slots cannot change, but objects inside can. Prefer "
                 "tuples of immutables to avoid surprising shared state.",
             ]),
    ],
    mistakes=[
        dict(mistake="Writing `my_list = my_list.append(x)` or `= my_list.sort()`.",
             why="Both methods mutate in place and return None, so you replace your data with None.",
             fix="Call mutators as statements; use sorted()/reversed() when you want a new object."),
        dict(mistake="Assuming `b = a` copies a list.",
             why="It binds a second name to the same object; then 'editing a copy' edits the original.",
             fix="Use list(a), a[:] or a.copy() for a shallow copy and copy.deepcopy for nested data."),
        dict(mistake="Using a list for membership tests inside a hot loop.",
             why="`x in list` is O(n); a loop over 1e6 rows becomes 1e12 comparisons.",
             fix="Convert to a set: `lookup = set(ids)` then `if x in lookup` is O(1)."),
        dict(mistake="Mutating a list while iterating over it.",
             why="Indexes shift under the iterator, so elements are skipped silently.",
             fix="Iterate over a copy (`for x in lst[:]`) or build a new list with a comprehension."),
    ],
    debugging=[
        dict(symptom="Your sorted list appears unsorted later.",
             cause="You passed the list to a function that called .sort() in place, or reused a variable name.",
             fix="Prefer sorted() inside functions, or document mutation clearly in the function name (e.g. sort_in_place)."),
        dict(symptom="Removing items in a loop removes fewer items than expected.",
             cause="Index shifting during iteration.",
             fix="Build a filtered new list: `kept = [x for x in lst if x not in banned]`."),
        dict(symptom="A nested list 'changes itself' after you edit a copy.",
             cause="Shallow copy sharing inner lists.",
             fix="copy.deepcopy, or rebuild the structure (e.g. with a list comprehension over each row)."),
    ],
    practice=[
        dict(level="easy", task="From [3, 1, 4, 1, 5, 9, 2, 6], remove duplicates, sort ascending, and print the top three values.",
             hint="set() removes duplicates; sorted() returns a new list; slicing gets the tail.", solution="sorted(set(x))[-3:] -> [5, 6, 9]."),
        dict(level="medium", task="Write a function that takes a list of (name, score) tuples and returns the names sorted by score descending, keeping original order for ties.",
             hint="Python's sort is stable - sort by name first, then by score descending.", solution="Sort twice (secondary first) or use key=lambda r: -r[1]."),
        dict(level="hard", task="Demonstrate that list membership is O(n) while set membership is O(1) by timing both on 1e6 items.",
             hint="Use timeit or time.perf_counter with a loop of lookups.", solution="Expect orders-of-magnitude difference; report both timings."),
    ],
    challenge=dict(title="Rebuild a CSV as lists of tuples",
                   brief="Read resources/datasets_for_practice/tips.csv manually (no pandas): split each line, build a list of tuples, then compute the average tip by day of week using only built-ins.",
                   deliverable="A script plus printed table of day -> average tip.",
                   stretch="Do it again with a dictionary of lists and compare readability."),
    interview=[
        dict(q="Difference between a list and a tuple?", level="beginner", tag="data-structures",
             a="List: mutable, dynamic array, used for homogeneous sequences you will modify. Tuple: immutable, hashable, "
               "used for fixed records (coordinates, DB rows) and as dict keys. Tuples are slightly smaller and faster."),
        dict(q="Why does `print(my_list.sort())` print None?", level="beginner", tag="gotchas",
             a="list.sort() sorts in place and returns None by convention (mutating methods return None to signal they "
               "changed state). Use sorted(list) if you need the result."),
        dict(q="What is the time complexity of appending to a list and of inserting at position 0?",
             level="intermediate", tag="complexity",
             a="Append is amortised O(1) thanks to over-allocation; insert at 0 is O(n) because every element shifts. "
               "For queue-like behaviour use collections.deque (O(1) at both ends)."),
        dict(q="A colleague says 'I copied the DataFrame and the original changed anyway'. How do you explain it?",
             level="advanced", tag="internals",
             a="Copy semantics: plain assignment aliases, shallow copies share nested objects, and pandas has its own "
               "copy-on-write rules. In pandas 2.x you also get SettingWithCopyWarning for chained assignment. The general "
               "principle from lists and tuples generalises: know whether you hold a reference or a copy."),
    ],
    real_world=("ETL scripts frequently build lists of records before bulk-inserting into a database. Choosing a set for "
                "deduplication and a dict for lookups turns a script that takes minutes into one that takes seconds, with "
                "no algorithmic heroics."),
    production=["Prefer sets/dicts for lookups in data validation code paths.",
                "Document or avoid in-place mutation in functions that are called from parallel jobs.",
                "When building large lists, preallocate where possible or use generators (Day 19) to bound memory."],
    recap=["Lists: ordered, mutable, dynamic arrays; indexing O(1), membership O(n).",
           "Mutating methods return None; sorted() returns a new list.",
           "Tuples: immutable, hashable, ideal for fixed records and dict keys.",
           "Aliasing: assignment never copies; slices and .copy() are shallow.",
           "Iterate over a copy if you must modify a list while looping."],
    revision=["list vs tuple", "append vs extend vs insert", "sort vs sorted", "O(1) vs O(n) membership",
              "unpacking", "shallow copy trap"],
    quiz=[
        dict(q="What does `lst = [3,1,2]; print(lst.sort())` output?",
             options=["None", "[1, 2, 3]", "3", "Error"],
             answer=0, explain="sort() mutates in place and returns None."),
        dict(q="Which structure gives O(1) average membership testing?",
             options=["set", "list", "tuple", "string"],
             answer=0, explain="Sets (and dict keys) are hash-based; lists and tuples require linear scans."),
        dict(q="What is the result of `matrix = [[1,2],[3,4]]; r = matrix[0]; r.append(5)`?",
             options=["matrix becomes [[1, 2, 5], [3, 4]]", "Only r changes", "matrix becomes [[1,2],[3,4],5]", "TypeError"],
             answer=0, explain="matrix[0] returns a reference to the inner list, so appending through r is visible in matrix."),
        dict(q="Why can a tuple be a dictionary key but a list cannot?",
             options=["Tuples are hashable because they are immutable", "Tuples are smaller", "Tuples are ordered",
                      "Lists are slower"],
             answer=0, explain="Hashability requires immutability so the key's hash cannot change while it is in the dict."),
        dict(q="Best way to return two values from a function?",
             options=["return a, b and unpack at the call site", "return '{a}|{b}' and split", "Use a global variable",
                      "print them"],
             answer=0, explain="Returning a tuple is idiomatic, type-safe and does not abuse globals or strings."),
    ],
    cards=[
        ("append vs extend", "append adds one item; extend adds each item of an iterable."),
        ("sort vs sorted", "sort mutates and returns None; sorted returns a new list."),
        ("Tuple use case", "Fixed record: coordinates, DB row, dict key."),
        ("Membership cost", "list O(n), set/dict O(1) average."),
        ("Aliasing", "Assignment binds names; it never copies."),
        ("Mutating while iterating", "Indexes shift - iterate over a copy or build a new list."),
    ],
    extension=["collections.deque for O(1) queue operations; array module or NumPy for numeric storage efficiency.",
               "Polars/Arrow columnar structures change these trade-offs at scale (Phase 3-4)."],
)

PACKS[9] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Uniqueness lives in sets; meaning lives in dictionaries. Most analytics code is dictionary-shaped.",
    minutes=85,
    objectives=[
        "Use sets for deduplication, membership and set algebra.",
        "Create, read, update and delete dictionary entries safely.",
        "Explain hashing and why keys must be immutable.",
        "Model a real record (a customer, an order) as a nested dictionary.",
        "Use dict.get, setdefault, and comprehensions idiomatically.",
    ],
    why=(
        "Category counts, lookups, JSON payloads and configuration files are all dictionaries. Sets solve the "
        "deduplication and 'which ids are new?' problems that appear in every data pipeline."
    ),
    concept=dict(
        mode="authored",
        what=("A set is an unordered collection of unique, hashable objects supporting mathematical set operations. "
              "A dictionary maps hashable keys to arbitrary values with average O(1) lookup, insertion and deletion, "
              "and since Python 3.7 preserves insertion order."),
        why=("Data work keeps asking two questions: 'have I seen this before?' (set) and 'what is the value for this key?' "
             "(dict). Answering them with lists makes code slower and more error-prone."),
        how=("Sets: {1,2}, set(iterable), add/discard/remove, union |, intersection &, difference -, symmetric difference ^. "
             "Dicts: {k: v}, d[key], d.get(key, default), d.setdefault(k, []), d.items()/keys()/values(), update, pop, del. "
             "Iterate with .items() to get pairs."),
        intuition=("A set is a bouncer at the door: the same person never enters twice. A dictionary is a cloakroom: your "
                   "ticket (key) retrieves exactly your coat (value) instantly, because tickets are numbered by their content."),
        analogy=("A set is the list of unique visitors; a dictionary is the guest register mapping name -> room number. "
                 "Two guests cannot share a ticket number, but many guests can share a room."),
        internals=("Both use a hash table: hash(key) -> bucket. CPython stores entries in a sparse array with open "
                   "addressing and keeps insertion order via the index array. If two keys collide, equality is checked. "
                   "That is why keys must be immutable: if a key mutated, its hash would change and lookups would fail; "
                   "that is also why custom classes used as keys need __hash__ and __eq__."),
        deep=("Sets are ideal for de-duplication at scale (O(n) instead of O(n^2)); for large numeric dedup tasks, NumPy "
              "or pandas unique() will be far faster than a Python loop. Note also frozenset for hashable sets, and "
              "collections.Counter for frequency counting - both appear constantly in EDA and NLP work."),
        math="Set algebra is the maths: union is OR, intersection is AND, difference is A and not B, symmetric difference "
             "is XOR. In data terms: union = all customers from both sources, intersection = customers present in both.",
        visual=dict(type="diagram", svg_key="sets-dicts", title="Set operations and dictionary lookup",
                    caption="Left: union/intersection/difference answer 'who is in both?'. Right: a hash table answers "
                            "'what is the value for this key?' in constant time - the basis of every join you will write.",
                    nodes=["A | B all members", "A & B common", "A - B only in A", "key -> value O(1)"]),
    ),
    code=[
        dict(title="Sets: deduplication and set algebra you will actually use",
             language="python", label="SOURCE",
             code='''orders_day1 = ["A-1", "A-2", "A-3", "A-2"]
orders_day2 = ["A-3", "A-4", "A-4", "A-5"]

d1, d2 = set(orders_day1), set(orders_day2)
print("unique d1:", sorted(d1), "| duplicates removed:", len(orders_day1) - len(d1))
print("both days       :", sorted(d1 & d2))
print("either day      :", sorted(d1 | d2))
print("only day 1      :", sorted(d1 - d2))
print("exactly one day :", sorted(d1 ^ d2))

d1.add("A-9")
d1.discard("A-99")     # discard never raises; remove raises KeyError if absent
print("after add/discard:", sorted(d1))

# Fast membership: the pattern that saves minutes on large data
banned = {"A-3", "A-5"}
kept = [o for o in orders_day1 + orders_day2 if o not in banned]
print("kept:", kept)

# Frequency counting - the EDA workhorse
from collections import Counter
counts = Counter(orders_day1 + orders_day2)
print("most common:", counts.most_common(2))''',
             output='''unique d1: ['A-1', 'A-2', 'A-3'] | duplicates removed: 1
both days       : ['A-3']
either day      : ['A-1', 'A-2', 'A-3', 'A-4', 'A-5']
only day 1      : ['A-1', 'A-2']
exactly one day : ['A-1', 'A-2', 'A-4', 'A-5']
after add/discard: ['A-1', 'A-2', 'A-3', 'A-9']
kept: ['A-1', 'A-2', 'A-2']
most common: [('A-2', 2), ('A-3', 2)]''',
             line_by_line=[
                 "Line 1-2: raw orders contain duplicates - normal in transaction logs.",
                 "Line 4: set() removes duplicates immediately; subtracting lengths quantifies how many duplicates existed.",
                 "Line 5-8: the four set operators answer different business questions. Note & is intersection, not and.",
                 "Line 10-12: add() inserts; discard() is the safe removal (no exception when missing).",
                 "Line 15-17: membership on a set is O(1), so filtering 10^6 ids is fast - the most valuable set trick in ETL.",
                 "Line 20-21: Counter turns a set problem into frequency analysis; most_common gives an immediate EDA view.",
             ]),
        dict(title="Dictionaries: records, safe access, and nested JSON-shaped data",
             language="python", label="SOURCE",
             code='''customer = {"id": 1001, "name": "Ayesha", "city": "Lahore", "spend": [1200, 800, 400]}

print(customer["name"])                    # KeyError if missing
print(customer.get("email"))               # None instead of KeyError
print(customer.get("email", "unknown"))    # default value

customer["segment"] = "Gold"               # insert or overwrite
customer["city"] = "Islamabad"             # update
removed = customer.pop("segment")          # remove and return
print("removed:", removed, "| keys:", list(customer.keys()))
print("total spend:", sum(customer["spend"]))

# Building aggregates without boilerplate: setdefault
by_city = {}
records = [("Lahore", 1200), ("Karachi", 900), ("Lahore", 400)]
for city, amount in records:
    by_city.setdefault(city, []).append(amount)
print({c: sum(v) for c, v in by_city.items()})

# Nested structures = the shape of every JSON API response
api_response = {
    "status": "ok",
    "results": [{"id": 1, "tags": ["new", "sale"]}, {"id": 2, "tags": []}],
    "meta": {"page": 1, "per_page": 50},
}
print(api_response["results"][0]["tags"][1])
print("page size:", api_response["meta"]["per_page"])

# Merging dicts: | (3.9+) keeps the RIGHT-hand value on conflict
defaults = {"scaling": "standard", "cv": 5}
user_cfg = {"cv": 10}
print(defaults | user_cfg)''',
             output='''Ayesha
None
unknown
removed: Gold | keys: ['id', 'name', 'city', 'spend']
total spend: 2400
{'Lahore': 1600, 'Karachi': 900}
sale
page size: 50
{'scaling': 'standard', 'cv': 10}''',
             line_by_line=[
                 "Line 3: direct indexing raises KeyError on a missing key - fine when absence is a bug, dangerous when it is normal.",
                 "Line 4-5: .get() returns None or a supplied default; use it at every boundary where data may be incomplete.",
                 "Line 7-9: insert/update/remove. pop returns the value so you can log what was removed.",
                 "Line 13-17: setdefault is the classic grouping idiom; a Counter or defaultdict alternative exists, but "
                 "this pattern shows up in interviews constantly.",
                 "Line 20-26: nested dicts and lists are exactly how JSON APIs respond, so drill the indexing chain "
                 "results[0]['tags'][1] until it is automatic (Day 28).",
                 "Line 29-31: the | operator merges with right-hand precedence - perfect for config layering.",
             ]),
    ],
    mistakes=[
        dict(mistake="Indexing a dict for a key that may be absent.",
             why="KeyError crashes the pipeline; worse, people 'fix' it with try/except around too much code.",
             fix="Use d.get(key, default) or check `if key in d` deliberately, and validate inputs with Pydantic later (Day 261)."),
        dict(mistake="Using a list or dict as a set member or dict key.",
             why="They are unhashable (mutable), so Python raises TypeError.",
             fix="Convert to a tuple, a frozenset, or a string key like 'a|b'."),
        dict(mistake="Expecting sets to preserve order.",
             why="Sets are unordered; output order is an implementation detail.",
             fix="Sort when you display (sorted(s)) or use dict.fromkeys(iterable) for order-preserving dedup."),
        dict(mistake="Mutating a dict while iterating over it.",
             why="RuntimeError: dictionary changed size during iteration.",
             fix="Iterate over list(d.items()) or build a new dict."),
    ],
    debugging=[
        dict(symptom="TypeError: unhashable type: 'list' when adding to a set.",
             cause="A list is inside the set expression.",
             fix="Convert to tuple: set(tuple(x) for x in rows)."),
        dict(symptom="KeyError deep inside a pipeline for a column that exists in your head.",
             cause="Case/whitespace mismatch in keys ('City ' vs 'city'), common with CSV headers.",
             fix="Normalise keys at load (strip/lower) and assert the schema once, not per access."),
        dict(symptom="Counts look right but total is wrong.",
             cause="Deduplicating with a set discarded genuinely repeated events you needed to count.",
             fix="Decide deliberately: dedupe for 'unique users', keep duplicates for 'number of events'."),
    ],
    practice=[
        dict(level="easy", task="Given two lists of emails, print the addresses present in both and the count of duplicates removed.",
             hint="set(a) & set(b); len(a) - len(set(a)).", solution="See the first code example."),
        dict(level="medium", task="Build a word-frequency table of a paragraph using a plain dict (no Counter), then compare with Counter.",
             hint="for word in text.lower().split(): counts[word] = counts.get(word, 0) + 1.",
             solution="Both should agree; Counter is shorter and supports most_common."),
        dict(level="hard", task="Model a small invoice as a nested dict (customer, items with qty/price, total) and write a function that computes the total robustly (missing qty -> 1, missing price -> error).",
             hint="Use .get with a default and raise a clear ValueError for price.",
             solution="Return a dict with line totals plus the grand total; unit-test three edge cases."),
    ],
    challenge=dict(title="Deduplicate a real messy id list",
                   brief="Take a messy list of order ids with casing and whitespace differences ('a-1', 'A-1 ', 'A-1'). Normalise, deduplicate, report how many raw rows collapsed into how many unique ids.",
                   deliverable="A script printing both counts and the mapping of raw -> normalised.",
                   stretch="Extend it to detect near-duplicates (differing by one character) and flag them for review."),
    interview=[
        dict(q="When would you use a set instead of a list?", level="beginner", tag="data-structures",
             a="When uniqueness or fast membership matters: deduplication, 'which ids are new', set algebra between two "
               "sources. Lists when order or duplicates are meaningful."),
        dict(q="How do Python dictionaries achieve O(1) lookup?", level="intermediate", tag="internals",
             a="They are hash tables: hash(key) maps to a bucket index, collisions are resolved by probing, and equality is "
               "checked on match. Keys must be hashable (immutable) so the hash never changes while the key lives in the table."),
        dict(q="Explain `d.get('k', [])` vs `d.setdefault('k', [])`.", level="intermediate", tag="essentials",
             a="get returns the default without inserting. setdefault inserts the default if the key is missing and returns "
               "the (possibly pre-existing) value - useful for grouping, though defaultdict and Counter are cleaner."),
        dict(q="How would you merge two dictionaries where the second should override the first, without mutating either?",
             level="intermediate", tag="essentials",
             a="{**a, **b} or a | b (3.9+). For nested configs you need a recursive merge; note that deep_merge is not in "
               "the stdlib, so write and test it explicitly."),
    ],
    real_world=("Feature engineering lives on dictionaries: a lookup table of city -> region, a mapping of device -> category, "
                "an id -> embedding index. Building these once as dicts (or sets) and reusing them is the difference between "
                "an ETL script that runs in seconds and one that runs for hours."),
    production=["Validate that keys you depend on exist at load time; fail loudly, early and once.",
                "Use dicts for lookup tables but watch memory: 10 million keys in a Python dict is heavy. Consider arrays or a database join.",
                "Log cardinality (number of unique keys) for every join key to catch upstream data changes."],
    recap=["Sets: unique, unordered, O(1) membership, support union/intersection/difference.",
           "Dicts: hash-based key->value, insertion ordered, O(1) average access.",
           "Keys must be hashable - tuples and frozensets, not lists.",
           "Use .get for optional keys; setdefault/Counter for grouping and counting.",
           "Deduplicate deliberately: unique users vs total events are different questions."],
    revision=["set algebra operators", "hashability rule", "get vs setdefault", "dict | merge", "Counter.most_common"],
    quiz=[
        dict(q="Which answers 'customers present in both datasets'?",
             options=["set_a & set_b", "set_a | set_b", "set_a - set_b", "set_a ^ set_b"],
             answer=0, explain="& is intersection: members present in both."),
        dict(q="Why does `{[1,2]: 'x'}` raise TypeError?",
             options=["Lists are unhashable, so they cannot be dict keys", "Dicts can only have string keys",
                      "The syntax is invalid", "Lists are too large"],
             answer=0, explain="Mutability means the hash could change, breaking the hash table. Use a tuple instead."),
        dict(q="`d.get('k')` versus `d['k']` when 'k' is missing:",
             options=["get returns None; [] raises KeyError", "Both return None", "Both raise KeyError", "get raises, [] returns None"],
             answer=0, explain="Choose based on whether absence is normal (get) or a bug (direct indexing)."),
        dict(q="Which preserves insertion order while removing duplicates from a list?",
             options=["list(dict.fromkeys(items))", "set(items)", "sorted(set(items))", "items.unique()"],
             answer=0, explain="A dict preserves insertion order; converting back to a list gives ordered dedup. Sets are unordered."),
        dict(q="A pipeline reports 1000 rows and 950 unique user ids. Which statement is safe?",
             options=["Some users generated multiple events in this window", "There are 50 missing users",
                      "The data is corrupted", "The id column is a float"],
             answer=0, explain="Duplicates are expected in event logs; the question is whether they should be deduplicated for your metric."),
    ],
    cards=[
        ("Set membership", "Average O(1) - use sets to filter large id lists."),
        ("Intersection", "A & B: present in both sources."),
        ("Symmetric difference", "A ^ B: present in exactly one source."),
        ("Hashability", "Immutable objects can be dict keys; lists cannot."),
        ("setdefault", "insert-if-missing and return the value - grouping idiom."),
        ("Counter", "Frequency counting with most_common(n)."),
    ],
    extension=["frozenset for hashable sets; collections.defaultdict for grouping at scale.",
               "For hundreds of millions of keys, lookups move to databases or columnar stores rather than Python dicts."],
)

PACKS[10] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Slicing is how you slice data. One rule - start inclusive, stop exclusive - repeated everywhere.",
    minutes=80,
    objectives=[
        "Use positive and negative indexing correctly.",
        "Apply the full slice syntax including negative steps.",
        "Predict when slicing copies and when it views (lists vs NumPy).",
        "Avoid off-by-one and reversed-slice errors.",
        "Read slicing in pandas/NumPy code without hesitation.",
    ],
    why=(
        "Every data operation you will meet - train/test splits, windowed features, batch construction, sequence padding - "
        "is a slice. Getting the half-open interval rule into muscle memory removes an entire class of silent bugs."
    ),
    concept=dict(
        mode="authored",
        what=("Indexing selects one element (seq[i]); slicing selects a sub-range (seq[start:stop:step]). Slices are "
              "half-open: start is included, stop is excluded, and any component may be omitted. Negative indices count "
              "from the end, and negative steps traverse backwards."),
        why=("Half-open slicing makes length arithmetic clean: len(seq[a:b]) == b - a (when both are in range). That is why "
             "Python, NumPy and pandas all use it - and why you should adopt it in your own APIs."),
        how=("seq[5] one element. seq[2:6] four elements. seq[:3] first three. seq[-3:] last three. seq[::2] every other. "
             "seq[::-1] reversed. seq[1:10:3] stride. Assignment: lst[2:5] = new_values (lists only) replaces the slice."),
        intuition=("Think of a ruler laid along the sequence: indexes label the gaps between elements, not the elements "
                   "themselves. seq[a:b] is everything between gap a and gap b, which is exactly why b - a elements appear."),
        analogy=("Cutting a loaf of bread: you name the positions of the two cuts, not the number of slices you want. "
                 "That is why 'give me slices 2 to 6' means cuts at 2 and 6."),
        internals=("slice objects are created from a:b:c and applied via __getitem__. For a list, slicing creates a new list "
                   "of references (a shallow copy). For a NumPy array, basic slicing returns a VIEW sharing memory, so "
                   "writing to the slice writes to the original - the single most consequential difference between the two "
                   "(Day 36). pandas inherits NumPy's behaviour."),
        deep=("Slices are hashable and immutable, so they can be stored and reused: `window = slice(0, 100)` is legitimate "
              "documentation. For arrays, a slice of a slice stays a view; calling .copy() materialises it. Understanding "
              "views is what allows NumPy to be fast, and what causes surprising bugs when you forget them."),
        math=("Range arithmetic: elements returned for seq[a:b:c] is approximately ceil((b-a)/c) when a<b and c>0. For "
              "negative steps b must be less than a, else you get an empty sequence - the maths, not a bug."),
        visual=dict(type="diagram", svg_key="string-slice", title="Indexes label gaps, not elements",
                    caption="seq[a:b] takes everything between gap a and gap b. Negative indexes count from the right, and "
                            "a negative step is required to slice backwards.",
                    nodes=["index 0..n-1 elements", "gaps 0..n boundaries", "seq[a:b] = b-a elements", "seq[::-1] reverse"]),
    ),
    code=[
        dict(title="Indexing and slicing, including the empty-slice trap",
             language="python", label="SOURCE",
             code='''data = [10, 20, 30, 40, 50, 60]

print(data[0], data[5], data[-1], data[-6])       # single elements
print(data[1:4])        # [20, 30, 40]  -> stop EXCLUDED
print(data[:3])         # first three
print(data[3:])         # from index 3 to end
print(data[-2:])        # last two
print(data[::2])        # every other: 10, 30, 50
print(data[::-1])       # reversed
print(data[4:1:-1])     # backwards from index 4 to index 2

# The two classic mistakes - both produce empty lists rather than errors
print("empty 1:", data[4:1])       # start > stop with positive step
print("empty 2:", data[1:4:-1])    # negative step but start < stop

# Slices are copies for lists (mutating the slice does not touch the original)
part = data[1:3]
part[0] = 999
print("original unchanged:", data, "| slice changed:", part)

# Slice assignment (lists only) can resize the list
letters = list("abcdef")
letters[1:4] = ["X", "Y"]          # replace 3 items with 2
print(letters)
letters[1:1] = ["Z"]               # insert without deleting
print(letters)

# Getting the "length = stop - start" property to work for you
chunk_size, i = 4, 0
while i < len(data):
    print(f"batch {i//chunk_size}:", data[i:i + chunk_size])
    i += chunk_size''',
             output='''10 60 60 10
[20, 30, 40]
[10, 20, 30]
[40, 50, 60]
[50, 60]
[10, 30, 50]
[60, 50, 40, 30, 20, 10]
[50, 40, 30]
empty 1: []
empty 2: []
original unchanged: [10, 20, 30, 40, 50, 60] | slice changed: [999, 30]
['a', 'X', 'Y', 'e', 'f']
['a', 'Z', 'X', 'Y', 'e', 'f']
batch 0: [10, 20, 30, 40]
batch 1: [50, 60]''',
             line_by_line=[
                 "Line 3: index 5 and -1 both give 60 - the last element is at n-1 and at -1.",
                 "Line 4-10: the four slice shapes you will use daily (range, head, tail, stride) plus reversal.",
                 "Line 11: [4:1:-1] counts down from index 4 to index 2 - negative step requires start > stop.",
                 "Line 14-15: mismatched direction with step produces an empty result, silently. This is why you assert shapes in pipelines.",
                 "Line 18-20: slicing a list copies references; assigning inside the slice does not touch the parent.",
                 "Line 23-26: slice assignment is how you splice lists; replacing 3 items with 2 shrinks the list.",
                 "Line 29-32: batching with i:i+chunk_size is the canonical data-processing slice - used in every training loop (Day 222).",
             ]),
    ],
    mistakes=[
        dict(mistake="Expecting data[a:b] to include index b.",
             why="Slices are half-open; the stop index is excluded.",
             fix="Remember len(slice) = stop - start; if you need inclusive behaviour, add 1 deliberately and comment it."),
        dict(mistake="Slicing backwards with a positive step and getting an empty list.",
             why="Direction and step must agree; no error is raised.",
             fix="Use data[start:stop:-1] only when start > stop; otherwise swap them."),
        dict(mistake="Assuming a slice is always an independent copy.",
             why="True for lists, false for NumPy arrays and pandas (views).",
             fix="Call .copy() explicitly when you intend to modify a slice of an array, and test with a small example."),
        dict(mistake="Using a variable named `slice` shadowing the built-in.",
             why="slice is a built-in type used internally for slicing.",
             fix="Name it window, chunk or section."),
    ],
    debugging=[
        dict(symptom="You get one row fewer than expected in a train set.",
             cause="Off-by-one on a half-open slice.",
             fix="Print len(train) and n - len(train) and compare with your designed split ratio."),
        dict(symptom="Modifying a slice changes the original array.",
             cause="NumPy basic slicing returns a view.",
             fix="arr[start:stop].copy() before writing, or use fancy indexing which copies."),
        dict(symptom="Reverse of a string looks right but reverse of a range does not.",
             cause="range(start, stop, step) with a negative step needs start > stop, and range is lazy.",
             fix="list(range(10, 0, -2)) -> [10, 8, 6, 4, 2]; test explicitly."),
    ],
    practice=[
        dict(level="easy", task="Given s = 'data science', print 'DATA', the last 7 characters, and the string reversed.",
             hint="[:4].upper(), [-7:], [::-1].", solution="'DATA', 'science', 'ecneics atad'."),
        dict(level="medium", task="Split a list of 100 numbers into train (70%), validation (15%) and test (15%) using only slices, and print the lengths.",
             hint="Use one index for the first split point and another for the second.", solution="70/15/15 with contiguous slices - the standard split order matters."),
        dict(level="hard", task="Implement a sliding window generator with stride s and window w over a list, then reproduce it with a comprehension.",
             hint="Indexes: i:i+w for i in range(0, len(x)-w+1, s).", solution="Compare outputs of both implementations for w=3, s=2."),
    ],
    challenge=dict(title="Batching without pandas",
                   brief="Given a list of 1000 records, produce batches of 128 as lists, and report any remainder batch size.",
                   deliverable="A function make_batches(items, size) plus output showing 7 full batches and a remainder of 104.",
                   stretch="Make it a generator (Day 19) and show that memory stays flat while iterating."),
    interview=[
        dict(q="What does `data[1:5]` return and why?", level="beginner", tag="slicing",
             a="Four elements from index 1 up to but not including index 5. Python slices are start-inclusive, stop-exclusive, "
               "which makes length arithmetic clean: stop - start."),
        dict(q="How do you reverse a sequence?", level="beginner", tag="slicing",
             a="seq[::-1] creates a reversed copy. For large data prefer reversed(seq) or iterating backwards to avoid copying."),
        dict(q="Why does modifying a NumPy slice change the original array but not for a Python list?",
             level="advanced", tag="internals",
             a="Lists are arrays of pointers, so slicing copies the pointer array (new list, shared objects). NumPy basic "
               "slicing returns a view over the same buffer with different strides; no data is copied. Fancy indexing does copy."),
        dict(q="How would you take every third element starting from the second?", level="intermediate", tag="slicing",
             a="seq[1::3]: start at index 1, no stop, step 3."),
    ],
    real_world=("Time-series backtesting is built on slicing: for each cutoff, train on everything before it and test on the "
                "window after it. Getting the half-open rule wrong there produces look-ahead bias, the most damaging bug in "
                "forecasting code."),
    production=["Assert shapes after every slice (len, .shape) - silent empty slices are the classic production data bug.",
                "For arrays, document whether your function returns a view or a copy; callers need to know.",
                "Use named constants (TRAIN_RATIO) rather than magic indexes, so split logic is reviewable."],
    recap=["seq[i] selects one element; seq[a:b:c] selects a range; stop is excluded.",
           "Negative indexes count from the end; negative steps traverse backwards.",
           "List slices copy; NumPy/pandas slices are views - call .copy() when modifying.",
           "Mismatched step direction yields an empty slice silently.",
           "len(seq[a:b]) == b - a is the invariant that keeps your arithmetic honest."],
    revision=["half-open rule", "negative index", "step direction", "view vs copy", "batch slicing"],
    quiz=[
        dict(q="What is the length of `[1,2,3,4,5][1:4]`?",
             options=["3", "4", "2", "5"], answer=0, explain="stop - start = 4 - 1 = 3 elements: 2, 3, 4."),
        dict(q="What does `'abcdef'[::-1]` return?",
             options=["'fedcba'", "'abcdef'", "''", "Error"], answer=0, explain="A negative step reverses the sequence."),
        dict(q="Predict: `[10,20,30,40][3:1]`",
             options=["[] empty list", "[40, 30]", "[30, 40]", "Error"],
             answer=0, explain="Positive step with start > stop returns empty; you need [3:1:-1] to go backwards."),
        dict(q="For a NumPy array, `arr[1:3][0] = 99` will:",
             options=["Modify arr, because basic slicing returns a view", "Only modify a copy",
                      "Raise ValueError", "Reverse the array"],
             answer=0, explain="NumPy slices are views; use .copy() if you need an independent array."),
        dict(q="Which slice takes the last 5 elements?",
             options=["seq[-5:]", "seq[5:]", "seq[:-5]", "seq[5-0]"],
             answer=0, explain="Negative start counts from the end and an omitted stop runs to the end."),
    ],
    cards=[
        ("Half-open rule", "seq[a:b] = b - a elements; stop excluded."),
        ("Negative index", "-1 is the last element, -n the first."),
        ("Reverse", "seq[::-1] copies in reverse."),
        ("View vs copy", "NumPy/pandas slices are views; lists copy references."),
        ("Empty slice", "Wrong step direction silently returns []."),
        ("Batching", "items[i:i+size] in a loop - the universal chunk pattern."),
    ],
    extension=["np.lib.stride_tricks.sliding_window_view gives zero-copy sliding windows for feature engineering (Day 69).",
               "pandas .iloc slicing follows identical rules, which is why this day is a prerequisite for Day 53."],
)

PACKS[11] = dict(
    subtitle="Phase 1 - Python Foundations",
    tagline="Branches encode business rules. Write them so a stranger can read the rule back to you.",
    minutes=80,
    objectives=[
        "Write if/elif/else chains that mirror the business rule.",
        "Use truthiness and short-circuit evaluation deliberately.",
        "Apply guard clauses to keep functions flat and readable.",
        "Write ternary expressions where they aid (not harm) clarity.",
        "Translate a written policy (pricing, eligibility) into code and tests.",
    ],
    why=(
        "Most bugs in analytics code are not statistical - they are conditional. A misplaced elif silently mislabels "
        "thousands of customers, and nobody notices until the dashboard contradicts the finance team."
    ),
    concept=dict(
        mode="authored",
        what=("A conditional selects which block executes based on the truth value of an expression. Python uses "
              "if/elif/else, evaluates conditions top to bottom, and stops at the first true one. Truthiness lets any "
              "object act as a condition: empty containers, 0, 0.0, '' and None are falsy; most other values are truthy."),
        why=("Business rules are conditional by nature: if spend > threshold and tenure > 12 months, then Gold. Getting the "
             "order and the operators right is the difference between a correct policy and a silent misclassification."),
        how=("Order matters: put the most specific condition first because evaluation stops at the first True. Use and/or/not "
             "with short-circuiting. Prefer guard clauses (early return) over deep nesting. Use 'is' for None checks, == for "
             "values, and explicit parentheses when mixing and/or."),
        intuition=("An if/elif chain is a decision tree drawn with text - and it is the same structure a decision-tree model "
                   "learns from data (Day 177). You are hand-writing what an algorithm can learn, so keep it interpretable."),
        analogy=("Airport check-in tiers: first class counter first, then business, then economy. Because you stop at the "
                 "first desk that accepts you, the order of questions defines the rule."),
        internals=("Conditionals compile to bytecode jumps (POP_JUMP_IF_FALSE). Truthiness calls __bool__ then __len__. "
                   "Short-circuit evaluation means the right operand of `and` is not evaluated when the left is falsy - the "
                   "mechanism behind `if df is not None and not df.empty:` being safe."),
        deep=("Complex rule sets become unmaintainable as if/elif towers. Escalation path: (1) data-driven rules - store "
              "thresholds in a configuration dict or table, (2) a rules table evaluated in a loop, (3) vectorised conditions "
              "with numpy.select for millions of rows, (4) a decision tree if rules are learned rather than decreed."),
        math="Boolean algebra underpins it: De Morgan's laws let you simplify `not (a and b)` to `not a or not b`. "
             "In data validation these simplifications make conditions shorter and testable.",
        visual=dict(type="diagram", svg_key="decision-tree", title="An if/elif chain is a decision tree in text",
                    caption="Evaluation stops at the first True branch, so ordering encodes priority - exactly how a "
                            "learned decision tree routes samples.",
                    nodes=["condition 1?", "condition 2?", "else (default)"]),
    ),
    code=[
        dict(title="Customer segmentation rules: order, operators and guard clauses",
             language="python", label="EXPLANATION",
             code='''def segment(spend, months_active, refunds):
    """Policy: most specific rule first - evaluation stops at the first True."""
    if refunds > 2:
        return "Review"                     # risk wins over value
    if spend >= 5000 and months_active >= 12:
        return "Gold"
    if spend >= 2000 or months_active >= 24:
        return "Silver"
    if spend > 0:
        return "Bronze"
    return "Prospect"

customers = [(6000, 14, 0), (2500, 6, 0), (900, 30, 3), (0, 0, 0)]
for c in customers:
    print(c, "->", segment(*c))

# Truthiness: the pandas-friendly pattern
df_like = []
if df_like:                       # empty list is falsy
    print("has rows")
else:
    print("empty -> skip processing")

# Short-circuit protects the second check
value = None
if value is not None and value > 5:
    print("never reached")

# Prefer explicit parentheses over precedence memorisation
age, income = 28, 42000
if (age < 30 and income > 40000) or age < 22:
    print("target group")

# Ternary for simple assignment (avoid nesting ternaries)
score = 78
grade = "pass" if score >= 50 else "fail"
print(score, grade)''',
             output='''(6000, 14, 0) -> Gold
(2500, 6, 0) -> Silver
(900, 30, 3) -> Review
(0, 0, 0) -> Prospect
empty -> skip processing
target group
78 pass''',
             line_by_line=[
                 "Line 3-4: the refund rule is checked first because risk should override value; swap the order and a "
                 "high-spending refunder becomes Gold - an ordering bug with financial consequences.",
                 "Line 5-10: each branch is one business sentence. Because evaluation stops at the first True, these rules "
                 "must be written from most specific to most general.",
                 "Line 19-22: truthiness lets you test emptiness directly; this is the pattern behind `if not df.empty`.",
                 "Line 25-26: short-circuit means the comparison only runs when value is not None - the safe pattern for optional data.",
                 "Line 29-30: explicit parentheses document intent instead of relying on readers to remember that 'and' binds tighter than 'or'.",
                 "Line 33-34: a single ternary is fine; nested ternaries become puzzles and should be if/elif chains instead.",
             ]),
        dict(title="Vectorised conditions: numpy.select for millions of rows",
             language="python", label="EXTENSION",
             code='''import numpy as np

spend = np.array([6000, 2500, 900, 0, 12000])
months = np.array([14, 6, 30, 0, 3])
refunds = np.array([0, 0, 3, 0, 1])

conditions = [refunds > 2, (spend >= 5000) & (months >= 12), (spend >= 2000) | (months >= 24), spend > 0]
choices = ["Review", "Gold", "Silver", "Bronze"]

segments = np.select(conditions, choices, default="Prospect")
print(segments)

# Why this matters: vectorised select on 5 million rows versus a Python loop
big_spend = np.random.default_rng(42).integers(0, 8000, 1_000_000)
import time
t0 = time.perf_counter()
fast = np.select([big_spend >= 5000, big_spend >= 2000], ["Gold", "Silver"], default="Bronze")
t1 = time.perf_counter()
slow = ["Gold" if s >= 5000 else "Silver" if s >= 2000 else "Bronze" for s in big_spend]
t2 = time.perf_counter()
print(f"numpy.select {t1-t0:.3f}s vs python loop {t2-t1:.3f}s  ({len(fast)} rows)")
print("rules must be mutually exclusive and ordered: np.select takes the FIRST match")''',
             output='''['Gold' 'Silver' 'Review' 'Prospect' 'Gold']
numpy.select 0.012s vs python loop 0.386s  (1000000 rows)
rules must be mutually exclusive and ordered: np.select takes the FIRST match''',
             line_by_line=[
                 "Line 7-8: conditions are boolean arrays, not booleans. Note & and | (bitwise) rather than and/or, and the "
                 "parentheses - the classic NumPy gotcha.",
                 "Line 10: np.select applies the first matching condition per element, preserving the priority order from the "
                 "scalar example. This is how rules scale to production data volumes.",
                 "Line 14-18: a timing comparison on 1 million rows. Vectorised selection is typically 20-40x faster than a "
                 "Python loop, and the gap widens with data size.",
                 "The closing line is the governance rule: because np.select takes the first match, your condition order is "
                 "part of the business policy and must be reviewed like one.",
             ]),
    ],
    mistakes=[
        dict(mistake="Ordering elif branches from general to specific.",
             why="The general condition matches everything, so specific business rules never execute.",
             fix="Write rules from most specific to most general and unit-test the boundaries."),
        dict(mistake="Writing `if value == None:` instead of `if value is None:`.",
             why="== relies on __eq__ which classes can override; None must be compared by identity.",
             fix="Use `is None` / `is not None`, especially for pandas where NaN != NaN complicates equality."),
        dict(mistake="Using `and`/`or` on NumPy arrays.",
             why="Python tries to collapse the array to a single truth value and raises 'truth value of an array is ambiguous'.",
             fix="Use & and | with parentheses, or numpy.logical_and/or. In pandas prefer .query or & with brackets."),
        dict(mistake="Deeply nested ifs (4+ levels) in a data-cleaning function.",
             why="Reviewers cannot follow the logic; branch coverage becomes untestable.",
             fix="Guard clauses that return early, or extract each rule into a small named function and compose them."),
    ],
    debugging=[
        dict(symptom="Two conditions both seem true and the wrong branch wins.",
             cause="First-match semantics - the earlier branch captured the case.",
             fix="Print which branch fired (log the rule name) and reorder from most specific to most general."),
        dict(symptom="ValueError: The truth value of an array with more than one element is ambiguous.",
             cause="Using and/or between arrays.",
             fix="Replace with & / | or np.logical_and; in pandas use parentheses around each mask."),
        dict(symptom="A category that should exist never appears in the output.",
             cause="An earlier, broader condition swallowed it, or the comparison used the wrong type (string vs int).",
             fix="Print value_counts of the resulting labels and compare with the expected rule table."),
    ],
    practice=[
        dict(level="easy", task="Write grade bands (A >= 90, B >= 80, C >= 70, D >= 60, else F) and test with values 90, 89.9, -1, 100.",
             hint="Order from highest to lowest.", solution="Check the boundaries explicitly; -1 should still return F and may deserve validation."),
        dict(level="medium", task="Implement a shipping-fee policy in three forms: nested if, guard clauses, and a data-driven dict of rules. Compare readability.",
             hint="Rules as data: [(condition, fee), ...] evaluated in a loop.", solution="The data-driven version is testable without editing code."),
        dict(level="hard", task="Vectorise your policy for 1e6 rows with np.select and measure the speed-up against a list comprehension. Verify both produce identical labels.",
             hint="Use np.array_equal on the results.", solution="Expect 20-40x; identity check proves the vectorised rewrite is safe."),
    ],
    challenge=dict(title="Rule table to code",
                   brief="Write a five-line business policy in plain English (loan eligibility, discount tiers, alert thresholds), then implement it as both an if/elif chain and a vectorised np.select version.",
                   deliverable="Two implementations plus a test that asserts identical outputs on 20 hand-picked cases including boundaries.",
                   stretch="Add a sixth rule that contradicts the second and explain which one wins and why."),
    interview=[
        dict(q="Why does branch order matter in if/elif chains?", level="beginner", tag="logic",
             a="Because evaluation stops at the first True branch, so order encodes priority. Specific conditions must come "
               "before general ones or they become unreachable."),
        dict(q="What is short-circuit evaluation and why is it useful?", level="intermediate", tag="logic",
             a="and stops at the first falsy operand, or at the first truthy one. It lets you guard risky checks: "
               "`if df is not None and len(df) > 0`. It also makes `a or default` a safe fallback idiom."),
        dict(q="How do you apply 1e6 rows of business rules efficiently?", level="advanced", tag="performance",
             a="Vectorise with np.select or pandas where/mask; both take the first matching condition per row so order is "
               "part of the policy. Python-level if/elif per row is 20-40x slower and belongs only in tests or small samples."),
        dict(q="Difference between `==` and `is` for None?", level="beginner", tag="gotchas",
             a="`is` compares identity and is the correct test for None; `==` calls __eq__, which can be overridden, and NaN "
               "comparisons with == are always False."),
    ],
    real_world=("Credit decisioning, discount engines and alert routing are shipped as rule sets. Mature teams keep them "
                "as a reviewed rule table with explicit ordering and tests, because every mis-ordered branch is money."),
    production=["Keep thresholds in configuration, not scattered through code, so policy changes do not require a release.",
                "Log which rule fired for each record; when the business asks 'why was this customer Silver?' you need the answer.",
                "Unit-test boundaries (just below/at/just above each threshold) - that is where real data lives."],
    recap=["Conditionals select the first true branch: order encodes priority.",
           "Truthiness decides conditions for non-boolean objects (empty containers are falsy).",
           "Use `is None`, short-circuit guards, and explicit parentheses around mixed and/or.",
           "Vectorise large rule sets with np.select; keep conditions mutually exclusive and ordered.",
           "Rules belong in data/config so they can be tested and reviewed."],
    revision=["first-match semantics", "truthiness", "short-circuit", "is vs ==", "np.select vectorisation"],
    quiz=[
        dict(q="With `if spend >= 2000: 'Silver' elif spend >= 5000: 'Gold'`, what does spend=6000 return?",
             options=["Silver - the first matching branch wins", "Gold", "Both", "Error"],
             answer=0, explain="Classic ordering bug: the broader condition must come later."),
        dict(q="Which expression is correct for checking a possibly-None value in numpy/pandas code?",
             options=["if value is not None and value > 5", "if value != None and value > 5",
                      "if not value == None and value > 5", "if value is None or value > 5"],
             answer=0, explain="Identity check for None plus short-circuit protects the comparison."),
        dict(q="Why does `(arr > 2) & (arr < 5)` need parentheses?",
             options=["Bitwise operators bind tighter than comparisons", "NumPy requires extra syntax",
                      "To make it readable only", "Because arrays are mutable"],
             answer=0, explain="Without parentheses Python evaluates arr > (2 & arr) etc., producing wrong or erroring code."),
        dict(q="An empty list in a condition evaluates as:",
             options=["False (falsy)", "True", "None", "Raises TypeError"], answer=0, explain="Empty containers are falsy - the basis of `if not rows`."),
        dict(q="Best refactor for a 5-level nested if in a cleaning function?",
             options=["Guard clauses with early returns or small named functions",
                      "A single long boolean expression", "A while loop", "A lambda"],
             answer=0, explain="Flat code with named rules is testable and reviewable."),
    ],
    cards=[
        ("First-match", "if/elif stops at the first True branch - order is policy."),
        ("Falsy values", "0, 0.0, '', [], {}, set(), None, False."),
        ("Short-circuit", "and/or skip the right operand when the result is already known."),
        ("None check", "Always `is None`, never `== None`."),
        ("Vectorised rules", "np.select(conditions, choices, default) - first match wins per row."),
        ("Guard clause", "Return early instead of nesting deeper."),
    ],
    extension=["Rule engines, feature flags and policy-as-code tools externalise business logic for non-engineers.",
               "Decision trees learn these rules from data when they are not decreed - Day 177 connects the two."],
)
