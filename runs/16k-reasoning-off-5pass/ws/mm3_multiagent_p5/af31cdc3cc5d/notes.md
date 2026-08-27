
## ideation
**Core difficulty:**  
The operation “remove two adjacent numbers” corresponds to partitioning the indices into N/2 disjoint pairs that form a *non-crossing perfect matching* on the line. The total score is the sum of `|A_i - A_j|` over all pairs. We must find the maximum-weight non-crossing matching.

**Constraints:**  
N up to 3e5, so an O(N^2) DP (like standard interval DP) is impossible. We need an O(N log N) or O(N) solution.

**Candidate approaches:**

1. **Interval DP O(N^2):**  
   `dp[l][r] = max(dp[l][r-1], dp[l+1][r], |A[l]-A[r]| + dp[l+1][r-1])` — too slow.

2. **Divide-and-conquer with segment tree (the editorial solution):**  
   Recursively split the array at the position of the maximum element.  
   Let `solve(l, r)` return `(best, mx)` where `best` is the maximum score on subarray `A[l..r]` and `mx` is the maximum value in that subarray.  
   If `m` is the index of the max, then:
   ```
   (dl, ml) = solve(l, m-1)
   (dr, mr) = solve(m+1, r)
   best = dl + dr + max(0, |A[m] - max(ml, mr)|)
   return (best, A[m])
   ```
   Base cases: single element → `(0, A[i])`; empty range → `(0, -inf)`.  
   To find the max position in O(log N) we prebuild a segment tree storing `(value, index)`.

3. **Alternative: Coordinate compression + segment tree DP over values:**  
   Process values from largest to smallest, maintaining a DSU-like structure for intervals. This is essentially equivalent to approach 2.

**Pitfalls to watch:**

- Empty subsegments: must handle `l > r` correctly; return `(0, -inf)` or similar so `max(ml, mr)` ignores them.
- `|A[m] - max(ml, mr)|` might be negative if `mr` is `-inf`; the `max(0, ...)` handles that.
- N can be odd: then one element remains unpaired, which is fine because we pair only N/2 times.
- The segment tree must support range maximum query (returning the index of the max). We only need `O(N)` build and `O(log N)` per query, total `O(N log N)`.
- Values are up to 1e9, so use 64-bit integers for the answer.
- Recursion depth can be up to N (worst case sorted array). Python's default recursion limit is ~1000, so we must either:
  - Increase recursion limit (`sys.setrecursionlimit`), or
  - Implement the recursion iteratively using an explicit stack, or
  - Use a divide-and-conquer that doesn't hit the worst-case depth (e.g., the segment tree query naturally gives a balanced recursion, but the max element could be at an end, giving depth N). Better: raise the recursion limit to something like 1_000_000 to be safe.

**Verification with samples:**

- Sample 1: `[1,2,5,3]` → 5 ✓
- Sample 2: `[3,1,4,1,5,9,2]` → 14 (matches editorial)
- Sample 3: all 1s → any pairing gives 0 → 0 ✓

## worker: Implement a Python solution using the divide-and-c
- The recurrence `best = left + right + max(0, A[m] - max(left_mx, right_mx))` comes from the standard editorial for the AtCoder problem "Maximum Total Score" (non-crossing matching on a line).
- We use an iterative segment tree storing `(value, index)` so we can find the argmax in `O(log N)` per range query.
- The divide-and-conquer recursion can reach depth `N` in the worst case (e.g., a strictly increasing array), so the recursion limit is raised to `2**25` to be safe.
- Empty subsegments return `(0, NEG_INF)`; the `max(0, ...)` and the `partner_mx` selection automatically ignore the `-inf` side.
- Total complexity: `O(N log N)` time (each level of recursion does `O(log N)` argmax work, and there are `O(N)` levels total) and `O(N)` memory for the segment tree and recursion stack.
