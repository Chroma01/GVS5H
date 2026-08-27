
## ideation
Core difficulty: the middle segment’s distinct count depends on both cut positions, so a simple `prefix[i] + suffix[j+1]` decomposition is insufficient. Need maximize `P[i] + D(i+1,j) + S[j+1]` over `1 <= i < j <= N-1` in near-linear time.

Key sweep insight: fix the right cut `j` and maintain, for every possible left cut `i < j`, the value `P[i] + distinct(A_{i+1..j})`. When `j` advances and `x = A_j` is appended to the middle, `x` is newly distinct exactly for left cuts `i >= prev[x]`, where `prev[x]` is the previous occurrence of `x` before `j` (use `0` if none). Thus only a suffix/prefix range of cut positions needs `+1`, suggesting a lazy segment tree / range-add range-max structure.

Complexity target: `O(N log N)` time, `O(N)` memory. `A_i <= N` allows a direct `last` array. Python needs fast I/O and preferably an iterative lazy segment tree or carefully optimized recursive one.

Pitfalls: off-by-one on suffix index (`S[j+1]`); ensuring all three parts are non-empty (`i >= 1`, `j <= N-1`, `i < j`); updating the correct cut range `[max(1, prev[x]), j-1]`; not querying before applying `A_j`; avoiding `O(N^2)` middle recomputation; large answer fits in int but use Python ints anyway.

## worker: Implement the complete O(N log N) Python solution:
- **Algorithm**: For each right cut `j` (2..N-1), maintain for every left cut `i < j` the value `P[i] + distinct(A[i+1..j])` in a segment tree; the answer candidate is that max plus `S[j+1]`.
- **Key update rule**: when `j` advances and `x = A[j]` is appended to the middle, `x` is newly distinct exactly for left cuts `i >= prev[x]` (previous occurrence of `x`, 0 if none). So apply `+1` on cut range `[max(1, prev[x]), j-1]`.
- **Optimizations for Python speed**:
  - Left-cut positions are activated lazily (initially `-inf`): position `j-1` becomes active at step `j` with value `P[j-1]`, then receives the `+1` from the range add. This makes the query a plain root read (`tree[1]`) instead of a range-max query with push-downs.
  - Proved no push-downs are ever needed: updates are range adds followed by rebuilding both boundary root-to-leaf paths, which maintains the invariant `tree[p] = true_subtree_max - (lazy on strict ancestors)`. Since only `tree[1]` (no ancestors) is read, values are always exact.
  - Also proved ancestors of the newly activated leaf always have lazy 0 (any node with pending lazy lies entirely inside a past update range ending `<= R-1`), so activation is a plain leaf assignment.
- **Verification**: hand-traced Sample 1 (answer 5) and Sample 2 (answer 9) through the exact update logic; both match. Edge cases checked: `N=3`, all-equal values, all-distinct values.
- **Complexity**: `O(N log N)` time (~60 simple loop iterations per step), `O(N)` memory, fast stdin parsing via `read().split()`.
