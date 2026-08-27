
## ideation
The problem asks for the number of valid tile orientations on a toroidal grid such that line segments form closed loops (no dead ends). This is equivalent to ensuring that for every shared edge between adjacent cells, either both cells have a segment connecting to that edge, or neither does.

1.  **Tile Analysis**:
    *   **Type B (Straight)**: Connects opposite edges.
        *   Orientation 1 (Top-Bottom): Active vertical ports (Top, Bottom), inactive horizontal ports (Left, Right).
        *   Orientation 2 (Left-Right): Active horizontal ports (Left, Right), inactive vertical ports (Top, Bottom).
    *   **Type A (Corner)**: Connects adjacent edges.
        *   All 4 orientations (TR, RB, BL, LT) have exactly one active vertical port and one active horizontal port.
        *   Crucially, for Type A, the choice of orientation determines *which* vertical port (Top or Bottom) and *which* horizontal port (Left or Right) is active.

2.  **Edge Variables**:
    Let $h_{i,j}$ be the state of the horizontal edge between cell $(i,j)$ and $(i, j+1 \pmod W)$.
    Let $v_{i,j}$ be the state of the vertical edge between cell $(i,j)$ and $(i+1 \pmod H, j)$.
    The condition "no dead ends" implies:
    *   Left port of $(i,j)$ is active $\iff h_{i, j-1} = 1$.
    *   Right port of $(i,j)$ is active $\iff h_{i, j} = 1$.
    *   Top port of $(i,j)$ is active $\iff v_{i-1, j} = 1$.
    *   Bottom port of $(i,j)$ is active $\iff v_{i, j} = 1$.

3.  **Constraints per Cell**:
    *   **Type B (TB)**: Requires $v_{i-1,j}=1, v_{i,j}=1$ and $h_{i,j-1}=0, h_{i,j}=0$.
    *   **Type B (LR)**: Requires $h_{i,j-1}=1, h_{i,j}=1$ and $v_{i-1,j}=0, v_{i,j}=0$.
    *   **Type A**: Requires exactly one of $\{v_{i-1,j}, v_{i,j}\}$ to be 1, and exactly one of $\{h_{i,j-1}, h_{i,j}\}$ to be 1.
        *   TR: $v_{i-1,j}=1, h_{i,j}=1$ (implies $v_{i,j}=0, h_{i,j-1}=0$).
        *   RB: $v_{i,j}=1, h_{i,j}=1$ (implies $v_{i-1,j}=0, h_{i,j-1}=0$).
        *   BL: $v_{i,j}=1, h_{i,j-1}=1$ (implies $v_{i-1,j}=0, h_{i,j}=0$).
        *   LT: $v_{i-1,j}=1, h_{i,j-1}=1$ (implies $v_{i,j}=0, h_{i,j}=0$).

4.  **Decomposition**:
    The constraints on $h$ variables and $v$ variables are coupled only within Type A cells. However, notice that for Type A cells, the choice of orientation is determined by the values of the surrounding edges.
    Specifically, if we fix the entire set of horizontal edge values $\{h_{i,j}\}$ and vertical edge values $\{v_{i,j}\}$, we can check if a valid orientation exists for each cell.
    *   For Type B cells, the edge values are fixed by the tile type. If the fixed values don't match the global edge configuration, the configuration is invalid.
    *   For Type A cells, the edge values must satisfy the "one active vertical, one active horizontal" rule. If they do, there is exactly 1 orientation that matches those specific edge values. If they don't (e.g., both vertical edges active), there are 0 orientations.

    Thus, the problem reduces to counting the number of binary matrices $H$ (size $H \times W$) and $V$ (size $H \times W$) such that:
    1.  For every cell $(i,j)$ with Type B:
        *   If TB: $v_{i-1,j}=1, v_{i,j}=1, h_{i,j-1}=0, h_{i,j}=0$.
        *   If LR: $h_{i,j-1}=1, h_{i,j}=1, v_{i-1,j}=0, v_{i,j}=0$.
    2.  For every cell $(i,j)$ with Type A:
        *   $v_{i-1,j} + v_{i,j} = 1$
        *   $h_{i,j-1} + h_{i,j} = 1$

    Notice that the constraints on $H$ and $V$ are **completely independent**.
    *   The constraints on $V$ only involve $V$ entries and Type B/TB or Type A cells.
    *   The constraints on $H$ only involve $H$ entries and Type B/LR or Type A cells.
    
    We can solve for the number of valid $V$ configurations ($N_V$) and valid $H$ configurations ($N_H$) independently. The total answer is $N_V \times N_H \pmod{998244353}$.

5.  **Solving for $N_V$**:
    The constraints on $V$ form a system of linear equations over GF(2) or simple logical constraints on a cycle.
    For each column $j$, the variables are $v_{0,j}, v_{1,j}, \dots, v_{H-1,j}$.
    The constraints come from cells in column $j$.
    *   If cell $(i,j)$ is Type B (TB): $v_{i-1,j}=1, v_{i,j}=1$.
    *   If cell $(i,j)$ is Type B (LR): $v_{i-1,j}=0, v_{i,j}=0$.
    *   If cell $(i,j)$ is Type A: $v_{i-1,j} + v_{i,j} = 1$.

    This defines a chain of constraints along the column. Since it's a torus, it's a cycle. We can check if the constraints are consistent and count the number of solutions.
    Actually, it's simpler: The constraints propagate.
    Start with $v_{0,j}$.
    - If cell $(0,j)$ is A: $v_{1,j} = 1 - v_{0,j}$.
    - If cell $(0,j)$ is TB: $v_{0,j}=1, v_{1,j}=1$. (Fixes $v_{0,j}$)
    - If cell $(0,j)$ is LR: $v_{0,j}=0, v_{1,j}=0$. (Fixes $v_{0,j}$)
    
    We can iterate through the column. If we encounter a fixed value that contradicts the propagated value, the count is 0. If we complete the cycle and the last constraint is consistent with the first, we have 1 solution (if fixed) or 2 solutions (if free)?
    Actually, since it's a linear system on a cycle, there are either 0 or 2 solutions, or 1 if fully constrained?
    Let's trace:
    If there are no Type B tiles in the column, all are Type A. $v_{i} = 1 - v_{i-1}$.
    $v_1 = 1-v_0, v_2 = v_0, \dots$.
    The condition $v_H = v_0$ (torus) implies $v_0 = v_0$ if H is even, or $v_0 = 1-v_0$ (impossible) if H is odd.
    So for all A, if H is even, 2 solutions. If H is odd, 0 solutions.
    
    If there are Type B tiles, they fix values. We just need to check consistency.
    Algorithm for one column:
    1. Initialize an array `val` of size H with -1 (unknown).
    2. Process Type B constraints: Set `val[i-1]=1, val[i]=1` for TB, `val[i-1]=0, val[i]=0` for LR. If conflict, return 0.
    3. Process Type A constraints: For each A at row i, `val[i-1] + val[i] = 1`.
       If both known, check sum. If one known, set other. If none, leave unknown.
    4. After processing all, if there are unknowns, they form independent cycles? No, the graph is a single cycle.
       If there is at least one fixed value, all values in the column are determined. Check consistency of the wrap-around.
       If there are NO fixed values (all A), then if H is even, 2 solutions; else 0.

6.  **Solving for $N_H$**:
    Identical logic, but iterating over rows and using horizontal constraints.

7.  **Implementation**:
    - Parse input.
    - For each test case:
        - Compute $N_V$: Iterate each column. Apply constraints.
        - Compute $N_H$: Iterate each row. Apply constraints.
        - Result is $(N_V \times N_H) \% MOD$.

## worker: Implement the solution logic: parse input, define 
The problem asks for the number of valid tile placements on a toroidal grid such that line segments form closed loops (no dead ends). This condition is equivalent to requiring that for every shared edge between adjacent cells, either both cells have a segment connecting to that edge, or neither does.

By defining binary variables for the state of each horizontal and vertical edge between cells, we can translate the tile constraints into logical equations on these edge variables.
- For a **Type B** tile, the two possible orientations (Top-Bottom or Left-Right) imply that the two vertical edges (or two horizontal edges) connected to the tile must have the **same** state (both active or both inactive).
- For a **Type A** tile, the four possible orientations imply that the two vertical edges connected to the tile must have **different** states (one active, one inactive), and similarly for the horizontal edges.

Crucially, the constraints on the vertical edge variables are independent of the constraints on the horizontal edge variables. The total number of valid placements is the product of the number of valid vertical edge configurations ($N_V$) and the number of valid horizontal edge configurations ($N_H$).

For each column, the vertical edge constraints form a cycle of equations $v_{i-1} \oplus v_i = d_i$, where $d_i=0$ for Type B and $d_i=1$ for Type A. A solution exists if and only if the XOR sum of all $d_i$ in the column is 0. If it is 0, there are 2 solutions (corresponding to $v_0=0$ or $v_0=1$). If it is 1, there are 0 solutions. The same logic applies to rows for horizontal edges.

The algorithm iterates through each column to compute $N_V$ and each row to compute $N_H$, multiplying the results modulo 998244353. The complexity is $O(HW)$ per test case, which fits within the constraints.
