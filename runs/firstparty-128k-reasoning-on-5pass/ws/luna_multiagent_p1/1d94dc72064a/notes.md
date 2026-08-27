- **State abstraction:** After an index is selected for the first time, it becomes marked and contributes \(A_i-1\) ordinary delaying moves. All delaying moves are globally interchangeable; only their total remaining count and the parity pattern of the unmarked indices matter.
- **Parity recurrence:** Let \(W_k(e,r)\) denote whether the player to move wins with \(k\) unmarked indices, \(e\) of whose original residual values \(A_i-1\) are even, and with \(r\) delaying moves available. The recurrence is
  \(W_k(e,r)=\neg W_k(e,r-1)\) when a pass is available, or a winning marking move exists; marking an even residual preserves \(r\)'s parity, while marking an odd residual flips it.
- **Initial-state outcome:** Evaluating the recurrence at \(r=0\) gives the following exact small-size tables, where \(e\) is the number of odd \(A_i\):
  - \(N=1\): Fennec for every \(e\).
  - \(N=2\): Snuke for every \(e\).
  - \(N=3\): Fennec iff \(e\ge1\).
  - \(N=4\): Fennec iff \(e=1\).
  - \(N=5\): Fennec iff \(e=1\) or \(e\ge3\).
  - \(N=6\): Fennec iff \(e\in\{1,3\}\).
  - \(N=7\): Fennec iff \(e\in\{1,3,5,6,7\}\).
- **General criterion:** For \(N\ge8\), Fennec wins exactly when
  \(\binom{N-1}{m}\) is odd, where \(m\) is the number of even \(A_i\). By Lucas' theorem, this is equivalent to every set bit of \(m\) also being a set bit of \(N-1\), implemented as `(m & ~(N-1)) == 0`.
- **Complexity:** Counting odd values takes \(O(N)\) time and \(O(1)\) extra space.
