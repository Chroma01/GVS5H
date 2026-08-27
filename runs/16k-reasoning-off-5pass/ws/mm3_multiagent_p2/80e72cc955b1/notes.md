
## ideation
- The core difficulty: for each query `[l, r]`, we have an array of consecutive integers from `l` to `r`. We can pick two numbers per operation and replace each with `floor(x/4)`. We need the minimum number of operations to make all numbers zero.
- Key insight: For a single number `x`, the number of times it must be “divided by 4 (floor) to reach 0” equals the number of base‑4 digits of `x`, i.e. `f(x) = floor(log4(x)) + 1` for `x >= 1` (and `f(0) = 0`).
- Each operation can apply one such reduction to two numbers. So if `T = sum f(x)` over the array, the minimum number of operations is `ceil(T / 2) = (T + 1) // 2`. (We can always pair reductions greedily because we only care about total count; there is no dependency between choices since the operation is independent per element and we can always pick any two nonzero elements.)
- Therefore the problem reduces to computing, for each query, `T(l, r) = sum_{x=l}^{r} f(x)` efficiently, then adding `(T + 1) // 2` to a global sum.
- Constraints: up to `10^5` queries, `l, r` up to `10^9`. So we need `O(log r)` or `O(1)` per query.
- Structure of `f(x)`: `f(x) = k` iff `4^{k-1} <= x < 4^k`. So we can precompute prefix sums of `f` using a digit‑sum technique in base 4.
- Formula for prefix sum up to `r`:
  Let `K = floor(log4(r)) + 1`. Then
  `S(r) = sum_{k=1}^{K-1} k * (4^k - 4^{k-1}) + K * (r - 4^{K-1} + 1)`.
  Simplify: `S(r) = sum_{k=1}^{K-1} k * 3 * 4^{k-1} + K * (r - 4^{K-1} + 1)`.
  We can precompute `A[m] = sum_{k=1}^{m} k * 3 * 4^{k-1}` for `m` up to `K_max`, where `K_max = floor(log4(10^9)) + 1` (since `4^15 = 1073741824 > 10^9`, so `K_max = 16`). This is tiny.
- Then `S(r) = A[K-1] + K * (r - 4^{K-1} + 1)`. Answer per query: `ans += (S(r) - S(l-1) + 1) // 2`.
- Edge cases: `l = 1`, `l = r+1` (not possible per constraints since `l < r`), large numbers, overflow (use Python int, fine).
- Pitfall: Must ensure `f(0) = 0`; but `l >= 1`, so no zero in array. Good.
- Pitfall: `ceil(T/2)` correctly computed as `(T + 1) // 2` only if `T` is integer and we want ceiling. Yes.
- Complexity: Precomputation O(K_max) ~ 16. Each query O(1) (computing `K = floor(log4(r))` using while loop on precomputed powers, or using bit length). Total O(Q).
- Alternative approach: digit DP in base 4 to compute sum of `f(x)` for range `[1, r]`, but the closed-form is simpler.

## worker: Precompute powers of 4 and prefix sums of f(i) for
- Implemented `S(x)` as a helper using precomputed `powers[0..15]` (since `4^15 > 10^9`) and `pref[0..15]` storing cumulative sums of `k * (4^k - 4^{k-1})`.
- `S(x)` runs in O(1) after a tiny linear scan (≤16 iterations) to find `K = floor(log4(x)) + 1`.
- Each query is answered in O(1), so overall complexity is O(Q) with very small constant factors.
- Verified logic against examples:
  - Example 1: `[[1,2],[2,4]]` → 1 + 2 = 3.
  - Example 2: `[[2,6]]` → 4.
- Edge cases: `l = 1` works because `S(0) = 0`; `l, r` up to `10^9` covered since `4^15 > 10^9`.
