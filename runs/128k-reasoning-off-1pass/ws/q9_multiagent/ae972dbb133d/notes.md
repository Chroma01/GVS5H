
## ideation
**Core Difficulty**:
The problem asks for the number of valid rotations of tiles in a grid (with wrap-around torus topology) such that the resulting line segments form a continuous flow with no dead ends.
- **Type A**: Connects two adjacent edges (e.g., Left-Right, Top-Bottom, etc.).
- **Type B**: Connects two opposite edges (e.g., Left-Right, Top-Bottom).
- **Constraint**: For any edge between two cells, either both have a segment crossing it, or neither does.

**Key Insight**:
1.  **Flow Conservation**: The condition "no dead ends" on a torus implies that every vertex (midpoint of an edge) has degree 2 in the graph formed by the segments. Since each tile contributes exactly one segment of length 1 (connecting two points on its boundary), the entire grid forms a collection of disjoint cycles covering all edges.
2.  **Tile Types and Directions**:
    -   Type A tiles have 4 possible orientations. They connect "adjacent" sides.
    -   Type B tiles have 2 possible orientations. They connect "opposite" sides.
    -   Crucially, for a Type A tile, if we fix the direction of the segment (e.g., it goes Right), the other end *must* go Down (or Up/Left depending on rotation). It cannot go Left-Right (that's Type B behavior) or Top-Bottom.
    -   For a Type B tile, if it goes Right, it must go Right (parallel) or Left (parallel)? No, Type B connects opposite edges. So if it connects Left and Right, it's horizontal. If it connects Top and Bottom, it's vertical.
3.  **Decomposition**:
    Let's analyze the constraints on the edges.
    -   Consider a horizontal edge between $(i, j)$ and $(i, j+1)$.
        -   If $(i, j)$ has a segment going Right, $(i, j+1)$ must have a segment coming from Left.
        -   Type A can provide a Right/Left segment (e.g., rotated 0° or 180°? No, Type A connects adjacent. Wait, let's re-read carefully).
        -   **Re-reading Type A**: "connecting the midpoints of two **adjacent** edges". Examples: Left-Top, Top-Right, Right-Bottom, Bottom-Left.
        -   **Re-reading Type B**: "connecting the midpoints of two **opposite** edges". Examples: Left-Right, Top-Bottom.
    -   **Implication**:
        -   A Type A tile **never** connects Left and Right. It never connects Top and Bottom.
        -   A Type B tile **can** connect Left and Right (Horizontal) or Top and Bottom (Vertical).
    -   **Constraint Logic**:
        -   If a horizontal edge between $(i,j)$ and $(i, j+1)$ is used (segment crosses it), then:
            -   $(i,j)$ must have a segment going Right. Since Type A cannot do this, $(i,j)$ **must be Type B**.
            -   $(i, j+1)$ must have a segment coming from Left. Since Type A cannot do this, $(i, j+1)$ **must be Type B**.
        -   If a horizontal edge is **not** used:
            -   $(i,j)$ cannot go Right.
            -   $(i, j+1)$ cannot come from Left.
            -   Type A tiles naturally satisfy this if oriented correctly (e.g., Top-Right, Bottom-Left, etc., but specifically avoiding Left/Right).
            -   Type B tiles must be oriented vertically (Top-Bottom) to avoid using the horizontal edge.
        -   **Conclusion**: The existence of a horizontal segment on an edge strictly requires both adjacent cells to be Type B. If either cell is Type A, the horizontal edge between them **cannot** be used.
        -   Similarly, the existence of a vertical segment on an edge strictly requires both adjacent cells to be Type B.

4.  **Global Structure**:
    -   Let $H_A$ be the set of cells with Type A, $H_B$ be the set of cells with Type B.
    -   If a cell $(i,j) \in H_A$, it cannot participate in any horizontal or vertical flow crossing its boundaries.
        -   This means for all neighbors of $(i,j)$, the edges connecting to $(i,j)$ are "blocked" (not used).
        -   Consequently, if $(i,j) \in H_A$, then for the horizontal edge to its right, the neighbor $(i, j+1)$ must NOT have a horizontal segment. Since $(i,j)$ doesn't provide a Right segment, the edge is unused.
        -   Does this force $(i, j+1)$ to be Type A? No. $(i, j+1)$ could be Type B, but it must be oriented vertically.
    -   However, consider the connectivity. The problem states the grid is a torus. The segments form cycles.
    -   If there is at least one Type A tile, does it break the cycle?
        -   Type A tiles connect adjacent edges (e.g., Left-Top). This creates a "corner" turn.
        -   Type B tiles connect opposite edges (e.g., Left-Right). This creates a "straight" line.
        -   On a torus, a continuous flow without dead ends means every vertex has degree 2.
        -   Let's look at the "flow" variable $x_{i,j} \in \{0, 1\}$ representing whether a horizontal edge is used, and $y_{i,j} \in \{0, 1\}$ for vertical.
        -   Actually, a simpler invariant exists. Consider the parity or the specific configuration types.
    -   **Hypothesis**: The answer is non-zero only if the grid allows a consistent assignment.
    -   Let's re-evaluate the "Type A blocks flow" idea.
        -   If $(i,j)$ is Type A, it has 4 orientations. None of them cross the Left-Right or Top-Bottom boundaries.
        -   Therefore, if $(i,j)$ is Type A, the horizontal edges incident to it are **never** used. The vertical edges incident to it are **never** used.
        -   Wait, is that true?
            -   Type A connects Left-Top.
                -   Left edge: Used (incoming/outgoing).
                -   Top edge: Used.
                -   Right edge: Not used.
                -   Bottom edge: Not used.
            -   So Type A **does** use its boundaries, but only adjacent ones.
            -   Type B connects Left-Right.
                -   Left: Used.
                -   Right: Used.
                -   Top: Not used.
                -   Bottom: Not used.
        -   **Correction**: My previous deduction was wrong. Type A *does* use edges.
        -   Let's restart the constraint analysis properly.

    **Correct Constraint Analysis**:
    Let $u_{i,j} \in \{0,1\}$ be the state of the horizontal edge between $(i,j)$ and $(i, j+1)$.
    Let $v_{i,j} \in \{0,1\}$ be the state of the vertical edge between $(i,j)$ and $(i+1, j)$.
    
    For a cell $(i,j)$:
    -   If it is Type A: It must connect exactly two adjacent edges.
        -   Possible connections (4 options): (Left, Top), (Top, Right), (Right, Bottom), (Bottom, Left).
        -   In terms of edge states $(u_{i,j}, u_{i,j-1}, v_{i,j}, v_{i-1,j})$ (using local coords):
            -   It must have exactly 2 active edges, and they must be adjacent.
    -   If it is Type B: It must connect exactly two opposite edges.
        -   Possible connections (2 options): (Left, Right) or (Top, Bottom).
        -   It must have exactly 2 active edges, and they must be opposite.

    **Consistency Conditions**:
    -   Horizontal edge $u_{i,j}$ (between $(i,j)$ and $(i, j+1)$):
        -   If $u_{i,j}=1$, then $(i,j)$ must have a Right segment, and $(i, j+1)$ must have a Left segment.
        -   For $(i,j)$ to have a Right segment:
            -   If Type A: Must be oriented (Top, Right) or (Right, Bottom).
            -   If Type B: Must be oriented (Left, Right).
        -   For $(i, j+1)$ to have a Left segment:
            -   If Type A: Must be oriented (Bottom, Left) or (Left, Top).
            -   If Type B: Must be oriented (Left, Right).
    
    **Key Observation**:
    Notice that for Type A, having a Right segment implies the other segment is either Top or Bottom.
    For Type B, having a Right segment implies the other segment is Left.
    
    Let's try to map the orientations to a global variable.
    Consider the grid as a graph where nodes are cells? No, edges are the segments.
    Actually, this looks like a system of equations over $\mathbb{Z}_2$ or similar.
    
    Let's define a variable $c_{i,j}$ for each cell representing its "rotation" or "phase".
    However, the types A and B are fixed.
    
    Let's test small cases or look for invariants.
    If we have a Type A tile, it forces a "turn".
    If we have a Type B tile, it forces a "straight".
    On a torus, the sum of turns along any cycle must be 0 mod 4 (or 2 depending on definition)?
    
    Let's reconsider the "Type A blocks horizontal flow" idea.
    If $(i,j)$ is Type A and oriented (Top, Right):
        -   Right edge is active.
        -   Top edge is active.
        -   Left, Bottom inactive.
    If $(i,j)$ is Type A and oriented (Left, Top):
        -   Left, Top active.
        -   Right, Bottom inactive.
    
    Is it possible to have a configuration where all constraints are satisfied?
    Yes, Sample 1 gives 2.
    Sample 1 Case 1:
    AAB
    AAB
    BBB
    Output: 2.
    
    Let's try to derive the formula.
    The problem is equivalent to counting the number of valid Eulerian orientations or similar?
    Actually, this is a known problem type: "Counting valid tilings/orientations on a grid with fixed types".
    
    **Crucial Realization**:
    The condition "no dead ends" on a torus with these specific tiles implies that the configuration corresponds to a **perfect matching** on a specific auxiliary graph, or more simply, the choices are highly constrained.
    
    Let's look at the degrees of freedom.
    If we fix the orientation of one tile, does it propagate?
    Consider the horizontal edges.
    If $(i,j)$ is Type B and we choose it to be horizontal (Left-Right), then $u_{i,j}=1$.
    This forces $(i, j+1)$ to have a Left segment.
    If $(i, j+1)$ is Type B, it can be horizontal (Left-Right) $\to u_{i,j+1}=1$.
    If $(i, j+1)$ is Type A, it must be oriented to have a Left segment. Options: (Bottom, Left) or (Left, Top).
        -   If (Bottom, Left): Vertical edge $v_{i,j+1}$ (bottom) is active. Horizontal $u_{i,j+1}$ (left) is active.
        -   If (Left, Top): Vertical edge $v_{i-1,j+1}$ (top) is active.
    
    This suggests that the "flow" can switch between horizontal and vertical modes at Type A tiles.
    However, Type B tiles *cannot* switch. They are either purely horizontal or purely vertical.
    
    **Hypothesis**: The grid must be decomposed into rows and columns of Type B tiles that form straight lines, interrupted by Type A tiles which act as "switches" or "terminators"?
    But Type A tiles don't terminate; they turn 90 degrees.
    
    Let's consider the **parity** of the number of Type A tiles? Or their positions?
    
    **Alternative Approach: Transfer Matrix / DP?**
    $H, W \le 10^6$ (sum), so $O(HW)$ is required.
    We can process row by row.
    State for DP: The configuration of the vertical edges connecting row $i$ and $i+1$.
    There are $W$ vertical edges. Each can be active (1) or inactive (0).
    So state space is $2^W$. Too big if $W$ is large.
    However, the constraints might force the state to be very simple (e.g., all 0, or all 1, or alternating).
    
    Let's check the constraints on the vertical edges for a valid row transition.
    For row $i$ to row $i+1$:
    Let $V_i$ be the vector of vertical edges $(v_{i,0}, v_{i,1}, \dots, v_{i, W-1})$.
    For each column $j$:
    -   Cell $(i,j)$ has vertical edge $v_{i,j}$ (bottom of $i$) and $v_{i-1,j}$ (top of $i$).
    -   Cell $(i+1,j)$ has vertical edge $v_{i,j}$ (top of $i+1$) and $v_{i+1,j}$ (bottom of $i+1$).
    
    If $v_{i,j}=1$:
    -   $(i,j)$ must have a Bottom segment.
    -   $(i+1,j)$ must have a Top segment.
    
    If $(i,j)$ is Type B:
    -   If it has Bottom segment, it MUST have Top segment (since B connects opposite).
    -   So $v_{i-1,j}$ must be 1.
    -   Thus, if $(i,j)$ is Type B and $v_{i,j}=1$, then $v_{i-1,j}=1$.
    -   Also, if $(i,j)$ is Type B and $v_{i-1,j}=0$, then $v_{i,j}=0$.
    -   Conclusion: For Type B, $v_{i,j} = v_{i-1,j}$. The vertical status propagates straight through.
    
    If $(i,j)$ is Type A:
    -   If it has Bottom segment, it must have Left or Right segment.
    -   It cannot have Top segment (since A connects adjacent, Bottom is adjacent to Left/Right, opposite to Top).
    -   So if $v_{i,j}=1$ (Bottom active), then $v_{i-1,j}$ MUST be 0.
    -   Similarly, if $v_{i-1,j}=1$ (Top active), then $v_{i,j}$ MUST be 0.
    -   Conclusion: For Type A, $v_{i,j} \neq v_{i-1,j}$. The vertical status flips.
    
    **This is the breakthrough!**
    Let $x_{i,j} \in \{0, 1\}$ be the state of the vertical edge between row $i$ and $i+1$ (bottom of $i$).
    Let $x_{i-1,j}$ be the state of the vertical edge between row $i-1$ and $i$ (top of $i$).
    
    For cell $(i,j)$:
    -   If $S_{i,j} == 'B'$: $x_{i,j} = x_{i-1,j}$.
    -   If $S_{i,j} == 'A'$: $x_{i,j} \neq x_{i-1,j}$.
    
    This determines the vertical edges completely based on the top edge and the tile type!
    $x_{i,j}$ is uniquely determined by $x_{i-1,j}$ and $S_{i,j}$.
    Specifically, $x_{i,j} = x_{i-1,j} \oplus (1 \text{ if } S_{i,j}=='A' \text{ else } 0)$.
    
    Now we must check consistency with the **horizontal** edges.
    For each cell $(i,j)$, once we know the vertical edges ($x_{i-1,j}$ and $x_{i,j}$), we must check if there exists a valid orientation of the tile that satisfies these vertical constraints AND allows the horizontal edges to be consistent with neighbors.
    
    Let's analyze the horizontal consistency for a fixed column $j$ and row $i$.
    We know:
    -   Top edge state: $T = x_{i-1,j}$
    -   Bottom edge state: $B = x_{i,j}$
    
    Case 1: $T=0, B=0$.
    -   No vertical segments.
    -   Tile must connect Left and Right.
    -   This is only possible if the tile is **Type B**.
    -   If Type A: Impossible (A connects adjacent, cannot connect L-R without vertical).
    -   So if $T=0, B=0$, we MUST have $S_{i,j} == 'B'$.
    -   If $S_{i,j} == 'A'$, this state is invalid (0 solutions).
    -   If $S_{i,j} == 'B'$, the tile is fixed to Horizontal.
        -   This implies Left edge is active, Right edge is active.
        -   This imposes constraints on $u_{i,j-1}$ and $u_{i,j}$.
    
    Case 2: $T=1, B=1$.
    -   Vertical segments active at both top and bottom.
    -   Tile must connect Top and Bottom.
    -   Only possible if **Type B**.
    -   If Type A: Impossible.
    -   So if $T=1, B=1$, we MUST have $S_{i,j} == 'B'$.
    -   If $S_{i,j} == 'B'$, tile is fixed to Vertical.
        -   Left edge inactive, Right edge inactive.
    
    Case 3: $T=0, B=1$.
    -   Bottom active, Top inactive.
    -   Tile must connect Bottom and (Left or Right).
    -   Must be **Type A**.
    -   If Type B: Impossible (B connects opposite, cannot do Bottom+Left/Right).
    -   So if $T=0, B=1$, we MUST have $S_{i,j} == 'A'$.
    -   If $S_{i,j} == 'A'$, the tile connects Bottom and Left OR Bottom and Right.
        -   Option 1: Bottom + Left. $\implies$ Left active, Right inactive.
        -   Option 2: Bottom + Right. $\implies$ Left inactive, Right active.
        -   This gives 2 choices for the horizontal edges of this cell.
    
    Case 4: $T=1, B=0$.
    -   Top active, Bottom inactive.
    -   Tile must connect Top and (Left or Right).
    -   Must be **Type A**.
    -   If Type B: Impossible.
    -   So if $T=1, B=0$, we MUST have $S_{i,j} == 'A'$.
    -   If $S_{i,j} == 'A'$, choices:
        -   Top + Left $\implies$ Left active, Right inactive.
        -   Top + Right $\implies$ Left inactive, Right active.
        -   2 choices.
    
    **Summary of Vertical Propagation**:
    $x_{i,j} = x_{i-1,j} \oplus (S_{i,j} == 'A')$.
    This defines the vertical edges for the whole grid given the initial row $x_{-1,j}$.
    Since it's a torus, $x_{-1,j} = x_{H-1,j}$.
    This implies a consistency condition on the column $j$:
    After $H$ steps, $x_{H,j} = x_{0,j}$.
    $x_{H,j} = x_{0,j} \oplus (\text{count of A in col } j \pmod 2)$.
    So, for a valid configuration to exist, **every column must have an even number of Type A tiles**.
    If any column has an odd number of A's, the answer is 0.
    
    **Counting the Ways**:
    If the even-A condition is met:
    For each column $j$:
    -   If $S_{i,j} == 'B'$:
        -   If $x_{i-1,j}=0 \implies x_{i,j}=0$. State (0,0). Tile must be Horizontal.
            -   Left active, Right active.
        -   If $x_{i-1,j}=1 \implies x_{i,j}=1$. State (1,1). Tile must be Vertical.
            -   Left inactive, Right inactive.
        -   In both cases, the horizontal edges of this cell are **determined** (L=1,R=1 or L=0,R=0).
        -   Number of choices for this cell's horizontal contribution: **1**.
    -   If $S_{i,j} == 'A'$:
        -   If $x_{i-1,j}=0 \implies x_{i,j}=1$. State (0,1). Tile must be Bottom+Left or Bottom+Right.
            -   L=1,R=0 OR L=0,R=1.
            -   Number of choices: **2**.
        -   If $x_{i-1,j}=1 \implies x_{i,j}=0$. State (1,0). Tile must be Top+Left or Top+Right.
            -   L=1,R=0 OR L=0,R=1.
            -   Number of choices: **2**.
    
    So, for a fixed initial state $x_{-1}$ (which is a vector of length $W$), the number of ways to fill the grid is $2^{\text{total count of A tiles}}$.
    Wait, is it that simple?
    We need to ensure that the **horizontal** edges are consistent across columns.
    For each row $i$, and for each cell $(i,j)$, we have a required Left edge state $L_{i,j}$ and Right edge state $R_{i,j}$.
    Consistency requires: $R_{i,j} = L_{i, j+1}$ (with wrap around).
    
    Let's trace the horizontal flow.
    For a fixed row $i$ and fixed vertical states $x_{i-1}, x_i$:
    -   For each $j$, the tile type and vertical states determine the possible values of $(L_{i,j}, R_{i,j})$.
    -   If $S_{i,j} == 'B'$:
        -   $(L, R)$ is fixed to $(1, 1)$ if $x=0$, or $(0, 0)$ if $x=1$.
    -   If $S_{i,j} == 'A'$:
        -   $(L, R)$ can be $(1, 0)$ or $(0, 1)$.
    
    Let's define a variable $h_{i,j} \in \{0, 1\}$ representing the state of the horizontal edge between $j$ and $j+1$.
    Then $L_{i,j} = h_{i, j-1}$ and $R_{i,j} = h_{i,j}$.
    
    For $S_{i,j} == 'B'$:
    -   If $x_{i-1,j}=0$ (so $x_{i,j}=0$): Need $L=1, R=1 \implies h_{i, j-1}=1, h_{i,j}=1$.
    -   If $x_{i-1,j}=1$ (so $x_{i,j}=1$): Need $L=0, R=0 \implies h_{i, j-1}=0, h_{i,j}=0$.
    -   So for Type B, $h_{i,j} = h_{i, j-1} = x_{i-1,j}$?
        -   If $x=0$, $h=1$. If $x=1$, $h=0$.
        -   So $h_{i,j} = 1 - x_{i-1,j} = x_{i-1,j} \oplus 1$.
        -   This fixes $h_{i,j}$ uniquely.
    
    For $S_{i,j} == 'A'$:
    -   If $x_{i-1,j}=0$ ($x_{i,j}=1$): Need $(L,R) \in \{(1,0), (0,1)\}$.
        -   $L=1, R=0 \implies h_{i, j-1}=1, h_{i,j}=0$.
        -   $L=0, R=1 \implies h_{i, j-1}=0, h_{i,j}=1$.
        -   So $h_{i,j} \neq h_{i, j-1}$.
    -   If $x_{i-1,j}=1$ ($x_{i,j}=0$): Need $(L,R) \in \{(1,0), (0,1)\}$.
        -   Same logic: $h_{i,j} \neq h_{i, j-1}$.
    -   So for Type A, $h_{i,j} \neq h_{i, j-1}$.
    
    **Recurrence for Horizontal Edges**:
    Let $h_{i,j}$ be the horizontal edge state between col $j$ and $j+1$.
    For each row $i$:
    -   If $S_{i,j} == 'B'$: $h_{i,j} = h_{i, j-1} \oplus (x_{i-1,j} \oplus 1)$.
        -   Actually, let's re-verify:
            -   $x=0 \implies h=1$. $x=1 \implies h=0$.
            -   So $h_{i,j} = x_{i-1,j} \oplus 1$.
            -   Does this depend on $h_{i, j-1}$?
            -   Yes, because $h_{i,j}$ must equal $h_{i, j-1}$ for the B tile to be valid?
            -   Wait. For B tile:
                -   If $x=0$, we need $L=1, R=1$. So $h_{i, j-1}=1$ and $h_{i,j}=1$.
                -   If $x=1$, we need $L=0, R=0$. So $h_{i, j-1}=0$ and $h_{i,j}=0$.
            -   So $h_{i,j}$ is determined by $x_{i-1,j}$.
            -   BUT, we also need $h_{i,j} = h_{i, j-1}$.
            -   So for a Type B tile at $j$, we require $h_{i,j} = h_{i, j-1} = x_{i-1,j} \oplus 1$.
            -   This creates a constraint linking $j$ and $j-1$.
    
    Let's formalize the constraint for row $i$:
    We have a sequence of required horizontal states $H_j$ for $j=0..W-1$.
    $H_j$ is the value of the edge between $j$ and $j+1$.
    For each $j$:
    -   If $S_{i,j} == 'B'$:
        -   Requires $H_j = H_{j-1} = x_{i-1,j} \oplus 1$.
    -   If $S_{i,j} == 'A'$:
        -   Requires $H_j \neq H_{j-1}$.
    
    This looks like we can determine $H_j$ from $H_{j-1}$ and the tile type.
    Let $k_j = 1$ if $S_{i,j} == 'A'$, else $0$.
    Then $H_j = H_{j-1} \oplus k_j$.
    Wait, for Type B, we found $H_j = H_{j-1}$ AND $H_j = x_{i-1,j} \oplus 1$.
    For Type A, we found $H_j \neq H_{j-1}$.
    
    Let's re-evaluate Type A constraint.
    If $S_{i,j} == 'A'$:
    -   We have 2 choices for the tile orientation: (L=1, R=0) or (L=0, R=1).
    -   This corresponds to $H_{j-1}=1, H_j=0$ OR $H_{j-1}=0, H_j=1$.
    -   In both cases, $H_j \neq H_{j-1}$.
    -   So the relation is $H_j = H_{j-1} \oplus 1$.
    
    So for ANY cell, regardless of type:
    -   If Type A: $H_j = H_{j-1} \oplus 1$. (1 choice of relation, but 2 choices of absolute orientation? No, the relation fixes the relative change, but the absolute value $H_{j-1}$ propagates).
        -   Actually, if $H_j = H_{j-1} \oplus 1$, then given $H_{j-1}$, $H_j$ is fixed.
        -   Does this match the "2 choices" earlier?
        -   Earlier: "2 choices for the horizontal edges".
        -   If $H_{j-1}=0$, then $H_j=1$. (Choice 1: L=0, R=1).
        -   If $H_{j-1}=1$, then $H_j=0$. (Choice 2: L=1, R=0).
        -   So yes, once the global horizontal flow $H$ is fixed, the specific tile orientation is determined.
        -   So for Type A, there is **1** way to set the tile given the $H$ sequence.
        -   Wait, the "2 choices" I counted earlier was assuming we could pick $H_{j-1}$ and $H_j$ freely? No, they are coupled to neighbors.
        -   Let's restart the counting logic carefully.
    
    **Global Flow Logic**:
    We need to find the number of binary sequences $H_{i,0}, H_{i,1}, \dots, H_{i, W-1}$ (for each row $i$) such that:
    1.  $H_{i,j} = H_{i, j-1} \oplus 1$ if $S_{i,j} == 'A'$.
    2.  $H_{i,j} = H_{i, j-1}$ if $S_{i,j} == 'B'$.
    3.  Also, for Type B, we have an additional constraint: $H_{i,j} = x_{i-1,j} \oplus 1$.
        -   Wait, is this always true?
        -   If $S_{i,j} == 'B'$, the tile MUST be horizontal if $x=0$ (L=1,R=1) or vertical if $x=1$ (L=0,R=0).
        -   If vertical ($x=1$), then $L=0, R=0 \implies H_{j-1}=0, H_j=0$. Consistent with $H_j = H_{j-1}$.
        -   If horizontal ($x=0$), then $L=1, R=1 \implies H_{j-1}=1, H_j=1$. Consistent with $H_j = H_{j-1}$.
        -   AND the value is fixed to $x_{i-1,j} \oplus 1$.
        -   So for Type B, $H_{i,j}$ is **fixed** to a specific value ($x_{i-1,j} \oplus 1$).
        -   For Type A, $H_{i,j}$ is determined by $H_{i, j-1} \oplus 1$.
    
    So, for a fixed row $i$ and fixed vertical inputs $x_{i-1}$:
    -   Start with $H_{i,-1}$ (which is $H_{i, W-1}$ due to torus).
    -   Propagate:
        -   If $S_{i,j} == 'A'$: $H_{i,j} = H_{i, j-1} \oplus 1$.
        -   If $S_{i,j} == 'B'$: $H_{i,j} = x_{i-1,j} \oplus 1$.
            -   This also imposes a constraint: $H_{i,j}$ must equal $H_{i, j-1}$.
            -   So if we arrive at a Type B, we check if the propagated $H_{i, j-1}$ matches the required $x_{i-1,j} \oplus 1$.
            -   If not, this initial $H_{i,-1}$ is invalid.
    
    This means for each row, the sequence $H$ is either fully determined (if no contradictions) or impossible.
    Actually, since $H_{i,j}$ depends on $H_{i, j-1}$ for A, and is fixed for B, the value of $H_{i,0}$ determines the whole row?
    -   Let's trace:
        -   $H_{i,0}$ is free? No, it's part of the cycle.
        -   Let's assume $H_{i, -1} = v$.
        -   Compute $H_{i,0}$ from $v$ and $S_{i,0}$.
        -   Compute $H_{i,1}$ from $H_{i,0}$ and $S_{i,1}$.
        -   ...
        -   Finally compute $H_{i, W-1}$ from $H_{i, W-2}$.
        -   Check consistency: $H_{i, W-1}$ must equal $v$ (torus).
        -   AND, for every Type B at $j$, the computed $H_{i,j}$ must match $x_{i-1,j} \oplus 1$.
    
    Wait, if $S_{i,j} == 'B'$, then $H_{i,j}$ is fixed to $x_{i-1,j} \oplus 1$.
    This fixes the value at $j$.
    Since $H$ propagates linearly ($H_j = H_{j-1} \oplus 1$ or $H_j = H_{j-1}$), the value at any $j$ is $H_{-1} \oplus (\text{parity of A's before } j)$.
    So $H_{i,j} = H_{i,-1} \oplus (\sum_{k=0}^{j-1} [S_{i,k}=='A']) \pmod 2$.
    
    Constraint for Type B at $j$:
    $H_{i,j} = x_{i-1,j} \oplus 1$.
    Substitute:
    $H_{i,-1} \oplus (\text{count A in } 0..j-1) = x_{i-1,j} \oplus 1$.
    $\implies H_{i,-1} = x_{i-1,j} \oplus 1 \oplus (\text{count A in } 0..j-1)$.
    
    This must hold for **all** $j$ where $S_{i,j} == 'B'$.
    If there are multiple Type B tiles in a row, they must all yield the same required $H_{i,-1}$.
    If they yield different values, the row is impossible (0 ways).
    If there are no Type B tiles, then $H_{i,-1}$ can be anything?
    -   If no Type B, then no fixed constraints.
    -   We just need the torus condition: $H_{i, W-1} = H_{i,-1}$.
    -   $H_{i, W-1} = H_{i,-1} \oplus (\text{total A in row})$.
    -   So we need $\text{total A in row} \equiv 0 \pmod 2$.
    -   If total A is even, any $H_{i,-1}$ works?
        -   If $H_{i,-1}=0$, sequence is valid.
        -   If $H_{i,-1}=1$, sequence is valid.
        -   So 2 choices for the row's horizontal flow.

## worker: Check if every column has an even number of 'A's. 
The problem asks for the number of valid tile rotations on a torus grid such that there are no dead ends.
1.  **Parity Constraints**: The condition "no dead ends" on a torus implies that the flow of segments must be consistent.
    -   For vertical edges: A Type A tile flips the vertical flow state (0->1 or 1->0), while a Type B tile preserves it. For the flow to be consistent on a torus (wrapping around), the total number of flips in any column must be even. Thus, every column must have an even number of 'A' tiles.
    -   Similarly, for horizontal edges, every row must have an even number of 'A' tiles.
    -   If either condition fails, the answer is 0.

2.  **Graph Construction**:
    -   If the parity conditions are met, we need to count the number of valid global configurations.
    -   The state of the vertical edges entering row $i$ (denoted $x_{i-1, j}$) and the horizontal edges entering column $j$ of row $i$ (denoted $H_{i, j-1}$) are coupled by the tile types.
    -   Specifically, for a Type B tile at $(i, j)$, the horizontal edge state $H_{i, j}$ is fixed relative to the vertical edge state $x_{i-1, j}$. This creates a constraint equation: $H_{i, -1} \oplus x_{-1, j} = \text{constant}$.
    -   For Type A tiles, the relationship is determined by the horizontal flow propagation ($H_{i, j} = H_{i, j-1} \oplus 1$), which doesn't add new constraints between $x$ and $H$ variables directly, but ensures consistency if the $H$ sequence is valid.
    -   The constraints from Type B tiles form a system of linear equations over GF(2) involving variables $x_{-1, j}$ (for each column) and $H_{i, -1}$ (for each row).
    -   This system can be modeled as a graph where nodes are the variables ($W$ for $x$, $H$ for $H$) and edges represent the constraints from Type B tiles.
    -   Each connected component in this graph allows 2 independent choices (fix one variable, others determined). If a cycle is inconsistent, the answer is 0.
    -   The number of solutions is $2^{\text{number of connected components}}$.

3.  **Algorithm**:
    -   Check row and column 'A' counts. If any odd, output 0.
    -   Build a graph with $W+H$ nodes.
    -   Iterate through the grid. For each 'B' at $(i, j)$, add an edge between node $j$ (representing $x_{-1, j}$) and node $W+i$ (representing $H_{i, -1}$) with a weight derived from the prefix sums of 'A's.
    -   Count connected components using BFS/DFS.
    -   Result is $2^{\text{components}} \pmod{998244353}$.

## worker: Implement the graph building and BFS logic in the 
The problem asks for the number of valid tile rotations on a torus grid such that no dead ends exist.
1.  **Parity Constraints**: The "no dead ends" condition on a torus implies that the flow of segments must be continuous. This requires that for any vertical cut (column), the number of "turns" (Type A tiles) must be even to allow the flow to wrap around consistently. Similarly, for any horizontal cut (row), the number of Type A tiles must be even. If either condition is violated, the answer is 0.
2.  **Graph Modeling**: If parity conditions are met, the problem reduces to counting the number of valid assignments of edge states (horizontal and vertical) that satisfy the constraints imposed by the tiles.
    -   Let $x_{i,j}$ be the state of the vertical edge between row $i$ and $i+1$ at column $j$.
    -   Let $h_{i,j}$ be the state of the horizontal edge between column $j$ and $j+1$ at row $i$.
    -   Type A tiles flip the state of the vertical edge ($x_{i,j} = x_{i-1,j} \oplus 1$) and force the horizontal edges to differ ($h_{i,j} \neq h_{i,j-1}$).
    -   Type B tiles preserve the vertical edge state ($x_{i,j} = x_{i-1,j}$) and force the horizontal edges to be equal ($h_{i,j} = h_{i,j-1}$), but also fix the absolute value of the horizontal edge relative to the vertical state ($h_{i,j} = x_{i-1,j} \oplus 1$).
3.  **System of Equations**: The constraints from Type B tiles create linear equations over GF(2) linking the initial vertical states ($x_{-1, j}$) and initial horizontal states ($h_{i, -1}$). Specifically, each Type B tile at $(i, j)$ imposes a constraint of the form $h_{i, -1} \oplus x_{-1, j} = \text{constant}$.
4.  **Counting Solutions**: This system can be modeled as a graph where nodes represent the variables ($x$ and $h$) and edges represent the constraints. Each connected component allows 2 independent choices (fix one variable, others determined). If a cycle in the graph is inconsistent, the answer is 0. Otherwise, the answer is $2^{\text{number of connected components}}$.
5.  **Complexity**: The algorithm runs in $O(HW)$ time to check parities and build the graph, and $O(H+W)$ to traverse the graph, which fits within the constraints ($\sum HW \le 10^6$).

## worker: Implement the solution in Python, ensuring efficie
The solution implements the logic derived in the thought process:
1.  **Parity Check**: It first verifies that every row and every column has an even number of 'A' tiles. If not, the answer is 0 because the flow cannot wrap around the torus consistently.
2.  **Graph Construction**: It constructs a graph where nodes represent the initial states of vertical edges ($x_{-1, j}$) and horizontal edges ($H_{i, -1}$). For each 'B' tile at $(i, j)$, it adds an edge between node $j$ and node $W+i$ with a weight derived from the prefix sums of 'A's encountered so far in that row and column. This weight encodes the constraint $H_{i, -1} \oplus x_{-1, j} = \text{constant}$.
3.  **BFS Traversal**: It performs a BFS to count connected components and checks for consistency (cycles with conflicting parity). If inconsistent, the answer is 0.
4.  **Result Calculation**: The number of valid configurations is $2^{\text{number of connected components}} \pmod{998244353}$.

The complexity is $O(HW)$ per test case due to the grid traversal, which fits the constraints ($\sum HW \le 10^6$).

## worker: Run the code against the provided sample inputs to
The code implements the logic derived:
1.  **Parity Check**: It verifies that every row and every column has an even number of 'A' tiles. If not, the flow cannot wrap around the torus consistently, so the answer is 0.
2.  **Graph Construction**: It constructs a graph where nodes represent the initial states of vertical edges ($x_{-1, j}$) and horizontal edges ($H_{i, -1}$). For each 'B' tile at $(i, j)$, it adds an edge between node $j$ and node $W+i$ with a weight derived from the prefix sums of 'A's encountered so far in that row and column. This weight encodes the constraint $H_{i, -1} \oplus x_{-1, j} = \text{constant}$.
3.  **BFS Traversal**: It performs a BFS to count connected components and checks for consistency (cycles with conflicting parity). If inconsistent, the answer is 0.
4.  **Result Calculation**: The number of valid configurations is $2^{\text{number of connected components}} \pmod{998244353}$.

The complexity is $O(HW)$ per test case due to the grid traversal, which fits the constraints ($\sum HW \le 10^6$).

## worker: finalize
The problem asks for the number of valid tile rotations on a torus grid such that there are no dead ends.
1.  **Parity Constraints**: The "no dead ends" condition on a torus implies that the flow of segments must be continuous. This requires that for any vertical cut (column), the number of "turns" (Type A tiles) must be even to allow the flow to wrap around consistently. Similarly, for any horizontal cut (row), the number of Type A tiles must be even. If either condition is violated, the answer is 0.
2.  **Graph Modeling**: If parity conditions are met, the problem reduces to counting the number of valid assignments of edge states (horizontal and vertical) that satisfy the constraints imposed by the tiles.
    -   Let $x_{i,j}$ be the state of the vertical edge between row $i$ and $i+1$ at column $j$.
    -   Let $h_{i,j}$ be the state of the horizontal edge between column $j$ and $j+1$ at row $i$.
    -   Type A tiles flip the state of the vertical edge ($x_{i,j} = x_{i-1,j} \oplus 1$) and force the horizontal edges to differ ($h_{i,j} \neq h_{i,j-1}$).
    -   Type B tiles preserve the vertical edge state ($x_{i,j} = x_{i-1,j}$) and force the horizontal edges to be equal ($h_{i,j} = h_{i,j-1}$), but also fix the absolute value of the horizontal edge relative to the vertical state ($h_{i,j} = x_{i-1,j} \oplus 1$).
3.  **System of Equations**: The constraints from Type B tiles create linear equations over GF(2) linking the initial vertical states ($x_{-1, j}$) and initial horizontal states ($h_{i, -1}$). Specifically, each Type B tile at $(i, j)$ imposes a constraint of the form $h_{i, -1} \oplus x_{-1, j} = \text{constant}$.
4.  **Counting Solutions**: This system can be modeled as a graph where nodes represent the variables ($x$ and $h$) and edges represent the constraints. Each connected component allows 2 independent choices (fix one variable, others determined). If a cycle in the graph is inconsistent, the answer is 0. Otherwise, the answer is $2^{\text{number of connected components}}$.
5.  **Complexity**: The algorithm runs in $O(HW)$ time to check parities and build the graph, and $O(H+W)$ to traverse the graph, which fits within the constraints ($\sum HW \le 10^6$).
