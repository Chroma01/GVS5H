- **Cumulative divisibility identity:** For a positive pair sum \(s\), if \(v=v_2(s)\), then \(f(s)=s/2^v\). The geometric identity
  \[
  s-\sum_{k=1}^{v}\frac{s}{2^k}=\frac{s}{2^v}
  \]
  gives
  \[
  \sum_{i\le j} f(A_i+A_j)
  =
  T-\sum_{k\ge1}\frac{S_k}{2^k},
  \]
  where \(T=\sum_{i\le j}(A_i+A_j)\), and \(S_k\) is the sum of all qualifying pair sums divisible by \(2^k\).
- **Unfiltered total:** Every \(A_i\) occurs in exactly \(N+1\) expressions among unordered pairs \(i\le j\): once with itself contributing twice, and once in each pair with every other index. Therefore \(T=(N+1)\sum_i A_i\).
- **Residue buckets:** For a fixed modulus \(q=2^k\), a pair qualifies exactly when its residues satisfy \(r+s\equiv0\pmod q\). Store for each present residue its element count \(c_r\) and value sum \(u_r\).
- **Different complementary buckets:** For residues \(r\ne t=(-r)\bmod q\), all cross pairs qualify and their pair-sum total is \(c_r u_t+c_t u_r\). Process only when \(r<t\) to avoid double counting.
- **Self-complementary bucket:** If \(r=(-r)\bmod q\), all pairs within that bucket qualify. For a bucket with count \(c\) and element sum \(u\), the total over unordered pairs including diagonals is \((c+1)u\). This correctly includes each diagonal \(2A_i\).
- **Power range:** No positive pair sum exceeds \(2\max A_i\), so only powers \(2^k\le2\max A_i\) matter. The implementation uses `range(1, (2*max(a)).bit_length())`.
- **Complexity:** There are \(O(\log M)\) powers, where \(M=\max A_i\). Each level builds sparse residue buckets and scans them, for total expected \(O(N\log M)\) time and \(O(N)\) memory. With \(M\le10^7\), there are at most 24 levels.
- **Integer safety:** Python integers safely hold the answer, which can be on the order of \(N^2M\).
