- **Fixed target formulation:** Let the final common sum be \(S\). Since all final A and B values must be nonnegative, necessarily \(S\) is at least every initially fixed value in both sequences. Thus set \(L=\max(\max A_{\text{fixed}},\max B_{\text{fixed}})\), with the empty-side maximum ignored.

- **Complementary fixed matches:** For a fixed \(S\ge L\), a fixed A value \(x\) and fixed B value \(y\) can share an index exactly when \(x+y=S\). Let \(M(S)=\sum_x \min(c_A(x),c_B(S-x))\). This is the maximum number of fixed-A/fixed-B pairs, because each A value can only complement one B value for this S.

- **Wildcard capacities:** Let \(p,q\) be the counts of fixed A and fixed B entries, and let \(a=N-p,b=N-q\) be wildcard counts in A and B. After making \(M(S)\) fixed/fixed pairs, the remaining \(p-M(S)\) fixed A values require wildcard B positions, so \(p-M(S)\le b\). Similarly, remaining fixed B values require wildcard A positions, so \(q-M(S)\le a\). Therefore feasibility for fixed S is exactly
  \[
  M(S)\ge T,\qquad T=\max(0,p-b,q-a).
  \]
  This is sufficient because all remaining fixed values are at most S and can be paired with appropriately assigned nonnegative wildcard values \(S-x\) or \(S-y\); leftover wildcard/wildcard positions can be filled with 0 and S.

- **Candidate sums:** If \(T=0\), every \(S\ge L\) is feasible, so the answer is immediately Yes. If \(T>0\), every feasible S has at least one complementary fixed pair, hence belongs to the finite set
  \[
  \{x+y \mid x\text{ fixed in A},\,y\text{ fixed in B},\,x+y\ge L\}.
  \]
  Testing this set is complete.

- **Enumeration method:** Compress fixed values with counters. For every distinct pair \((x,y)\), its contribution to \(M(x+y)\) is \(\min(c_A(x),c_B(y))\). Encode each pair’s sum and contribution, sort by sum, and accumulate contributions for equal sums. This is \(O(U_AV_A\log(U_AV_B))\subseteq O(N^2\log N)\) time and \(O(U_AV_B)\subseteq O(N^2)\) memory.

- **Special case:** For \(T=1\), a valid candidate exists iff some fixed pair has sum at least L. This is equivalent to \(\max A_{\text{fixed}}+\max B_{\text{fixed}}\ge L\), avoiding quadratic storage.
