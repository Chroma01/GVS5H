
## ideation
The problem asks to minimize the sum of coordinates of $N$ pieces on a number line by repeatedly applying a specific reflection operation.
The operation involves picking indices $i, i+1, i+2, i+3$ (in sorted order) and reflecting the middle two ($i+1, i+2$) across the midpoint of the outer two ($i, i+3$).
Key observations:
1.  **Invariant**: The operation fixes the coordinates of the $i$-th and $(i+3)$-th pieces. It changes the coordinates of the middle two.
2.  **Effect on Differences**: Let the sorted coordinates be $x_1, x_2, \dots, x_N$. Define differences $d_k = x_{k+1} - x_k$ for $k=1 \dots N-1$.
    The operation on indices $i, i+1, i+2, i+3$ effectively swaps the difference $d_i$ (between $i$ and $i+1$) and $d_{i+2}$ (between $i+2$ and $i+3$) in the sequence of differences of the *newly sorted* array.
    Specifically, if we consider the sequence of differences $d_1, d_2, \dots, d_{N-1}$, the operation allows us to swap $d_i$ and $d_{i+2}$ for any valid $i$.
3.  **Reachability**: Since we can swap $d_i$ and $d_{i+2}$, we can independently permute the differences at odd indices ($d_1, d_3, d_5, \dots$) and the differences at even indices ($d_2, d_4, d_6, \dots$) to any order. We cannot swap an odd-indexed difference with an even-indexed one.
4.  **Objective Function**: The sum of coordinates is $S = \sum_{k=1}^N x_k$. Since $x_k = x_1 + \sum_{j=1}^{k-1} d_j$, we can rewrite the sum in terms of $x_1$ and $d_j$:
    $S = N \cdot x_1 + \sum_{k=1}^{N-1} (N-k) d_k$.
    Here, $x_1$ is the first coordinate, which is never moved (it's always the $i$-th piece for $i=1$, but never the $(i+1), (i+2), (i+3)$-th piece). Thus $x_1$ is constant.
    To minimize $S$, we need to minimize $\sum_{k=1}^{N-1} (N-k) d_k$.
    The coefficients $(N-k)$ are decreasing: $N-1, N-2, \dots, 1$.
    To minimize the dot product, we should assign the smallest available differences to the largest coefficients.
    Since the sets of odd-indexed and even-indexed differences are independent, we should sort the odd-indexed differences in ascending order and place them at positions $1, 3, 5, \dots$, and sort the even-indexed differences in ascending order and place them at positions $2, 4, 6, \dots$.

Algorithm:
1.  Read $N$ and the array $X$.
2.  Extract $x_1$ (the first element).
3.  Compute the differences array $D$ where $D[k] = X[k+1] - X[k]$ for $k=0 \dots N-2$ (0-indexed logic).
    Note: In 1-based indexing for the problem, $d_1 = X_2 - X_1$, etc.
    Let's stick to 0-based implementation:
    $D[i] = X[i+1] - X[i]$ for $i \in [0, N-2]$.
    The coefficient for $D[i]$ in the sum formula corresponds to the position in the sorted array.
    If we use 0-based index $i$ for the difference array (representing gap between $i$-th and $(i+1)$-th element), the weight is $(N - 1 - i)$.
    Wait, let's re-verify the weight.
    $S = x_1 + (x_1+d_1) + (x_1+d_1+d_2) + \dots$
    $S = N x_1 + (N-1)d_1 + (N-2)d_2 + \dots + 1 \cdot d_{N-1}$.
    So the weight for $d_k$ (where $k$ is 1-based index of the gap) is $N-k$.
    In 0-based array $D$, $D[i]$ corresponds to $d_{i+1}$. So weight is $N-(i+1) = N-1-i$.
4.  Separate $D$ into two lists: `odds` (indices 0, 2, 4...) and `evens` (indices 1, 3, 5...).
    Wait, the parity of the index in the difference array corresponds to the parity of the gap position.
    Gap 1 ($d_1$) is at index 0. Gap 2 ($d_2$) is at index 1.
    We established we can swap $d_i$ and $d_{i+2}$.
    $d_1$ (idx 0) swaps with $d_3$ (idx 2).
    $d_2$ (idx 1) swaps with $d_4$ (idx 3).
    So yes, we sort elements at even indices of $D$ among themselves, and elements at odd indices of $D$ among themselves.
5.  Reconstruct the minimal sum.
    $Total = N \cdot X[0] + \sum_{i=0}^{N-2} (N-1-i) \cdot D_{sorted}[i]$.
    Where $D_{sorted}[i]$ is the value at index $i$ after sorting.

Pitfalls:
-   Large numbers: Coordinates up to $10^{12}$, $N$ up to $2 \cdot 10^5$. Sum can exceed $2^{63}-1$?
    Max sum approx $N \cdot 10^{12} \approx 2 \cdot 10^{17}$, which fits in a 64-bit signed integer (max $\approx 9 \cdot 10^{18}$). Python handles large integers automatically.
-   Input reading: Standard.
-   Indices: Careful with 0-based vs 1-based.

## worker: Implement the solution in Python: read input, comp
The problem asks us to minimize the sum of coordinates of $N$ pieces on a number line. The allowed operation involves selecting four consecutive pieces in sorted order ($i, i+1, i+2, i+3$) and reflecting the middle two ($i+1, i+2$) across the midpoint of the outer two ($i, i+3$).

Key insights derived:
1.  **Invariant**: The coordinates of the $i$-th and $(i+3)$-th pieces remain unchanged during the operation. Specifically, the first piece ($x_1$) and the last piece ($x_N$) are never moved because they can never be the "middle" pieces of a valid operation (indices $i+1, i+2$ require $i \ge 1$, so $i+1 \ge 2$, and $i+3 \le N$ implies $i \le N-3$, so $i+3 \le N$). Thus, $x_1$ is constant.
2.  **Difference Array Transformation**: Let $d_k = x_{k+1} - x_k$ be the differences between adjacent sorted pieces. The operation effectively allows us to swap $d_i$ and $d_{i+2}$ in the sequence of differences. This means the set of differences at odd indices ($d_1, d_3, d_5, \dots$) can be permuted among themselves arbitrarily, and the set of differences at even indices ($d_2, d_4, d_6, \dots$) can be permuted among themselves arbitrarily.
3.  **Objective Function**: The sum of coordinates $S = \sum x_k$ can be expressed as $S = N \cdot x_1 + \sum_{k=1}^{N-1} (N-k) d_k$. To minimize $S$, we need to minimize the weighted sum of differences. The weights $(N-k)$ are strictly decreasing ($N-1, N-2, \dots, 1$). By the rearrangement inequality, we should assign the smallest differences to the largest weights.
4.  **Algorithm**:
    -   Compute the initial differences $d_1, \dots, d_{N-1}$.
    -   Split these differences into two lists: one containing differences at odd positions (indices 1, 3, ...) and one at even positions (indices 2, 4, ...). Note that in 0-based implementation, this corresponds to indices 0, 2, ... and 1, 3, ... of the difference array.
    -   Sort both lists in ascending order.
    -   Reconstruct the minimal sum by placing the sorted odd-positioned differences back into odd positions and sorted even-positioned differences into even positions, then calculating the weighted sum.

Complexity:
-   Time Complexity: $O(N \log N)$ due to sorting the difference lists.
-   Space Complexity: $O(N)$ to store the differences and lists.
-   Constraints: $N \le 2 \times 10^5$, coordinates $\le 10^{12}$. The sum fits within a 64-bit integer, and Python handles arbitrary precision integers automatically.
