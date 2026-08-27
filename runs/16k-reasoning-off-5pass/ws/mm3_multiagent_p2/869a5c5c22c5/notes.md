
## ideation
The problem asks whether we can place R red and B blue pieces on a large board such that they form a closed loop where each piece can move to the next in one step (orthogonal for red, diagonal for blue), and the last can move to the first.

Key observations:
1. The board is huge (10^9 x 10^9), so we only need to ensure a valid relative configuration exists.
2. A cycle in the original coordinates corresponds to a cycle in (u,v) = (x+y, x-y) coordinates where red moves become diagonal and blue moves become orthogonal.
3. In the original coordinates, red moves are orthogonal. The sum of x-changes and y-changes from red moves must have the same parity as the number of red moves. Since each red move changes one coordinate by ±1, the total x-change parity = number of horizontal red moves, y-change parity = number of vertical red moves. Blue moves change both coordinates by ±1, contributing parity B to both. For the cycle to close, both sums must be even, so R must be even.
4. If R=0, we have only blue pieces. Diagonal moves preserve the parity of x+y, and the diagonal graph is bipartite, so B must be even.
5. If R>0 and B>0, R must be even. B can be any value (including 0? No, B>0 here). The conditions are:
   - R must be even.
   - If R=0, then B must be even.
   - If B=0, then R must be even.
   - All other cases are possible.

Construction strategies:
- B=0, R even: Use a 2×(R/2) rectangle cycle.
- R=0, B even: Use a rotated grid cycle (e.g., a cycle in the integer lattice rotated 45°).
- R≥2 even, B≥1: Place reds at the four corners of a rectangle, and fill the edges with blues. More systematically, we can use a "spiral" or a "ladder" construction.

A known clean construction for R≥2, B≥1:
Place reds at (1,1), (1,3), (3,3), (3,1) for a base of 4 reds. For additional reds, extend the rectangle. For blues, we can insert them along the edges by replacing a red move with a path of blue moves. Specifically, we can create a cycle that goes around a 2×k rectangle but with the horizontal moves replaced by "staircases" of blue moves.

Simpler general construction for R even ≥2, B≥1:
- Place reds at (0,0), (0,2), (0,4), ..., (0, R-2) and (2, R-2), (2, R-4), ..., (2,0). This is a cycle of R reds.
- Now we need to insert B blues. We can "expand" each vertical move into a zigzag of blues. For example, replace the move from (0,0) to (0,2) (which is two vertical orth moves: (0,0)→(1,0)→(0,2)? No, we need to add blues, not change reds.

Actually, a robust construction:
- If B=0 and R even: use 2×(R/2) rectangle.
- If R=0 and B even: use a cycle in the diagonal grid (e.g., a diamond).
- If R≥2 and B≥1: we can always build a cycle using a "snake" that alternates red and blue pieces. A simple explicit construction: place reds at (1,1), (1,2), (2,2), (2,1) for R=4. For larger R, extend the rectangle. For blues, place them along the diagonal between two reds. More generally, we can use a "path" that goes back and forth.

After research and recalling similar problems (AtCoder ARC 155 D "Pieces on Board"), the exact conditions are:
- Impossible iff:
  1. R is odd, or
  2. R=0 and B is odd, or
  3. (R,B) = (1,1) [but this is covered by R odd], or
  4. (R,B) = (1,2) or (2,1)? Wait, we found (2,1) works. So only (1,1) and (1,2) are impossible among small cases? Actually (1,2) is R=1 odd, so covered. So the condition is simply: R must be even, and if R=0 then B must be even. (Since R=0 is even, we need B even separately). So the only impossible cases are:
  - R is odd
  - R=0 and B is odd
  - B=0 and R is odd (same as first)
So condition: R is even AND (R>0 OR B is even).

But wait, what about (R,B) = (2,0)? R=2 even, works. (0,2) works. (0,1) invalid input. (1,0) invalid.

So the answer is "No" iff R is odd OR (R=0 and B is odd). Since B=0 and R odd is already covered, and R+B≥2, the only impossible cases are when R is odd, or when R=0 and B is odd.

Construction for Yes:
We can provide a general construction that works for all allowed cases.

General construction:
Let k = R/2.
If B=0:
  Place reds at (1,1), (1,2), ..., (1,k), (2,k), (2,k-1), ..., (2,1). This forms a cycle of R reds.
If R=0 (and B even):
  Let m = B/2.
  Place blues at (1,1), (2,2), ..., (m,m), (m+1,m), (m,m-1), ..., (1,0)? No, that doesn't close. Better: use a rotated rectangle. For B=2: (1,1),(2,2). For B=4: (1,1),(2,2),(3,1),(2,0) rotated? Actually, we can use the following: place blues at (1,1), (2,2), (3,3), (4,2), (3,1) for B=5? But B must be even. For B=6: (1,1),(2,2),(3,3),(4,4),(4,3),(3,2),(2,3),(1,2)? Not a cycle.
  Instead, we can use a cycle in the grid graph and rotate it. For B even, we can take a 2×(B/2) rectangle cycle in the grid graph and apply the 45° rotation. The grid cycle for length B: (0,0)-(1,0)-...-(B/2-1,0)-(B/2-1,1)-...-(0,1)-(0,0). Rotated: map (x,y) to (x+y, x-y). This gives valid coordinates. We can shift to positive.
If R≥2 and B≥1:
  We can use a construction that places reds at (1,1) and (1,3) for R=2, and for R>2, we can add more reds by extending a "comb" shape. A known construction: 
  - Place reds at (1,1), (1,2), ..., (1, R/2) and (2, R/2), (2, R/2 -1), ..., (2,1). That's the B=0 case.
  - To add blues, we can "insert" them into the vertical segments. For example, replace the vertical move from (1,i) to (2,i) with a staircase of blues. A vertical orth move (0,1) can be replaced by two diag moves (1,1) and (-1,0)? No, diag moves are (1,1) etc. We can replace two orth moves (one horizontal, one vertical) with a diag move. 
  Actually, a simple construction for R=2, B arbitrary: 
    Place R1 at (1,1), R2 at (1, B+3). 
    Place blues at (2,2), (3,3), ..., (B+1, B+1) and (2, B+2)? Let's try to design a cycle.
    Sequence: R1, B1, B2, ..., B_B, R2, and back to R1.
    R1 at (1,1). B1 at (1,2) (orth). B2 at (2,3) (diag). B3 at (3,4) (diag). ... B_B at (B, B+1) (diag). R2 at (B+1, B+2) (diag). Then R2 must move orth to R1: (B+1, B+2) to (1,1)? Not orth. So we need to bring R2 closer. Instead, make a loop: R1, B1, ..., B_B, R2, and then back to R1 using another path. But we have no more blues.
  Another idea: Use a "spiral" that uses all pieces.
  Let's use the construction from the editorial (if I recall): 
  For R≥2, B≥1, we can place the pieces on a "snake" that goes:
  Start at (1,1) [R]
  Go right to (1,2) [R]
  Go down to (2,2) [B]? No.

  After some thought, a universal construction for R even ≥2, B≥1:
  Place reds at (1,1), (1,3), (1,5), ..., (1, R-1) and (3, R-1), (3, R-3), ..., (3,1). This is a cycle of R reds using a 2×(R/2) rectangle but with a gap at y=2? Actually, the moves are: (1,1)→(1,3) is orth (skip (1,2)). That's a move of length 2. But orth moves are only length 1! So we cannot skip squares. The pieces must be placed on the squares they occupy. The move is from one piece to the next. So if we have reds at (1,1) and (1,3), the move from (1,1) to (1,3) is not a single orth move. So we cannot skip squares. All intermediate squares must be occupied by pieces? No, the move is from the square containing piece i to the square containing piece i+1. They must be adjacent. So if we have a red at (1,1) and the next piece is at (1,3), the move is not allowed because distance is 2. So we must have pieces at every step.

  So the cycle must visit squares that are adjacent. This means the cycle is a simple cycle in the grid graph (for red moves) or diagonal graph (for blue moves), but with mixed move types.

  Let's design a "figure-8" or "loop" that is small.
  For R=2, B=1: (1,1)R, (1,2)R, (2,2)B. This is a 3-cycle.
  For R=4, B=1: we can add two more reds to the R=2,B=1 solution? 
    Take R=2,B=1: (1,1)R, (1,2)R, (2,2)B.
    Add two more reds: we can "extend" one of the red moves. But we have only one blue.
    Maybe: (1,1)R, (1,2)R, (1,3)R, (2,3)R, (2,2)B. Check moves:
    R(1,1)→R(1,2): orth.
    R(1,2)→R(1,3): orth.
    R(1,3)→R(2,3): orth.
    R(2,3)→B(2,2): orth.
    B(2,2)→R(1,1): diag? (2,2)→(1,1) is diag (-1,-1). Yes!
    So R=4,B=1 works with a 5-cycle: (1,1),(1,2),(1,3),(2,3),(2,2). Colors: R,R,R,R,B.
    Moves: O,O,O,O,D. Sum: 3O + 1D? Wait, 4 reds and 1 blue: moves are O,O,O,O,D. Sum of 4 O's: three horizontal? Actually (1,1)→(1,2): O, (1,2)→(1,3): O, (1,3)→(2,3): O, (2,3)→(2,2): O. So four O's: three horizontal? (1,1)→(1,2) horizontal, (1,2)→(1,3) horizontal, (1,3)→(2,3) vertical, (2,3)→(2,2) horizontal. So horizontal moves: 3, vertical: 1. Sum: (1+1-1, 0+0+1-1) = (1,0). D: (-1,-1). Total: (0,-1)? Not (0,0). Wait, let's recalc:
    (1,1) to (1,2): +1,0
    (1,2) to (1,3): +1,0
    (1,3) to (2,3): 0,+1
    (2,3) to (2,2): 0,-1
    Sum: (2,0). Then B(2,2) to R(1,1): -1,-1. Total: (1,-1) ≠ (0,0). So that doesn't close. My mistake: (2,2) to (1,1) is (-1,-1). Sum: (2-1, 0-1) = (1,-1). Not zero. So that doesn't work.

  Let's find a working R=4,B=1.
  We need sum of 4 O's and 1 D = (0,0).
  O's are (±1,0) or (0,±1). D is (±1,±1).
  We need the sum of O's to be (±1,∓1) to cancel the D.
  So we need three O's in one direction and one in the other? Actually, sum of O's must be a vector with one coordinate ±1 and the other ∓1. For example, sum O = (1,-1). That means we need horizontal moves summing to 1, vertical moves summing to -1.
  So possible: two horizontal +1 and one horizontal -1? That sums to +1. Vertical: one +1 and one -1? That sums to 0. Not -1.
  Let's try: O1: (1,0), O2: (0,1), O3: (0,-1), O4: (0,-1)? Sum: (1, -1). Then D: (-1,1). Total (0,0).
  So sequence of moves: (1,0), (0,1), (0,-1), (0,-1), (-1,1). The D is last.
  So we need to place 4 reds and 1 blue such that the moves are in that order.
  Let's place B at (0,0) [the last piece, which moves D to the first red].
  Actually, the cycle is a sequence of pieces. Let's decide the order of colors: R,R,R,R,B.
  Moves: O,O,O,O,D.
  Let's assign the D to be (-1,1). So the last move (from B to first R) is (-1,1).
  So if B is at (x,y), first R is at (x-1, y+1).
  Now we need to place three more reds and one more red? Total reds=4. So we have 4 reds. The moves between them are O,O,O,O. The sum of these four O's must be (1,-1) to cancel the D? Wait, total sum = sum(O) + D = 0. So sum(O) = -D = (1,-1).
  So the four O's must sum to (1,-1).
  Let's try: O1=(1,0), O2=(0,1), O3=(0,-1), O4=(0,-1) sums to (1,-1). Yes.
  Now, we need to arrange the four O's in a path that ends at the first R? No, the path is: R1 --O1--> R2 --O2--> R3 --O3--> R4 --O4--> B --D--> R1.
  So R1 is the start. B is at the end. B moves to R1.
  We have B at (x,y). R1 at (x-1, y+1) (since D=(-1,1) from B to R1 means B + (-1,1) = R1, so R1 = (x-1, y+1)).
  Now R4 is at B - O4? The move from R4 to B is O4=(0,-1). So B = R4 + (0,-1) => R4 = (x, y+1).
  Then R3 to R4 is O3=(0,-1). So R3 = R4 - (0,-1) = (x, y+2).
  R2 to R3 is O2=(0,1). So R2 = R3 - (0,1) = (x, y+1)? That would be same as R4. Not allowed. So O3 cannot be (0,-1) if O2 is (0,1) and they are adjacent? Wait, the moves are between consecutive pieces. R2 and R3 are adjacent. R3 and R4 are adjacent. So we need a path of four O's that is a simple path.
  Let's try a different set of O's: (1,0), (0,1), (0,1), (0,-1)? Sum: (1,1). Not (1,-1).
  (1,0), (1,0), (-1,0), (0,-1)? Sum: (1,-1). This is a path: (1,0), (1,0) goes right twice, then (-1,0) left, then (0,-1) down. This is a path that goes right, right, left, down. It doesn't self-intersect if placed properly. Let's try:
  Start R1 at (0,0).
  R1 --(1,0)--> R2 at (1,0).
  R2 --(1,0)--> R3 at (2,0).
  R3 --(-1,0)--> R4 at (1,0)? That's same as R2. Not allowed. So we need to avoid revisiting squares.
  Try: (1,0), (0,1), (-1,0), (0,-1) is a square cycle of length 4, sum (0,0). Need sum (1,-1).
  Try: (1,0), (0,1), (0,1), (0,-1) sum (1,1).
  Try: (1,0), (0,1), (1,0), (-1,-1)? (-1,-1) is not an O move.
  Try: (1,0), (0,1), (0,-1), (1,0) sum (2,0).
  Try: (0,1), (0,1), (0,1), (1,-2)? No.
  We need four O's summing to (1,-1). The possible sums of four O's: each O is (±1,0) or (0,±1). The sum of x-components is sum of ±1 for horizontal moves. Let h be number of horizontal moves, v vertical. h+v=4. x-sum = sum of h terms of ±1. To get x=1, we need h odd? Actually, sum of h terms of ±1 has the same parity as h. For x=1 (odd), h must be odd. Similarly, y=-1 (odd), v must be odd. Since h+v=4, the only way both are odd is if h=1, v=3 or h=3, v=1.
  If h=3, v=1: x-sum = sum of three ±1's = ±1 or ±3. To get 1, we need two +1 and one -1. y-sum = ±1 (one vertical). To get -1, we need the vertical to be -1.
  So we need three horizontal moves: two (1,0) and one (-1,0), and one vertical move (0,-1). The order must be such that the path doesn't cross itself.
  Let's try: R1 at (0,0).
  Move 1: (1,0) -> R2 at (1,0).
  Move 2: (1,0) -> R3 at (2,0).
  Move 3: (-1,0) -> R4 at (1,0) (back to R2). Not allowed.
  So we cannot do the (-1,0) immediately after two (1,0). We need to separate them.
  Try: (1,0), (0,-1), (1,0), (-1,0)? Sum: x: 1+0+1-1=1, y: 0-1+0+0=-1. Yes!
  Path: R1(0,0) --(1,0)--> R2(1,0) --(0,-1)--> R3(1,-1) --(1,0)--> R4(2,-1) --(-1,0)--> B(1,-1)? That's back to R3. Not allowed.
  Try: (1,0), (0,-1), (0,1)? No, sum y=0.
  Try: (0,-1), (1,0), (1,0), (-1,0). Sum: x: 0+1+1-1=1, y: -1+0+0+0=-1.
  Path: R1(0,0) --(0,-1)--> R2(0,-1) --(1,0)--> R3(1,-1) --(1,0)--> R4(2,-1) --(-1,0)--> B(1,-1). Again B at (1,-1) which is R3.
  Try: (1,0), (0,1), (0,-1), (0,-1)? Sum: x=1, y=-1.
  Path: R1(0,0)->(1,0)R2->(1,1)R3->(1,0) which is R2.
  Try: (0,1), (1,0), (0,-1), (0,-1)? Sum: x=1, y=-1.
  R1(0,0)->(0,1)R2->(1,1)R3->(1,0)R4->(1,-1)B. B is at (1,-1).
  Check distinctness: (0,0),(0,1),(1,1),(1,0),(1,-1). All distinct!
  Now B at (1,-1) must move D to R1 at (0,0). D must be (-1,1) from B to R1. (1,-1) + (-1,1) = (0,0). Yes!
  So this works!
  Sequence: R1(0,0), R2(0,1), R3(1,1), R4(1,0), B(1,-1).
  Colors: R,R,R,R,B.
  Moves: (0,1), (1,0), (0,-1), (0,-1), (-1,1). Wait, from R4(1,0) to B(1,-1) is (0,-1). From B(1,-1) to R1(0,0) is (-1,1).
  Check: R1 to R2: (0,0)→(0,1) orth.
  R2 to R3: (0,1)→(1,1) orth.
  R3 to R4: (1,1)→(1,0) orth.
  R4 to B: (1,0)→(1,-1) orth.
  B to R1: (1,-1)→(0,0) diag.
  All distinct? Yes.
  So R=4,B=1 works.

This suggests a general method: we can always arrange the O moves to sum to the required vector while keeping the path simple. In fact, we can always make a "staircase" that goes in one direction, then turns, etc., to get the desired sum.

Given the complexity, and since this is a known problem, I can implement the following constructive solution based on the editorial (which I recall now):

The condition for "No" is:
- R is odd, or
- R=0 and B is odd.

Otherwise "Yes".

Construction for "Yes":
- If B=0: R even. Use 2×(R/2) rectangle.
- If R=0: B even. Use rotated grid cycle.
- If R≥2 and B≥1: 
  We can use a "comb" construction:
  Place reds at (1,1), (1,2), ..., (1, R/2) and (2, R/2), (2, R/2 -1), ..., (2,1). This is a cycle of R reds.
  Now we need to insert B blues. We can "expand" the vertical segments. For each vertical orth move from (1,i) to (2,i), we can replace it with a zigzag of blues. Specifically, a vertical move (0,1) can be replaced by two diag moves (1,1) and (-1,0)? No, diag moves are (1,1) and (-1,0) is orth. We need to use diag moves.
  Actually, a vertical orth move (0,1) can be replaced by a sequence of diag moves that net (0,1) but that's impossible because diag moves change both coordinates. However, we can replace a vertical move and a horizontal move together.
  Alternative: Use a different base cycle for reds that is "loose" enough to insert blues.

After more thought, a simpler universal construction for R≥2, B≥1:
We can place the pieces in a "spiral" that uses all pieces.
Start with a red at (0,0). Go right with a red, then down with a blue, left with a blue, up with a red, etc. But we need exact counts.

Actually, there is a very simple construction:
If R≥2 and B≥1, we can do:
- Place two reds at (1,1) and (1,2).
- Place B-1 blues at (2,2), (3,3), ..., (B, B) [if B≥2] or just one blue at (2,2) if B=1? Wait, for B=1, we need a different path.
Let's try to construct for R=2, B arbitrary:
We have a solution for B=1,2,3. We can generalize.
For R=2, B=2k-1 (odd B):
  Place R1 at (0,0).
  Place B1 at (1,0) (orth from R1).
  Place B2 at (2,1) (diag).
  Place B3 at (3,2) (diag).
  ...
  Place B_{2k-2} at (2k-2, 2k-3) (diag).
  Place B_{2k-1} at (2k-1, 2k-2) (diag).
  Place R2 at (2k, 2k-1) (diag from B_{2k-1}).
  Then R2 must move orth to R1. R2 at (2k, 2k-1) to (0,0)? Not orth. So this doesn't work.

Let's look at the pattern for R=2, B=1: (1,1)R, (1,2)R, (2,2)B. B is at (2,2), R1 at (1,1). R2 at (1,2). R2→B is orth. B→R1 is diag.
For R=2, B=3: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4).
Notice that the two reds are at (3,2) and (2,4). The blues form a path from (2,3) to (2,2) to (3,3). The cycle is: B1(2,3) -> R1(3,2) -> B2(2,2) -> B3(3,3) -> R2(2,4) -> B1(2,3).
The last move R2->B1 is orth: (2,4)->(2,3).
The first move B1->R1 is diag: (2,3)->(3,2).
The reds are at positions (3,2) and (2,4). They are connected via the blue path.

For R=2, B=5: we can extend the blue path. The pattern seems to be that the blue path is a "staircase" that goes down-left and up-right, and the reds are at the "ends" of the staircase.
Specifically, for B=2k-1:
  Place B1 at (0,1).
  Place R1 at (1,0).
  Place B2 at (1,1).
  Place B3 at (2,2).
  Place B4 at (2,1)? No.
Let's try to formalize the sample:
B1: (2,3)
R1: (3,2)
B2: (2,2)
B3: (3,3)
R2: (2,4)
Differences:
B1->R1: (1,-1) diag
R1->B2: (-1,0) orth
B2->B3: (1,1) diag
B3->R2: (-1,1) diag
R2->B1: (0,-1) orth
Sum: (1-1+1-1+0, -1+0+1+1-1) = (0,0).

If we add more blues, we can insert them between B2 and B3, or between B3 and R2. For example, to add two more blues, we can replace B2->B3 (which is (1,1)) with a longer path. We can replace a (1,1) diag move with three diag moves: (1,1) = (1,1) + (1,-1) + (-1,1)? (1,1)+(1,-1)+( -1,1) = (1,1). So we can insert two extra pieces (one blue at (1,0) from B2? Let's see: B2 at (2,2). Add B_new1 at (3,1) (diag: (1,-1)). Then B_new2 at (4,2) (diag: (1,1)). Then B3 at (3,3) (diag: (-1,1)). So path: (2,2)->(3,1)->(4,2)->(3,3). That's two extra blues. We can repeat this to add any even number of blues. For odd number, we might need a different insertion.

But we have R≥2. We can use a more flexible construction.

Given the time, and since this is a coding problem, I will implement the following known solution from the editorial of "Pieces on Board" (AtCoder ARC 155 D? Actually it's from a different contest, but the solution is well-known):

Algorithm:
1. If R is odd: print "No".
2. Else if R == 0:
   - If B is odd: print "No".
   - Else: print "Yes" and construct a cycle of blues using a rotated rectangle.
3. Else (R >= 2, even):
   - Print "Yes" and construct a cycle.
   - Construction for R even, B >= 0:
     If B == 0: use 2×(R/2) rectangle.
     Else: use a "spiral" or "ladder" construction.

A robust construction for R>=2, B>=1:
Place the pieces in the following order:
- R/2 reds at (1,1), (1,2), ..., (1, R/2).
- Then B blues at (2,2), (3,3), ..., (B+1, B+1) if B>=1? No.

Let's design a simple "staircase" cycle that works for any R>=2, B>=1.
Consider the cycle:
Start at (0,0) [R]
Go right R/2 - 1 times with reds? No.

Another idea: Use the fact that we can make a cycle that is a "snake" covering a 2×(R/2 + B) grid? But we need to assign colors.

I recall a very simple construction:
For R even >= 2, B >= 1:
  Place the pieces in a 2×k grid where k = R/2 + B.
  The cycle goes: (1,1) -> (1,2) -> ... -> (1,k) -> (2,k) -> (2,k-1) -> ... -> (2,1) -> (1,1).
  Now we need to assign colors to these k*2 pieces such that there are R reds and B blues.
  In this cycle, the moves are all orthogonal.
  But we need the moves to be orth or diag according to the piece's color.
  If we assign all pieces to be red, we need B=0.
  If we assign some pieces to be blue, then the moves from those pieces must be diagonal. But in this cycle, all moves are orthogonal! So if a piece is blue, it cannot move to the next piece if the next piece is orthogonally adjacent. Because blue moves are diagonal.
  So this cycle only works if all pieces are red. We need a cycle with diagonal moves as well.

So we need to incorporate diagonal moves. A cycle with both orth and diag moves must have changes in direction that allow diag moves.

What about a cycle that goes around a "diamond" shape? For example, the 8-cycle around a 3x3 square center? But we need to assign colors.

Maybe we can use a cycle that is a "staircase" that goes diagonally, and we insert reds at the turns.
A staircase: (0,0) -> (1,1) -> (2,2) -> ... -> (m,m) -> (m, m+1) -> (m-1, m+1) -> ... -> (0, m+1) -> (0, m) -> (1, m) -> ... -> (m, m). This is a cycle if m=1? For m=2: (0,0)->(1,1)->(2,2)->(2,3)->(1,3)->(0,3)->(0,2)->(1,2)->(2,2)? No, last is (2,2) which is already visited.
Actually, a common cycle in diagonal grid is a "rectangle" rotated. For example, a 4x4 cycle: (0,0)->(1,1)->(2,2)->(3,3)->(3,2)->(2,1)->(1,0)->(0,0)? Not diag.

Given the time, I will implement the solution as follows:
- Check impossibility: R odd, or (R==0 and B odd).
- For construction:
  - If B == 0: R even. Place reds in a 2x(R/2) cycle.
  - If R == 0: B even. Place blues in a rotated 2x(B/2) cycle.
  - If R >= 2 and B >= 1: 
    Use the construction from the AtCoder editorial:
    Place pieces in a "comb" shape.
    Specifically, for R >= 2, B >= 1:
    Let h = R/2.
    We will place 2h reds and B blues.
    Place reds at:
      (1, 1), (1, 2), ..., (1, h)
      (2, h), (2, h-1), ..., (2, 1)
    Now we have R reds forming a cycle.
    To insert B blues, we replace some of the vertical moves with "detours" of blues.
    Specifically, for each blue we want to add, we can replace one vertical move (0,1) with a path of two blues? But that would add one piece and change the move from orth to diag.
    Actually, we can replace a vertical move (0,1) with two diagonal moves: (1,1) and (-1,0)? No, (-1,0) is orth.
    We need to use diagonal moves.
    A vertical move (0,1) can be replaced by three diagonal moves: (1,1), (0,-1)? No, (0,-1) is orth.
    A vertical move (0,1) can be replaced by a sequence of diagonal moves that net (0,1). As noted, sum of diagonal moves has both components even. So we cannot net (0,1) with diagonal moves. So we cannot replace a single vertical move.
    However, we can replace a pair of moves: a horizontal and a vertical. For example, (1,0) + (0,1) = (1,1). We can replace these two orth moves with one diag move (1,1). That removes one red and adds one blue. But we want to add blues, not remove reds.
    So we can start with a base cycle of R+something reds, and then replace some reds with blues? No, R is fixed.

    Another approach: Build the cycle from scratch with the required number of pieces.
    We can use a "spiral" that has exactly R reds and B blues.
    For R even >= 2, B >= 1:
    Place the pieces in the following order (sequence of colors):
    R, R, B, B, ..., B, R, R, B, B, ...? No.

    Let's try to construct explicitly for R=2, B=1,2,3,4 and generalize.
    R=2, B=1: (1,1)R, (1,2)R, (2,2)B.
    R=2, B=2: (1,1)B, (2,2)B, (2,3)R, (1,3)R. (Wait, earlier we had B(0,0), B(1,1), R(1,2), R(0,2). Let's use positive: B(1,1), B(2,2), R(2,3), R(1,3). Check: B(1,1)->B(2,2) diag, B(2,2)->R(2,3) orth, R(2,3)->R(1,3) orth, R(1,3)->B(1,1) orth. Works.)
    R=2, B=3: sample: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4).
    R=2, B=4: We can try to extend. Maybe: B(1,1), B(2,2), B(3,3), B(4,4), R(4,5), R(1,5)? Then R(1,5)->B(1,1) orth? (1,5) to (1,1) is not orth. So need to close the loop.
    Let's try to make a cycle that goes diagonally up-right for B steps, then orth left/right, etc.
    Actually, for R=2, we can always do:
    Place R1 at (1,1).
    Place R2 at (1, B+2) if B is even? Or (1, B+3) if B is odd?
    For B=1: R2 at (1,2) -> B at (2,2). Works.
    For B=2: R2 at (1,4)? Let's try: R1(1,1), B1(1,2) (orth), B2(2,3) (diag), B3(3,4) (diag), B4(4,5) (diag)? No, B=2.
    Let's try: R1(1,1), B1(2,1) (orth down), B2(3,2) (diag), R2(3,3) (diag from B2). Then R2->R1: (3,3) to (1,1) is not orth.
    So we need R2 to be orth adjacent to R1.
    So R1 and R2 must be in the same row or column, or adjacent diagonally? No, they must be orth adjacent.
    In all our examples, the two reds are orth adjacent? 
    R=2,B=1: R1(1,1), R2(1,2) -> orth adjacent.
    R=2,B=2: R1(2,3), R2(1,3) -> orth adjacent.
    R=2,B=3: R1(3,2), R2(2,4) -> not orth adjacent! (3,2) and (2,4) are not orth adjacent. But the move from R2 to R1 is not direct; the cycle goes R2->B1->...->R1. So the reds don't need to be adjacent. The cycle can have a long path of blues between the two reds.
    So R1 and R2 can be far apart.

    Let's look at the sample for R=2,B=3:
    B1(2,3) -> R1(3,2) -> B2(2,2) -> B3(3,3) -> R2(2,4) -> B1(2,3).
    Here R1 and R2 are at (3,2) and (2,4). They are not adjacent.
    The path from R2 to R1 goes through B1: R2(2,4) -> B1(2,3) (orth) -> R1(3,2) (diag).
    So the path from R2 to R1 is: orth then diag.
    The path from R1 to R2 is: orth then diag then diag: R1(3,2) -> B2(2,2) (orth) -> B3(3,3) (diag) -> R2(2,4) (diag).
    So the cycle is symmetric if we swap the two paths.
    In general, for R=2, we can have a path of blues from R1 to R2, and a path of blues from R2 to R1. The total number of blues is B. We can split B into B1 and B2 such that the path from R1 to R2 uses B1 blues, and the path from R2 to R1 uses B2 blues, with B1+B2 = B.
    The path from R1 to R2 starts with an orth move (from R1 to first blue) and then B1-1 diag moves, then a diag move to R2. So the displacement from R1 to R2 is: orth + B1 diag moves.
    Similarly, displacement from R2 to R1 is: orth + B2 diag moves.
    Sum of displacements = 0.
    Let the orth from R1 be v1, and the orth from R2 be v2. v1 and v2 are (±1,0) or (0,±1).
    The diag moves sum to some vectors d1 and d2.
    So v1 + d1 + v2 + d2 = 0.
    Also, the diag moves must form a path of length B1 and B2 respectively.
    We can choose B1 and B2 to be anything as long as B1+B2=B and B1,B2 >= 1? Actually, one of the paths could have 0 blues? If B1=0, then R1 moves directly to R2 with an orth move. That would mean R1 and R2 are orth adjacent. Then the other path has B blues. So we can have R1 and R2 orth adjacent, and the other path is a long diag path. This might be easier.
    For example, for R=2, B=3: we could have R1 and R2 orth adjacent, and the other path has 3 blues. Let's try: R1(0,0), R2(1,0) (orth adjacent). The cycle is R1->R2->B1->B2->B3->R1. Moves: R1->R2: orth. R2->B1: orth? No, R2 is red, so R2->B1 is orth. Then B1->B2: diag, B2->B3: diag, B3->R1: diag.
    So we need: R2 to B1 orth, B1 to B2 diag, B2 to B3 diag, B3 to R1 diag.
    R1 at (0,0), R2 at (1,0).
    B1 must be orth adjacent to R2: (0,0), (2,0), (1,1), (1,-1). (0,0) is R1, (2,0) is free, (1,1) free, (1,-1) free.
    Choose B1 at (2,0). Then B1 to B2 diag: B2 at (3,1) or (3,-1) or (1,1) or (1,-1). Choose B2 at (3,1).
    B2 to B3 diag: B3 at (4,2) or (4,0) or (2,2) or (2,0) [B1]. Choose B3 at (4,2).
    B3 to R1 diag: R1 at (0,0). B3 at (4,2) to (0,0) is not diag. So this doesn't work.
    Choose B1 at (1,1). B2 at (2,2) or (2,0) or (0,2) or (0,0). Choose B2 at (2,2). B3 at (3,3) or (3,1) or (1,3) or (1,1). Choose B3 at (3,3). B3 to R1(0,0): not diag.
    Choose B1 at (1,-1). B2 at (2,-2) or (2,0) or (0,-2) or (0,0). B2 at (2,-2). B3 at (3,-3) or (3,-1) or (1,-3) or (1,-1). B3 at (3,-3). To (0,0): not diag.
    So having R1 and R2 orth adjacent with a single long blue path back doesn't work easily because the blue path goes away and can't return in one diag step.

    So the two-path approach with both paths having at least one blue is better. In the sample, both paths have blues. Path1: R1->B2->B3->R2 (B1=2 blues? Wait, R1 to B2 is orth, B2 to B3 is diag, B3 to R2 is diag. So that's 2 blues between R1 and R2? Actually, the blues between R1 and R2 are B2 and B3: 2 blues. Path2: R2->B1->R1: R2 to B1 is orth, B1 to R1 is diag. So 1 blue between R2 and R1. Total 3 blues. Yes.
    So we can split B into B_left and B_right.
    The displacement from R1 to R2 is: v1 + sum of B_left diag moves.
    The displacement from R2 to R1 is: v2 + sum of B_right diag moves.
    Sum = 0.
    We can choose v1 and v2 to be, say, (1,0) and (-1,0). Then the diag moves must sum to (0,0).
    If we choose v1=(1,0) and v2=(-1,0), then d1 + d2 = (0,0).
    We can make d1 and d2 be paths that go out and back.
    For example, for B=3, we can have B_left=2, B_right=1.
    d1: two diag moves that sum to (0,0). Example: (1,1) and (-1,-1). So path: B2, B3 with B2 at (1,1) from R1? R1 at (0,0), v1=(1,0) so B_first is at (1,0). Then B2 at (2,1) (diag (1,1)), B3 at (1,0) (diag (-1,-1))? That goes back. We want to end at R2.
    Actually, we need the path from B_first to R2 using B_left diag moves.
    B_first is at R1 + v1.
    Then B_left-1 diag moves, then last diag move to R2.
    So the displacement from B_first to R2 is sum of B_left diag moves = d1.
    So R2 = B_first + d1 = R1 + v1 + d1.
    Similarly, R1 = R2 + v2 + d2.
    So v1 + d1 = R2 - R1.
    v2 + d2 = R1 - R2.
    We can choose R1 and R2 freely, then choose v1, v2, and then find d1, d2.
    Since we can make d1 and d2 any vectors that can be expressed as sum of diag moves with the path constraints, we have flexibility.

    Given the complexity, and since this is a standard problem, I will implement the following construction which I know works (from the AtCoder ARC 155 D editorial):

    For R >= 2, B >= 1:
    Let k = R/2.
    We will place 2k reds and B blues.
    The cycle is:
    (1,1) R
    (1,2) R
    ...
    (1,k) R
    (2,k) B
    (3,k+1) B
    ...
    (B+1, k+B-1) B
    (B+1, k+B) R
    (B, k+B) R
    ...
    (2, k+2) R? No.

    Let's search for the exact construction. I recall that for R even >= 2, B >= 1, the answer is always Yes, and one construction is:
    Place reds at (1,1), (1,2), ..., (1, R/2) and (2, R/2 + B), (2, R/2 + B - 1), ..., (2, B+1).
    Place blues at (2, B+1)? No.

    Another construction: Use a "snake" that goes:
    Row 1: R R R ... R
    Row 2: B B B ... B
    Row 3: R R R ... R
    ...
    But we only have R reds and B blues. If B > R, we might have multiple rows of blues.

    Actually, a very simple construction for R even >= 2, B >= 1:
    Place the pieces in a single row alternating? No.

    Let's think of a cycle that is a "staircase" with reds at the corners.
    For example, a cycle of length 6: (0,0)R, (1,0)B, (1,1)R, (2,1)B, (2,2)R, (0,2)B? No, (0,2) to (0,0) is not orth.
    Wait, (0,2) to (0,0) is orth if they are adjacent? No, distance 2.

    What about a cycle that is a "loop" of width 2:
    (0,0)R, (0,1)B, (1,1)B, (1,0)R. This is R=2, B=2.
    For R=4, B=2: we can add two more reds to the R=2,B=2 cycle by extending one of the sides.
    R=2,B=2: (1,1)B, (2,2)B, (2,3)R, (1,3)R.
    Add R at (1,2) and R at (2,1)? 
    Try: (1,1)B, (2,2)B, (2,3)R, (1,3)R, (1,2)R, (2,1)R? Check moves:
    B(1,1)->B(2,2) diag
    B(2,2)->R(2,3) orth
    R(2,3)->R(1,3) orth
    R(1,3)->R(1,2) orth
    R(1,2)->R(2,1) orth? (1,2) to (2,1) is (1,-1) diag, not orth.
    So no.

    Given the time constraints, I will implement the following known solution from a similar problem (Codeforces or AtCoder):

    The condition for "No" is: R % 2 == 1 OR (R == 0 AND B % 2 == 1).

    Construction for "Yes":
    - If B == 0:
        R is even and >= 2.
        Place reds at (1,1) to (1, R/2) and (2, R/2) down to (2,1).
        Sequence: (1,1), (1,2), ..., (1, R/2), (2, R/2), (2, R/2 -1), ..., (2,1).
    - If R == 0:
        B is even and >= 2.
        Place blues at (1,1) to (B/2, B/2) [diagonal] then (B/2+1, B/2) to (B/2+1, 1) [vertical? No, diagonal only].
        We need a cycle of diagonal moves of even length.
        Use: (1,1), (2,2), ..., (m,m), (m+1, m), (m, m-1), ..., (1,0) shifted? 
        Actually, use the rotated grid cycle: take a 2x(B/2) rectangle in the grid, cycle it, and rotate.
        Grid cycle: (0,0)-(1,0)-...-(k-1,0)-(k-1,1)-...-(0,1)-(0,0) where k=B/2.
        Rotate: (x,y) -> (x+y, x-y+offset).
        Let's do it explicitly for B=2: (0,0)->(1,1). (1,1)->(0,0). Cycle: (1,1),(2,2).
        For B=4: k=2. Grid: (0,0),(1,0),(1,1),(0,1). Rotated: (0,0)->(0,0); (1,0)->(1,1); (1,1)->(2,0); (0,1)->(1,-1). Cycle: (0,0),(1,1),(2,0),(1,-1). Shift to positive: (2,2),(3,3),(4,2),(3,1).
        For general even B=2k: grid cycle of length 2k: (0,0),(1,0),(2,0),...,(k-1,0),(k-1,1),(k-2,1),...,(0,1). Rotate and shift.
        Rotation: u = x+y, v = x-y. Then points: (0,0), (1,1), (2,2), ..., (k-1, k-1), (2k-2, k-1), (2k-3, k-2), ..., (k, 1).
        Let's list:
        (0,0) -> (0,0)
        (1,0) -> (1,1)
        (2,0) -> (2,2)
        ...
        (k-1,0) -> (k-1, k-1)
        (k-1,1) -> (k, k-2)
        (k-2,1) -> (k-1, k-3)
        ...
        (0,1) -> (1, -1)
        This is a cycle of diagonal moves. We can shift by adding (1,1) to make positive: (1,1),(2,2),...,(k,k),(k+1,k-1),...,(2,0).
        Let's check: (1,1)->(2,2) diag, (2,2)->(3,3) diag,... (k-1,k-1)->(k,k) diag, (k,k)->(k+1,k-1) diag? (k,k) to (k+1,k-1) is (1,-1) diag, yes. (k+1,k-1)->(k,k-2) diag, ... (2,0)->(1,1) diag? (2,0) to (1,1) is (-1,1) diag, yes.
        So this works! All coordinates are positive if we shift by (1,1). Actually (2,0) is positive. (1,1) is positive. So it's fine.
        So for R=0, B even, we use this construction.
    - If R >= 2 and B >= 1:
        We can combine the two constructions.
        Use the R=0 construction for B+2 pieces? No.
        Use a construction that "wraps" the red cycle with blues.
        Specifically, for R even >=2, B >=1:
        Let m = R/2.
        We will place the reds at:
        (1,1), (1,2), ..., (1,m)
        (2,m), (2,m-1), ..., (2,1)
        This is a cycle of R reds.
        Now we have B blues. We can "insert" them by replacing some moves.
        Actually, we can add the blues as a "spike" or by extending the cycle.
        A simple way: take the R=0 construction for B blues, and "merge" it with the red cycle by replacing one red move with the blue cycle.
        Since we can't easily merge, we can build a new cycle from scratch.
        Let's use the following cycle (spiral):
        Start at (1,1) [R]
        Go right m-1 times: (1,2) [R], ..., (1,m) [R]
        Go down: (2,m) [R]
        Go left: (2,m-1) [R], ..., (2,2) [R]? No, we need to insert blues.
        Let's go: (1,1)R, (1,2)R, ..., (1,m)R.
        Then (2,m)B? No, (2,m) is orth from (1,m). So if we put a blue at (2,m), it must be blue, and the move is orth. Then from (2,m), we can go diag to (3,m+1)B, etc., and eventually come back to (1,1) via a red.
        This is exactly the R=2,B=3 sample extended!
        In the sample, m=1. R=2. B=3.
        They did: (1,1) was not used. They had B(2,3), R(3,2), B(2,2), B(3,3), R(2,4).
        Let's map to m=1:
        R1 at (3,2), R2 at (2,4).
        B1 at (2,3), B2 at (2,2), B3 at (3,3).
        Path: B1->R1 (diag), R1->B2 (orth), B2->B3 (diag), B3->R2 (diag), R2->B1 (orth).
        Notice that R1 and R2 are not in the "comb" position. They are placed such that the blue path connects them.
        For general m and B, we can do:
        Place the two "end" reds at (m+1, 2) and (2, m+B+1)? Let's try to generalize the sample.
        Sample: m=1, B=3. R1 at (3,2) = (m+2, 2)? m+2=3, yes. R2 at (2,4) = (2, m+B+1)? 1+3+1=5? No, 4. m+B=4, so (2, m+B)? Yes, (2,4).
        B1 at (2,3) = (2, m+B)? m+B=4, but 3. So (2, m+B-1)?
        B2 at (2,2) = (2, m+1)? m+1=2.
        B3 at (3,3) = (m+2, m+2)? 3,3.
        This is getting messy.

        Let's try a different systematic construction for R>=2, B>=1.
        We can use a "ladder" that has R reds as the "rails" and B blues as the "rungs".
        Specifically, place reds at:
        (1,1), (1,2), ..., (1, B+1)  [B+1 reds? No, we only have R reds. R could be less than B+1.]

        Actually, since R>=2 is even, we can set k = R/2.
        Place k reds on the top row: (1,1) to (1,k).
        Place k reds on the bottom row: (2,k) to (2,1) (reversed).
        This is the red cycle.
        Now we want to add B blues. We can "expand" the cycle by inserting blues into the vertical segments.
        For each vertical segment from (1,i) to (2,i), we can replace it with a zigzag of blues.
        A vertical move (0,1) cannot be replaced by diag moves. But we can replace the pair of moves: the horizontal move from (1,i) to (1,i+1) and the vertical move from (1,i+1) to (2,i+1)? No.

        Another idea: Use a cycle that is a "large" loop with reds at the corners and blues along the edges.
        For example, a rectangle with R/2 reds on the top, R/2 reds on the bottom, and blues on the left and right sides.
        The top and bottom edges are orth moves. The left and right edges need to be diag moves to accommodate blues.
        So we can have:
        Top: (1,1) to (1, R/2) all reds, orth moves.
        Right: from (1, R/2) down to (2, R/2) with blues using diag moves.
        Bottom: (2, R/2) to (2, 1) all reds, orth moves.
        Left: from (2,1) up to (1,1) with blues using diag moves.
        The right side: we need a path of blues from (1, R/2) to (2, R/2) using diag moves.
        The left side: a path of blues from (2,1) to (1,1) using diag moves.
        The total number of blues is B. We can split B into B_left and B_right for the two sides.
        The path on the right: start at (1, R/2). The first move is orth? No, the piece at (1, R/2) is red, so it moves orth to the next piece. The next piece is the first blue on the right side. So the first blue is orth adjacent to (1, R/2). So it could be at (1, R/2+1) or (2, R/2) or (0, R/2) or (1, R/2-1). We want to go down, so we pick (2, R/2). So B1_right is at (2, R/2). Then B1_right moves diag to B2_right, etc., until the last blue on the right side moves diag to the first red on the bottom side, which is at (2, R/2). But (2, R/2) is already B1_right! So the last blue must be at (2, R/2) or (3, R/2+1) or (1, R/2+1) or (1, R/2-1). We want it to be at (2, R/2) to connect to the bottom red. So the last blue is at (2, R/2). But the first blue is also at (2, R/2). So the path of blues on the right is a cycle that starts and ends at (2, R/2)? That would mean the blues form a cycle, and the reds just touch it. But we need a single cycle for all pieces.
        Actually, the cycle would be: ... top reds ... -> B1_right -> B2_right -> ... -> B_{B_right}_right -> bottom reds -> ... -> B1_left -> ... -> B_{B_left}_left -> top reds ...
        The move from the last top red (1, R/2) is orth to B1_right. So B1_right must be orth adjacent to (1, R/2). The move from B_{B_right}_right to the first bottom red (2, R/2) is diag. So B_{B_right}_right must be diag adjacent to (2, R/2).
        Similarly for the left side: move from last bottom red (2,1) is orth to B1_left. B1_left orth adjacent to (2,1). Move from B_{B_left}_left to first top red (1,1) is diag.
        So we need a path of blues on the right from a square orth adjacent to (1, R/2) to a square diag adjacent to (2, R/2).
        Let's choose B1_right at (2, R/2) (orth adjacent to (1, R/2) via down). Then we need the last blue to be diag adjacent to (2, R/2). The last blue could be at (2, R/2) itself, but then it's the same square. Or at (3, R/2+1), (3, R/2-1), (1, R/2+1), (1, R/2-1). We want the path to go down and then back up? Actually, the path can go down-right, down-left, etc.
        If B=1, we can have B1_right at (2, R/2). Then it must be diag adjacent to (2, R/2)? No, the last blue is B1_right itself, and it must move diag to the bottom red (2, R/2). So (2, R/2) must be diag adjacent to itself? Impossible. So B1_right cannot be the same as the destination.
        So we need the path to have at least one intermediate blue, or start elsewhere.
        Let's choose B1_right at (1, R/2+1) (orth right from (1, R/2)). Then the path of blues must go from (1, R/2+1) to a square diag adjacent to (2, R/2). For B=1, we have only one blue, so it is both first and last. It must be orth adjacent to (1, R/2) and diag adjacent to (2, R/2). Is there a square that is orth adjacent to (1, R/2) and diag adjacent to (2, R/2)? The orth adjacent squares to (1, R/2) are (0, R/2), (2, R/2), (1, R/2-1), (1, R/2+1). The diag adjacent to (2, R/2) are (1, R/2-1), (1, R/2+1), (3, R/2-1), (3, R/2+1). The intersection is (1, R/2-1) and (1, R/2+1). So we can place B1 at (1, R/2+1). Then the move from (1, R/2) to (1, R/2+1) is orth, and from (1, R/2+1) to (2, R/2) is diag? (1, R/2+1) to (2, R/2) is (1,-1) diag, yes! So this works!
        So for B=1, we can do:
        Top reds: (1,1) to (1, R/2).
        Last top red at (1, R/2) moves orth to B1 at (1, R/2+1).
        B1 moves diag to bottom red at (2, R/2).
        Bottom reds: (2, R/2) to (2,1) (moving left).
        First bottom red at (2,1) moves orth to... we need to close the cycle. We need to go from (2,1) back to (1,1). We have no more blues. So we need a path from (2,1) to (1,1). (2,1) is red, so it moves orth. It can go to (1,1) directly! (2,1) to (1,1) is orth (-1,0). So the cycle is:
        (1,1)R, (1,2)R, ..., (1, R/2)R, (1, R/2+1)B, (2, R/2)R, (2, R/2-1)R, ..., (2,1)R.
        Check moves:
        (1,1)->(1,2): orth
        ...
        (1, R/2 -1)->(1, R/2): orth
        (1, R/2)->(1, R/2+1): orth (R to B? No, the piece at (1, R/2) is R, so it moves orth. The piece at (1, R/2+1) is B. So R moves orth to B. That's allowed.)
        (1, R/2+1)->(2, R/2): diag (B moves diag to R)
        (2, R/2)->(2, R/2-1): orth (R to R)
        ...
        (2,2)->(2,1): orth
        (2,1)->(1,1): orth (R to R)
        All pieces distinct? Yes, as long as R/2+1 != 2, i.e., R/2 != 1, i.e., R != 2.
        If R=2, then R/2=1. Then the top red is at (1,1), bottom red at (2,1). The blue is at (1,2). The cycle: (1,1)->(1,2) orth, (1,2)->(2,1) diag, (2,1)->(1,1) orth. This is exactly the R=2,B=1 solution! (1,1)R, (1,2)B, (2,1)R? Wait, in my earlier R=2,B=1: (1,1)R, (1,2)R, (2,2)B
