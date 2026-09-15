
## ideation
The core difficulty is that the number of completions is exponential in the number of zero entries, while `p` can be as large as `10^9`, so neither enumeration nor per-completion matrix exponentiation is possible. The key structure is that all computations are over the finite field `F_p`, and the sum is over all nonzero values for each zero variable.

Let the zero positions be variables `x_e`, so `B = A + sum_e x_e E_e`, where `E_e` is the matrix unit at a zero position. Each entry of `B^p` is a polynomial of total degree at most `p` in these variables. When summing over all `x_e in F_p^*`, a monomial survives only if every variable exponent is a multiple of `p-1`, because `sum_{x in F_p^*} x^k = -1` if `(p-1) | k`, and `0` otherwise. For odd `p`, since the total variable degree is at most `p`, the only surviving monomials are:
- the constant term, which is `A^p`;
- monomials of the form `x_e^(p-1)` for a single zero variable.

Each surviving term contributes a factor `(-1)^K`, where `K` is the number of zeros. Thus the odd-prime answer should be `(-1)^K` times `A^p` plus the sum of the coefficients of `x_e^(p-1)` in `(A + x_e E_e)^p` over all zero positions.

The coefficient of `x_e^(p-1)` comes from products with exactly `p-1` copies of the matrix unit `E_e` and exactly one copy of `A`. This makes the correction very sparse:
- If the zero is diagonal, `E_e` is idempotent, and the coefficient reduces to row/column contributions from `A`, with the diagonal entry canceling modulo `p`.
- If the zero is off-diagonal, `E_e` is nilpotent, so consecutive copies of `E_e` vanish. With only one `A` separating the `E_e` copies, this can only happen when `p = 3`, giving a single contribution from the opposite entry `A_{c,r}` at position `(r,c)`.

The case `p = 2` is exceptional because `F_2^* = {1}`. The survival rule based on multiples of `p-1 = 1` no longer filters monomials usefully; there is only one completion, obtained by replacing every zero with `1`, and its square modulo `2` can be computed directly.

Main pitfalls to watch:
- `p = 2` must not be handled by the odd-prime monomial-filtering formula.
- The global sign `(-1)^K` applies to both `A^p` and all corrections.
- Diagonal and off-diagonal zero positions behave differently.
- For off-diagonal zeros, corrections exist only for `p = 3`.
- Matrix exponentiation `A^p mod p` must be efficient for `N <= 100` and `p <= 10^9`.
- Modular multiplication and summation can become slow if not optimized, especially in Python.
- Defensive handling of invalid or edge-case `p = 1` may be useful, although the statement says `p` is prime.
