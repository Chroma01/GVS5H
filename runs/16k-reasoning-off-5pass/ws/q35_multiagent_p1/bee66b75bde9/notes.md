
## ideation
The problem asks whether we can assign a "black count" $R_i$ for each row $i$ (number of black cells from the left) and $C_j$ for each column $j$ (number of black cells from the top) such that the pre-colored cells are consistent with the grid structure.

The grid structure implies that cell $(r, c)$ is black if and only if $c \le R_r$ AND $r \le C_c$.
This leads to two types of constraints:
1. **Pre-colored Black cells $(r, c)$**: Must satisfy $c \le R_r$ and $r \le C_c$. This gives lower bounds:
   $R_r \ge \max(\{c \mid (r,c) \text{ is Black}\} \cup \{0\})$
   $C_c \ge \max(\{r \mid (r,c) \text{ is Black}\} \cup \{0\})$
   Let these minimal values be $R_r^{min}$ and $C_c^{min}$.

2. **Prefix Consistency**:
   - For row $r$ to have black cells exactly at $1 \dots R_r$, it must be that for all $c \in \{1, \dots, R_r\}$, the cell $(r, c)$ is black. This requires $r \le C_c$ for all $c \in \{1, \dots, R_r\}$.
   - For column $c$ to have black cells exactly at $1 \dots C_c$, it must be that for all $r \in \{1, \dots, C_c\}$, the cell $(r, c)$ is black. This requires $c \le R_r$ for all $r \in \{1, \dots, C_c\}$.

3. **Pre-colored White cells $(r, c)$**: Must NOT be black. So, $\neg (c \le R_r \land r \le C_c)$, which means $c > R_r$ OR $r > C_c$.

The minimal assignment $R_r = R_r^{min}$ and $C_c = C_c^{min}$ is the best candidate to satisfy the white constraints because increasing $R_r$ or $C_c$ only makes it more likely for a white cell to become black. However, this minimal assignment might violate the prefix consistency constraints. If it does, we must increase some $R_r$ or $C_c$, which might trigger further increases (propagation).

We can model this as a constraint propagation problem:
- Initialize $R_r = R_r^{min}$ and $C_c = C_c^{min}$.
- Use a queue to propagate changes.
- When $R_r$ increases to $new\_R$, we must ensure $C_c \ge r$ for all $c \in [1, new\_R]$. If any $C_c < r$, update $C_c = r$ (or higher) and push $c$ to the queue.
- When $C_c$ increases to $new\_C$, we must ensure $R_r \ge c$ for all $r \in [1, new\_C]$. If any $R_r < c$, update $R_r = c$ (or higher) and push $r$ to the queue.

Since $N$ is up to $10^9$, we cannot iterate over all cells. However, $M$ is up to $2 \cdot 10^5$. The number of distinct values for $R_r$ and $C_c$ is limited by the input and the propagation. We can use a Segment Tree with Lazy Propagation (or a similar structure like a Disjoint Set Union for range updates) to efficiently handle range max updates and point queries. Given the ranges are always $[1, K]$, we can use a dynamic segment tree or coordinate compression. Coordinate compression on the values of $R_r^{min}$ and $C_c^{min}$ is sufficient because updates only happen at these values or values forced by them.

Finally, after propagation, we check if all white cells satisfy the condition $c > R_c$ OR $r > C_c$. If any white cell violates this, output No.

Pitfalls:
- Large $N$ requires efficient range updates.
- Propagation must be correct and complete.
- White cell check must be done after final $R$ and $C$ values are determined.

## worker: Implement reading input and computing initial $R_r
The solution uses a dynamic segment tree to handle range max updates and range min queries efficiently, given the large grid size $N \le 10^9$. The key insight is that the constraints on $R_r$ and $C_c$ propagate: if a row $r$ has $R_r$ black cells, then all columns $c \le R_r$ must have $C_c \ge r$. Similarly for columns.

1.  **Initialization**: Compute initial lower bounds $R_r^{min}$ and $C_c^{min}$ from pre-colored black cells.
2.  **Propagation**: Use two dynamic segment trees (one for $R$, one for $C$) to maintain the current values. Use queues to propagate updates. When $R_r$ increases, it forces $C_c \ge r$ for all $c \le R_r$. The segment tree allows us to find if any $C_c < r$ in the range $[1, R_r]$ and update them. The `propagate_C_updates` function traverses the tree to find and update all such $C_c$ values, adding newly updated or activated columns to the queue.
3.  **Consistency Check**: After propagation, check all pre-colored white cells. A white cell $(r, c)$ is invalid if the final $R_r$ and $C_c$ imply it should be black (i.e., $c \le R_r$ and $r \le C_c$).

The complexity is roughly $O(M \log N)$ due to the segment tree operations, which fits within the time limits for $M \le 2 \cdot 10^5$ and $N \le 10^9$.
