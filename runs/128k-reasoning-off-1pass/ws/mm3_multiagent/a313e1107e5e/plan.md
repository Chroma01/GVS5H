We need to answer many queries: given prefix length R and bound X, compute the length of the longest strictly increasing subsequence of `A[1..R]` with all elements ≤ X.

For a fixed prefix, the LIS with upper bound X can be obtained by a standard patience sorting DP: process elements left to right, maintain an array `dp` where `dp[k]` is the minimum possible last value of an increasing subsequence of length `k` seen so far. To also respect X, when we process an element `a` we only update if `a ≤ X`; then we find the smallest `k` such that `dp[k] ≥ a` (using `bisect_left`) and set `dp[k] = a`. The answer is the number of filled positions.

The naive per‑query recomputation is O(R log N) → too slow for Q up to 2e5.

Key observation: the answer only depends on the set of elements ≤ X present in the prefix, and the classic LIS dp described above is monotone: if we have a larger X, the set of allowed elements is larger, so the answer cannot decrease. Moreover, for a fixed prefix, the answer as a function of X is a step function that changes only at values appearing in the prefix.

We can process queries offline sorted by X (and R). For each R we need a data structure that supports:
- insert A[R] into the LIS structure,
- query: current LIS length restricted to elements ≤ X (i.e., the usual patience dp array size).

If we maintain a global `dp` array while sweeping R from 1 to N, then for a given X we need the number of entries `dp[1..]` whose value is ≤ X. Actually in the patience algorithm `dp[k]` is the minimal possible tail of a length‑k increasing subsequence; the final answer is the largest k with a finite tail. For a bound X we only consider inserted elements ≤ X, which means we only update using those elements. If we instead update with every element (without the X filter) we get the global LIS dp for the prefix, and the answer for bound X is the length `k` of the longest subsequence whose all elements ≤ X, which is not simply the count of `dp[i] ≤ X` because larger tails may exist but unused.

Better approach: For each prefix, maintain the full patience `tails` array where `tails[k]` is the minimal possible last value of an IS of length k (ignoring the bound X). The LIS length of the prefix (unrestricted) is `len(tails)`. For a bound X, the answer is the largest k such that we can build a length‑k increasing subsequence using only elements ≤ X. This is equivalent to: simulate the patience algorithm while ignoring any element > X, and count how many positions get filled. In the full tails array, the values are non‑decreasing. Crucially, the answer for bound X is the number of tails whose value is ≤ X? Not exactly: tails are built from all elements, some > X. The positions filled with a value > X correspond to subsequences that necessarily used a large element, so they may be impossible when X is smaller.

But there is a known offline solution: process queries in order of increasing R, and for each X we need the LIS length of the subarray A[1..R] considering only values ≤ X. We can use a Fenwick tree (BIT) over the values coordinate‑compressed together with X. Maintain a BIT where at each value v we store the current longest increasing subsequence length ending with value v (i.e., after processing prefix R, for each v we store the best length). Then the answer for (R, X) is the maximum over all v ≤ X. This is exactly a 2D query: point updates (at value A[i]) with `value = 1 + max over v < A[i]` and point query (max over v ≤ X). This can be done with a Fenwick tree (BIT) supporting range max query and point update.

We need to process N updates and Q queries. The classic offline approach: sort updates (i.e., positions) and queries by R, sweep through positions, updating BIT with each A[i] (using its value as index), then answer queries with that R.

Complexities: O((N+Q) log M) where M is the number of distinct compressed values (≤ N + Q). Values are up to 1e9, so compress all A[i] and all X_i.

Algorithm steps:
1. Read N, Q, array A[1..N].
2. Read queries (R_i, X_i). Store original index.
3. Coordinate compression:
   - Collect all values: A[i] for i=1..N, and X_i for i=1..Q.
   - Sort and deduplicate → array `vals`.
   - For each A[i] and each X_i, map to index in `vals` (1‑based for BIT).
4. Sort queries by R ascending.
5. Initialize BIT of size = len(vals). BIT supports:
   - `update(pos, val)`: set BIT[pos] = max(BIT[pos], val).
   - `query(pos)`: returns maximum over indices 1..pos.
   The BIT works because to compute new dp at value v = A[i], we need best length among values < v (strictly increasing), i.e., query(v_idx-1) + 1. Then we update at v_idx with this length (if larger).
6. Sweep i = 1..N:
   - let v = compressed index of A[i].
   - best = bit.query(v-1) (if v>1 else 0).
   - bit.update(v, best+1).
   - While next query has R == i, answer it: ans = bit.query(x_idx) (where x_idx is compressed index of X_i), record.
7. Output answers in original order.

This works because the BIT always stores, for each value, the length of the longest increasing subsequence ending with that value (considering only values ≤ that exact value). When we process elements in order, the standard O(N log N) LIS algorithm using BIT (or segment tree) yields correct DP. For queries we just take the max over all values ≤ X, which is exactly the answer for bound X.

Edge cases: multiple equal values: strictly increasing requires later values > previous, so we must query strictly smaller values (v-1). For X bound we want ≤ X, so query up to index of X (including equal). Since we only ever store at positions corresponding to A[i] values, and we use compression that includes both A values and X values, we need to ensure that for query we consider all A values ≤ X. If X equals a value that is not an A value, the compressed index will be the same as the next larger A value; we query up to that index, which is correct because there is no A value between X and the next larger A value.

Time complexity: O((N+Q) log (N+Q)). Memory: O(N+Q).

Let's verify with sample:
A = [2,4,1,3,3]
Vals: 1,2,3,4 plus Xs 5,2,3 → after dedup 1,2,3,4,5. Indices: 1->1,2->2,3->3,4->4,5->5.
Sweep:
i=1, A=2, v=2, best=query(1)=0, update(2,1) → BIT[2]=1
i=2, A=4, v=4, best=query(3)=1, update(4,2) → BIT[4]=2
i=3, A=1, v=1, best=query(0)=0, update(1,1) → BIT[1]=1
i=4, A=3, v=3, best=query(2)=max(BIT[1],BIT[2])=1, update(3,2) → BIT[3]=2
i=5, A=3, v=3, best=query(2)=1, update(3, max(2,2)=2) stays.
Queries:
(2,5): after i=2, R=2, X=5 idx=5, query(5)=max over 1..5 = BIT[4]=2 → answer 2.
(5,2): after i=5, X=2 idx=2, query(2)=max(BIT[1],BIT[2])=1 → answer 1.
(5,3): X=3 idx=3, query(3)=max(BIT[1..3])=2 → answer 2. Matches.

Great.

Implementation details:
- Use list of queries with fields: R, X, idx, x_idx.
- Sort queries by R.
- Use a while pointer to process queries when their R is reached.
- BIT class: 1‑based, size m. `update` and `query` in O(log m).
- `query(pos)` should clamp to m if pos > m (but X ≤ max value so x_idx ≤ m).
- Ensure best+1 can be at most current BIT value? We do max update, so fine.

Edge Cases:
- R_i could be 0? No, R_i ≥ 1.
- If all A_i > X, but constraints guarantee min A[1..R] ≤ X, so at least one element qualifies, so answer ≥ 1? Actually not necessarily strictly increasing: single element is a valid strictly increasing subsequence, so answer at least 1. Our BIT will reflect that because update will put length 1 at some index ≤ X, and query up to X will return ≥1. Good.
- For R = 1, works.

Large constraints: N, Q up to 2e5, log 2e5 ~ 18, fine.

Thus the solution is offline sweep with BIT.

Let's write the final solution.