We need to arrange R red (orthogonal moves) and B blue (diagonal moves) pieces on a huge board so that each consecutive piece (including last→first) is a single move apart. This is essentially constructing a Hamiltonian cycle in the graph where red nodes connect orthogonally and blue nodes connect diagonally, but we can freely choose positions. The key insight: we can place pieces on a small pattern that forms a closed loop respecting piece colors.

Observation: A red piece can only be adjacent to a red piece orthogonally, and a blue piece can only be adjacent to a blue piece diagonally. So consecutive pieces in the cycle must have the same color. Hence the cycle must consist of a contiguous block of reds followed by a contiguous block of blues (or vice versa), with the transition between colors requiring a move that changes color — but that's impossible because red moves orthogonally and blue moves diagonally, and a red square is never diagonally adjacent to a blue square (they differ in both coordinates by 1, which is a diagonal move, but red cannot move diagonally). Wait: red moves orthogonally (change one coordinate by ±1). Blue moves diagonally (change both coordinates by ±1). So a red piece at (r,c) can reach (r±1,c) or (r,c±1). A blue piece at (r,c) can reach (r±1,c±1). For a red piece to be adjacent to a blue piece in one move, we need a square that is both orthogonally adjacent to the red piece and diagonally adjacent to the blue piece. That means the blue piece must be at (r±1,c±1) relative to the red piece. But then the red piece would need to move diagonally to reach the blue piece — impossible. So red and blue pieces cannot be adjacent in the cycle! Therefore the cycle must be monochromatic: all reds or all blues.

But we have both R and B pieces. If both R>0 and B>0, we need a cycle that includes both colors. Since adjacent pieces must be same color, the only possibility is that the cycle has length 1 (impossible since R+B≥2) or that we alternate colors but that's impossible. Wait — re-read: "the i-th piece placed can move in one move to the square containing the (i+1)-th piece placed." So piece i moves to piece i+1's square. Piece i is red or blue. If piece i is red, it moves orthogonally. So piece i+1 must be on an orthogonally adjacent square. If piece i+1 is blue, it must be on a square diagonally adjacent to piece i's square? No: piece i+1 is just placed on some square; piece i moves to that square. So piece i+1's square must be orthogonally adjacent to piece i's square. Similarly, piece i+1 (if blue) moves diagonally to piece i+2's square. So piece i+2's square must be diagonally adjacent to piece i+1's square.

So the adjacency constraints are: red→next: orthogonal; blue→next: diagonal. The pieces themselves have fixed colors. So if piece i is red and piece i+1 is blue, then piece i+1 is on an orthogonally adjacent square to piece i. Then piece i+1 (blue) moves diagonally to piece i+2. So piece i+2 is diagonally adjacent to piece i+1. This is possible! The colors don't have to match for adjacency; the move type is determined by the moving piece's color, not the target's color.

So we can have red→blue→red→blue... as long as the geometric constraints work. Let's analyze: red at (r,c) moves to (r±1,c) or (r,c±1). Suppose it moves to (r+1,c), and that's where a blue piece is. Then blue at (r+1,c) moves diagonally to (r+2,c+1), (r+2,c-1), (r,c+1), or (r,c-1). So the next piece (say red) is at one of those. This is feasible.

So the cycle alternates move types based on the color of the piece making the move. The sequence of pieces has colors p_1, p_2, ..., p_n. The move from i to i+1 is orthogonal if p_i=R, diagonal if p_i=B.

We need to find positions for all pieces such that:
- For each i, pos_{i+1} is orthogonally adjacent to pos_i if p_i=R, diagonally adjacent if p_i=B.
- All positions distinct.
- Positions within [1, 10^9].

This is a known problem from AtCoder ARC 155 D or similar. Let me think of a construction.

Key idea: We can build a "snake" that uses a small bounding box. The board is huge, so we can use coordinates up to 10^9.

Standard solution approach:
- If R=0 or B=0: all pieces same color. We can make a simple cycle.
  - All red: place them in a 2×k rectangle forming a cycle. For R≥2, we can do a cycle on a 2×R grid: (1,1),(1,2),...,(1,R),(2,R),(2,R-1),...,(2,1). Each consecutive pair is orthogonally adjacent, and last to first: (2,1) to (1,1) is orthogonal. Works for R≥2. For R=1, B≥1: impossible because we need a cycle of length ≥2 and only one red, but blue pieces need to be placed too. Actually if R=1, B≥1, we need to place 1 red and B blues. The red piece must be adjacent (orthogonally) to the next piece, and the last piece must be adjacent to the red piece. Since only one red, the cycle has one red and B blues. The red piece has two blue neighbors in the cycle (prev and next). Both must be orthogonally adjacent to the red. So two blue pieces must be on squares orthogonally adjacent to the red. But blue pieces move diagonally, so the pieces adjacent to red in the cycle are placed on orthogonally adjacent squares. That's fine. But then those blue pieces must connect to other blue pieces via diagonal moves. This might be possible. Let's not special-case too early.

Actually, the known result: It's possible iff (R,B) ≠ (1,1) and not (R=0 and B=1) etc. Wait, sample: R=1,B=1 → No. R=4,B=0 → Yes. R=2,B=3 → Yes.

Let me recall: This is AtCoder ARC 155 D? No, it's "Pieces on Board" or similar. Actually it's from a recent contest. The condition for impossibility is when one of R,B is 0 and the other is 1? No, R=4,B=0 works. R=1,B=0: total 1 piece, but constraint says R+B≥2. So R=1,B=0 is invalid input. R=0,B=1 invalid. R=0,B=2: two blues, can they form a cycle? Blue moves diagonally. Two blues: need pos1 diagonally adjacent to pos2, and pos2 diagonally adjacent to pos1. That's symmetric. So place at (1,1) and (2,2). Then blue at (1,1) moves to (2,2) (diagonal), blue at (2,2) moves to (1,1) (diagonal). Works! So R=0,B=2 is possible.

R=1,B=1: one red, one blue. Red moves orthogonally to blue, blue moves diagonally to red. So red at (r,c), blue at (r±1,c) or (r,c±1). Then blue must move diagonally to red: blue at (r+1,c) moves to (r,c+1),(r,c-1),(r+2,c+1),(r+2,c-1). For this to equal (r,c), we need (r+1±1, c±1) = (r,c). So r+1+1=r → 2=0 impossible, or r+1-1=r → c±1=c → ±1=0 impossible. So no solution. Hence (1,1) is impossible.

What about R=1,B=2? Red, blue, blue. Sequence: R,B,B. Moves: R→B (orthogonal), B→B (diagonal), B→R (diagonal). So red at (r,c). Blue1 at (r+1,c) (say). Blue2 at (r+2,c+1) (diagonal from blue1). Then blue2 must move diagonally to red: (r+2±1, c+1±1) = (r,c). So r+2+1=r → 3=0 no; r+2-1=r → c+1±1=c → c+2=c or c=c no. So impossible? Let's check other choices. Red at (r,c). Blue1 at (r,c+1). Blue2 at (r+1,c+2) (diagonal). Then blue2 to red: (r+1±1, c+2±1) = (r,c). r+1+1=r no; r+1-1=r → c+2±1=c → c+3=c or c+1=c no. So impossible. What if blue1 is at (r+1,c), blue2 at (r,c+1) (diagonal from blue1: (r+1-1,c+1)=(r,c+1)). Then blue2 to red: (r±1,c+1±1)=(r,c). r+1=r no; r-1=r no; c+1+1=c no; c+1-1=c → r±1=r no. So impossible. Thus R=1,B=2 impossible? But wait, maybe different sequence order? The sequence is fixed by the colors we have: we have one R and two B. The cycle must include all pieces. The order could be R,B,B or B,R,B or B,B,R. Let's try B,B,R. Moves: B→B (diag), B→R (diag), R→B (orth). Blue1 at (r,c), blue2 at (r+1,c+1) (diag). Red at (r+2,c+2) or (r,c+2) or (r+2,c) or (r,c) (diag from blue2). Then red moves orthogonally to blue1: red at (r+2,c+2) moves to (r+1,c+2),(r+3,c+2),(r+2,c+1),(r+2,c+3). None is (r,c). Red at (r,c+2) moves to (r-1,c+2),(r+1,c+2),(r,c+1),(r,c+3). None is (r,c). Red at (r+2,c) moves to (r+1,c),(r+3,c),(r+2,c-1),(r+2,c+1). None is (r,c). Red at (r,c) is same as blue1, not allowed. So impossible. Thus R=1,B=2 impossible.

What about R=2,B=1? By symmetry, also impossible? Let's check: R,R,B. Moves: R→R (orth), R→B (orth), B→R (diag). Red1 at (1,1), red2 at (1,2) (orth). Blue at (1,3) or (2,2) or (0,2) or (1,1) [taken]. Try blue at (2,2) (orth from red2). Then blue moves diag to red1: (2±1,2±1) = (1,1) → (1,1) or (1,3) or (3,1) or (3,3). (1,1) is red1! So blue at (2,2) moves to (1,1). Works! So R=2,B=1 is possible. Sequence: R at (1,1), R at (1,2), B at (2,2). Moves: (1,1)→(1,2) orth, (1,2)→(2,2) orth, (2,2)→(1,1) diag. Yes! So R=2,B=1 works.

So the impossibility condition is not just (1,1). Let's think more systematically.

This is a known problem: AtCoder Beginner Contest 295 G? No. Actually it's "Pieces" from some contest. Let me search my memory: It's AtCoder Regular Contest 155 D? No. Wait, I recall a problem: "Red and Blue Pieces" on a grid, need to form a cycle. The answer is "No" iff (R,B) = (1,1) or (R,B) = (1,2) or (2,1)? Let's test R=1,B=3. Sequence R,B,B,B. Moves: R→B (orth), B→B (diag), B→B (diag), B→R (diag). Red at (r,c). Blue1 at (r+1,c). Blue2 at (r+2,c+1). Blue3 at (r+3,c+2) or (r+1,c+2) or (r+3,c) or (r+1,c). Then blue3 to red: (r+3±1, c+2±1) = (r,c). r+3+1=r no; r+3-1=r → c+2±1=c → c+3=c or c+1=c no. Other positions: (r+1,c+2): r+1±1=r → r+2=r or r=r no. (r+3,c): r+3±1=r no. (r+1,c): r+1±1=r → r+2=r or r=r no. So impossible? What if we start differently? Red at (r,c), blue1 at (r,c+1). Blue2 at (r+1,c+2). Blue3 at (r+2,c+3) or (r,c+3) or (r+2,c+1) or (r,c+1) [taken]. Blue3 to red: (r+2±1,c+3±1)=(r,c). r+2+1=r no; r+2-1=r → c+3±1=c → c+4=c or c+2=c no. (r,c+3): r±1=r no. (r+2,c+1): r+2±1=r no. So impossible. Thus R=1,B=3 impossible.

It seems if min(R,B)=1 and the other is ≥2, it's impossible? But R=2,B=1 worked. So the condition is: if one color has exactly 1 piece, then the other must be exactly 1? No, R=2,B=1 works. So maybe: if R=1, then B must be 0 or 1? But B=0 invalid (total<2). B=1 impossible. B=2 impossible. B=3 impossible. So R=1 always impossible? But wait, what if R=1,B=0? Invalid. So R=1 always impossible? Let's check R=1,B=4. Probably impossible. So if R=1, no solution. Similarly if B=1, no solution? But R=2,B=1 worked! Wait, B=1 means one blue piece. R=2,B=1 we found a solution. So B=1 is possible if R≥2. Similarly R=1 is impossible even with B≥2? Let's verify R=1,B=2 again carefully. We tried all configurations and found none. So R=1 is impossible for any B≥1. B=1 is possible for R≥2.

What about R=0? Then all blue. B≥2. We can make a cycle of blues: place at (1,1),(2,2),(3,3),...,(B,B). Then (i,i) to (i+1,i+1) is diagonal. Last (B,B) to (1,1): need diagonal. (B,B) to (1,1) requires |B-1|=1 and |B-1|=1, so B=2. For B>2, (B,B) to (1,1) is not a single diagonal move. So we need a different cycle for B≥3 blues.

For all blue, we need a cycle where each step is diagonal. This is a cycle on the diagonal grid. We can use a "staircase" that loops back. For example, for B=4: (1,1),(2,2),(3,3),(4,4) doesn't close. We can do (1,1),(2,2),(3,3),(3,4) then (3,4) to (1,1)? No. Better: use a 2×k rectangle but with diagonal moves. Actually, we can place blues on a cycle that goes around a rectangle using diagonals. For example, a cycle of length 4: (1,1),(2,2),(2,1),(1,2). Check: (1,1)→(2,2) diag, (2,2)→(2,1)? Not diag (diff (0,-1)). So no.

For all blue, we can use a "zigzag" that returns. Consider placing them on a line with slope 1, but to close the loop we need to turn around. We can use a "snake" that goes diagonally up-right, then down-left, etc. For B=2k, we can do: (1,1),(2,2),...,(k,k),(k+1,k+1),(k,k+1),(k-1,k+1),...,(1,k+1),(1,k). Check moves: (i,i)→(i+1,i+1) diag. (k+1,k+1)→(k,k+1) diag. (i,k+1)→(i-1,k+1) diag. (1,k+1)→(1,k) diag. (1,k)→(1,1)? Not diag (diff (0,1-k)). So need to close.

Actually, for all blue, we can use a cycle that goes around a 2×2 square: (1,1),(2,2),(1,2),(2,1). Check: (1,1)→(2,2) diag, (2,2)→(1,2)? Diff (-1,0) not diag. (2,2)→(2,1) diff (0,-1) not diag. So no.

Wait, diagonal moves change both coordinates by ±1. So the parity of r+c changes by 0 or ±2? Actually (r+1,c+1): sum increases by 2. (r+1,c-1): sum unchanged. (r-1,c+1): sum unchanged. (r-1,c-1): sum decreases by 2. So the parity of r+c is invariant under diagonal moves! Because change is ±2 or 0. So all blue pieces in a connected component must have the same parity of r+c. For a cycle, all pieces must have the same parity. So we can only connect blues of same parity.

Similarly, red moves change r+c by ±1, so parity flips each move. So in a cycle of reds, parity must be consistent? Actually red moves change sum by ±1, so parity alternates. For a cycle of even length, parity is consistent (start and end same parity). For odd length, impossible. So all-red cycle requires even number of reds. R=4 works (sample). R=2 works. R=3? Three reds: need cycle of length 3 with orthogonal moves. Is that possible? Three squares mutually orthogonally adjacent in a cycle? (1,1),(1,2),(2,2). (1,1)→(1,2) orth, (1,2)→(2,2) orth, (2,2)→(1,1)? Not orth (diff (-1,-1)). So no. (1,1),(1,2),(2,1): (2,1)→(1,1) orth, (1,1)→(1,2) orth, (1,2)→(2,1) diff (1,-1) not orth. So no 3-cycle with orthogonal moves. In fact, orthogonal moves form a grid graph, which is bipartite. Any cycle must be even length. So R must be even for all-red cycle. Similarly, all-blue cycle: diagonal moves preserve parity of r+c, so the graph is disconnected into two components (even sum, odd sum). Each component is a grid graph rotated 45 degrees, which is also bipartite? Let's check: diagonal moves change r by ±1 and c by ±1. Consider the difference r-c. (r+1,c+1): r-c unchanged. (r+1,c-1): r-c increases by 2. (r-1,c+1): r-c decreases by 2. (r-1,c-1): r-c unchanged. So r-c changes by 0 or ±2, parity of r-c is invariant. So the diagonal graph has two components based on parity of r-c. Within a component, moves change r-c by ±2, so parity of (r-c)/2? Actually, if we fix parity of r+c and parity of r-c, then r and c are determined mod 2. The diagonal moves within same parity of r+c and same parity of r-c: (r+1,c+1) changes both r+c and r-c by 2, so parity unchanged. (r+1,c-1) changes r+c by 0, r-c by 2, parity unchanged. So the graph is connected and is isomorphic to a grid graph (by rotating 45 degrees). So it's bipartite. Thus all-blue cycle requires even number of blues.

So if R=0, B must be even. If B=0, R must be even.

Now mixed colors. Let's analyze the general case.

We have a sequence of moves. Each move is either orthogonal (if moving piece is red) or diagonal (if moving piece is blue). Let's denote the sequence of move types: O for orthogonal, D for diagonal. The sequence is determined by the colors of the pieces: if piece i is R, move i is O; if B, move i is D.

We need to place pieces on the grid such that the walk is a cycle.

This is equivalent to: can we find a cycle in the grid where edges are labeled O or D according to the color of the starting vertex, and the vertices are colored R/B according to the input counts.

We can think of it as: we need to assign coordinates to each piece such that the displacement from i to i+1 is (±1,0) or (0,±1) if p_i=R, and (±1,±1) if p_i=B.

Sum of all displacements around the cycle must be (0,0).

Let's denote the displacement vectors. For red moves: (±1,0) or (0,±1). For blue moves: (±1,±1).

We can choose signs freely. The sum of all x-displacements must be 0, and sum of y-displacements must be 0.

This is a system of equations. We need to find integer solutions with each displacement being one of the allowed vectors, and all positions distinct and within bounds.

Since the board is huge (10^9), we can always shift the whole configuration to fit. The only constraints are relative positions.

So the problem reduces to: given a sequence of R and B of length n=R+B, can we assign to each R a vector in {(1,0),(-1,0),(0,1),(0,-1)} and to each B a vector in {(1,1),(1,-1),(-1,1),(-1,-1)} such that the sum is (0,0), and the walk doesn't self-intersect (all positions distinct)? Self-intersection is the tricky part.

But maybe we can always avoid self-intersection by making the walk spiral or something, as long as the sum condition holds and we have enough space.

Actually, the known solution for this problem (I recall it's from AtCoder ARC 155 or similar) is:

- If R=0 and B is odd: No.
- If B=0 and R is odd: No.
- If R=1 or B=1: special cases.
- Otherwise: Yes.

Wait, sample: R=1,B=1 → No. R=4,B=0 → Yes (4 is even). R=2,B=3 → Yes.

Let's check R=1,B=2: we suspect No. R=1,B=3: No. R=1,B=4: maybe Yes? Let's test R=1,B=4. Sequence: R,B,B,B,B. Moves: O,D,D,D,D. Sum of displacements: O + 4D = 0. O is (±1,0) or (0,±1). D is (±1,±1). Sum of four D's: each changes both coordinates by ±1. The sum of four D's has x-sum even, y-sum even. O has one coordinate ±1, other 0. So total x-sum and y-sum have different parity? Let's see: sum of four D's: x-sum is sum of four ±1's, so even. y-sum is sum of four ±1's, so even. O adds ±1 to one coordinate, 0 to other. So total x-sum parity = parity of O's x-component. Total y-sum parity = parity of O's y-component. Since O has one ±1 and one 0, the parities are different: one is odd, one is even. But sum must be (0,0), so both must be even. Contradiction! So R=1,B=4 is impossible.

General parity argument: Let R be number of red moves, B be number of blue moves. Each red move changes x by ±1 or 0, and y by 0 or ±1. Specifically, one coordinate changes by ±1, the other by 0. So the sum of x-changes from red moves has the same parity as the number of red moves that are horizontal (i.e., change x). Similarly for y. But each red move is either horizontal or vertical. Let R_h be number of horizontal red moves, R_v vertical. R_h + R_v = R. Sum of x-changes from reds: sum of ±1 over R_h moves, so parity = R_h mod 2. Sum of y-changes from reds: parity = R_v mod 2.

Blue moves: each changes both x and y by ±1. Sum of x-changes from blues: sum of B terms of ±1, parity = B mod 2. Similarly y-sum parity = B mod 2.

Total x-sum parity = (R_h + B) mod 2. Total y-sum parity = (R_v + B) mod 2.

For the cycle to close, both sums must be 0 (even). So:
R_h + B ≡ 0 (mod 2)
R_v + B ≡ 0 (mod 2)

Thus R_h ≡ R_v ≡ B (mod 2). Since R_h + R_v = R, we have R ≡ 2B (mod 2) → R ≡ 0 (mod 2). So R must be even! Similarly, from R_h ≡ B and R_v ≡ B, we get R_h and R_v have same parity as B.

So necessary condition: R is even. Similarly, by symmetry (swap x and y? No, blue moves are symmetric in x and y, red moves are not symmetric in the sense that horizontal and vertical are different. But we can rotate the board 45 degrees? Not exactly. Let's derive condition for B.

Wait, the above used the fact that red moves are axis-aligned. We can also consider the sum of (x+y) and (x-y). For red moves: horizontal move (1,0): x+y changes by 1, x-y changes by 1. Vertical move (0,1): x+y changes by 1, x-y changes by -1. So each red move changes x+y by ±1, and x-y by ±1. Specifically, horizontal: (+1,+1), vertical: (+1,-1) or (-1,+1) depending on direction. Actually (0,1): x+y +1, x-y -1. (0,-1): x+y -1, x-y +1. So red moves change both x+y and x-y by ±1, with the product of signs being -1? Let's check: (1,0): x+y +1, x-y +1 (product +1). (0,1): x+y +1, x-y -1 (product -1). So red moves change (x+y, x-y) by (±1, ±1) with the constraint that the two signs are either both + or opposite? Actually:
(1,0): (+,+)
(-1,0): (-,-)
(0,1): (+,-)
(0,-1): (-,+)
So the four possibilities are (+,+), (-,-), (+,-), (-,+). That's all four combinations! So red moves can achieve any combination of signs for (x+y) and (x-y). So in the (u,v) = (x+y, x-y) coordinate system, red moves are diagonal moves! And blue moves: (1,1): u changes by 2, v changes by 0. (1,-1): u changes by 0, v changes by 2. (-1,1): u changes by 0, v changes by -2. (-1,-1): u changes by -2, v changes by 0. So blue moves are axis-aligned in (u,v) coordinates!

So the problem is symmetric under 45-degree rotation: red and blue swap roles if we rotate the board by 45 degrees and scale by sqrt(2). In the rotated coordinate system, red pieces move diagonally and blue pieces move orthogonally.

Therefore, the necessary condition from the rotated system is: B must be even! Because in the original system, R must be even (from the parity argument). By symmetry, B must be even.

Wait, is that correct? Let's verify with R=2,B=1. R=2 is even, B=1 is odd. But we found a solution! So B does not need to be even. Let's re-examine.

In the rotated system, the moves are:
- Original red move (1,0): in (u,v) = (x+y, x-y), this is (1,1) — diagonal.
- Original red move (0,1): (1,-1) — diagonal.
- Original blue move (1,1): (2,0) — horizontal in (u,v).
- Original blue move (1,-1): (0,2) — vertical in (u,v).

So in (u,v) coordinates, red moves are diagonal (change both u and v by ±1), blue moves are orthogonal (change one of u,v by ±2, other by 0).

Now, the parity argument in (u,v) coordinates: For a cycle, sum of u-changes = 0, sum of v-changes = 0.
Red moves change u by ±1, v by ±1.
Blue moves change u by 0 or ±2, v by 0 or ±2.

Sum of u-changes from reds: parity = R mod 2 (since each red contributes ±1).
Sum of u-changes from blues: parity = 0 (since each blue contributes 0 or ±2, sum is even).
So total u-sum parity = R mod 2. Must be 0 → R even.
Similarly v-sum parity = R mod 2 → R even.

So R must be even. This matches our earlier conclusion. There is no condition on B from this parity argument because blue moves contribute even amounts to both u and v. So B can be odd.

Let's check R=2,B=1: R=2 even, B=1 odd. Works.
R=1,B=2: R=1 odd. Should be impossible. We found it impossible.
R=1,B=1: R=1 odd. Impossible.
R=3,B=0: R=3 odd. Impossible? Let's check: three reds, need cycle of length 3 with orthogonal moves. As argued, orthogonal graph is bipartite, no odd cycles. So impossible.
R=4,B=0: R=4 even. Possible (sample).
R=0,B=3: R=0 even. But B=3. Can we have a cycle of 3 blues with diagonal moves? Diagonal graph is bipartite (as argued), no odd cycles. So impossible. So B must be even if R=0.
R=0,B=2: B=2 even. Possible.
R=0,B=4: B=4 even. Possible.

So the condition is: R must be even. But wait, what about R=2,B=3? R=2 even, works. R=4,B=1? R=4 even, should work. Let's test R=4,B=1. Sequence: R,R,R,R,B. Moves: O,O,O,O,D. Sum of four O's and one D. O's are axis-aligned, D is diagonal. We need to find a cycle. Likely possible.

But is R even sufficient? What about R=2,B=0? R=2 even, works (2-cycle: (1,1),(1,2) with (1,2)→(1,1) orth? (1,2) to (1,1) is orth, yes. So 2-cycle works).

What about R=0,B=2? Works.

So the necessary condition seems to be: R is even. But wait, we also need to consider the case when R=0 and B is odd: impossible. When R>0 and B=0 and R odd: impossible. When R>0 and B>0: R must be even. But is that sufficient? Let's check R=2,B=1 we have a solution. R=2,B=3 sample works. R=4,B=1? Let's try to construct.

Actually, I recall the exact condition for this problem (it's AtCoder ARC 155 D? No, it's "Pieces on Board" from some contest). The answer is "No" iff:
- R is odd, or
- (R,B) = (0, odd) [which is covered by R odd? No, R=0 is even, but B odd is bad], or
- (R,B) = (1,1) [but R=1 is odd, so covered], or
- (R,B) = (1,2) or (2,1)? Wait, R=2,B=1 works. So (2,1) is possible.

Wait, we need to be careful. The parity condition R even is necessary. But is it sufficient? Let's test R=2,B=1: works. R=2,B=2: should work. R=2,B=3: works. R=2,B=4: should work.

What about R=4,B=0: works. R=4,B=2: should work.

But there might be additional constraints when one of them is 0. If R=0, B must be even (as we saw, diagonal graph is bipartite). If B=0, R must be even (orthogonal graph is bipartite). So the condition is: R is even AND (if B=0 then R is even, which is same; if R=0 then B is even). Actually, if R=0, the condition "R is even" is true (0 is even), but we also need B even. So the full condition is: R is even, and if R=0 then B is even. But if R>0, is there any condition on B? We saw R=2,B=1 works. R=2,B=3 works. R=4,B=1 should work. So no condition on B when R>0.

But wait, what about R=2,B=0? R=2 even, B=0. Works.
R=0,B=2: R=0 even, B=2 even. Works.
R=0,B=4: works.
R=0,B=1: invalid input (R+B≥2, but R+B=1? No, R+B≥2, so R=0,B=1 is invalid because total is 1. Actually constraint says 2 ≤ R+B. So R=0,B=1 is not in input. R=0,B=0 not in input. So the only cases with one color zero are R≥2,B=0 or R=0,B≥2. For these, we need the non-zero count to be even.

So the condition is:
- If R=0: B must be even.
- If B=0: R must be even.
- If R>0 and B>0: R must be even. (B can be anything?)

But wait, is there any case with R>0,B>0,R even that is impossible? Let's try to construct for R=2,B=1 (works). R=2,B=3 (works). R=2,B=5? Let's try to construct a general method.

Construction idea:
We can build a "base" cycle using the red pieces, and insert blue pieces into the cycle by "detours". Since blue moves are diagonal, we can replace a red move with a sequence of blue moves that net the same displacement but use diagonal steps.

Specifically, a red move is (1,0). We can replace it with two blue moves: (1,1) then (0,-1)? But (0,-1) is not a blue move. Blue moves are (±1,±1). So we cannot get (1,0) from blue moves directly. But we can get (2,0) from two blue moves: (1,1)+(1,-1) = (2,0). Or (0,2) from (1,1)+(-1,1). Or (0,0) from (1,1)+(-1,-1). Or (2,2) from two (1,1). Etc.

So we can "expand" a red move into a path of blue moves that starts and ends at the right places, but we need to insert blue pieces at the intermediate squares. However, the blue pieces must be placed exactly at the squares visited by the blue moves. So if we replace a red move with a sequence of blue moves, we are adding blue pieces at the intermediate squares.

But we have a fixed number of blue pieces. We need to use exactly B blue pieces. So we can design a cycle that uses some number of blue moves and some red moves, with total pieces R+B.

Alternatively, we can think of the cycle as a sequence of moves. We need to assign to each piece a move type (O or D) according to its color. The sequence of move types is fixed by the order of pieces. But we can choose the order of pieces! The problem says "place all (R+B) pieces on the board in any order". So we can choose the sequence of colors arbitrarily, as long as there are R reds and B blues.

So we can choose the order to make construction easy.

For example, we can put all reds first, then all blues, or alternate, etc.

Let's try to construct for general R even, B arbitrary (with R>0).

Case 1: R ≥ 2, B = 0. R even. Construct a cycle of reds. Use a 2×(R/2) rectangle? Actually, for R reds, we can make a cycle that goes around a 2×(R/2) grid. Place reds at:
(1,1), (1,2), ..., (1, R/2),
(2, R/2), (2, R/2 - 1), ..., (2, 1).
This is a cycle of length R. Each step is orthogonal. Last step: (2,1) to (1,1) is orthogonal. Works for any R≥2. But R must be even? Wait, this construction works for any R≥2? Let's check R=3: (1,1),(1,2),(2,2),(2,1). That's 4 pieces. For R=3, we need 3 pieces. Can we make a 3-cycle? No, orthogonal graph has no odd cycles. So R must be even. Our construction uses R pieces: if R is even, R/2 is integer. If R is odd, we can't use this. So for B=0, R must be even, and we can use this construction.

Case 2: R = 0, B even. Construct a cycle of blues. We need a cycle of length B with diagonal moves. As noted, diagonal graph is bipartite, so B must be even. Construction: Use a "staircase" that goes up-right, then down-left in a loop. For B=2k, we can do:
(1,1), (2,2), ..., (k,k),
(k+1, k+1), (k, k+1), (k-1, k+1), ..., (1, k+1),
(1, k), (2, k), ..., (k, k).
Wait, check moves:
(1,1)→(2,2) diag.
(2,2)→(3,3) diag.
...
(k,k)→(k+1,k+1) diag.
(k+1,k+1)→(k,k+1) diag.
(k,k+1)→(k-1,k+1) diag.
...
(2,k+1)→(1,k+1) diag.
(1,k+1)→(1,k) diag.
(1,k)→(2,k) diag.
(2,k)→(3,k) diag.
...
(k-1,k)→(k,k) diag.
Now last move: (k,k)→(1,1)? Not diag. So we need to close the loop. We have visited (1,1) at start and (k,k) at end. We need (k,k)→(1,1) to be diag. That requires |k-1|=1 and |k-1|=1, so k=2. So this only works for B=4 (k=2). For larger B, we need a different cycle.

Better construction for all-blue cycle: Use a "diamond" shape. For B=4: (1,2),(2,1),(2,3),(3,2). Check: (1,2)→(2,1) diag? (1,2) to (2,1): diff (1,-1) yes. (2,1)→(2,3): diff (0,2) no. So no.

Actually, we can use a cycle that goes around a rectangle using diagonals. For example, a cycle of length 4: (1,1),(2,2),(2,1),(1,2). Check: (1,1)→(2,2) diag, (2,2)→(2,1)? diff (0,-1) no. So no.

Wait, diagonal moves change both coordinates. So to traverse a rectangle, we need to alternate directions. A cycle of diagonal moves on a grid: consider the graph where vertices are grid points, edges are diagonal moves. This graph is isomorphic to the grid graph rotated 45 degrees. So a cycle in this graph corresponds to a cycle in the grid graph. The grid graph has cycles of any even length ≥4. So we can take any even cycle in the grid graph and rotate it 45 degrees to get a cycle of diagonal moves.

For example, a 2×2 square in the grid graph: (0,0)-(1,0)-(1,1)-(0,1)-(0,0). Rotated 45 degrees: map (x,y) to (x+y, x-y). The points become: (0,0)→(0,0); (1,0)→(1,1); (1,1)→(2,0); (0,1)→(1,-1). The edges become diagonal moves between these points. Check: (0,0) to (1,1) is diag. (1,1) to (2,0) is diag? (1,1) to (2,0): diff (1,-1) yes. (2,0) to (1,-1): diff (-1,-1) yes. (1,-1) to (0,0): diff (-1,1) yes. So this is a 4-cycle of diagonal moves! Coordinates: (0,0),(1,1),(2,0),(1,-1). But we need positive coordinates. Add 2 to all: (2,2),(3,3),(4,2),(3,1). Check: (2,2)→(3,3) diag, (3,3)→(4,2) diag, (4,2)→(3,1) diag, (3,1)→(2,2) diag. Works! So for B=4, we have a cycle.

For B=6, we can take a 3×2 rectangle cycle in grid graph: (0,0)-(1,0)-(2,0)-(2,1)-(1,1)-(0,1)-(0,0). Rotated: (0,0),(1,1),(2,2),(3,1),(2,0),(1,-1). Check moves: (0,0)→(1,1) diag, (1,1)→(2,2) diag, (2,2)→(3,1) diag, (3,1)→(2,0) diag, (2,0)→(1,-1) diag, (1,-1)→(0,0) diag. Works! So for any even B≥4, we can take a cycle in the grid graph of length B and rotate it.

For B=2: just (1,1) and (2,2). Works.

So for R=0, B even, we can construct.

Case 3: R>0, B>0, R even. We need to construct a cycle with both red and blue pieces.

We can use a base cycle of reds (since R≥2 and even), and "insert" blue pieces by replacing some red moves with sequences of blue moves.

Specifically, a red move (1,0) can be replaced by two blue moves: (1,1) and (0,-1)? No, (0,-1) is not blue. But we can replace a red move with a path of blue moves that has the same net displacement. For example, to get net (1,0), we can use two blue moves: (1,1) and (0,-1) — no. (1,1) and (-1,1) gives (0,2). (1,1) and (1,-1) gives (2,0). (1,1) and (-1,-1) gives (0,0). So we cannot get (1,0) from an even number of blue moves. We can get (2,0) from two blue moves. So we can replace a red move of (2,0) with two blue moves. But our red cycle might have moves of (1,0) or (0,1). We can adjust the red cycle to have moves of (2,0) or (0,2) by scaling.

Alternatively, we can build a cycle that uses both red and blue moves directly.

Let's think of a simple pattern. Consider a "staircase" that alternates red and blue moves. For example, sequence: R,B,R,B,... with moves O,D,O,D,...

Let's try to construct for R=2, B=1. We already have a solution: (1,1)R, (1,2)R, (2,2)B. Moves: (1,1)→(1,2) O, (1,2)→(2,2) O, (2,2)→(1,1) D. This works.

For R=2, B=3. Sample solution: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4). Let's check moves:
1: B at (2,3) → R at (3,2)? B moves diag: (2,3)→(3,2) is diag (1,-1). Yes.
2: R at (3,2) → B at (2,2)? R moves orth: (3,2)→(2,2) is orth (-1,0). Yes.
3: B at (2,2) → B at (3,3)? B moves diag: (2,2)→(3,3) is diag (1,1). Yes.
4: B at (3,3) → R at (2,4)? B moves diag: (3,3)→(2,4) is diag (-1,1). Yes.
5: R at (2,4) → B at (2,3)? R moves orth: (2,4)→(2,3) is orth (0,-1). Yes.
Works.

So the idea is to create a "loop" that uses a few red pieces as "corners" and blue pieces as "edges".

General construction for R even ≥2, B≥1:
We can make a cycle that looks like a "staircase" with red pieces at the turns and blue pieces along the diagonals.

Consider placing red pieces at (0,0), (0,2), (2,2), (2,0) — a square of 4 reds. But R=4. We can insert blues along the edges.

Actually, a known construction for this problem (I think it's from AtCoder ARC 155 D "Pieces on Board") is:
- If R is odd: No.
- If R=0 and B is odd: No.
- Otherwise: Yes.

And the construction is:
- If B=0: use the 2×k rectangle cycle.
- If R=0: use the rotated grid cycle.
- If R≥2 and B≥1: use a construction that places reds at (1,1), (1,3), (3,3), (3,1) ... wait, need to handle arbitrary B.

Let's try to design a general construction for R≥2 even, B≥1.

We can use a "spiral" or "snake" that starts with a red piece, then alternates blue and red, but we need exactly R reds and B blues.

One approach: Use a base cycle of reds (R pieces) that forms a large rectangle. Then replace some of the red moves with sequences of blue moves. Each replacement of a red move with k blue moves increases the number of pieces by k-1. We need to increase by B. So we need to replace some red moves with paths of blue moves such that total added pieces = B.

But we can also change the number of reds? No, R is fixed.

Alternatively, we can construct a cycle directly with the given R and B.

Let's think of a "template" that can be adjusted.

Consider a cycle that goes:
Start at (0,0) [Red]
Move right (orth) to (0,1) [Blue? No, we need to place pieces at each step. The piece at (0,1) is the next piece. Its color determines the next move.

So the sequence of pieces and moves:
Piece 1: Red at (0,0). Move: orth.
Piece 2: at (0,1). Color? If we want to insert blues, we can make piece 2 Blue. Then move is diag.
Piece 3: at (1,2) (diag from (0,1)). Color? Maybe Red.
Piece 4: at (1,3) (orth from (1,2)). Color? Blue.
...

This is getting complicated.

Let's look for a simpler pattern. Notice that in the sample for R=2,B=3, the cycle is:
B (2,3)
R (3,2)
B (2,2)
B (3,3)
R (2,4)

Coordinates:
(2,3) B
(3,2) R
(2,2) B
(3,3) B
(2,4) R

Plot:
Row 2: col 2 B, col 3 B, col 4 R
Row 3: col 2 R, col 3 B

So it's a small cluster.

Maybe we can use a "diamond" shape. For R=2, B=1: (1,1)R, (1,2)R, (2,2)B. That's a corner.

For R=2, B=3: we have two reds and three blues. The reds are at (3,2) and (2,4). They are not adjacent. The blues connect them.

Idea: Use a "path" of blues connecting two red "anchors". The reds are placed such that they can be connected by a path of blues that starts and ends at the reds with the correct moves.

Specifically, we need a cycle. We can think of it as: we have R red pieces. We can arrange them in a cycle using orth moves, but we need to insert B blue pieces into the edges. Each blue piece insertion replaces an orth edge with a path of diag edges.

An orth edge is a vector like (1,0). We can replace it with a sequence of diag vectors that sum to (1,0). But as noted, sum of diag vectors has both components even. So we cannot sum to (1,0) using diag vectors. So we cannot replace a single orth edge with a path of diag edges that has the same net displacement.

However, we can replace a pair of orth edges with a path of diag edges. For example, two orth edges: (1,0) and (0,1) sum to (1,1). We can replace this with one diag edge (1,1). That would remove one piece (the corner red) and replace with a blue. But we want to add blues, not remove reds.

Alternatively, we can replace a red piece with a "detour" using blues. For example, a red piece at a corner: instead of turning, we go straight with a blue, then turn with another blue, etc.

Let's think of the cycle as a sequence of moves. We need to assign colors to vertices such that the number of reds is R, blues is B, and the move from a vertex is orth if vertex is red, diag if vertex is blue.

We can choose the sequence of colors. Let's try to find a sequence that works for any R even ≥2 and B≥1.

Consider the sequence: R, B, B, ..., B, R, B, B, ..., B, R, ... where we have blocks of blues between reds.

Suppose we have k red pieces. We want to connect them in a cycle using blues. Between two consecutive reds, we have a path of blues. The first red moves orth to the first blue. The last blue moves diag to the next red.

So we need: for each adjacent pair of reds in the cycle, there is a path of blues from a square orthogonally adjacent to the first red to a square diagonally adjacent to the last blue? Wait, the path is: Red_i --(orth)--> Blue_1 --(diag)--> Blue_2 --(diag)--> ... --(diag)--> Blue_m --(diag)--> Red_{i+1}.

So Red_i is at some position. Blue_1 is orthogonally adjacent to Red_i. Blue_2 is diagonally adjacent to Blue_1. ... Blue_m is diagonally adjacent to Blue_{m-1}. Red_{i+1} is diagonally adjacent to Blue_m.

So the path from Red_i to Red_{i+1} consists of: one orth step, then m-1 diag steps, then one diag step? Actually, the moves are:
Red_i to Blue_1: orth.
Blue_1 to Blue_2: diag.
...
Blue_{m-1} to Blue_m: diag.
Blue_m to Red_{i+1}: diag.

So total displacement from Red_i to Red_{i+1} is: orth + (m) diag steps? Wait: there are m blues, so m diag moves between them? Let's count: Blue_1 to Blue_2 is one diag, ..., Blue_{m-1} to Blue_m is one diag. That's m-1 diag moves. Then Blue_m to Red_{i+1} is one diag move. So total diag moves = m. Plus one orth move.

So displacement = orth_vector + sum of m diag_vectors.

We need to choose the orth_vector and the m diag_vectors such that the displacement is whatever we need to connect the reds in a cycle.

If we have R reds, we can place them in a cycle using orth moves only (since R even). That cycle has R orth moves. We want to replace some of these orth moves with paths of blues. But as argued, we cannot replace a single orth move with diag moves because parity of displacement doesn't match.

However, we can replace two orth moves with a path of blues. For example, two orth moves: (1,0) and (0,1) sum to (1,1). We can replace them with one diag move (1,1). That uses one blue instead of two reds? No, the vertices are the pieces. If we have a red at corner, we remove that red and put a blue there. That changes R and B.

We need to keep R and B fixed. So we need to add blues without removing reds. That means we need to insert blues into the edges, but the edges are moves between pieces. If we insert a blue between two reds, the move from first red to blue is orth, and from blue to second red is diag. So the displacement from first red to second red is orth + diag. This is not the same as the original orth move between the two reds. So the positions of the reds must change.

So we can design a new cycle from scratch.

Let's try to construct a cycle for any R even ≥2 and B≥1.

We can use a "ladder" shape. Place reds at (0,0), (0,2), (0,4), ..., (0, 2k-2) and (2, 2k-2), (2, 2k-4), ..., (2,0). This is a cycle of R=2k reds. The moves are all orth.

Now we want to insert blues. We can "expand" each orth move into a path of blues. But we need to keep the reds in place? No, we can move the reds.

Alternatively, we can build a cycle that uses a "zigzag" of blues and reds.

Consider the following pattern for R=2, B arbitrary:
Place reds at (1,1) and (1, B+2). Place blues at (2,2), (3,3), ..., (B+1, B+1) and also at (2, B+2)? Let's try.

Sequence: R1, B1, B2, ..., B_B, R2, and then back to R1? But we need a cycle.

Let's try: R1 at (1,1). B1 at (2,2) (diag from R1? No, R1 moves orth to B1. So B1 must be orth adjacent to (1,1). Say B1 at (1,2). Then B1 moves diag to B2 at (2,3) or (2,1) or (0,3) or (0,1). Let's go (2,3). B2 at (2,3). B2 moves diag to B3 at (3,4) or (3,2) or (1,4) or (1,2). Continue: B_i at (i, i+1). Then B_B at (B, B+1). Then we need to reach R2. R2 must be diag adjacent to B_B. So R2 at (B+1, B+2) or (B-1, B+2) or (B+1, B) or (B-1, B). Let's pick R2 at (B+1, B+2). Then R2 moves orth to... we need to close the cycle back to R1. R2 at (B+1, B+2) moves orth to (B+1, B+1) or (B+2, B+2) or (B, B+2) or (B+1, B+3). We need to reach R1 at (1,1). That's far. So we need a path from R2 back to R1 using blues? But we have used all B blues. So we need to insert more blues or use a different path.

Maybe we can make a cycle that goes out and back. For R=2, B=1 we had: R(1,1), R(1,2), B(2,2). That's a triangle.

For R=2, B=3: we had a pentagon.

For R=2, B=5: maybe a heptagon.

Generalizing: For R=2, B=2k-1 (odd B), we can make a cycle with 2 reds and 2k-1 blues. The sample had B=3 (k=2). Let's try to construct for B=5.

Pattern from sample: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4).
Notice the reds are at (3,2) and (2,4). The blues form a path between them.

Maybe we can place the two reds at (0,0) and (0,2m) and blues along a path.

Let's try to design a cycle for R=2, B odd.
Place R1 at (0,0).
Place R2 at (0, 2B+2)? No.

Let's think of the cycle as a sequence of moves. We need to assign colors to the vertices. Let's try the sequence: B, R, B, B, ..., B, R.
That is: start with B, then R, then B repeated B-1 times, then R.
Total pieces: 1 + 1 + (B-1) + 1 = B+2 = R+B since R=2.
Moves: B→R (diag), R→B (orth), B→B (diag), ..., B→R (diag).
So the cycle is: B1 --diag--> R1 --orth--> B2 --diag--> B3 --diag--> ... --diag--> B_B --diag--> R2 --?--> B1.
The last move is from R2 to B1. R2 is red, so move is orth. So R2 must be orth adjacent to B1.

Let's set coordinates:
Let B1 be at (0,0).
R1 is diag adjacent to B1. Choose R1 at (1,1).
R1 moves orth to B2. Choose B2 at (1,0) (left) or (1,2) (right) or (0,1) (down) or (2,1) (up). Let's pick B2 at (1,0).
B2 moves diag to B3. B3 at (2,1) or (2,-1) or (0,1) or (0,-1). Let's pick B3 at (2,1).
B3 moves diag to B4. B4 at (3,2) or (3,0) or (1,2) or (1,0). Pick (3,2).
Continue: B_i at (i, i-1) for i≥2? Let's check:
B2: (1,0) = (2,1)? No, i=2: (2,1). But we said B2 at (1,0). Let's define:
B1: (0,0)
R1: (1,1)
B2: (1,0) (orth from R1: (1,1)→(1,0) is left)
B3: (2,1) (diag from B2: (1,0)→(2,1) is (1,1))
B4: (3,2) (diag from B3: (2,1)→(3,2) is (1,1))
...
B_k: (k-1, k-2) for k≥2? Let's check: B2: (1,0) = (2-1, 2-2) = (1,0). Yes.
B3: (2,1) = (3-1, 3-2) = (2,1). Yes.
So B_k = (k-1, k-2) for k=2,...,B.
Then B_B = (B-1, B-2).
Now R2 must be diag adjacent to B_B. So R2 at (B, B-1) or (B-2, B-1) or (B, B-3) or (B-2, B-3).
We also need R2 to move orth to B1 at (0,0). So R2 must be orth adjacent to (0,0). That means R2 is at (1,0), (-1,0), (0,1), or (0,-1). But B2 is at (1,0). So R2 cannot be at (1,0). It could be at (0,1) or (0,-1) or (-1,0). But R2 is at (B, B-1) or similar. For B≥2, (B, B-1) is far from (0,0). So this doesn't work.

We need R2 to be close to B1. So maybe we should not go far away. Let's try a different path.

We want a cycle. Let's try to make a "loop" that stays in a small area.

For R=2, B=1: (1,1)R, (1,2)R, (2,2)B. This is a 3-cycle.
For R=2, B=3: (2,3)B, (3,2)R, (2,2)B, (3,3)B, (2,4)R. This is a 5-cycle.
Notice that in both cases, the two reds are not adjacent. They are separated by some blues.

For R=2, B=5: maybe we can extend the pattern.
Coordinates from sample:
B1: (2,3)
R1: (3,2)
B2: (2,2)
B3: (3,3)
R2: (2,4)

Let's try to add more blues. After R2 at (2,4), we need to go back to B1 at (2,3). But R2 is red, so it moves orth. (2,4) to (2,3) is orth. So we can add a blue at (2,3)? But (2,3) is already B1. So we need to insert blues between R2 and B1.

In the sample, the cycle is B1→R1→B2→B3→R2→B1.
Moves: B1→R1: diag. R1→B2: orth. B2→B3: diag. B3→R2: diag. R2→B1: orth.
So the sequence of moves: D, O, D, D, O.
The displacements: D: (1,-1) from (2,3) to (3,2). O: (-1,0) from (3,2) to (2,2). D: (1,1) from (2,2) to (3,3). D: (-1,1) from (3,3) to (2,4). O: (0,-1) from (2,4) to (2,3).
Sum: (1-1+1-1+0, -1+0+1+1-1) = (0,0). Good.

Now for B=5, we need to insert two more blues. We can insert them in the path from B2 to B3 or from B3 to R2, etc. But we need to maintain the cycle.

Maybe we can make a general construction for R=2, B odd:
Place the two reds at (0,1) and (0, -1)? No.

Let's think of a "diamond" shape. For R=2, B=1: triangle.
For R=2, B=3: pentagon.
For R=2, B=5: heptagon.
In general, a (2+B)-gon? But B can be even or odd? We saw R=2,B=1 works, R=2,B=3 works. What about R=2,B=2? Should work. R=2,B=4? Should work.

Let's try to construct for R=2, B=2.
We need 4 pieces: 2 reds, 2 blues.
Sequence: R,B,B,R or R,R,B,B or B,R,R,B or B,B,R,R or R,B,R,B.
Try R,B,R,B:
R1 at (0,0). B1 at (1,0) (orth). R2 at (2,1) (diag from B1). B2 at (2,2) (orth from R2). Then B2 must move diag to R1: (2,2)→(1,1) or (3,1) or (1,3) or (3,3). (1,1) is not (0,0). So no.
Try R,B,B,R:
R1 at (0,0). B1 at (1,0) (orth). B2 at (2,1) (diag). R2 at (3,2) (diag). Then R2 moves orth to R1: (3,2)→(0,0)? Not orth.
Try B,R,R,B:
B1 at (0,0). R1 at (1,1) (diag). R2 at (1,2) (orth). B2 at (2,3) (diag). Then B2 moves diag to B1: (2,3)→(1,2) or (3,2) or (1,4) or (3,4). None is (0,0).
Try B,R,B,R:
B1 at (0,0). R1 at (1,1) (diag). B2 at (1,2) (orth). R2 at (2,3) (diag). Then R2 moves orth to B1: (2,3)→(0,0)? No.
Try R,R,B,B:
R1 at (0,0). R2 at (1,0) (orth). B1 at (2,1) (diag). B2 at (3,2) (diag). Then B2 moves diag to R1: (3,2)→(2,1) or (4,1) or (2,3) or (4,3). None is (0,0).
Try B,B,R,R:
B1 at (0,0). B2 at (1,1) (diag). R1 at (1,2) (diag). R2 at (0,2) (orth). Then R2 moves orth to B1: (0,2)→(0,0) is orth! Yes!
So: B1(0,0), B2(1,1), R1(1,2), R2(0,2).
Check moves:
B1→B2: (0,0)→(1,1) diag.
B2→R1: (1,1)→(1,2) orth.
R1→R2: (1,2)→(0,2) orth.
R2→B1: (0,2)→(0,0) orth.
Wait, R2 is red, so move is orth. (0,2) to (0,0) is orth. Yes!
So R=2,B=2 works with sequence B,B,R,R.
Coordinates: B(0,0), B(1,1), R(1,2), R(0,2).
This is a 4-cycle: a square.

Great! So for R=2, B=2 we have a solution.

Now for R=2, B=4? Sequence B,B,B,B,R,R? Let's try to extend.
We have B1(0,0), B2(1,1), B3(2,2), B4(3,3), R1(3,4), R2(0,4)? Then R2→B1: (0,4)→(0,0) orth. But we need to connect B4 to R1: B4→R1 diag: (3,3)→(3,4) is orth, not diag. So B4 must move diag to R1. So R1 should be at (4,4) or (2,4) or (4,2) or (2,2). Let's try R1 at (4,4). Then R1→R2 orth. R2 must be orth adjacent to R1 and also orth adjacent to B1? No, R2 moves orth to B1. So R2