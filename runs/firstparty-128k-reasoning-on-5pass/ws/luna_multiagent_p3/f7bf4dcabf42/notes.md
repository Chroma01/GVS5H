- **State representation:** After processing a prefix of the unknown length-\(M\) string, store the complete LCS DP row against every prefix of the fixed string \(S\). The state is a tuple of length \(N+1\), with index \(j\) equal to the LCS length against \(S[:j]\).
- **Transition:** For each possible next alphabet character, construct the next row using
  \[
  dp'[j]=\max(dp[j],dp'[j-1],dp[j-1]+[S[j-1]=c]).
  \]
  The value at index zero remains zero.
- **Aggregation:** Different letters can produce the same next row, so transitions are grouped and represented by their multiplicity among the 26 letters.
- **Dynamic programming:** Start from the all-zero row with count one and iterate exactly \(M\) characters. Counts are stored modulo 998244353.
- **Final extraction:** The LCS length after all characters is the last row entry, so sum counts of states by `state[N]`.
- **Complexity:** Only reachable LCS rows are stored. Each state has at most 26 letter transitions, each computed in \(O(N)\), and there are \(M\) iterations. This is easily feasible for \(N\le10\) and \(M\le100\).
