
## ideation
We need to count, for each removal of one conflicting pair, the number of subarrays of `[1..n]` that avoid containing both endpoints of any remaining pair.  
Key reformulation:  
- A subarray `[l, r]` is **valid** iff for every pair `(x, y)` (with `x < y`), it is not the case that both `x, y ∈ [l, r]`.  
- For a fixed right endpoint `i`, the leftmost possible start `l` is determined by the “most restrictive” pair whose larger endpoint is exactly `i`. Specifically, among all pairs with larger endpoint `i`, let `min_left(i)` be the maximum of the smaller endpoint. Then any subarray ending at `i` must start after `min_left(i)`, i.e., `l > min_left(i)`. So the number of valid subarrays ending at `i` is `i - min_left(i)`.  
- Total valid subarrays = `Σ_{i=1}^{n} (i - min_left(i))`.

**Effect of removing a pair:**  
A pair `(a, b)` with `a < b` only affects position `b` (the larger endpoint). If we remove it, the new `min_left(b)` becomes the second largest smaller-endpoint among pairs ending at `b` (or 0 if none).  
Thus the gain in total subarrays when removing pair `(a, b)` is:
- `max1[b] - max2[b]` if `a` was the current maximum (largest) smaller-endpoint at `b`.
- `0` otherwise.

We precompute for each `i` the sorted list of smaller endpoints of pairs whose larger endpoint is `i`. Let `max1[i]` be the largest, `max2[i]` the second largest distinct value.  
Base total = `Σ (i - max1[i])`.  
For each pair, compute its gain and take the maximum. The answer is `base + max_gain`.

**Pitfalls:**
- Ensure `max2` is the next *distinct* value, not just the second element in a multiset.
- If a pair has `a > b`, we must swap to ensure the smaller endpoint is stored under the larger index.
- If after removal there are no remaining candidates, the new bound is 0, so `max2` is effectively 0.
- Complexity: `O(n + m log m)` with `m ≤ 2n`, fine for `n ≤ 10^5`.

## worker: Implement the solution in Python: preprocess pairs
- The algorithm treats each conflicting pair `(a, b)` (with `a < b`) as imposing a restriction on subarrays ending at `b`: the left bound must be greater than `a`. For a fixed `b`, the most restrictive bound is the maximum over all such `a`'s, which we denote `max1[b]`. The number of valid subarrays ending at `b` is `b - max1[b]`.
- The total base count is the sum over all positions.
- Removing a pair only affects its own larger endpoint. If that pair was the one giving the current maximum (`max1`), the bound drops to the second maximum (`max2`), increasing the count by `max1 - max2`. If the pair was not the maximum, the count is unchanged.
- `max2` is computed as the first strictly smaller value in the sorted list, which correctly handles duplicate smaller endpoints (e.g., multiple pairs `(3, 5)`).
- Complexity: building candidates and sorting per index is `O(m log m)` in total, where `m` is the number of pairs (`m ≤ 2n`). All other loops are `O(n + m)`. This fits the constraints.
