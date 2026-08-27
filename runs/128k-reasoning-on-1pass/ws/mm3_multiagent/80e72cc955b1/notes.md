
## ideation
**Core difficulty**  
- The operation reduces two numbers by `floor(x/4)` each time.  
- For a number `x>0` the number of times it must be selected to become `0` is the number of times we can divide by `4` until the result is `0`, i.e. `f(x) = ⌊log₄(x)⌋ + 1`.  
- The total “work” needed for an array is `S = Σ f(x)`. Since each operation reduces the work of two numbers, the minimum number of operations is `⌈S/2⌉`. The pairing is always possible (when `S` is odd we can pair the last reduction with a zero).  
- The main challenge is computing `S(l,r) = Σ_{x=l}^{r} f(x)` for up to `10⁵` queries with `l,r ≤ 10⁹` efficiently.

## worker: Precompute the list of powers of 4 (up to where th
- **Key observation** – For a positive integer `x`, the number of times it must be processed (i.e. selected) to become `0` equals `f(x) = ⌊log₄(x)⌋ + 1`.  
- **Total work** – The array `[l, r]` needs `S = Σ f(x)` total “steps”.  
- **Optimal operations** – Each operation can reduce the step count of two numbers, so the minimum number of operations for a query is `ceil(S/2) = (S+1)//2`.  
- **Efficient summation** – `f(x)` is constant on intervals `[4^{k-1}, 4^{k}−1]` (value `k`). Since `4¹⁵ > 10⁹`, at most 15 intervals exist. For each query we iterate over these intervals, count how many numbers of the query fall into each, and multiply by `k`. This yields `O(log₄(max_val))` ≈ 15 operations per query, easily handling `10⁵` queries.  

The implementation pre‑computes the powers of 4 (`pow4` list) and uses a helper `total_f(l, r)` to compute the sum of `f(x)` over any interval in constant time (independent of interval length). The final answer sums the per‑query results.
