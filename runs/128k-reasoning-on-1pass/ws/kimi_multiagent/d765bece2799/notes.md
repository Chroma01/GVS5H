
## ideation
Core difficulty: `n` up to 80000 rules out enumerating all `O(nk)` subarrays. Need an `O(n)`/near-`O(n)` contribution method: each `nums[i]` contributes as the maximum/minimum for a contiguous range of subarrays, but only those whose total length is `≤ k`.

Key idea: split answer into `sumMax(nums,k) + sumMin(nums,k)`, and compute `sumMin` by reusing max logic on `-nums`. For max contribution, use monotonic stack boundaries: previous greater and next greater-or-equal (or equivalent tie rule) so duplicates are counted once. If an element can extend `L` steps left and `R` steps right while remaining the chosen max, the number of endpoint choices `(a,b)` with `1≤a≤L`, `1≤b≤R`, and subarray length `a+b-1≤k` must be counted by a closed-form triangular/truncated-rectangle formula, not nested loops.

Main pitfalls: inconsistent `>` vs `>=` causing duplicate/missing equal values; off-by-one in length constraint (`a+b-1≤k` means `a+b≤k+1`); assuming `k≤n` without clamping; overflow in fixed-width languages; negative values making min logic error-prone if not mapped to max of negated array; validating formula when `k` is smaller than `L`/`R` or larger than `L+R`.

## worker: Implement the complete solution: derive the O(1) c
- **Decomposition**: answer = `sumMax(nums, k) + sumMin(nums, k)`, and `sumMin(nums, k) = -sumMax([-x for x in nums], k)`, so only one contribution routine is needed.
- **Ownership of a subarray to one index**: for each `i`, `prev_g[i]` = nearest left index with a *strictly greater* value, and the right scan finds the nearest right index with a *greater-or-equal* value. Any subarray whose start lies in `(prev_g[i], i]` and end in `[i, next_ge[i])` has `arr[i]` as its maximum, and ties are uniquely assigned to the leftmost maximal position (equal left neighbors don't block `prev_g`, but equal right neighbors close the right boundary). No subarray is double-counted or missed.
- **Length cap**: with `L = i - prev_g[i]` left extensions and `R = r - i` right extensions, a choice `(a, b)` gives subarray length `a + b - 1 ≤ k`, i.e. `a + b ≤ k + 1 = s`. `countPairs` counts these in O(1) assuming WLOG `L ≤ R`:
  - `s ≥ L + R`: all `L·R` pairs.
  - `s ≤ L + 1`: unconstrained triangle `s(s-1)/2`.
  - `L + 1 < s ≤ R + 1`: trapezoid `L·s − L(L+1)/2`.
  - `s > R + 1`: rectangle minus mirrored triangle, `L·R − s'(s'-1)/2` with `s' = L + R + 1 − s`.
- **Verification**: hand-checked both examples (`[1,2,3], k=2 → 20`; `[1,-3,1], k=2 → -6`) and the `k = n` case (`[1,2,3], k=3 → sumMax = 14`).
- **Complexity**: O(n) time (two monotonic-stack passes over `nums` and its negation), O(n) space. Python ints avoid overflow.
