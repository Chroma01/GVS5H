
## ideation
The core difficulty is aggregating powers of all subarray sums without enumerating the \(O(N^2)\) subarrays. Writing each subarray sum as a difference of prefix sums gives \(P_r-P_j\), where \(0\le j<r\). Since \(K\le 10\), the binomial expansion has only \(K+1\) terms, allowing low-degree moment sums to be maintained efficiently. All arithmetic must be performed modulo \(998244353\), including handling the alternating signs in the expansion.

Potential pitfalls include using the prefix \(P_r\) itself as a previous prefix before querying it, forgetting that \(P_0=0\) must be included, and incorrectly treating negative terms without reducing modulo the modulus.

## worker: Derive and implement the \(O(NK)\) prefix-moment a
For each right endpoint \(r\), every subarray ending at \(r\) has sum \(P_r-P_j\) for some \(0 \le j<r\). Expanding by the binomial theorem:

\[
(P_r-P_j)^K
=
\sum_{t=0}^{K}
\binom{K}{t}P_r^{K-t}(-1)^tP_j^t.
\]

The algorithm maintains `moments[t] = sum(P_j^t)` over all previously inserted prefixes. The current prefix is queried before insertion, ensuring only \(j<r\) are included. Each endpoint takes \(O(K)\) time, for total \(O(NK)\) time and \(O(K)\) memory.
