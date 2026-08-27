We must transform the string into one where every maximal group has length ≥ 3, using minimum adjacent-letter changes (±1), and among minimum‑cost solutions return the lexicographically smallest. Because cost is just number of position changes (no weight), this is a shortest‑path / DP problem over positions with states encoding how the last group is being built.

Define `dp[i][k][c]` = minimum cost to process first `i` characters, where `k` (0,1,2) counts how many trailing characters already equal `c` (the character of the current open group). Transitions:
- Extend the current group: stay in same `c` with `k+1` (cost +0, but we may need to change `s[i]` to `c` ⇒ cost = (s[i]!=c)).
- Close the current group and start a new one of length ≥3: only allowed if `k≥3`. Choose new `c'`, set count=1, cost = (s[i]!=c') + dp[i-1][k][c].
At the end (i=n), any group count ≥3 is valid (we just need last group closed). Add sentinel requiring a final close (handled by only accepting states with k≥3).

We also need to reconstruct the lexicographically smallest among optimal solutions. While filling DP we store for each state the chosen predecessor (c_prev, k_prev, action) that gives minimal cost; when costs tie, prefer the one yielding a lexicographically smaller resulting prefix (compare reconstructable strings). This tie‑break can be done by storing, alongside DP, the actual resulting string (or a pointer to build it). Since n ≤ 5e4, 26*3 ≈ 78 states per position → 26*3*26 transitions = O(26²·3·n) ≈ 2e6, feasible.

Lexicographic comparison of prefixes during DP: keep the resulting string for each state (cost‑min first, then lexicographically smaller). Memory: store strings only at current and previous layer (O(26*3) strings of length up to n), acceptable. Or store predecessor indices and compare lazily; but storing actual strings is simpler and still O(n) total.

Finally, if no final state has reachable cost, return "".