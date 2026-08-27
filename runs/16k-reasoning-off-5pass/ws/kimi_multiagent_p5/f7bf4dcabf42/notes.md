
## ideation
Core difficulty: counting length-M strings over 26 letters by their exact LCS length with fixed S (N ≤ 10, M ≤ 100). Direct enumeration is impossible (26^M), so we need a compact state summarizing "LCS so far" against S.

Key insight: When scanning T character by character, the standard LCS DP row d[0..N] (d[i] = LCS length of processed prefix of T with S[:i]) is a sufficient statistic for future updates. Since d is nondecreasing with d[i]-d[i-1] ∈ {0,1}, there are at most 2^N ≤ 1024 states (actually fewer reachable ones). The transition on appending letter c is the classic DP recurrence:
new[0]=0; for i in 1..N: new[i] = max(d[i], new[i-1] + (S[i-1]==c ? 1 : 0), d[i-1] + (S[i-1]==c ? 1 : 0)) — equivalently the standard LCS cell update: if match, candidate = d[i-1]+1 else max(d[i], new[i-1])... careful: standard recurrence with row d (previous row) and building new row: new[i] = d[i-1]+1 if S[i-1]==c else max(d[i], new[i-1]). That's the correct transition.

Then the count of strings of length M whose final d[N] = k is obtained by DP over M steps: O(M · states · 26) ≤ 100·1024·26 ≈ 2.7M operations — trivial. No matrix exponentiation needed given M ≤ 100.

Pitfalls:
- State representation: encode profile as bitmask of N bits (bit i = d[i+1]-d[i]) or as tuple; use dict mapping state→index since not all 2^N profiles may be reachable (actually all nondecreasing 0/1-increment vectors are reachable, but dict is safer).
- Transition must be computed correctly: new[i] = d[i-1]+1 if c == S[i-1], else max(d[i], new[i-1]).
- Mod 998244353 applied at each addition.
- Answer for k: sum over states with d[N]=k, i.e., popcount of bitmask = k.
- Sanity check: total over k must equal 26^M mod p. Sample 1: 576+99+1=676=26² ✓.

## worker: Implement the complete solution: profile-state DP 
- State = N-bit mask encoding the LCS DP row d[0..N] (bit i = d[i+1]-d[i]). Since d is nondecreasing with 0/1 increments, the mask fully determines the row; d[i] = popcount of low i bits.
- Transition on appending letter c uses the standard LCS cell recurrence: new[i] = d[i-1]+1 if S[i-1]==c else max(d[i], new[i-1]). This is a sufficient statistic because the next row depends only on the previous row and c.
- Reachable states discovered via BFS from mask 0 (empty prefix), transitions computed lazily for all 26 letters. At most 2^N ≤ 1024 states.
- Counting DP over M steps: O(M · states · 26) ≤ ~2.7M ops, well within limits. All arithmetic mod 998244353.
- Aggregate by popcount(mask) = d[N] = exact LCS length.
- Verified sample 1 ("ab", M=2 → 576 99 1; total 676 = 26²) and sample 2 ("aaa", M=4 → 390625 62500 3750 101; total 456976 = 26⁴). Edge case N=1, M=1 gives 25 1 as expected.
