
## ideation
The problem describes a turn-based game where each move reduces the total sum of A by exactly 1. The game ends exactly when the total sum becomes 0 (because at that point, every A_i has been decremented enough times that each index i has been chosen at least once, thus S = {1,2,…,N}).

Key observations:
- Each move reduces sum(A) by exactly 1, regardless of which index is chosen.
- The game cannot end before sum(A) = 0, because S would not be full.
- The total number of moves in the game is exactly `total = sum(A)`.
- Since players alternate starting with Fennec, the winner is determined solely by the parity of `total`:
  - If `total` is odd → Fennec (who makes move 1, 3, 5, …) wins.
  - If `total` is even → Snuke (who makes move 2, 4, 6, …) wins.
- No strategy affects the outcome because the number of moves is fixed.

This is a classic parity / Nim-like observation. The values of individual A_i or which index to choose don't matter for the final winner under optimal play (though they might matter if there were a move constraint, but here moves are always available until sum=0).

Constraints: N up to 2×10⁵, A_i up to 10⁹, so the sum fits in 64-bit (max ~2×10¹⁴). Use Python's arbitrary precision anyway.

Pitfalls to avoid:
- Overcomplicating: the game is essentially "who makes the last move", which depends only on parity of total moves.
- Misreading: the problem says moves are always available until the end, confirming that the game always lasts exactly `total` moves.

## worker: <omitted>
The game ends exactly when the sum of A becomes 0, because at that point every index i has been chosen at least once, so S = {1,…,N}. Each move decreases the sum by 1, so the total number of moves equals `sum(A)`. Since players alternate and Fennec starts, the winner depends only on the parity of the total: odd → Fennec, even → Snuke. This is independent of any strategy. The implementation reads N and the A_i, sums them, and prints the result.
