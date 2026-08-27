
## ideation
The core difficulty lies in constructing a valid cycle of moves given the distinct movement rules for Red (orthogonal) and Blue (diagonal) pieces, while satisfying parity constraints.

1.  **Parity Analysis**:
    *   **Red Piece**: Moves $(r, c) \to (r\pm 1, c)$ or $(r, c\pm 1)$. The sum of coordinates $r+c$ changes by $\pm 1$. Thus, Red pieces always move between squares of different colors (in a chessboard coloring).
    *   **Blue Piece**: Moves $(r, c) \to (r\pm 1, c\pm 1)$. The sum of coordinates $r+c$ changes by $0$ or $\pm 2$. Thus, Blue pieces always stay on squares of the same color.
    *   **Cycle Constraint**: For a cycle to exist, the total parity change must be 0 modulo 2. Since only Red pieces change parity, the number of Red pieces $R$ must be even. If $R$ is odd, output "No".
    *   **Blue-only Case**: If $R=0$, all pieces are Blue. They must form a cycle on squares of the same color. The graph of diagonal moves on a single color class is bipartite (partitioned by the parity of the row index $r$). Therefore, any cycle must have even length. If $R=0$ and $B$ is odd, output "No".

2.  **Construction Strategy**:
    *   **Case $R > 0, B > 0$**: We can interleave Reds and Blues. A robust pattern is to create a "core" loop using 2 Reds and 2 Blues, and then extend it.
        *   Core Loop: $R_1(2,2) \to B_1(2,3) \to R_2(1,4) \to B_2(1,3) \to R_1(2,2)$.
        *   This uses 2 Reds and 2 Blues.
        *   If we have more Reds, we can insert them into the Red-to-Red transitions? No, Reds move to Blues.
        *   Actually, we can treat the Reds as nodes in a path and Blues as nodes in a path?
        *   Better approach: Place all Reds in a simple even cycle (since $R$ is even). Place all Blues in a simple even cycle (since if $R>0$, $B$ can be odd or even? Wait. If $R>0$, the parity constraint is only on $R$. $B$ can be odd. But can we connect an odd number of Blues to Reds?
        *   Let's check $R=2, B=1$. $R \to B \to R$. $R(2,2) \to B(2,3) \to R(1,4)$? No, $B(2,3)$ to $R(1,4)$ is diagonal, valid. $R(1,4)$ to $R(2,2)$? No, must go to $B$ or next $R$? The sequence is $P_1, P_2, \dots$.
        *   Sequence: $R_1, B_1, R_2$.
        *   $R_1(2,2) \xrightarrow{orth} B_1(2,3) \xrightarrow{diag} R_2(1,4) \xrightarrow{orth} R_1(2,2)$? No, $R_2$ must move to $P_1=R_1$. $R_2(1,4)$ to $R_1(2,2)$ is not orthogonal.
        *   So $R=2, B=1$ might be impossible?
        *   Let's re-evaluate. The cycle is $P_1 \to P_2 \to \dots \to P_{R+B} \to P_1$.
        *   If $R=2, B=1$, sequence $R, B, R$.
        *   $R_1 \to B_1$ (orth), $B_1 \to R_2$ (diag), $R_2 \to R_1$ (orth).
        *   $R_1(r,c)$. $B_1(r, c+1)$. $R_2(r-1, c+2)$ (diag from $B_1$). $R_1$ must be orth adjacent to $R_2$.
        *   $R_1(r,c)$ and $R_2(r-1, c+2)$. Distance is $\sqrt{1^2+2^2}$. Not orth adjacent.
        *   Try $R_2(r+1, c+2)$. Dist $\sqrt{1^2+2^2}$.
        *   Try $B_1(r, c-1)$. $R_2(r-1, c-2)$. Dist to $R_1(r,c)$ is $\sqrt{1^2+2^2}$.
        *   It seems $R=2, B=1$ is impossible.
        *   Hypothesis: If $B$ is odd, we need at least 2 Blues to form a "bridge" or loop?
        *   Actually, if $B$ is odd, the Blues form paths of odd length? No, Blues preserve parity.
        *   Let's look at the structure. The cycle alternates between "Red moves" and "Blue moves" in terms of graph edges, but the pieces are distinct.
        *   The condition is: $P_i$ moves to $P_{i+1}$.
        *   If $P_i$ is Red, $P_{i+1}$ must be orth adjacent.
        *   If $P_i$ is Blue, $P_{i+1}$ must be diag adjacent.
        
        Let's try a general construction for $R$ even, $B$ even.
        We can form a cycle of length $R+B$.
        If $B$ is odd, is it possible?
        Consider $R=4, B=1$. $R, B, R, R, R$.
        $R_1 \to B_1 \to R_2 \to R_3 \to R_4 \to R_1$.
        $R_1(2,2) \to B_1(2,3) \to R_2(1,4)$.
        $R_2(1,4) \to R_3(1,3) \to R_4(2,3)$? No, $B_1$ is at $(2,3)$. Distinct squares.
        $R_4(2,1) \to R_1(2,2)$.
        Path: $(2,2) \xrightarrow{B} (2,3) \xrightarrow{R} (1,4) \xrightarrow{R} (1,3) \xrightarrow{R} (2,3)$ Collision.
        
        It turns out that if $B$ is odd, we can't easily close the loop with Reds because Reds form a bipartite graph (orthogonal moves). A cycle involving Reds must have even length if it only involves Reds. With Blues, it's more complex.
        
        However, note that if $R > 0$, we can always pair up Reds.
        If $B$ is odd, we can use 2 Blues to make an even block, and the remaining $B-2$ Blues?
        Actually, if $R > 0$, we can construct a solution for ANY $B$?
        Let's check $R=2, B=1$ again. We found it likely impossible.
        What about $R=4, B=1$?
        
        Let's rely on the following sufficient conditions:
        1. $R$ is even.
        2. If $R=0$, $B$ is even.
        
        Is $R>0, B$ odd possible?
        Sample 1: $R=2, B=3$. Output Yes.
        So $B$ can be odd if $R>0$.
        
        Construction for $R=2, B=3$:
        Output:
        B 2 3
        R 3 2
        B 2 2
        B 3 3
        R 2 4
        
        Check:
        1. B(2,3) -> R(3,2): Diag? $|2-3|=1, |3-2|=1$. Yes.
        2. R(3,2) -> B(2,2): Orth? $|3-2|=1, |2-2|=0$. Yes.
        3. B(2,2) -> B(3,3): Diag? $|2-3|=1, |2-3|=1$. Yes.
        4. B(3,3) -> R(2,4): Diag? $|3-2|=1, |3-4|=1$. Yes.
        5. R(2,4) -> B(2,3): Orth? $|2-2|=0, |4-3|=1$. Yes.
        
        So $R>0$ allows any $B$.
        
        **General Algorithm**:
        1. If $R \% 2 != 0$, return "No".
        2. If $R == 0$ and $B \% 2 != 0$, return "No".
        3. Otherwise, "Yes".
