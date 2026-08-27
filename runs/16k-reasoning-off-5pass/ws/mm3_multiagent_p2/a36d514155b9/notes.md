
## ideation
We need to compute the sum of Manhattan distances over all unordered pairs of pieces, summed over every valid arrangement (choosing k distinct cells from an m×n grid). Let the total number of cells be N = m * n. Each arrangement is a k-subset of cells, and there are C(N, k) arrangements.

Manhattan distance is separable: |x_i - x_j| + |y_i - y_j|. Because symmetry is the same for x- and y-coordinates, we can compute Sx = sum over all unordered cell pairs of |x_i - x_j|, and similarly Sy. Then the answer is (Sx + Sy) * C(N-2, k-2) * inv(C(N, k)) mod MOD. (Each pair appears in C(N-2, k-2) arrangements out of C(N, k).)

To compute Sx: each row i (0-indexed) has n cells. For any two distinct rows i < j, there are n * n pairs of cells with x-coordinate difference |i - j|. So Sx = n^2 * sum_{0 ≤ i < j < m} (j - i) = n^2 * (m^3 - m)/6. Similarly, Sy = m^2 * (n^3 - n)/6.

Then total = (Sx + Sy) * C(N-2, k-2) % MOD * inv(C(N, k)) % MOD.

We need modular inverses. Precompute factorials and inverse factorials up to N (≤ 10^5). All operations O(N) precomputation plus O(1) for the answer.

Pitfalls:
- N can be up to 10^5, so precomputation is fine.
- Division by 6: use modular inverse of 6.
- Ensure the modular arithmetic is correct: multiply (Sx + Sy) mod MOD by the fraction C(N-2, k-2) * inv(C(N, k)) mod MOD.
- Edge cases: large m, n, but formula uses multiplication; risk of overflow in Python? Use pow with MOD.

We must write class Solution with method distanceSum(self, m, n, k).

## worker: Write the `Solution` class in Python implementing 
- The Manhattan distance separates into x and y contributions.
- For x-contribution: each pair of rows `i < j` contributes `j - i` to the x-distance of every pair of cells (one from row i, one from row j), giving `n * n` pairs per row pair. Sum over all row pairs gives `n^2 * m*(m^2-1)/6`.
- Similarly for y-contribution: `m^2 * n*(n^2-1)/6`.
- A specific unordered cell pair appears in exactly `C(N-2, k-2)` of the `C(N, k)` arrangements, so we multiply the total pair distance by that fraction.
- Modular arithmetic uses `MOD = 10^9 + 7`, with factorials precomputed up to `N = m*n <= 10^5`, and modular inverses via Fermat's little theorem.
