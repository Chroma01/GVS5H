- **Linearity of counting:** For each unordered pair of distinct grid cells, every valid arrangement containing both cells contributes exactly that pair's Manhattan distance once. The remaining k - 2 pieces can be placed in C(mn - 2, k - 2) ways, so the total answer is C(mn - 2, k - 2) times the sum of Manhattan distances over all unordered cell pairs.

- **Manhattan separation:** The total cell-pair distance sum separates into row and column components. For the row component, fix two distinct rows at distance d. The two cells may independently choose any of the n columns, giving n^2 unordered cell pairs for that row pair. Summing d over all row pairs gives sum_{d=1}^{m-1} d(m - d) = m(m^2 - 1) / 6. Therefore the row contribution is n^2 * m(m^2 - 1) / 6.

- **Column component:** By symmetry, the column contribution is m^2 * n(n^2 - 1) / 6. The earlier plan's factors of n and m undercount; the correct factors are n^2 and m^2. The 2x2, k=2 example confirms this: the formula gives 8.

- **Final formula:** answer = C(mn - 2, k - 2) * (n^2 * sum1d(m) + m^2 * sum1d(n)) modulo 1e9 + 7, where sum1d(L) = L(L^2 - 1) / 6.

- **Modular arithmetic:** Since MOD is prime and 6 is invertible modulo MOD, compute division by 6 using inv6 = pow(6, MOD - 2, MOD). Factorials and inverse factorials are precomputed up to mn, which is at most 1e5, so all binomial coefficients are computed safely modulo MOD.

- **Edge cases:** mn = 2 works because C(0, 0) = 1. If m = 1 or n = 1, the corresponding one-dimensional sum is zero. k = 2 gives C(mn - 2, 0) = 1, and k = mn gives C(mn - 2, mn - 2) = 1.

- **Verification:** m = 2, n = 2, k = 2 gives 8. m = 1, n = 4, k = 3 gives C(2, 1) * 10 = 20. Small brute-force enumeration over all cell subsets matches the formula for small m, n, and k, including k = 2 and k = mn.

- **Complexity:** Precomputing factorials takes O(mn) time and O(mn) memory. The geometric sum is O(1). This is well within the constraints because mn <= 1e5.
