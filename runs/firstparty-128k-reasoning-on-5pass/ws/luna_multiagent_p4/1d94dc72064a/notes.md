- **State model:** Once an index is selected for the first time, it becomes visited. Its remaining decrements are ordinary expendable pass moves. If the unvisited indices are \(U\), and the total number of remaining decrements on visited indices is \(P\), a pass changes \((U,P)\) to \((U,P-1)\), while visiting \(i\) changes it to \((U\setminus\{i\},P+A_i-1)\). Visiting the last unvisited index immediately wins.

- **Parity-state lemma:** For every state with at least two unvisited indices, the losing values of \(P\) are exactly one of:
  1. all even \(P\);
  2. all odd \(P\);
  3. no values of \(P\).
  Thus only the parity of \(P\), together with which of these three cases applies, matters. The singleton state is always winning because the next new-index move wins immediately.

- **Why unavailable passes cause no issue:** At \(P=0\), a pass is simply not an option; at \(P>0\), the pass moves to the opposite parity. If the child state has losing parity \(q\), visiting an index of parity \(b=(A_i-1)\bmod 2\) is winning exactly when \(P\bmod2=q\oplus b\). Let \(R\) be the set of such target parities over all possible new indices. If \(R\) is empty, the current state loses exactly for even \(P\). If \(R=\{r\}\), it loses exactly for parity \(1-r\). If \(R\) contains both parities, it is always winning. This also proves the lemma inductively, including the special \(P=0\) boundary.

- **Compression to parity counts:** Let \(q(n_0,n_1)\) describe the losing-parity type for a set with \(n_0\) indices having \(A_i-1\) even and \(n_1\) indices having \(A_i-1\) odd. The recurrence only uses the two states obtained by deleting an even or odd index, so it depends only on these counts.

- **Evaluating the recurrence:** For two unvisited indices, the state loses at \(P=0\), so \(q=0\). For three indices, the state is losing at \(P=0\) only when all three \(A_i-1\) are odd, i.e. all three \(A_i\) are even. For every \(N\ge4\), induction on \(N\) gives:
  \[
  q =
  \begin{cases}
  n_1\bmod2,&N\text{ even},\\
  1-(n_1\bmod2),&N\text{ odd}.
  \end{cases}
  \]
  Fennec starts with \(P=0\), so Fennec wins exactly when \(q\ne0\).

- **Final criterion:** \(N=1\) is immediately won by Fennec; \(N=2\) is always won by Snuke. For \(N=3\), Snuke wins exactly if all \(A_i\) are even. For \(N\ge4\), writing \(k\) for the number of even \(A_i\), Fennec wins exactly when \(N+k\) is odd.
