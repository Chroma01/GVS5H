We need to count subarrays of `[1…n]` that avoid every remaining conflicting pair after deleting exactly one pair.  
For each index `i` (treated as the right end of a subarray) the only restriction comes from pairs whose larger endpoint is `i`; the subarray must start after the smallest possible start that is still valid, i.e. after the **largest left endpoint** among all those pairs.  
Thus for each `i` we maintain the two largest left endpoints `max1[i]` and `max2[i]`.  
- Base valid subarrays (no deletion) = ` Σ (i - max1[i]) ` over all `i`.  
- Deleting a pair can only improve the count for the index equal to the larger endpoint of that pair.  
  If that pair contributed `max1[i]`, the new effective max becomes `max2[i]`, giving a gain of `max1[i] - max2[i]`.  
- The best deletion yields the maximum gain across all `i`.  

The algorithm therefore:
1. Scan all pairs, keep the two largest left endpoints for each right endpoint.  
2. Compute the base sum and the per‑index gain, track the maximum gain.  
3. Return `base + max_gain`.  

All operations are linear in `n` and the number of pairs, fitting the `n ≤ 10⁵` limits.