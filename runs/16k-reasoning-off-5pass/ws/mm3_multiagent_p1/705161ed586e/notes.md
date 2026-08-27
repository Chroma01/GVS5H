
## ideation
**Core difficulty**
- We need to transform a string into one where every maximal run of equal characters has length ≥ 3.
- Allowed operation: change a character to its immediate neighbor in the alphabet (cost = 1 per step). So converting `c` to `ch` costs `|ord(c) - ord(ch)|`.
- Goal: minimize total cost; among minimum‑cost results, return the lexicographically smallest string.
- If impossible, return `""`.

**Key observations**
- The only constraint on the final string is the “run length ≥ 3” rule. There is no other restriction; any letter can appear anywhere.
- This is a classic DP on positions with a small state describing the current run.
- State per position `i`:
  - chosen character `ch` (0…25)
  - length of the current run modulo 3: `1`, `2`, or `3` (where `3` means “≥3”).
- Transition from state `(prev_ch, prev_run)` at position `i‑1` to `(ch, run)` at position `i`:
  - If `ch == prev_ch`:
    - `run = prev_run + 1`; if `prev_run == 2` then `run = 3` (capped).
  - If `ch != prev_ch`:
    - `run = 1` (new run starts).
- Cost added: `abs(ord(caption[i]) - ord(ch))`.
- For `i = 0` we only allow `run = 1` (no previous character).
- At the end (`i = n‑1`) we only accept states with `run == 3` (last run length ≥ 3). If `n < 3`, no state is valid → return `""`.

**Lexicographically smallest tie‑break**
- Naively storing full strings in DP would be O(n²) memory/time.
- Instead, store a back‑pointer: `(prev_i, prev_ch, prev_run)` for each state.
- After DP, among the end states with minimum cost, pick the one whose reconstructed string is lexicographically smallest. There are at most 26 candidates, so reconstruction cost is negligible.
- Reconstruction: walk back pointers from the chosen end state to the start, reverse, and build the answer.

## worker: Implement the DP solution in `Solution.minCostGood
The solution uses dynamic programming with state `(character, run_length_mod3)` where `run_length_mod3` is 0 (length 1), 1 (length 2), or 2 (length ≥3). For each position, we compute the minimum cost to reach each state, considering two transitions: starting a new run (different character) or continuing the current run (same character). The cost to change a character is the absolute alphabet distance.

Back-pointers are stored for reconstruction. At the end, we pick the state with minimum cost among those ending with a run length ≥3. If no such state exists (only possible when n < 3), we return empty string.

The lexicographically smallest tie-breaking is handled by storing back-pointers and reconstructing only the optimal path. Since we pick the minimum cost state, and there can be multiple states with the same minimum cost, we should ideally compare reconstructed strings. However, in this implementation, we pick the first one found (lowest character index) which may not always be lexicographically smallest. To properly handle ties, we should compare reconstructed strings among all states with the minimum cost.

**Correction needed**: The current code picks the first state with minimum cost (lowest character index), but this doesn't guarantee lexicographically smallest string. We need to collect all states with minimum cost and compare their reconstructed strings.

Let me revise the solution to properly handle lexicographic tie-breaking.

## worker: Fix the lexicographic tie-breaking by collecting a
The solution uses dynamic programming with state `(character, run_length_mod3)` where `run_length_mod3` is 0 (length 1), 1 (length 2), or 2 (length ≥3). For each position, we compute the minimum cost to reach each state, considering two transitions: starting a new run (different character) or continuing the current run (same character). The cost to change a character is the absolute alphabet distance.

Back-pointers are stored for reconstruction. At the end, we collect all states with minimum cost among those ending with a run length ≥3, reconstruct each candidate string, and pick the lexicographically smallest one. This properly handles the tie-breaking requirement.

If no feasible state exists (only possible when n < 3), we return empty string.

Time complexity: O(26·3·n) for DP plus O(26·n) for reconstruction of at most 26 candidates, which is efficient for n ≤ 5·10⁴.
