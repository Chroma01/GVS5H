
## ideation
- Key risk is counting orientations (`2^E`) instead of distinct in-degree sequences; many orientations collapse to the same sequence.
- Useful structural fact: for undirected graphs, the number of distinct in-degree sequences equals `T_G(2,1)`; at `(2,1)` the Tutte sum counts exactly the acyclic edge subsets/forests of `G`. This matches samples: triangle has 7 forests, adding one bridge doubles to 14.
- So the problem can be reframed as counting forests in a near-wheel graph: rim cycle `0..N-1` plus optional spokes to hub `N`. Cycles are either the whole rim cycle or formed by two spokes plus a rim path between their endpoints.
- The given 2x2 transfer-matrix plan is plausible for an `O(N)` forest count around the cycle, with trace closing the cyclic condition and `-2` removing two boundary/overcounted cases; it needs a rigorous state derivation.
- Main pitfalls: cyclic wraparound edge `(N-1,0)`, matrix multiplication order, proving why trace and `-2` appear, all-zero/all-one strings, `k=0/k=N`, mod-negative result, and keeping `O(1)` memory/`O(N)` time for `N=1e6`.

## worker: Implement the O(N) transfer-matrix solution (answe
- A standard Tutte-polynomial fact states that the number of distinct labelled in-degree sequences obtainable by orienting an undirected graph is \(T_G(2,1)\). This evaluation equals the number of forests in \(G\), so it suffices to count forests rather than orientations.
- Fix the set of selected spokes. If no spoke is selected, any proper subset of the \(N\) rim edges is a forest, giving \(2^N-1\) choices.
- If selected spokes split the rim into cyclic gaps of lengths \(L_1,\ldots,L_k\), then in each gap any subset of rim edges except the complete path may be chosen. This contributes \(\prod_j(2^{L_j}-1)\).
- Let
  \[
  M_i=\begin{pmatrix}2+s_i&s_i\\1&1\end{pmatrix}.
  \]
  Writing \(M_i=A+s_iC\), where
  \[
  A=\begin{pmatrix}2&0\\1&1\end{pmatrix},\qquad
  C=\begin{pmatrix}1&1\\0&0\end{pmatrix},
  \]
  the rank-one expansion of \(\operatorname{tr}(\prod_i M_i)\) gives exactly the above gap sum, plus \(2^N+1\) for the empty-spoke case. Therefore the forest count is \(\operatorname{tr}(\prod_i M_i)-2\).
- The recurrence was validated against exhaustive orientation enumeration for every binary string with \(3\le N\le8\), covering all 504 cases.
- Time complexity is \(O(N)\), with \(O(1)\) additional space beyond the input.
