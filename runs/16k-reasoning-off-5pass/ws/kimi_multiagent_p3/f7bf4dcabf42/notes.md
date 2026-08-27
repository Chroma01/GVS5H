
## ideation
The core difficulty is counting length-M strings T by their exact LCS length with fixed short S (N ≤ 10). Direct enumeration (26^M) is impossible for M up to 100, so we need a DP/automaton approach.

Key insight: When computing LCS(S, T) via the standard DP, processing T left to right, the "DP row" after each character of T is a tuple (d_1, ..., d_N) where d_i = LCS(T-prefix, S[1..i]). Properties: 0 ≤ d_1 ≤ ... ≤ d_N ≤ N, and consecutive entries differ by at most 1. The number of such states is small for N ≤ 10 (bounded by Motzkin/Catalan-like numbers; empirically a few thousand at most). Each new character c gives a deterministic transition: new_i = max(new_{i-1}, d_i, d_{i-1} + [S[i-1] == c]). So we build a finite automaton, then do M-step counting DP over states, and group final counts by d_N = k.

Pitfalls:
- State encoding must be canonical; use tuples as dict keys, assign ids via BFS from the all-zero state.
- Transitions depend on the full row, not just the last value — must store the whole tuple.
- Mod 998244353 arithmetic; M steps × states × 26 letters must be efficient (states ~ few thousand, 26 × 100 × few thousand ≈ manageable in Python, but precompute per-state transition lists of 26 next-ids and aggregate counts of letters leading to the same next state to speed up).
- Answer for k=0 includes strings avoiding all characters of S appropriately — handled naturally.
- Verify with sample: N=2, M=2, "ab" → 576 99 1; total must equal 26^M mod p.

## worker: Implement the complete solution: LCS row-transitio
- State = DP row tuple (d_1..d_N) of LCS lengths of processed prefix of T against each prefix of S. Transition per letter uses standard recurrence: new_i = max(d_i, new_{i-1}, d_{i-1} + match).
- BFS from the all-zero tuple enumerates all reachable states over 26 letters; transitions aggregated as next-state → letter multiplicity for speed.
- M-step linear DP counts strings per state mod 998244353; answers grouped by last component d_N = exact LCS length.
- Sanity: sum of answers ≡ 26^M (mod p). Sample 1: 576+99+1 = 676 = 26^2 ✓. Sample 2: 390625+62500+3750+101 = 456976 = 26^4 ✓. State count for N=10 is small (a few thousand), so 100 × states × ≤26 transitions runs fast.
