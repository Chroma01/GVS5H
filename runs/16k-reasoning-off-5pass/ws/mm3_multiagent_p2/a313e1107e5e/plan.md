The problem asks, for each query (R, X), to find the length of the longest strictly increasing subsequence (LIS) of prefix A[1..R] where every element is ≤ X.

We can precompute, for each position i, the LIS of the whole prefix A[1..i] (standard patience sorting O(N log N)). Let `global[i]` be that length.

For a query (R, X), we need LIS where we only consider elements ≤ X, not necessarily the whole prefix LIS. Notice that the elements that can be used are exactly those indices j ≤ R with A[j] ≤ X. This is a subset of the prefix.

A standard trick: compress A values to 1..N (with coordinate compression). For each value v (in compressed space), maintain the LIS length sequence of elements equal to v. More precisely, we can precompute for each compressed value v, a list `pos[v]` containing the LIS length of the subsequence ending with value v, in order of occurrence.

Specifically, we traverse i = 1..N. When we see A[i] = v (compressed), we compute `dp[i] = 1 + max_{u < v} last_length[u]`, where `last_length[u]` is the maximum LIS length seen so far for values u. This is just the global LIS computation, and we also store `len_at_v[i] = dp[i]`.

Now, for a query (R, X), we need LIS among indices ≤ R with value ≤ X. Consider processing queries offline sorted by R ascending. Maintain a Fenwick tree (BIT) over value domain (1..M) that stores the best LIS length among processed positions (≤ current R) for each value. When we add position i (as we sweep R), we update BIT at index `v = comp(A[i])` with `dp[i]`. However, updates should keep the maximum for that value.

Then query answer is `max_{v ≤ Xc} BIT.query(Xc)`, where Xc is compressed value of X. This gives the LIS length using only values ≤ X, because any valid increasing subsequence must use values v_1 < v_2 < ... < v_k ≤ X, and the BIT maximum over v ≤ X picks the best length achievable with last value ≤ X.

Complexities:
- Coordinate compression O(N log N).
- dp[i] via BIT: O(N log N).
- Process Q queries sorted by R: for each i added, one BIT update; for each query, one BIT query. Total O((N+Q) log N).
- Each BIT operation is O(log N).

Edge cases:
- X is not present in A; compressed index of X must be computed carefully. We can map X to the index of the largest compressed value ≤ X. Use sorted unique values and bisect_right.
- BIT should support point max update (i.e., `tree[i] = max(tree[i], val)` for i and its ancestors).

Finally, output answers in original order.