
## ideation
The core difficulty is efficiently computing the inversion count for all `M` cyclic shifts. The key insight is that when incrementing `k` by 1, only pairs where exactly one element equals `M-1` change order. This allows a transition formula based on precomputed frequencies and position sums. The initial inversion count requires a Fenwick tree, but subsequent updates are O(1).

## worker: Implement the solution: read inputs, compute frequ
- The algorithm computes `inv_0` in O(N log M) using a Fenwick tree.
- For each subsequent shift `k`, we use the fact that only pairs involving the value that becomes `M-1` change order. Precomputing the frequency and sum of positions for each value allows O(1) updates.
- The formula for `L` (number of "M-1 first" pairs) uses 0-indexed positions: `L = m*(N-1) - S - m*(m-1)/2`, where `S` is the sum of positions of elements with value `v`.
- The net change in inversion count is `delta = m*(N-m) - 2L`, which accounts for both gained and lost inversions.
- Total complexity: O((N+M) log M) due to the Fenwick tree, with the rest being O(M). This fits easily within the limits for N, M ≤ 2×10⁵.

## worker: Carefully verify the transition formula used for u
The transition formula was carefully re-derived:

- When `k` increases by 1, elements equal to `M-1` wrap to `0`, becoming the smallest values. For a pair where exactly one element equals `M-1`:
  - If the `M-1` element is at index `i` and the other at `j > i`: originally `v_i > v_j` (inversion exists), but after shift `v_i = 0 < v_j` (inversion lost).
  - If the `M-1` element is at index `j` and the other at `i < j`: originally `v_i < v_j` (no inversion), but after shift `v_i > v_j` (inversion gained).

- For a value `v` with frequency `m` and sum of positions `S` (0-indexed), the number of pairs where `v` appears first is:
  `L = m*(N-1) - S - m*(m-1)/2`
  (total possible later positions minus same-value pairs).

- The net change is: `delta = (gained) - (lost) = m*(N-m) - 2L`.

- This formula correctly handles all cases, verified against sample inputs and additional tests.

The solution runs in O((N+M) log M) time due to the Fenwick tree for `inv_0`, with the rest being O(M). It uses O(N+M) memory and handles all edge cases including M=1 and N=1.
