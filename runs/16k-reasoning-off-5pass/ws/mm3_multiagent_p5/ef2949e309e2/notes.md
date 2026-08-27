
## ideation
The core difficulty: for each position `i` acting as middle, count pairs (2 left, 2 right) where `a = nums[i]` is the unique mode of the resulting 5-subsequence. With `x` = # of `a`'s picked from sides, `a`'s total count is `x+1`. Uniqueness requires every other value `v` to appear at most `x` times in the 4 chosen. This gives clean case splits by `x`:

- `x = 0`: impossible (need max count 0, but 4 non-`a` picked).
- `x = 1`: the 3 non-`a` chosen must all be distinct values.
- `x >= 2`: any pick of `4-x` non-`a` elements works (since `x+1 > 4-x`).

Key trick: when `x >= 2`, the non-`a` count constraint is automatically satisfied, so we just multiply combinations. The `x=1` case is the only tricky one, but it factors into sums over values `v != a` of `cl[v] * C(R'-cr[v], 2)` (and symmetric).

Naive O(n²) with hash maps per position is fine for n ≤ 1000.

## worker: Implement the O(n²) solution in Python: for each i
Implemented the O(n²) approach with case analysis on `x` (number of `a`'s picked from sides):
- `x = 0`: impossible (all non-`a`, can't have max count 0).
- `x = 1`: the 3 non-`a` elements must all be distinct values, handled via sums over other values `v`.
- `x >= 2`: automatic (since `x+1 > 4-x`), just multiply combinations of picking `a`'s and non-`a`'s.

For each position `i`, maintained a running `left_counter` and used `total_counter` to derive right counts. Iterated over all distinct values for the `x=1` case sums.

Complexity: O(n × distinct_values) per position, but with the prefix trick, overall O(n × V) where V is distinct values ≤ n, so O(n²) = 10⁶ for n=1000, feasible.

## worker: Verify the current implementation against all thre
Verified implementation against the three examples:
- `[1,1,1,1,1,1]` → 6 ✓ (only one subsequence value, middle is unique mode, formed in C(6,5)=6 ways)
- `[1,2,2,3,3,4]` → 4 ✓ (only the two qualifying subsequences, each formed in 2 ways = 4)
- `[0,1,2,3,4,5,6,7,8]` → 0 ✓ (no value repeats, middle can never be unique mode)

Added `C2(k)` helper that returns `0` when `k < 2` to safely handle the `x=1` case computations like `C(Rp - cr_v, 2)` when there aren't enough elements. This prevents negative or invalid intermediate values and keeps the math correct. The overall approach decomposes by `x` (count of middle value `a` picked from sides), where `x >= 2` is automatic and `x = 1` requires the 3 non-`a` elements to be all distinct values, handled via per-value sums.
