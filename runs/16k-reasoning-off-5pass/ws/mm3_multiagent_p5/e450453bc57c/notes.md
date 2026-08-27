
## ideation
The problem asks for the minimum number of ±1 operations to create at least **k non-overlapping subarrays of length exactly x** where each subarray consists of equal elements.

Key observations:
- For a fixed window of length `x`, the cost to make all its elements equal to some value `v` is `Σ |nums[i] - v|`. This is minimized when `v` is the **median** of the window.
- Therefore, for every possible window (start index `s`), we can precompute `cost[s] = Σ |nums[i] - median(window)|`.
- After computing costs, we need to choose **k non-overlapping windows** with minimum total cost. Since windows have a fixed length and must be disjoint, this becomes a classic DP on a line:
  - `dp[i][j]` = minimum operations to place `j` disjoint windows using the first `i` elements of the array.
  - Transition: either skip position `i`, or place a window ending at `i` (i.e., starting at `i - x + 1`) → `dp[i][j] = min(dp[i-1][j], dp[i-x][j-1] + cost[i-x+1])`.
- `n ≤ 10^5`, `k ≤ 15`, so `O(n*k)` DP is fine.
- The tricky part is computing all `n - x + 1` window costs efficiently. A sliding-window median with two heaps (max-heap for lower half, min-heap for upper half) plus lazy deletions using a hashmap gives `O(n log x)`.

Pitfalls:
- Indexing (0 vs 1 based) in DP.
- Handling the median when `x` is even (any value between the two middle values is optimal; picking either middle works).
- Heap balancing and lazy deletion correctness.
- Edge case: after placing a window, the next window must start at least `x` positions later (handled by the `i - x` transition).

## worker: Implement a `SlidingMedian` class with two heaps a
**What I did:**

1. **`SlidingMedian` class** – maintains the median of a sliding window using two heaps (a max-heap `low` for the lower half and a min-heap `high` for the upper half).  
   - Lazy deletion is implemented via a `defaultdict(int)` `delayed` that marks elements for removal. The `_prune` helper cleans the heap top whenever a stale element is encountered.  
   - Sums of each half (`low_sum`, `high_sum`) and their sizes are tracked so the total cost `Σ |a_i - median|` can be computed in **O(1)** once the median is known:  
     `cost = median * low_size - low_sum + high_sum - median * high_size`.  
   - All heap operations are O(log x), and pruning amortizes to O(1) per element, giving **O(n log x)** total.

2. **`get_costs(nums, x)`** – fills the first window of size `x`, records the cost, then slides one element at a time, updating the data structure and appending the cost for each new start index. This returns a list `cost` where `cost[s]` is the minimum number of ±1 operations to make `nums[s : s+x]` all equal (the optimal target is the window's median).

3. **DP phase** – a classic 1-D DP over the array index:
   - `dp[i][j]` = minimum operations to cover the first `i` elements with exactly `j` non-overlapping windows.
   - Transition: either skip element `i` (carry forward `dp[i-1][j]`) or place a window ending at `i` (start at `i-x`) → `dp[i-x][j-1] + cost[i-x]`.
   - Complexity **O(n·k)**, which is fine because `k ≤ 15` and `n ≤ 10^5`.

**Correctness highlights:**

- For a fixed window, the value minimizing Σ|a_i − v| is the median; using the median guarantees the minimal operation count.
- Windows are forced to be disjoint because placing a window ending at `i` consumes the preceding `x` positions (transition from `i-x`).
- The DP explores all valid placements of `k` windows and selects the cheapest combination.
- Lazy deletion correctly handles elements leaving the window; the balance operation guarantees the median is always the top of the appropriate heap.

**Complexities:**

- Precomputation: **O(n log x)** time, **O(x)** space.
- DP: **O(n·k)** time, **O(n·k)** space (could be reduced to **O(k)** with rolling arrays, but `n·k ≤ 1.5·10^6` is acceptable).

## worker: Test the implementation against the provided examp
- **Sliding Median with Lazy Deletion:** The `SlidingMedian` class maintains the median of a moving window in O(log x) per update. It uses a max‑heap `low` (negated) for the lower half, a min‑heap `high` for the upper half, and a `delayed` map for amortized O(1) clean‑up of removed elements.
- **Cost Computation:** For a window, the minimum number of ±1 operations to make all elements equal is achieved by the median. The cost formula  
  `cost = median * low_size - low_sum + high_sum - median * high_size`  
  gives this in O(1) after the median is known.
- **DP for k Non‑Overlapping Windows:**  
  `dp[i][j]` = min cost using first `i` elements with `j` windows.  
  Transition: skip position `i` or place a window ending at `i` (start = `i‑x`) → `dp[i‑x][j‑1] + cost[start]`.  
  Implemented with rolling arrays to use O(k) space.
- **Testing:** The provided examples both pass (outputs 8 and 3). A brute‑force checker was run on 100 random small arrays (n ≤ 8) and matched the optimized solution in every case, confirming correctness.
