
## ideation
**Core task.** Compute `S = Σ_{subarrays with length ≤ k} (max + min)`. With n up to 8·10⁴, brute force over all O(nk) subarrays could be up to 6.4·10⁹ — too slow. Need a per-element "contribution" decomposition.

**Contribution framework (for max).** For each index `i`, determine the range of subarrays in which `nums[i]` is *the* maximum. Use a monotonic stack to get:
- `L[i]` = index of nearest element to the left that is **strictly greater** than `nums[i]` (−1 if none),
- `R[i]` = index of nearest element to the right that is **greater or equal** (n if none).

(One side strict, the other non-strict → each subarray attributed to exactly one index; avoids double counting on duplicates. Must be consistent when reusing the routine for the negated array.)

Then valid subarrays are `s ∈ [L+1, i]`, `e ∈ [i, R−1]`. Let `a = i − L`, `b = R − i`, and reparametrize `x = i − s ∈ [0, a−1]`, `y = e − i ∈ [0, b−1]`. Length = `x + y + 1 ≤ k` ⇔ `x + y ≤ m` with `m = k − 1`.

**Counting formula.** Number of lattice points with `x,y ≥ 0`, `x ≤ a−1`, `y ≤ b−1`, `x+y ≤ m`:
```
f(t) = (t+1)(t+2)//2 if t >= 0 else 0      # count of x,y>=0 with x+y<=t
N = f(m) - f(m-a) - f(m-b) + f(m-a-b)
```
Standard 2-D inclusion–exclusion (subtract `x ≥ a`, subtract `y ≥ b`, add back both). Sanity checks: `k=1` ⇒ `m=0` ⇒ `N = 1 - 0 - 0 + 0 = 1` ✓; `k ≥ n` ⇒ `N = a·b` ✓ (verify: `f(m)-f(m-a)-f(m-b)+f(m-a-b)` collapses to `ab` when `m ≥ a+b−2`).

**Min part.** `Σ min(subarray) = −Σ max(subarray of negated array)`. So write one helper `sumOfMaxes(arr, k)` and return `sumOfMaxes(nums,k) - sumOfMaxes([-x for x in nums], k)`.

**Pitfalls to watch.**
- Tie handling: if both sides use non-strict comparison, equal elements get double counted; if both strict, some subarrays get counted twice/zero. Pick strict-left / non-strict-right (or the mirror) and keep it fixed.
- After negation, the "strictly greater / greater-or-equal" roles must remain the same in the helper (helper operates on its own array, so it's automatic).
- Negative values are fine — contributions can be negative; no clamping.
- Don't forget subarrays of length 1 (they contribute `2*nums[i]` total across both parts).
- Python recursion/stack not an issue; use iterative monotonic stack, O(n).
- Verify formula edge cases where `m - a`, `m - b`, `m - a - b` are negative.
- Answer can be large-ish (≈ 8e4 · 8e4 · 1e6) but Python ints are unbounded.

**Alternative approaches (backup / cross-check).**
- Sliding window of size k with two monotonic deques, maintaining running sum of window maxima/minima incrementally (harder to get right; the "sum over all windows of all sizes ≤ k" isn't directly a single window scan).
- Divide and conquer / offline with a stack + prefix sums of counts — more code, same complexity.
- Brute force O(n·k) reference implementation for random testing against the fast one.

## worker: Write the complete `Solution.minMaxSubarraySum` im
- **Decomposition**: total = Σ_{|sub| ≤ k} max + Σ_{|sub| ≤ k} min, and Σ min(sub) = −Σ max(sub of negated array). So one helper suffices.
- **Attribution**: for index `i`, `L[i]` = nearest left index with *strictly greater* value, `R[i]` = nearest right index with value *≥* `arr[i]`. With this strict/non-strict split, each subarray is attributed to exactly one index (the leftmost occurrence of its maximum), so no double counting with duplicates.
- **Counting**: subarrays containing `i` inside `(L[i], R[i])` are parametrized by `x = i − s ∈ [0, a−1]`, `y = e − i ∈ [0, b−1]` with `a = i − L[i]`, `b = R[i] − i`; length constraint `x + y ≤ m = k − 1`. Inclusion–exclusion gives `f(m) − f(m−a) − f(m−b) + f(m−a−b)` where `f(t) = (t+1)(t+2)/2` counts nonnegative pairs with sum ≤ t.
- **Sanity checks**: `k = 1` ⇒ `m = 0` ⇒ count = 1 per index ✓. `k ≥ n` ⇒ `m ≥ a+b−2` ⇒ formula collapses to `a·b` ✓. Example 1 verified by hand: max-sum = 11, min-sum = 9, total 20 ✓. Example 2: max-sum over subarrays of len ≤2 = 1 + (−3) + 1 + 1 + 1 = 1; min-sum = 1 −3 + 1 −3 −3 = −7; total −6 ✓.
- **Complexity**: O(n) time, O(n) space; single monotonic-stack pass computes both `L` and `R` (popping `j` at `i` means `R[j] = i`). Python big ints handle the magnitude (~6.4e15 max).
