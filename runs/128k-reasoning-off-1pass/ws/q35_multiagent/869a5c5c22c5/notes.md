
## ideation
The core difficulty lies in satisfying the movement constraints for both Red and Blue pieces simultaneously in a cycle.
1.  **Parity Analysis**:
    *   Red pieces move orthogonally, changing the parity of $r+c$ (flipping parity).
    *   Blue pieces move diagonally, preserving the parity of $r+c$ (keeping parity).
    *   In the cycle, each Red piece contributes exactly one parity flip (transition to next piece). Each Blue piece contributes zero parity flips.
    *   For the cycle to close (return to start parity), the total number of parity flips must be even. Thus, $R$ must be even. If $R$ is odd, the answer is "No".

2.  **Constructive Strategy for Even R**:
    *   If $R$ is even, a solution always exists.
    *   We can construct a base cycle of $R$ Red pieces using orthogonal moves. A simple cycle is a rectangle of size $2 \times (R/2)$.
    *   Blue pieces can be inserted into the edges between Red pieces. An edge from Red $i$ to Red $i+1$ (orthogonal move) can be replaced by a path $R_i \to B_1 \to \dots \to B_k \to R_{i+1}$.
    *   Specifically, inserting a single Blue $B$ between $R_i(r,c)$ and $R_{i+1}(r, c+1)$ can be done by placing $B$ at $(r+1, c)$.
        *   $R_i(r,c) \to B(r+1,c)$ is orthogonal (valid for Red).
        *   $B(r+1,c) \to R_{i+1}(r, c+1)$ is diagonal (valid for Blue).
    *   To handle multiple Blues and avoid collisions, we can distribute the $B$ Blues across different edges of the Red cycle. Since we have $R$ edges and $R \ge 2$ (if $R>0$), and if $R=0$ then $B$ must be even? No, if $R=0$, we only have Blues. Blue moves preserve parity. A cycle of Blues requires them to form a closed loop of diagonal moves. This is possible if $B$ is even? Actually, a single Blue cannot form a cycle alone ($B \ge 2$). A cycle of Blues is just a path where each step is diagonal. This forms a bipartite graph component? No, diagonal moves on a grid preserve $r+c \pmod 2$. All Blues must have the same parity of coordinates. They can form a cycle if $B \ge 2$ and we arrange them properly (e.g., a $2 \times 2$ diamond shape).
    *   However, the problem states $R+B \ge 2$.
    *   Case $R=0$: Only Blues. We need a cycle of Blues. A simple cycle of length $B$ using diagonal moves exists if $B$ is even? Actually, any cycle in the diagonal graph (which is two disconnected grids based on parity) must have even length? No, the diagonal graph is bipartite? No, diagonal moves connect $(r,c)$ to $(r\pm 1, c\pm 1)$. $r+c$ changes by $\pm 2$ or $0$. So parity is invariant. The graph splits into two components: even sum and odd sum. Within one component, can we have odd cycles? Yes, e.g., $(1,1) \to (2,2) \to (1,3) \to (2,4) \dots$ wait. $(1,1) \to (2,2) \to (1,3)$ is valid. $(1,3) \to (2,2)$ is valid. $(2,2) \to (1,1)$ is valid. This is a triangle? No, $(1,1)$ to $(1,3)$ is not a diagonal move.
    *   Actually, simpler: If $R=0$, we can just place Blues in a $2 \times 2$ block if $B=2$? $(1,1) \to (2,2) \to (1,1)$ is length 2. For $B > 2$, we can extend. But wait, if $R=0$, $B$ can be odd? Sample 2 is $R=1, B=1 \to$ No. Sample 1 is $R=2, B=3 \to$ Yes.
    *   Let's check $R=0, B=3$. Can we place 3 Blues in a cycle?
        *   $B_1(1,1) \to B_2(2,2) \to B_3(1,3) \to B_1(1,1)$?
        *   $B_3(1,3) \to B_1(1,1)$: $\Delta r = 0, \Delta c = -2$. Not diagonal.
        *   It turns out a cycle of only Blues requires $B$ to be even? Or can we have odd?
        *   Actually, if $R=0$, the condition "Red moves" doesn't apply. Only Blue moves.
        *   Blue moves preserve parity. So all Blues must be on squares with same $r+c \pmod 2$.
        *   The graph of diagonal moves on a fixed parity grid is bipartite?
            *   Let $u = (r,c)$. Neighbors are $(r\pm 1, c\pm 1)$.
            *   Consider coloring by $r \pmod 2$.
            *   If $r$ is even, neighbors have $r$ odd.
            *   If $r$ is odd, neighbors have $r$ even.
            *   So yes, the diagonal graph is bipartite (partitioned by row parity).
            *   Therefore, any cycle must have even length.
            *   So if $R=0$, $B$ must be even.
    *   Combined with $R$ even, the condition is: **$R$ must be even**. (If $R=0$, $B$ must be even, which is consistent with $R$ even? No, $R=0$ is even. But if $R=0$ and $B$ is odd, is it No? Yes. So the condition is: If $R=0$, $B$ must be even. If $R>0$, $R$ must be even.
    *   Wait, if $R>0$ and $B$ is odd, is it possible?
        *   Sample 1: $R=2, B=3$. $R$ is even. Output Yes.
        *   So if $R>0$, $R$ even is sufficient.
        *   If $R=0$, we need $B$ even.
    *   So the condition is: **If $R=0$, $B$ must be even. If $R>0$, $R$ must be even.**
    *   This can be summarized as: **$R$ must be even, AND if $R=0$ then $B$ must be even.**
    *   Actually, if $R>0$, we can always satisfy the cycle regardless of $B$'s parity because Blues can be inserted into Red edges.
    *   So:
        *   If $R$ is odd: No.
        *   If $R=0$: If $B$ is even: Yes. If $B$ is odd: No.
        *   If $R$ is even and $R>0$: Yes.

3.  **Construction Details**:
    *   **Case $R=0, B$ even**: Place Blues in a simple cycle. E.g., for $B=2$, $(1,1), (2,2)$. For $B=4$, $(1,1), (2,2), (1,3), (2,4)$? No, need cycle.
        *   Simple cycle for Blues: Use a $2 \times (B/2)$ rectangle perimeter? No, diagonal moves.
        *   Use a "zig-zag" that closes.
        *   Actually, just use the same logic as Red but with diagonal moves.
        *   Place Blues at $(1,1), (2,2), (1,3), (2,4), \dots$
        *   This forms a path. To close, last must connect to first.
        *   If $B$ is even, we can form a cycle. E.g., $B=2$: $(1,1) \leftrightarrow (2,2)$.
        *   $B=4$: $(1,1) \to (2,2) \to (1,3) \to (2,4) \to (1,1)$?
            *   $(2,4) \to (1,1)$: $\Delta r = -1, \Delta c = -3$. Not diagonal.
        *   Better: Place Blues in a $2 \times 2$ block repeated?
        *   Actually, if $R>0$, we can just use the Red cycle and insert Blues.
        *   If $R=0$, we handle separately.

    *   **Case $R>0, R$ even**:
        *   Construct Red cycle on $2 \times (R/2)$ grid.
        *   Distribute $B$ Blues into the $R$ edges.
        *   For each edge, if we assign $k$ Blues, we insert them.
        *   To avoid collision, we can use unique "detour" coordinates for each Blue insertion.
        *   Since coordinates up to $10^9$, we can shift rows/cols.
