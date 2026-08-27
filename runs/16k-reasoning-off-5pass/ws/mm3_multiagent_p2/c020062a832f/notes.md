
## ideation
We need to compute the inversion count of `B(k)` where `B_i(k) = (A_i + k) mod M` for each `k = 0, 1, ..., M-1`. N, M ≤ 2×10⁵.

**Core difficulty**: Naively recomputing inversions for each k is too slow (O(NM log M) or O(NM)). We need to leverage the relationship between consecutive k values.

**Key insight**: When k increases by 1, the transformation `(A_i + k) mod M` is equivalent to taking the current array and adding 1 modulo M. Only elements with value M-1 "wrap" to 0; all others simply increment. This allows us to express the change in inversion count as a function of the positions of the wrapping elements.

**Change formula derivation**:
At step k, let S be the set of positions where `B_i(k) = M-1`. When moving to k+1:
- Each pair (i,j) with i<j, i∈S, j∉S: was an inversion, becomes not → **loss**
- Each pair (i,j) with i<j, i∉S, j∈S: was not an inversion, becomes one → **gain**

Let c = |S|, prefix_S[i] = number of S-elements in positions 1..i. Then:
```
change = sum_{i in S} [2i - N - 2 + c - 2*prefix_S[i-1]]
```

**Crucial observation**: At step k, the set S consists of positions where `A_i = (M-1-k) mod M`. So the change depends only on the original value v = (M-1-k) mod M. We can precompute `change[v]` for every value v in O(N) total.

## worker: Implement BIT (Fenwick tree) to compute the initia
The solution computes the initial inversion count `inv(0)` using a Fenwick tree (BIT) in O(N log M). Then, for each value `v` in `[0, M-1]`, it precomputes the change in inversion count when that value is the one wrapping from M-1 to 0. The change formula `change[v] = sum_{p in pos_v} (2p - N - 2 + c - 2*prefix)` is derived by tracking how many inversions are gained/lost when elements with value v wrap around. Finally, we iterate k=1 to M-1, using `v = (M-k) mod M` to look up the precomputed change and update the running answer. Total complexity is O(N log M + M), which fits the constraints.
