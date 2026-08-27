- **Identity:** For a positive integer \(s\), if \(v=v_2(s)\), then
  \[
  f(s)=\frac{s}{2^v}=s-\sum_{k=1}^{v}\frac{s}{2^k}.
  \]
  Hence, letting \(T_k=\sum_{i\le j,\ 2^k\mid A_i+A_j}(A_i+A_j)\), the required answer is
  \[
  \sum_{i\le j}(A_i+A_j)-\sum_{k\ge1}\frac{T_k}{2^k}.
  \]
  The initial total is \((N+1)\sum_i A_i\), since each \(A_i\) occurs once in its diagonal pair with coefficient 2 and once in each of its \(N-1\) off-diagonal pairs.
- **One modulus formula:** For \(m=2^k\), maintain for every residue \(r\): \(c_r\), the number of values congruent to \(r\pmod m\), and \(s_r\), their original-value sum. A pair has sum divisible by \(m\) exactly when its residue classes are \(r\) and \(q=(-r)\bmod m\).
- **Distinct complement classes:** If \(r<q\), all pairs selecting one element from class \(r\) and one from class \(q\) qualify. Their total pair-sum contribution is
  \[
  c_r s_q+c_q s_r.
  \]
  This counts every unordered index pair exactly once: processing only \(r<q\) avoids later processing the reversed class pair \(q,r\), while every choice of one index from each distinct class determines exactly one pair with smaller index first.
- **Self-complement classes:** If \(r=q\), equivalently \(2r\equiv0\pmod m\), all pairs inside that class qualify, including diagonal pairs. For \(c=c_r\) values with total \(s=s_r\), the sum over all pairs \(i\le j\) is
  \[
  (c+1)s.
  \]
  Each value appears in \(c-1\) off-diagonal pair sums and contributes twice in its diagonal pair, for total coefficient \(c+1\). This correctly handles residues \(0\) and \(m/2\).
- **Termination:** It suffices to process powers \(m\le2\max A_i\), because every pair sum is positive and at most \(2\max A_i\); larger powers divide no pair sum.
- **Complexity:** There are at most 24 relevant powers for the constraints. Building residue maps for every power takes \(O(N\log \max A)\) time and \(O(N)\) memory. Python integers safely hold the result.
