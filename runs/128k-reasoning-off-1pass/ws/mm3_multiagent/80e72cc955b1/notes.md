
## ideation
**Core difficulty:** For each query `[l, r]`, we need the minimum number of *pairwise* operations of the form `(a,b) -> (⌊a/4⌋, ⌊b/4⌋)` to make all numbers in `[l, r]` zero.

**Key observations:**
1. The operation reduces two numbers by one "division step". The number of steps needed to reduce a positive integer `x` to 0 is `level(x) = floor(log4(x)) + 1` (the index of the highest base-4 digit). This is equivalent to counting the number of times you must apply `x = floor(x/4)` until reaching 0.
2. Since each operation simultaneously reduces the level of two selected numbers by exactly 1, the minimum number of operations equals `ceil(total_levels / 2)`, where `total_levels = Σ_{x=l}^{r} level(x)`. (Each operation can contribute at most 2 to the level reduction.)
3. Computing `Σ_{x=1}^{n} level(x)` efficiently is the main subproblem. The set `[1, n]` can be partitioned into blocks `[1]`, `[2,3,4]`, `[5,...,16]`, `[17,...,64]`, ... i.e., blocks of size `4^k` for `k=0,1,2,...`. In a block `[4^k + 1, 4^{k+1}]` (or the first one `[1]` with `k=0`), exactly `4^k / 4 = 4^{k-1}` numbers have level `k+1` (those divisible by 4, except the first), and the rest have lower levels. More cleanly, in the range `[4^k, 4^{k+1}-1]`, each level `0..k` appears exactly `4^{k-1}` times (with appropriate handling for k=0).
4. A standard approach: process full blocks of size `4^k` starting from 1, and for each such complete block, add `4^{k-1}` to the count for each level (or more simply, compute the total contribution of the block). A clean way: iterate k from 0 while `4^k ≤ n`, let `blockSize = 4^k`, `cnt = n // blockSize` full blocks, and `remainder = n % blockSize`. The `cnt` full blocks each contribute `blockSize / 4` to the sum of levels (for k≥1). Handle the remainder similarly by recursing or iterating.

**Pitfalls:**
- Off-by-one on the interval boundaries: the array is `[l, r]` inclusive, so sum = `sumLevels(r) - sumLevels(l-1)`.
- Special case `k=0`: a block of size 1 (number 1) has level 1, contribution 1, not `1/4`.
- Use 64-bit integers because the sum can be large: for `n ≈ 10^9`, `sumLevels(n)` ≈ n * log4(n) ≈ 1e9 * 15 ≈ 1.5e10, and the final result is up to ~1.5e10 per query, and sum over 1e5 queries could be 1e15, fits in Python int but must be careful in other languages.
- `ceil(total_levels / 2)` = `(total_levels + 1) // 2` in integer arithmetic.

**Candidate approaches:**
- **Approach A (math-based, O(log r) per query):** Precompute `sumLevels(n)` using the block decomposition in base 4. For each query, total = `sumLevels(r) - sumLevels(l-1)`, answer = `(total + 1) // 2`. This is optimal: O(log max(r)) per query, O(1) space.
- **Approach B (simulation/BFS):** Not feasible for r up to 1e9 and 1e5 queries.
- **Approach C (digit DP):** Possible but unnecessarily complex compared to the arithmetic block approach.

**Best approach:** A — arithmetic block decomposition in base 4.

## worker: Implement the `sum_levels(n)` function using the c
The `sum_levels` function computes the total number of division-by-4 steps needed to reduce all numbers in `[1, n]` to zero. For each number `x >= 1`, `level(x) = floor(log4(x)) + 1`. The numbers with level `k+1` are exactly those in `[4^k, 4^{k+1}-1]`, and there are `3 * 4^k` of them. The algorithm finds `K = floor(log4(n)) + 1`, sums the contributions of all full levels `1` through `K-1` using a loop, then adds the partial top level `K` for the remaining numbers in `[4^(K-1), n]`. The minimum operations per query is `ceil(total_levels / 2)` since each operation can reduce the level of two numbers by 1.
