
## ideation
The core difficulty is counting, for each k, the number of length-M strings T over a 26-letter alphabet such that LCS(S,T)=k, with N≤10. Since N is tiny, we can model the LCS DP state after processing a prefix of T as a vector dp[0..N] where dp[i] = LCS(S[0..i-1], current T prefix). The transition for a new character c is:

```
new_dp = dp[:]
for i = 1..N:
    if S[i-1] == c:
        new_dp[i] = max(new_dp[i], dp[i-1] + 1)
    new_dp[i] = max(new_dp[i], new_dp[i-1])
return new_dp
```

This is the correct recurrence (uses old dp[i-1] and new dp[i-1] as in the standard LCS DP). The number of reachable states is small (≤ a few thousand for N=10). We can BFS from the initial state (all zeros) to collect all reachable states, build a transition count matrix T[state][next_state] = number of characters causing that transition, then run a length-M DP over states. Finally, sum counts for states with last entry = k.

Pitfalls:
- Incorrect transition (must use both old and new dp values).
- BFS must include all reachable states; using a set avoids duplicates.
- Modulo 998244353 throughout.
- M can be up to 100, so the M-step DP is trivial.

The plan is solid and matches the sample outputs once the transition is correct.

## worker: Implement the solution in Python: read inputs, BFS
We used the standard LCS DP state vector `dp[0..N]` where `dp[i]` is the LCS length between the processed prefix of `T` and the prefix `S[0..i-1]`. The transition for a new character `c` is correctly implemented as:

```python
new_dp = dp[:]
for i in 1..N:
    if S[i-1] == c:
        new_dp[i] = max(new_dp[i], dp[i-1] + 1)
    new_dp[i] = max(new_dp[i], new_dp[i-1])
```

This corresponds to the recurrence `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` with the extra match case `dp[i-1][j-1]+1`.  
We BFS over reachable states (at most a few thousand for `N ≤ 10`), build a 26‑way transition count matrix, then run a length‑`M` DP over states. Finally we sum counts for states whose last entry equals `k`.  
All operations are modulo `998244353`. The algorithm runs easily within the limits (`N ≤ 10`, `M ≤ 100`).
