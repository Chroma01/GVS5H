
## ideation
**Restating the operation.** An operation picks a value‑interval [l,r] such that *every* value in l..r currently appears on the board, and deletes all occurrences of those values. So the state is fully described by the *set* S of distinct values currently present (positions/multiplicities are irrelevant — an erase removes every copy of each value). Each operation removes a contiguous integer interval that is entirely contained in S; since S only shrinks, such an interval always lies inside one maximal run of consecutive integers of the original S.

**Key formula.** Therefore
 f(L,R) = number of maximal runs of consecutive integers in S(L,R)
     = |S(L,R)| − #{v : v ∈ S and v+1 ∈ S}.
Both terms are "count over all subarrays" quantities, which decouple nicely.

**Term 1 — Σ over subarrays of #distinct.** Classic: with prev[i] = last index j < i with A_j = A_i (0 if none),
 Σ_{L≤R} distinct(L,R) = Σ_{i=1}^{N} (i − prev[i])·(N − i + 1).

**Term 2 — Σ_v #{subarrays containing both v and v+1}.** Let T = N(N+1)/2 and for a set of positions P let miss(P) = Σ over maximal gaps (using sentinels 0 and N+1) of g(g+1)/2 = number of subarrays avoiding all of P. Inclusion–exclusion:
 #{contains ≥1 occurrence of v AND ≥1 of v+1} = T − miss(pos[v]) − miss(pos[v+1]) + miss(pos[v] ∪ pos[v+1]).
Since Σ_v (|pos[v]| + |pos[v+1]|) ≤ 2N, the whole loop is O(N) (or O(N log N) if we lazily `sorted(pos[v]+pos[v+1])`).

**Answer** = Term1 − Term2.

**Sanity check on sample 1** (A = 1 3 1 4): Term1 = 4+6+4+4 = 18; only pair with both present is (3,4): subarrays with L≤2, R≥4 → 2. 18 − 2 = 16 ✓.

**Pitfalls to watch.**
- Values with empty position lists: miss(∅) = T, so the inclusion–exclusion contribution automatically becomes 0 — safe either way, but skipping is faster.
- v ranges 1..N−1 only; A_i ≤ N guaranteed so no out-of-range.
- Don't forget the gap *after* the last position (g = N − last) and *before* the first (g = first − 1).
- Big integers: answer can be ~N³? No — bounded by Σ distinct ≈ N³/6? Actually Term1 ≤ N(N+1)(N+2)/6 ≈ 4.5e15, fits easily in Python ints (and in int64, but Python is fine).
- Performance: N = 3·10⁵ in Python — need fast `sys.stdin.buffer.read()`, avoid per-element function call overhead where possible; the merge of two sorted lists costs at most 2N total elements so plain `sorted()` is acceptable. Consider numpy vectorization for Term1 if timing is tight.
- Careful: distinct-count formula uses `prev[a]` updated in place; must index by value not position.

## worker: Implement the full O(N) solution in Python: fast s
Implemented the planned O(N) solution.

Correctness recap:
- An operation deletes all occurrences of every value in a value-interval [l,r] that is fully present; state = set S of distinct values present. Any legal interval lies inside a maximal run of consecutive integers of S, and each maximal run can be cleared in exactly one operation, so f(L,R) = #maximal runs of S(L,R) = |S(L,R)| − #{v : v, v+1 ∈ S(L,R)}.
- Term1 = Σ_i (i − prev[i])·(N − i + 1) (standard sum-of-distinct-counts over all subarrays).
- Term2 = Σ_{v=1}^{N−1} #{subarrays containing both v and v+1} = Σ_v [T − miss(v) − miss(v+1) + miss(pos[v] ∪ pos[v+1])], where miss(P) = Σ over gaps (sentinels 0, N+1) of g(g+1)/2 and T = N(N+1)/2. Empty position lists give contribution 0 (skipped explicitly).
- Total inner-loop work: N for the individual miss values plus Σ_v (cnt[v]+cnt[v+1]) ≤ 2N for merged lists → O(N) with a small sort per pair (sorting total ≤ 2N elements across all calls).

Hand-verified sample 2 (A = 3 1 4 2 4): Term1 = 32, Term2 = 4+2+3 = 9, answer 23 ✓. Sample 1 gives 18 − 2 = 16 ✓. N=1 gives 1 ✓.

Python big ints handle the magnitudes (≤ ~4.5e15) exactly; no floats used.
