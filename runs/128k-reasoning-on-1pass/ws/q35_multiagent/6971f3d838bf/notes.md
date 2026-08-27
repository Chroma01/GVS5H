
## ideation
The problem asks for the maximum subarray sum after removing all occurrences of at most one integer $x$. This is equivalent to finding the maximum subarray sum in the original array, or in an array where all occurrences of some $x$ are replaced by 0.

Let $A_x$ be the array obtained by replacing all occurrences of $x$ in `nums` with 0. We want to compute $\max(M, \max_{x} \text{maxSubarraySum}(A_x))$, where $M$ is the max subarray sum of the original array.

Computing $\text{maxSubarraySum}(A_x)$ for each distinct $x$ naively takes $O(N^2)$, which is too slow. We can optimize this using a segment tree. Let $dp[x]$ be the maximum subarray sum ending at the current position in $A_x$. The recurrence is $dp[x]_i = \max(0, dp[x]_{i-1}) + A_x[i]$. Since $A_x[i] = \text{nums}[i]$ if $x \neq \text{nums}[i]$ else 0, we have:
- For $x \neq \text{nums}[i]$, $dp[x]_i = dp[x]_{i-1} + \text{nums}[i]$.
- For $x = \text{nums}[i]$, $dp[x]_i = dp[x]_{i-1}$.

This suggests we can maintain $dp[x]$ values using a global lazy addition. Let $G$ be a global add value. We maintain $dp[x] = \text{stored\_dp}[x] + G$. When processing $\text{nums}[i] = v$:
1. Update $G \leftarrow G + v$.
2. For $x = v$, we want $dp[v]$ to not increase by $v$. Since $G$ increased by $v$, we must decrease $\text{stored\_dp}[v]$ by $v$ to compensate. So $\text{stored\_dp}[v] \leftarrow \text{stored\_dp}[v] - v$.
3. For $x \neq v$, $\text{stored\_dp}[x]$ remains unchanged, so $dp[x]$ increases by $v$ as desired.

We use a segment tree to maintain $\text{stored\_dp}$ values, supporting point updates and range maximum queries. The values in `nums` are in $[-10^6, 10^6]$, so we offset them by $10^6$ to map to $[0, 2000000]$. The segment tree size is $O(\max V)$. This gives an overall time complexity of $O(N \log (\max V))$, which fits within the constraints.
