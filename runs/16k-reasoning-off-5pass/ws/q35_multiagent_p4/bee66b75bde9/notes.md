
## ideation
The core difficulty lies in correctly modeling the constraints imposed by the "black prefix" property for both rows and columns. The key insight is that the coloring is determined by two parameters per row/column: $R_r$ (number of black cells in row $r$) and $C_c$ (number of black cells in column $c$). A cell $(r, c)$ is black if and only if $c \le R_r$ AND $r \le C_c$. It is white if and only if $c > R_r$ OR $r > C_c$.

To satisfy the conditions:
1.  **Lower Bounds from Black Cells**: For each row $r$, $R_r$ must be at least the maximum column index of any black cell in that row. Let this be $R_r^{min}$. Similarly, for each column $c$, $C_c$ must be at least the maximum row index of any black cell in that column, denoted $C_c^{min}$.
2.  **Minimality Argument**: The condition for a white cell $(r, c)$ is $c > R_r \lor r > C_c$. Increasing $R_r$ or $C_c$ makes this condition harder to satisfy (shrinks the region where it's true). Therefore, the "best chance" of satisfying all white cell constraints is to choose the smallest possible valid values for $R_r$ and $C_c$, which are $R_r^{min}$ and $C_c^{min}$.
3.  **Verification**: After setting $R_r = R_r^{min}$ and $C_c = C_c^{min}$, we must verify that every pre-colored white cell $(r, c)$ satisfies $c > R_r \lor r > C_c$. If any white cell fails this (i.e., it falls into the region defined as black by our parameters), then no solution exists. The black cells automatically satisfy their constraints by construction of the lower bounds.

Pitfalls to avoid:
-   Confusing row/column indices (1-based vs 0-based). The problem uses 1-based indexing.
-   Not handling rows/columns with no black cells correctly (their min value is 0).
-   Assuming that satisfying white cells is sufficient without checking if the derived $R$ and $C$ values are consistent with each other. However, since $R$ and $C$ are independent variables in the definition (except for the cell color logic), and we derived them independently from black cells, the only conflict can arise if a white cell is forced to be black by the derived parameters.

## worker: (None)
The problem asks if we can assign a "black prefix length" $R_i$ for each row $i$ and $C_j$ for each column $j$ such that the given pre-colored cells are consistent with the rule: cell $(r, c)$ is black iff $c \le R_r$ AND $r \le C_c$.

1.  **Lower Bounds**: From each black cell $(r, c)$, we derive that $R_r \ge c$ and $C_c \ge r$. To maximize the chance of satisfying white cell constraints, we should pick the smallest possible values for $R_r$ and $C_c$. Thus, we set $R_r = \max(\{c \mid (r,c) \text{ is black}\} \cup \{0\})$ and $C_c = \max(\{r \mid (r,c) \text{ is black}\} \cup \{0\})$.
2.  **White Cell Verification**: For each white cell $(r, c)$, the condition requires that it is NOT the case that ($c \le R_r$ AND $r \le C_c$). This is equivalent to $c > R_r$ OR $r > C_c$. If any white cell violates this (i.e., $c \le R_r$ AND $r \le C_c$), then it's impossible to satisfy the conditions, and we output "No".
3.  **Complexity**: We process $M$ cells to build the dictionaries $R_{min}$ and $C_{min}$, which takes $O(M)$ time. Then we iterate through the white cells (at most $M$) to verify them, taking another $O(M)$ time. The space complexity is $O(M)$ to store the dictionaries and white cells. Given $M \le 2 \times 10^5$, this is efficient.
