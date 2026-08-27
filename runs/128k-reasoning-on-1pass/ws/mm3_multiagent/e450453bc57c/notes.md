
## ideation
**Core difficulty**  
- For any fixed window of size `x` the cheapest way to make all its elements equal is to change them to a median. The cost of a window is the sum of absolute deviations to that median.  
- The whole problem therefore reduces to:  
  1. Compute the minimal cost `cost[i]` for every length‑`x` window starting at position `i`.  
  2. Choose `k` non‑overlapping windows whose total cost is minimum.  

**Computing `cost[i]` (sliding‑window median)**  
- A median of a multiset can be found with a data structure that supports insertion, deletion and order‑statistics in `O(log n)`.  
- Two standard options:  
  * **Two heaps** (max‑heap for the left part, min‑heap for the right part) with lazy deletions and extra sums for each heap.  
  * **Fenwick tree (BIT)** after coordinate‑compressing the values. We keep two BITs: one for frequencies, one for the sum of values. The median is the element whose prefix count reaches rank `r = (x+1)//2`. With a BIT we can obtain the index of the `r`‑th element by binary lifting (`find_kth`).  
- While sliding the window we maintain the current sum `S` of its elements, update the BITs (add the new element, remove the leaving element) and after each full window we compute  
  ```
  freq_left = BIT_cnt.prefix_sum(median_idx)   # count of elements ≤ median
  sum_left  = BIT_sum.prefix_sum(median_idx)   # sum of elements ≤ median
  cost = median*freq_left - sum_left + (S - sum_left) - median*(x - freq_left)
  ```
  which is the standard formula for `Σ|a_i – median|`.  
- The sliding process is `O(n log M)` where `M ≤ n` (the number of distinct values), well within the limits (`n ≤ 10⁵`).  

**Choosing `k` non‑overlapping windows (DP)**  
- Let `m = n - x + 1` be the number of possible start positions.  
- Define `dp[t][i]` = minimum total cost to place `t` windows inside the prefix of length `i` (first `i` elements).  
- Recurrence:  
  ```
  dp[t][i] = min( dp[t][i-1] ,                # skip position i-1
                 cost[i-x] + dp[t-1][i-x] )   # place a window ending at i-1
  ```
  (the second term is valid only when `i ≥ x` and `i-x < m`).  
- Only the previous row is needed, so we keep two 1‑D arrays of size `n+1`.  
- Complexity: `O(k·n)` time, `O(n)` memory (`k ≤ 15`, `n ≤ 10⁵` → ~1.5 M operations).  

**Pitfalls & details to watch**  
- **Median tie‑breaking**: for even `x` any value between the two middle elements is optimal. Using the lower median (`(x+1)//2`‑th smallest) works; all occurrences of that value are counted as “≤ median” in the left part.  
- **Duplicates of the median**: the BIT query for `freq_left` includes all elements equal to the median, which yields the correct cost.  
- **Negative numbers**: the cost formula works unchanged.  
- **Indexing**: DP uses 1‑based prefix length; the start index of a window covering positions `[i-x, i-1]` is `i-x`. The cost array is 0‑based, so `cost[i-x]` is used.  
- **Bounds**: `m = n-x+1`. When `i` runs up to `n`, `i-x ≤ m-1`, so the start is always valid. Guarding against out‑of‑range is optional.  
- **INF**: use a value larger than any possible answer, e.g. `10**18`.  
- **BIT implementation**: need a `find_kth` routine (binary lifting) for order statistics; both BITs must support `add` and `prefix_sum`.  
- **Complexity fits** because `n·log n` (`≈ 1.7 M` operations) plus `k·n` (`≈ 1.5 M`) is easily under the time limit.  

**Alternative approaches**  
- Heaps method is also `O(n log n)` and may be simpler for some, but the BIT method gives a clean formula for the L1 distance to the median.  
- A segment tree storing a sorted multiset and a sum could also work, but BIT is lighter.  
- The DP part can be optimized with a monotone queue for the `k`‑window selection, but not necessary for the given constraints.

## worker: Implement a `BIT` (Fenwick tree) class with `add`,
- The `BIT` class provides the required `add`, `prefix_sum`, and `find_kth` operations.  
  `find_kth` works in `O(log n)` using binary lifting on the internal tree array.
- The solution first compresses the array values, then maintains two Fenwick trees while sliding a window of length `x`.  
  One tree stores frequencies, the other stores the sum of original values, enabling an `O(log n)` median query and the `Σ|a_i – median|` cost computation.
- After obtaining `cost[i]` for every possible start position, a simple DP (`O(k·n)`) selects `k` non‑overlapping windows with minimal total cost.  
  The DP only needs two rows, so memory stays `O(n)`.
- The algorithm runs in `O((n + m)·log n + k·n)` time (`≈ 2·10⁶` operations for the worst‑case limits) and uses `O(n)` additional memory.
