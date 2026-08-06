# Day 3 Learning Log

## Concepts completed

- Lists
- Tuples
- Dictionaries
- Sets
- Stack behavior
- Queue behavior
- Dictionary indexing
- Duplicate detection
- Big-O intuition
- Microbenchmarking with `timeit`

## Why each structure was selected

### List

The raw synthetic records were stored in an ordered `list` because records arrived in a dynamic sequence where order of ingestion mattered. Lists provide fast indexed access ($\mathcal{O}(1)$ by position) and allow dynamic appending ($\mathcal{O}(1)$ amortized) as new records arrive.

### Tuple

The required field names were stored in an immutable `tuple` (`REQUIRED_FIELDS`). Tuples prevent accidental runtime modification of schema definitions, communicate fixed structural constraints to other developers, and incur slightly less memory overhead than dynamic lists.

### Dictionary

Individual records were represented as dictionaries to map property names (e.g., `"age"`, `"department"`) to heterogeneous data types. The master lookup index (`build_record_index`) also used a dictionary to map `record_id` directly to record objects, enabling constant-time ($\mathcal{O}(1)$ average) key-based retrieval instead of scanning the full dataset.

### Set

Sets were used for duplicate detection (`find_duplicate_ids`) and tracking unique IDs because membership testing (`item in set`) operates in $\mathcal{O}(1)$ average time via hash tables. In contrast, checking membership in a list takes $\mathcal{O}(n)$ time, which would make duplicate detection across large datasets inefficient ($\mathcal{O}(n^2)$).

### Stack

A list-based stack was used to log processing steps in a Last-In, First-Out (LIFO) order. Actions were pushed onto the stack using `append()` ($\mathcal{O}(1)$) and the most recently completed action was retrieved using `pop()` ($\mathcal{O}(1)$ without index arguments).

### Queue

A First-In, First-Out (FIFO) queue was implemented using `collections.deque` (`double-ended queue`). `deque` provides $\mathcal{O}(1)$ atomic operations for both `append()` (enqueue) and `popleft()` (dequeue). Standard lists were avoided because `list.pop(0)` causes an $\mathcal{O}(n)$ memory shift of all remaining elements to the left.

## Lookup experiment

Dataset size: 10,000 synthetic records

| Target Position | Target ID | List Search Time | Dictionary Lookup Time |
|---|---|---:|---:|
| First record | `SYN-00001` | 0.000012 s | 0.000025 s |
| Last record | `SYN-10000` | 0.098431 s | 0.000026 s |
| Missing record | `SYN-99999` | 0.097812 s | 0.000026 s |

## What the results mean

The empirical timing results demonstrate the fundamental difference between sequential scanning and hash indexing:
1. **Best-case List Search ($\mathcal{O}(1)$)**: When the target is at index 0 (`SYN-00001`), the list loop terminates on the first iteration, performing as quickly as a dictionary lookup.
2. **Worst/Average-case List Search ($\mathcal{O}(n)$)**: When searching for the last element (`SYN-10000`) or a non-existent element (`SYN-99999`), the list search must evaluate every record in sequence. Execution time scales linearly with the size of the dataset.
3. **Dictionary Hash Lookup ($\mathcal{O}(1)$)**: Dictionary lookup times remain virtually constant regardless of position or presence. The key `SYN-10000` hashes directly to a bucket location in memory without iterating through other entries.

*Note: Microbenchmarks reflect machine-specific CPU load, memory caching, and Python interpreter overhead; they illustrate theoretical time complexity trends rather than absolute bounds.*

## Real error or confusion

Staging incremental commits failed with `no changes added to commit` and `fatal: pathspec 'notes/day03.md' did not match any files`.

## Root cause

All 332 lines of `exercises/day03.py` were added and committed in a single initial commit (`chore: add Day 3 data structures scaffold`). Subsequent `git add exercises/day03.py` commands registered no new unstaged changes. Additionally, the `notes/` directory and `day03.md` file had not yet been created on disk when running `git add`.

## Fix

Reset the initial commit soft-state using `git reset --soft HEAD~1` to keep the code intact while clearing the commit log. Used `git add -p` (patch mode) to selectively stage code chunks into distinct logical commits, and created the missing directory/file path using `New-Item -ItemType Directory -Force -Path notes`.

## One design decision I would improve

I would decouple raw data validation from duplicate handling earlier in the pipeline by returning a validated, deduplicated `dataclass` or schema wrapper object. Currently, dictionary indexing silently overwrites earlier records when duplicate IDs exist. Raising an explicit logging error or holding duplicates in an isolated quarantine list during ingestion would prevent data loss.

## Next smallest action

Begin Day 4: File handling, reading/writing CSV and JSON formats, exception handling, basic logging, and explicit type hints.