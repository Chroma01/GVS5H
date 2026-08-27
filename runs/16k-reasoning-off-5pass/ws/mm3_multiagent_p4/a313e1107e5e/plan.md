For each prefix of the array, we need to answer many queries: given a bound `R` and a value `X`, find the length of the longest strictly increasing subsequence (LIS) within `A[1..R]` using only elements ≤ `X`.

We will process queries offline sorted by `R`. While scanning the array from left to right, we maintain for every value `v` the best (largest) length of a strictly increasing subsequence that ends with value `v` using only the first `i` elements. This is the classic patience-sorting DP: for each `A[i]`, compute `dp = 1 + max_len among values < A[i]`, and store it. Since values can be up to 1e9, we compress them.

The key observation: after processing position `i`, the multiset `best[v]` (maximum length ending exactly with value `v`) is non‑decreasing in `v` (strictly increasing DP ensures monotonicity). Therefore, for a query `(R, X)`, the answer is the maximum `best[v]` over all `v ≤ X` in the prefix `R`. This is just a prefix maximum over the compressed values.

We will:
1. Coordinate‑compress all `A[i]` and all `X_i` from queries.
2. Sort queries by `R` and process the array element by element.
3. While processing, keep a Fenwick tree (or a simple array) over the compressed value axis storing the current `best[v]`. Each update for `A[i]` sets the position of `A[i]` to the new value (which is always ≥ the old one, so the array stays non‑decreasing).
4. For each query arriving at position `R`, query the Fenwick tree for the prefix max up to the compressed index of `X`. Because the array is non‑decreasing, the prefix max can also be obtained by keeping a running prefix maximum without a Fenwick, but using a Fenwick is simpler and O(log N).

Complexities: O((N+Q) log N).