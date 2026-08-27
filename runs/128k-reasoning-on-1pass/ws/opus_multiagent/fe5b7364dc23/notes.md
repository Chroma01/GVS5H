
## ideation
**Restatement / core idea.** With prefix sums `S_0 = 0`, `S_r = A_1+…+A_r (mod p)`, the target is
`Σ_{1≤l≤r≤N} (S_r − S_{l−1})^K = Σ_{r=1}^{N} Σ_{j=0}^{K} C(K,j)(−1)^{K−j} S_r^j · (Σ_{p=0}^{r−1} S_p^{K−j})`.
So we only need, for each exponent m = 0..K, the running (exclusive) prefix sums `T_m(r) = Σ_{p<r} S_p^m`. That's O(N·K) work — mathematically trivial; **the real difficulty is constant-factor speed in Python**, ~2×10⁵ × 11 power computations plus ~2×10⁵ × 11 multiply-accumulates ≈ 4–5×10⁶ modmuls, which in pure CPython can run 3–6 s.

**Key correctness details / pitfalls.**
- `S_0 = 0` must be included in the T arrays (it handles l = 1), and the m = 0 power of it must be **1** (0⁰ = 1 convention). If powers are computed by `pow(S,0)` that's fine, but a naive `S**m` loop or `np.power` on zeros still gives 1 for m=0 — just make the m=0 array explicitly all-ones.
- Sign: `(−1)^{K−j}` — accumulate with `+`/`−` then take a final `% p` (Python handles negatives fine; in numpy add `p` before mod).
- `A_i` can be 0 and up to p−1; reduce prefix sums mod p at every step.
- K=1 and N=1 must work (answer for N=1 is A_1^K).
- Read input with `sys.stdin.buffer.read().split()`.

**Numpy vectorization (preferred) — overflow analysis.**
- `np.cumsum` of the raw `A` (each < 2³⁰, N ≤ 2×10⁵) reaches ≤ 2×10⁵·2³⁰ ≈ 2.1×10¹⁴ < 2⁶³ ⇒ safe in int64, then `% p`.
- Power arrays: multiply two reduced values (< 2³⁰) ⇒ < 2⁶⁰, safe, then `% p` each step.
- Prefix sums of a power array: entries < 2³⁰, cumsum ≤ 2×10⁵·2³⁰ ≈ 2¹⁴·2³⁰ = 2⁴⁴ ⇒ safe; mod afterwards.
- Dot product `Σ_r P_j[r]·T_{K−j}[r]`: must reduce **after the elementwise multiply** (`(x*y) % p`) before `.sum()`, otherwise summing 2×10⁵ values of size 2⁶⁰ overflows. Even better: `.sum()` on reduced values ≤ 2⁴⁴, safe; then `% p`.
- Total: only ~(K+1) power arrays + (K+1) cumsums + (K+1) dot products = ~30 numpy passes over 2×10⁵ elements ⇒ milliseconds.

**Pure-Python fallback.** Single sweep r = 1..N: maintain list `T[0..K]`; before using r, fold `S_{r−1}` powers into T (reuse the powers list computed in the previous iteration so each S needs only K multiplications total). Unroll/precompute `C(K,j)(−1)^{K−j} mod p` coefficients outside the loop. Should be acceptable but is the risky path timing-wise.

**Alternatives (probably unnecessary).** Divide-and-conquer / generating-function (EGF: Σ e^{S_r x} · Σ e^{−S_p x} truncated at degree K) is the same binomial identity in disguise; no asymptotic gain. Don't bother with NTT.

**Sanity check to reason through (not to run):** N=3, K=2, A=(3,1,2): S = 0,3,4,6. Formula gives 75.

## worker: Write the complete numpy-based solution: read inpu
- Implemented the binomial-expansion approach: answer = Σ_{r=1..N} Σ_{j=0..K} C(K,j)(−1)^{K−j} S_r^j · (Σ_{q=0}^{r−1} S_q^{K−j}).
- Index alignment: `T[m] = cumsum(P[m]) % p` so `T[m][r-1] = Σ_{q=0}^{r-1} P[m][q]`; aligning `T[m][:-1]` (indices 0..N−1, i.e. r=1..N) with `P[j][1:]` (S_r for r=1..N) is exactly right. S_0=0 is included, handling l=1, and P[0][0]=1 encodes 0⁰=1 as required.
- Overflow safety (int64): A_i < p < 2³⁰; cumsum of A ≤ 2×10⁵·2³⁰ ≈ 2.1×10¹⁴ < 2⁶³. Power arrays multiply two reduced values (<2³⁰ each → <2⁶⁰) then reduce. Cumsum of reduced power array ≤ 2×10⁵·2³⁰ ≈ 2⁴⁴. Dot products reduce elementwise before `.sum()`, so the sum ≤ 2⁴⁴ — all safe.
- Signs are folded into precomputed coefficients mod p; final result printed non-negative.
- Manual check N=3,K=2,A=(3,1,2): S=(0,3,4,6); expansion gives Σ (S_r−S_{l−1})² = 9+1+4+16+9+36 = 75. ✔
- Edge cases: N=1 (single term A_1^K), K=1, A_i=0 (P[0] explicitly ones), A_i up to p−1 (reduced immediately).
- Added a pure-Python fallback (only used if numpy import fails) that reuses the previous iteration's power list logic; the numpy path is the primary one and runs in milliseconds.
