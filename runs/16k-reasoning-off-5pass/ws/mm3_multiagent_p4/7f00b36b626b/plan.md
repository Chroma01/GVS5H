We need to count connected components where edges exist between numbers whose LCM ≤ threshold. Direct O(n²) edge checks are impossible for n up to 10⁵. Key insight: since threshold ≤ 2·10⁵, any valid LCM must be ≤ 2·10⁵, so only numbers ≤ threshold can possibly be in non-trivial components (numbers > threshold are isolated, as LCM with any other number ≥ that number > threshold). We can use Union-Find (DSU) to unite numbers that are connected.

For each pair (i, j), the LCM condition is equivalent to: nums[i] divides L, and nums[j] divides L, for some L ≤ threshold. Two numbers are connected if they share a common multiple ≤ threshold. A more efficient approach: for each divisor d of numbers ≤ threshold, group indices whose value is a multiple of d. Since threshold ≤ 2·10⁵, we can enumerate multiples of each d up to threshold. Use DSU: for each d, unite all numbers that are multiples of d. Complexity: sum over d of (threshold/d) ≈ threshold · log threshold, which is acceptable.

Steps:
1. Filter numbers > threshold → each is its own component; count them.
2. For numbers ≤ threshold, use DSU.
3. For d from 1 to threshold, collect all indices where nums[i] is a multiple of d; if more than one, union them all.
4. Count remaining unique DSU parents among numbers ≤ threshold.
5. Return total components.