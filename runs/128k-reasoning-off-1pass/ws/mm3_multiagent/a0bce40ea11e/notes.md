
## ideation
The core difficulty is computing the sum of \(B^p\) over all possible \(B\) (where zeros in \(A\) are replaced by nonzero values in \(\mathbb{F}_p\)) efficiently for \(N \le 100\) and prime \(p \le 10^9\). The key insight is that for each monomial in the expansion of \(B^p\), the sum over assignments factors into a product of sums \(\sum_{x \in \mathbb{F}_p^*} x^d\). This sum is \(-1 \pmod p\) iff \((p-1) \mid d\) (including \(d=0\)), and 0 otherwise. For \(p \ge 3\), total degree \(p\) forces surviving monomials to either avoid zeros entirely (Type A) or use exactly one zero position \(p-1\) times and one nonzero position once (Type B). The factor becomes \((-1)^K\) in both cases. Type A is simply \(M^p\) where \(M\) is \(A\) with zeros kept. Type B involves contributions from diagonal zeros (adding to rows/columns) and for \(p=3\) specific off-diagonal patterns. The case \(p=2\) requires separate handling because every monomial survives. Matrix exponentiation \(M^p\) is \(O(N^3 \log p)\), feasible with numpy.

## worker: Implement the solution in Python using numpy: read
The solution correctly handles all cases:
- For p=2, the sum reduces to (A')^2 mod 2 where A' replaces zeros with 1.
- For p≥3, the sum is (-1)^K × (M^p + D) mod p, where M is A with zeros, and D accounts for special paths using one zero p-1 times and one nonzero once.
- Diagonal zeros contribute to D by adding A values along their row/column.
- Off-diagonal zeros only contribute for p=3 (the specific case r→c→r→c path).
- The matrix exponentiation is done efficiently using numpy.
- Complexity: O(N^3 log p) for the exponentiation, which is fast for N=100 with numpy.

## worker: Test the solution with the provided sample inputs 
The solution was tested against the three sample inputs and produced the correct output for all of them. The key mathematical insight is that for \(p \geq 3\), the sum \(\sum_{x \in \mathbb{F}_p^*} x^d\) is \(-1 \pmod p\) when \((p-1) \mid d\) (including \(d=0\)), and 0 otherwise. This restricts the surviving monomials in the expansion of \(B^p\) to two types: those that avoid all zero positions (giving \(M^p\)) and those that use exactly one zero position \(p-1\) times and one nonzero position once (giving the correction matrix \(D\)). The overall factor is \((-1)^K\) from the zero positions. For \(p=2\), every monomial survives, so the answer is simply \((A')^2\) where \(A'\) has ones at zero positions. The matrix exponentiation is performed efficiently using numpy, handling the \(O(N^3 \log p)\) complexity well for \(N \leq 100\).
