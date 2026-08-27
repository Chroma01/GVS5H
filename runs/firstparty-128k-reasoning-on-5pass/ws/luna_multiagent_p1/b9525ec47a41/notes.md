- **Encoding:** Let \(x_i\) indicate whether the cycle edge from \(i-1\) to \(i\) contributes to the indegree of \(i\). For a spoke-present position, let \(y_i\) indicate whether its spoke contributes to \(i\). Then
  \[
  d_i=x_i+1-x_{i+1}+s_i y_i.
  \]
- **Local relations:** A degree choice defines a Boolean relation from \(x_i\) to \(x_{i+1}\), encoded by four bits using bit \(2x+y\) for transition \(x\to y\).
- **When \(s_i=0\):** Degree values \(0,1,2\) give masks \(2,9,4\), respectively.
- **When \(s_i=1\):** Degree values \(0,1,2,3\) give masks \(2,11,13,4\). The corrected degree-2 relation is \(0\to0\), \(1\to0\), and \(1\to1\), hence \(1|4|8=13\).
- **Dynamic programming:** The accumulated relation after processing a prefix is one of only 16 masks. For every possible local degree label, compose the current relation with its local relation. Each degree-label string corresponds to exactly one ordinary-vertex degree sequence, so multiplicities are counted correctly even if different label strings produce the same accumulated relation.
- **Cyclic condition:** The cycle closes exactly when the final relation contains \(0\to0\) or \(1\to1\), represented by bit 0 or bit 3. The hub indegree is then uniquely determined by the fixed total number of edges and the ordinary indegrees.
- **Complexity:** \(O(N)\) time and \(O(1)\) memory, with at most 16 relation states and four transitions per position.
- **Verification:** Exhaustive enumeration for small \(N\) and all binary strings agrees with direct orientation enumeration after applying the corrected mask. The provided samples produce 14 and 261339902.
