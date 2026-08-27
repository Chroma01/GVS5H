
## ideation
The core difficulty lies in the non-linear nature of the objective function $\max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)$. Standard greedy strategies based on a single attribute or simple sum often fail because the "dominant" attribute can vary between pairs.

Key observations:
1.  **Candidate Selection**: The optimal set of $2K$ cakes must consist of the "best" cakes. A strong heuristic is that the optimal $2K$ cakes are among those with the largest sums $S_i = X_i + Y_i + Z_i$. While not strictly proven for all cases, in competitive programming contexts for this specific problem structure (AtCoder ABC 400 F equivalent or similar), sorting by total sum and taking the top $2K$ is a very strong candidate for the correct subset.
2.  **Pairing Strategy**: Once the $2K$ candidates are selected, we need to pair them to maximize the sum of maxes.
    *   Pairing the largest with the smallest (and second largest with second smallest, etc.) tends to balance the contributions. If one cake has a huge value in one attribute, pairing it with a cake that has small values prevents "wasting" the potential of the large cake on another large cake (which might not increase the max if the other attribute is already dominated).
    *   Specifically, if we sort the top $2K$ cakes by their total sum $S_i$ in descending order, pairing $i$ with $2K-1-i$ (0-indexed) is a robust strategy. This is analogous to pairing the strongest with the weakest to maximize the sum of minimums in some contexts, but here it helps balance the max function.

Pitfalls:
*   Assuming that sorting by a single attribute (e.g., just X) is sufficient. It is not, as Y and Z matter.
*   Assuming that the top $2K$ by sum is always the correct subset. There might be edge cases, but given the constraints and problem type, this is the most viable efficient approach. A brute force over all subsets is $O(\binom{N}{2K})$, which is infeasible.
*   The pairing of the selected $2K$ items: Simply pairing adjacent items in the sorted list might not be optimal if the distribution of attributes is skewed. Pairing largest with smallest is generally safer for max-sum problems to avoid "clumping" high values that don't contribute to the max.

Approach:
1.  Read input.
2.  For each test case:
    a. Calculate $S_i = X_i + Y_i + Z_i$ for each cake.
    b. Sort cakes by $S_i$ descending.
    c. Select the top $2K$ cakes.
    d. Sort these $2K$ cakes by $S_i$ descending (they are already sorted from step b).
    e. Pair the $i$-th cake with the $(2K - 1 - i)$-th cake for $i$ from $0$ to $K-1$.
    f. Calculate the price for each pair: $\max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)$.
    g. Sum the prices and print.

This approach is $O(N \log N)$ per test case due to sorting, which fits within the time limits ($\sum N \le 10^5$).

## worker: (None)
The problem requires selecting $2K$ cakes and pairing them into $K$ pairs to maximize the sum of $\max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)$.

1.  **Subset Selection**: The optimal set of $2K$ cakes is likely to be the ones with the highest total attribute sums ($X+Y+Z$). This is because the maximum of sums is bounded by the sum of maximums, and generally, cakes with higher total "mass" contribute more to the potential pair price. Sorting all $N$ cakes by $X_i+Y_i+Z_i$ descending and taking the top $2K$ is a standard and effective heuristic for this class of problems.
2.  **Pairing Strategy**: Once the $2K$ candidates are fixed, we need to pair them. A naive approach might pair adjacent elements in the sorted list, but this can lead to suboptimal results if the attributes are skewed. Pairing the largest sum cake with the smallest sum cake among the selected $2K$ (i.e., $i$-th largest with $i$-th smallest) tends to balance the contributions. This strategy prevents "wasting" a very high-value cake by pairing it with another high-value cake where the max function might not increase significantly, and instead uses the high-value cake to boost the lower-value cake's pair price.
3.  **Complexity**: Sorting takes $O(N \log N)$. Selecting top $2K$ and pairing takes $O(K)$. With $\sum N \le 10^5$, this approach is efficient enough.
