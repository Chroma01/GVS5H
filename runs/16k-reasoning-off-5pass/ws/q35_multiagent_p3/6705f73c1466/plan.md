1. Identify the positions of all '1's in the string. Let these positions be $p_0, p_1, \ldots, p_{k-1}$ (0-indexed).
2. The goal is to move all these 1s to a contiguous block of length $k$. If the final block starts at index $l$, the 1s will occupy positions $l, l+1, \ldots, l+k-1$.
3. The cost to move the $j$-th 1 (originally at $p_j$) to position $l+j$ is $|p_j - (l+j)| = |(p_j - j) - l|$.
4. Let $q_j = p_j - j$. The problem reduces to finding an integer $l$ that minimizes $\sum_{j=0}^{k-1} |q_j - l|$. This is the classic problem of finding the median.
5. The optimal $l$ is the median of the values $q_j$. If $k$ is odd, it's the middle element; if even, any integer between the two middle elements works (we can pick either).
6. Compute the sum of absolute differences from the median to get the minimum number of swaps.