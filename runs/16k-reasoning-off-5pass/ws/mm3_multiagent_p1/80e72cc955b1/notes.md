
## ideation
The problem reduces to: each number `x` needs `f(x) = ⌊log₄(x)⌋ + 1` division-by-4 steps to reach 0. Each operation can advance at most 2 numbers by one step. The minimum number of operations is `max(⌈total_steps / 2⌉, max_per_element_steps)`.

The key insight: `f(x)` is piecewise constant over intervals `[4^k, 4^{k+1} - 1]`. Since `4^15 ≈ 10^9`, there are only ~16 distinct levels. For each query `[l, r]`, decompose the range into `O(log r)` contiguous blocks of constant `f`, and sum using arithmetic/geometric formulas.

For each query:
1. `max_steps = f(r)` (since `r` is the largest number, and `f` is non-decreasing).
2. `total_steps = Σ f(x)` over `x ∈ [l, r]` via block decomposition.
3. Answer = `max((total_steps + 1) // 2, max_steps)`.

Block decomposition: start from `l`, find `k` such that `4^k ≤ l < 4^{k+1}`, block is `[l, min(4^{k+1}-1, r)]`, contribution is `(block_len) * (k+1)`. Advance to `min(4^{k+1}-1, r) + 1` and repeat.

With 10^5 queries and ~16 blocks each, this is O(10^5 × 16) = fast.

## worker: Implement the `Solution.minOperations` method with
The solution implements the key insight: each number `x` requires `f(x) = ⌊log₄(x)⌋ + 1` division-by-4 steps to reach zero. Since each operation can advance at most 2 numbers by one step, the minimum number of operations is `max(⌈total_steps / 2⌉, max_steps)`.

- **`f(x)`** uses binary search on precomputed `pow4` array: `bisect_right(pow4, x)` gives the smallest `k` such that `4^k > x`, which equals the number of steps needed.
- **`sum_f(l, r)`** decomposes `[l, r]` into contiguous blocks where `f` is constant. Each block corresponds to a power-of-4 interval `[4^k, 4^{k+1}-1]`, contributing `count * (k+1)` to the sum. With at most ~16 blocks per query, this is very fast.
- The final answer for each query is `max((total_steps + 1) // 2, f(r))`, and we sum across all queries.
- Time complexity: `O(Q * log log(max_val))` ≈ `O(10^5 * 16)`, well within limits.
- Edge cases: `l >= 1` per constraints, so no need to handle `f(0)` in `sum_f`; `f(0)=0` is defined for safety.
