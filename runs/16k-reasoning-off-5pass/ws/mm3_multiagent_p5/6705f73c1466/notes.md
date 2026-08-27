
## ideation
The core difficulty: we need to transform the binary string into one where all 1s form a single contiguous block, and we are allowed to swap adjacent characters. The number of adjacent swaps needed equals the total distance each 1 moves.

Let the 1-indexed positions of the 1s be `p1 < p2 < ... < pK`. If we aim to make the final block start at index `l` (1-indexed) and occupy `[l, l+K-1]`, then the i-th 1 must go to `l + i - 1`. The number of adjacent swaps is `sum_i |p_i - (l + i - 1)|`. We want to minimize this over all valid `l` (such that the block fits inside the string, i.e., `1 ≤ l ≤ N-K+1`).

This is a classic problem: define `q_i = p_i - i`. Then the expression becomes `sum_i |q_i - (l-1)|`. This is minimized by choosing `l-1` to be the median of the `q_i` values. Then compute the total cost.

Edge case: if K = 1, the answer is 0 (or cost 0 because any median gives 0).

Complexities: O(N) to find positions, O(K log K) to find the median, O(K) to compute the cost. With N up to 5e5, this is fine.

Pitfalls:
- Use 0-indexing internally to avoid confusion, but be consistent.
- The block must fit: l ranges from 0 to N-K (0-indexed). The median might fall outside this range, but due to convexity the unconstrained minimum gives the correct answer if the median is within bounds; if not, the optimal is at the boundary. However, with at least one 1, the median always lies in a valid range? Actually, if K=1, l=pos, median is pos, valid. For K>1, the median is always between the first and last 1, and the first 1 can be moved to the left boundary and the last to the right boundary, so the median is always a feasible l. So we can safely take the median.
- Large N: use 64-bit integers for the sum (Python int is arbitrary precision, fine).

## worker: Read N and S, collect zero-based positions of '1's
The solution follows the standard approach for minimizing adjacent swaps to make 1s contiguous:

1. Collect zero-based positions of all '1's in the string.
2. Let `K` be the count. If `K` ≤ 1, the answer is 0.
3. For a final block starting at `l` (0-indexed), the i-th '1' must move to position `l + i`, giving cost `|pos[i] - (l + i)|`.
4. Transform to `q_i = pos[i] - i`; the cost becomes `sum |q_i - l|`, minimized at `l = median(q_i)`.
5. Compute the median (middle element after sorting) and sum the absolute differences.

Complexities: O(N) to scan, O(K log K) to sort (K ≤ N ≤ 5×10⁵), O(K) to compute the sum — all within limits. Python integers handle the large sum automatically.

The median always lies in a feasible range (between the first and last '1'), so no boundary check is needed.
