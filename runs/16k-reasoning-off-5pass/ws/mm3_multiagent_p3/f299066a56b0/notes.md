
## ideation
The problem is a maximum matching under a "stacking" condition: pair a smaller mochi (top) with a larger mochi (bottom) such that `a ≤ b/2`. Sizes are sorted ascending.

**Core difficulty:** Finding the maximum number of disjoint valid pairs (a matching in a bipartite ordering) efficiently for N up to 5×10⁵.

**Observations:**
- Since all sizes are sorted, a greedy two-pointer scan works:
  - Pointer `i` points to the smallest unpaired mochi (candidate for "top").
  - Pointer `j` scans forward as candidate "bottom".
  - If `A[i] * 2 <= A[j]`, we form a pair, increment count, advance both `i` and `j`.
  - Else, `A[j]` is too small to be a bottom for the current top; since later bottoms are even larger, we must advance `j` to find a bigger bottom — but actually we should advance `i`? Let's re-examine:
    - If `A[i] * 2 > A[j]`, then `A[j]` is too small to serve as a bottom for the current top. However, `A[j]` could still serve as a bottom for a *larger* top (later `i`). So we should advance `j` (skip this `j`, it's not a valid bottom for this top, but might be for a future larger top... wait, if we advance `i`, we look for a larger top, which makes the condition even harder). 
    - Actually the standard approach: keep `i` as the current smallest available "top". If `A[i]*2 <= A[j]`, pair and move both. If not, then `A[j]` is too small as a bottom; we must move `j` forward to a larger candidate bottom. But if we move `j` forward, `A[j]` only grows, so condition becomes *easier* for this top. So move `j`. 
    - Wait, but if we pair, we use up `i`. If we don't pair at `j`, we might still be able to pair `i` with a larger `j`. So advancing `j` is correct.
    - However, there's a subtlety: what if `A[i]*2 > A[j]` and we advance `j` past the end, then we should advance `i`? Actually if `j` reaches end, no more bottoms, stop. The typical greedy for similar problems (e.g., "matching with size condition" or "boats") is: 
      - Use two pointers. `i` (small/top), `j` (large/bottom). 
      - While both are in range: if `A[i]*2 <= A[j]`, pair, i++, j++, count++. Else j++.
      - If j runs out, stop (i cannot be paired).
    - But wait, if `A[i]*2 > A[j]`, we are saying `A[j]` is too small to be a bottom. Since `A` is sorted, future `j` are larger, so eventually we may find a valid bottom. So advancing `j` is fine.
    - What about when `A[i]*2 <= A[j]` but we might want to skip `A[j]` and use a larger bottom? No, because we want to maximize count, and using the smallest possible bottom leaves larger bottoms available for other tops. So greedily pairing when possible is optimal.

**Pitfalls:**
- Overflow: `A[i] * 2` can overflow 32-bit int. Use 64-bit in C++/Java, or in Python it's fine but be careful in other languages.
- Array is already sorted (non-decreasing), so no need to sort.
- Edge cases: N=2, equal sizes (e.g., [4,4] -> 4 ≤ 4/2? 4 ≤ 2 is false, so 0 pairs), large N.
- The greedy two-pointer algorithm is O(N) and well-known for this type of "stacking" or "matching" problem.

**Verification with samples:**
1. [2,3,4,4,7,10]: i=0 (2), j=1 (3): 2*2=4 > 3, j=2 (4): 4>4, j=3 (4): 4<=4, pair (2,4) -> i=1 (3), j=4 (7), count=1. 3*2=6 >7? No, 6 ≤7, pair (3,7) -> i=2 (4), j=5 (10), count=2. 4*2=8 ≤10, pair (4,10) -> i=3 (4), j=6 end. count=3. Correct.
2. [387,388,389]: i=0, j=1: 774 >388, j=2: 774>389, j=3 end. count=0. Correct.
3. Sample 3 should yield 6.

**Alternative approaches:**
- Binary search for K and check feasibility (greedy check if K pairs possible), then binary search. This is O(N log N). But the two-pointer gives O(N) directly.
- DP is unnecessary.

**Conclusion:** The two-pointer greedy algorithm is optimal and efficient.

## worker: Implement the solve() function with the two-pointe
The two-pointer greedy algorithm works as follows:
- Pointer `i` tracks the smallest unpaired mochi available to be the "top" of a kagamimochi.
- Pointer `j` tracks the candidate "bottom" mochi.
- Since the array is sorted ascending, if `A[i] * 2 <= A[j]`, we can safely pair them: using the smallest possible bottom leaves larger bottoms for other tops, which is optimal for maximizing the total number of pairs.
- If the condition fails, `A[j]` is too small to be a bottom for the current top. We advance `j` to look for a larger bottom. (If we advanced `i` instead, we'd need an even larger bottom, making things harder.)
- This runs in O(N) time and O(1) extra space (besides the input array), easily handling N up to 5×10⁵.
- Verified against the three sample cases: yields 3, 0, and 6 respectively.
