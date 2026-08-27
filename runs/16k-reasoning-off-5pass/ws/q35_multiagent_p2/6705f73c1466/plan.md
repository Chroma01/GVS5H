1. Identify the positions of all '1's in the string S. Let these positions be $p_0, p_1, \ldots, p_{k-1}$ (0-indexed).
2. The goal is to move all these 1s to a contiguous block of length $k$. If we choose the target block to start at index $l$ (0-indexed), the 1s will occupy positions $l, l+1, \ldots, l+k-1$.
3. The minimum number of swaps to move the $i$-th 1 (currently at $p_i$) to position $l+i$ is $|p_i - (l+i)|$. The total cost for a given $l$ is $\sum_{i=0}^{k-1} |p_i - l - i|$.
4. Let $q_i = p_i - i$. Then the cost becomes $\sum_{i=0}^{k-1} |q_i - l|$. This is minimized when $l$ is the median of the values $q_0, q_1, \ldots, q_{k-1}$.
5. Compute the median of $q$, then calculate the total cost using that median as $l$.