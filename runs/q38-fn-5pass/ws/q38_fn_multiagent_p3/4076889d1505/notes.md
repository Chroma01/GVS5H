- **Construction:** For each test case, output `A = N + 1` and `M = N * N`. For `N = 1`, this outputs `2 1`, which is valid because every positive integer `n` satisfies `1 | 2^n - 1`, so the smallest such `n` is `1`.
- **Bounds:** Since `1 <= N <= 10^9`, we have `A = N + 1 <= 10^9 + 1 <= 10^18` and `M = N^2 <= 10^18`. Also `gcd(A, M) = gcd(N + 1, N^2) = 1`.
- **Core proof idea:** We need the smallest positive `n` such that `N^2 | (N + 1)^n - 1` to be exactly `N`. This is equivalent to requiring, for every prime power `p^e || N`, that `p^{2e} | (N + 1)^n - 1` if and only if `p^e | n`.
- **Odd prime powers:** Let `p` be odd and `p^e || N`. Since `p | (N + 1) - 1` and `p` does not divide `(N + 1) * 1`, LTE gives  
  `v_p((N + 1)^n - 1) = v_p(N) + v_p(n) = e + v_p(n)`.  
  Therefore `p^{2e}` divides `(N + 1)^n - 1` exactly when `v_p(n) >= e`, i.e. `p^e | n`.
- **Power of two, `e = 1`:** If `N` is even but not divisible by `4`, then `v_2(N) = 1`. For odd `n`, `v_2((N + 1)^n - 1) = v_2(N) = 1`, which is less than `2`. For even `n`, LTE gives  
  `v_2((N + 1)^n - 1) = v_2(N) + v_2(N + 2) + v_2(n) - 1`.  
  Here `N + 2` is divisible by `4`, so this is at least `3`, hence at least `2`. Thus the condition is exactly that `n` is even, i.e. `2 | n`.
- **Power of two, `e >= 2`:** If `4 | N`, then `v_2(N) = e >= 2` and `v_2(N + 2) = 1`. For odd `n`, `v_2((N + 1)^n - 1) = e < 2e`, so it fails. For even `n`, LTE gives  
  `v_2((N + 1)^n - 1) = e + 1 + v_2(n) - 1 = e + v_2(n)`.  
  Therefore `2^{2e}` divides `(N + 1)^n - 1` exactly when `v_2(n) >= e`, i.e. `2^e | n`.
- **Combining prime powers:** The divisibility `N^2 | (N + 1)^n - 1` holds exactly when every prime power `p^e || N` divides `n`, which is equivalent to `N | n`. Hence the smallest positive such `n` is `N`.
- **Complexity:** The implementation is `O(T)` time and `O(T)` output storage, with no factorization or modular exponentiation needed.
- **Implementation details:** Read all input at once, parse `T`, then for each `N` print `N + 1` and `N * N`. Python's arbitrary-precision integers safely handle `N^2` up to `10^18`.
