1.  Read the number of test cases $T$.
2.  For each test case, read $N$ and the sequence $A$.
3.  Initialize a DP array `dp` of size $N+1$ with `dp[0] = 0`.
4.  Maintain a dictionary or array `last_pos` to store the last seen index of each value in $A$.
5.  Iterate $i$ from 1 to $N$:
    - Set `dp[i] = dp[i-1] + 1`.
    - If $A[i-1]$ (using 0-based indexing for A, so value is $A[i-1]$) has been seen before at index $j$ (1-based), update `dp[i] = min(dp[i], dp[j-1] + (i - j))`.
    - Update `last_pos[A[i-1]] = i`.
6.  Print `dp[N]`.