
## ideation
We need to count, for each k (0…N), how many length‑M strings T have LCS(T,S)=k. N≤10 is tiny, M≤100.  
The standard LCS DP can be compressed to a 1‑dimensional row f[0…N] where f[i] = LCS length between the processed prefix of T and the first i characters of S.  
When a new character c is appended, the update is  
 f'[i] = max( f[i] , (c==S[i‑1] ? f[i‑1]+1 : f[i‑1]) ) , using the old values f[·].  

Because f[i] is non‑decreasing and increases by at most 1 at each step, the row is completely described by a bitmask of length N: bit j is 1 iff position j of S is matched in an LCS of the processed prefix. Indeed, f[i] equals the number of set bits among the first i positions.  

Thus each state is a mask (0 … 2^N‑1). The transition for a character c can be computed from the current mask by:
1. Reconstruct the old row f[i] = popcount(mask & ((1<<i)-1)).
2. Apply the DP recurrence to obtain the new row f'.
3. Derive the new mask by setting bit (i‑1) iff f'[i] > f'[i-1].

The number of states is ≤1024, the number of characters is 26, and N≤10, so we can pre‑compute all transitions (mask, char) → new_mask.

Now we count all strings of length M by a DP over the automaton:
- dp[mask] = number of processed strings that end in this mask.
- Start with dp[0]=1.
- For each of the M positions, for every mask, distribute its count to the 26 next states given by the transitions.

After M steps, the answer for k is the sum of dp[mask] over masks with popcount(mask)=k.

All operations are modulo 998244353. The total work is O(M·2^N·26·N) ≤ 100·1024·26·10 ≈ 2.6·10⁶, easily fast.

Pitfalls:
- Must use the old row values when updating (do not mix new and old in the same loop).
- The new mask is derived from the new row after the character is processed.
- N can be up to 10, so 2^N fits in an int.
- The DP counts each string exactly once because the automaton is deterministic.
