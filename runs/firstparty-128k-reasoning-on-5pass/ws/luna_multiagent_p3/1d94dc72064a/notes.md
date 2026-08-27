- **State abstraction:** Once an index is visited, all its remaining decrements are equivalent “waste” moves. Let \(U\) be the multiset of unvisited indices, and let \(R\) be the total number of available waste moves from visited indices. Visiting an index with value \(A_i\) removes it from \(U\) and increases \(R\) by \(A_i-1\); a waste move decreases \(R\) by one. Visiting the final unvisited index immediately wins.

- **Two unvisited indices:** Every claim move wins immediately on the next state, so only waste moves matter. The state is losing exactly when \(R\) is even.

- **Three unvisited indices:** If the three values \(A_i-1\) do not all have the same parity, some claim move reaches a losing two-index state, so the position is winning. If they all have parity \(p\), the position is losing exactly when \(R\not\equiv p\pmod 2\).

- **At least four unvisited indices:** Induction on the number \(m\) of unvisited indices gives a parity-only characterization. Let \(T\) be the parity of the sum of \(A_i-1\) over all unvisited indices. For even \(m\), the position is losing iff \(R\equiv T\); for odd \(m\), it is losing iff \(R\not\equiv T\). The \(m=4\) case follows directly from the three-index characterization. In the induction step, a claim of index \(i\) changes both \(R\) and \(T\) by \(A_i-1\), while a waste move changes only \(R\), causing the losing-parity condition to alternate with \(m\).

- **Initial position for \(N\ge4\):** Here \(R=0\), and \(T\) is the parity of the number of even \(A_i\), equivalently \(N+\#\{i:A_i\text{ odd}\}\pmod2\). Substituting into the induction condition shows that the initial position is losing exactly when the number of odd \(A_i\) is even. Therefore Snuke wins iff that count is even.

- **Exceptional cases:** \(N=1\) is always won by Fennec. \(N=2\) is always won by Snuke. For \(N=3\), Snuke wins exactly when all \(A_i\) are even.
