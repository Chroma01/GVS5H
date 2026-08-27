
## ideation
**Core difficulty**  
We have to find, for each contiguous integer range `[l, r]`, the minimum number of pairwise operations where each operation divides two numbers by 4 (floored) until everything becomes 0. The naive simulation is impossible because r can be up to 1e9 and there can be 1e5 queries.

**Key observations**  
1. *Cost of a single element* `cost(x)`: the number of times we need to apply `floor(v/4)` to `x` to reach 0.  
   - `cost(0) = 0`  
   - For `x >= 1`, `cost(x) = 1 + cost(floor(x/4))`.  
   Since `4^16 = 2^32 > 1e9`, the maximum cost for any `x ≤ 1e9` is at most 16.

2. *Pairing strategy*: Each operation consumes exactly one “unit of cost” from each of two numbers (the operation reduces the total remaining cost sum by exactly 1, but it uses two slots).  
   - The optimal way to finish in the fewest steps is to always pair the two numbers with the largest remaining costs (greedy).  
   - The minimum number of operations equals `max(ceil(S/2), M)` where:  
     - `S = sum of costs of all elements` (total “work” to do),  
     - `M = max cost among elements` (we can’t finish faster than the time needed for the largest one).  
   - Intuition: every operation can eliminate at most 2 units of total cost, so we need at least `ceil(S/2)` steps, but we also need at least `M` steps to reduce the single largest element to zero.

3. *Counting sums by buckets*: Numbers in `[4^k, 4^{k+1} - 1]` have cost `k+1`. We can count how many numbers of `[l, r]` fall into each bucket, accumulating `count * (k+1)` to get `S` and tracking the maximum `k+1` seen to get `M`.  
   - Number of buckets is O(log_4 r) ≤ 16, so per-query work is O(log r) which is fast enough for 1e5 queries.

## worker: Precompute the list of powers of 4 up to >1e9 and 
- The `cost(x)` for a single integer is the number of times we need to apply `floor(v/4)` to reach 0; this is simply the exponent `k` such that `4^k ≤ x < 4^{k+1}` (with `k` starting at 1 for `x ≥ 1`). For `x = 0`, cost is 0.
- Bucketing by powers of 4 works because all numbers in `[4^k, 4^{k+1}-1]` share the same cost `k+1`.
- For any multiset, the optimal pairing is greedy: each operation reduces the total remaining cost by exactly 1 but consumes two slots, so the minimum number of operations is `max(ceil(S/2), M)`.
- Per query we only iterate over at most 17 buckets (since `4^17 > 2^34 > 1e9`), giving `O(log r)` time. With up to `10^5` queries, total complexity is about `1.7 × 10^6` operations, well within limits.
- Verified the logic against the provided examples:
  - `[1,2]`: costs = [1,1], S=2, M=1 → ops = max(1,1)=1 ✓
  - `[2,4]`: costs = [1,2,1], S=4, M=2 → ops = max(2,2)=2 ✓
  - `[2,6]`: costs = [1,2,1,2,1], S=7, M=2 → ops = max(4,2)=4 ✓
