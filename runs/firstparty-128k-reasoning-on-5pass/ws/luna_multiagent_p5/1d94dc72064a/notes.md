- **State recurrence:** Let \(W(U,R)\) denote whether the player to move wins, where \(U\) is the set of unvisited indices and \(R\) is the total number of remaining decrements on visited indices. If \(|U|=1\), then \(W(U,R)=\text{true}\), since selecting the final unvisited index immediately wins.
- **General recurrence:** For \(|U|>1\),
  \[
  W(U,R)=
  (R>0\land \neg W(U,R-1))
  \lor
  \bigvee_{i\in U}\neg W(U\setminus\{i\},R+A_i-1).
  \]
  A reserve move only changes the turn, while introducing \(i\) adds \(A_i-1\) reserve moves.
- **Only parity matters:** Starting from states with one or two unvisited indices, the recurrence shows that all relevant values depend on \(A_i\) only through the parity of \(A_i\). Removing an odd \(A_i\) leaves \(R\) unchanged; removing an even \(A_i\) increases \(R\) by one modulo two.
- **Small cardinalities:**
  - \(N=1\): Fennec always wins immediately.
  - \(N=2\): both children are singleton winning states, so the initial state is losing; Snuke wins.
  - \(N=3\): Fennec wins exactly when the three values are not all of the same parity.
- **Inductive pattern for \(N\ge4\):** Applying the recurrence by induction on \(|U|\), with the two parity classes tracked, gives that the initial state \(R=0\) is winning exactly when the number of odd values in the current set is odd. The reserve-move term flips the winner between consecutive parity values of \(R\), while each transition to a smaller set flips the parity contribution precisely when an even-valued index is selected. The resulting parity invariant is stable for all set sizes at least four.
- **Final criterion:** Fennec wins for \(N=1\); loses for \(N=2\); for \(N=3\), wins iff the odd count is \(1\) or \(2\); for \(N\ge4\), wins iff the odd count is odd.
- **Complexity:** Counting odd entries takes \(O(N)\) time and \(O(1)\) extra space.
