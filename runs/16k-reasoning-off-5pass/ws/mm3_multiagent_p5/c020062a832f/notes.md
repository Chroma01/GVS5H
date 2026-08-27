
## ideation
The problem asks for the inversion count of the sequence \(B_i = (A_i + k) \bmod M\) for all \(k = 0, 1, \dots, M-1\).  
When \(k\) increases by 1, every element increases by 1 modulo \(M\). The only pairs whose order can change are those involving an element that wraps from \(M-1\) to \(0\). Let \(x = (M-1 - k) \bmod M\) be the value that wraps at step \(k\). The change in inversion count is \(\Delta[x] = P[x] - Q[x]\), where  
- \(P[x]\) = number of pairs \((i,j)\) with \(i<j\), \(A_i \neq x\), \(A_j = x\),  
- \(Q[x]\) = number of pairs \((i<j)\) with \(A_i = x\), \(A_j \neq x\).  

We can compute \(P[x]\) efficiently: for each \(x\), let \(S[x]\) be the frequency and \(\text{pos\_sum}[x]\) the sum of 1-based indices where \(A_i = x\). Then  
\(P[x] = \text{pos\_sum}[x] - S[x] - \binom{S[x]}{2}\) (since pairs of \(x\)’s are excluded).  
\(Q[x] = S[x] (N - S[x]) - P[x]\), and \(\Delta[x] = 2P[x] - S[x](N-S[x])\).  

The answer for \(k=0\) is the ordinary inversion count of \(A\), computed with a Fenwick tree in \(O(N \log M)\).  
Then we iterate \(k = 1 \dots M-1\): the wrapped value at the previous step was \(x = (M - k) \bmod M\), so  
\(\text{ans}[k] = \text{ans}[k-1] + \Delta[(M-k) \bmod M]\).  

Pitfalls:  
- Indices must be handled carefully (1-based for position sums).  
- Edge cases with \(S[x]=0\) give zero delta.  
- Use 64-bit (Python int is unlimited) to avoid overflow.

## worker: Read N, M and the array A from standard input, and
The solution computes the inversion count for \(k=0\) using a Fenwick tree (BIT) over the values \(0 \dots M-1\) in \(O(N \log M)\).  
For each value \(x\), it precomputes the change in inversion count \(\Delta[x]\) that occurs when the elements equal to \(x\) wrap from \(M-1\) to \(0\). This uses the frequency \(S[x]\) and the sum of 1-based positions `pos_sum[x]`, giving the number of pairs where a non-\(x\) element appears before an \(x\) element.  
The answers for \(k \ge 1\) are obtained by accumulating these deltas in the order in which the wrapped value cycles: \(x = (M-1, M-2, \dots, 0)\), which corresponds to index \((M-k) \bmod M\) for the transition from \(k-1\) to \(k\).  
Total complexity is \(O((N+M)\log M)\) and fits easily in the given limits.
