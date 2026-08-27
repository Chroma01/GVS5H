- **Cycle encoding:** Let \(x_i\) indicate the direction of cycle edge \(\{i,i+1\}\), with \(x_i=1\) for \(i\to i+1\). The cycle contribution to vertex \(i\) is \(1+x_{i-1}-x_i\).

- **Correct local relations:** A local degree \(d_i\) defines a Boolean relation from \(x_{i-1}\) to \(x_i\). Using bits \(1,2,4,8\) for \(0\to0,0\to1,1\to0,1\to1\):
  - If \(s_i=0\), the masks for \(d_i=0,1,2\) are respectively \(2,9,4\).
  - If \(s_i=1\), the masks for \(d_i=0,1,2,3\) are respectively \(2,11,13,4\).

- **Hub degree is determined by the local degree word:** For an active spoke, let \(y_i=1\) when it points into vertex \(i\). Then \(d_i=1+x_{i-1}-x_i+y_i\). Summing over all cycle vertices on a cyclic path gives
  \[
  \sum_i d_i=N+\sum_i y_i.
  \]
  If \(m\) is the number of active spokes, the hub receives \(m-\sum_i y_i\) spokes, so
  \[
  d_N=m+N-\sum_i d_i.
  \]
  Therefore every attainable local degree word determines exactly one hub degree, and counting pairs (local word, hub degree) is identical to counting attainable local words.

- **Automaton DP:** Compose the local relations from left to right. There are only 16 possible Boolean relations on the two cycle-direction states. `dp[r]` counts distinct degree prefixes whose composed relation is \(r\). Each degree choice is one distinct symbol, so this counts words rather than orientations.

- **Cycle closure:** After all \(N\) vertices, the initial and final cycle states must agree. Thus the composed relation must contain \(0\to0\) or \(1\to1\), i.e. relation bit 0 or bit 3.

- **Complexity:** The algorithm uses \(O(16\cdot4\cdot N)=O(N)\) time and \(O(16)\) memory.
