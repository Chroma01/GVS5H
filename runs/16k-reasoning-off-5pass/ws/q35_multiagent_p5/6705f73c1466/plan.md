1. Identify the positions of all '1's in the string. Let these positions be $p_1, p_2, \ldots, p_k$ (0-indexed).
2. The goal is to move all '1's to a contiguous block. If we choose the final block to start at index $l$ and end at $l+k-1$, the cost is the sum of distances each '1' moves to its target position.
3. Specifically, if the $j$-th '1' (0-indexed among the 1s) moves to position $l+j$, the cost for that '1' is $|p_j - (l+j)|$. The total cost is $\sum_{j=0}^{k-1} |p_j - l - j|$.
4. Let $q_j = p_j - j$. Then the cost becomes $\sum_{j=0}^{k-1} |q_j - l|$. This is minimized when $l$ is the median of the values $q_0, q_1, \ldots, q_{k-1}$.
5. Compute the median of $q_j$ values and calculate the total cost using that median.