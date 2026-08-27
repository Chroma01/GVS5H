
## ideation
The problem asks for the maximum number of disjoint pairs (top, bottom) within a subarray `[L,R]` such that `top ≤ bottom/2`. The array is sorted non‑decreasing.

**Core difficulty:**  
A naïve greedy per query works in linear time, but `Q` can be `2·10^5`, so we need roughly `O((N+Q) log N)` or similar.

**Key observations:**
1. Precompute `next[i]` = smallest index `j` such that `A[j] ≥ 2·A[i]` (or `N+1` if none). This can be done in `O(N)` with a two‑pointer scan from the right.
2. `next[i]` is **non‑decreasing** because `A` is sorted: if `i < j` then `2·A[i] ≤ 2·A[j]`, so the first index satisfying the condition for `j` is at least that for `i`.
3. For a fixed right endpoint `R`, an index `i` is a valid “top” iff `next[i] ≤ R`. Because `next` is non‑decreasing, the set of valid tops in `[1,R]` is a prefix `[1, M]` where `M = max{i | next[i] ≤ R}`.
4. Within a query `[L,R]`, the valid tops are exactly `[L, T]` where `T = min(R, M)`. All elements in `(T, R]` are forced bottoms.
5. The optimal matching is obtained by scanning tops in increasing order and pairing each with the **smallest available bottom index ≥ next[i]**. This greedy is optimal because the compatibility condition is monotone.
6. The matching process on `[L,R]` can be simulated with two pointers: maintain a pointer `p` (the smallest unused bottom index). For each `i` from `L` to `T`, advance `p` until `p ≥ next[i]`; if `p ≤ R`, match and set `p = p+1`; otherwise stop. The answer is the number of successful matches.

**Candidate approaches:**
- **Two‑pointer per query:** `O(R-L)` per query → too slow.
- **Segment tree with “merge” states:** Each node stores the result of processing its segment assuming no incoming bottoms, but the state must capture the multiset of available bottom indices. Because `next` is non‑decreasing, the available bottoms after processing a segment form a contiguous suffix of the segment’s indices. This allows a compact representation: for a segment, store the number of matches and the “offset” or the smallest index of an available bottom. However, the condition `next[i] ≤ R` depends on the global `R`, so a static segment tree is not directly applicable.
- **Offline processing by `R`:** Sort queries by `R`. As `R` increases, `M` (the last valid top) increases. Maintain a data structure that can answer, for any `L`, the number of matches in `[L,R]`. This resembles a “sliding window” matching problem.
- **Binary indexed tree (Fenwick) with order‑statistics:** Simulate the two‑pointer process efficiently by finding the next available bottom ≥ `next[i]` using a BIT that stores 1 for unused bottoms. For each query we would need to reset the BIT, which is costly.
- **Divide‑and‑conquer (CDQ) on queries:** Recursively solve for left and right halves, handling cross‑queries. This is a standard technique for offline interval queries with a greedy that depends on both ends.

**Pitfalls:**
- The simple “stack” greedy (pop any bottom) is incorrect because a top `i` can only match with a bottom `j ≥ next[i]`. The stack must respect this index constraint.
- The answer is **not** simply `min(#good, #bad)` because the goods are all on the left and the compatibility depends on the exact `next` values, not just counts.
- `next[i]` can be `N+1` (no valid bottom); treat it as “always bad”.
- The array can have equal values; `next[i]` must be strictly greater than `i` (or `N+1`) because a mochi cannot be paired with itself and `A[i] ≤ A[i]/2` is false for `A[i] > 0`.

**Next steps to try:**
1. Verify the two‑pointer greedy on random small arrays by brute force to ensure correctness.
2. Attempt an offline solution using a segment tree where each node stores the “state” of its segment as a function of the incoming bottom count, but parameterized by `R`. Since `next` is non‑decreasing, the state might be representable by just two numbers: the number of matches and the “required minimum bottom index” for the next top.
3. Explore a divide‑and‑conquer offline approach: for a segment `[l,r]`, precompute the matching result for any sub‑interval `[L,R] ⊆ [l,r]` in `O((r-l) log(r-l))` time, then answer queries in `O(log N)` each. This is similar to the “offline segment tree for interval matching” used in some AtCoder problems.
4. Consider using a BIT to maintain the set of “available bottoms” as we sweep `R`, and for each query `[L,R]` we need to count how many tops in `[L,T]` can be matched. This might be reducible to counting how many `i` in `[L,T]` satisfy `next[i] ≤ R` and the number of available bottoms ≥ `next[i]` is sufficient. This could be answered with a range‑count query on a BIT of “next” values.

## worker: Implement a brute-force checker for small N to con
I implemented a brute-force checker that enumerates all possible matchings for small subarrays (N ≤ 11) and compares with the proposed two-pointer greedy algorithm. The greedy precomputes `next[i]` (smallest index > i with `A[next[i]] ≥ 2·A[i]`) using a two-pointer scan in O(N). For a query `[L,R]`, it finds the largest index `M` with `next[M] ≤ R` (via binary search), sets `T = min(R, M)`, then simulates the matching: maintain a pointer `p` to the smallest unused bottom; for each top `i` from `L` to `T`, advance `p` to `max(p, next[i])`; if `p ≤ R`, match and increment `p`. The test runs 100 random arrays of sizes 2–11 and all subintervals of length ≥ 2, and confirms that the greedy result matches the exhaustive maximum matching.
