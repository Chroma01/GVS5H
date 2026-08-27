
## ideation
The problem requires computing the sum of (minimum + maximum) over all subarrays whose length is at most `k`. With `n` up to 80,000, any `O(n·k)` or `O(n²)` brute-force enumeration of subarrays is infeasible.

**Core difficulty:**
1.  **Efficient aggregation:** We need to avoid touching every subarray explicitly. The standard trick for "sum of subarray minimums/maximums" (LeetCode 907 style) is to use a *contribution method*: for each index `i`, count how many valid subarrays have `nums[i]` as the minimum (and similarly for the maximum), then multiply by `nums[i]`.
2.  **Length constraint (`≤ k`):** This turns the counting problem from "all subarrays" into "subarrays with `a + b ≤ k-1`", where `a` and `b` are the left/right extensions from `i`. This requires an `O(1)` combinatorial formula per element, or the whole approach collapses back to `O(n·k)`.
3.  **Monotonic stack boundaries:** Finding the range where `i` is the (leftmost/rightmost) minimum requires careful handling of duplicates—using `strictly less` on one side and `less-or-equal` on the other to partition subarrays without double-counting or dropping them.
4.  **Symmetry:** The maximum case is identical to the minimum case with reversed comparisons, so we can reuse the same counting logic.

**Candidate approaches:**
-   **Contribution + monotonic stack (O(n)):** The PLAN's approach. For each `i`, compute `prev_less[i]`, `next_le[i]`, `prev_greater[i]`, `next_ge[i]` via four monotone-stack passes. Then count valid subarrays using the closed-form pair-counting function.
-   **Contribution + segment tree / BIT (O(n log n)):** Less efficient and unnecessary.
-   **Divide & conquer:** Possible but much more complex for this variant.
-   **Brute force / sliding window with multisets:** Too slow (`O(n·k)` worst case).

**Pitfalls observed in the provided PLAN:**
-   **Bug in `prev_less` computation:** The code uses `while st and nums[st[-1]] > nums[i]: st.pop()`. This pops only strictly greater elements, leaving equal elements in the stack. As a result, it computes *previous less-or-equal* (`prev_le`), not *previous strictly less* (`prev_less`). The correct condition for `prev_less` should be `>= nums[i]`. With the current code, subarrays containing duplicate minimums (e.g., `[1,1]`) will be **missed** entirely from the count.
-   **`count_pairs` correctness:** The formula for `A' = min(A, K+1)` and the case split (`B ≥ K+1` vs. `B < K+1`) appears algebraically correct, but must be tested with edge cases (e.g., `B=1`, `A` very small, `K=0`).
-   **Edge case `k=1`:** Only single-element subarrays exist. Each `nums[i]` should be counted twice (once as min, once as max), giving `2 * sum(nums)`. The formula must reduce correctly.
-   **Edge case all-equal array:** Tests that duplicates are partitioned exactly once per subarray.
-   **Off-by-one in `next` boundaries:** `next_le[i]` should be the first index to the right with value `≤ nums[i]` (or `n` if none), and `next_ge[i]` the first with value `≥ nums[i]`. The PLAN's right-to-left passes look correct here.
-   **Integer size:** Python handles big ints, but the sum can be as large as `~10⁶ · 8·10⁴ · 8·10⁴ ≈ 6·10¹⁴`, well within Python's range.
-   **Sign of `nums[i]`:** Negative values reduce the sum when duplicated; the linear `Σ` still works.

## worker: Write the Python implementation of `Solution.minMa
- The problem asks for the sum of `min + max` over all subarrays whose length is at most `k`.  
- We use the standard contribution technique: for each index `i` we count how many subarrays of length ≤ k have `nums[i]` as the (leftmost) minimum and similarly for the maximum, then multiply by `nums[i]` and add to the answer.  
- The boundaries for the minimum are obtained with two monotone‑stack passes:
  * `prev_less[i]` – index of the closest element left of `i` with value **<** `nums[i]` (‑1 if none).  
  * `next_le[i]` – index of the closest element right of `i` with value **≤** `nums[i]` (`n` if none).  
  The asymmetric handling (`<` on the left, `≤` on the right) ensures each subarray is assigned exactly once (to the rightmost occurrence of its minimum).  
- The maximum case is symmetric: use `prev_greater` (strictly greater) and `next_ge` (greater‑or‑equal).  
- With those borders we have for a fixed `i`:
  * `A = i - prev_less[i]` possible left extensions (`a` from `0` to `A‑1`),
  * `B = next_le[i] - i` possible right extensions (`b` from `0` to `B‑1`),
  * a subarray length is `a+b+1`. The constraint `a+b ≤ k‑1` (let `K = k‑1`) gives a counting problem for pairs `(a,b)`.  
- The counting of valid pairs is done in **O(1)** by a closed‑form formula that splits into two cases (`B ≥ K+1` and `B < K+1`).  
- A bug in the original plan was using `>` instead of `>=` when computing `prev_less`; the correct condition is `while st and nums[st[-1]] >= nums[i]: st.pop()`. The code above contains the fix.  
- Overall complexity: **O(n)** time (four linear stack passes and a final linear scan) and **O(n)** extra memory. This easily satisfies the limits (`n ≤ 80 000`).
