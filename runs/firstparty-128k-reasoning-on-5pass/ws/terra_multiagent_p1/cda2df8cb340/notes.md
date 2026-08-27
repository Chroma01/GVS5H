- **Telescoping identity:** For a positive sum \(s\), if \(v_2(s)=t\), then
  \[
  f(s)=\frac{s}{2^t}=s-\sum_{k=1}^{t}\frac{s}{2^k}.
  \]
  Therefore, summing over all pairs \(i\le j\),
  \[
  \sum f(A_i+A_j)
  =
  \sum_{i\le j}(A_i+A_j)
  -
  \sum_{k\ge1}\frac{W_k}{2^k},
  \]
  where \(W_k\) is the sum of \(A_i+A_j\) over pairs \(i\le j\) whose sum is divisible by \(2^k\).
- **Base term:** Every \(A_i\) appears in \(N-1\) off-diagonal pairs and contributes \(2A_i\) in its diagonal pair. Thus
  \[
  \sum_{i\le j}(A_i+A_j)=(N+1)\sum_i A_i.
  \]
- **Residue grouping:** For modulus \(M=2^k\), a pair is valid iff residues satisfy \(r_i+r_j\equiv0\pmod M\). Store for each occurring residue its count and sum of values.
- **Ordered weighted aggregate:** Let \(O_M\) be the weighted sum over all ordered pairs \((i,j)\) satisfying divisibility:
  \[
  O_M=\sum_r \left(C_{-r}S_r+C_rS_{-r}\right),
  \]
  where \(C_r,S_r\) are the count and value sum of residue group \(r\). Iterating all sparse groups computes this directly.
- **Ordered to unordered correction:** Let \(D_M\) be the valid diagonal weighted sum. Since off-diagonal pairs occur twice in \(O_M\), while diagonals occur once,
  \[
  W_M=\frac{O_M+D_M}{2}.
  \]
  A diagonal is valid when \(2A_i\equiv0\pmod M\), so \(A_i\bmod M\) is either \(0\) or \(M/2\). Hence
  \[
  D_M=2(S_0+S_{M/2}).
  \]
- **Stopping point:** No positive pair sum exceeds \(2\max A\), so for powers \(M>2\max A\), no sum can be divisible by \(M\). Process all powers of two up to that bound.
- **Complexity:** At most about 25 moduli occur because \(A_i\le10^7\). Each level builds and scans sparse residue maps in \(O(N)\) expected time, for \(O(N\log\max A)\) total time and \(O(N)\) memory.
- **Validation:** The formula yields the supplied sample outputs 5, 384, and 20241214.
