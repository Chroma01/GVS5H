1. Sort sequences A and B to enable efficient prefix sum calculations.
2. Precompute prefix sums for sorted A and sorted B to allow O(1) range sum queries.
3. For each query (X_k, Y_k), we need to compute sum_{i=1}^{X_k} sum_{j=1}^{Y_k} |A_i - B_j|.
4. To compute this efficiently, for each A_i (i from 1 to X_k), find how many B_j (j from 1 to Y_k) are less than or equal to A_i using binary search (bisect_right) on the sorted B[0:Y_k].
5. For each A_i, split the B_j's into those <= A_i and those > A_i. Use prefix sums to quickly compute the sum of absolute differences.
6. Sum up the contributions for all i from 1 to X_k to get the final answer for each query.