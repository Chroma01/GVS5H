
## ideation
**Core difficulty:**
We need to compute  
\( S = \sum_{1\le l\le r\le N} \left(\sum_{i=l}^r A_i\right)^K \pmod{M} \)  
with \( N\le 2\cdot10^5 \), \( K\le 10 \), \( M=998244353 \).  
A naive double loop is O(N²) and impossible. The sum of K-th powers of subarray sums must be computed in roughly O(N·K) or similar.

**Key observation – prefix sums:**
Let \( S_0 = 0 \), \( S_i = \sum_{k=1}^i A_k \) for \( i=1..N \).  
For any subarray \( [l, r] \), the sum is \( S_r - S_{l-1} \). Thus
\[
S = \sum_{0\le i < j \le N} (S_j - S_i)^K .
\]
(The term \( i=j \) gives 0 anyway because \( K\ge 1 \).)

**Binomial expansion trick:**
\[
(S_j - S_i)^K = \sum_{t=0}^K \binom{K}{t} S_j^t (-S_i)^{K-t}.
\]
Therefore
\[
S = \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \sum_{j=0}^N S_j^t \left(\sum_{i=0}^{j-1} S_i^{K-t}\right).
\]

**Prefix accumulation O(N·K):**
- Precompute all powers \( S_i^p \) for \( p=0..K \) in O(N·K) (fast exponentiation or iterative multiplication by \( S_i \)).
- Precompute binomial coefficients \( \binom{K}{t} \) mod M.
- For each \( j = 0..N \), maintain a running array `pref[p] = sum_{i=0}^{j-1} S_i^p` for all p.
- For each j, add to answer:
  \[
  \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_j^t \cdot \text{pref}[K-t].
  \]
  Then update `pref[p] += S_j^p`.

Overall O(N·K) = 2·10⁶ operations, easily feasible.

**Pitfalls / Edge Cases:**
- Modulo M must be applied after every operation (binomial coefficients, powers, additions).
- Use `pow` carefully (avoid O(log K) per call → precompute once).
- \( S_0 = 0 \), so the term j=0 contributes nothing (pref[·] are all 0 initially), consistent.
- K=0 is not allowed by constraints (K≥1), but the code can handle it anyway (sum would be number of subarrays).
- Negative sign: multiply by `(-1)**(K-t)`; compute as `1` or `M-1`.
- Since M is prime, we could use Fermat inverses if we needed division; here only multiplication and addition needed (no division). Good.
- Precomputing powers: keep array `powS[j][p]` (size (N+1)×(K+1)) may be memory heavy: 2e5×11 ≈ 2.2M integers → ~8 MB, acceptable. Or compute on the fly iteratively.

**Alternative approaches (not needed but considered):**
- DP over subarrays ending at i: also O(N·K), but the prefix-sum + binomial expansion is simpler to implement and clearly correct.
- FFT / convolution: would be O(N log N) but unnecessary for K≤10.

**Plan summary:**
1. Read N, K, array A.
2. Compute prefix sums S[0..N].
3. Precompute binomial coefficients `C[t]` for t=0..K.
4. Precompute for each j the powers `P[j][p] = S[j]^p` for p=0..K.
5. Initialize `pref[p] = 0` for p=0..K.
6. Loop j from 0 to N:
   - For t from 0 to K:
       - term = C[t] * ((-1)**(K-t) mod M) mod M
       - term = term * P[j][t] % M
       - term = term * pref[K-t] % M
       - add to answer.
   - Then for p from 0 to K: `pref[p] = (pref[p] + P[j][p]) % M`.
7. Output answer.

**Complexity:**
- Time: O(N·K) ≈ 2·10⁶ operations.
- Memory: O(N·K) for powers + O(K) for prefix → < 100 MB (fine).

## worker: Implement the solution in Python: read input, comp
The solution uses the prefix-sum transformation to convert the sum over all subarrays into a sum over pairs of prefix sums: \(S = \sum_{0\le i < j \le N} (S_j - S_i)^K\). Expanding the K‑th power binomially and swapping the order of summation yields a double sum that can be evaluated in a single left‑to‑right sweep by maintaining the running sums of the powers of the earlier prefix values. The algorithm runs in \(O(N \cdot K)\) time (≈ 2·10⁶ operations for the limits) and uses \(O(N \cdot K)\) memory for the precomputed powers, which is well within the limits for Python.

Key details:
- Modulus 998244353 is prime; no division is required, only multiplication and addition.
- Binomial coefficients are computed exactly with `math.comb` (since K ≤ 10) and taken modulo MOD.
- The sign \((-1)^{K-t}\) is handled as `1` or `MOD-1`.
- `S_0 = 0` is included, and its contribution correctly vanishes because `pref` starts at zero.
- The algorithm correctly produces the sample outputs: 75, 0, and 428633385.
