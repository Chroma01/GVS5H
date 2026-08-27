
## ideation
The plan's key insight: f(L,R) = number of runs of consecutive integers among distinct values in A[L..R] = (distinct count) − (number of v such that both v and v+1 appear). Need to verify this carefully: an operation erases [l,r] where every value in [l,r] appears on the board; it erases ALL occurrences of those values. So one operation can erase exactly a set of values forming a complete interval [l,r] ⊆ present values. To minimize operations, we want to cover the present value set with as few complete intervals as possible — but intervals can be larger than minimal runs? No: [l,r] must be a subset of present values, so it must lie within a maximal run of consecutive present values. Each maximal run can be erased in one operation (take [l,r] = the whole run). And we need at least one operation per run since runs are separated by gaps (a single interval can't span a missing value). So f = number of maximal runs = distinct − (# adjacent pairs both present). 

Answer = Σ subarrays distinct − Σ_{v=1}^{N-1} (subarrays containing both v and v+1).

Term 1: classic — each position i contributes (i − last[A_i]) * (N − i + 1) where last is previous occurrence (1-indexed).

Term 2: for each v, let P = sorted positions of value v, Q = positions of value v+1. Count subarrays containing at least one position from P and one from Q. Compute via complement: total − avoid P − avoid Q + avoid both. "Avoid set S" count = sum over gaps g of g(g+1)/2 where gaps are runs of positions not in S. Avoid both = avoid P∪Q. Each is O(|P|+|Q|) per v, total O(N) since each position belongs to at most two values' lists (as v and as v+1... actually position with value x appears in list for v=x and in "other" list for v=x−1; union work per v is O(|P|+|Q|), summed over v gives O(2N) total, fine).

Pitfalls: 64-bit overflow in other languages (Python fine); values v and v+1 both must exist in whole array else count 0; N up to 3e5, O(N) fine. Edge: A_i can equal N, then v+1 = N+1 doesn't exist, skip.

Alternative: could also count "both present" directly via two pointers per v, but complement with gaps is simplest.

## worker: Implement the full solution in Python: term1 via l
- **Reduction**: For subarray A[L..R], one operation erases all occurrences of a complete value-interval [l,r] contained in the present value set. Hence f(L,R) = number of maximal runs of consecutive integers among distinct present values = (distinct count) − (# of v with both v and v+1 present). Verified by brute force on all subarrays of many small random arrays (n ≤ 8) against a BFS/greedy-free direct computation of f (minimum interval cover = runs count, cross-checked with exhaustive search over operation sequences for tiny cases).
- **Term 1**: classic last-occurrence contribution: position i adds `(i - last[A_i]) * (n - i + 1)`.
- **Term 2**: for each value v, count subarrays containing both v and v+1 via inclusion–exclusion: total − avoid(v) − avoid(v+1) + avoid(v ∪ v+1), where "avoid S" = sum of g(g+1)/2 over gaps of consecutive non-S positions. Each position appears in at most two lists (as value v and as value v+1's partner), so total work is O(N).
- **Verification**: Sample 1 → 16, Sample 2 → 23, Sample 3 → 129 (all match). Random small arrays matched brute force exactly.
- Complexity: O(N) time, O(N) memory; Python ints avoid overflow.
