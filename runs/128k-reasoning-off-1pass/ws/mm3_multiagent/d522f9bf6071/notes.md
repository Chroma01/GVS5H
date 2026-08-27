
## ideation
**Core difficulty:**  
- Selecting *up to* 4 non‑overlapping intervals to maximize weight → small K (4) but large N (5e4) and large coordinates.  
- Lexicographically smallest index set among those achieving the max weight is the tricky tie‑breaker.

**Candidate approaches:**  
1. **DP + segment tree / Fenwick** (typical weighted interval scheduling with small K).  
   - Sort intervals by start (or end).  
   - For each interval, need the best previous state of size 0…3 that ends before its start.  
   - Maintain, for each k = 0..4, a structure mapping `position` → best state `(score, indices_tuple)` and supporting “max over all positions < l_i”. A Fenwick tree with four parallel arrays (one per k) works, where each node stores the best state for that k.  
   - State comparison: higher score wins; if scores equal, lexicographically smaller index tuple wins.  
   - Transition:  
     `new(k) = old_best(k-1) + (weight_i, [i])`  
     then update `fenwick_k at r_i` with `new(k)` (keeping the better of existing and new).  
   - Complexity: O(K · N log N) = O(4 N log N) = acceptable.  
   - Return the best state among all k by score then lexicographic order.

2. **DP + binary search + dict per k** (no segment tree).  
   - For each interval, binary search the last interval that ends before its start among the *sorted‑by‑end* list.  
   - Keep a dict `best[k][end] = best state` but we need to query “best among ends < l_i”. Could use a balanced BST (sortedcontainers) per k, but Python lacks one natively; segment tree is simpler.

3. **Brute‑force / meet‑in‑the‑middle** – impossible for 5e4.

4. **Greedy** – not optimal.

**Pitfalls:**  
- Intervals sharing a boundary are overlapping → strict `prev_end < l_i` (or `<=`, but need to be consistent with sort order).  
- Indices must be returned in **ascending order** of original positions; when building the tuple we just append `i` because we process intervals in order (if sorted by start) — but lexicographic order refers to indices as they appear in the returned array, which should be sorted ascending. Since we process in some order, we must sort the tuple before adding to state to keep the lexicographic property correct.  
- Need to store the actual index set (as a tuple) for tie‑breaking; using only scores will not yield lex smallest.  
- Up to 4 intervals → K small, but the segment tree must store 5 states (k=0..4). `k=0` is just empty state with score 0.  
- Large weights (1e9) and N (5e4) → scores can exceed 32‑bit, use Python int (unlimited).  
- The result should be the indices of the chosen intervals in the **original** input order, not the sorted order.  
- Edge cases: no intervals (but N≥1), all overlapping, identical intervals.

**Key idea to implement:**  
- Sort intervals by start (and maybe end) while remembering original index.  
- Fenwick tree of size N (or number of distinct r’s) where each node stores, for each k=0..4, the best state in its range.  
- `update(pos, state_k)` merges `state_k` into node’s existing `state_k` using the custom comparator (max score, min lex).  
- `query(pos)` returns, for each k, the best state among indices ≤ pos.  
- At each interval i, we do:  
  `prev = query(start_i)`  (best states for each k before this interval)  
  For k=1..4: `cur = (prev[k-1].score + w_i, tuple(sorted(prev[k-1].indices + [orig_idx])))`  
  Then `update(end_i, cur_for_k)`.  
- After processing all intervals, `query(max_coord)` gives the best states among all k. Pick the one with highest score (and smallest lex tuple if tie) and return its indices as a list.

**Why Fenwick over segment tree?**  
- Both are O(log N). Fenwick is easier to implement in Python with small K.

**Custom comparator:**  
Define a function `better(a, b)`:  
- If a is None → return b.  
- If b is None → return a.  
- If a.score != b.score → return a if a.score > b.score else b.  
- Else compare a.idx_tuple and b.idx_tuple lexicographically → return the smaller one (or the one with smaller length if prefix equal). Actually, when scores equal, we want the lexicographically smaller *list* of indices. Since we always keep tuples sorted, we can just compare tuples: `a.indices < b.indices` → a is better.

**Index handling:**  
- After sorting, we compress `r_i` to `[1..M]` for Fenwick. Use coordinate compression of all `r_i`.

**Return format:**  
- Convert the tuple of indices to a list. The order of indices in the list should be ascending (lexicographic order), which matches our tuple representation.

## worker: Implement the Fenwick tree class that stores, for 
- Implemented a Fenwick tree class `Fenwick` that stores, for each of the 4 counts (k=0..3), the best state `(score, indices_tuple)`.
- The `_better` method implements the tie-breaking rule: higher score wins; if scores are equal, the lexicographically smaller sorted index tuple wins.
- `update` propagates the state up the tree, merging with the existing best at each node.
- `query` aggregates the best states from the prefix `[1..pos]`.
- The main `maximumWeight` method sorts intervals by start, compresses end coordinates, and processes each interval. It queries the Fenwick for the best states ending before the current start, then extends them by one interval to create new states for k=1..4. States for k=1..3 are updated into the Fenwick; k=4 is tracked separately since no further extension is needed.
- Finally, it picks the best state among all counts (0..4) and returns its index list.

## worker: Test the current solution with the provided exampl
Tested the solution against the two provided examples and several edge cases:

- **Example 1** → `[2,3]` ✓
- **Example 2** → `[1,3,5,6]` ✓
- **Single interval** → `[0]` ✓
- **All overlapping** → picks the highest weight index `[3]` ✓
- **Identical intervals** → picks the one with largest weight `[2]` ✓
- **Touching boundaries** (`[1,2]` and `[2,3]`) correctly treated as overlapping → `[1]` ✓
- **Four non-overlapping** → returns all four `[0,1,2,3]` ✓
- **Large coordinates** → works fine ✓
- **Tie-breaking by shorter length** → `[1]` is returned over `[0,2]` ✓
- **Lexicographic tie** → `[0,1]` is returned over `[0,2]` (or equivalent) ✓
- **Capping at 4** when more are available → correctly picks the 4 with max weight `[1,2,3,4]` ✓

All tests pass. The algorithm runs in `O(N log N)` time (4 Fenwick operations per interval) and `O(N)` memory, well within the 5×10⁴ constraint.
