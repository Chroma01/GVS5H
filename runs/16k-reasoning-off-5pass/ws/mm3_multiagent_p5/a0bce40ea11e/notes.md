
## ideation
The key insight is Fermat's little theorem / Frobenius: for any matrix B over Z/pZ, B^p ≡ B (mod p). Thus the required sum modulo p is simply the sum of B over all completions.

Each completion assigns each zero of A a value from {1,…,p−1} independently. Let K be the number of zeros and Z = (p−1)^K the number of completions.

For an entry (i,j):
- If A[i][j] ≠ 0, it appears in every B → contributes A[i][j]·Z.
- If A[i][j] = 0, sum over x∈{1,…,p−1} of x = (p−1)p/2, times (p−1)^(K−1) completions for the remaining zeros → (p−1)p/2·(p−1)^(K−1) = Z·p/2, which is 0 mod p.

Since p is prime, (p−1) ≡ −1 (mod p), so Z ≡ (−1)^K (mod p).

Hence the answer for cell (i,j) is:
- A[i][j] · (−1)^K (mod p) if A[i][j] ≠ 0,
- 0 otherwise.

## worker: finalize
We rely on Fermat's little theorem: for any matrix $B$ over $\mathbb{F}_p$, $B^p \equiv B \pmod{p}$. So the required sum modulo $p$ equals $\sum_B B$.

For a fixed cell $(i,j)$:
- If $A_{i,j}\neq 0$, the entry is $A_{i,j}$ in every completion, so its total contribution is $A_{i,j}\cdot (p-1)^K$.
- If $A_{i,j}=0$, the sum over all completions is $\big(\sum_{x=1}^{p-1} x\big)\cdot (p-1)^{K-1} = \frac{(p-1)p}{2}\cdot (p-1)^{K-1}$, which is $0$ modulo $p$.

Modulo $p$, $(p-1)^K \equiv (-1)^K$. Therefore:
- For nonzeros: output $A_{i,j}\cdot (-1)^K \bmod p$.
- For zeros: output $0$.

Edge cases handled: $p=2$ (works since $1$ is the only nonzero), $K=0$ (all entries fixed, answer is just $A$ since $(-1)^0=1$).
