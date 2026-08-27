
## ideation
The problem asks us to minimize the sum of coordinates of $N$ pieces on a number line by repeatedly applying an operation. The operation involves selecting an index $i$ and moving the $(i+1)$-th and $(i+2)$-th pieces to positions symmetric with respect to the midpoint of the $i$-th and $(i+3)$-th pieces.

**Key Insights:**
1.  **Effect on Differences:** Let $d_k = X_{k+1} - X_k$ be the difference between adjacent pieces. The operation on index $i$ effectively reverses the order of the three differences $d_i, d_{i+1}, d_{i+2}$ to $d_{i+2}, d_{i+1}, d_i$. Specifically, the new differences become $d'_{i} = d_{i+2}$, $d'_{i+1} = d_{i+1}$, and $d'_{i+2} = d_i$. The difference $d_{i+1}$ remains in the middle, while $d_i$ and $d_{i+2}$ swap places.
2.  **Invariant:** The set of differences at odd positions $\{d_1, d_3, d_5, \dots\}$ and the set of differences at even positions $\{d_2, d_4, d_6, \dots\}$ are invariant under the operation. We can only swap $d_i$ and $d_{i+2}$.
3.  **Objective:** The sum of coordinates is given by $S = \sum_{k=1}^N X_k = N X_1 + \sum_{k=1}^{N-1} (N-k) d_k$. To minimize $S$, we need to minimize $\sum_{k=1}^{N-1} (N-k) d_k$. Since the coefficients $(N-k)$ are strictly decreasing with $k$, we should assign smaller values of $d_k$ to larger coefficients (smaller $k$) and larger values of $d_k$ to smaller coefficients (larger $k$). This implies we want the sequence of differences to be sorted in non-decreasing order.
4.  **Constraint:** Due to the invariant property (odd indices stay odd, even indices stay even), we cannot arbitrarily sort all differences. We must sort the differences at odd indices among themselves and the differences at even indices among themselves.
5.  **Algorithm:**
    -   Calculate the initial differences $d_1, \dots, d_{N-1}$.
    -   Separate them into two lists: `odd_diffs` (indices $1, 3, 5, \dots$) and `even_diffs` (indices $2, 4, 6, \dots$).
    -   Sort both lists in ascending order.
    -   Reconstruct the difference array by placing the sorted `odd_diffs` back into odd positions and sorted `even_diffs` into even positions.
    -   Compute the final sum of coordinates using the new difference array.

**Pitfalls:**
-   Integer overflow: Coordinates can be up to $10^{12}$ and $N$ up to $2 \times 10^5$, so the sum can exceed $2^{63}-1$. Use 64-bit integers (Python handles this automatically).
-   1-based vs 0-based indexing: Be careful when mapping the sorted lists back to the array.
-   The operation reverses the outer two differences, but the middle one stays put. This confirms the parity invariant.
