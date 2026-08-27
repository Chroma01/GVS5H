- **Fixed target sum:** Let the final common sum be \(S\). Every fixed B-value \(b\) must receive an A-value exactly \(S-b\). Every fixed A-value \(a\) placed at an originally unknown B-position can be paired with B-value \(S-a\).

- **Non-negativity:** A feasible target must satisfy \(S \ge \max\) of all fixed A- and B-values. Then every generated complement \(S-a\) or \(S-b\) is non-negative. If both sides are unknown in a remaining slot, use values \(0\) and \(S\), which are non-negative since \(S\ge0\).

- **Notation:** Let \(p\) be the number of fixed A-elements, \(q\) the number of fixed B-elements, \(x=N-p\) the number of unknown A-elements, and \(y=N-q\) the number of unknown B-elements.

- **Complementary fixed matches:** For a target \(S\), define
  \[
  M(S)=\sum_v \min(\operatorname{count}_A(v),\operatorname{count}_B(S-v)).
  \]
  This is the maximum number of fixed B-elements that can be paired with fixed A-elements. Multiplicity is essential: contributions are minimum counts, not the number of raw pairs.

- **Feasibility condition:** For a fixed valid \(S\), feasibility is exactly
  \[
  M(S)+x\ge q.
  \]
  Necessity: among the \(q\) fixed B-positions, at most \(M(S)\) can use fixed A-values; every other one needs an unknown A-value, of which only \(x\) exist. Sufficiency: assign the \(M(S)\) matching fixed A/B pairs, then use unknown A-values for the remaining \(q-M(S)\) fixed B-values. The remaining fixed A-values number \(p-M(S)\). The inequality \(q-M(S)\le x=N-p\) is equivalent to \(p-M(S)\le N-q=y\), so all remaining fixed A-values fit into unknown B-positions. Fill their B-values as \(S-a\), and fill any entirely unknown leftover positions arbitrarily to sum to \(S\).

- **Immediate case:** If \(x\ge q\), all fixed B-values can be supplied by unknown A-values. Choose any sufficiently large \(S\), so the answer is immediately Yes. This also handles the case of no fixed B-values.

- **Candidate targets:** Otherwise, required fixed matches are \(r=q-x>0\). Any feasible target has \(M(S)\ge r>0\), hence contains at least one complementary fixed A/B pair and therefore must be \(S=a+b\) for some fixed A-value \(a\) and fixed B-value \(b\). It is sufficient to inspect these sums, rejecting sums below the maximum fixed value.

- **Computation:** For every pair of distinct fixed values \(a,b\), add \(\min(c_A(a),c_B(b))\) to the score for sum \(a+b\). This exactly computes \(M(S)\). The implementation packs each contribution with its sum, sorts the \(O(uv)\) values where \(u,v\le N\) are distinct-value counts, and scans equal sums. Time is \(O(uv\log(uv))\), with \(uv\le4\cdot10^6\); packed integers reduce memory compared with a large Python dictionary.
