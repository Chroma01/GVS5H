- **Fixed target sum formulation:** Let the final common sum be \(S\). For every known \(B_i=b\), its paired final A value must be exactly \(S-b\). Every known A and known B value must be at most \(S\), since final values must be non-negative.
- **Matching interpretation:** Let \(x\) be the number of unknown entries in A, and let \(m\) be the number of known entries in B. For fixed \(S\), known-B positions require the multiset \(\{S-b\}\). A fixed A value \(a\) can satisfy such a requirement exactly when \(a+b=S\).
- **Number of fixed/fixed matches:** With frequency maps \(c_A,c_B\), the largest number of fixed A values usable at known-B positions is
  \[
  M(S)=\sum_a \min(c_A(a),c_B(S-a)).
  \]
  There is no conflict between terms: for a fixed \(S\), each A value \(a\) corresponds to only the B value \(S-a\).
- **Feasibility proof for fixed S:** The \(m-M(S)\) known-B requirements not supplied by fixed A values must use unknown A entries, so necessity is \(m-M(S)\le x\). It is also sufficient: after using \(M(S)\) fixed A values at known-B positions, the remaining fixed A count is \((N-x)-M(S)\). The number of unknown-B positions is \(N-m\), and
  \[
  (N-x)-M(S)\le N-m \iff m-M(S)\le x.
  \]
  Thus all remaining fixed A values fit at unknown-B positions; choose their B values as \(S-a\). Assign unknown A values as needed, also using \(S-b\), all non-negative because \(S\ge b\).
- **Immediate case:** If \(m\le x\), choose any sufficiently large \(S\). Unknown A entries supply all known-B positions. The inequality above guarantees remaining fixed A values fit into unknown-B positions, so answer is always Yes.
- **Candidate sums:** Otherwise \(m>x\), so feasibility requires \(M(S)\ge m-x>0\). Hence some fixed A and fixed B must match, so \(S=a+b\) for a fixed value pair. Enumerate all pairs of distinct fixed values from the two frequency maps.
- **Aggregation algorithm:** For every pair of distinct values \((a,b)\), add \(\min(c_A(a),c_B(b))\) to a dictionary keyed by \(a+b\). Ignore sums below the maximum fixed input value, since they cannot yield non-negative complements. If an aggregate reaches \(m-x\), output Yes. This is \(O(D_A D_B)\) time and uses a frequency map over encountered sums.
- **Implementation details:** Treat `-1` only as unknown, never as a numeric value. Use early termination once a sum reaches the required number of matches.
