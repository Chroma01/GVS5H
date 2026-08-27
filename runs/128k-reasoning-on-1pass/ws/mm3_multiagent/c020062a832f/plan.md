The inversion count for each shift `k` can be obtained iteratively from the count for `k-1`.  
When we increase `k` by one, every element whose current value is `M‑1` (i.e. those with original value `v = (M‑k) mod M`) wraps to `0`; all other elements simply increase by one.  
Only pairs consisting of one wrapping element and one non‑wrapping element change their contribution to the inversion number, and the total change can be expressed using only the number of such elements and the sum of their positions:

```
delta(k) = 2 * sumPos[v] - cnt[v] * (N + 1)
```

where `cnt[v]` is how many times the value `v` occurs in `A`, and `sumPos[v]` is the sum of 1‑based indices of those occurrences.  
We compute the initial inversion number `inv0` with a Fenwick tree, then apply the formula for `k = 1 … M‑1` to obtain all answers in `O(N log M + M)` time and `O(N + M)` memory.