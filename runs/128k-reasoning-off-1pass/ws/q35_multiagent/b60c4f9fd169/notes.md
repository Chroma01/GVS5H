
## ideation
The core difficulty is computing the Levenshtein distance between two very long strings (up to $5 \times 10^5$) with a very small constraint on the maximum allowed distance ($K \le 20$). The standard dynamic programming approach for edit distance has a time complexity of $O(|S| \cdot |T|)$, which is far too slow ($2.5 \times 10^{11}$ operations).

However, since we only care if the distance is $\le K$, we can use the "banded" or "bounded" edit distance algorithm. The key insight is that if the edit distance is at most $K$, then at step $i$ (processing the $i$-th character of $S$), we only need to consider characters in $T$ within the range $[i-K, i+K]$. Any cell $(i, j)$ in the DP table where $|i - j| > K$ will have a value greater than $K$ and can be ignored.

This reduces the time complexity to $O(K \cdot \max(|S|, |T|))$, which is roughly $20 \times 500,000 = 10^7$ operations, well within the time limit.

Pitfalls to avoid:
1.  **Indexing**: Carefully handle the boundaries of the strings. The band of relevant indices for $T$ at step $i$ is $\max(0, i-K)$ to $\min(|T|, i+K)$.
2.  **Initialization**: The first row and column of the DP table represent distances from an empty string. We can initialize the DP array such that `dp[j]` represents the edit distance between $S[0:i]$ and $T[0:j]$. We need to be careful with the initial values to ensure they don't artificially limit the search space incorrectly, but since we prune values $> K$, initializing with a large number (infinity) and letting the natural progression handle it is standard.
3.  **Space Optimization**: We only need two rows (current and previous) to save space, reducing space complexity from $O(|S| \cdot |T|)$ to $O(K)$ or $O(|T|)$ depending on implementation. Given $K$ is small, $O(K)$ space per row is efficient.
4.  **Early Termination**: If at any point the minimum value in the current row exceeds $K$, we can immediately return "No".

## worker: finalize
The problem requires determining if the Levenshtein distance between two strings $S$ and $T$ is at most $K$, where $K \le 20$ but the strings can be up to $500,000$ characters long. The standard $O(|S| \cdot |T|)$ dynamic programming approach is infeasible.

The solution uses the **bounded edit distance** algorithm (also known as the banding technique). The key observation is that if the edit distance is at most $K$, then at any step $i$ (processing the $i$-th character of $S$), the corresponding character in $T$ must be within the index range $[i-K, i+K]$. This is because if $|i-j| > K$, the edit distance would already exceed $K$ due to the necessary insertions/deletions.

By restricting the DP computation to this diagonal band, the time complexity becomes $O(K \cdot \max(|S|, |T|))$, which is approximately $20 \times 500,000 = 10^7$ operations, well within the time limit.

Space complexity is optimized to $O(|T|)$ by using two rows (current and previous) for the DP table, or even $O(K)$ if we only store the band, but $O(|T|)$ is simpler and still fits in memory.

Key implementation details:
1.  **Initial Check**: If $| |S| - |T| | > K$, it's immediately impossible.
2.  **Band Calculation**: For each $i$, we only compute $j$ in $[\max(0, i-K), \min(|T|, i+K)]$.
3.  **Pruning**: Values exceeding $K$ are capped at $K+1$ (or a large constant) to prevent overflow and unnecessary computation.
4.  **Early Termination**: If all values in the current band exceed $K$, we can terminate early.
