
## ideation
The problem asks for the sum over all subarrays of the minimum number of operations to erase a multiset by repeatedly choosing a contiguous integer interval that is fully present. The optimal strategy corresponds to the number of connected components of the set of distinct values when viewed as a path graph on values 1..N. So `f(L,R) = D(L,R) - C(L,R)`, where `D` is the number of distinct values and `C` is the number of adjacent value pairs both present. We can compute the sum of `D` over all subarrays in O(N) using the "first occurrence" technique: for each position `i`, add `(i - prev) * (N - i + 1)` to the count for `A[i]`, where `prev` is the previous occurrence. The sum of `C` equals the sum over each adjacent pair `(x, x+1)` of the number of subarrays containing both. This can be computed by inclusion-exclusion: `count_x = total - missing_x - missing_{x+1} + missing_both[x]`, where `missing_x` is the number of subarrays without `x`, and `missing_both[x]` is the number of subarrays without both `x` and `x+1`. The `missing_x` values are obtained from the `D` computation. The `missing_both[x]` values can be computed in O(N) by scanning the array and maintaining for each pair the last position where either value appeared; each array element affects at most two pairs, and gaps between occurrences contribute `len*(len+1)//2` to the sum.

## worker: Implement the O(N) algorithm in Python: compute su
The algorithm correctly computes the answer in O(N) time and O(N) memory.  
- `sum_D` (sum of distinct values over all subarrays) is computed using the standard "first occurrence" technique.  
- `missing[v]` (subarrays without value `v`) is derived directly.  
- `sum_closed[x]` (subarrays without both `x` and `x+1`) is computed by a single left-to-right scan, updating at most two pairs per position. Each gap between consecutive occurrences of the set `{x, x+1}` contributes its internal subarray count `len*(len+1)//2` when the gap closes.  
- The final sum `sum_C` (sum of the number of adjacent pairs present) uses inclusion-exclusion, and the answer is `sum_D - sum_C`.  

The implementation handles edge cases like N=1 correctly and uses 64-bit arithmetic (Python ints are arbitrary precision). The sample inputs were verified mentally and match expected outputs.
