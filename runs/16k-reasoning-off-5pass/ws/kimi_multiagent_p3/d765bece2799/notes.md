
## ideation
The problem asks for the sum of (min + max) over all subarrays of length ≤ k. The naive O(n·k) or O(n²) enumeration is too slow for n = 80000 (worst case ~3.2·10⁹ operations). The natural decomposition is: answer = (sum of max over all subarrays with length ≤ k) + (sum of min over all subarrays with length ≤ k). These two are symmetric, so solving one solves the other (min version = negate array, or flip comparisons).

Core difficulty: the classic "sum of subarray maximums" uses monotonic stacks to get, for each i, the number of subarrays where nums[i] is the maximum = left_count · right_count, where left_count = i - prev_greater_or_equal(i), right_count = next_greater(i) - i. But that counts subarrays of ALL lengths. Here we must restrict to subarrays of length ≤ k, so the simple product breaks — we need to count pairs (l, r) with l ∈ (prev_boundary, i], r ∈ [i, next_boundary), and r - l + 1 ≤ k.

Let L = i - pge(i) (max steps left), R = nge(i) - i (max steps right). We need the number of pairs (a, b) with 1 ≤ a ≤ L, 1 ≤ b ≤ R, and a + b - 1 ≤ k, i.e., a + b ≤ k + 1. This count is a piecewise formula:
- Let a range over [1, L]; for each a, b can range over [1, min(R, k+1-a)].
- If L + R ≤ k + 1: count = L·R (no constraint binds).
- Otherwise it's a trapezoidal sum: count = Σ_{a=1}^{L} min(R, k+1-a), which can be computed in O(1) by splitting a at the point where k+1-a drops below R. Concretely, define t = k+1-R; for a ≤ t, min = R; for a > t, min = k+1-a (while positive). Need care when k+1-a ≤ 0.

Alternative viewpoint: for each window length, sliding min/max — but summing over all lengths ≤ k still needs O(n·k). Another alternative: convolution-style counting. The contribution approach is cleanest.

Pitfalls:
- Duplicate values: must use strict on one side and non-strict on the other (e.g., previous greater-or-equal on left, strictly greater on right) to avoid double-counting subarrays whose max appears multiple times. Same for mins.
- Negative numbers: contributions can be negative; no modular arithmetic mentioned, so plain integer arithmetic (Python handles big ints anyway).
- Off-by-one in the length constraint: subarray length = a + b - 1 ≤ k.
- k can be up to n, in which case the formula must reduce to the classic L·R.
- Edge cases: k = 1 (each element contributes 2·nums[i]); single element array.

The combinatorial count f(L, R, k) = number of (a,b), 1≤a≤L, 1≤b≤R, a+b ≤ k+1:
- If k+1 ≥ L+R: L·R.
- Else: let s = k+1. Count = Σ_{a=1}^{L} clamp(s-a, 0, R). Split: a from 1 to s-R gives R each (if s-R ≥ 1); a from s-R+1 to s-1 gives s-a each; a ≥ s gives 0. All computable in O(1) with triangular numbers.

Monotonic stack gives pge/nge (and symmetric ple/nle for minima) in O(n). Total O(n) time, O(n) space.

## worker: Implement the full solution: monotonic-stack helpe
- Decomposed answer into (sum of subarray maximums) + (sum of subarray minimums) over all subarrays of length ≤ k.
- For each index i, monotonic stacks give `left[i]` (max steps extendable left) and `right[i]` (max steps right) such that nums[i] is the attributed extremum. Tie-breaking: for max, pop strictly-smaller on the left pass (so left boundary is previous ≥) and pop ≤ on the right pass (right boundary is next strictly >), ensuring each subarray's max is attributed exactly once (to its leftmost occurrence). Symmetric for min.
- `count_pairs(L, R)` counts (a, b) with 1≤a≤L, 1≤b≤R, a+b ≤ k+1 in O(1): if L+R ≤ k+1 it's L·R; otherwise split into a region where b is capped at R and a region where b = s−a (triangular sum).
- Verified against both examples (20 and -6) and a brute-force cross-check on random small arrays including duplicates, negatives, k=1, and k=n — all matched.
- Complexity: O(n) time, O(n) space; n ≤ 80000 is fine. Python ints handle negative/large sums natively.
