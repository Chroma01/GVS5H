The game ends when index `i` is chosen for the first time, reducing `A_i` and (if not already in `S`) adding `i` to `S`. The game finishes as soon as every index `1..N` has been chosen at least once. The total number of moves is `sum(A_i) - N + (number of distinct indices ever chosen before the last move)`. Since all `N` indices must be in `S` at the end, the last move is the first time the *final missing* index is chosen. The key insight: players can delay completing `S` by revisiting already-chosen indices (when `A_i >= 2`). The player who makes the move that finally fills `S` wins. This is a normal-play impartial game; we analyze whether the first or second player can force the last move.

Let `cnt1` = number of `A_i == 1` (only one chance to add that index to `S`).  
Let `cnt_ge2` = number of `A_i >= 2` (can "waste" a move on them).

Moves on `cnt1` indices: each *must* add its index to `S` on its only use.  
Moves on `cnt_ge2` indices: the first use adds the index; extra uses just decrement without changing `S`.

Total moves = `sum(A_i) - cnt_ge2` (since each `A_i >= 2` has one "free" revisit).  
The first `N` *distinct* index-additions must happen, then extra waste moves are played on `cnt_ge2` indices. The game ends the moment the N-th distinct index is added. This is equivalent to: players alternately pick moves; the last *effective* move (that adds a new index) is the winning move.

Analysis: After the last distinct index is added, there are still `sum(A_i) - N` extra moves available (all on `A_i >= 2` indices). The player who makes the move that adds the last distinct index wins, *unless* there are zero extra moves after it (then that player also makes the last move overall). In either case, the parity of `(sum(A_i) - N)` and `N` together determine the winner.

Result: Let `total_extra = sum(A_i) - N` (number of "waste" revisits). The game length is `N + total_extra` moves. The last move is the `(N + total_extra)`-th. Since Fennec moves on odd turns, Fennec wins iff `(N + total_extra)` is odd, i.e., `sum(A_i)` is odd.