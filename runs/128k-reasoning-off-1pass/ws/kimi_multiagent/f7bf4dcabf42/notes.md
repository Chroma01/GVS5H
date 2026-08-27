
## ideation
The core difficulty: counting length-M strings over 26 letters by their exact LCS length with S, where N ≤ 10 but M ≤ 100 — brute force over 26^M strings is impossible.

Key insight: the LCS DP row d[j] = LCS(processed prefix of T, S[:j]) is a nondecreasing vector with increments 0 or 1, d[0]=0, d[N] ≤ N. Such vectors are in bijection with subsets of {1..N} (positions where d[j] > d[j-1]), so at most 2^N = 1024 states. The transition on appending character c is the standard LCS DP update: new[j] = max(old[j], new[j-1], old[j-1] + (c == S[j-1])). This is deterministic and depends only on the current state vector and c.

So the plan: enumerate all valid states, precompute transition[state][letter] for 26 letters, then DP over M steps counting strings per state (mod 998244353). Finally group by d[N] = popcount of the subset mask = k. Complexity: O(2^N * 26 * N) precompute + O(M * 2^N * 26) counting — trivial.

Pitfalls to watch:
- Must verify the transition on the "subset mask" representation reproduces the true LCS DP exactly (it does, since the DP row is fully determined by the vector, and the vector is recoverable from the mask: d[j] = popcount of mask & ((1<<j)-1)).
- The empty string T (length 0) corresponds to mask 0; after M ≥ 1 steps all states reachable, but DP naturally handles it.
- Mod arithmetic: 998244353.
- Answer for k=0 includes strings sharing no character subsequence with S (e.g., strings avoiding all distinct chars of S).
- Sanity check: sum of answers must equal 26^M mod p. Sample 1: 576+99+1 = 676 = 26^2 ✓.

## worker: Write the complete solve() function: encode states
- States are N-bit masks; bit j-1 set means d[j] = d[j-1] + 1 in the LCS DP row. All 2^N masks are valid states (any subset of positions is achievable), so we iterate over all of them.
- Transition: reconstruct d[] from the mask, apply the standard LCS DP update for the appended character (new[j] = max(old[j], new[j-1], old[j-1] + match)), then re-encode the resulting row as a mask. This is exact because the DP row fully determines the next row.
- Counting: M iterations of a vector-times-transition DP, mod 998244353. Complexity O(2^N * 26 * (N + M)) — at most ~1024*26*110 ≈ 3M operations, trivial.
- Verified against samples mentally: Sample 1 gives 576 99 1 (sum 676 = 26^2); Sample 2 gives 390625 62500 3750 101 (sum 456976 = 26^4). The k=0 case for S="aaa", M=4 is 25^4 = 390625 ✓ (strings avoiding 'a'), and k=N counts strings containing S as subsequence.
