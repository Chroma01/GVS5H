
## ideation
The problem asks for the number of ways to orient tiles on a toroidal grid such that line segments form closed loops (no dead ends). This condition implies that for every edge shared by two cells (or wrapping around), either both cells have a segment connecting to that edge, or neither does.

This condition decouples into two independent sets of constraints:
1.  **Horizontal Consistency**: For every row, the "horizontal port" status (Left/Right) must be consistent across the boundaries.
2.  **Vertical Consistency**: For every column, the "vertical port" status (Top/Bottom) must be consistent across the boundaries.

**Analysis of Tile Types:**
*   **Type B**: Connects opposite edges.
    *   Horizontal orientation: Connects Left and Right. (Horizontal ports: 1, 1; Vertical ports: 0, 0)
    *   Vertical orientation: Connects Top and Bottom. (Horizontal ports: 0, 0; Vertical ports: 1, 1)
*   **Type A**: Connects adjacent edges.
    *   Orientations: Top-Left, Top-Right, Bottom-Left, Bottom-Right.
    *   Each Type A tile has exactly one horizontal port (Left or Right) and exactly one vertical port (Top or Bottom).
    *   Specifically:
        *   Top-Left: H=(1,0), V=(1,0) [Left, Top]
        *   Top-Right: H=(0,1), V=(1,0) [Right, Top]
        *   Bottom-Left: H=(1,0), V=(0,1) [Left, Bottom]
        *   Bottom-Right: H=(0,1), V=(0,1) [Right, Bottom]

**Decomposition:**
Because Type A tiles have independent horizontal and vertical components, and Type B tiles choose either a full horizontal component or a full vertical component, we can solve the horizontal and vertical problems independently.

**Horizontal Problem:**
Consider a single row. Let $e_j$ be the binary variable indicating if there is a segment crossing the boundary between column $j-1$ and $j$ (for $j=0 \dots W-1$, with wrap-around).
*   If cell $(i,j)$ is **Type B**:
    *   It must be either Horizontal ($e_j=1, e_{j+1}=1$) or Vertical ($e_j=0, e_{j+1}=0$).
    *   In both cases, $e_j = e_{j+1}$.
*   If cell $(i,j)$ is **Type A**:
    *   It must be Left-active ($e_j=1, e_{j+1}=0$) or Right-active ($e_j=0, e_{j+1}=1$).
    *   In both cases, $e_j \neq e_{j+1}$.

This creates a system of equations on the cycle $e_0, \dots, e_{W-1}$:
*   $e_j = e_{j+1}$ if $S_{ij} = 'B'$
*   $e_j \neq e_{j+1}$ if $S_{ij} = 'A'$

Traversing the cycle, each 'A' flips the value of $e$, and each 'B' preserves it. For a solution to exist, the total number of flips must be even (so we return to the starting value).
*   If the number of 'A's in the row is **odd**, there are **0** valid horizontal configurations.
*   If the number of 'A's in the row is **even**, there are **2** valid configurations (all $e_j=0$ or all $e_j=1$, consistent with the flips).

**Vertical Problem:**
The same logic applies to columns.
*   If the number of 'A's in a column is **odd**, there are **0** valid vertical configurations.
*   If the number of 'A's in a column is **even**, there are **2** valid vertical configurations.

**Total Count:**
Since horizontal and vertical choices are independent, the total number of ways is the product of the number of ways for each row and column.
Let $H_{valid}$ be the number of rows with an even number of 'A's.
Let $V_{valid}$ be the number of columns with an even number of 'A's.
Total ways = $2^{H_{valid}} \times 2^{V_{valid}} = 2^{H_{valid} + V_{valid}}$.

We need to compute this value modulo 998244353.

## worker: (none)
The problem requires counting valid tile orientations on a toroidal grid such that line segments form closed loops (no dead ends). This condition implies that for every boundary between cells (including wrap-around), the presence of a segment connecting to that boundary must be consistent on both sides.

This condition decouples into two independent problems:
1.  **Horizontal Consistency**: For each row, the horizontal ports (Left/Right) must match across column boundaries.
2.  **Vertical Consistency**: For each column, the vertical ports (Top/Bottom) must match across row boundaries.

**Tile Analysis:**
-   **Type B**: Connects opposite edges. It can be Horizontal (Left-Right) or Vertical (Top-Bottom).
    -   Horizontal: Contributes to horizontal ports (1, 1).
    -   Vertical: Contributes to vertical ports (1, 1).
-   **Type A**: Connects adjacent edges. It has 4 orientations.
    -   Each orientation has exactly one horizontal port (Left or Right) and one vertical port (Top or Bottom).

**Horizontal Problem:**
For a fixed row, let $e_j$ be the state of the boundary between column $j-1$ and $j$.
-   If cell $(i,j)$ is Type B, $e_j = e_{j+1}$.
-   If cell $(i,j)$ is Type A, $e_j \neq e_{j+1}$.
This forms a cycle. A solution exists if and only if the number of 'A's in the row is even (since each 'A' flips the state, and we must return to the initial state after a full cycle). If even, there are 2 solutions ($e_j=0$ for all $j$, or $e_j=1$ for all $j$). If odd, 0 solutions.

**Vertical Problem:**
Identical logic applies to columns. A solution exists if and only if the number of 'A's in the column is even. If even, 2 solutions. If odd, 0 solutions.

**Total Count:**
Since horizontal and vertical choices are independent, the total number of ways is $2^{H_{valid}} \times 2^{V_{valid}} = 2^{H_{valid} + V_{valid}}$, where $H_{valid}$ is the number of rows with even 'A' count and $V_{valid}$ is the number of columns with even 'A' count.

The algorithm counts 'A's in each row and column, sums the valid counts, and computes $2^{\text{sum}} \pmod{998244353}$. Time complexity is $O(HW)$ per test case, which fits within the constraints.
