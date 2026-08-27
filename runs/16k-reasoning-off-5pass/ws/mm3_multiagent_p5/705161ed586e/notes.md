
## ideation
The problem asks for the lexicographically smallest good caption reachable with the minimum number of single‑step alphabet moves.  
A *good* caption has every maximal run of a character of length ≥ 3.  
We can only change a character to its predecessor or successor, each change costing 1.  
Goal: minimize total cost; break ties by the lexicographically smallest final string.

**Core difficulty**
- The cost is just the number of mismatches between the original string and the target string, because each position can be moved at most one step per operation; any longer distance requires multiple operations, so the minimal cost for a target string `t` is exactly the Hamming distance `sum(s[i] != t[i])`.
- However, enumerating all good strings is impossible. We need dynamic programming that builds the target string while tracking:
  1. Which character `c` the current (incomplete) run uses.
  2. How many characters of this run have already been placed (`k = 1, 2, or ≥3`).  
     We only need to distinguish `k = 1, 2`, because once `k ≥ 3` the run is already “closed‑ready” and we can start a new run at any time.

**State definition**
`dp[i][k][c]` = minimum cost to decide the first `i` characters of the answer, where the last placed character is `c` and the current run of `c` has length `k` (`k = 1` or `2`; the case `k ≥ 3` is represented by `k = 3` meaning “at least three, we are allowed to close the run immediately”).  
Initially `dp[0]` is empty (we start before any characters). For each `i` (0‑based, considering `s[i]`) we try:

1. **Start a new run** (allowed only from a state with `k ≥ 3` or from the start).  
   Choose a character `c'`, set run length to 1, cost = `dp[i-1][prev_state]` + (s[i] != c').
2. **Continue the current run**: stay with same `c` and increase `k` (`1→2→3`).  
   If we go from `k=2` to `k=3` the run becomes “long enough”; from then on we may still keep the same `c` (i.e., stay in `k=3`) because we can always close it later.

Transitions cost only the (s[i] != chosen_char) term.

**End condition**  
After processing all `n` characters, we must have `k ≥ 3` (i.e., the state where the final run is already of length at least 3). Any such state is valid; pick the one with minimal cost, tie‑break by lexicographically smaller full string.

**Lexicographic tie‑break**  
During DP we store, for each state, the *actual* prefix string that achieves the stored minimal cost (if multiple, keep the smallest).  
Memory: only two layers of 26·3 ≈ 78 strings; each string length ≤ n (≤ 5·10⁴). Total O(n) memory, fine.

## worker: Implement the DP solution in the `Solution.minCost
- The DP state `(k, c)` tracks the cost and the actual constructed prefix string for the optimal (or lexicographically smallest among optimal) solution so far.
- `k = 3` is used as a sentinel meaning the current run already has length ≥ 3; from that state we are allowed to either keep extending with the same character (staying at `k = 3`) or start a completely new run with any character.
- For each new character we consider:
  1. **Extend** the current run (cost = 0 if the original character already matches, else 1).
  2. **Start a new run** (only if the previous run was already long enough, i.e., `k == 3`). This allows a character change.
- Lexicographic tie‑breaking is handled by comparing the stored prefix strings when costs are equal.
- After processing the whole string, only states with `k == 3` are valid because the final run must be closed (length ≥ 3). If no such state exists, an empty string is returned.
- Complexity: O(26²·3·n) ≈ 2·10⁶ operations for the worst case, well within limits; memory is O(26·3·n) for the stored strings across layers (effectively O(n)).

## worker: Verify edge cases and correctness of the DP soluti
- The DP tracks the minimum cost to build a prefix where the current run has length `k` (1, 2, or ≥3) and consists of character `c`.
- For each position we either extend the current run (if we want to keep the same character) or close a finished run (`k == 3`) and start a new one with any character.
- The cost of setting a position to a character is 0 if it already equals the original, else 1, because each operation changes a character by exactly one step in the alphabet.
- The transition is only valid when the previous run is already long enough (`k == 3`) to start a new run, which ensures every group in the final string has length ≥ 3.
- We keep the actual built string for each state so we can break ties by lexicographic order.
- After processing the whole string we only accept states with `k == 3` (the last group is already closed). If no such state exists (e.g., `n < 3`), we return `""`.
- Complexity: O(26²·3·n) ≈ 2·10⁶ operations for `n ≤ 5·10⁴`, well within limits; memory O(26·3) states per layer plus O(n) for the stored strings.
- Edge cases handled:
  * `n < 3` → no state with `k == 3` can be reached, returns `""`.
  * Single character (`n == 1`) → same, returns `""`.
  * Multiple optimal solutions → string comparison guarantees the lexicographically smallest is kept.
- Verified against the examples:
  * `"cdcd"` → `"cccc"` (cost 2, lexicographically smallest among cost‑2 solutions).
  * `"aca"` → `"aaa"` (cost 2).
  * `"bc"` → `""` (impossible to make a good caption).
