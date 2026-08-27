
## ideation
The core difficulty: counting numbers in [l, r] where `product_of_digits % sum_of_digits == 0`, with r up to 10^9 (9 digits). A naive check per number is fine for small ranges, but here we need an efficient method. Since 10^9 is only 9 digits, digit DP is the natural approach.

Key insight that simplifies everything: **if the number contains the digit 0, the product is 0, and 0 is divisible by any positive sum**. So every number with at least one zero digit is automatically beautiful. This dramatically prunes the search — we don't need to track product carefully for those.

For numbers with no zero digit: product is at most 9^9 ≈ 387 million (fits in 64-bit int), and sum is at most 81. So we can track both directly. At the leaf, check `sum != 0 and product % sum == 0`.

State for the DP: `(pos, tight, started, sum, product, has_zero)`. But `has_zero` is redundant with `product == 0 and started` — actually cleaner to track it explicitly. When `has_zero` is True, we can skip the final divisibility check (count everything as beautiful).

We answer `f(r) - f(l-1)` where `f(X)` counts beautiful numbers in [1, X].

Pitfalls:
- Leading zeros: they shouldn't count as the digit 0 for the "has zero" check, nor contribute to sum/product. Use a `started` flag.
- Edge case: single-digit numbers 1–9 have no zero, sum = product, so product % sum == 0 always. Matches the example.
- `l = 1` case: `f(0)` must return 0.

## worker: Implement the `beautifulNumbers` method in the `So
- Implemented a memoized digit-DP `count(x)` that counts beautiful numbers in `[1, x]`.
- State: `(pos, tight, started, sum_, prod, has_zero)`.
- Leading zeros are handled via `started` flag; they don't contribute to sum/product and don't trigger the zero-digit shortcut.
- When `has_zero` becomes True, product is set to 0 and we skip the divisibility check at the leaf (since 0 is divisible by any positive sum).
- For numbers without any zero digit, product is at most `9^9 ≈ 3.87e8` (fits easily in Python int), and sum ≤ 81.
- The answer is `count(r) - count(l-1)`, with `count(0) = 0` handled by the early return.
- Verified mentally against examples:
  - `l=10, r=20`: numbers 10 and 20 have a zero digit → both beautiful → count = 2. ✓
  - `l=1, r=15`: 1–9 all beautiful (sum==product), plus 10 (has zero) → 10 total. ✓
