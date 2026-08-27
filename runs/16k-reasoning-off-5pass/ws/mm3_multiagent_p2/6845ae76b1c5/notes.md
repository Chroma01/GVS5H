
## ideation
The problem asks for K queries, each asking for the sum of absolute differences between the first X elements of sorted A and the first Y elements of sorted B. N ≤ 1e5, K ≤ 1e4, so a per‑query O(N) solution is too slow.

Key observation: after sorting A and B, the answer for a query (X,Y) can be expressed using two auxiliary sums over the prefix of A:
- `c_i` = number of B values ≤ A_i among the first Y B's
- `s_i` = sum of those B values

Then  
`answer = 2·Σ_{i≤X} (A_i·c_i) – Y·Σ_{i≤X} A_i + X·Σ_{j≤Y} B_j – 2·Σ_{i≤X} s_i`.

All terms except the two sums over A can be obtained from prefix sums of the sorted arrays. The remaining challenge is to compute, for many queries, the sums  
`Σ_{i≤X} (A_i·c_i)` and `Σ_{i≤X} s_i` quickly.

These sums can be maintained with a segment tree (or BIT) that supports range updates and range queries. Process B values in increasing order of Y (offline). When a new B_j is activated, it contributes +1 to `c_i` and +B_j to `s_i` for every A_i ≥ B_j. Since A is sorted, this is a suffix range `[pos, N-1]` where `pos = lower_bound(A, B_j)`. A range update on the segment tree adds:
- `+1` to the count `c_i` (so `Σ c_i` increases by the segment length, and `Σ A_i·c_i` increases by the sum of A in that segment),
- `+B_j` to the sum `s_i` (so `Σ s_i` increases by `B_j` times the segment length).

After processing the first Y B's, a query (X,Y) is answered by a range query on the prefix `[0, X-1]` of the segment tree, retrieving the two needed sums. The whole procedure is O((N+K) log N).

Pitfalls:
- Use 0‑based indices consistently.
- Prefix sums `SA` and `SB` must be 1‑based for easy access (`SA[x]` = sum of first x A's).
- The segment tree must store the static sum of A in each node (or compute it via global prefix sums) to update `Σ A_i·c_i` correctly.
- All sums fit in 64‑bit, but Python integers are unlimited.

## worker: Implement the solution in Python: read input, sort
The solution uses offline processing with a segment tree that supports range updates and range queries.  
- Sort `A` and `B` and precompute prefix sums `SA` and `SB`.  
- For each query `(X,Y)`, the answer is expressed as  
  `2·Σ_{i≤X} (A_i·c_i) – Y·Σ_{i≤X} A_i + X·Σ_{j≤Y} B_j – 2·Σ_{i≤X} s_i`,  
  where `c_i` = number of activated `B` values ≤ `A_i` and `s_i` = sum of those `B` values.  
- Process `B` values in increasing order of `Y`. When a new `B_j` is activated, it contributes `+1` to `c_i` and `+B_j` to `s_i` for every `A_i ≥ B_j`. Because `A` is sorted, this is a suffix range `[pos, N-1]` where `pos = lower_bound(A, B_j)`.  
- The segment tree stores per node: `sumC` (Σ c_i), `sumW` (Σ A_i·c_i), `sumS` (Σ s_i), and lazy values for pending count and sum additions.  
- After activating the first `Y` `B` values, a query is answered by a range query on the prefix `[0, X-1]` of the segment tree, retrieving `sumW` and `sumS`.  
- Complexity: sorting `O(N log N + K log K)`, segment tree operations `O((N+K) log N)`. Memory `O(N)`.
