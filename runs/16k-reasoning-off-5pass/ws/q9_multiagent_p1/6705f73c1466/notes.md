
## ideation
**Core Difficulty**:
The problem asks for the minimum number of swaps to make all '1's contiguous. The key insight is that the minimum number of swaps required to move a set of items to specific target positions (where the relative order of identical items is preserved) is equal to the sum of the distances each item travels. In this context, if we decide the final block of '1's occupies indices $[L, R]$, the $i$-th '1' (from the left in the original string) should move to the $i$-th position in $[L, R]$. The cost is $\sum |original\_pos_j - target\_pos_j|$.

**Candidate Approaches**:
1.  **Brute Force Simulation**: Try every possible contiguous block of length $K$ (where $K$ is the count of '1's) starting from every possible index. Calculate the cost by summing distances.
    *   *Complexity*: $O(N^2)$ or $O(N \cdot K)$. With $N=5 \times 10^5$, this is too slow (TLE).
2.  **Sliding Window / Prefix Sums Optimization**:
    *   Identify the positions of all '1's: $p_1, p_2, \dots, p_K$.
    *   The target block will end at some index $E$. Since the block must contain all '1's, the start of the block is $E - K + 1$. The valid range for $E$ is from $p_1$ (if we pack them as far left as possible, though technically the block could start before $p_1$? No, the block must cover the '1's, so the leftmost '1' must be $\ge$ start of block, and rightmost $\le$ end of block. Actually, the optimal block will always be within the range $[p_1, p_K]$? Not necessarily the indices, but the block of length $K$ must cover the range $[p_1, p_K]$. The optimal block starts at some $S$ such that $S \le p_1$ and $S+K-1 \ge p_K$. Wait, actually, we can just iterate the *end* position of the block. The block of ones will occupy indices $[x, x+K-1]$. The leftmost '1' ($p_1$) must be $\ge x$, and the rightmost '1' ($p_K$) must be $\le x+K-1$. Thus $x \le p_1$ and $x \ge p_K - K + 1$. So $x \in [p_K - K + 1, p_1]$.
    *   Let's re-evaluate the range. The target positions for the $i$-th '1' are $x + (i-1)$.
    *   Cost function $f(x) = \sum_{i=1}^K |p_i - (x + i - 1)| = \sum |p_i - (i-1) - x|$.
    *   Let $q_i = p_i - (i-1)$. Then $f(x) = \sum |q_i - x|$.
    *   This is the classic problem: find a point $x$ that minimizes the sum of absolute differences to a set of points $q_i$. The optimal $x$ is the **median** of $q_i$.
    *   We need to ensure the chosen $x$ results in a valid block (i.e., the block doesn't go out of bounds or violate the "contiguous" definition relative to the original string structure? Actually, the mathematical formulation $\sum |p_i - \text{target}_i|$ holds regardless of whether the target block overlaps with existing 0s in a weird way, as long as the target positions are distinct and form a contiguous block. The constraint is just that the target block must be within $[1, N]$. However, since we are moving '1's to form a block, the optimal block will naturally lie between the leftmost and rightmost '1' in the original string, extended by at most one '1' worth of space? Actually, the median approach gives the global minimum for the sum of distances. We just need to clamp the median to the valid range of $x$ if necessary, or simply check the valid range $[p_K - K + 1, p_1]$.
    *   Wait, is the range of $x$ strictly $[p_K - K + 1, p_1]$?
        *   The block is $[x, x+K-1]$.
        *   Condition: The $1^{st}$ '1' (at $p_1$) must map to $x$. So $x \le p_1$.
        *   The $K^{th}$ '1' (at $p_K$) must map to $x+K-1$. So $x+K-1 \ge p_K \implies x \ge p_K - K + 1$.
        *   Yes, $x$ must be in $[p_K - K + 1, p_1]$.
    *   The function $g(x) = \sum |q_i - x|$ is convex. The minimum is at the median of $q_i$. If the median falls outside $[p_K - K + 1, p_1]$, the minimum in the interval is at the boundary closest to the median.
    *   Algorithm:
        1. Collect indices of '1's into list $P$.
        2. Compute $Q_i = P_i - (i-1)$ for all $i$.
        3. Find median of $Q$.
        4. Calculate cost at median (clamped to valid range).
        5. Output cost.
    *   *Complexity*: $O(N)$ to find indices, $O(K \log K)$ to sort $Q$ (or $O(N)$ with linear selection), $O(1)$ to calculate cost using prefix sums of $Q$. Total $O(N)$.

3.  **Alternative Sliding Window**:
    *   Instead of median, iterate the start position $L$ of the block.
    *   Cost for a fixed $L$: $\sum_{i=1}^K |P_i - (L + i - 1)|$.
    *   We can update the cost incrementally as $L$ moves from $L$ to $L+1$.
    *   $Cost(L+1) = \sum |P_i - (L + i)| = \sum |(P_i - (L+i-1)) - 1|$.
    *   This looks like shifting the target by +1. For each '1', if it was to the left of the new target, distance increases by 1; if to the right, decreases by 1.
    *   Specifically, let $d_i(L) = P_i - (L + i - 1)$. Then $d_i(L+1) = d_i(L) - 1$.
    *   $|d_i(L) - 1| - |d_i(L)|$ is $-1$ if $d_i(L) \ge 0$, and $+1$ if $d_i(L) < 0$.
    *   So $\Delta Cost = (\text{count of } i \text{ where } P_i < L+i-1) - (\text{count of } i \text{ where } P_i \ge L+i-1)$.
    *   This can be computed efficiently if we maintain the counts. However, the median approach is simpler to implement and strictly $O(N)$ or $O(N \log N)$. Given $N=5 \times 10^5$, $O(N \log N)$ is perfectly fine.

## worker: Implement the solution using the median approach: 
1.  **Problem Analysis**: The problem asks for the minimum number of swaps to make all '1's contiguous. This is equivalent to moving the '1's to a contiguous block of length $K$ (where $K$ is the count of '1's) such that the sum of distances moved is minimized.
2.  **Mathematical Formulation**:
    *   Let the positions of '1's in the original string be $p_1, p_2, \dots, p_K$ (0-indexed).
    *   Suppose the final contiguous block of '1's starts at index $x$. Then the $i$-th '1' (originally at $p_i$) will move to position $x + i$.
    *   The cost (number of swaps) is $\sum_{i=0}^{K-1} |p_i - (x + i)|$.
    *   Rearranging the term inside the absolute value: $|p_i - i - x|$.
    *   Let $q_i = p_i - i$. The problem reduces to finding an integer $x$ that minimizes $\sum_{i=0}^{K-1} |q_i - x|$.
3.  **Optimization**:
    *   The function $f(x) = \sum |q_i - x|$ is a convex function. The value of $x$ that minimizes this sum is the **median** of the values in the list $q$.
    *   We collect all $q_i$, sort them, and pick the median (element at index $K // 2$).
    *   The minimum cost is then calculated by summing the absolute differences between each $q_i$ and the median.
4.  **Complexity**:
    *   Collecting indices: $O(N)$.
    *   Creating list $q$: $O(K)$.
    *   Sorting $q$: $O(K \log K)$. Since $K \le N$, this is $O(N \log N)$.
    *   Calculating cost: $O(K)$.
    *   Overall Time Complexity: $O(N \log N)$, which fits well within the limit for $N = 5 \times 10^5$.
    *   Space Complexity: $O(N)$ to store indices and the transformed list.

## worker: Run the provided Python solution to verify correct
The provided solution implements the optimal algorithm for this problem.
1.  **Logic**: It correctly identifies that moving all '1's to a contiguous block is equivalent to finding a target start position $x$ that minimizes the sum of distances $\sum |p_i - (x+i)|$.
2.  **Transformation**: By defining $q_i = p_i - i$, the problem reduces to finding $x$ that minimizes $\sum |q_i - x|$, which is a classic problem solved by the median.
3.  **Complexity**: The solution runs in $O(N \log N)$ due to sorting the list of '1' positions (or $O(N)$ with linear selection, but sorting is sufficient for $N=5 \times 10^5$). This fits well within the time limits.
4.  **Verification**:
    *   Sample 1: `0101001` (N=7). Indices of 1s: `[1, 3, 6]`. $q = [1-0, 3-1, 6-2] = [1, 2, 4]$. Median = 2. Cost = $|1-2| + |2-2| + |4-2| = 1 + 0 + 2 = 3$. Correct.
    *   Sample 2: `100` (N=3). Indices: `[0]`. $q = [0]$. Median = 0. Cost = 0. Correct.
    *   Sample 3: `0101001001` (N=10). Indices: `[1, 3, 6, 9]`. $q = [1, 2, 4, 5]$. Median (index 2) = 4. Cost = $|1-4| + |2-4| + |4-4| + |5-4| = 3 + 2 + 0 + 1 = 6$. Wait, sample output says 7. Let me re-check the sample logic.
    *   Re-check Sample 3 manually:
        *   String: `0101001001`
        *   1s at indices (0-based): 1, 3, 6, 9.
        *   Target block length $K=4$.
        *   Possible target blocks (start index $x$):
            *   $x=1$: targets 1, 2, 3, 4. Cost: $|1-1| + |3-2| + |6-3| + |9-4| = 0 + 1 + 3 + 5 = 9$.
            *   $x=2$: targets 2, 3, 4, 5. Cost: $|1-2| + |3-3| + |6-4| + |9-5| = 1 + 0 + 2 + 4 = 7$.
            *   $x=3$: targets 3, 4, 5, 6. Cost: $|1-3| + |3-4| + |6-5| + |9-6| = 2 + 1 + 1 + 3 = 7$.
            *   $x=4$: targets 4, 5, 6, 7. Cost: $|1-4| + |3-5| + |6-6| + |9-7| = 3 + 2 + 0 + 2 = 7$.
            *   $x=5$: targets 5, 6, 7, 8. Cost: $|1-5| + |3-6| + |6-7| + |9-8| = 4 + 3 + 1 + 1 = 9$.
        *   Minimum cost is indeed 7.
    *   Why did my manual calculation of the median approach yield 6?
        *   $q = [1, 2, 4, 5]$. Sorted $q$. $K=4$. $K//2 = 2$. $q[2] = 4$.
        *   Cost = $|1-4| + |2-4| + |4-4| + |5-4| = 3 + 2 + 0 + 1 = 6$.
        *   Wait, is the median logic flawed for even $K$?
        *   The function $f(x) = \sum |q_i - x|$ is minimized for any $x$ in $[q_{K/2 - 1}, q_{K/2}]$.
        *   Here $q = [1, 2, 4, 5]$. The range is $[2, 4]$.
        *   If I pick $x=2$: Cost = $|1-2| + |2-2| + |4-2| + |5-2| = 1 + 0 + 2 + 3 = 6$.
        *   If I pick $x=3$: Cost = $|1-3| + |2-3| + |4-3| + |5-3| = 2 + 1 + 1 + 2 = 6$.
        *   If I pick $x=4$: Cost = $|1-4| + |2-4| + |4-4| + |5-4| = 3 + 2 + 0 + 1 = 6$.
        *   Why does the brute force check give 7?
        *   Ah, the constraint! The target block must be valid. The target positions are $x, x+1, x+2, x+3$.
        *   The original indices are $1, 3, 6, 9$.
        *   If we choose $x=2$, targets are $2, 3, 4, 5$.
            *   1st '1' (at 1) moves to 2. Dist = 1.
            *   2nd '1' (at 3) moves to 3. Dist = 0.
            *   3rd '1' (at 6) moves to 4. Dist = 2.
            *   4th '1' (at 9) moves to 5. Dist = 4.
            *   Total = 7.
        *   My formula calculation: $|1-2| + |3-3| + |6-4| + |9-5| = 1 + 0 + 2 + 4 = 7$.
        *   Wait, in my manual check above for $x=2$, I wrote $|9-5|=4$, but in the "median calculation" step I wrote $|5-2|=3$.
        *   Let's re-calculate $q$ carefully.
        *   $p_0 = 1 \implies q_0 = 1 - 0 = 1$.
        *   $p_1 = 3 \implies q_1 = 3 - 1 = 2$.
        *   $p_2 = 6 \implies q_2 = 6 - 2 = 4$.
        *   $p_3 = 9 \implies q_3 = 9 - 3 = 6$.
        *   Ah! $q_3 = 9 - 3 = 6$, not 5. I made an arithmetic error in the manual trace.
        *   So $q = [1, 2, 4, 6]$.
        *   Median range $[2, 4]$. Let's pick $x=2$.
        *   Cost = $|1-2| + |2-2| + |4-2| + |6-2| = 1 + 0 + 2 + 4 = 7$.
        *   Matches sample output. The code logic is correct.
