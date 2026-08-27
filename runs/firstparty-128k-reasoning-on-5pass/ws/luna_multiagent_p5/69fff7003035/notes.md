- **Contribution decomposition:** For a distinguished value \(x\), let \(B\) be the set of elements appearing after \(x\). If \(B\) has size \(k\), its decimal multiplier is \(10^{\sum_{y\in B}\ell(y)}\). Every such subset corresponds to \(k!(N-1-k)!\) permutations, so its total contribution is multiplied by that factor.
- **Digit-length classes:** Elements with equal decimal length \(\ell\) have the same subset weight \(q_\ell=10^\ell\). For a fixed class, only the sum of its element values is needed.
- **Generating polynomial:** For all elements, define
  \[
  G(z)=\prod_\ell(1+q_\ell z)^{c_\ell}.
  \]
  Its coefficient \(g_k\) is the total weight of all \(k\)-element subsets.
- **Excluding the distinguished element:** For an element of length \(d\), the required polynomial is
  \[
  F_d(z)=G(z)/(1+q_dz).
  \]
  Its coefficient \(f_{d,k}\) gives the weighted sum over suffix sets of size \(k\) that do not contain the distinguished element. Coefficients are obtained by \(f_{d,0}=1\) and \(f_{d,k}=g_k-q_df_{d,k-1}\).
- **Computing \(G\) in \(O(NL)\):** Let \(Q(z)=\prod_\ell(1+q_\ell z)\) and
  \[
  R(z)=\sum_\ell c_\ell q_\ell\prod_{j\ne\ell}(1+q_jz).
  \]
  Then \(QG'=RG\). Since the number \(L\) of digit lengths is at most 6, coefficient recurrence uses only \(O(L)\) previous terms per coefficient.
- **Final formula:** For class \(d\), add
  \[
  \left(\sum_{x:\ell(x)=d}x\right)
  \sum_{k=0}^{N-1}f_{d,k}\,k!(N-1-k)!.
  \]
  All computations are modulo 998244353. Overall complexity is \(O(NL)\), with \(O(N)\) memory.
