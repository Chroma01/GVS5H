1. Identify the positions of all '1's in the string. Let these positions be $p_0, p_1, \ldots, p_{k-1}$ (0-indexed).
2. The goal is to move all these 1s to a contiguous block of length $k$. If we choose the final block to start at index $l$ (0-indexed), the 1s will occupy positions $l, l+1, \ldots, l+k-1$.
3. The minimum number of swaps to move the 1s from their current positions $p_i$ to the target positions $l+i$ is $\sum_{i=0}^{k-1} |p_i - (l+i)| = \sum_{i=0}^{k-1} |(p_i - i) - l|$.
4. Let $q_i = p_i - i$. We need to find an integer $l$ that minimizes $\sum_{i=0}^{k-1} |q_i - l|$. This is a classic problem: the optimal $l$ is the median of the values $q_i$.
5. The valid range for $l$ is $0 \leq l \leq N-k$. However, since the median of $q_i$ will naturally fall within the range $[q_0, q_{k-1}]$ and $q_0 = p_0 \geq 0$ and $q_{k-1} = p_{k-1} - (k-1) \leq N-k$, the median is always a valid starting position.
6. Compute the sum of absolute differences using the median.