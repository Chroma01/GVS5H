
## ideation
**Core difficulty:** Count, modulo 998244353, the number of length-M strings whose LCS with a fixed length-N string S is exactly k, for every k. N is tiny (≤10) but M can be up to 100, so any DP over the characters of S is fine.

**Idea:** We don't need to know the *alignment*; we just need to know the *current LCS length* after processing each character of the generated string. For a fixed S, we can define a transition: from a state `i` (current LCS length between the prefix of the generated string and S) and a new character `c`, what is the new LCS length?

Computing this transition naively would require recomputing the whole LCS DP, but N is small, so we can precompute `next[i][c]` in O(N²) per character (or O(N²·26) total). Specifically, for each `c`, run a 1D DP over the positions of S to compute the best LCS that can be achieved when we are allowed to match `c` as a new character. Since we are appending one character to the right, the standard recurrence:
```
if S[j] == c: new_j = max(new_j, old_i + 1)
else: new_j = max(new_j, old_i)
```
where `old_i` is the LCS length between the processed prefix of S up to position `i` and the already generated string. We need to incorporate that we *must* take `c` into the generated string.

**DP over generated string length:**
- `dp[i]` = number of strings processed so far whose LCS with S is exactly `i`.
- For each of the M positions, for each state `i` and each character `c` (26 choices), update `next[next_state] += dp[i]`.
- `next[i][c]` is precomputed.

**Complexity:** O(M·N·26 + 26·N²) which is trivial for N=10, M=100.

**Pitfalls:**
- The transition `next[i][c]` must consider that we *must* use the new character `c`; it is not optional. So we compute the LCS where we have the choice of matching `c` somewhere in S or not, but we always have the character present. The recurrence above (with max) correctly accounts for the option of not matching `c` (keeping the old LCS value). We also need to consider that the LCS can increase by at most 1 per added character.
- The final answer for k is simply `dp[k]` after processing M characters. We must output `dp[0] dp[1] ... dp[N]`. Note that `dp[N]` corresponds to strings whose LCS with S equals N (full match). It is possible that some states are unreachable; they will stay 0.
- Modulo 998244353 must be applied at every addition.

## worker: Implement a solution in Python that computes the D
The solution uses a state compression approach: instead of tracking only the current LCS length, we track the entire last row of the LCS dynamic programming table. Since N ≤ 10, the number of possible rows is at most 2^N = 1024, which is very small. For each state (row) and each of the 26 possible characters, we precompute the next state using the standard LCS DP recurrence. Then we perform M steps of DP, where each step multiplies the number of states by 26 but the total number of states remains bounded by 1024. Finally, we aggregate counts by the maximum value in the row (which equals the LCS length). This yields the exact counts for each k modulo 998244353.

The algorithm runs in O(M · 2^N · 26 + 2^N · N · 26) time, which is trivial for the given constraints. Memory usage is also small.
