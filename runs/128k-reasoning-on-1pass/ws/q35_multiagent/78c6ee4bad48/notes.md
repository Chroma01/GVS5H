
## ideation
The problem asks us to minimize the sum of coordinates of $N$ pieces on a number line. The allowed operation involves choosing four consecutive pieces in sorted order and reflecting the inner two pieces across the midpoint of the outer two.

Key observations:
1.  **Effect on Gaps**: Let the sorted coordinates be $x_1 < x_2 < \dots < x_N$ and the gaps be $d_j = x_{j+1} - x_j$. The operation on index $i$ (involving $x_i, x_{i+1}, x_{i+2}, x_{i+3}$) transforms the gaps $(d_i, d_{i+1}, d_{i+2})$ into $(d_{i+2}, d_{i+1}, d_i)$. This means the operation swaps $d_i$ and $d_{i+2}$ while keeping $d_{i+1}$ unchanged.
2.  **Permutation of Gaps**: Since we can swap any $d_i$ and $d_{i+2}$, we can arbitrarily permute the gaps at odd indices ($d_1, d_3, d_5, \dots$) among themselves, and similarly permute the gaps at even indices ($d_2, d_4, d_6, \dots$) among themselves.
3.  **Invariant Coordinates**: The first coordinate $x_1$ and the last coordinate $x_N$ remain invariant because the set of gaps is preserved and their sum is $x_N - x_1$.
4.  **Minimizing the Sum**: The sum of coordinates can be expressed as $\sum_{k=1}^N x_k = N \cdot x_1 + \sum_{j=1}^{N-1} (N-j) d_j$. The coefficients $(N-j)$ are decreasing with $j$. To minimize the sum, we should assign the smallest gaps to the largest coefficients. Since odd-indexed gaps can only move to odd positions and even-indexed gaps to even positions, we sort the odd-indexed gaps and even-indexed gaps separately in ascending order and assign them to their respective positions.

The algorithm is:
1.  Compute the gaps $d_j = X_{j+1} - X_j$.
2.  Separate gaps into odd-indexed and even-indexed lists.
3.  Sort both lists in ascending order.
4.  Reconstruct the sum by assigning the sorted gaps to positions $j=1, \dots, N-1$ with coefficients $N-j$.

The time complexity is dominated by sorting, which is $O(N \log N)$, well within the constraints.

## worker: [todo] Read the input values $N$ and the list of c
The operation described swaps the gaps $d_i$ and $d_{i+2}$ while keeping $d_{i+1}$ unchanged. This means gaps at odd indices ($d_1, d_3, \dots$) can be arbitrarily permuted among themselves, and similarly for even indices ($d_2, d_4, \dots$). The sum of coordinates is $\sum X_k = N \cdot X_1 + \sum_{j=1}^{N-1} (N-j) d_j$. The coefficients $(N-j)$ are strictly decreasing. To minimize the sum, we assign the smallest available gaps to the largest coefficients. Since odd and even indexed gaps cannot mix, we sort each parity group independently in ascending order and place them back into their respective positions. This greedy assignment is optimal and runs in $O(N \log N)$ time due to sorting, which fits well within the constraints.
