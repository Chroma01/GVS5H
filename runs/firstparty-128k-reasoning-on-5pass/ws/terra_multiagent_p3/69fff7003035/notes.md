- **Formula:** Assign independent continuous random priorities to all values. For a fixed value `x`, another value `y` is after `x` exactly when its priority is larger. Conditioning on `x`'s priority `t`, its expected place-value factor is `product_{y != x} (1 + t(10^{len(y)} - 1))`. Integrating `t` from `0` to `1` and multiplying by `N!` gives the permutation sum.
- **Digit grouping:** Let `b_d = 10^d - 1`, and let `c_d` be the count of numbers in `1..N` having `d` digits. Define `P(t) = product_d (1 + b_d t)^{c_d}`. For every number with digit length `d`, the needed integrand is `P(t) / (1 + b_d t)`.
- **Polynomial recurrence:** Let `D(t) = product_d (1 + b_d t)` and `A(t) = sum_d c_d b_d D(t)/(1+b_d t)`. Since `D P' = A P`, coefficients of `P` can be computed with an order-`#digits` recurrence:
  `n p_n = sum_j A_j p_{n-1-j} - sum_{j>=1} D_j (n-j) p_{n-j}`.
  This computes all degree-`N` coefficients in `O(N * #digits)`.
- **Exclusion polynomial:** For each digit class, divide `P(t)` by `1+b t` using `q_0=1`, `q_k=p_k-b q_{k-1}`. Its integral over `[0,1]` is `sum_k q_k/(k+1)`. All divisions are modular inverses, valid because `N < 998244353`.
- **Complexity:** There are at most six digit classes for the constraints. Runtime is `O(N * #digits)` and memory is `O(N)`.
