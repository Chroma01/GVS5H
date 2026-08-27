We need to arrange R red pieces (Manhattan moves) and B blue pieces (diagonal moves) into a directed cycle where each consecutive piece (including last→first) can reach the next in one move. The board is huge (1e9×1e9), so we can place pieces anywhere.

Key observations:
- Red pieces can only move along same row/column (Manhattan distance 1).
- Blue pieces can only move diagonally (Chebyshev distance 1 with opposite parity).
- A red piece can reach a blue piece in one move iff they share a row or column and are adjacent (distance 1).
- A blue piece can reach a red piece in one move iff they are diagonally adjacent (|Δr|=|Δc|=1).
- Two blue pieces can reach each other in one move iff they are diagonally adjacent.
- Two red pieces can reach each other in one move iff they are orthogonally adjacent.

We need to construct a cycle. The simplest construction is to alternate red and blue pieces around a small rectangle. For example, place pieces around a 2×3 or 3×3 rectangle.

General construction:
- If R ≥ 1 and B ≥ 1: Place pieces in a cycle alternating R and B around a small pattern. We can use a 2×3 rectangle: corners and edges.
  - Pattern: B at (1,1), R at (1,2), B at (1,3), R at (2,3), B at (2,2), R at (2,1) — this forms a cycle of length 6 with alternating colors.
  - But we need exactly R reds and B blues. We can repeat the pattern or adjust.

Better approach: Use a cycle that goes around a rectangle. For any R,B ≥ 1, we can construct as follows:
- Place all blue pieces in a row, then all red pieces in a column, forming a cycle.
- Actually, we can use a "staircase" pattern.

Simpler known solution:
- If R == 0 or B == 0: Only possible if R+B ≥ 4 and we can form a cycle with same-color pieces.
  - Red-only: Need a cycle of orthogonal moves. Minimum cycle length 4 (a square). So if R ≥ 4, place a square. If R < 4, impossible.
  - Blue-only: Need a cycle of diagonal moves. Minimum cycle length 4 (a diamond shape). So if B ≥ 4, place a diamond. If B < 4, impossible.
- If R ≥ 1 and B ≥ 1: Always possible? Let's check.
  - We can place pieces in a cycle alternating colors. For example, a cycle of length R+B alternating R and B.
  - We need to ensure adjacency constraints: R→B requires same row/col adjacent; B→R requires diagonal adjacent.
  - We can construct a zigzag pattern.

Standard solution for this problem (from AtCoder ABC/ARC):
- If R == 0 and B == 0: impossible (but R+B ≥ 2).
- If R == 0: Only blue pieces. Blue moves diagonally. A cycle of blue pieces requires even length ≥ 4. So if B ≥ 4, possible; else impossible.
- If B == 0: Only red pieces. Red moves orthogonally. A cycle of red pieces requires length ≥ 4. So if R ≥ 4, possible; else impossible.
- If R ≥ 1 and B ≥ 1: Always possible. Construction:
  - Place pieces in a cycle that alternates between red and blue as much as possible.
  - One known construction: Use a 2×(R+B) grid or similar.

Actually, looking at the sample:
- R=2, B=3: Output has 5 pieces. The pattern shown is:
  B at (2,3), R at (3,2), B at (2,2), B at (3,3), R at (2,4)
  Wait, that's not alternating. Let's trace the cycle:
  1: B(2,3) → 2: R(3,2) [diagonal? (2,3) to (3,2): Δr=1, Δc=-1, yes diagonal]
  2: R(3,2) → 3: B(2,2) [orthogonal? (3,2) to (2,2): Δr=-1, Δc=0, yes]
  3: B(2,2) → 4: B(3,3) [diagonal? (2,2) to (3,3): Δr=1, Δc=1, yes]
  4: B(3,3) → 5: R(2,4) [diagonal? (3,3) to (2,4): Δr=-1, Δc=1, yes]
  5: R(2,4) → 1: B(2,3) [orthogonal? (2,4) to (2,3): Δr=0, Δc=-1, yes]
  So the cycle is B-R-B-B-R. Not strictly alternating.

General construction idea:
- We can place all blue pieces in a diagonal line, and red pieces connecting them.
- Or use a "comb" pattern.

A robust construction:
- Place pieces in a cycle that goes around a rectangle.
- For R ≥ 1, B ≥ 1:
  - Place one red piece at (1,1).
  - Place blue pieces in a diagonal chain from (1,2) to (B, B+1) or similar.
  - Place remaining red pieces in a column.

Actually, a simpler universal construction for R≥1, B≥1:
- Use a 2×N grid where N = R+B.
- Place pieces in a cycle that goes: right along top row, down, left along bottom row, up.
- But we need to assign colors such that moves are valid.

Let's think differently. We can construct a cycle of length R+B as follows:
- If we have at least one red and one blue, we can make a cycle that alternates colors as much as possible.
- The only problematic case is when one color has many pieces and the other has few.

Known solution from similar problems (e.g., AtCoder Grand Contest):
- If R == 0:
  - If B >= 4: place blue pieces in a 2×2 diamond: (1,2), (2,1), (3,2), (2,3) — cycle of 4. For more, extend.
  - Else: No.
- If B == 0:
  - If R >= 4: place red pieces in a square: (1,1), (1,2), (2,2), (2,1) — cycle of 4. For more, extend.
  - Else: No.
- If R >= 1 and B >= 1:
  - Always Yes.
  - Construction: Place pieces in a cycle that goes around a rectangle of size 2 × (R+B) or similar.
  - One method: Place all pieces in a single row or column with appropriate spacing? No, moves are only distance 1.

Let's design a concrete construction for R≥1, B≥1:
- We want a cycle of length N = R+B.
- We can use a "zigzag" pattern:
  - Start at (1,1) with a red piece.
  - Go right to (1,2) with blue? But blue can't move horizontally.
  - So we need to alternate between horizontal/vertical (red) and diagonal (blue).

Pattern: R moves orthogonally, B moves diagonally.
- If we have a sequence: R, B, R, B, ...
- R→B: need orthogonal adjacency.
- B→R: need diagonal adjacency.
- So if we place R at (r,c), then B must be at (r±1, c) or (r, c±1).
- Then from B at (r±1, c), R must be at (r±1±1, c±1) or (r±1, c±1) — diagonal from B.
- This suggests a staircase pattern.

Example staircase:
- R at (1,1)
- B at (1,2) [right of R]
- R at (2,3) [diagonal from B: (1,2)→(2,3) is diagonal]
- B at (2,4) [right of R]
- R at (3,5) [diagonal]
- ...
- This goes up and right. To close the cycle, we need to come back.

We can make a cycle that goes around a rectangle:
- Top edge: alternating R and B moving right.
- Right edge: moving down.
- Bottom edge: moving left.
- Left edge: moving up.

But we need to assign colors to satisfy move types.

Alternative: Use a cycle of length 4 as a building block.
- Basic 4-cycle: R(1,1) → B(1,2) → R(2,2) → B(2,1) → R(1,1)
  - R(1,1)→B(1,2): orthogonal (right)
  - B(1,2)→R(2,2): diagonal (down-right? (1,2)→(2,2) is Δr=1, Δc=0, not diagonal. Wait, diagonal means both coordinates change by ±1. So (1,2)→(2,2) is not diagonal.
  - So that doesn't work.

Let's check valid 4-cycle with R and B:
- R(1,1) → B(2,2) [diagonal? No, R can't move diagonally. R moves orthogonally.]
- So R→B must be orthogonal.
- B→R must be diagonal.

Valid 4-cycle:
- R(1,1) → B(1,2) [orthogonal right]
- B(1,2) → R(2,1) [diagonal down-left: (1,2)→(2,1) is Δr=1, Δc=-1, yes]
- R(2,1) → B(2,2) [orthogonal right]
- B(2,2) → R(1,1) [diagonal up-left: (2,2)→(1,1) is Δr=-1, Δc=-1, yes]
- Cycle: R(1,1) → B(1,2) → R(2,1) → B(2,2) → R(1,1)
- This uses 2 reds and 2 blues.

We can chain such 4-cycles or extend.

General construction for R≥1, B≥1:
- Place pieces in a cycle that goes around a 2×k rectangle.
- For k = R+B, we can place:
  - Top row: alternating R and B from left to right.
  - Right column: going down.
  - Bottom row: going left.
  - Left column: going up.
- But we need to ensure move validity at corners.

Let's try to construct a cycle for any R,B ≥ 1:
- We can use a "spiral" or "snake" pattern.
- Actually, a simple construction:
  - Place all blue pieces in a diagonal line: (1,1), (2,2), ..., (B,B).
  - Place red pieces to connect them in a cycle.
  - Connect (1,1) to (2,2) via red? No, red can't move diagonally.

Another idea: Use a cycle that goes:
- Start at (1,1) with Red.
- Move right to (1,2) with Blue.
- Move diagonally down-right to (2,3) with Red.
- Move right to (2,4) with Blue.
- ...
- Eventually, we need to close the loop.

We can make a cycle that goes around a rectangle of width W and height H.
- The perimeter has 2*(W+H) - 4 squares.
- We can assign colors to perimeter squares such that adjacent squares have valid moves.

Let's try a 2×3 rectangle (perimeter 6 squares):
- (1,1), (1,2), (1,3), (2,3), (2,2), (2,1)
- Assign colors: B, R, B, R, B, R? Let's check:
  - B(1,1) → R(1,2): orthogonal? B can't move orthogonally. B moves diagonally. So B→R must be diagonal.
  - So if we have B then R, they must be diagonally adjacent.
  - If we have R then B, they must be orthogonally adjacent.

So the sequence of colors around the cycle must satisfy:
- R followed by B: orthogonal adjacency.
- B followed by R: diagonal adjacency.
- R followed by R: orthogonal adjacency.
- B followed by B: diagonal adjacency.

So we can have runs of same color with appropriate adjacency.

For the 2×3 perimeter:
- (1,1) to (1,2): horizontal adjacent.
- (1,2) to (1,3): horizontal adjacent.
- (1,3) to (2,3): vertical adjacent.
- (2,3) to (2,2): horizontal adjacent.
- (2,2) to (2,1): horizontal adjacent.
- (2,1) to (1,1): vertical adjacent.

All adjacent pairs on this perimeter are orthogonally adjacent (distance 1 in Manhattan).
- So if we have two pieces on adjacent perimeter squares, they are orthogonally adjacent.
- This means if we have R→R, it's fine (orthogonal).
- But B→B requires diagonal adjacency, so two blues cannot be on orthogonally adjacent squares.
- So on this perimeter, we cannot have two consecutive blues.
- Also, B→R requires diagonal adjacency, so if B is followed by R, they must be diagonally adjacent, not orthogonally adjacent.
- So on this perimeter, B cannot be followed by R either (unless they are also diagonally adjacent, but perimeter squares are only orthogonally adjacent to their neighbors).

So the 2×3 perimeter doesn't work well for mixing colors.

We need a cycle where some adjacent pairs are diagonal and some are orthogonal.
- This happens if we use a "knight's move" pattern or a zigzag.

Consider a zigzag cycle:
- (1,1) → (1,2) → (2,3) → (2,4) → (3,5) → ...
- Here, (1,1)→(1,2) is orthogonal.
- (1,2)→(2,3) is diagonal.
- (2,3)→(2,4) is orthogonal.
- (2,4)→(3,5) is diagonal.
- So we alternate between orthogonal and diagonal moves.
- This means we alternate between R/B and B/R? Let's see:
  - If move 1 is orthogonal, piece 1 could be R and piece 2 could be B (R→B orthogonal).
  - If move 2 is diagonal, piece 2 is B and piece 3 is R (B→R diagonal).
  - So the sequence is R, B, R, B, ...
- So if we alternate orthogonal and diagonal moves, we get alternating R and B.
- This requires R and B to be equal or differ by 1.

If R != B, we need to handle the extra pieces.
- If R > B: we have more reds. We can have two reds in a row (orthogonal move between them).
- If B > R: we have more blues. We can have two blues in a row (diagonal move between them).

Construction for R ≥ 1, B ≥ 1:
- We can build a cycle that goes in a zigzag and then closes.
- One robust method:
  - Place all blue pieces in a diagonal chain.
  - Connect them with red pieces.

Let's design a specific construction:
- Case 1: R >= 2 and B >= 1.
  - We can make a cycle: R, B, R, R, B, R, R, ..., B, R
  - Or use a "comb" shape.

Actually, I recall a solution:
- If R == 0:
  - If B >= 4: Yes, place in a 2×2 diamond pattern, then extend.
  - Else: No.
- If B == 0:
  - If R >= 4: Yes, place in a square, then extend.
  - Else: No.
- If R >= 1 and B >= 1:
  - Yes.
  - Construction:
    - Place one red at (1,1).
    - Place blues in a diagonal line from (1,2) to (B, B+1).
    - Place remaining reds in a vertical line at column B+2 from row 1 to row R-1.
    - Connect back to start.
  - Let's verify this construction.

Construction details:
- Start: R at (1,1).
- Then B at (1,2) [orthogonal right].
- Then B at (2,3) [diagonal from (1,2): (1,2)→(2,3) is Δr=1, Δc=1, yes].
- Then B at (3,4) [diagonal from (2,3)].
- ...
- Then B at (B, B+1) [diagonal from previous].
- Now we need to place R-1 more reds.
- Place R at (1, B+2) [diagonal from (B, B+1)? (B, B+1)→(1, B+2) is not adjacent unless B=1. So no.]

Let's try a different construction.
- Place pieces in a cycle that goes around a 2×N rectangle but with some diagonals.
- Actually, we can use a cycle that goes:
  - Right along top row (orthogonal moves).
  - Diagonally down to next row.
  - Left along bottom row (orthogonal moves).
  - Diagonally up to top row.
- This creates a cycle with orthogonal segments and diagonal connections.

Example for R=2, B=3 (sample):
- They used: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4)
- Let's see the pattern:
  - B(2,3) → R(3,2): diagonal
  - R(3,2) → B(2,2): orthogonal (up)
  - B(2,2) → B(3,3): diagonal
  - B(3,3) → R(2,4): diagonal
  - R(2,4) → B(2,3): orthogonal (left)
- So the cycle has: B-R-B-B-R
- Moves: diag, orth, diag, diag, orth.

Generalizing:
- We can make a cycle with a "core" of blues connected diagonally, and reds inserted orthogonally.

A known construction for R≥1, B≥1:
- If R == 1 and B == 1: Place R at (1,1), B at (1,2). Then R→B is orthogonal, but B→R? (1,2)→(1,1) is orthogonal, not diagonal. So B cannot reach R. So R=1, B=1 is impossible? Wait, sample says 1 1 is No. Yes.
- So R=1, B=1 is impossible.
- R=1, B>=2: ?
- R>=2, B=1: ?

Let's check small cases:
- R=1, B=1: No (sample).
- R=1, B=2: ?
  - Need cycle of 3 pieces: R, B, B.
  - R→B: orthogonal.
  - B→B: diagonal.
  - B→R: diagonal.
  - So: R at (1,1), B at (1,2) [orth], B at (2,3) [diag from (1,2)], then B(2,3)→R(1,1)? (2,3) to (1,1) is not adjacent. So no.
  - Try: R(1,1), B(2,2) [diag? R can't move diag]. So R→B must be orth.
  - R(1,1) → B(1,2) [orth].
  - B(1,2) → B(2,1) [diag: (1,2)→(2,1) is Δr=1, Δc=-1, yes].
  - B(2,1) → R(1,1) [diag: (2,1)→(1,1) is Δr=-1, Δc=0, not diag. (2,1)→(1,1) is orth, but B→R must be diag]. So no.
  - Try: R(1,1) → B(2,1) [orth down].
  - B(2,1) → B(1,2) [diag: (2,1)→(1,2) is Δr=-1, Δc=1, yes].
  - B(1,2) → R(1,1) [diag: (1,2)→(1,1) is orth, not diag]. No.
  - So R=1, B=2 might be impossible.
- R=2, B=1:
  - Cycle: R, R, B.
  - R→R: orth.
  - R→B: orth.
  - B→R: diag.
  - R(1,1) → R(1,2) [orth].
  - R(1,2) → B(2,2) [orth down].
  - B(2,2) → R(1,1) [diag: (2,2)→(1,1) is Δr=-1, Δc=-1, yes].
  - So R=2, B=1 is possible!
- R=2, B=2:
  - R(1,1) → B(1,2) [orth].
  - B(1,2) → R(2,1) [diag].
  - R(2,1) → B(2,2) [orth].
  - B(2,2) → R(1,1) [diag].
  - Possible.
- R=1, B=3:
  - Cycle: R, B, B, B.
  - R→B: orth.
  - B→B: diag.
  - B→R: diag.
  - R(1,1) → B(1,2) [orth].
  - B(1,2) → B(2,3) [diag].
  - B(2,3) → B(3,2) [diag: (2,3)→(3,2) is Δr=1, Δc=-1, yes].
  - B(3,2) → R(1,1)? (3,2)→(1,1) is not adjacent. No.
  - Try different: R(1,1) → B(2,1) [orth].
  - B(2,1) → B(1,2) [diag].
  - B(1,2) → B(2,3) [diag].
  - B(2,3) → R(1,1)? (2,3)→(1,1) no.
  - So R=1, B=3 might be impossible.

So the condition is not just R>=1 and B>=1.
- R=1, B=1: No.
- R=1, B=2: ?
- R=2, B=1: Yes.
- R=1, B=3: ?

Let's think about parity or connectivity.
- The moves form a bipartite graph? No.
- Actually, consider the parity of (r+c).
  - Red move: changes r or c by 1, so changes (r+c) parity.
  - Blue move: changes both r and c by ±1, so changes (r+c) by 0 or ±2. So (r+c) parity is preserved.
- So:
  - Red piece: moves to opposite parity.
  - Blue piece: moves to same parity.
- In the cycle, each piece must be able to reach the next.
- So if piece i is Red, piece i+1 must be on opposite parity.
- If piece i is Blue, piece i+1 must be on same parity.
- This means:
  - R → B: R is on parity p, B must be on parity 1-p.
  - B → R: B is on parity p, R must be on parity p (since B preserves parity, R must be on same parity as B).
  - R → R: R is on parity p, next R must be on parity 1-p.
  - B → B: B is on parity p, next B must be on parity p.
- So in the cycle:
  - Between R and B: R→B flips parity, B→R preserves parity.
  - So if we have ... R, B ... then R is on parity p, B is on parity 1-p.
  - Then B → R: B is on 1-p, R must be on 1-p.
  - So we have R(p), B(1-p), R(1-p).
  - Then R → B: R(1-p) → B(p).
  - So the pattern of parities for R,B,R,B,... is: p, 1-p, 1-p, p, p, 1-p, ...
  - Actually: R(p), B(1-p), R(1-p), B(p), R(p), B(1-p), ...
  - So reds alternate parity, blues alternate parity, and they are offset.

This parity constraint might restrict some cases.
- For R=1, B=1: Cycle is R, B.
  - R(p), B(1-p).
  - Then B→R: B(1-p) → R must be on 1-p.
  - But we only have one R, which is on p. Contradiction unless p = 1-p, impossible.
  - So R=1, B=1 is impossible. Matches sample.
- For R=1, B=2: Cycle is R, B, B.
  - R(p), B(1-p), B(1-p) [since B→B preserves parity].
  - Then B→R: B(1-p) → R must be on 1-p.
  - But R is on p. Contradiction.
  - So R=1, B=2 is impossible.
- For R=2, B=1: Cycle is R, R, B.
  - R(p), R(1-p) [R→R flips], B(p) [R→B flips: R(1-p)→B(p)].
  - Then B→R: B(p) → R must be on p.
  - But we have R on p and R on 1-p. So we can choose the one on p.
  - So possible if we arrange correctly.
  - We found a construction earlier. So R=2, B=1 is possible.
- For R=1, B=3: Cycle is R, B, B, B.
  - R(p), B(1-p), B(1-p), B(1-p).
  - B→R: B(1-p) → R must be on 1-p. But R is on p. Contradiction.
  - So R=1, B=3 is impossible.
- For R=1, B=4: Cycle is R, B, B, B, B.
  - R(p), B(1-p), B(1-p), B(1-p), B(1-p).
  - B→R: B(1-p) → R must be on 1-p. Contradiction.
  - So R=1, B>=2 is impossible? Wait, what about R=1, B=4?
  - Let's check: R(p), then B(1-p), B(1-p), B(1-p), B(1-p).
  - Last B is on 1-p. It must reach R on p. But B→R requires same parity. So impossible.
  - So R=1, B>=2 is impossible.
- Similarly, R=2, B=1 is possible.
- R=3, B=1: Cycle R,R,R,B.
  - R(p), R(1-p), R(p), B(1-p) [R→B flips].
  - B→R: B(1-p) → R must be on 1-p. We have R on p and 1-p. So we can use the one on 1-p.
  - So possible.
- R=1, B=1: impossible.
- R=1, B>=2: impossible.
- R>=2, B=1: possible? Let's check R=2, B=1: yes. R=3, B=1: yes.
- R=2, B=2: possible.
- R=2, B=3: possible (sample).
- R=1, B=0: R=1, B=0 means only red. Cycle of reds: R→R flips parity. So cycle must have even length to return to start parity. So R must be even and >=4. So R=1,2,3 impossible. R=4 possible.
- R=0, B=1: only blue. B→B preserves parity. So cycle can be any length >=4? Actually, B→B preserves parity, so all blues must be on same parity. And we need a cycle. Minimum cycle for blue is 4 (diamond). So B>=4 possible, B=1,2,3 impossible.

Summary of conditions:
- If R == 0:
  - B >= 4: Yes.
  - Else: No.
- If B == 0:
  - R >= 4: Yes.
  - Else: No.
- If R >= 1 and B >= 1:
  - If R == 1 and B == 1: No.
  - If R == 1 and B >= 2: No.
  - If R >= 2 and B == 1: Yes.
  - If R >= 2 and B >= 2: Yes.

Wait, is R=2, B=1 always yes? Yes, we constructed it.
Is R=1, B=2 always no? Yes, parity argument.
Is R=1, B=3 no? Yes.
So the only impossible cases with both colors present are:
- R=1, B=1
- R=1, B>=2 (i.e., R=1, B>=1 except B=0, but B=0 is separate case)
Actually, R=1, B=1 is covered by R=1, B>=1.
So: If R==1 and B>=1: No.
If B==1 and R>=2: Yes.
If R>=2 and B>=2: Yes.

Let's verify with sample:
- 2 3: R=2>=2, B=3>=2: Yes.
- 1 1: R=1, B=1: No.
- 4 0: B=0, R=4>=4: Yes.

Matches sample.

Now we need to construct placements for all "Yes" cases.

Construction methods:

Case 1: R == 0, B >= 4.
- Place blue pieces in a cycle of diagonal moves.
- Simple cycle: (1,2), (2,1), (3,2), (2,3) — that's 4 pieces.
- For more, we can extend by adding more pieces in a "staircase" or larger diamond.
- Actually, we can place them in a cycle that goes around a rectangle diagonally.
- Or simply: place B pieces in a cycle where each is diagonally adjacent to next.
- One construction: Place them in a 2×k grid? No, diagonal moves.
- We can place them in a single diagonal line and connect the ends with a detour.
- Or use a "zigzag" of diagonals.
- Simple: For B pieces, place them at:
  - (1,2), (2,3), (3,4), ..., (B-1, B), (B, B-1), (B-1, B-2), ..., (2,1)
  - This goes diagonally down-right then diagonally up-left.
  - Check adjacency:
    - (i, i+1) to (i+1, i+2): diagonal (Δr=1, Δc=1).
    - (i+1, i+2) to (i+2, i+1): diagonal (Δr=1, Δc=-1).
    - ...
    - Last: (2,1) to (1,2): diagonal (Δr=-1, Δc=1).
  - This works for B >= 2? Let's check B=4:
    - (1,2), (2,3), (3,2), (2,1)
    - (1,2)→(2,3): diag.
    - (2,3)→(3,2): diag.
    - (3,2)→(2,1): diag.
    - (2,1)→(1,2): diag.
  - Works for B=4.
  - For B=5:
    - (1,2), (2,3), (3,4), (4,3), (3,2)
    - (3,4)→(4,3): diag.
    - (4,3)→(3,2): diag.
    - (3,2)→(1,2)? No, we need to close to (1,2).
    - (3,2) to (1,2) is not adjacent.
  - So we need to adjust.
  - Better: Use a cycle that goes around a diamond shape.
  - For B=4: (1,2), (2,3), (3,2), (2,1).
  - For B=5: Add one more. We can make a larger diamond.
  - Or use a "staircase" that goes up and down.
  - Actually, we can use a cycle that goes:
    - (1,2), (2,3), (3,4), ..., (k, k+1), then turn back: (k+1, k), (k, k-1), ..., (2,1), then back to (1,2).
    - This requires the turn at (k, k+1) to (k+1, k) to be diagonal: (k, k+1)→(k+1, k) is Δr=1, Δc=-1, yes.
    - And (2,1)→(1,2) is Δr=-1, Δc=1, yes.
    - So for any B >= 4, we can choose k = B-2? Let's see:
      - Sequence: (1,2), (2,3), ..., (k, k+1), (k+1, k), (k, k-1), ..., (2,1).
      - Number of pieces: k (from (1,2) to (k,k+1)) + k-1 (from (k+1,k) to (2,1)) = 2k-1.
      - We need 2k-1 = B, so k = (B+1)/2.
      - This works if B is odd.
      - If B is even, we can adjust.
    - For B=4: k=2.5? No.
    - Alternative: Use a cycle that goes around a 2×2 square but with diagonal moves? No, diagonal moves don't stay on a square.
    - For B=4: (1,2), (2,3), (3,2), (2,1) — this is a diamond of size 2.
    - For B=6: We can make a larger diamond or two diamonds connected.
    - Actually, we can place them in a cycle that goes:
      - (1,2), (2,3), (3,4), (4,3), (3,2), (2,1) — that's 6 pieces.
      - Check: (4,3)→(3,2): diag. (3,2)→(2,1): diag. (2,1)→(1,2): diag.
      - Yes! This is a hexagon.
    - For B=5: (1,2), (2,3), (3,4), (4,3), (3,2) — that's 5 pieces.
      - (3,2)→(1,2)? No.
      - We need to close the loop.
      - (1,2), (2,3), (3,2), (2,1), (1,2)? That's 4 unique.
      - For 5, we can do: (1,2), (2,3), (3,4), (4,3), (3,2), (2,1) is 6.
      - For 5: (1,2), (2,3), (3,4), (4,5), (5,4), (4,3), (3,2), (2,1) is 8.
      - We need exactly 5.
      - Maybe: (1,2), (2,3), (3,2), (2,1), (1,0)? No, column must be >=1.
      - Or: (2,1), (1,2), (2,3), (3,2), (2,1) — that's a cycle of 4, but we need 5.
      - We can add a "spike": (1,2), (2,3), (3,4), (4,3), (3,2), (2,1) is 6.
      - For 5: (1,2), (2,3), (3,4), (4,3), (3,2) — last to first: (3,2) to (1,2) not adjacent.
      - So we need to adjust the shape.
      - Actually, we can use a cycle that goes around a rectangle:
        - (1,2), (2,3), (3,4), (4,5), (5,4), (4,3), (3,2), (2,1) — 8 pieces.
        - For any B >= 4, we can take a cycle of length B by choosing appropriate size.
        - The cycle: (1,2), (2,3), ..., (k, k+1), (k+1, k), (k, k-1), ..., (2,1).
          - Length: k + (k-1) = 2k-1.
          - For B=5: 2k-1=5 => k=3.
          - Sequence: (1,2), (2,3), (3,4), (4,3), (3,2).
          - Check: (3,2) to (1,2)? Not adjacent.
          - Wait, the sequence ends at (2,1) for k=3? Let's list:
            - k=3: (1,2), (2,3), (3,4) [that's k=3 pieces], then (4,3), (3,2), (2,1) [that's k=1 pieces? No, from (k+1,k) to (2,1): (4,3), (3,2), (2,1) — that's 3 pieces].
            - Total: 3 + 3 = 6.
          - So for k=3, length is 6.
          - For length 5, we need 2k-1=5 => k=3, but that gives 6.
          - So we need a different shape for odd B.
      - Alternative: Use a cycle that goes around a 2×m rectangle but with diagonal moves? No.
      - We can use a "figure 8" or just place them in a line and connect with a U-turn.
      - Actually, for any B >= 4, we can place them in a cycle like this:
        - Start at (1,2).
        - Go diagonally down-right to (B-2, B-1).
        - Then go diagonally down-left to (B-1, B-2).
        - Then go diagonally up-left to (2,1).
        - Then go diagonally up-right to (1,2).
        - This is a diamond shape.
        - Number of pieces: (B-2) steps down-right + 1 + (B-2) steps down-left + 1 + (B-2) steps up-left + 1 + (B-2) steps up-right + 1? No.
        - Let's count: (1,2) to (B-2, B-1): that's B-2 moves, so B-2 pieces? No, including start.
        - Actually, the diamond has 4 sides.
        - For B=4: (1,2), (2,3), (3,2), (2,1). Sides: 1 piece each? No.
        - Let's just use a simple construction for B>=4:
          - If B is even: place them in a cycle of length B around a 2×(B/2) rectangle? No.
          - We can use the following cycle for any B>=4:
            - (1,2), (2,3), (3,4), ..., (B-1, B), (B, B-1), (B-1, B-2), ..., (2,1).
            - This has length: (B-1) + (B-2) = 2B-3.
            - Too long.
          - We need exactly B pieces.
          - For B=4: (1,2), (2,3), (3,2), (2,1).
          - For B=5: (1,2), (2,3), (3,4), (4,3), (3,2). But (3,2) to (1,2) is not adjacent.
          - We can modify: (1,2), (2,3), (3,4), (4,5), (5,4), (4,3), (3,2), (2,1) is 8.
          - For B=5, we can do: (1,2), (2,3), (3,4), (4,3), (3,2), (2,1) is 6.
          - We need to remove one. Remove (4,3)? Then (3,4) to (3,2) not adjacent.
          - Remove (3,4)? Then (2,3) to (4,3) not adjacent.
          - So we need a different shape for odd B.
          - Actually, we can use a cycle that goes around a 2×3 rectangle but with diagonal moves? No.
          - Wait, we can place them in a cycle that goes:
            - (1,1), (2,2), (3,3), ..., (k,k), then turn.
            - But (1,1) to (2,2) is diagonal.
            - We can make a cycle: (1,1), (2,2), (3,3), (4,4), (4,3), (3,2), (2,1), (1,2).
            - That's 8 pieces.
          - For B=5: (1,1), (2,2), (3,3), (3,2), (2,1), (1,2) — that's 6.
          - (1,1), (2,2), (3,3), (4,4), (4,3), (3,2), (2,1) — that's 7.
          - (1,1), (2,2), (3,3), (4,4), (5,5), (5,4), (4,3), (3,2), (2,1), (1,2) — 10.
          - This is getting complicated.
          - Simpler: For B>=4, we can always place them in a cycle by using a "staircase" that goes up and down.
          - Actually, the simplest is to place them in a 2×B grid? No, diagonal moves.
          - We can place them in a single row and use diagonal moves to go back? No, diagonal moves change both coordinates.
          - Let's think of a cycle as a polygon where each step is diagonal.
          - A diagonal step changes both r and c by ±1.
          - So the sum r+c changes by 0 or ±2.
          - In a cycle, the sum r+c must return to start.
          - This is possible.
          - One simple cycle for any B>=4:
            - Place pieces at: (1,2), (2,1), (3,2), (4,1), (5,2), ..., alternating between column 2 and 1.
            - But (1,2) to (2,1) is diagonal.
            - (2,1) to (3,2) is diagonal.
            - So we can place them in a zigzag between two columns.
            - Sequence: (1,2), (2,1), (3,2), (4,1), ..., (B, 2) if B is odd, or (B,1) if B is even.
            - Then we need to close the cycle.
            - If B is even, say B=4: (1,2), (2,1), (3,2), (4,1).
              - (4,1) to (1,2) is not adjacent.
            - If B is odd, say B=5: (1,2), (2,1), (3,2), (4,1), (5,2).
              - (5,2) to (1,2) is not adjacent.
            - So we need to connect the ends.
            - We can connect (B, x) to (1, y) with a diagonal move if they are adjacent.
            - For B=4: (4,1) to (1,2) is not adjacent.
            - We can modify the pattern to make the ends adjacent.
            - Place them in a cycle that goes around a rectangle:
              - (1,2), (2,3), (3,4), ..., (k, k+1), then (k+1, k), (k, k-1), ..., (2,1), then back to (1,2).
              - This requires the last to be (2,1) and first to be (1,2), which are adjacent.
              - Length: k + (k-1) = 2k-1.
              - For B=4: 2k-1=4 => k=2.5, no.
              - For B=5: k=3, length 6.
              - For B=6: k=3.5, no.
            - So this gives odd lengths only.
            - For even B, we can use a different shape.
            - Or we can use a cycle that goes around a 2×2 square but with diagonal moves? No.
            - Actually, we can use a cycle that goes:
              - (1,1), (2,2), (3,3), (4,4), (4,3), (3,2), (2,1), (1,2).
              - Length 8.
            - For any B>=4, we can take a cycle of length B by choosing appropriate k.
            - The cycle: (1,1), (2,2), ..., (k,k), (k+1, k+1), (k+1, k), (k, k-1), ..., (2,1), (1,2).
            - This is getting messy.
          - Let's look for a simpler universal construction for B>=4.
          - We can place them in a cycle that goes around a diamond of size s.
          - Diamond of size s has 4s pieces.
          - For B=4: s=1.
          - For B=5: we can take s=2 (8 pieces) and remove 3? No.
          - We can take a diamond of size 2 and remove some pieces, but we need to maintain the cycle.
          - Alternatively, we can place them in a "snake" pattern:
            - (1,1), (2,2), (1,3), (2,4), (1,5), ...
            - This goes up and down.
            - (1,1) to (2,2): diag.
            - (2,2) to (1,3): diag.
            - (1,3) to (2,4): diag.
            - ...
            - This is a zigzag.
            - To close the cycle, we need to connect the end back to start.
            - If we have odd number of pieces, the end is at (1, c) or (2, c).
            - We can adjust the pattern to make the ends adjacent.
            - For example, for B=5:
              - (1,1), (2,2), (1,3), (2,4), (1,5).
              - (1,5) to (1,1) is not adjacent.
            - We can change the last move:
              - (1,1), (2,2), (1,3), (2,4), (3,5).
              - (3,5) to (1,1) not adjacent.
            - We can make a cycle that goes:
              - (1,1), (2,2), (3,3), (4,4), (5,5), (5,4), (4,3), (3,2), (2,1), (1,2).
              - Length 10.
            - This is not efficient.
          - Let's think differently. We can place the B pieces in a cycle by using a "comb" shape.
          - Or we can use the following trick: place them in a 2×B grid and move diagonally? No.
          - Actually, we can place them in a cycle that goes around a 2×(B-2) rectangle with diagonal moves on the corners.
          - Wait, I think the simplest is to use a cycle that goes:
            - For B >= 4:
              - If B is even: place at (1,2), (2,1), (3,2), (4,1), ..., (B-1,2), (B,1), then (B,2), (B-1,3), ..., (2,B), (1,B-1), then back to (1,2)? No.
          - Let's search for a known construction.
          - Actually, for B>=4, we can place them in a cycle that goes:
            - (1,2), (2,3), (3,4), ..., (B-2, B-1), (B-1, B-2), (B-2, B-3), ..., (2,1), (1,2).
            - This is the diamond shape.
            - Length: (B-2) + (B-3) + 2 = 2B-3? No.
            - Let's count: from (1,2) to (B-2, B-1): that's B-2 pieces.
            - Then (B-1, B-2) to (2,1): that's B-2 pieces.
            - Total: 2B-4.
            - For B=4: 2*4-4=4. Pieces: (1,2), (2,3), (3,2), (2,1). Yes.
            - For B=5: 2*5-4=6. Pieces: (1,2), (2,3), (3,4), (4,3), (3,2), (2,1). That's 6 pieces, but we need 5.
            - We can remove one piece from the middle? But then the cycle breaks.
            - We can make a smaller diamond for B=5.
            - Diamond of size 2 has 8 pieces.
            - We need 5.
            - We can take a path and connect the ends with a diagonal move if they are adjacent.
            - For B=5: (1,2), (2,3), (3,4), (4,3), (3,2).
              - (3,2) to (1,2) is not adjacent.
            - (1,2), (2,3), (3,2), (2,1), (1,2) is 4 pieces.
            - (1,2), (2,3), (3,4), (4,5), (5,4), (4,3), (3,2), (2,1) is 8.
            - We can take a subset that forms a cycle? No, must use all pieces.
          - Alternative: Use a cycle that goes around a 2×3 rectangle but with diagonal moves? No.
          - Let's try to construct for B=5 manually:
            - Need 5 pieces, all blue, cycle of diagonal moves.
            - Try: (1,1), (2,2), (3,3), (2,4), (1,3).
              - (1,1)→(2,2): diag.
              - (2,2)→(3,3): diag.
              - (3,3)→(2,4): diag.
              - (2,4)→(1,3): diag.
              - (1,3)→(1,1): not diag.
            - Try: (1,2), (2,3), (3,2), (2,1), (3,0)? No.
            - Try: (2,1), (1,2), (2,3), (3,2), (2,1) — that's 4 unique.
            - Try: (1,1), (2,2), (1,3), (2,2)? No, duplicate.
            - Try: (1,1), (2,2), (3,1), (2,2)? No.
            - Try: (1,1), (2,2), (3,3), (4,2), (3,1).
              - (1,1)→(2,2): diag.
              - (2,2)→(3,3): diag.
              - (3,3)→(4,2): diag.
              - (4,2)→(3,1): diag.
              - (3,1)→(1,1): not diag.
            - Try: (1,2), (2,1), (3,2), (2,3), (1,2) — that's 4 unique.
            - Try: (1,2), (2,3), (3,4), (2,3)? No.
            - It seems B=5 might be impossible? But we said B>=4 is possible.
            - Wait, is B=5 possible?
            - Let's check parity.
            - Blue moves preserve parity of r+c.
            - So all blues in the cycle must have the same parity of r+c.
            - For B=5, we need 5 distinct squares with same parity, forming a cycle where each is diagonally adjacent to the next.
            - Diagonally adjacent squares have the same parity.
            - So we need a cycle in the graph where vertices are squares of one parity, edges are diagonal moves.
            - This graph is bipartite? No, it's a grid graph.
            - Actually, the diagonal adjacency graph on same-parity squares is connected.
            - We need a cycle of length 5.
            - Is there a cycle of length 5 in this graph?
            - The graph is like a grid rotated 45 degrees.
            - Minimum cycle is 4 (a diamond).
            - Can we have a cycle of length 5?
            - In a grid graph, odd cycles are possible if the graph is not bipartite.
            - The diagonal adjacency graph on same-parity squares: each vertex has degree up to 4.
            - Is it bipartite? A graph is bipartite if it has no odd cycles.
            - Can we have a 5-cycle?
            - Try: (1,1), (2,2), (3,3), (3,2)? No, (3,3) to (3,2) is not diagonal.
            - (1,1), (2,2), (3,1), (2,0)? No.
            - (1,2), (2,3), (3,2), (2,1), (1,2) is 4.
            - (1,2), (2,3), (3,4), (4,3), (3,2) — (3,2) to (1,2) not adjacent.
            - (1,2), (2,1), (3,2), (4,1), (3,2)? No.
            - (1,1), (2,2), (3,3), (4,4), (5,3), (4,2), (3,1), (2,2)? No.
            - It seems difficult to have a cycle of length 5 with diagonal moves only.
            - Let's check if the diagonal adjacency graph on same-parity squares has odd cycles.
            - Consider the coordinates (r,c) with r+c even.
            - Map to (x,y) = ((r+c)/2, (r-c)/2) or something.
            - Actually, diagonal moves change r by ±1 and c by ±1.
            - So r+c changes by 0 or ±2.
            - If we only consider same parity, r+c is constant mod 2, but can change by 2.
            - Let's fix r+c = 2k.
            - Then r = k + d, c = k - d for some integer d.
            - A diagonal move changes r by ±1 and c by ±1.
            - So d changes by ±1 or ∓1? r+c constant, so if r increases by 1, c decreases by 1, so d increases by 1.
            - If r increases by 1, c increases by 1, then r+c increases by 2, so we move to a different parity class.
            - So within the same parity class, diagonal moves are those where r and c change in opposite directions.
            - So d changes by ±1.
            - So the graph is a 1D chain? No, because we can also have r-c change.
            - Actually, if r+c is fixed, then the squares form a diagonal line.
            - On a diagonal line, diagonal moves that keep r+c constant are moves along the line.
            - So the graph is a set of disjoint paths (the diagonals).
            - So there are no cycles!
            - Wait, that's important.
            - If we fix r+c = constant, then the squares are on a diagonal.
            - Diagonal moves that keep r+c constant are moves along that diagonal.
            - So the graph is a collection of paths (the diagonals).
            - There are no cycles within one diagonal.
            - To make a cycle, we need to move between diagonals.
            - But moving between diagonals changes r+c by ±2, which changes the parity.
            - So if we restrict to same parity, we are confined to one diagonal (or a set of diagonals with same parity).
            - Actually, r+c even means we are on diagonals where r+c is even.
            - These are disjoint lines.
            - On each line, diagonal moves that keep r+c even are moves along the line.
            - So the graph is a set of disjoint lines (paths).
            - There are no cycles!
            - Therefore, a cycle of only blue pieces is impossible!
            - But the problem says we can place pieces anywhere, and we need a cycle.
            - If the graph has no cycles, then we cannot form a cycle using only blue pieces.
            - Wait, but we can have a cycle that goes through different parities? No, blue moves preserve parity, so all blues in the cycle must have the same parity.
            - And on that parity class, the graph is a set of paths, so no cycles.
            - Therefore, B=0 is the only possibility for blue-only? No, we need R+B >= 2.
            - But if B>=1 and R=0, we need a cycle of blues.
            - Is it really impossible?
            - Let's check B=4: (1,2), (2,3), (3,2), (2,1).
              - r+c: 3, 5, 5, 3.
              - Parities: odd, odd, odd, odd.
              - All same parity.
              - Are they on the same diagonal? (1,2) and (2,1) are on r+c=3.
              - (2,3) and (3,2) are on r+c=5.
              - So they are on two different diagonals.
              - How do we move from (1,2) to (2,3)? r+c changes from 3 to 5.
              - That's a change of 2, so parity is preserved (odd to odd).
              - So we can move between diagonals if the difference in r+c is 2.
              - So the graph is not just disjoint paths; it's a grid where each vertex is connected to others with r+c difference 0 or 2.
              - Actually, from (1,2), we can move to:
                - (2,3): r+c=5
                - (2,1): r+c=3
                - (0,3): invalid
                - (0,1): invalid
              - So (1,2) is connected to (2,3) and (2,1).
              - (2,3) is connected to (1,2), (3,2), (3,4), (1,4).
              - So the graph is connected and has cycles.
              - For example, (1,2)-(2,3)-(3,2)-(2,1)-(1,2) is a 4-cycle.
              - Can we have a 5-cycle?
              - Let's try to find a 5-cycle in this graph.
              - The graph is bipartite? Let's check.
              - Color vertices by (r-c) mod 2? Or something.
              - Actually, the diagonal move changes r by ±1 and c by ±1.
              - So r-c changes by 0 or ±2.
              - So (r-c) mod 2 is preserved.
              - So the graph is bipartite with partition based on (r-c) mod 2.
              - Therefore, all cycles must have even length!
              - So B must be even for a blue-only cycle.
              - Similarly, for red-only: red move changes r by ±1 or c by ±1.
              - So r+c changes by ±1.
              - So (r+c) mod 2 flips.
              - So the graph is bipartite with partition based on (r+c) mod 2.
              - So all cycles must have even length.
              - So R must be even for a red-only cycle.
              - And minimum cycle length is 4.
              - So:
                - R=0, B>=4 and B even: Yes.
                - R=0, B odd: No.
                - B=0, R>=4 and R even: Yes.
                - B=0, R odd: No.
              - This matches the parity argument.
              - So for R=0, B must be even and >=4.
              - For B=0, R must be even and >=4.
              - Now for mixed:
                - R>=1, B>=1.
                - We need to check if there are other constraints.
                - From earlier parity analysis:
                  - R=1, B=1: No.
                  - R=1, B>=2: No (since B must be even? No, B can be odd if we have reds).
                  - Wait, earlier we said R=1, B>=2 is impossible due to parity of the cycle.
                  - Let's re-verify with the graph bipartiteness.
                  - The whole graph (with both red and blue moves) is not bipartite because blue moves preserve parity and red moves flip parity.
                  - So odd cycles are possible in the mixed graph.
                  - But we need to assign colors to the vertices.
                  - The cycle must alternate between red and blue moves? Not necessarily, but the colors of the pieces determine the move type.
                  - Actually, the move type is determined by the piece making the move.
                  - So if piece i is Red, it moves to piece i+1 using a red move (orthogonal).
                  - If piece i is Blue, it moves to piece i+1 using a blue move (diagonal).
                  - So the cycle in the grid graph must have edges that are either orthogonal or diagonal, and the edge type must match the color of the source piece.
                  - So we need a cycle in the grid where each edge is labeled by the color of its source vertex.
                  - This is more flexible.
                  - So R=1, B=2: cycle of 3 pieces: R, B, B.
                    - R→B: orthogonal.
                    - B→B: diagonal.
                    - B→R: diagonal.
                    - So we need a path of length 3 that forms a cycle.
                    - R at (1,1), B at (1,2) [orth], B at (2,1) [diag from (1,2)], then B(2,1)→R(1,1) [diag? (2,1)→(1,1) is orth, not diag].
                    - So no.
                    - Try: R(1,1), B(2,1) [orth], B(1,2) [diag from (2,1)], then B(1,2)→R(1,1) [diag? (1,2)→(1,1) is orth].
                    - So no.
                    - So R=1, B=2 is impossible.
                  - R=1, B=3: cycle R,B,B,B.
                    - R→B: orth.
                    - B→B: diag.
                    - B→R: diag.
                    - Try: R(1,1), B(1,2) [orth], B(2,3) [diag], B(3,2) [diag], then B(3,2)→R(1,1) [diag? no].
                    - So no.
                  - So R=1, B>=2 is impossible.
                  - R=2, B=1: cycle R,R,B.
                    - R→R: orth.
                    - R→B: orth.
                    - B→R: diag.
                    - R(1,1), R(1,2) [orth], B(2,2) [orth from (1,2)], then B(2,2)→R(1,1) [diag: (2,2)→(1,1) is diag].
                    - Yes! So R=2, B=1 is possible.
                  - R=2, B=2: possible.
                  - R=2, B=3: possible (sample).
                  - So the conditions are:
                    - R=0: B even and B>=4.
                    - B=0: R even and R>=4.
                    - R=1, B=1: No.
                    - R=1, B>=2: No.
                    - R>=2, B=1: Yes.
                    - R>=2, B>=2: Yes.
                  - Wait, what about R=3, B=1?
                    - Cycle R,R,R,B.
                    - R→R: orth.
                    - R→B: orth.
                    - B→R: diag.
                    - R(1,1), R(1,2) [orth], R(1,3) [orth], B(2,3) [orth], then B(2,3)→R(1,1) [diag? (2,3)→(1,1) no].
                    - Try: R(1,1), R(2,1) [orth], R(2,2) [orth], B(3,2) [orth], then B(3,2)→R(1,1) [diag? (3,2)→(1,1) no].
                    - Try: R(1,1), R(1,2) [orth], R(2,2) [orth], B(3,2) [orth], then B(3,2)→R(1,1) [diag? (3,2)→(1,1) no].
                    - Try: R(1,1), R(2,1) [orth], R(3,1) [orth], B(3,2) [orth], then B(3,2)→R(1,1) [diag? (3,2)→(1,1) no].
                    - Try: R(1,1), R(1,2) [orth], R(2,2) [orth], B(2,3) [orth], then B(2,3)→R(1,1) [diag? (2,3)→(1,1) no].
                    - Try: R(1,1), R(2,1) [orth], R(2,2) [orth], B(1,3) [orth from (2,2)? (2,2)→(1,3) is diag, not orth].
                    - So R(2,2)→B must be orth, so B at (1,2), (3,2), (2,1), or (2,3).
                    - If B at (2,3): B→R(1,1) must be diag. (2,3)→(1,1) no.
                    - If B at (1,2): B→R(1,1) must be diag. (1,2)→(1,1) is orth.
                    - If B at (3,2): B→R(1,1) must be diag. (3,2)→(1,1) no.
                    - If B at (2,1): B→R(1,1) must be diag. (2,1)→(1,1) is orth.
                    - So no.
                    - Try different order: R,R,B,R.
                      - R(1,1)→R(1,2) [orth].
                      - R(1,2)→B(2,2) [orth].
                      - B(2,2)→R(3,3) [diag].
                      - R(3,3)→R(1,1) [orth? no, (3,3)→(1,1) not adjacent].
                    - Try: R(1,1), R(2,1), B(2,2), R(1,2).
                      - R(1,1)→R(2,1) [orth].
                      - R(2,1)→B(2,2) [orth].
                      - B(2,2)→R(1,2) [diag? (2,2)→(1,2) is orth].
                    - Try: R(1,1), R(2,1), B(3,2), R(2,3).
                      - R(1,1)→R(2,1) [orth].
                      - R(2,1)→B(3,2) [diag? (2,1)→(3,2) is diag, but R→B must be orth].
                    - So R(2,1)→B must be orth, so B at (1,1) [taken], (3,1), (2,2).
                      - If B at (2,2): B→R must be diag. R at (1,1) [taken], (3,1), (2,3), (1,3).
                        - If R at (3,1): R→R(1,1) must be orth. (3,1)→(1,1) no.
                        - If R at (2,3): R→R(1,1) must be orth. (2,3)→(1,1) no.
                        - If R at (1,3): R→R(1,1) must be orth. (1,3)→(1,1) no.
                      - If B at (3,1): B→R must be diag. R at (2,2) [taken by B? no, B is at (3,1)], (4,2), (2,0) invalid,