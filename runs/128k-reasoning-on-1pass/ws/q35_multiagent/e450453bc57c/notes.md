
## ideation
The core difficulty lies in efficiently computing the minimum operations to make each sliding window of size `x` uniform, which corresponds to finding the sum of absolute deviations from the median. A naive approach would take $O(x \log x)$ per window, leading to $O(nx \log x)$ overall, which is too slow. Using two heaps (max-heap for the lower half, min-heap for the upper half) with lazy deletion allows maintaining the median and computing the cost in $O(\log x)$ per slide, resulting in $O(n \log x)$ total time for cost computation.

The second part is selecting $k$ non-overlapping windows to minimize total cost. This is a classic dynamic programming problem where `dp[j][i]` represents the minimum cost to pick `j` windows from the first `i` windows. The transition considers either skipping the current window or picking it (adding its precomputed cost and ensuring non-overlap by jumping back `x` steps). This DP runs in $O(nk)$ time.

Pitfalls to avoid:
1. Incorrect heap balancing or lazy deletion handling can lead to wrong medians or negative counts.
2. DP initialization must correctly set impossible states to infinity and base cases to 0.
3. The median for even-length windows can be any value between the two middle elements; using the lower median (top of `lo`) is standard and correct for sum of absolute differences.

## worker: (none)
1. **Sliding Window Median & Cost Calculation**: The cost to make a subarray uniform is the sum of absolute differences from its median. We maintain a sliding window of size `x` using a Binary Indexed Tree (BIT) over coordinate-compressed values. The BIT tracks frequencies and sums, allowing $O(\log N)$ updates and queries. The median is found using binary lifting on the BIT in $O(\log N)$. The cost is computed as `(med * cnt_lo - sum_lo) + (sum_hi - med * cnt_hi)`.
2. **Dynamic Programming**: After precomputing costs for all $m = n - x + 1$ windows, we use DP where `dp[j][i]` is the minimum cost to pick `j` non-overlapping windows from the first `i` windows. The transition considers either skipping the current window or picking it (adding its cost and jumping back `x` steps to ensure non-overlap). This runs in $O(K \cdot N)$ time.
3. **Complexity**: Coordinate compression and BIT operations take $O(N \log N)$. DP takes $O(KN)$. Overall time complexity is $O(N \log N + KN)$, well within limits for $N=10^5, K=15$. Space complexity is $O(N)$.
4. **Edge Cases**: Handles negative numbers via coordinate compression and signed sums. Ensures valid states in DP are initialized to 0 or INF correctly. The constraint $k \cdot x \le n$ guarantees a solution exists.
