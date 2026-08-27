
## ideation
The core difficulty is that the problem requires minimizing total operations (where each operation changes a character by ±1 in alphabet) to transform the string into a "good caption" (every character appears in runs of length ≥ 3), and then among all minimum-cost solutions, return the lexicographically smallest one.

Key observations:
1. The allowed operation is changing a character to its adjacent alphabet letter (cost = 1 per step). So the cost to change `caption[i]` to character `c` is `|ord(caption[i]) - ord(c)|`.
2. A "good caption" consists of runs of length ≥ 3. Any such string can be decomposed into runs of length exactly 3 or more. We can model this with a DP where states track the current run's character and length (up to 3, since once length ≥ 3, the run is "complete" and we can either continue it or start a new one).
3. State space: 26 characters × 3 length states (1, 2, 3+) = 78 states. This is small enough for efficient DP.
4. Forward DP: `fwd[i][c][s]` = min cost to make prefix `[0..i]` good, where position `i` is the `s`-th char of a run of `c` (`s=1,2,3` where 3 means length ≥ 3).
5. Transitions at position `i`:
   - From "start" (i=0) or from a completed run (s=3 at i-1): can start a new run of any `c` with length 1. Cost = `best_prev + cost[i][c]`.
   - From run of `c` with length 1 or 2: must continue with `c`. Length becomes 2 or 3. Cost = `fwd[i-1][c][s] + cost[i][c]`.
   - From run of `c` with length 3+: can continue with `c` (stays 3+) or end and start new run of any `c'` (length 1).
6. Answer: `min over c of fwd[n-1][c][3]`. If `n < 3`, impossible (return "").
7. For lexicographically smallest string among minimum-cost solutions, we need reconstruction. We can precompute a "suffix" DP `suf[i][c][s]` = min cost to complete suffix `[i..n-1]` given that position `i` is the `s`-th char of a run of `c`. This is computed backward similarly to forward DP.
8. Reconstruct greedily left-to-right: track accumulated cost `acc`. At position `i` with previous state `(c_prev, s_prev)`, try candidate next characters `c` from 'a' to 'z' (respecting the forced continuation if `s_prev < 3`). For each valid transition to new state `(c, s)`, check if `acc + suf[i][c][s] == target`. Pick the smallest `c` that works, update `acc` and state, and continue.
9. Pitfalls:
   - Must handle the "3+" state correctly: once a run has length ≥ 3, we can keep extending it (which is equivalent to having multiple adjacent runs of the same char, but represented as one longer run).
   - The forward DP naturally allows runs of any length ≥ 3 by using the "3+" state.
   - Lexicographic tie-breaking must look at the actual string, which is determined by the sequence of run characters. Greedy left-to-right with suffix costs works because we only commit to a character if the remaining cost can still achieve the target.
   - The suffix DP must be computed carefully to match the forward DP state semantics.

The approach runs in O(n × 26) time and space, which is fine for n = 5×10^4.

## worker: Implement the forward DP with rolling arrays to co
I implemented the forward DP to compute the minimum cost `target` for transforming the string into a good caption, using rolling arrays to save space. The state space is 26 characters × 3 length states (1, 2, 3+). The DP correctly handles the transitions: starting a new run after a completed one, continuing a run, and extending a completed run. I also implemented the suffix DP (backward) and the reconstruction logic to produce the lexicographically smallest valid string among those achieving the minimum cost. The code handles the edge case `n < 3` by returning an empty string.

## worker: Test the solution on the provided examples ("cdcd"
The solution uses forward and backward dynamic programming to compute the minimum cost and then reconstruct the lexicographically smallest valid string. The forward DP tracks states of (character, run_length) with run_length being 1, 2, or 3+ (encoded as 0, 1, 2). The backward DP (suffix) computes the minimum cost to complete the string from any state at any position. Reconstructing greedily left-to-right while checking against the target cost ensures the lexicographically smallest result. Edge cases like `n < 3` return an empty string, and the DP naturally handles infeasibility.
