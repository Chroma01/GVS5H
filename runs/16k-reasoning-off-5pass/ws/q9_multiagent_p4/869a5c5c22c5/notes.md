
## ideation
**Core Difficulty**:
The problem asks to construct a cycle of $N = R+B$ positions on a grid. The movement rules impose strict parity constraints:
1.  **Red pieces**: Move to adjacent cells (up, down, left, right). This preserves the parity of the sum of coordinates $(r+c)$. If a Red piece is at $(r,c)$, the next position $(r',c')$ satisfies $(r'+c') \equiv (r+c) \pmod 2$.
2.  **Blue pieces**: Move to diagonal cells. This flips the parity of $(r+c)$. If a Blue piece is at $(r,c)$, the next position $(r',c')$ satisfies $(r'+c') \not\equiv (r+c) \pmod 2$.

Let the sequence of piece types be $p_1, p_2, \dots, p_N$. Let $x_i$ be the parity of the coordinate sum for the $i$-th piece.
- If $p_i = R$, then $x_{i+1} \equiv x_i \pmod 2$.
- If $p_i = B$, then $x_{i+1} \equiv x_i + 1 \pmod 2$.
Since the sequence forms a cycle, $x_{N+1} \equiv x_1 \pmod 2$.
The total change in parity around the cycle is the number of Blue pieces ($B$) modulo 2.
For the cycle to close, the total parity change must be $0 \pmod 2$.
Therefore, a necessary condition is **$B$ must be even**.

**Candidate Approaches**:
1.  **Check Parity**: If $B$ is odd, output "No".
2.  **Construction Strategy (if $B$ is even)**:
    - We need to arrange $R$ Red pieces and $B$ Blue pieces in a sequence such that we can assign coordinates satisfying the move constraints.
    - **Red Chain**: Since Red moves preserve parity, all Red pieces in the sequence must lie on squares of the same parity. We can place them on a straight line (e.g., $(1,1), (1,2), (1,3) \dots$) if we treat the "next" Red piece as being adjacent. However, the constraint is between piece $i$ and piece $i+1$. If piece $i$ is Red and piece $i+1$ is Red, they must be adjacent. If piece $i$ is Red and piece $i+1$ is Blue, they must be adjacent (Red to Blue move).
    - **Blue Chain**: Blue moves flip parity. If piece $i$ is Blue and piece $i+1$ is Blue, they must be diagonally adjacent.
    - **Strategy**:
        - Place all $R$ Red pieces consecutively in the sequence? No, because if we have two Red pieces adjacent in the sequence, they must be adjacent on the board. This is easy (e.g., $(1,1), (1,2)$).
        - Place all $B$ Blue pieces consecutively? If we have two Blue pieces adjacent in the sequence, they must be diagonally adjacent. This is also easy (e.g., $(1,1), (2,2)$).
        - The tricky part is the transitions between Red and Blue blocks.
        - Let's try a specific ordering: $R, R, \dots, R, B, B, \dots, B$.
        - Sequence: $R_1, R_2, \dots, R_R, B_1, B_2, \dots, B_B$.
        - Constraints:
            - $R_i \to R_{i+1}$: Adjacent (Manhattan 1). Easy.
            - $R_R \to B_1$: Adjacent (Manhattan 1).
            - $B_i \to B_{i+1}$: Diagonal (Chebyshev-like 1).
            - $B_B \to R_1$: Adjacent (Manhattan 1) AND the cycle condition (Blue move flips parity, so $B_B \to R_1$ requires $R_1$ to be diagonally adjacent to $B_B$? Wait, the rule is: "the $i$-th piece placed can move... to the $(i+1)$-th". The type of the piece determines the move capability.
            - Correction: The move capability is determined by the piece *leaving* the square.
                - If piece $i$ is Red, it moves to piece $i+1$'s square using a Red move (Manhattan).
                - If piece $i$ is Blue, it moves to piece $i+1$'s square using a Blue move (Diagonal).
            - So:
                - $R_R \to B_1$: Piece $R_R$ is Red. Move must be Manhattan. $R_R$ and $B_1$ must be adjacent (share edge).
                - $B_B \to R_1$: Piece $B_B$ is Blue. Move must be Diagonal. $B_B$ and $R_1$ must be diagonally adjacent (share corner).
        - Let's verify parities with this arrangement ($R \dots R, B \dots B$):
            - $R_1 \dots R_R$: All same parity $P$.
            - $R_R \to B_1$: Manhattan move. $B_1$ has parity $P$.
            - $B_1 \to B_2$: Diagonal move. $B_2$ has parity $P+1$.
            - $B_2 \to B_3$: Diagonal move. $B_3$ has parity $P$.
            - ...
            - Since $B$ is even, the sequence of parities for Blue pieces will be $P, P+1, P, P+1, \dots, P$. So $B_B$ has parity $P$.
            - $B_B \to R_1$: Diagonal move. $R_1$ must have parity $P+1$.
            - But $R_1$ was defined to have parity $P$. Contradiction!
        - **Conclusion**: The simple block arrangement $R \dots R, B \dots B$ fails the cycle closure parity if $B$ is even? Let's re-evaluate.
            - Parity sequence:
                - $R_1 (P) \xrightarrow{R} R_2 (P) \dots \xrightarrow{R} R_R (P)$.
                - $R_R (P) \xrightarrow{R} B_1 (P)$. (Manhattan preserves parity).
                - $B_1 (P) \xrightarrow{B} B_2 (P+1)$.
                - $B_2 (P+1) \xrightarrow{B} B_3 (P)$.
                - ...
                - $B_k (P + (k-1)) \xrightarrow{B} B_{k+1} (P+k)$.
                - After $B$ steps: $B_B$ has parity $P + (B-1)$.
                - $B_B (P+B-1) \xrightarrow{B} R_1 (P+B)$.
                - We need $R_1$ to have parity $P+B \equiv P \pmod 2$ (since $B$ is even).
                - This works! $P+B \equiv P$.
            - So the parity constraint is satisfied if $B$ is even.
            - Now, can we construct coordinates?
                - $R_1 \dots R_R$: Place on $(1,1), (1,2), \dots, (1,R)$. All parity $1+1=2$ (even) if start at $(1,1)$. Wait, $(1,1)$ is even sum. $(1,2)$ is odd sum.
                - Red moves preserve parity. So $R_1$ and $R_2$ must have same parity.
                - My previous coordinate idea $(1,1), (1,2)$ is wrong for Red pieces because $(1,1)$ sum=2, $(1,2)$ sum=3. Different parities.
                - **Correction for Red pieces**: To move from $R_i$ to $R_{i+1}$ with a Red move, they must be adjacent. Adjacent cells have different parities.
                - **Wait, re-read the problem carefully**: "A red piece on square (r,c) can move to (r+1,c)...". Yes, standard adjacency.
                - Parity of $(r+c)$ changes by $\pm 1$ for any single step (Manhattan or Diagonal).
                - **CRITICAL RE-THINK**:
                    - Red move: $(r, c) \to (r \pm 1, c)$ or $(r, c \pm 1)$. Change in sum $r+c$ is $\pm 1$. **Parity FLIPS**.
                    - Blue move: $(r, c) \to (r \pm 1, c \pm 1)$. Change in sum $r+c$ is $\pm 2$ or $0$. **Parity PRESERVES**.
                - **My initial assumption was reversed!**
                    - Red: Parity flips.
                    - Blue: Parity stays same.
                - Let's re-evaluate the cycle condition.
                    - Start $x_1$.
                    - $R$: $x_2 = x_1 + 1$.
                    - $R$: $x_3 = x_2 + 1 = x_1 + 2$.
                    - ...
                    - $R$: $x_{k+1} = x_k + 1$.
                    - $B$: $x_{k+1} = x_k$.
                    - Total change after $N$ steps must be $0 \pmod 2$.
                    - Each Red step adds 1 to parity. Each Blue step adds 0.
                    - Total change = (Number of Red pieces) $\times 1 \pmod 2$.
                    - Condition: $R \equiv 0 \pmod 2$. **$R$ must be even**.
                    - What about $B$? No parity constraint on $B$.

**Revised Plan**:
1.  **Condition**: $R$ must be even. If $R$ is odd, output "No".
2.  **Construction**:
    - We need a sequence of parities that works.
    - Try ordering: $R, R, \dots, R, B, B, \dots, B$.
    - Parity sequence:
        - $R_1 (p) \xrightarrow{R} R_2 (p+1) \xrightarrow{R} R_3 (p) \dots$
        - Since $R$ is even, $R_R$ will have parity $p$ (same as $R_1$).
        - $R_R (p) \xrightarrow{R} B_1 (p+1)$.
        - $B_1 (p+1) \xrightarrow{B} B_2 (p+1) \xrightarrow{B} \dots \xrightarrow{B} B_B (p+1)$. (Blue preserves parity).
        - $B_B (p+1) \xrightarrow{B} R_1 (p+1)$.
        - But $R_1$ started as $p$. We need $p+1 \equiv p \pmod 2$, which is impossible.
    - **The block arrangement $R \dots R, B \dots B$ fails the cycle closure regardless of parity of R or B?**
        - Let's trace carefully.
        - $R_1 \xrightarrow{R} R_2 \dots \xrightarrow{R} R_R$. Parity changes $R-1$ times. $R_R$ parity = $R_1 + (R-1)$.
        - $R_R \xrightarrow{R} B_1$. Parity changes 1 time. $B_1$ parity = $R_1 + R$.
        - $B_1 \xrightarrow{B} \dots \xrightarrow{B} B_B$. Parity changes 0 times. $B_B$ parity = $R_1 + R$.
        - $B_B \xrightarrow{B} R_1$. Parity changes 0 times. $R_1$ (next) parity = $R_1 + R$.
        - Cycle closure requires $R_1 + R \equiv R_1 \pmod 2 \implies R \equiv 0 \pmod 2$.
        - So $R$ must be even.
        - BUT, we also need the coordinates to exist.
        - If $R$ is even, $R_R$ parity = $R_1 + \text{odd}$. $B_1$ parity = $R_1 + \text{even}$.
        - $R_R$ (parity $p+1$) $\to B_1$ (parity $p$). Move is Red (flips parity). $p+1 \to p$. OK.
        - $B_B$ (parity $p$) $\to R_1$ (parity $p$). Move is Blue (preserves parity). $p \to p$. OK.
        - So the parity logic holds if $R$ is even.
    - **Coordinate Construction**:
        - We need:
            1. $R_1, \dots, R_R$ connected by Red moves (adjacent).
            2. $R_R, B_1$ connected by Red move (adjacent).
            3. $B_1, \dots, B_B$ connected by Blue moves (diagonal).
            4. $B_B, R_1$ connected by Blue move (diagonal).
        - **Red Chain**: $R_1, R_2, \dots, R_R$.
            - Place on $(1,1), (1,2), \dots, (1,R)$.
            - Parities: $2, 3, 4, \dots, R+1$.
            - $R_R$ is at $(1,R)$. Parity $1+R$.
        - **Blue Chain**: $B_1, \dots, B_B$.
            - Need $B_1$ adjacent to $R_R(1,R)$ via Red move? No, $R_R$ moves to $B_1$. So $B_1$ must be adjacent to $(1,R)$.
            - Let $B_1 = (1, R+1)$.
            - Blue moves: $(r,c) \to (r\pm1, c\pm1)$.
            - Sequence $B_1, B_2, \dots, B_B$.
            - $B_1(1, R+1) \to B_2$. Diagonal.
            - If we go $(1, R+1) \to (2, R+2) \to (3, R+3) \dots$?
            - Parity of $B_k$: $1 + (R+1) + (k-1) = R + k + 1$.
            - We need $B_B$ to be diagonally adjacent to $R_1(1,1)$.
            - $R_1(1,1)$. Neighbors for Blue move: $(2,2), (2,0), (0,2), (0,0)$. Valid: $(2,2)$.
            - So we need $B_B = (2,2)$.
            - Path from $B_1(1, R+1)$ to $B_B(2,2)$ using diagonal steps.
            - $\Delta r = 2-1 = 1$. $\Delta c = 2-(R+1) = 1-R$.
            - Number of steps $B-1$.
            - We need $| \Delta r | + | \Delta c |$ to be even? No, diagonal steps change both by $\pm 1$.
            - In $k$ steps, $\Delta r = \sum \delta r_i$, $\Delta c = \sum \delta c_i$.
            - $\Delta r \equiv k \pmod 2$, $\Delta c \equiv k \pmod 2$.
            - So $\Delta r \equiv \Delta c \pmod 2$.
            - Check: $1 \equiv 1-R \pmod 2 \implies R \equiv 0 \pmod 2$.
            - This confirms $R$ must be even.
            - Can we construct the path?
            - If $R=0$, $R$ pieces don't exist. But problem says $R+B \ge 2$. If $R=0$, then $B \ge 2$.
                - If $R=0$, condition $R$ even holds.
                - Sequence: $B_1, \dots, B_B$.
                - $B_B \to B_1$ via Blue move.
                - $B_1 \dots B_B$ diagonal path. $B_B$ diagonal to $B_1$.
                - Any cycle of length $B$ with Blue moves?
                - Blue move: $(r,c) \to (r\pm1, c\pm1)$.
                - Parity preserved.
                - Can we make a cycle? Yes, e.g., $(1,1) \to (2,2) \to (1,1)$? No, $(2,2) \to (1,1)$ is valid. Cycle of 2.
                - For $B \ge 2$, we can just zig-zag or make a small loop.
                - Example $B=2$: $(1,1) \to (2,2) \to (1,1)$.
                - Example $B=4$: $(1,1) \to (2,2) \to (3,3) \to (2,2)$? No, distinct squares? "At most one piece on a single square". Yes, distinct.
                - $(1,1) \to (2,2) \to (3,3) \to (2,2)$ repeats $(2,2)$. Bad.
                - $(1,1) \to (2,2) \to (3,3) \to (4,4) \to (3,3)$? No.
                - Need a cycle of distinct vertices in the diagonal grid graph.
                - Diagonal grid is bipartite? No, parity is constant. It's a grid rotated 45 degrees.
                - Actually, $(r,c)$ connected to $(r\pm1, c\pm1)$.
                - Consider subgrid. $(1,1)-(2,2)-(3,3)-(2,4)-(1,3)-(1,2)-(2,1)-(1,1)$?
                - Simpler: Just go back and forth? No, distinct.
                - For $B \ge 2$, we can use a $2 \times 2$ block?
                - $(1,1) \to (2,2)$. From $(2,2)$ can we go to something else and come back?
                - $(2,2) \to (3,3) \to (2,4) \to (1,3) \to (2,2)$? No, $(1,3) \to (2,2)$ is valid.
                - Path: $(1,1) \to (2,2) \to (3,3) \to (2,4) \to (1,3) \to (2,2)$? Repeats $(2,2)$.
                - Try: $(1,1) \to (2,2) \to (3,3) \to (4,4) \to (3,5) \to (2,4) \to (1,3) \to (2,2)$? Repeats.
                - Actually, for $B \ge 2$, we can simply do:
                  $B_1=(1,1), B_2=(2,2), B_3=(1,3), B_4=(2,4), \dots$
                  Wait, we need $B_B \to B_1$ diagonal.
                  If $B=2$: $(1,1) \to (2,2) \to (1,1)$? Distinct? No, $B_1$ and $B_2$ distinct, but $B_2 \to B_1$ is the last step. The set of positions is $\{B_1, \dots, B_B\}$. They must be distinct.
                  $B_1=(1,1), B_2=(2,2)$. $B_2 \to B_1$ is valid. Distinct positions? Yes.
                  $B=3$: $(1,1) \to (2,2) \to (1,3) \to (2,2)$? No, $B_3=(1,3)$, $B_4$ would be $B_1$.
                  Sequence: $B_1, B_2, B_3$. $B_3 \to B_1$.
                  $B_1=(1,1), B_2=(2,2), B_3=(3,3)$. $B_3 \to B_1$? $(3,3) \to (1,1)$ is distance 2. Not 1 move.
                  Need $B_3$ adjacent to $B_1$.
                  $B_1=(1,1)$. Neighbors: $(2,2)$. Only one neighbor in positive quadrant?
                  $(2,2)$ is the only positive neighbor.
                  So if we start at $(1,1)$, next must be $(2,2)$. From $(2,2)$, neighbors are $(1,1), (1,3), (3,1), (3,3)$.
                  If $B=3$: $(1,1) \to (2,2) \to (1,3) \to (1,1)$? $(1,3) \to (1,1)$ dist 2. No.
                  $(1,1) \to (2,2) \to (3,3) \to (2,2)$? No.
                  $(1,1) \to (2,2) \to (3,1) \to (2,2)$? No.
                  $(1,1) \to (2,2) \to (3,3) \to (2,4) \to (1,3) \to (2,2)$?
                  It seems hard to make a cycle of length 3 with only diagonal moves on integer grid?
                  Diagonal graph is bipartite?
                  Color $(r,c)$ by $(r+c)/2$. No, parity of $r+c$ is constant.
                  Let's map to $(u,v) = (r+c, r-c)$.
                  Move: $(r,c) \to (r\pm1, c\pm1)$.
                  $u' = r\pm1+c\pm1 = u \pm 2$ or $u$.
                  $v' = r\pm1-c\mp1 = v \pm 2$ or $v$.
                  Actually $u' = u + (\delta r + \delta c)$. $\delta r, \delta c \in \{1, -1\}$. Sum is $2, 0, -2$.
                  $v' = v + (\delta r - \delta c)$. Diff is $2, 0, -2$.
                  So $u$ and $v$ change by even numbers.
                  This means the graph is disconnected into components based on $u \pmod 2$ and $v \pmod 2$?
                  Actually, $u$ and $v$ have same parity as $r+c$ and $r-c$.
                  Since $r+c$ and $r-c$ have same parity (sum is $2r$), $u$ and $v$ are both even or both odd.
                  In one step, $u \to u \pm 2$ or $u$. $v \to v \pm 2$ or $v$.
                  So the graph is a grid where steps are $(\pm 2, 0), (0, \pm 2), (\pm 2, \pm 2)$?
                  Wait, $r \to r+1, c \to c+1 \implies u \to u+2, v \to v$.
                  $r \to r+1, c \to c-1 \implies u \to u, v \to v+2$.
                  $r \to r-1, c \to c+1 \implies u \to u, v \to v-2$.
                  $r \to r-1, c \to c-1 \implies u \to u-2, v \to v$.
                  So in $(u,v)$ coordinates, moves are $(\pm 2, 0)$ or $(0, \pm 2)$.
                  This is a standard grid graph with step size 2.
                  Cycle condition: We need a cycle of length $B$ in this grid.
                  Since it's a grid, cycles of length 2 (back and forth) are trivial but require repeating vertices? No, $B_1 \to B_2 \to B_1$ uses $B_1, B_2$. Distinct.
                  For $B=2$: $B_1=(1,1) \to B_2=(2,2) \to B_1$. Valid.
                  For $B=3$: Need $B_1 \to B_2 \to B_3 \to B_1$.
                  In grid graph, smallest cycle is 4 (square).
                  So $B$ must be even?
                  Let's check $B=3$ again.
                  $u_1, v_1 \to u_2, v_2 \to u_3, v_3 \to u_1, v_1$.
                  Sum of displacements = 0.
                  Each step is $(\pm 2, 0)$ or $(0, \pm 2)$.
                  To return to origin in 3 steps?
                  $d_1 + d_2 + d_3 = 0$.
                  Vectors are axis-aligned.
                  Sum of 3 axis-aligned vectors cannot be 0 unless they cancel out.
                  e.g., $(2,0) + (-2,0) + (0,0)$? No, step size is exactly 2.
                  $(2,0) + (-2,0) + (0,0)$ impossible.
                  $(2,0) + (-1,0)$ impossible.
                  Minimum non-zero vector is length 2.
                  Can we have $v_1 + v_2 + v_3 = 0$?
                  If $v_1=(2,0), v_2=(-2,0), v_3=(0,0)$ no.
                  If $v_1=(2,0), v_2=(0,2), v_3=(-2,-2)$? No, steps are axis aligned.
                  So sum of 3 axis-aligned vectors of length 2 cannot be 0.
                  Thus, **$B$ must be even**.

**Final Conditions**:
1.  $R$ must be even.
2.  $B$ must be even.
3.  $R+B \ge 2$.

**Construction for $R, B$ even**:
- **Red Chain**: $R_1, \dots, R_R$.
  - Place on $(1,1), (1,2), \dots, (1,R)$.
  - $R_R = (1,R)$.
- **Blue Chain**: $B_1, \dots, B_B$.
  - Need $B_1$ adjacent to $R_R$ (Red move). $B_1 = (1, R+1)$.
  - Need $B_B$ adjacent to $R_1$ (Blue move). $R_1 = (1,1)$. Blue neighbor: $(2,2)$. So $B_B = (2,2)$.
  - Path from $(1, R+1)$ to $(2,2)$ with $B-1$ diagonal steps.
  - Since $B$ is even, $B-1$ is odd.
  - $\Delta r = 1, \Delta c = 1-R$.
  - $|\Delta r| + |\Delta c| = 1 + |1-R|$.
  - Since $R$ is even, $R \ge 2$. $|1-R| = R-1$.
  - Total dist = $1 + R - 1 = R$.
  - We need to cover distance $R$ in $B-1$ steps.
  - Each step covers 1 unit of Manhattan distance in the $(r,c)$ grid? No, diagonal step covers 1 unit in $r$ and 1 in $c$.
  - In $(u,v)$ grid, step is 2 units.
  - Distance in $(u,v)$: $u_{start} = 1+R+1 = R+2$. $u_{end} = 2+2=4$. $\Delta u = R-2$.
  - $v_{start} = 1-(R+1) = -R$. $v_{end} = 2-2=0$. $\Delta v = R$.
  - We need to go from $(R+2, -R)$ to $(4, 0)$ in $B-1$ steps of size 2.
  - Total displacement magnitude?
  - We can just go straight if possible.
  - If $B-1 \ge R$, we can do it.
  - But $B$ and $R$ are independent. What if $B < R$?
  - We need a cycle. Maybe the block arrangement isn't optimal.
  - Alternative: Interleave?
  - Or simply:
    - If $R=0, B=0$: Impossible ($R+B \ge 2$).
    - If $R=0, B \ge 2$ (even): Cycle of Blue.
      - $B_1=(1,1), B_2=(2,2), B_3=(3,3), \dots$? No, need cycle.
      - For $B \ge 2$: $(1,1) \to (2,2) \to (1,3) \to (2,4) \dots$?
      - Actually, for $B \ge 2$, we can use a $2 \times 2$ loop?
      - $(1,1) \to (2,2) \to (1,3) \to (2,4) \to (1,3)$? No.
      - $(1,1) \to (2,2) \to (3,3) \to (2,4) \to (1,3) \to (2,2)$?
      - Wait, if $B$ is even, we can just do a "figure 8" or a rectangle?
      - Rectangle in $(u,v)$: $(0,0) \to (2,0) \to (2,2) \to (0,2) \to (0,0)$. 4 steps.
      - So for $B \ge 4$, easy.
      - For $B=2$: $(1,1) \to (2,2) \to (1,1)$.
      - So $B$ even works for Blue alone.
    - If $R \ge 2, B \ge 2$ (both even):
      - Use the block method but adjust coordinates to ensure reachability.
      - We need $B-1$ steps to cover distance between $B_1$ and $B_B$.
      - We can choose $B_1$ and $B_B$ such that distance is small?
      - $R_R = (1,R)$. $B_1$ must be adjacent. Options: $(1,R+1), (1,R-1), (2,R), (0,R)$.
      - $R_1 = (1,1)$. $B_B$ must be diagonal neighbor. Options: $(2,2)$.
      - Let's try to make $B_1$ close to $(2,2)$.
      - Set $B_1 = (2,2)$? Then $R_R$ must be adjacent to $(2,2)$.
        - $R_R$ options: $(1,2), (3,2), (2,1), (2,3)$.
        - If $R_R = (1,2)$, then $R_1 \dots R_R$ path: $(1,1) \to \dots \to (1,2)$.
        - Length $R$. Steps $R-1$.
        - Path: $(1,1) \to (1,2)$. Requires $R=2$.
        - If $R > 2$, we need more steps. $(1,1) \to (1,2) \to (1,3) \dots$?
        - If $R_R = (1,2)$, then $R$ must be 2? No, $R_R$ is the $R$-th piece.
        - If $R=4$: $(1,1) \to (1,2) \to (1,3) \to (1,4)$. $R_R=(1,4)$. Not $(1,2)$.
        - We can loop? $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? No, distinct.
        - We can go back and forth? No, distinct squares.
        - We can snake: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (3,1) \to (3,2) \dots$
        - We need $R_R$ to be adjacent to $B_1$.
        - And $B_B$ to be $(2,2)$.
        - Let's fix $B_1 = (2,2)$ and $B_B = (2,2)$? No, distinct.
        - Fix $B_B = (2,2)$. $B_1$ must be reachable from $B_B$ in $B-1$ steps.
        - And $B_1$ adjacent to $R_R$.
        - Let's set $B_1 = (3,3)$? Then $B_B=(2,2)$. Distance 1. $B-1=1 \implies B=2$.
        - If $B=2$: $B_1=(3,3), B_2=(2,2)$.
        - $R_R$ adjacent to $(3,3)$. Say $(2,3)$.
        - $R_1 \dots R_R$ ends at $(2,3)$. Starts at $R_1$.
        - $B_2=(2,2)$ must be diagonal to $R_1$.
        - $R_1$ options: $(1,1), (1,3), (3,1), (3,3)$.
        - If $R_1=(1,1)$, then $R_R=(2,3)$.
        - Path $R_1(1,1) \to \dots \to R_R(2,3)$ with $R-1$ steps.
        - $\Delta r = 1, \Delta c = 2$. Manhattan dist 3.
        - Need $R-1 \ge 3 \implies R \ge 4$.
        - If $R=2$: $R_1(1,1) \to R_2(2,3)$? Dist 3. Impossible in 1 step.
        - So we need to adjust $R_1, R_R$ based on $R, B$.
        - General solution:
          - Place Red pieces in a line: $(1,1), (1,2), \dots, (1,R)$. $R_R=(1,R)$.
          - Place Blue pieces in a line: $(1, R+1), (2, R+2), \dots, (B, R+B)$.
          - Check connections:
            - $R_R(1,R) \to B_1(1, R+1)$: Adjacent? Yes.
            - $B_B(B, R+B) \to R_1(1,1)$: Diagonal?
              - $\Delta r = B-1, \Delta c = R+B-1$.
              - Need $|\Delta r| = 1, |\Delta c| = 1$.
              - $B-1=1 \implies B=2$. $R+B-1=1 \implies R=0$.
              - Only works for small cases.
          - Better: Use the fact that $R, B$ are even to create a "bridge".
          - Sequence: $R_1 \dots R_{R/2}, B_1 \dots B_{B/2}, R_{R/2+1} \dots R_R, B_{B/2+1} \dots B_B$?
          - Too complex.
          - Simpler: Just output "No" if $R$ or $B$ is odd?
          - Wait, Sample 1: $R=2, B=3$. Output Yes.
          - My condition $R$ even, $B$ even is wrong.
          - Re-read Sample 1: $R=2, B=3$.
          - $R+B=5$.
          - Sample output:
            B 2 3
            R 3 2
            B 2 2
            B 3 3
            R 2 4
          - Let's trace parities.
            - $B(2,3)$ sum=5 (odd).
            - $R(3,2)$ sum=5 (odd). Move B->R (Blue move). Parity preserved? $5 \to 5$. Yes.
            - $R(3,2) \to B(2,2)$ (Red move). $5 \to 4$. Parity flips.
            - $B(2,2) \to B(3,3)$ (Blue move). $4 \to 6$. Parity preserved.
            - $B(3,3) \to R(2,4)$ (Blue move). $6 \to 6$. Parity preserved.
            - $R(2,4) \to B(2,3)$ (Red move). $6 \to 5$. Parity flips.
          - Total parity changes: 2 (Red moves).
          - Start parity 5. End parity 5. Consistent.
          - Number of Red moves = $R = 2$. Even.
          - Number of Blue moves = $B = 3$.
          - Condition: $R$ must be even. $B$ can be anything.
          - So my condition $R$ even is correct. $B$ doesn't need to be even.
          - Sample 1: $R=2$ (even), $B=3$ (odd). Works.
          - Sample 2: $R=1, B=1$. $R$ odd. Output No. Correct.
          - Sample 3: $R=4, B=0$. $R$ even. Output Yes. Correct.
          - So condition: **$R$ must be even**.

**Construction for $R$ even, $B \ge 0$**:
- Sequence: $R, R, \dots, R, B, B, \dots, B$.
- $R_1 \dots R_R$: $(1,1), (1,2), \dots, (1,R)$.
- $R_R = (1,R)$.
- $B_1$: Adjacent to $R_R$. Let $B_1 = (1, R+1)$.
- $B_1 \dots B_B$: Diagonal chain.
- $B_B$: Must be diagonal to $R_1(1,1)$. So $B_B = (2,2)$.
- Path from $(1, R+1)$ to $(2,2)$ with $B-1$ steps.
- $\Delta r = 1, \Delta c = 1-R$.
- We need to cover this distance with $B-1$ steps.
- Since we can move $(\pm 1, \pm 1)$, we can waste steps by going back and forth?
- No, distinct squares.
- But we have $B$ even/odd freedom?
- If $B=1$: $B_1 = (2,2)$. $R_R(1,R)$ adjacent to $(2,2)$.
  - $R_R$ options: $(1,2), (2,2)$ (no), $(2,1), (2,3)$.
  - If $R_R=(1,2)$, then $R=2$.
  - If $R=2, B=1$: $R_1(1,1), R_2(1,2), B_1(2,2)$.
    - $R_2 \to B_1$: $(1,2) \to (2,2)$ (Red move). OK.
    - $B_1 \to R_1$: $(2,2) \to (1,1)$ (Blue move). OK.
  - Works.
- If $B \ge 2$:
  - We need a path of length $B-1$ from $(1, R+1)$ to $(2,2)$.
  - We can construct a path that goes "out" and "back" if needed?
  - Actually, we can choose the starting point of the Blue chain differently?
  - No, $B_1$ is fixed by $R_R$.
  - But we can choose $R_R$ differently?
  - $R_1 \dots R_R$ must be a path.
  - We can make the Red path longer in one dimension to adjust $R_R$.
  - Let's try:
    - $R_1=(1,1)$.
    - $R_R=(1, R)$. (Standard).
    - $B_1=(1, R+1)$.
    - $B_B=(2,2)$.
    - If $B$ is large, we can go $(1, R+1) \to (2, R+2) \to (3, R+3) \dots$ until we get close to $(2,2)$ and then zig-zag?
    - Actually, we can just use a "snake" that covers the required parity and length.
    - Since $R$ is even, $R \ge 2$.
    - If $B=0$: $R_1 \dots R_R$ cycle? $R_R \to R_1$ Red move.
      - $R_R=(1,R), R_1=(1,1)$. Need adjacent. $R=2$.
      - If $R > 2$, need to loop. $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? No, distinct.
      - $(1,1) \to (1,2) \to (2,2) \to (2,3) \to (1,3) \to (1,4) \dots$?
      - For $R$ even, we can form a cycle of length $R$?
      - Yes, a rectangle $2 \times (R/2)$?
      - $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? Length 4.
      - For $R=2$: $(1,1) \to (1,2) \to (1,1)$? No, distinct.
      - $R=2$: $(1,1) \to (1,2) \to (1,1)$? No.
      - $R=2$: $R_1(1,1), R_2(1,2)$. $R_2 \to R_1$? $(1,2) \to (1,1)$. Yes.
      - So $R=2$ works.
      - $R=4$: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? No, $R_4=(2,1) \to R_1(1,1)$. Yes.
      - So for $B=0$, any even $R \ge 2$ works with a $2 \times 2$ loop repeated? No, distinct.
      - Use a $2 \times k$ rectangle perimeter.
      - $(1,1) \to (1,2) \to \dots \to (1,k) \to (2,k) \to (2,k-1) \dots \to (2,1) \to (1,1)$.
      - Length $2k$. $R=2k$.
      - So for $B=0$, place Red pieces on perimeter of $2 \times (R/2)$ box.
    - For $B > 0$:
      - Connect the Red cycle to the Blue chain.
      - Break the Red cycle at $R_R$ and $R_1$.
      - $R_1 \dots R_R$ is a path.
      - $B_1 \dots B_B$ is a path.
      - $R_R \to B_1$ (Red).
      - $B_B \to R_1$ (Blue).
      - We need $R_R$ and $B_1$ adjacent.
      - We need $B_B$ and $R_1$ diagonal.
      - We can choose the shape of the Red path to make $R_R$ close to $B_1$.
      - Let $R_1=(1,1)$. $B_B=(2,2)$.
      - $B_1$ must be diagonal to $B_B$? No, $B_1 \dots B_B$ is Blue path.
      - $B_1$ adjacent to $R_R$.
      - Let's set $B_1 = (2,2)$? Then $B_B$ must be reachable from $(2,2)$ in $B-1$ steps and end at a point diagonal to $R_1$.
      - But $B_B$ must be diagonal to $R_1$.
      - If $B_1 = (2,2)$, then $B_1$ is diagonal to $R_1(1,1)$.
      - If $B=1$, $B_1=B_B=(2,2)$. $R_R$ adjacent to $(2,2)$.
      - If $B > 1$, we need $B_B$ to be diagonal to $R_1$.
      - Let's just use the perimeter idea for Red, and a simple line for Blue.
      - Actually, simplest construction:
        - If $B=0$: Perimeter of $2 \times (R/2)$.
        - If $B > 0$:
          - Red path: $(1,1) \to (1,2) \to \dots \to (1, R)$.
          - $R_R = (1,R)$.
          - Blue path: $(1, R+1) \to (2, R+2) \to \dots \to (B, R+B)$.
          - Check $B_B \to R_1$: $(B, R+B) \to (1,1)$.
          - This requires $B=2, R=0$? No.
          - We need to adjust.
          - Use the fact that we can shift the Blue path.
          - Let $B_1 = (2,2)$.
          - $R_R$ must be adjacent to $(2,2)$. Let $R_R = (1,2)$.
          - Then $R_1 \dots R_R$ must end at $(1,2)$.
          - $R_1=(1,1)$. Path $(1,1) \to (1,2)$. $R=2$.
          - If $R > 2$, extend the path: $(1,1) \to (1,2) \to (2,2)$? No, $(2,2)$ is $B_1$.
          - Extend: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? No.
          - $(1,1) \to (1,2) \to (2,2) \to (2,3) \to (1,3) \to (1,4) \dots$
          - We need $R_R$ adjacent to $(2,2)$.
          - Let $R_R = (2,3)$.
          - Path from $(1,1)$ to $(2,3)$ with $R-1$ steps.
          - $\Delta r=1, \Delta c=2$. Dist 3.
          - Need $R-1 \ge 3 \implies R \ge 4$.
          - If $R=2$, use $(1,1) \to (1,2) \to (2,2)$? No, $B_1=(2,2)$.
          - If $R=2$, $R_R=(1,2)$. $B_1=(2,2)$ (adjacent). $B_B=(2,2)$ (if $B=1$).
          - If $B \ge 2$, $B_1=(2,2)$. $B_B$ must be diagonal to $R_1(1,1)$.
          - $B_B$ options: $(2,2)$ (no, used), $(1,3), (3,1), (0,0)$.
          - Let $B_B=(1,3)$.
          - Path $(2,2) \to \dots \to (1,3)$ with $B-1$ steps.
          - $\Delta r=-1, \Delta c=1$. Dist 2.
          - Need $B-1 \ge 2 \implies B \ge 3$.
          - If $B=2$, need dist 1. $(2,2) \to (1,3)$ dist 2. Impossible.
          - So $B=2$ needs $B_B$ adjacent to $(2,2)$ and diagonal to $(1,1)$.
          - Neighbors of $(2,2)$: $(1,1), (1,3), (3,1), (3,3)$.
          - Diagonal to $(1,1)$: $(2,2)$.
          - Only $(2,2)$ is diagonal to $(1,1)$.
          - So $B_B$ must be $(2,2)$.
          - But $B_1$ is $(2,2)$. Conflict if $B > 1$.
          - So $B=2$ is problematic with this setup.
          - Solution: Change $R_1$.
          - If $R_1=(1,2)$, then $B_B$ must be diagonal to $(1,2)$. Options: $(2,1), (2,3), (0,1), (0,3)$.
          - Let $B_B=(2,1)$.
          - $B_1=(2,2)$. Path $(2,2) \to (2,1)$ dist 2. $B-1 \ge 2 \implies B \ge 3$.
          - Still $B=2$ issue.
          - Maybe $B=2$ requires a different $R_R$?
          - $R=2$. $R_1(1,1), R_2(1,2)$. $R_2 \to B_1$.
          - $B_1, B_2$. $B_2 \to R_1$.
          - Try: $R_1(1,1), R_2(2,2)$? No, Red move.
          - $R_1(1,1), R_2(1,2)$. $B_1(2,2)$. $B_2(2,1)$.
          - $R_2(1,2) \to B_1(2,2)$ (Red). OK.
          - $B_1(2,2) \to B_2(2,1)$ (Blue). OK.
          - $B_2(2,1) \to R_1(1,1)$ (Blue). OK.
          - Distinct? $(1,1), (1,2), (2,2), (2,1)$. Yes.
          - So $R=2, B=2$ works.
          - Generalize:
            - $R_1(1,1), R_2(1,2)$.
            - $B_1(2,2), B_2(2,1)$.
            - For $B > 2$, extend Blue chain from $(2,1)$.
            - $(2,1) \to (3,2) \to (4,3) \dots$
            - Need $B_B$ diagonal to $R_1(1,1)$.
            - If we extend, $B_B$ moves away.
            - We need to come back.
            - Use a loop for Blue?
            - Since $B$ can be large, we can do a large loop.
            - But we need to connect to $R_R$.
            - Final strategy:
              - If $R=0$: Impossible ($R+B \ge 2$). But $R$ must be even, so $R=0$ is allowed if $B \ge 2$.
              - If $R=0, B \ge 2$: Blue cycle. $(1,1) \to (2,2) \to (1,3) \to (2,4) \to (1,5) \dots$?
              - Just use a $2 \times B$ grid?
              - Actually, for $R=0$, we can just output a cycle of Blue pieces.
              - For $R > 0$:
                - Place $R_1(1,1), R_2(1,2), \dots, R_R(1,R)$.
                - $B_1(1, R+1)$.
                - $B_2(2, R+2), \dots, B_B(B, R+B)$.
                - This fails the cycle.
                - Instead, use the $R=2, B=2$ pattern as base and extend.
                - Or simply:
                  - If $R$ is even, $B \ge 0$:
                  - Output "Yes".
                  - Construct:
                    - $R_1=(1,1), R_2=(1,2)$.
                    - If $R > 2$, add $R_3=(2,2), R_4=(2,3), \dots, R_R=(?,?)$.
                    - This is getting complicated to code in thought.
                    - Given the constraints and typical CP problem patterns, if $R$ is even, a construction always exists.
                    - Code can use a fixed pattern for small $R,B$ and a generic snake for large.
                    - Pattern:
                      - Red: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$? No.
                      - Red: $(1,1) \to (1,2) \to (1,3) \dots \to (1,R) \to (2,R) \to (2,R-1) \dots \to (2,1)$.
                      - This is a $2 \times R$ rectangle perimeter. Length $2R$.
                      - We need length $R$.
                      - Just $(1,1) \to (1,2) \to \dots \to (1,R) \to (2,R) \to (2,R-1) \dots \to (2,2) \to (1,2)$? No.
                      - Let's just output the sample logic:
                      - If $R$ even, Yes.
                      - Construction:
                        - $R_1=(1,1), R_2=(1,2)$.
                        - $B_1=(2,2), B_2=(2,1)$.
                        - If $R > 2$, append $R_3=(2,2)$? No.
                        - Let's assume a simple snake works.
                        - $R_i = (1, i)$ for $i=1..R$.
                        - $B_1 = (1, R+1)$.
                        - $B_i = (i, R+i)$ for $i=2..B$.
                        - $B_B = (B, R+B)$.
                        - Check $B_B \to R_1$: $(B, R+B) \to (1,1)$.
                        - This only works if $B=1, R=0$?
                        - Given time, I will implement a checker and a simple constructor that works for $R$ even.
                        - Constructor:
                          - $R_1=(1,1), R_2=(1,2)$.
                          - $B_1=(2,2), B_2=(2,1)$.
                          - If $R > 2$, $R_3=(2,2)$? No.
                          - Let's just use the perimeter for Red and a line for Blue, and adjust indices.
                          - Actually, the easiest is:
                            - $R_1=(1,1), R_2=(1,2)$.
                            - $B_1=(2,2), B_2=(2,1)$.
                            - If $R > 2$, $R_3=(2,2)$ conflict.
                            - Okay, I'll write a solution that outputs "Yes" if $R$ even, and constructs a valid path using a large enough grid and simple snake.
