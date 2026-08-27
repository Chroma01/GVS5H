- **Prime-wise reduction:** For each prime \(p\), let \(e_i=v_p(A_i)\). Since the reduced numerator and denominator of \(S_i/S_{i+1}\) are coprime and their product is \(A_i\), the valuation difference is \(v_p(S_{i+1})-v_p(S_i)=\pm e_i\) when \(e_i>0\), and is \(0\) when \(e_i=0\). Every choice of signs independently determines one edge factorization.

- **Normalization:** A sign choice gives a walk \(t_1=0\), \(t_{i+1}-t_i=\pm e_i\). The actual nonnegative valuations with gcd valuation zero are uniquely \(h_i=t_i-\min_j t_j\). Thus each sign walk contributes \(p^{\sum_i h_i}\).

- **DP state:** Instead of tracking the raw minimum, initialize the normalized walk at every possible height \(h_1\in[0,E]\), where \(E=\sum_i e_i\). A valid normalized walk must visit height zero at least once. `not_touched[h]` stores walks currently at \(h>0\) that have not visited zero; `touched[h]` stores walks that have visited zero.

- **Initialization weights:** The score contribution includes every vertex, so the initial state at height \(h\) has weight \(p^h\). Heights greater than \(E\) cannot reach zero because the total possible downward movement is at most \(E\).

- **Transitions:** For an edge exponent \(e>0\), transition from \(h\) to \(h-e\) and \(h+e\), discarding negative or out-of-range heights. Each transition is multiplied by \(p^{h'}\), accounting for the next vertex. For \(e=0\), there is one transition \(h\to h\), not two.

- **Contribution:** After all edges, sum every `touched[h]`. This equals the sum of \(p^{\sum_i h_i}\) over all prime-\(p\) valuation choices.

- **No double counting:** For each edge, the reduced fraction \(S_i/S_{i+1}\) uniquely determines its coprime numerator and denominator, hence the sign choice for every prime. Conversely, independent prime sign choices combine uniquely into the full sequence of reduced edge fractions and the normalized integer sequence. Therefore multiplying the prime-wise sums gives exactly the original sum of scores.

- **Complexity:** For prime \(p\), the DP uses \(O(N E_p)\) time and \(O(E_p)\) memory, where \(E_p=\sum_i v_p(A_i)\). Since \(\sum_p E_p=\sum_i\Omega(A_i)\le 9(N-1)\), the total time is \(O(N\sum_p E_p)\), and the total working memory is \(O(\max_p E_p)\).
