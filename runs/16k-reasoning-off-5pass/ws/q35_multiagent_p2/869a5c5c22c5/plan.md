The problem requires constructing a cycle of length $N = R+B$ where consecutive pieces are adjacent according to their movement rules (Red: Manhattan distance 1, Blue: Chebyshev distance 1, specifically diagonal steps). This is equivalent to finding a cycle in a graph where nodes are board squares and edges connect squares reachable by one move of either piece type. However, since we assign types to positions in the cycle, the constraint is that if position $i$ is Red and $i+1$ is Blue, the distance must be compatible. Specifically:
- Red to Red: Manhattan dist 1.
- Blue to Blue: Diagonal dist 1 (Manhattan dist 2, same color parity).
- Red to Blue: Red moves to adjacent (Manhattan 1). Blue is at that square. Blue moves diagonally to next. So Red at $(r,c)$, Blue at $(r\pm 1, c)$ or $(r, c\pm 1)$. The Blue piece is on a square of opposite color parity to Red? No. Red at $(r,c)$ has parity $r+c$. Blue at $(r\pm 1, c)$ has parity $r+c \pm 1$. So they have different parity.
- Blue to Red: Blue at $(r,c)$ moves diagonally to $(r\pm 1, c\pm 1)$. Red is at that square. Parity of Blue: $r+c$. Parity of Red: $r+c \pm 2 \equiv r+c \pmod 2$. So Blue and Red must have same parity? Wait.
Let's check parity constraints.
Red moves change parity of $r+c$ by 1.
Blue moves change parity of $r+c$ by $1+1=2$ or $1-1=0$, so parity is invariant for Blue.
Therefore:
- If we have a sequence of pieces, the parity of the square $(r_i, c_i)$ changes by 1 if $p_i$ is Red. It stays same if $p_i$ is Blue.
- Let $P_i = (r_i + c_i) \pmod 2$.
- If $p_i = R$, $P_{i+1} = 1 - P_i$.
- If $p_i = B$, $P_{i+1} = P_i$.
- The cycle closes: $P_1$ must equal $P_{N+1}$ (which is determined by the sequence of moves from 1 to N).
- Specifically, $P_{N+1} = P_1 + (\text{number of Reds in } 1 \dots N) \pmod 2$.
- For a valid cycle, we need $P_{N+1} = P_1$, so the number of Reds $R$ must be even.
- If $R$ is odd, it's impossible? Let's check Sample 2: R=1, B=1. Output No. Correct.
- Sample 1: R=2, B=3. R is even. Output Yes.
- Sample 3: R=4, B=0. R is even. Output Yes.
- What if R=0? Then all are Blue. Blue moves preserve parity. So all squares must have same parity. A cycle of Blues is possible if we can form a cycle using only diagonal moves. This requires a bipartite-like structure on the "diagonal graph". Actually, Blue moves connect $(r,c)$ to $(r\pm 1, c\pm 1)$. This graph is bipartite? No, $(r,c) \to (r+1, c+1) \to (r+2, c+2) \dots$. It's a set of independent lines. Can we form a cycle? Only if we can turn around. But Blue moves are strictly diagonal. You cannot return to start in a cycle of length > 1 using only diagonal moves on a grid? Wait. $(1,1) \to (2,2) \to (1,1)$ is a cycle of length 2. Yes. So B=2 is possible. B=1? No, need cycle length >=2.
- So, necessary condition: R must be even.
- Is it sufficient?
- If R > 0 and even, we can construct a "base" cycle involving Reds and Blues.
- Strategy:
  1. If R=0: If B=1, No. If B>=2, Yes. Construct a simple cycle of 2 Blues: $(1,1), (2,2)$ and back? No, the cycle is $p_1 \to p_2 \dots \to p_N \to p_1$.
     For B=2: $B(1,1) \to B(2,2) \to B(1,1)$. Move 1: B at (1,1) to (2,2). Move 2: B at (2,2) to (1,1). Valid.
     For B>2, we can extend or use a larger loop. E.g., $(1,1)-(2,2)-(1,3)-(2,2)$? No, distinct squares.
     We can use a "diamond" or just repeat a pattern? No, distinct squares.
     For B Blues, we can place them on a cycle like $(1,1) \to (2,2) \to (1,3) \to (2,4) \dots$?
     Actually, if R=0, we just need a cycle in the diagonal graph. The diagonal graph consists of components based on $r-c$ and $r+c$.
     Simplest: If B is even, we can pair them up? No, one cycle.
     We can construct a cycle of length B using coordinates $(1, 1), (2, 2), \dots, (B/2, B/2)$ and then back? No, must be distinct.
     Consider a rectangle: $(1,1) \to (2,2) \to (1,3) \to (2,4) \dots$ this doesn't close easily.
     Better: Use a $2 \times 2$ block for 2 Blues. For more, expand.
     Actually, if R=0, B must be even?
     Parity argument: Blue preserves parity. So all B pieces are on same parity squares.
     Can we form a cycle of any even length B >= 2 on same parity squares using diagonal moves?
     Yes. Example for B=4: $(1,1) \to (2,2) \to (1,3) \to (2,2)$? No, distinct.
     $(1,1) \to (2,2) \to (3,1) \to (2,0)$? Out of bounds.
     $(1,1) \to (2,2) \to (1,3) \to (2,2)$ is invalid.
     Try: $(1,1) \to (2,2) \to (3,1)$? No, $(2,2)$ to $(3,1)$ is diagonal. $(3,1)$ to $(1,1)$? No, dist 2.
     How about $(1,1) \to (2,2) \to (1,3) \to (2,4) \to (1,3)$? No.
     Let's use a "zig-zag" that closes.
     Actually, if R=0, B=2: Yes.
     If R=0, B=4: $(1,1) \to (2,2) \to (1,3) \to (2,2)$? No.
     $(1,1) \to (2,2) \to (3,1) \to (2,0)$?
     Let's try: $(1,2) \to (2,1) \to (1,2)$? No, distinct.
     $(1,2) \to (2,1) \to (3,2) \to (2,3) \to (1,2)$.
     Moves:
     1. B at (1,2) to (2,1). Valid.
     2. B at (2,1) to (3,2). Valid.
     3. B at (3,2) to (2,3). Valid.
     4. B at (2,3) to (1,2). Valid.
     This is a cycle of 4 Blues.
     Generalizing: For B Blues, we can form a cycle of length B if B is even and B>=2.
     
  2. If R > 0 and R is even:
     We can mix Reds and Blues.
     A simple unit is a Red-Red pair or Red-Blue interaction.
     Consider a "cross" or small loop.
     Example from Sample 1: R=2, B=3.
     Output: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4).
     Let's trace:
     1. B(2,3) -> R(3,2). Dist: $|2-3|+|3-2|=2$. Wait. Red moves 1 step.
        The condition is: $i$-th piece moves to $(i+1)$-th.
        So B at (2,3) moves to R at (3,2)?
        Blue moves diagonally. $(2,3) \to (3,2)$ is diagonal ($+1, -1$). Valid.
     2. R(3,2) -> B(2,2).
        Red moves vertically/horizontally. $(3,2) \to (2,2)$ is vertical. Valid.
     3. B(2,2) -> B(3,3).
        Blue moves diagonally. $(2,2) \to (3,3)$ is diagonal. Valid.
     4. B(3,3) -> R(2,4).
        Blue moves diagonally. $(3,3) \to (2,4)$ is diagonal ($-1, +1$). Valid.
     5. R(2,4) -> B(2,3).
        Red moves horizontally. $(2,4) \to (2,3)$ is horizontal. Valid.
     
     This works. The key is that we can construct a cycle by alternating or grouping.
     Since R is even, we can pair up Reds.
     A robust construction:
     Use a "base" cycle of length 4 involving 2 Reds and 2 Blues?
     Or just 2 Reds?
     If B=0, R even: Cycle of Reds. E.g., $(1,1)-(1,2)-(2,2)-(2,1)-(1,1)$. Length 4.
     If R=2, B=0: $(1,1)-(1,2)-(1,1)$? No, distinct squares.
     So if B=0, R must be >= 2? But distinct squares required.
     Cycle of 2 Reds: $(1,1) \to (1,2) \to (1,1)$? No, $p_2$ must be distinct from $p_1$.
     So min cycle for Reds is 4? Or can we do 2?
     $(1,1) \to (1,2)$. Then $(1,2) \to (1,1)$.
     $p_1=R(1,1), p_2=R(1,2)$.
     Move 1: R(1,1) to R(1,2). OK.
     Move 2: R(1,2) to R(1,1). OK.
     Are squares distinct? Yes.
     So R=2, B=0 is possible.
     
     General Construction Plan:
     - If R is odd: No.
     - If R=0:
       - If B=1: No.
       - If B>=2: Yes. Construct a cycle of B Blues.
         We can use a "rectangle" like pattern or a simple loop.
         For B=2: $(1,1), (2,2)$.
         For B=4: $(1,2), (2,1), (3,2), (2,3)$.
         For general even B, we can create a "snake" or use a $2 \times K$ area.
         Actually, we can just use a cycle of length B on a "diagonal strip".
         Coordinates: $(1, 1), (2, 2), \dots$ doesn't close.
         Use the pattern:
         For $k=0 \dots B/2-1$:
         $P_{2k+1} = (1 + k, 2)$
         $P_{2k+2} = (2 + k, 1)$
         This creates pairs. Do they connect?
         $P_1(1,2) \to P_2(2,1)$ (Diagonal).
         $P_2(2,1) \to P_3(2,2)$? No, $P_3$ is $(2,2)$ if k=1?
         Let's define:
         $P_{2k+1} = (1+k, 2)$
         $P_{2k+2} = (2+k, 1)$
         Connection $P_{2k+2} \to P_{2k+3}$:
         $P_{2k+2} = (2+k, 1)$. $P_{2k+3} = (2+k, 2)$ (since next k is k+1, $1+(k+1) = 2+k$).
         Move: $(2+k, 1) \to (2+k, 2)$. This is horizontal. But piece $2k+2$ is Blue. Blue cannot move horizontally.
         So this pattern fails for B->B transition if we alternate coordinates like that.
         
         Correct B-only cycle:
         We need $B_i \to B_{i+1}$ to be diagonal.
         Try: $(1,1) \to (2,2) \to (1,3) \to (2,4) \dots$
         This is a path. To close, we need to return.
         If B is even, say B=2m.
         Points: $(1,1), (2,2), (1,3), (2,4), \dots, (1, 2m-1), (2, 2m)$.
         Last point $(2, 2m)$ needs to go to $(1,1)$.
         Dist: $|2-1| + |2m-1| = 1 + 2m - 1 = 2m$. Not diagonal.
         
         Alternative: Use a "loop" of 4 and repeat?
         We can construct a cycle of length B by taking a base cycle of 4 and "inserting" pairs?
         Or simply:
         If B=2: $(1,1), (2,2)$.
         If B>2 and even:
         Use a "diamond" shape extended?
         Actually, if we have R>0, we can mix.
         
     - If R>0 and even:
       We can construct a cycle using a "core" of 2 Reds and 2 Blues (length 4) and then add remaining pieces.
       Core:
       $R_1(1,1) \to B_1(1,2) \to R_2(2,2) \to B_2(2,1) \to R_1(1,1)$.
       Check:
       $R(1,1) \to B(1,2)$: Red moves right. OK.
       $B(1,2) \to R(2,2)$: Blue moves diag $(+1,0)$? No, $(1,2)\to(2,2)$ is vertical. Blue cannot move vertically.
       
       Let's use the Sample 1 structure for R=2, B=3.
       We can generalize:
       Place 2 Reds at $(1,1)$ and $(1,2)$.
       Place Blues around them.
       
       Simpler approach:
       If R is even and R>=2:
       We can form a cycle of just Reds if B=0.
       If B>0, we can "insert" Blues into the Red cycle or vice versa.
       
       Let's use a standard "grid cycle" for Reds and replace some edges with Blue paths?
       No, Blue moves are specific.
       
       Let's try a constructive algorithm:
       1. If R % 2 != 0: return No.
       2. If R == 0:
          If B == 1: return No.
          If B >= 2:
             Construct a cycle of B Blues.
             We can use a $2 \times (B/2)$ block?
             Let's try:
             For $i$ from 0 to $B/2 - 1$:
                $P_{2i+1} = (1+i, 1)$
                $P_{2i+2} = (1+i, 2)$
             This is Red-like.
             
             For Blues, we need diagonal.
             Let's use coordinates:
             $P_k = (1 + (k-1)//2, 1 + (k-1)%2)$? No.
             
             Let's use the following pattern for B Blues:
             If B=2: $(1,1), (2,2)$.
             If B=4: $(1,2), (2,1), (3,2), (2,3)$.
             If B=6: $(1,2), (2,1), (3,2), (2,3), (1,4), (2,3)$? No, distinct.
             
             Pattern for B=2m:
             Points:
             $(1, 2), (2, 1), (3, 2), (2, 3), (1, 4), (2, 3)$? No.
             
             Let's use a "spiral" or "rectangle".
             Rectangle $(1,1)$ to $(m, m)$?
             
             Actually, if we have R>0, we can just output a solution that mixes them.
             If R>=2, we can create a "backbone" of 2 Reds and attach Blues.
             
             Let's try this for any R>=2, B>=0:
             Place Reds at $(1,1)$ and $(1,2)$.
             We need to connect them in a cycle with B Blues.
             
             Case 1: B=0.
             Cycle of R Reds.
             If R=2: $(1,1), (1,2)$.
             If R=4: $(1,1), (1,2), (2,2), (2,1)$.
             If R>2 even:
             We can extend the rectangle.
             $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$ is 4.
             For R=6: Add $(1,3), (2,3)$?
             $(1,1)-(1,2)-(2,2)-(2,3)-(1,3)-(1,2)$? No, distinct.
             
             Standard cycle for 2k Reds:
             $(1,1) \to (1,2) \to (2,2) \to (2,1) \to (1,1)$ is 4.
             For 6: $(1,1) \to (1,2) \to (1,3) \to (2,3) \to (2,2) \to (2,1) \to (1,1)$.
             This works for any even R>=2.
             Coordinates:
             Top row: $(1,1) \dots (1, R/2)$
             Right col: $(2, R/2)$
             Bottom row: $(2, R/2-1) \dots (2,1)$
             Left col: $(1,1)$ closes.
             
             Case 2: B>0.
             We can insert Blues into the Red cycle.
             Each Blue inserted must be adjacent to its neighbors.
             Since Blue moves diagonally, and Red moves orthogonally:
             If we have $R \to B \to R$:
             $R(r,c) \to B(r',c') \to R(r'',c'')$.
             $R \to B$: Orthogonal move. So $B$ is at $(r\pm 1, c)$ or $(r, c\pm 1)$.
             $B \to R$: Diagonal move. So $R$ is at $(r'\pm 1, c'\pm 1)$.
             
             Example: $R(1,1) \to B(1,2) \to R(2,1)$?
             $R(1,1) \to B(1,2)$: Right. OK.
             $B(1,2) \to R(2,1)$: Diag $(+1, -1)$. OK.
             $R(2,1)$ is part of the cycle.
             
             So we can replace an edge $R_i \to R_{i+1}$ with $R_i \to B \to R_{i+1}$?
             Only if $R_{i+1}$ is diagonally reachable from the intermediate Blue.
             And Blue is orthogonally reachable from $R_i$.
             
             If we have a Red cycle, we can insert Blues between any two adjacent Reds, provided we can find a square for Blue.
             Since the board is huge, we can always find space.
             
             Algorithm:
             1. Generate a base cycle of R Reds.
             2. If B=0, done.
             3. If B>0, we need to insert B Blues into the cycle.
                We can insert them one by one or in groups.
                Inserting one Blue between $R_i$ and $R_{i+1}$:
                Find a square $S$ such that $R_i \to S$ (orth) and $S \to R_{i+1}$ (diag).
                Then the sequence becomes $R_i, B, R_{i+1}$.
                This consumes 1 Blue.
                We can do this B times.
                However, we must ensure distinct squares.
                Since the board is $10^9$, we can use "unused" squares near the base cycle.
                
             Implementation:
             - Generate R Reds in a compact rectangle (e.g., $2 \times R/2$).
             - For each of the B Blues, pick an edge in the current cycle and insert a Blue.
             - To avoid collision, use a "layer" outside the rectangle.
             
             Let's refine the insertion:
             Base cycle for R Reds (R even, R>=2):
             If R=2: $(1,1) \to (1,2) \to (1,1)$.
             If R>=4:
             $R_1=(1,1), R_2=(1,2), \dots, R_{R/2}=(1, R/2)$.
             $R_{R/2+1}=(2, R/2), \dots, R_R=(2,1)$.
             Edges:
             Horizontal on row 1: $(1,k) \to (1,k+1)$.
             Vertical at end: $(1, R/2) \to (2, R/2)$.
             Horizontal on row 2: $(2,k) \to (2,k-1)$.
             Vertical at start: $(2,1) \to (1,1)$.
             
             We can insert Blues on any edge.
             For an edge $U \to V$:
             We want $U \to B \to V$.
             $U=(r_u, c_u), V=(r_v, c_v)$.
             Condition: $B$ is orth-adj to $U$ and diag-adj to $V$.
             
             Example: Edge $(1,1) \to (1,2)$.
             $U=(1,1), V=(1,2)$.
             Try $B=(2,2)$.
             $U \to B$: $(1,1) \to (2,2)$? No, Red moves orth.
             Try $B=(1,0)$? Out of bounds.
             Try $B=(2,1)$.
             $U(1,1) \to B(2,1)$: Orth (Down). OK.
             $B(2,1) \to V(1,2)$: Diag (Up-Right). OK.
             So we can insert B at $(2,1)$ between $(1,1)$ and $(1,2)$.
             But $(2,1)$ might be used by another Red.
             
             To avoid collision, we can use squares with larger coordinates.
             Since we have $10^9$, we can use a "buffer" zone.
             
             Plan:
             1. Construct R Reds in a $2 \times K$ block.
             2. For each Blue, assign it to a unique "slot" outside the block.
             3. We can insert Blues into the cycle by breaking an edge and adding $U \to B \to V$.
             
             Since we can insert multiple Blues into one edge?
             $U \to B_1 \to B_2 \to V$?
             $U \to B_1$ (Orth). $B_1 \to B_2$ (Diag). $B_2 \to V$ (Diag).
             This requires $B_1, B_2$ to be valid.
             
             Simpler: Insert 1 Blue per edge, using distinct external squares.
             If B > R, we need to insert multiple Blues into some edges.
             Chain of Blues: $U \to B_1 \to B_2 \dots \to B_k \to V$.
             $U \to B_1$ (Orth).
             $B_i \to B_{i+1}$ (Diag).
             $B_k \to V$ (Diag).
             
             We can generate a chain of Blues starting from a neighbor of U.
             
             Let's code this.