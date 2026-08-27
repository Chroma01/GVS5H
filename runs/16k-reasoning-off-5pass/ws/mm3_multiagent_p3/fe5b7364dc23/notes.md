
## ideation
We need to compute  

\[
S = \sum_{1\le l\le r\le N}\Bigl(\sum_{i=l}^r A_i\Bigr)^K \pmod{998244353}
\]

with \(N\le 2\cdot10^5\) and \(K\le 10\).

**Core difficulty**  
Directly enumerating all intervals is impossible. Using prefix sums \(S_i = \sum_{j=1}^i A_j\) (with \(S_0=0\)), the sum becomes  

\[
\sum_{0\le p<q\le N} (S_q - S_p)^K .
\]

**Candidate approaches**
1. Expand \((S_q - S_p)^K\) with the binomial theorem and sum over \(p<q\) by iterating \(q\) and maintaining running sums of powers of \(S_p\). This is \(O(NK)\) and fits the constraints.
2. Use generating functions or FFT convolution – unnecessary because \(K\le 10\).
3. Use multinomial expansion over original array – too large.

## worker: Implement the algorithm: read N, K and array A, co
The algorithm uses the binomial expansion of \((S_q - S_p)^K\) and a running sum of powers of earlier prefix sums. For each right endpoint \(q\) we maintain \(R[d] = \sum_{p<q} S_p^d\) and add  

\[
\sum_{t=0}^{K} \binom{K}{t} (-1)^{K-t} S_q^{\,t} \cdot R[K-t]
\]

to the answer. All operations are modulo \(998244353\).  
Complexity: \(O(NK)\) time, \(O(K)\) extra memory, which easily handles \(N\le 2\cdot10^5\) and \(K\le 10\).

The solution was verified against the provided samples:
- Sample 1 → 75
- Sample 2 → 0
- Sample 3 → 428633385
