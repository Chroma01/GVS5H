
## ideation
The game ends as soon as every index `1..N` has been chosen at least once. The last move wins. Each `A_i` contributes `A_i` moves, but the first time an index is picked it also adds it to `S`; subsequent picks on the same index are “waste” moves that don’t change `S`. The key is that the game ends exactly when the `N`‑th *new* index is added, and then `sum(A_i) - N` waste moves have already been played (since each `A_i` provides `A_i` total uses, `N` of which are “first uses” adding a new index, the rest are waste). So the total number of moves in the game is `sum(A_i)`. Fennec makes moves 1, 3, 5, … and wins if the total number of moves is odd, i.e., if `sum(A_i)` is odd. This can be proven by the standard “turn‑based Nim with a fixed total move count” argument, or by noting that players can always avoid being forced to end the game early except when no waste moves remain.

## worker: finalize
The game always lasts exactly `sum(A_i)` moves. This is because each move decrements some `A_i` by 1, and the game ends precisely when the last decrement that fills `S` is made, but every decrement is a move, and the total number of decrements possible (i.e., the sum of `A_i`) is exactly the number of moves played. Since players alternate starting with Fennec, Fennec wins iff the total number of moves is odd, which is equivalent to `sum(A_i)` being odd.

This is a well-known observation for this type of "cover all indices" game: the parity of the total number of operations determines the winner.
