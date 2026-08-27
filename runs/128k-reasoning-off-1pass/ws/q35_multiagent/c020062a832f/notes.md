
## ideation
The core difficulty lies in efficiently computing the inversion number for $M$ different sequences, where $M$ and $N$ are up to $2 \times 10^5$. A naive $O(N \log N)$ calculation for each $k$ would result in $O(M N \log N)$, which is too slow.

The key insight is that transitioning from $k$ to $k+1$ involves adding 1 to all elements modulo $M$. This operation only changes the relative order of pairs where one element "wraps around" from $M-1$ to $0$ and the other does not.
- Elements with value $M-1$ become $0$.
- All other elements $x$ become $x+1$.
- Since $0 < x+1$ for any $x \ge 0$, the wrapping elements become smaller than all non-wrapping elements.

Let $W$ be the set of indices of elements that wrap (i.e., $A_i + k = M - 1$) and $S$ be the set of indices of elements that do not wrap.
- Pairs within $W$: relative order unchanged (both increase by 1, then wrap).
- Pairs within $S$: relative order unchanged (both increase by 1).
- Pairs $(i, j)$ with $i \in W, j \in S$: Previously $B_i = M-1 > B_j$. Now $B_i = 0 < B_j$. Inversion is lost.
- Pairs $(i, j)$ with $i \in S, j \in W$: Previously $B_i < M-1 = B_j$. Now $B_i > 0 = B_j$. Inversion is gained.

The change in inversion count $\Delta$ is:
$\Delta = (\text{# pairs } i \in S, j \in W \text{ with } i < j) - (\text{# pairs } i \in W, j \in S \text{ with } i < j)$.

We can compute the initial inversion count for $k=0$ using a Fenwick Tree (BIT) in $O(N \log N)$.
Then, we iterate $k$ from $0$ to $M-2$. At each step, we identify the elements that wrap (those with current value $M-1$, which corresponds to original $A_i = M - 1 - k$).
To efficiently calculate the number of non-wrapping elements to the left/right of the wrapping elements, we maintain a BIT that tracks the positions of the "active" (non-wrapping) elements. Initially, all elements are active. When an element wraps, we remove it from the BIT (update its position to 0).
For each wrapping element $j$, we query the BIT for the count of active elements to its left ($L_j$) and right ($R_j$). The contribution to $\Delta$ is $\sum_{j \in W} (L_j - R_j)$.
After updating the inversion count, we remove the wrapping elements from the BIT.

Pitfalls:
- Handling $A_i=0$: It never wraps in the range $k=0 \dots M-1$ because it becomes $1, 2, \dots, M-1$. It would wrap at $k=M$, which is outside our loop. So we only consider $A_i > 0$ for wrapping. Specifically, an element with original value $v$ wraps when $k = M - v$. If $v=0$, $k=M$, which is not processed.
- The BIT should support point updates and prefix sums.
- Indices are 1-based for BIT convenience.

## worker: (none)
The solution efficiently computes the inversion numbers for all $k \in [0, M-1]$ by leveraging the structure of the transformation $B_i = (A_i + k) \pmod M$.

1.  **Initial Inversion Count**: We compute the inversion number for $k=0$ using a Fenwick Tree (BIT) in $O(N \log M)$ time. This is standard.
2.  **Transition Logic**: Moving from $k$ to $k+1$ involves adding 1 to all elements modulo $M$. The relative order of any pair $(A_i, A_j)$ only changes if exactly one of them wraps around from $M-1$ to $0$.
    - If $A_i$ wraps and $A_j$ doesn't, $A_i$ goes from being the largest to the smallest, potentially losing inversions if $i < j$ (since $A_i > A_j$ becomes $0 < A_j+1$) or gaining if $i > j$.
    - Specifically, for a set of wrapping indices $W$ and non-wrapping indices $S$:
        - Pairs within $W$ or within $S$ maintain their relative order.
        - Pairs $(i, j)$ with $i \in S, j \in W, i < j$: Previously $A_i < M-1 = A_j$ (no inversion). After wrap, $A_i+1 > 0 = A_j$ (inversion). **Gain 1**.
        - Pairs $(i, j)$ with $i \in W, j \in S, i < j$: Previously $A_i = M-1 > A_j$ (inversion). After wrap, $0 = A_i < A_j+1$ (no inversion). **Lose 1**.
    - The net change $\Delta = \sum_{j \in W} (\text{# active } i < j) - \sum_{i \in W} (\text{# active } j > i)$.
3.  **Efficient Updates**: We maintain a second BIT (`bit_pos`) that tracks the positions of "active" (non-wrapping) elements. Initially, all $N$ elements are active.
    - We group indices by their original value $A_i$. An element with original value $v$ wraps at step $k = M - v$.
    - For each $k$ from $0$ to $M-2$, we identify the elements wrapping at this transition (those with $A_i = M - 1 - k$).
    - For each such element, we query `bit_pos` to find the number of active elements to its left and right, compute its contribution to $\Delta$, and update the total inversion count.
    - Finally, we remove these wrapping elements from `bit_pos` (mark them as inactive) for subsequent steps.
4.  **Complexity**:
    - Initial inversion count: $O(N \log M)$.
    - Transitions: Each element wraps exactly once (if at all). For each wrap, we perform BIT queries and updates. Total time for all transitions is $O(N \log N)$.
    - Overall Time Complexity: $O(N \log N + N \log M)$, which fits within the constraints $N, M \le 2 \times 10^5$.
    - Space Complexity: $O(N + M)$ for the BITs and wrapper lists.
