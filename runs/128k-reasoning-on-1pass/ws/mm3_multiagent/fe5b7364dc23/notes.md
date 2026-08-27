
## ideation
- **Core difficulty** – Compute  
  \[
  \sum_{1\le l\le r\le N}\Bigl(\sum_{i=l}^{r}A_i\Bigr)^K
  \]
  efficiently.  
  Direct enumeration of all sub‑arrays is \(O(N^2)\), too slow for \(N\le2\cdot10^5\).  
  The exponent \(K\) is tiny (\(\le10\)), which suggests using algebraic expansions rather than complicated data structures.

- **Candidate approaches**  
  1. **Prefix sums + binomial theorem** –  
     Let \(S_0=0\) and \(S_i=\sum_{t=1}^{i}A_t\).  
     Then the sub‑array sum equals \(S_r-S_{l-1}\).  
     The whole sum becomes  
     \[
     \sum_{0\le i<j\le N}(S_j-S_i)^K.
     \]  
     Expand \((S_j-S_i)^K\) with the binomial theorem, giving a sum of terms
     \(\text{coeff}[t]\,S_j^t\,S_i^{K-t}\).  
     By scanning \(j\) from \(1\) to \(N\) and maintaining
     \(\displaystyle \text{acc}[e]=\sum_{i<j}S_i^e\) we can add the contribution
     of the current \(j\) in \(O(K)\) time. Total complexity \(O(NK)\).

  2. **Generating functions / convolution** –  
     Could view the sum as a convolution of powers of the prefix sums, but
     the above linear scan is simpler and fast enough.

  3. **Heavy data structures (e.g., segment trees with polynomial
     multiplication)** – Not needed because \(K\le10\).

- **Pitfalls to watch**  
  - **Modulo handling** – All operations must be performed modulo
    \(P=998244353\). Negative coefficients from the binomial expansion
    must be reduced to the range \([0,P-1]\).
  - **Including the empty prefix** – \(S_0=0\) must be part of the sum; it
    contributes to sub‑arrays that start at index 1.
  - **Zero‑based vs one‑based indices** – Use 0‑based internally for
    Python arrays, but be careful when indexing the prefix array.
  - **Edge cases** – \(N=1\), \(K\) up to 10, all \(A_i=0\). The algorithm
    naturally yields 0.
  - **Pre‑computation of binomial coefficients** – Compute factorials and
    inverse factorials up to \(K\) to obtain \(\binom{K}{t}\) quickly.
  - **Power computation** – For each \(j\) we need \(S_j^0,\dots,S_j^K\);
    recomputing them by successive multiplication costs only \(O(K)\).

## worker: finalize
- **Prefix sums** – let `S_0 = 0` and `S_i = A_1 + … + A_i`.  
  Then any sub‑array sum equals `S_r – S_{l-1}` and the required sum becomes  
  \(\displaystyle \sum_{0\le i<j\le N} (S_j - S_i)^K\).

- **Binomial expansion** –  
  \((S_j - S_i)^K = \sum_{t=0}^{K} \binom{K}{t} S_j^t (-S_i)^{K-t}
   = \sum_{t=0}^{K} (-1)^{K-t}\binom{K}{t} S_j^t S_i^{K-t}\).  
  Define `coeff[t] = (-1)^{K-t}·C(K,t) (mod MOD)`.

- **Scanning** – while moving `j` from `1` to `N` we keep  
  `acc[e] = Σ_{i<j} S_i^e`.  
  For the current `j` the contribution is  
  \(\displaystyle \sum_{t=0}^{K} coeff[t]·S_j^t·acc[K-t]\).  
  After adding it we update `acc` with `S_j`.  
  All operations are `O(K)`, total `O(N·K)`.

- **Complexity** –  
  Time: `O(N·K) ≤ 2·10⁶` elementary operations.  
  Memory: `O(N + K)` (prefix array and a few vectors of length `K+1`).

- **Correctness** – proved by Lemma 1 (binomial identity), Lemma 2 (maintaining the prefix sums of powers), Lemma 3 (contribution of a fixed `j`), and Lemma 4 (summing over all `j`). Together they show the algorithm returns exactly the required sum modulo `998244353`.
