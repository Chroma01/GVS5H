
## ideation
The core difficulty lies in efficiently computing the inversion count for $M$ different shifts of the array $A$. A naive $O(N \log N)$ computation for each $k$ would result in $O(MN \log N)$, which is too slow given $N, M \le 2 \times 10^5$.

The key insight is that moving from shift $k$ to $k+1$ corresponds to adding 1 to all elements modulo $M$. This operation only changes the relative order of elements when they "wrap around" from $M-1$ to $0$. Specifically, at step $k$, the elements that wrap are those with original value $A_i = M - 1 - k$.

Let $W_k$ be the set of indices where $A_i = M - 1 - k$. Let $c = |W_k|$.
When these elements wrap from $M-1$ to $0$:
1. They were previously greater than all non-wrapping elements (values $0 \dots M-2$).
2. They become smaller than all non-wrapping elements (which become $1 \dots M-1$).

The change in inversion count depends on the pairs formed by wrapping elements ($W_k$) and non-wrapping elements ($V \setminus W_k$).
- Pairs $(i, j)$ with $i \in W_k, j \notin W_k, i < j$: Previously an inversion ($M-1 > \text{other}$), now not ($0 < \text{other}$). Loss of 1.
- Pairs $(i, j)$ with $i \notin W_k, j \in W_k, i < j$: Previously not an inversion ($\text{other} < M-1$), now an inversion ($\text{other} > 0$). Gain of 1.

Let $P_{after}$ be the number of pairs $(i, j)$ such that $i \notin W_k, j \in W_k, i < j$.
Let $P_{before}$ be the number of pairs $(i, j)$ such that $i \in W_k, j \notin W_k, i < j$.
Total pairs between $W_k$ and $V \setminus W_k$ is $c(N-c)$.
$P_{before} + P_{after} = c(N-c)$.
The net change $\Delta = P_{after} - P_{before} = P_{after} - (c(N-c) - P_{after}) = 2 P_{after} - c(N-c)$.

To compute $P_{after}$ efficiently:
For each $j \in W_k$, the number of non-wrapping elements before $j$ is $j - (\text{count of elements in } W_k \text{ at indices } \le j)$.
Since we can store the indices for each value in sorted order, we can iterate through $W_k$ and compute this sum in $O(c)$ time.
Since $\sum c = N$, the total time for all updates is $O(N)$.
The initial inversion count for $k=0$ takes $O(N \log N)$ using a Fenwick Tree.
Total complexity: $O(N \log N + M)$.

Pitfalls:
- Integer overflow: Inversion counts can be up to $N(N-1)/2 \approx 2 \cdot 10^{10}$, so 64-bit integers are required. Python handles this automatically.
- Indexing: Ensure 0-based vs 1-based indexing is consistent. The problem uses 1-based indexing for description, but implementation is easier with 0-based.
- The wrap value for step $k$ (going to $k+1$) is $M - 1 - k$. For $k=M-1$, there is no next step, so we just print and stop.

## worker: (None)
The solution efficiently computes the inversion counts for all $M$ shifts by leveraging the fact that only elements wrapping from $M-1$ to $0$ change their relative order with respect to non-wrapping elements.

1.  **Initial Inversion Count**: Computed in $O(N \log M)$ using a Fenwick Tree (BIT).
2.  **Index Grouping**: Indices of each value $v \in [0, M-1]$ are stored in `indices_by_val`. This takes $O(N)$.
3.  **Iterative Update**: For each $k$ from $0$ to $M-1$:
    *   The current inversion count is recorded.
    *   To move to $k+1$, elements with $A_i = M - 1 - k$ wrap from $M-1$ to $0$.
    *   Let $W$ be the set of indices of these elements, and $c = |W|$.
    *   The change in inversions $\Delta$ is derived from pairs between $W$ and $V \setminus W$.
    *   $\Delta = 2 P_{after} - c(N-c)$, where $P_{after}$ is the number of pairs $(i, j)$ with $i < j$, $A_i \neq \text{val}$, $A_j = \text{val}$.
    *   $P_{after}$ is computed in $O(c)$ by iterating through the sorted list of indices in $W$.
    *   Since $\sum c = N$, the total time for all updates is $O(N)$.
4.  **Complexity**: $O(N \log M + N + M) = O(N \log M + M)$, which fits within the constraints.
