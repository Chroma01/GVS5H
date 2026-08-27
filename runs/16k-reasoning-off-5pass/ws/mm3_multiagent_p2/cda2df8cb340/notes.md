
## ideation
We need to compute `S = sum_{1 ≤ i ≤ j ≤ N} f(A_i + A_j)` where `f(x)` is the odd part of `x` (divide by 2 until odd). N up to 2e5, A_i up to 1e7.

Key observations:
- `f(x) = x / 2^{v2(x)}` where `v2(x)` is the exponent of 2 in `x`.
- Let `T_t = sum_{i≤j, 2^t | (A_i+A_j)} (A_i+A_j)`. Then `Answer = T_0 - sum_{t≥1} T_t / 2^t`.
- `T_0 = (N+1) * sum_A` (each element appears N+1 times).
- For `t≥1`, split `T_t` into diagonal (`i=j`) and off-diagonal (`i<j`).
  - Diagonal: `2 * sum_{i: 2^{t-1} | A_i} A_i`. Precompute `v2(A_i)` to get this quickly via suffix sums.
  - Off-diagonal: pairs `(i,j)` with `i<j` and `A_i + A_j ≡ 0 (mod 2^t)`.
- For off-diagonal, group by residue `r = A_i mod 2^t`. For each `r`, we need matching residue `r2 = (2^t - r) mod 2^t`.
  - If `r < r2`: contribution = `sum_r * cnt_{r2} + cnt_r * sum_{r2}`.
  - If `r == r2`: contribution = `(cnt_r - 1) * sum_r`.
  - If `r > r2`: skip (handled when processing `r2`).
- This can be computed in O(N) per `t` using a hash map from residue to (count, sum). With `t` up to ~24, total O(N log max) ≈ 5e6, which is fast.

Pitfalls:
- Integer division by 2: use `T_t >> t` since `2^t` divides `T_t`.
- Stop iterating `t` when `2^t > 2 * max_A` (no sums can be multiples of such large `2^t`).
- Watch out for large numbers: use Python's arbitrary integers or ensure 64-bit (Python int is fine).
- Diagonal condition: for `t=1`, need `2^{0}=1 | A_i` (always true). For `t≥1`, need `2^{t-1} | A_i`.

## worker: Implement the full solution in Python: read input,
- Implemented using the formula `Answer = T_0 - Σ_{t≥1} T_t / 2^t`.
- `T_0 = (N+1) * sum(A)` because each element appears `N+1` times in the sum of `A_i + A_j` over `i ≤ j`.
- Diagonal part for `t ≥ 1` uses precomputed `v2(A_i)` and suffix sums of values grouped by their `v2`.
- Off-diagonal part groups by residue mod `2^t` and uses the matching residue `-r mod 2^t`. The contribution formula `sum_r * cnt_{-r} + cnt_r * sum_{-r}` is correct for unordered pairs when `r < -r`; for `r == -r` we use `(cnt - 1) * sum`.
- Iterating `t` up to the largest power of two not exceeding `2 * max(A)` ensures no unnecessary work.
- Time complexity: O(N * log(max(A))) ≈ 5×10⁶ operations for the given limits, well within time limits.
