
## ideation
The problem asks for, for each k=0..N, the number of length‑M strings over the 26‑letter alphabet whose longest common subsequence (LCS) with a fixed string S (|S|=N≤10) has length exactly k.

Because N is tiny (≤10) we can keep the whole DP table of the classic LCS algorithm as a state.  
For a processed prefix of the candidate string T the LCS with S can be described by an array  
`cur[i] = LCS(S[0..i‑1], processed T)` for i=0..N.  
`cur[0]=0` and `cur` is monotone non‑decreasing with `cur[i]‑cur[i‑1] ∈ {0,1}`.  
Therefore the whole array is determined by a bitmask of length N: bit i‑1 is 1 iff `cur[i] = cur[i‑1]+1`.  
The number of ones in the mask equals `cur[N]`, i.e. the LCS length.

The transition of this mask when we append a new character `c` is deterministic and can be computed in O(N) time using the LCS recurrence:

```
newcur[0] = 0
for i = 1..N:
    old_i      = cur[i]          # dp[i][old column]
    old_i_1    = cur[i-1]        # dp[i-1][old column]
    prev_new   = newcur[i-1]     # dp[i-1][new column]
    match      = (S[i-1] == c) ? 1 : 0
    newcur[i]  = max(old_i, prev_new, old_i_1 + match)
```

After obtaining `newcur` we rebuild the new mask from its differences.

The number of possible masks is at most 2^N ≤ 1024, and the alphabet has size 26, so we can pre‑compute the transition `trans[mask][c]` for every mask and every letter.  
Then a simple DP over the M positions of the string T is performed:

```
dp[mask] = number of length‑t prefixes that end in this mask
dp[0] = 1
for step = 1..M:
    new = zero
    for each mask:
        if dp[mask] != 0:
            for each c in 0..25:
                new[ trans[mask][c] ] += dp[mask]
    dp = new
```

After M steps `dp[mask]` counts all strings of length M that finish in that mask.  
The answer for a given k is the sum of `dp[mask]` over masks whose popcount (number of 1‑bits) equals k, because the LCS length equals the number of increments in the mask.

Complexities:  
- Pre‑computation: O(2^N · 26 · N) ≤ about 2.6·10^5.  
- DP: O(M · 2^N · 26) ≤ 100·1024·26 ≈ 2.6·10^6.  
- Memory: O(2^N) for the DP and the transition table.

All operations are performed modulo 998244353.

Pitfalls to watch:
- The LCS DP must keep the “new” value of the previous index (`newcur[i‑1]`) to correctly propagate a match forward; using only the old values would lose the possibility of a carry.
- The transition must be applied for all 26 letters, not only the letters appearing in S.
- The mask size is exactly N (bits 0..N‑1), not N+1.
- The answer for k=N includes the absorbing state where the mask is (1<<N)‑1 (all bits 1).

## worker: Implement the solution in Python as described: par
The solution uses a profile DP over the LCS table.  
For each possible LCS profile (represented by a bitmask of length N, where bit i‑1 is 1 iff the LCS length increased when considering the i‑th character of S) we pre‑compute the next profile after appending each of the 26 possible letters.  
The transition is computed by simulating the classic LCS DP column by column, using the recurrence `newcur[i] = max(oldcur[i], newcur[i-1], oldcur[i-1] + match)`.  
Then we run a simple DP for M steps, accumulating the number of strings ending in each profile.  
Finally, the answer for each k is the sum over profiles with exactly k bits set (the LCS length).  
The algorithm runs in O(M·2^N·26) ≤ 2.6·10^6 operations and uses O(2^N) memory, easily fitting the limits.
