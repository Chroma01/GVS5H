1.  **Analyze Connectivity**: The problem requires forming a cycle of length $N = R+B$ where adjacent pieces in the cycle must be "one move apart" according to their type. Red pieces move like Kings (Chebyshev distance 1, but only orthogonal), Blue pieces move like Bishops (diagonal distance 1).
2.  **Parity and Bipartite Graph**:
    *   Red moves change the parity of $r+c$ (e.g., $(r,c) \to (r+1,c)$ changes sum by 1). So Red connects squares of different parity.
    *   Blue moves preserve the parity of $r+c$ (e.g., $(r,c) \to (r+1,c+1)$ changes sum by 2). So Blue connects squares of the same parity.
    *   Let the cycle be $p_1, p_2, \dots, p_N$. The condition is that $p_i$ and $p_{i+1}$ are adjacent.
    *   If we have a Blue piece, it must be adjacent to two other pieces. Since Blue stays on the same parity, its neighbors must also be on the same parity square? No, the *destination* of a Blue move is same parity. So if $p_i$ is Blue at $(r,c)$, $p_{i-1}$ and $p_{i+1}$ must be at squares with same parity as $(r,c)$.
    *   If $p_i$ is Red, it connects a square of parity $P$ to $P+1$.
3.  **Case Analysis**:
    *   **Case $B=0$**: All pieces are Red. The graph is a grid graph (orthogonal moves). A cycle exists if $R \ge 3$? No, a simple cycle of length $R$ in a grid. A $2 \times 2$ square gives a cycle of length 4. Can we make a cycle of length 3? No, grid is bipartite, so no odd cycles. Thus, if $B=0$, we need $R \ge 3$ and $R$ even? Wait. A cycle in a bipartite graph must be even length. So if $B=0$, we need $R$ even and $R \ge 4$? Sample 3: $R=4, B=0$ works. Sample 2: $R=1, B=1$.
    *   **Case $R=0$**: All Blue. Blue moves preserve parity. All pieces must be on squares of the same parity (all black or all white). Also, they must form a cycle. Since Blue moves are diagonal, this is equivalent to a grid graph on a rotated coordinate system. A cycle of length $B$ exists if $B \ge 3$? But wait, can we have a cycle of length 3 with only Blue? No, because the "diagonal grid" is also bipartite (checkerboard of the checkerboard). So $B$ must be even and $B \ge 4$? Let's check small cases. $B=2$: Two blues. $p_1$ Blue, $p_2$ Blue. $p_1$ moves to $p_2$, $p_2$ moves to $p_1$. This is a cycle of length 2. Is a 2-cycle allowed? The problem says "move in one move to the square containing the next". It doesn't forbid revisiting or 2-cycles explicitly, but "place all pieces... at most one piece per square". So $p_1 \neq p_2$. $p_1$ moves to $p_2$ and $p_2$ moves to $p_1$. This is valid. So $B=2$ works. $B=1$? $R+B \ge 2$, so $B=1, R=0$ is not possible by constraints ($R+B \ge 2$). If $R=0, B=1$, invalid input. If $R=0, B=2$, valid.
    *   **Mixed Case**:
        *   If we have at least one Red and one Blue:
            *   Red connects different parities. Blue connects same parity.
            *   Consider the sequence of parities.
            *   Key Insight: If $R \ge 1$ and $B \ge 1$, we can often construct a solution.
            *   Exception: $R=1, B=1$. Cycle $p_1, p_2$. $p_1$ Red, $p_2$ Blue.
                *   If $p_1$ is Red, it connects to $p_2$ (Blue). Red move: different parity. So $p_2$ is on different parity than $p_1$.
                *   $p_2$ is Blue. It must connect to $p_1$. Blue move: same parity. So $p_1$ must be on same parity as $p_2$.
                *   Contradiction: $p_1$ must be different parity from $p_2$ AND same parity as $p_2$. Impossible. So $R=1, B=1$ is No.
            *   What about $R=1, B=2$?
                *   Cycle $R, B, B$.
                *   $R$ (at $P$) $\to$ $B$ (at $P'$). Red move: $P' \neq P$.
                *   $B$ (at $P'$) $\to$ $B$ (at $P''$). Blue move: $P'' = P'$.
                *   $B$ (at $P''$) $\to$ $R$ (at $P$). Blue move: $P = P''$.
                *   So $P = P'' = P'$. But first step said $P' \neq P$. Contradiction.
                *   So $R=1, B=2$ is No? Let's re-read carefully.
                *   Wait, the cycle is undirected in terms of adjacency? No, "i-th piece ... move to ... (i+1)-th". It's a directed cycle of moves.
                *   Let's check $R=2, B=1$.
                *   $R_1 \to B \to R_2 \to R_1$.
                *   $R_1(P) \to B(P')$: $P' \neq P$.
                *   $B(P') \to R_2(P'')$: $P'' = P'$.
                *   $R_2(P'') \to R_1(P)$: $P \neq P''$.
                *   So $P'' = P'$ and $P \neq P'$. This is consistent.
                *   Can we place them?
                    *   $R_1$ at $(1,1)$ (sum 2, even).
                    *   $B$ at $(1,2)$ (sum 3, odd). Move $(1,1) \to (1,2)$ is Red move? Yes, $(1,1) \to (1,2)$ is horizontal.
                    *   $R_2$ at $(1,2)$? No, distinct squares.
                    *   $B$ is at $(1,2)$. $B$ moves to $R_2$. Blue move from $(1,2)$: $(2,3), (2,1), (0,3)...$. Let's pick $(2,1)$ (sum 3, odd).
                    *   $R_2$ at $(2,1)$.
                    *   $R_2$ moves to $R_1$. Red move from $(2,1)$ to $(1,1)$? Yes, vertical.
                    *   Squares: $R_1(1,1)$, $B(1,2)$, $R_2(2,1)$. All distinct.
                    *   So $R=2, B=1$ works.
            *   General Rule for Mixed:
                *   If $R=1$, we saw $B=1$ fails, $B=2$ fails.
                *   Try $R=1, B=3$.
                    *   $R \to B_1 \to B_2 \to B_3 \to R$.
                    *   $R(P) \to B_1(P')$: $P' \neq P$.
                    *   $B_1(P') \to B_2(P'')$: $P'' = P'$.
                    *   $B_2(P'') \to B_3(P''')$: $P''' = P''$.
                    *   $B_3(P''') \to R(P)$: $P = P'''$.
                    *   So $P = P'$. Contradiction ($P' \neq P$).
                    *   So if $R=1$, any $B$ fails?
                    *   Let's check $R=1, B=4$.
                    *   $R \to B_1 \to B_2 \to B_3 \to B_4 \to R$.
                    *   Parity chain: $P \xrightarrow{R} P' (\neq P) \xrightarrow{B} P' \xrightarrow{B} P' \xrightarrow{B} P' \xrightarrow{B} P' \xrightarrow{R} P$.
                    *   Last step: Blue move from $B_4$ to $R$. Blue preserves parity. So $Parity(B_4) = Parity(R)$.
                    *   But $B_4$ has parity $P'$ (from start). And $P' \neq P$. Contradiction.
                    *   So if $R=1$, it is always **No**.
                *   Similarly, if $B=1$, does it always work (except maybe small R)?
                    *   $B=1$. Cycle $R_1 \to \dots \to R_k \to B \to R_1$.
                    *   Parity: $P_1 \xrightarrow{R} P_2 \dots \xrightarrow{R} P_k \xrightarrow{R} P_{B} \xrightarrow{B} P_1$.
                    *   Blue move $B \to R_1$ implies $Parity(B) = Parity(R_1) = P_1$.
                    *   The chain of Reds: $R_1(P_1) \to R_2(P_2) \dots \to R_k(P_k) \to B(P_B)$.
                    *   Each Red flips parity. So $P_B = P_1 + k \pmod 2$.
                    *   We need $P_B = P_1$. So $k$ must be even.
                    *   So if $B=1$, we need $R$ even. And $R \ge 2$?
                    *   If $R=2, B=1$: Works (shown above).
                    *   If $R=4, B=1$: Works.
                    *   So if $B=1$, need $R$ even.
    *   **Summary of Conditions**:
        1.  If $R=0$: Need $B$ even and $B \ge 2$?
            *   $B=2$: Yes.
            *   $B=3$: No (odd cycle in bipartite).
            *   $B=4$: Yes.
            *   So $B$ even, $B \ge 2$.
        2.  If $B=0$: Need $R$ even and $R \ge 4$?
            *   $R=2$: No (bipartite, min cycle 4).
            *   $R=3$: No (odd).
            *   $R=4$: Yes.
            *   So $R$ even, $R \ge 4$.
        3.  If $R=1$: Always **No**.
        4.  If $B=1$: Need $R$ even and $R \ge 2$.
        5.  If $R \ge 2$ and $B \ge 2$:
            *   We can likely always construct a solution.
            *   Let's verify $R=2, B=2$.
                *   Parity check:
                *   $R_1 \to B_1 \to B_2 \to R_2 \to R_1$.
                *   $P_1 \xrightarrow{R} P_2 (\neq P_1) \xrightarrow{B} P_2 \xrightarrow{B} P_2 \xrightarrow{R} P_3 (\neq P_2) \xrightarrow{R} P_1$.
                *   Last step $R_2 \to R_1$: $P_1 \neq P_3$.
                *   So we need $P_3 \neq P_2$ and $P_1 \neq P_3$.
                *   This implies $P_1 = P_2$? No.
                *   $P_2 = P_1 + 1$.
                *   $P_3 = P_2 + 1 = P_1$.
                *   Last step: $R_2(P_3) \to R_1(P_1)$. Red move requires $P_1 \neq P_3$.
                *   But we derived $P_3 = P_1$. Contradiction.
                *   So $R=2, B=2$ is **No**?
                *   Let's re-evaluate the parity chain for $R=2, B=2$.
                *   Order: $R_1, B_1, B_2, R_2$.
                *   $R_1(P_1) \to B_1(P_2)$: $P_2 \neq P_1$.
                *   $B_1(P_2) \to B_2(P_3)$: $P_3 = P_2$.
                *   $B_2(P_3) \to R_2(P_4)$: $P_4 \neq P_3$.
                *   $R_2(P_4) \to R_1(P_1)$: $P_1 \neq P_4$.
                *   From above: $P_2 = P_1+1$. $P_3 = P_2 = P_1+1$. $P_4 = P_3+1 = P_1+2 = P_1$.
                *   Condition: $P_1 \neq P_4 \implies P_1 \neq P_1$. False.
                *   So $R=2, B=2$ is No.
            *   What about $R=3, B=2$?
                *   $R_1 \to B_1 \to B_2 \to R_2 \to R_3 \to R_1$.
                *   $P_1 \xrightarrow{R} P_2 (\neq) \xrightarrow{B} P_2 \xrightarrow{B} P_2 \xrightarrow{R} P_3 (\neq) \xrightarrow{R} P_4 (\neq) \xrightarrow{R} P_1 (\neq)$.
                *   $P_2 = P_1+1$.
                *   $P_3 = P_2+1 = P_1$.
                *   $P_4 = P_3+1 = P_1+1$.
                *   Last: $P_1 \neq P_4 \implies P_1 \neq P_1+1$. True.
                *   So $R=3, B=2$ works.
            *   What about $R=2, B=3$? (Sample 1)
                *   $R_1 \to B_1 \to B_2 \to B_3 \to R_2 \to R_1$.
                *   $P_1 \xrightarrow{R} P_2 (\neq) \xrightarrow{B} P_2 \xrightarrow{B} P_2 \xrightarrow{B} P_2 \xrightarrow{R} P_3 (\neq) \xrightarrow{R} P_1 (\neq)$.
                *   $P_2 = P_1+1$.
                *   $P_3 = P_2+1 = P_1$.
                *   Last: $P_1 \neq P_3 \implies P_1 \neq P_1$. False.
                *   Wait, Sample 1 says $R=2, B=3$ is **Yes**.
                *   My parity analysis assumes a specific order. The problem allows *any* order.
                *   In Sample 1 output: $B, R, B, B, R$.
                *   Let's trace:
                    1. $B(2,3)$ sum 5 (odd).
                    2. $R(3,2)$ sum 5 (odd). Move $B \to R$: Blue at $(2,3)$ to $R$ at $(3,2)$? $(2,3) \to (3,2)$ is diagonal. Yes.
                    3. $B(2,2)$ sum 4 (even). Move $R \to B$: Red at $(3,2)$ to $B$ at $(2,2)$? $(3,2) \to (2,2)$ is vertical. Yes.
                    4. $B(3,3)$ sum 6 (even). Move $B \to B$: $(2,2) \to (3,3)$ diagonal. Yes.
                    5. $R(2,4)$ sum 6 (even). Move $B \to R$: $(3,3) \to (2,4)$ diagonal? No, Blue moves diagonal. $(3,3) \to (2,4)$ is diagonal. Yes.
                    6. Move $R \to B$ (first): $R(2,4)$ to $B(2,3)$. Horizontal. Yes.
                *   Parity Chain:
                    *   $B_1(5) \xrightarrow{B} R_1(5)$: Blue move preserves parity. $5=5$. OK.
                    *   $R_1(5) \xrightarrow{R} B_2(4)$: Red move flips. $5 \to 4$. OK.
                    *   $B_2(4) \xrightarrow{B} B_3(6)$: Blue preserves. $4=6$? No, $4$ is even, $6$ is even. Parity is same. OK.
                    *   $B_3(6) \xrightarrow{B} R_2(6)$: Blue preserves. $6=6$. OK.
                    *   $R_2(6) \xrightarrow{R} B_1(5)$: Red flips. $6 \to 5$. OK.
                *   So the key is the **order** of pieces.
                *   General Strategy:
                    *   If we can group Blues together and Reds together, we can manage parities.
                    *   If $R=0$: $B$ even, $B \ge 2$.
                    *   If $B=0$: $R$ even, $R \ge 4$.
                    *   If $R=1$: No.
                    *   If $B=1$: $R$ even, $R \ge 2$.
                    *   If $R \ge 2, B \ge 2$:
                        *   We need to form a cycle.
                        *   If we put all Blues in a contiguous block and all Reds in a contiguous block:
                            *   $B_1 \dots B_B \to R_1 \dots R_R \to B_1$.
                            *   $B_1 \xrightarrow{B} \dots \xrightarrow{B} B_B$: Parity $P_B$.
                            *   $B_B \xrightarrow{R} R_1$: Flip. $P_{R1} = P_B + 1$.
                            *   $R_1 \xrightarrow{R} \dots \xrightarrow{R} R_R$: $R$ flips. $P_{RR} = P_{R1} + R = P_B + 1 + R$.
                            *   $R_R \xrightarrow{R} B_1$: Flip. $P_{B1} = P_{RR} + 1 = P_B + R + 2$.
                            *   We need $P_{B1} = P_B$.
                            *   So $R+2$ must be even $\implies R$ even.
                            *   So if we use this "block" structure, we need $R$ even.
                            *   Sample 1 ($R=2, B=3$) has $R$ even. Works.
                            *   What if $R$ is odd and $B \ge 2$?
                            *   Try interleaving?
                            *   If $R=3, B=2$. Block structure: $R$ odd $\implies$ fails block.
                            *   But we found $R=3, B=2$ works with order $R, B, B, R, R$.
                            *   Let's check parity for $R, B, B, R, R$:
                                *   $R_1(P) \to B_1(P')$: $P' \neq P$.
                                *   $B_1(P') \to B_2(P')$: $P' = P'$.
                                *   $B_2(P') \to R_2(P'')$: $P'' \neq P'$.
                                *   $R_2(P'') \to R_3(P''')$: $P''' \neq P''$.
                                *   $R_3(P''') \to R_1(P)$: $P \neq P'''$.
                                *   $P' = P+1$.
                                *   $P'' = P'+1 = P$.
                                *   $P''' = P''+1 = P+1$.
                                *   Last: $P \neq P+1$. True.
                                *   So $R=3, B=2$ works.
                            *   It seems if $R \ge 2$ and $B \ge 2$, it is always Yes?
                            *   Check $R=2, B=2$ again.
                                *   Block: $R$ even $\implies$ should work?
                                *   Wait, earlier I proved $R=2, B=2$ block fails.
                                *   $R_1 \to R_2 \to B_1 \to B_2 \to R_1$.
                                *   $P_1 \xrightarrow{R} P_2 (\neq) \xrightarrow{R} P_3 (=) \xrightarrow{B} P_3 \xrightarrow{B} P_3 \xrightarrow{R} P_1 (\neq)$.
                                *   $P_2 = P_1+1$.
                                *   $P_3 = P_2+1 = P_1$.
                                *   $P_B = P_3 = P_1$.
                                *   Last: $P_1 \neq P_1$. False.
                                *   Try different order for $R=2, B=2$: $R, B, R, B$.
                                *   $R_1(P) \to B_1(P')$: $P' \neq P$.
                                *   $B_1(P') \to R_2(P'')$: $P'' = P'$.
                                *   $R_2(P'') \to B_2(P''')$: $P''' \neq P''$.
                                *   $B_2(P''') \to R_1(P)$: $P = P'''$.
                                *   $P' = P+1$.
                                *   $P'' = P+1$.
                                *   $P''' = P+2 = P$.
                                *   Last: $P = P$. True.
                                *   So $R=2, B=2$ works with order $R, B, R, B$.
                            *   So $R \ge 2, B \ge 2$ is always Yes.

4.  **Final Conditions**:
    *   If $R=0$: Yes if $B$ even and $B \ge 2$.
    *   If $B=0$: Yes if $R$ even and $R \ge 4$.
    *   If $R=1$: No.
    *   If $B=1$: Yes if $R$ even and $R \ge 2$.
    *   If $R \ge 2$ and $B \ge 2$: Yes.

5.  **Construction**:
    *   **$B=0, R \ge 4$ even**: Use a $2 \times (R/2)$ rectangle? Or just a simple cycle.
        *   E.g., $R=4$: $(1,1)-(1,2)-(2,2)-(2,1)-(1,1)$.
        *   General: Place Reds in a $2 \times k$ grid where $2k=R$. Cycle around the perimeter? No, that's $2k+2$?
        *   Simple cycle: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (3,1) \dots$
        *   Actually, just use a $2 \times 2$ block repeated?
        *   Easier: Place them on a single row? No, need to return.
        *   Standard cycle: $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (3,1) \to (3,2) \to (4,2) \to (4,1) \dots$
        *   This zig-zags. Length $R$.
    *   **$R=0, B \ge 2$ even**: Similar diagonal cycle.
    *   **$B=1, R$ even $\ge 2$**:
        *   Place $R$ pieces in a cycle, insert $B$ in one edge?
        *   Or use the $R=2, B=1$ pattern and expand.
    *   **$R=1, B=1$**: No.
    *   **Mixed $R \ge 2, B \ge 2$**:
        *   Use order $R, B, R, B, \dots$ if possible?
        *   Or group Blues and Reds.
        *   Since we just need *one* example, we can hardcode constructions for small cases and general patterns for large.