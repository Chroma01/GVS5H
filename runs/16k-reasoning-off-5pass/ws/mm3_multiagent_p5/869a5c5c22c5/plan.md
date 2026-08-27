The problem asks for a Hamiltonian-like cycle in a mixed-move graph: red pieces move orthogonally, blue pieces move diagonally. We need to place R reds and B blues in a cyclic order where consecutive pieces (and last-to-first) can move to each other in exactly one move, i.e., a square of a piece must be exactly one king's-move (king without orthogonal+diagonal mix) away from the next piece's square, with the move type matching the piece that moves.

Key insight: A red piece (orthogonal move) at (r,c) and a blue piece (diagonal move) at (r',c') satisfy the "i-th can move to (i+1)-th" condition if and only if |r−r'|+|c−c'| = 1 (red moves orthogonally) OR max(|r−r'|,|c−c'|) = 1 and r−r' and c−c' are both nonzero (blue moves diagonally).

We can think of coloring the infinite grid like a checkerboard. On a standard chessboard, diagonal moves preserve color (same color), while orthogonal moves flip color. So:
- A red piece moves to a square of opposite color.
- A blue piece moves to a square of the same color.

Thus in the cycle, between two consecutive pieces:
- Red → any: red moved, so squares alternate color? Not exactly, because blue doesn't change color.
Let C(p) be the color of the square piece p is on. Then:
- If i-th is red, C(i+1) = opposite of C(i).
- If i-th is blue, C(i+1) = C(i).

We want a cycle of length N = R+B. This imposes parity constraints on the number of reds (since each red flips color, and returning to start requires even number of color flips).

Counting color flips around cycle = number of red pieces (each red contributes 1 flip). For a cycle, we must return to same color, so R must be even. If R is odd, answer is No.

If R is even, can we always construct? We need to be careful with small cases (R=0, R=2, etc.) but for R≥2 even and any B, or B=0 with R≥4, we can construct.

Actually, let's think more carefully:
- B=0, R=0: trivial but R+B≥2 so N≥2.
- B=0, R≥2: need a cycle using only orthogonal moves. This is a 2-coloring of cycle, need even R. Smallest: R=2, squares (1,1) and (1,2) — piece 1 at (1,1), piece 2 at (1,2), then piece 2 moves to (1,1) (yes, orthogonally adjacent). Cycle of 2 works.
- R=0, B≥2: need cycle with only diagonal moves. Diagonal moves on same color, so all squares same color. Can we form a cycle? For B=2: (1,1) and (2,2) — blue at (1,1) can move to (2,2) and back. Yes, works. For B≥2, easy.
- R=1, any B: R odd, so impossible.
- R=2, B=0: works as above.
- R=2, B=1: N=3, R=2 (even). Let's try: need cycle R,B,R. Place B at (2,2), R at (1,2) and R at (2,1). Check: R(1,2) → B(2,2)? Orthogonal, yes (down). B(2,2) → R(2,1)? Diagonal, yes. R(2,1) → R(1,2)? Orthogonal, yes (up). Works!
- General construction for R≥2 even: We'll build a "spine" using the two red pieces at the ends, and weave blue pieces in between.

Let me design a general construction:
Place two red pieces at fixed positions, and interleave blue pieces between them.

Construction idea:
- Place R₁ at (1, 1).
- Place R₂ at (1, 2). These two reds are orthogonally adjacent.
- For each blue piece, we can insert it in the sequence.

Wait, the cycle order matters. Let's fix the cycle as: R₁, (some blues), R₂, (some blues), back to R₁.

Actually, let's think of it as a cycle where red pieces appear, and between consecutive reds (in cycle order), there's a path of blues. Each blue-blue transition is a diagonal move. The transition from R to first blue: red moves orthogonally to blue. Transition from last blue to R: blue moves diagonally to R.

For a segment of k blues between two reds, we need:
- R at position A, then blue at A+orthogonal direction (say (1,1)→(1,2)), then k-1 more blues via diagonal, then last blue must be diagonal-adjacent to next red.

Let's set: R₁ at (r, c). Then blue B₁ at (r, c+1) (R₁ moves right). Then B₂ at (r+1, c+2) (B₁ moves diagonal). B₃ at (r, c+3) (B₂ moves diagonal? (r+1,c+2) to (r,c+3): r-1, c+1, yes diagonal). So blues alternate row parity: r, r+1, r, r+1, ... going right. After an even number of blues, we end on row r, col c+2k. To connect to R₂, we need R₂ to be orthogonally adjacent to this last blue. So R₂ at (r±1, c+2k) or (r, c+2k±1).

Then from R₂, we go back: R₂ moves to a blue, then more blues back to near R₁.

This is getting complex. Let me look for a simpler known construction.

Simpler approach: Use a "zigzag" path.

Actually, here's a clean construction for R≥2 even, any B≥0:
- Place all red pieces in a horizontal line: (1,1), (1,2), ..., (1,R). But this doesn't directly work because we need a cycle.

Let me try a different angle. Consider the graph where we have a "template" of length R+B that is a valid cycle, and we can expand the path between any two consecutive same-type pieces by adding pieces of opposite type.

Hmm, let me think about the known solution. I recall this is from AtCoder (ABC/ARC). The answer is "Yes" iff R is even (or R=1 and B=1? Let me check: R=1, B=1, N=2. R at (1,1), B at (2,2). R can move to B? Orthogonal from (1,1): (1,2) or (2,1), not (2,2). So No. What if B at (1,2)? R(1,1)→B(1,2) yes. Then B(1,2)→R(1,1)? Diagonal from (1,2): (2,1) or (2,3), not (1,1). So No. R=1,B=1: No.)

R=0,B=2: Yes, as shown.
R=2,B=0: Yes.
R=2,B=1: Yes, as constructed.
R=2,B=2: Let's try. R at (1,1),(1,2). B between them? Cycle: R(1,1), B(1,2)? But then B(1,2) needs to move to next. If cycle is R,B,B,R: R(1,1)→B(1,2) orth yes. B(1,2)→B(2,3) diag yes. B(2,3)→R(2,2) diag from (2,3): (1,2),(3,2),(3,4),(1,4). (2,2) not there. Try B(2,3)→R(3,3)? diag yes. R(3,3)→R(1,1)? (3,3) to (1,1): not orth. 

Let me redo: R₁(1,1), B₁(1,2), B₂(2,3), R₂(2,2). B₁(1,2)→B₂(2,3): diag (1,1) yes. B₂(2,3)→R₂(2,2): diag (0,-1) yes. R₂(2,2)→R₁(1,1): (1,2) to (1,1) is orth (0,-1) yes. R₁(1,1)→B₁(1,2): orth yes. Works!

So for R≥2 even, seems always possible. What about R=0, B=1? N=1, but N≥2, so R+B≥2. R=0,B≥2: works.

So condition is R even. (Including R=0.)

Wait, check R=0,B=1: invalid since N≥2.
R=0,B=2: works (two blues diagonally adjacent).
R=1: R odd, impossible.
R=2: even, works.
R=3: odd, impossible.
R=4: even, should work.
R=5: odd, impossible.

So: Yes iff R is even.

Now I need to provide a construction. Let me devise a general one.

Construction for R even, R≥2, any B≥0:

I'll build a cycle. Let me place pieces along a "staircase" pattern.

Let's denote the cycle order. I'll use a template:

For R=2, B=b: 
Cycle: R, B, B, ..., B, R, then back. Wait, need to connect last R to first R.

Actually, for R=2, here's a working pattern:
R₁ at (1,1).
Then b blues: B₁ at (1,2), B₂ at (2,3), B₃ at (1,4), ..., alternating rows.
If b is even, last blue at (1, 1+2b-1) = (1, 2b). Wait: B₁(1,2), B₂(2,3), B₃(1,4), B₄(2,5), ... Pattern: B_k at (1+(k-1)%2, 1+k) for k=1,...,b. 
If b is even, last B_b at (2, 1+b). Then R₂ at (2, 2+b) or (1, b) or (3, b) etc. We need R₂ orthogonally adjacent to B_b. B_b at (2, 1+b). Place R₂ at (2, 2+b) (right of B_b). Then R₂→R₁: (2, 2+b) to (1,1)? Not adjacent. Hmm.

Let me restart the construction.

Better construction:
- For R≥2 even, place R₁ at (1,1), R₂ at (1,2). 
- We want a cycle. The two reds are adjacent.
- Between them in the cycle, we can insert a path of blues that goes out and comes back, OR we can have multiple "excursions".

Actually, here's a cleaner approach. We can think of the cycle as a sequence. Between any two consecutive reds in the cycle, we can insert any number of blues (including zero) as long as:
1. The first piece after red R moves orthogonally from R.
2. Consecutive blues move diagonally.
3. The last blue before the next red R' is diagonal-adjacent to R'.

For condition 3: blue at (r,c) and red at (r',c') with diagonal adjacency: |r-r'|=1 and |c-c'|=1. So R' is at one of the 4 diagonal neighbors of the last blue.

For condition 1: red at (r,c), first blue at (r',c') orthogonal: |r-r'|+|c-c'|=1.

So given R at (r,c), first blue is at (r±1, c) or (r, c±1). Then we do a diagonal walk of length k (using k blues, but first is already placed, so k-1 more diagonal steps). After k-1 diagonal steps from (r',c'), we land at the last blue. Then R' is diagonally adjacent.

The diagonal walk changes both coordinates by ±1 each step. So starting from (r',c'), after k-1 steps we're at (r' + s, c' + t) where s+t and s-t have same parity as... actually each step changes r by ±1 and c by ±1. So after m steps, (Δr, Δc) has |Δr| ≤ m, |Δc| ≤ m, and m ≡ |Δr|+|Δc| (mod 2)? No, each step changes r by ±1 and c by ±1, so after m steps, r changes by odd/even same as m. Specifically, r goes from r' to r' + (a-b) where a+b=m, a,b≥0 (a steps +1, b steps -1). So Δr = a-b, and a+b=m. So Δr ≡ m (mod 2). Similarly Δc ≡ m (mod 2).

This is getting complicated. Let me just hardcode a construction for all valid (R,B) with R even.

Standard construction (I think this is the known solution):
- R ≥ 2, R even, B ≥ 0.

Place pieces as follows (cycle order = placement order):
1. R at (1, 1)
2. R at (1, 2)  
3. B at (2, 3)
4. B at (1, 4)
5. B at (2, 5)
... continue alternating rows for blues, expanding rightward.

Hmm, this doesn't close the cycle easily.

Let me look at this differently. Consider the "base cycle" for R=2, B=0:
(1,1) R, (1,2) R. That's it, 2 pieces, cycle of length 2.

For R=2, B=1: 
(1,1)R, (1,2)B, (2,2)R? Let's check: R(1,1)→B(1,2) orth yes. B(1,2)→R(2,2) diag (1,0)? No, diag needs both change. (1,2)→(2,2): row+1, col 0, not diagonal. 
Try: R(1,1), B(2,2), R(2,1). R(1,1)→B(2,2)? orth (1,1)→(2,2) no, that's diag distance. Not orth.
Earlier I had: R(1,2), B(2,2), R(2,1). R(1,2)→B(2,2) orth (1,0) yes. B(2,2)→R(2,1) diag (0,-1) yes. R(2,1)→R(1,2) orth (-1,1) yes. Works. So R₁(1,2), B(2,2), R₂(2,1).

Generalizing, for R=2 and any B, here's a construction:
Place R₁ and R₂ at (1,1) and (1,2) — but then we need to connect them through blues back to start. Actually in the cycle, after R₂ we need to get back to R₁.

Let me define the cycle order:
Position 1: R at A₁
Position 2: B at A₂  
...
Position N-1: B at A_{N-1}
Position N: R at A_N
And A_N → A₁ must be a valid move (R moves orthogonally).

The move A_N → A₁ is red moving orthogonally, so |A_N.r - A₁.r| + |A_N.c - A₁.c| = 1.

Move A₁ → A₂: R to B, orthogonally adjacent.
Move A_i → A_{i+1} for 2 ≤ i ≤ N-1: B to B, diagonally adjacent.

So: A₁ and A₂ orthogonally adjacent.
A_2, A_3, ..., A_{N-1} form a diagonal path (each consecutive pair diagonally adjacent).
A_{N-1} and A_N: B to R, diagonally adjacent.
A_N and A_1: R to R, orthogonally adjacent.

So A₁, A_N are orthogonally adjacent. A₁, A₂ orthogonally adjacent. A_{N-1}, A_N diagonally adjacent. And A₂...A_{N-1} is a diagonal path of length N-2 = R+B-2.

Since R=2, the diagonal path has B blues. The two reds A₁, A_N are orthogonally adjacent, and the diagonal path connects a neighbor of A₁ to a neighbor of A_N.

Let's set A₁ = (1,1), A_N = (1,2) (orthogonally adjacent, horizontal).
Then A₂ must be orthogonally adjacent to A₁: (2,1), (0,1)[invalid], (1,2)=A_N[can't reuse], (1,0)[invalid]. So A₂ = (2,1).
A_{N-1} must be diagonally adjacent to A_N=(1,2): (0,1)invalid, (0,3)invalid, (2,1)=A₂? possibly, (2,3).

If B=1, then A₂=A_{N-1}, so A₂=(2,1) must be diag adjacent to A_N=(1,2): |2-1|+|1-2|... wait diag means |Δr|=1 and |Δc|=1. (2,1) and (1,2): |2-1|=1, |1-2|=1, yes diagonally adjacent! So A₂=(2,1) works. Cycle: (1,1)R, (2,1)B, (1,2)R. Check: (1,1)R→(2,1)B: orth (1,0) yes. (2,1)B→(1,2)R: diag (-1,1) yes. (1,2)R→(1,1)R: orth (0,-1) yes. 

If B=2, A₂, A₃ are blues, A₃ diag adjacent to A_N=(1,2). A₂=(2,1), A₃ diag from A₂ and diag to A_N. A₃ diag adjacent to (1,2): could be (0,1),(0,3),(2,1),(2,3). Since A₃≠A₂=(2,1), A₃ ∈ {(0,1),(0,3),(2,3)}. Also A₃ diag adjacent to A₂=(2,1): (1,0)invalid,(1,2),(3,0)invalid,(3,2). So A₃ ∈ {(1,2),(3,2)}. But A₃ must be in {(0,1),(0,3),(2,3)} and {(1,2),(3,2)}. Intersection empty! So this specific A₂=(2,1) doesn't work for B=2 with A_N=(1,2).

So I need flexibility. Let me allow the two reds to be vertically adjacent instead, or use different A_N.

Let me parameterize: A₁=(1,1), A_N=(2,1) (vertically adjacent). A₂ orth adjacent to A₁: (2,1)=A_N, (0,1)inv, (1,2), (1,0)inv. So A₂=(1,2). A_{N-1} diag adjacent to A_N=(2,1): (1,0)inv,(1,2),(3,0)inv,(3,2). So A_{N-1} ∈ {(1,2),(3,2)}.

For B=2: A₂=(1,2), A₃ must be diag from A₂ and diag to A_N=(2,1). A₃ diag from (1,2): (0,1),(0,3),(2,1),(2,3). A₃ diag to (2,1): (1,0),(1,2),(3,0),(3,2). Intersection (excluding A₂=(1,2) and A_N=(2,1)): (0,1),(0,3),(2,3) ∩ (1,0),(3,0),(3,2) = ∅. Still no.

Hmm. The issue is the diagonal path has a parity constraint: after m diagonal steps, the parity of (r+c) changes by m (mod 2). Diagonal move changes r by ±1 and c by ±1, so r+c changes by 0 or ±2. So r+c mod 2 is INVARIANT under diagonal moves!

So all blue pieces in the diagonal path have the same (r+c) parity. Let's call this parity p.

A₂ is orth adjacent to A₁: if A₁=(r,c), A₂ has (r+c) parity opposite to A₁.
A_{N-1} is diag adjacent to A_N: so A_{N-1} has same parity as A_N.
A_N orth adjacent to A₁: A_N has opposite parity to A₁.

But A_{N-1} is in the diagonal path, so has parity p. A_N has parity p+1 (opposite to A₁). A₂ has parity opposite to A₁ = same as A_N = p+1. But A₂ is also in the diagonal path (as the first blue), so A₂ should have parity p. Contradiction unless p = p+1, impossible.

Wait, that means with R=2, the structure "R, B, B, ..., B, R" doesn't work because A₂ (blue, in diagonal path) and A₂ (orth adjacent to R₁) give conflicting parities.

Oh! I see my error. A₂ is a BLUE piece, and the move A₁→A₂ is the RED at A₁ moving to A₂. So A₁ and A₂ are orthogonally adjacent. The diagonal path is A₂, A₃, ..., A_{N-1}, and the move A_{N-1}→A_N is the BLUE at A_{N-1} moving diagonally to A_N.

Parity: diagonal moves preserve (r+c) mod 2. So A₂, A₃, ..., A_{N-1} all have same parity, call it q.
A₁ orth adjacent to A₂: A₁ has parity 1-q.
A_N orth adjacent to A₁: A_N has parity q.
A_N diag adjacent to A_{N-1}: A_N has same parity as A_{N-1}, which is q. Consistent! ✓

So the constraint is: A₁ has parity 1-q, A_N has parity q, A₂...A_{N-1} have parity q.

Now, A₁ and A_N are orthogonally adjacent (R_N → R₁), so A_N has parity opposite to A₁, i.e., parity q = 1-(1-q) = q. ✓ Always consistent.

So no contradiction. Let me recheck B=2 with A₁=(1,1), A_N=(1,2):
A₁=(1,1) parity 0. A_N=(1,2) parity 1. So q=1.
A₂ orth adj to A₁, parity 1: (2,1)parity1, (0,1)inv, (1,2)=A_N, (1,0)inv. So A₂=(2,1). ✓
A_{N-1}=A₃ diag adj to A_N=(1,2)parity1, and in diagonal path so parity 1. A₃ diag from A₂=(2,1)parity1: diag neighbors of (2,1) are (1,0)inv,(1,2),(3,0)inv,(3,2). Parity 1 ones: (1,2)parity1, (3,2)parity1. 
A₃ must also be diag adj to A_N=(1,2): diag neighbors of (1,2): (0,1)inv,(0,3)inv,(2,1),(2,3). Parity 1: (2,1)parity1, (2,3)parity1.
So A₃ ∈ {(1,2),(3,2)} ∩ {(2,1),(2,3)} = ∅. 

So A₁=(1,1), A_N=(1,2) doesn't work for B=2. Let me try A₁=(1,1), A_N=(2,1):
A₁ parity 0, A_N parity 1, q=1.
A₂ orth adj A₁, parity 1: (2,1)=A_N no, (0,1)inv, (1,2)parity1, (1,0)inv. A₂=(1,2).
A₃ diag adj A₂=(1,2), parity 1: (0,1)inv,(0,3)inv,(2,1),(2,3). Parity1: (2,1),(2,3).
A₃ diag adj A_N=(2,1), parity 1: (1,0)inv,(1,2),(3,0)inv,(3,2). Parity1: (1,2),(3,2).
Intersection: ∅. 

Hmm, A₁=(2,2), A_N=(2,3):
A₁ parity 0, A_N parity 1, q=1.
A₂ orth adj A₁, parity 1: (3,2)p1,(1,2)p1,(2,3)=A_N,(2,1)p1. A₂ ∈ {(3,2),(1,2),(2,1)}.
A₃ diag adj A₂, diag adj A_N=(2,3), parity 1.
A₂=(3,2): diag nbrs (2,1)p1,(2,3),(4,1)inv,(4,3)p1. Parity1: (2,1),(2,3),(4,3). Diag nbrs of A_N=(2,3): (1,2)p1,(1,4)inv,(3,2),(3,4)inv. Parity1: (1,2),(3,2). Intersection with A₂ nbrs (parity1): (2,1),(2,3),(4,3) ∩ (1,2),(3,2) = ∅.
A₂=(1,2): diag nbrs (0,1)inv,(0,3)inv,(2,1),(2,3). Parity1: (2,1),(2,3). ∩ (1,2),(3,2) = ∅.
A₂=(2,1): diag nbrs (1,0)inv,(1,2),(3,0)inv,(3,2). Parity1: (1,2),(3,2). ∩ (1,2),(3,2) = {(1,2),(3,2)}. 
So if A₂=(2,1), A₃ ∈ {(1,2),(3,2)}.

Let's pick A₃=(3,2). Check: A₂=(2,1)→A₃=(3,2): diag (1,1) ✓. A₃=(3,2)→A_N=(2,3): diag (-1,1) ✓. 
Full cycle for B=2, R=2: 
A₁=(2,2)R, A₂=(2,1)B, A₃=(3,2)B, A₄=(2,3)R.
Check all:
(2,2)R→(2,1)B: orth (0,-1) ✓
(2,1)B→(3,2)B: diag (1,1) ✓
(3,2)B→(2,3)R: diag (-1,1) ✓
(2,3)R→(2,2)R: orth (0,-1) ✓ 
Works! 

So I can construct for R=2, B=2. But this is ad hoc. I need a general construction for R≥2 even, B≥0.

Let me look for a more systematic construction. 

I recall that for this type of problem, a common construction uses a "comb" or "ladder" shape.

Here's a construction that works for R≥2 even, B≥0:

Use a "base" of two reds at (1,1) and (1,2), and for each blue, insert it in the cycle. But as we saw, inserting blues is tricky.

Alternative: Build the entire path explicitly.

Let me try a different template. Consider this cycle for R=4, B=0:
(1,1)R, (1,2)R, (2,2)R, (2,1)R. Check: orth moves, (1,1)→(1,2)✓, (1,2)→(2,2)✓, (2,2)→(2,1)✓, (2,1)→(1,1)✓. 4-cycle. 

For R=4, B=1: insert a blue. 
Try: (1,1)R, (1,2)B, (2,3)B... wait, (1,2)→(2,3) is diag ✓. Then (2,3)→? Need to get back to a red that connects to (1,1). 
Let me try: cycle (1,1)R, (2,2)B, (2,1)R, (1,1)... no, (1,1) used.

Let me think of a general construction with a "spine".

Here's an idea. Make a long horizontal segment of alternating R and B, with reds every other piece, and then close the loop.

Wait, I think the cleanest construction is:

For R ≥ 2, R even:
- Make a horizontal "ladder" with R reds placed at (1,1), (1,2), ..., (1,R) — but we need the cycle structure.

Actually, let me think of it as a graph. We have a sequence of pieces p₁, p₂, ..., p_N (N=R+B) where p₁ is R, and the moves are: p_i moves to p_{i+1}. 

A well-known construction: 
Place pieces along a path and then close it. 

Let me try this construction for R even, R ≥ 2:

Case B = 0: Place reds in a cycle around a rectangle. E.g., (1,1), (1,2), ..., (1, R/2), then down, then left, then up. But simpler: just use a 4-cycle if R=4, or a 2-cycle if R=2. For general R=2k, place at (1,1), (1,2), (2,2), (2,3), (3,3), (3,4), ..., (k, k), (k, k+1), (k-1, k+1), ..., (1, k+1), (1, k). Hmm, this is getting complex.

Easier: For B=0, R=2k, just place all reds in a 2×k rectangle perimeter, traversed. Or even simpler: a "snake". 
Snake: (1,1), (1,2), (1,3), ..., (1,k), (2,k), (2,k-1), ..., (2,1), and then (2,1)→(1,1) is orth. But we need to connect (1,k)→(2,k) which is orth, and (2,1)→(1,1) which is orth. And the snake path is all orth. This works! It uses 2k positions in a 2×k grid.

For R=2, B=0: 2×1 grid: (1,1),(2,1). (1,1)→(2,1)✓, (2,1)→(1,1)✓. 

For R=4, B=0: 2×2 grid: (1,1),(1,2),(2,2),(2,1). ✓

For B > 0, R ≥ 2 even:

I think the construction is to take the snake path for the reds, and "expand" each horizontal segment by inserting blues.

Specifically, in the snake, we have horizontal moves. Between two consecutive reds that are horizontally adjacent in the cycle, we can insert any number of blues, as long as we can route them.

Wait, in the cycle, between two consecutive pieces (which could be both red or one red one blue), we can insert blues. But inserting blues changes the adjacency.

Let me think again. The cycle has R reds and B blues. Between any two consecutive pieces in the cycle, the first piece moves to the second. 

Approach: Start with a valid cycle for (R, 0) (the snake), and "expand" it by replacing some moves with paths that go through blues.

Specifically, a horizontal red move (R at (r,c) → R at (r,c+1)) can be replaced by:
R at (r,c) → B at (r+1, c+1) → B at (r, c+2) → ... → B at (r±1, c+k) → R at (r, c+k+1).
Wait, this needs the last B to be diag-adjacent to the next R, and the first B orth-adjacent to the first R.

R(r,c) → first B: orth, so B at (r±1,c) or (r,c±1).
Then B → B → ... → B (diagonal path).
Last B → R(r,c+k+1): diag, so last B at (r±1, c+k) or (r±1, c+k+2).

Hmm, let me design this carefully.

Take R(r,c) → R(r,c+1). Replace with:
R(r,c) → B(r+1, c+1) [diag? No, orth from (r,c) to (r+1,c+1) is NOT orth, it's (1,1) distance. So B must be at (r,c+1) or (r+1,c) or (r-1,c) or (r,c-1).]

(r,c+1) is the original R position, can't use (unless we move it). 
So first B at (r+1, c) or (r-1, c). Say (r+1, c).
Then diag path: (r+1, c) → (r, c+1) → (r+1, c+2) → (r, c+3) → ...
After m steps of diagonal: starts at (r+1, c). After 1 step: (r, c+1) or (r+2, c+1) or (r, c-1) or (r+2, c-1).
We want to end at a position diag-adjacent to R(r, c+k+1).
Diag-adjacent to (r, c+k+1): (r±1, c+k) or (r±1, c+k+2).

The diagonal path alternates parity. (r+1, c) has parity (r+1+c). (r, c+k+1) has parity (r+c+k+1). For a path of length m (m diagonal moves, so m+1 blues including the start? No, the first B is already at (r+1,c), and we do m more diagonal steps to reach the last B. So total blues = m+1.

After m steps from (r+1, c): the position is (r+1 + a - b, c + a + b) where a+b=m, a,b≥0. Parity of r+c+1+a-b+c+a+b = r+2c+1+2a. Mod 2: r+c+1. So all positions in the diagonal path have parity r+c+1.

The target R is at (r, c+k+1) with parity r+c+k+1. Its diagonal neighbors have parity r+c+k (since ±1,±1 changes parity). So the last B (parity r+c+1) is diag-adjacent to R (parity r+c+k+1) requires r+c+1 ≠ r+c+k+1 mod 2, i.e., k must be even. 

Wait, diag adjacency: |Δr|=1, |Δc|=1, so Δ(r+c) = ±2 or 0. So parity is SAME. So last B and R have same parity. Last B parity = r+c+1. R parity = r+c+k+1. So r+c+1 ≡ r+c+k+1 (mod 2), so k must be even.

Hmm, that's restrictive. If k is odd (the horizontal distance in the original red-red move is 1, so k=1 in the replacement... wait, I'm confusing notation).

Let me restart with clearer notation. The original red-red move is R at A → R at B, with |A-B|=1 (orth). In the snake, this is horizontal: A=(r,c), B=(r,c+1). We replace this single move with a path: R(A) → B₁ → B₂ → ... → B_t → R(B), where B₁ is orth-adjacent to A, B_t is diag-adjacent to B, and consecutive B's are diag-adjacent.

t = number of blues inserted. We want t = B (total blues) to be distributed, but actually we insert blues one at a time and can do this for multiple red-red edges.

A → B₁: orth, so B₁ at (r,c+1)=B [occupied by R(B)], or (r+1,c), or (r-1,c), or (r,c-1). 
If B₁ = (r+1, c): then diagonal path from (r+1, c) to some B_t diag-adjacent to B=(r,c+1).
Diag-adjacent to (r,c+1): (r+1,c), (r+1,c+2), (r-1,c), (r-1,c+2). Excluding B₁=(r+1,c) (if t>1), B_t ∈ {(r+1,c+2),(r-1,c),(r-1,c+2)}.

For t=1 (one blue): B₁=B_t=(r+1,c). Check B_t=(r+1,c) diag-adjacent to B=(r,c+1): |1-0|=1, |c-(c+1)|=1, yes! ✓
So for t=1: R(r,c) → B(r+1,c) → R(r,c+1). Valid!

For t=2: B₁=(r+1,c), B₂ ∈ {(r+1,c+2),(r-1,c),(r-1,c+2)}.
B₂ diag from B₁=(r+1,c): (r,c-1)inv if c=1, (r,c+1)=B, (r+2,c-1),(r+2,c+1). So (r,c+1) or (r+2,c+1) (assuming c≥2 for the other). Excluding B: (r+2,c+1).
So B₂ must be (r+2,c+1) and also in {(r+1,c+2),(r-1,c),(r-1,c+2)}. 
(r+2,c+1) vs (r+1,c+2): different. vs (r-1,c): different. vs (r-1,c+2): different. No match!

So t=2 with B₁=(r+1,c) doesn't work.

Try B₁=(r-1,c). Symmetric. B₂ diag from (r-1,c) and diag to (r,c+1).
Diag from (r-1,c): (r-2,c-1),(r-2,c+1),(r,c-1),(r,c+1)=B. Excluding B: (r-2,c-1),(r-2,c+1),(r,c-1).
Diag to (r,c+1): (r-1,c),(r-1,c+2),(r+1,c),(r+1,c+2). Excluding B₁: (r-1,c+2),(r+1,c),(r+1,c+2).
Intersection: ∅. 

So we can't easily insert 2 blues in a horizontal move with this scheme.

What about replacing a vertical move? In the snake, we have vertical moves too. Or what about replacing the "turn" in the snake?

Actually, the standard construction for this problem (I believe this is AtCoder ABC 326 F or similar... actually I think it's "Stones" or similar) is different.

Let me reconsider. I think the construction is:

For R even, R ≥ 2:
Use a "long path" that we close into a cycle. The path has specific structure.

Here's a construction I think works:

Place pieces at these positions (cycle order):
- Start with the two reds at fixed positions.
- Insert blues in a specific pattern.

Let me try a completely different approach. 

Observation: If we can make a path from R₁ to R₂ using any number of blues (and these two reds), and then close with R₂ → R₁ (orth), we have our cycle.

So we need: a path R₁ → [blues] → R₂, where:
- R₁ → first blue: orth.
- consecutive blues: diag.
- last blue → R₂: diag.
- R₂ → R₁: orth.

The number of blues in the path can be anything ≥ 0.

For R=2, B=0: path is just R₁ → R₂, with R₂→R₁ orth. So R₁, R₂ orth-adjacent. E.g., (1,1), (1,2).

For R=2, B≥1: we need to insert B blues. As shown, for B=1 it works with R₁=(1,2), B=(2,2), R₂=(2,1), and R₂→R₁=(2,1)→(1,2) orth ✓.

Wait, I had it: R₁=(1,2), B=(2,1), R₂=(2,2). Check: (1,2)R→(2,1)B: orth (1,-1)? |1|+|-1|=2, not orth. 

Let me redo R=2,B=1. Earlier I had: (1,2)R, (2,2)B, (2,1)R.
(1,2)→(2,2): orth (1,0) ✓
(2,2)→(2,1): diag (0,-1)? No, diag needs both change. (2,2)→(2,1) is orth, not diag. 

Wait, (2,2) is B, moves diag. (2,2) diag to (2,1)? No. (2,2) diag to (1,1),(1,3),(3,1),(3,3). (2,1) is not there. 

Earlier working example: (1,2)R, (2,2)B, (2,1)R? Let me recheck.
(1,2)R → (2,2)B: orth ✓
(2,2)B → (2,1)R: B moves diag from (2,2) to (2,1)? Diag move changes both coords by ±1. (2,2)→(2,1): Δr=0, Δc=-1. Not diag. ✗

So that doesn't work. Let me recheck my earlier "working" example.

Earlier I wrote: "R₁(1,2), B(2,2), R₂(2,1). R(1,2)→B(2,2) orth yes. B(2,2)→R(2,1) diag yes."

B(2,2)→R(2,1) is NOT diag. I made an error. (2,2) to (2,1) is horizontal, not diagonal. 

Let me find a valid R=2, B=1 cycle.
R(1,1), R(1,2), B(2,3)? 
(1,1)R→(1,2)R: orth ✓ [but this is R→R, and we want B in between]
Try: R(1,1), B(2,2), R(2,1).
(1,1)→(2,2): orth? (1,1) distance, no. 
R(1,1), B(1,2), R(2,3).
(1,1)→(1,2): orth ✓
(1,2)B→(2,3)R: diag (1,1) ✓
(2,3)R→(1,1)R: (2,3) to (1,1): orth? |2-1|+|3-1|=1+2=3, no.
R(1,1), B(2,1), R(2,2).
(1,1)→(2,1): orth ✓
(2,1)B→(2,2): diag? (0,1) no.
R(1,1), B(2,2), R(1,3).
(1,1)→(2,2): not orth.
R(1,1), B(1,2), R(1,1)... no.
R(1,1), B(2,2), R(3,1).
(1,1)→(2,2): not orth.
R(1,1), B(1,2), R(2,1).
(1,1)→(1,2): orth ✓
(1,2)B→(2,1)R: diag (1,-1) ✓
(2,1)R→(1,1)R: orth (-1,0) ✓ 
Cycle: (1,1)R, (1,2)B, (2,1)R. R=2, B=1. ✓

So R₂=B₁=(1,2) is blue, R₁=(1,1) is red, and the cycle is R(1,1)→B(1,2)→R(2,1)→(1,1). 
In this cycle, the two reds are R₁=(1,1) and R₃=(2,1) (orthogonally adjacent vertically). The blue is at (1,2), which is orth-adjacent to R₁=(1,1) and diag-adjacent to R₃=(2,1). 

So for R=2, B=1: R₁=(r,c), R₂=(r+1,c), B=(r,c+1). Then R₁→B orth, B→R₂ diag, R₂→R₁ orth. 

For R=2, B=2: Need a longer path. 
R₁=(r,c), then blues, then R₂ orth-adjacent to R₁.
The path R₁ → B₁ → B₂ → ... → B_B → R₂.
R₁ orth to B₁, B_B diag to R₂, consecutive B's diag, R₂ orth to R₁.

As I computed, for B=2 with R₁=(2,2), R₂=(2,3): we found B₁=(2,1), B₂=(3,2). Let's generalize.

Pattern: R₁=(1,1), R₂=(1,2) [horizontal orth]. 
B₁ at (2,1) [orth to R₁, below].
B₂ at (3,2) [diag to B₁=(2,1): (1,1) ✓, diag to R₂=(1,2): (2,0) no, (3,2) to (1,2) is (2,0), not diag. Wait (3,2) to (1,2): |3-1|=2, |2-2|=0. Not diag. So B₂=(3,2) is NOT diag-adjacent to R₂=(1,2). 

Oh, in my earlier successful example: A₁=(2,2)R, A₂=(2,1)B, A₃=(3,2)B, A₄=(2,3)R.
A₃=(3,2)→A₄=(2,3): diag (-1,1) ✓. And A₄=(2,3)→A₁=(2,2): orth (0,-1) ✓.
So R₁=(2,2), R₂=(2,3), B₁=(2,1), B₂=(3,2).
B₁=(2,1)→R₁=(2,2)? No, R₁→B₁ is the move: (2,2)R→(2,1)B: orth (0,-1) ✓.
B₂=(3,2)→R₂=(2,3): diag (-1,1) ✓.
B₁→B₂: (2,1)→(3,2): diag (1,1) ✓.

So the path is: R(2,2) → B(2,1) → B(3,2) → R(2,3) → [back to R(2,2)].

This works! Can I extend this to more blues?

Pattern: R₁=(r,c), R₂=(r,c+1). 
B₁=(r, c-1) [left of R₁, orth].
B₂=(r+1, c) [diag from B₁=(r,c-1): (1,1) ✓, diag to R₂=(r,c+1)? (r+1,c) to (r,c+1): (-1,1) ✓ diag!].
B₃=(r+1, c+1) [diag from B₂=(r+1,c): (0,1) no, diag needs both. (r+1,c)→(r+1,c+1) is orth. (r+1,c) diag: (r,c-1),(r,c+1)=R₂,(r+2,c-1),(r+2,c+1). Excluding R₂: (r,c-1)=B₁, (r+2,c-1),(r+2,c+1).]
Hmm, B₃=(r+1,c+1) is not diag from (r+1,c). 

Let me think of a zig-zag.
R₁=(r,c). 
B₁=(r+1, c) [orth down].
B₂=(r, c+1) [diag up-right from B₁].
B₃=(r+1, c+2) [diag down-right from B₂].
B₄=(r, c+3) [diag up-right from B₃].
...
After 2k blues: B_{2k} at (r, c+2k-1). 
After 2k+1 blues: B_{2k+1} at (r+1, c+2k).
R₂ must be diag-adjacent to last blue.
If B is even (B=2k), last B at (r, c+2k-1). Diag to R₂=(r,c+2k): (r, c+2k-1) to (r, c+2k): (0,1) orth, not diag. 
Diag neighbors of (r, c+2k-1): (r-1,c+2k-2),(r-1,c+2k),(r+1,c+2k-2),(r+1,c+2k). 
So R₂ could be at (r-1, c+2k) or (r+1, c+2k) or (r-1, c+2k-2) or (r+1, c+2k-2).
And R₂ must be orth-adjacent to R₁=(r,c).
R₁=(r,c), R₂ orth: (r±1,c) or (r,c±1).
If R₂=(r+1, c+2k): orth to (r,c)? |1|+|2k|=1+2k, for k≥1 this is >1. Not orth unless k=0. 
If R₂=(r, c+2k): orth to (r,c) iff 2k=1, impossible.
So this doesn't close for k≥1.

Different approach. Let me use the R₂=R₁ structure differently, or use more reds.

For R=2, B=3: Can we find one?
R₁=(1,1), R₂=(1,2) [orth].
Path: B₁→B₂→B₃, B₁ orth to R₁, B₃ diag to R₂.
B₁ at (2,1) or (0,1)inv or (1,2)=R₂ or (1,0)inv. So B₁=(2,1).
B₂ diag from (2,1) and diag to... well, B₃ diag to R₂=(1,2) and diag from B₂.
Diag to (1,2): (0,1)inv,(0,3)inv,(2,1)=B₁,(2,3). So B₃=(2,3).
B₂ diag from B₁=(2,1) and diag to B₃=(2,3). 
Diag from (2,1): (1,0)inv,(1,2)=R₂,(3,0)inv,(3,2). 
Diag to (2,3): (1,2)=R₂,(1,4)inv,(3,2),(3,4)inv.
Intersection (excluding R₂): (3,2). 
So B₂=(3,2). 
Check: B₁(2,1)→B₂(3,2): diag (1,1)✓. B₂(3,2)→B₃(2,3): diag (-1,1)✓. B₃(2,3)→R₂(1,2): diag (-1,-1)✓.
R₁(1,1)→B₁(2,1): orth (1,0)✓. R₂(1,2)→R₁(1,1): orth (0,-1)✓.
Cycle: R(1,1), B(2,1), B(3,2), B(2,3), R(1,2). ✓

Pattern: R₁=(1,1), R₂=(1,2). Blues: (2,1), (3,2), (2,3), (5,4), (4,5), (3,6), ...? Let me see.
B₁=(2,1), B₂=(3,2), B₃=(2,3). 
B₄: diag from B₃=(2,3): (1,2)=R₂,(1,4),(3,2)=B₂,(3,4). Excluding used: (1,4),(3,4).
B₄ must be diag to B₅ eventually, and we need the last B to be diag to R₂.
Hmm, for B=4: B₁(2,1), B₂(3,2), B₃(2,3), B₄. B₄ diag to R₂=(1,2): (0,1)inv,(0,3)inv,(2,1)=B₁,(2,3)=B₃. All used or invalid! So no B₄ available. 

So with R₁=(1,1), R₂=(1,2), we can have at most B=3? Let me check B=4 differently.
B₁=(2,1), B₂=(1,2)? (1,2) is R₂, can't.
What if B₁=(r,c-1) i.e. (1,0) invalid.
B₁ must be (2,1) (only orth option to (1,1) excluding (1,2)).
Then B₃=(2,3) is forced (only diag to R₂ excluding B₁ and invalid).
B₂ must connect B₁ and B₃ via diag, and be at (3,2) (only option).
B₄: must be diag from B₃=(2,3) and diag to R₂=(1,2). Diag from (2,3): (1,2)=R₂,(1,4),(3,2)=B₂,(3,4). Diag to (1,2): (0,1),(0,3),(2,1)=B₁,(2,3)=B₃. Intersection: none available.

So indeed B≤3 for this R₁,R₂ choice. But the problem says R+B can be up to 2e5, and we need to support any B. So we need a construction that works for arbitrary B with R=2, or we need to use R>2.

Ah! For large B, we should use R>2. The construction should be: R=2 works for small B, but for general B we use R≥2 and distribute blues.

Wait, R is given. We can't choose R. We need a construction for the given (R,B) with R even.

So if R=2 and B=100, we need a construction with 2 reds and 100 blues.

Hmm, but with R=2, the two reds must be orth-adjacent, and all blues are on a diagonal path between them. The diagonal path from a neighbor of R₁ to a neighbor of R₂ has limited length.

The diagonal path from B₁ (orth-adj to R₁) to B_last (diag-adj to R₂). The diagonal path has B-1 internal nodes (blues) connecting B₁ and B_last, total B blues.

B₁ is at one of 3 orth-neighbors of R₁ (excluding R₂). B_last is at one of 4 diag-neighbors of R₂. The diagonal path between them has length at most... well, it can be arbitrarily long if we go far away.

But the path is a sequence of diagonal moves, which is like a king's move. The distance (in diagonal steps) between B₁ and B_last is |Δr|+|Δc|? No, diagonal step changes both by ±1, so it's like Chebyshev distance. Actually, after m diagonal steps, the max |Δr| or |Δc| is m.

But here's the constraint: the path must not revisit squares (at most one piece per square). So we need a simple path.

The diagonal graph on a grid: two squares are connected if they differ by (±1,±1). This is bipartite? Let's see: (r,c) and (r+1,c+1) have (r+c) and (r+c+2), same parity. So all squares of same parity are connected, and we can traverse them in a path.

The diagonal graph on same-parity squares: from (r,c) we can reach any (r',c') with r'-r and c'-c same parity and r'≡c' (mod 2)... actually r'+c' ≡ r+c (mod 2) is automatic for same parity. The graph is connected: from (r,c) we can reach (r+1,c+1), (r+1,c-1), etc. After 2 steps: (r,c)→(r+1,c+1)→(r+2,c) or (r,c+2) or (r,c) or (r+2,c+2). So we can move by (2,0), (0,2), (2,2), (0,0). So the graph is connected and we can make long paths.

But B₁ must be orth-adj to R₁ and have a specific parity (opposite to R₁), and B_last diag-adj to R₂ (same parity as R₂ = opposite to R₁). And R₂ orth-adj to R₁.

So: R₁ and R₂ orth-adj, opposite parity. B₁ orth-adj R₁, so B₁ has parity opposite to R₁ = same as R₂. B_last diag-adj R₂, so B_last has parity same as R₂. So both B₁ and B_last have parity = R₂'s parity. The diagonal path stays on this parity. 

The diagonal graph on squares of parity p: two squares (r,c) and (r',c') with r+c≡r'+c'≡p (mod 2) are connected by a diagonal path iff... well the graph is connected. Distance: min diagonal steps to connect them. Each step changes r and c by ±1, so after m steps, |r-r'|≤m, |c-c'|≤m, and m ≡ |r-r'| (mod 2)? Actually r' = r + Σε_i, c' = c + Σδ_i, |ε_i|=|δ_i|=1. So r'-r and c'-c have the same parity as m? r'-r = (# +1) - (# -1), and total steps m = (#+1)+(#-1). So r'-r ≡ m (mod 2) and c'-c ≡ m (mod 2). So |r-r'| and |c-c'| have the same parity as m. Thus m must be ≡ |r-r'| ≡ |c-c'| (mod 2). Also m ≥ max(|r-r'|,|c-c'|) and m ≡ max(|r-r'|,|c-c'|) (mod 2)? Actually m ≥ max(|r-r'|,|c-c'|) and m ≡ |r-r'| (mod 2).

OK so for R=2, given R₁ and R₂ orth-adj, and B₁ orth-adj R₁ (3 choices, excluding R₂), and B_last diag-adj R₂ (4 choices), we need a diagonal path from B₁ to B_last of length B-1 (using B-1 more blues) that doesn't hit any used square and stays in bounds (1..1e9).

Can we always do this? We need the path to have exactly B-1 steps (using B blues total including endpoints... wait, B₁ and B_last are 2 of the B blues, and there are B-2 internal blues, so B-1 steps total in the path B₁→...→B_last).

For B=1: path is just B₁=B_last, so B₁ must be diag-adj to R₂. 
R₁=(1,1), R₂=(1,2). B₁ orth-adj R₁: (2,1),(1,0)inv,(1,2)=R₂,(1,0)... (2,1),(0,1)inv. So B₁=(2,1). Is (2,1) diag-adj R₂=(1,2)? |2-1|=1,|1-2|=1. Yes! So B=1 works with B₁=(2,1)=B_last.

For B=2: B₁=(2,1), B_last diag-adj R₂=(1,2): (0,1)inv,(0,3)inv,(2,1)=B₁,(2,3). So B_last=(2,3). Path B₁→B_last: (2,1)→(2,3)? Not diag (differs by (0,2)). Distance: need m diag steps with m≥max(0,2)=2 and m≡0≡2(mod 2). m=2. Path: (2,1)→(3,2)→(2,3) or (2,1)→(1,2)→(2,3) but (1,2)=R₂. So (2,1)→(3,2)→(2,3). ✓ (This is what I found.)

For B=3: B₁=(2,1), B_last=(2,3) [forced for the choices, but actually we had B_last could be (2,3) only since (2,1) is B₁]. Wait diag-adj to (1,2) is 4 squares, and excluding B₁=(2,1) and invalid, we have (2,3). So B_last=(2,3) is forced. Then path (2,1)→?→?→(2,3) with 3 steps. m=3, |Δr|=0,|Δc|=2, need m≥2, m≡0(mod 2)? But m=3 is odd, and |Δr|=0 (even). Contradiction: 3 ≡ 0 (mod 2) is false. So no path of length 3? But I found one earlier: (2,1)→(3,2)→(2,3) is 2 steps (B=3 means 3 blues, 2 steps in path between first and last). 

Oh, B=3 blues: B₁, B₂, B₃. Path B₁→B₂→B₃, 2 steps. B_last=B₃. 
For B=3: B_last=(2,3), path length 2 from (2,1) to (2,3): (2,1)→(3,2)→(2,3). ✓ (2 steps, m=2, |Δr|=0,|Δc|=2, m=2≥2, 2≡0(mod 2) ✓).

For B=4: 4 blues, path B₁→B₂→B₃→B₄, 3 steps. B_last=(2,3) [forced], B₁=(2,1). 3 steps from (2,1) to (2,3): m=3, need |Δr|≤3,|Δc|≤3, m≡|Δr|(mod 2), m≡|Δc|(mod 2). (2,3)-(2,1)=(0,2). m=3, |Δr|=0≡0≠3(mod 2). Impossible! 

So with R₁=(1,1), R₂=(1,2), B₁=(2,1), we cannot have B=4. 

Can we choose different B₁? Only B₁=(2,1) is available (orth-adj to (1,1) excluding (1,2) and invalid). So R₁=(1,1), R₂=(1,2) gives at most B=3.

What if R₁=(1,1), R₂=(2,1) [vertical]?
B₁ orth-adj R₁ excluding R₂: (0,1)inv,(1,2),(1,0)inv,(2,1)=R₂. So B₁=(1,2).
B_last diag-adj R₂=(2,1): (1,0)inv,(1,2)=B₁,(3,0)inv,(3,2). Excluding B₁: (3,2). So B_last=(3,2).
Path (1,2)→...(1,2) to (3,2): Δ=(2,0). m steps, m≥2, m≡0(mod 2). 
B=2: m=1, 1<2. Impossible? But |Δr|=2, need m≥2. m=1: |Δr|≤1, but 2>1. So B=2 impossible with this choice.
B=3: m=2. Path (1,2)→(2,3)→(3,2) or (1,2)→(2,1)=R₂→(3,2) but R₂ used. (1,2)→(2,3)→(3,2). Check (1,2)→(2,3): diag (1,1)✓. (2,3)→(3,2): diag (1,-1)✓. But wait, is (2,3) free? Yes. And B_last=(3,2) diag to R₂=(2,1): (1,1)✓. 
B=3: (1,2),(2,3),(3,2). ✓
B=4: m=3, (1,2) to (3,2): |Δr|=2, m=3, 3≡1(mod 2), |Δr|=2≡0(mod 2). 1≠0. Impossible.
B=5: m=4. (1,2)→(2,3)→(3,2)→(2,1)=R₂ no, or (1,2)→(2,3)→(1,4)→(2,5)→(3,4) hmm need to end at (3,2). 
Actually, let me reconsider. The path from (1,2) to (3,2) with 4 steps. (1,2)→(2,3)→(3,2)→(2,1)→(3,2) but (2,1) is R₂ and (3,2) is endpoint. 
(1,2)→(2,3)→(3,4)→(2,3) no revisit. 
(1,2)→(2,1)=R₂ can't.
This is getting complicated. Let me just accept that for R=2, B is limited (up to 3 or 4 with careful choice).

For the problem, we need a construction for any R≥2 even, B≥0. The construction should be general.

Here's the key insight: with R≥4 even, we have more flexibility. And the standard solution uses a construction that works for all R≥2 even, B≥0.

Let me recall: I think the construction is as follows (for R ≥ 2, R even, B ≥ 0):

Use a "long cycle" with structure:
- Start at (1,1) with R.
- Go right with R, R, ..., R (along the top).
- Turn down, go right with B, B, ..., B.
- Etc.

Actually, I found a reference in my memory. The construction is:

For R = 2, B ≥ 0: impossible for large B? No, the problem says R+B ≤ 2e5 and we need to handle all.

Wait, I showed R=2, B=4 is impossible with the simple R₁=(1,1), R₂=(1,2) and B₁=(2,1). But maybe with different R₁, R₂ positions and B₁ choice we can get larger B.

R₁=(r,c), R₂=(r,c+1). B₁ orth-adj R₁, not R₂: must be (r+1,c) or (r-1,c) (since (r,c+1)=R₂, (r,c-1) is fine too). Oh! (r,c-1) is orth-adj to R₁ and not equal to R₂. So B₁ ∈ {(r+1,c),(r-1,c),(r,c-1)}.

Let me try R₁=(2,2), R₂=(2,3). B₁=(2,1).
B_last diag-adj R₂=(2,3): (1,2),(1,4),(3,2),(3,4). 
For B=4: B₁=(2,1), B_last must be reachable in 3 steps. (2,1) to (1,2): ( -1,1) m=1. m=3, |Δr|≤3,|Δc|≤3, m≡|Δr|(mod 2). (1,2)-(2,1)=(-1,1). m=3, |Δr|=1≡1, 3≡1 ✓. |Δc|=1≡1 ✓. m≥max(1,1)=1 ✓. So possible! Path (2,1)→(1,2)→(2,3)=R₂ no. (2,1)→(1,2)→(0,3)→(1,4)=B_last. Check: (2,1)→(1,2)diag✓, (1,2)→(0,3)diag(-1,1)✓, (0,3)→(1