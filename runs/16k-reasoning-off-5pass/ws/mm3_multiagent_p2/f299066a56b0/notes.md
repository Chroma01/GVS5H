
## ideation
The problem asks for the maximum number of disjoint pairs (i, j) with i < j such that A_i ≤ A_j / 2. The array is already sorted in non-decreasing order.

**Core difficulty:** We need to maximize the number of valid pairs without reusing any mochi. This is a classic matching problem on a sorted array.

**Candidate approaches:**
1. **Greedy two-pointer:** Use the smallest unused mochi as the "top" and the largest unused mochi as the "bottom". If the top fits on the bottom (A[l] ≤ A[r] / 2), pair them and move both pointers inward. Otherwise, the top is too large for this bottom, so discard the bottom (move r left). This is optimal because pairing the smallest top with the largest available bottom leaves the most room for future pairings.
2. **DP / binary search:** For each mochi as the bottom, find the smallest valid top using binary search. Then use DP or greedy matching. This is O(N log N) but the two-pointer approach is simpler and O(N).
3. **Brute force:** O(N²) — too slow for N up to 5×10⁵.

**Pitfalls:**
- The condition is A_i ≤ A_j / 2, which is equivalent to 2*A_i ≤ A_j. Use integer comparison to avoid floating-point issues.
- Since the array is sorted, the two-pointer approach works correctly: the left pointer (smallest available) and right pointer (largest available) guarantee optimality.
- Edge case: when no pair satisfies the condition, answer is 0.

**Proof of greedy optimality:** If the smallest available top fits on the largest available bottom, pairing them is optimal because any other pairing would use a smaller bottom, which is harder to pair with later tops. If the smallest top doesn't fit on the largest bottom, then no top can fit on this bottom (since all tops are ≥ the smallest), so this bottom must be discarded.

## worker: finalize
The two-pointer greedy works as follows:
- The array is sorted in non-decreasing order, so we can pick the smallest available mochi as the "top" (left pointer) and the largest available mochi as the "bottom" (right pointer).
- If `2 * a[l] <= a[r]`, the top fits on the bottom. We form a pair, increment the answer, and move both pointers inward.
- Otherwise, the current bottom is too small for the smallest top. Since any other top is at least as large, this bottom can never be used, so we discard it by moving the right pointer left.
- This greedy strategy is optimal: pairing the smallest top with the largest possible bottom leaves the most flexibility for the remaining mochi, maximizing the total number of pairs.
- Complexity: O(N) time, O(1) extra space (besides the input array).
- The condition `2 * a[l] <= a[r]` is equivalent to `a[l] <= a[r] / 2` and avoids floating-point issues. Since `a_i ≤ 10^9`, `2 * a[i]` fits in 32-bit signed integer, but Python handles big integers natively anyway.
