- **Initial inversion count:** Scan the sequence from left to right using a Fenwick tree over values `0..M-1`. For an element `A[i]`, the number of previous elements greater than it is `i - count(values <= A[i])`.

- **Effect of increasing the shift:** Every element increases by one modulo `M`. Only the elements currently having residue `M-1` wrap to `0`; all other pairs preserve their relative ordering.

- **Transition delta:** Suppose the wrapping group consists of original value `x`, with count `t` and zero-based position sum `S`. For an element at position `p`, comparisons with non-group elements on its left change from non-inversions to inversions, while comparisons with non-group elements on its right change from inversions to non-inversions. Comparisons with elements of the same group remain equal and do not change.

- **Aggregated update:** Summing over all positions in the wrapping group causes same-group contributions to cancel pairwise. Therefore the total change is:
  `delta = 2 * S - t * (N - 1)`.

- **Wrapping group:** During the transition from shift `k` to `k+1`, the wrapping group has original value:
  `x = (M - 1 - k) mod M`.

- **Complexity:** Initial Fenwick processing takes `O(N log M)`. The per-value counts and position sums are built during the same scan, and all transitions take `O(M)`. Total complexity is `O(N log M + M)` with `O(N + M)` memory.

- **Edge cases:** Repeated values are handled because equal-valued pairs never contribute to a transition delta. For `M = 1`, every residue is always zero, so the single initial inversion count is printed and no transition is needed.
