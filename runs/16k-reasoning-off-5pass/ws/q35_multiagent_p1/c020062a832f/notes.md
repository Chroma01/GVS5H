
## ideation
The core difficulty lies in efficiently updating the inversion count as we shift from $k$ to $k+1$. A naive recomputation for each $k$ would be $O(M \cdot N \log N)$ or $O(M \cdot N)$, which is too slow given $N, M \le 2 \times 10^5$.

The key insight is that when moving from shift $k$ to $k+1$, only elements with value $v = M - 1 - k$ "wrap around" from $M-1$ to $0$. All other elements simply increment by 1, preserving their relative order.
- Elements that don't wrap maintain their relative inversion status with each other.
- Elements that wrap interact with non-wrapping elements. Specifically:
  - A wrapping element at index $i$ was $M-1$ and becomes $0$.
  - For any non-wrapping element at index $j$:
    - If $j > i$: Previously $B_i = M-1 > B_j$ (inversion). Now $B_i = 0 < B_j$ (no inversion). Inversion count decreases by 1.
    - If $j < i$: Previously $B_j < M-1 = B_i$ (no inversion). Now $B_j > 0 = B_i$ (inversion). Inversion count increases by 1.

Thus, the change in inversion count $\Delta_k$ when transitioning from $k$ to $k+1$ is:
$$ \Delta_k = (\text{# non-wrapping elements to the left of wrapping elements}) - (\text{# non-wrapping elements to the right of wrapping elements}) $$
Let $S_v$ be the set of indices where $A_i = v$. For a specific value $v$, let its positions be $p_1, p_2, \dots, p_c$.
- Number of non-wrapping elements to the left of $p_m$ is $p_m - (m-1)$ (total left minus other wrapping elements to the left).
- Number of non-wrapping elements to the right of $p_m$ is $(N - 1 - p_m) - (c - m)$ (total right minus other wrapping elements to the right).

We can precompute the total change $\Delta_v$ for each value $v \in [0, M-1]$ in $O(N)$ time by iterating through the positions of each value. Then, we compute the initial inversion count for $k=0$ in $O(N \log N)$ and apply the precomputed deltas sequentially.

Pitfalls to avoid:
1. Incorrectly calculating the number of wrapping elements to the left/right of a specific instance.
2. Off-by-one errors in indices.
3. Using $O(N)$ per step for the delta calculation instead of precomputing.

## worker: (None)
The solution efficiently computes the inversion numbers for all shifts $k=0 \dots M-1$.
1. **Initial Inversion Count**: Computed in $O(N \log M)$ using a Fenwick Tree (BIT).
2. **Delta Precomputation**: The key insight is that transitioning from shift $k$ to $k+1$ only affects pairs involving elements that "wrap around" (value $M-1-k$ becomes $0$). For each value $v$, we precompute the net change in inversions $\Delta_v$ caused by all occurrences of $v$ wrapping. This is done by iterating through the positions of each value $v$. For each occurrence at index $p$, we calculate how many non-$v$ elements are to its left and right. The total change for value $v$ is the sum of (left non-$v$ - right non-$v$) for all its occurrences. This step takes $O(N)$ total time because each element's position is processed exactly once.
3. **Sequential Application**: We start with the inversion count for $k=0$ and sequentially apply the precomputed deltas. The transition from $k$ to $k+1$ corresponds to adding $\Delta_{M-1-k}$. This allows us to compute all answers in $O(M)$ time after the initial setup.
4. **Complexity**: Total time complexity is $O(N \log M + N + M) = O(N \log M + M)$, which fits well within the constraints $N, M \le 2 \times 10^5$. Space complexity is $O(N + M)$.
