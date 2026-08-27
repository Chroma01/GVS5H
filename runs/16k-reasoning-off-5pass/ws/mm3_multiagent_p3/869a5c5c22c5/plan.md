A valid arrangement forms a single directed cycle alternating piece types, where consecutive pieces are adjacent by their movement rules. Red moves are Manhattan (grid) edges, blue moves are diagonal (checkerboard-color changing) edges. We can build one long "snake" that covers all red and blue pieces and closes the cycle.

- If `R == 0` and `B == 0` is impossible by constraint (`R+B >= 2`). Handle trivial small totals:
  - If `R + B == 2` and `B == 2`: two blues need a 2-cycle of diagonal moves; placing two blues on a diagonal (e.g., (1,1) and (2,2)) works.
  - If `R + B == 2` and `B == 1`: one red and one blue must be adjacent by both rules — impossible because red moves to a same-colored square and blue to opposite-colored square, so no common edge exists. Print `No`.
- If `R + B == 2` and `B == 0`: two reds on adjacent squares (e.g., (1,1) and (1,2)) works.
- For larger cases (`R+B >= 3`):
  - If `B >= 2`: use a diagonal "spine" of 2 blue cells (e.g., (1,1) and (2,2)) plus extend with red and remaining blue into a snake cycle. We construct a closed path: start at (1,1), go along a zigzag on row 2 using reds/blue to cover the rest, and return to (1,1). Construction works for all combinations when `B >= 2` or `R >= 2` except the forbidden single-edge cases.
  - If `B == 1`: only one blue, remaining are reds. For `R >= 2`, we can build a cycle of reds and insert the single blue. We handle by placing the blue at a position with diagonals to two reds (e.g., (1,1) and (2,2)) and surrounding reds appropriately. Actually with `B==1, R>=2`, we construct a cycle of all reds except two reds are replaced/moved so that the single blue is inserted; we show a constructive layout. The forbidden case is `R=1, B=1` already covered.

Simplify the constructive answer:
- Output `Yes` and a cycle for almost all cases, except:
  - `R == 1 and B == 1` → `No`.
  - `R == 0 and B == 2` → `Yes` (blue diagonal pair).
  - `R == 2 and B == 0` → `Yes` (two adjacent reds).
  - For all other `(R, B)`, construct an explicit cycle.

Construction (all coordinates within 1..1e9):
We build a rectangular "snake" with two extra diagonal cells at one end to include the blues. Concretely, for `B >= 2`:
- Place a blue at (1,1), a blue at (2,2), and a red at (2,1) to connect them.
- Then walk row 2 from column 2 to column K+1 alternating with row 3 from column K+1 back to column 2 (using reds and blues as needed), finally close to (1,1).
- Distribute remaining pieces along this snake to fill counts.

For `B == 1, R >= 2`:
- Place a red at (1,1), red at (1,2), red at (2,2), red at (2,1) forming a red square cycle of length 4; we need `R+1` pieces total. For `R=2` we already placed the two reds; we insert the single blue adjacent to two reds — but we must keep red counts. Simpler: place the blue at (1,1) and (2,2) are reds? Actually we need a single blue in the cycle. We do: blue (1,1), red (2,2), then reds on a snake that returns to a red neighbor of (1,1), which must be (2,2) (diagonal) — that's the only blue-red adjacency. So cycle: B(1,1) → R(2,2) → (snake of reds) → R(1,2) → B(1,1)? Red (1,2) is not diagonally adjacent to B(1,1). So we need two blue-red adjacencies involving the single blue, meaning the blue is between two reds diagonally adjacent to it. But a blue only moves to diagonal squares, so in the cycle it must have one red on each diagonal neighbor. So we need at least two reds at (0,0) and (2,2) or (0,2) and (2,0) — but (0,0) invalid. We can use (2,2) and (1,1) is blue so (1,1) needs diagonals (0,0),(0,2),(2,0),(2,2). Only (2,2) is on board. So a single blue cannot be in a cycle of length > 2 with only reds around it. Thus `B == 1` and `R >= 2` is actually **impossible** for cycles? Let's check: cycle ... → red A → blue → red B → ... with red A and red B diagonally adjacent to blue. So we need two reds on different diagonal neighbors of the blue. That's fine, both can be placed. The rest of the cycle is reds only. So we need a red-only cycle that includes two reds at specific diagonal positions of the blue. A red-only cycle exists for any R ≥ 2? Not always: a red cycle is a 4-cycle in the grid (alternating horizontal/vertical). For R=2, two reds adjacent — cycle length 2 impossible because each red must have a red neighbor on both sides in the cycle; with 2 reds, they would need to be mutually adjacent both ways, impossible. For R=3, also impossible. For R≥4, a 4-cycle works. So we need:
  - `B == 1, R >= 4`: Yes (insert blue between two diagonally adjacent reds of a 4-cycle).
  - `B == 1, R == 2 or 3`: No.
  - `B == 0, R == 2`: Yes (two adjacent reds form a 2-cycle? Two reds must each move to the other in one move → they need to be adjacent both ways, which is true for two adjacent squares; but each red appears once in the cycle, so edge i→i+1 and edge (R)→1. For 2 reds at (1,1) and (1,2): (1,1)→(1,2) OK, (1,2)→(1,1) OK. So Yes).
  - `B == 0, R == 1`: impossible since R+B≥2, so R=0 here not relevant.

Re-evaluate conditions:
- `(R,B) = (1,1)`: No.
- `(R,B) = (0,2)`: Yes (B diagonal pair).
- `(R,B) = (2,0)`: Yes (R adjacent pair).
- `(R,B) = (0,1)` impossible by R+B≥2.
- `B == 1, R in {2,3}`: No.
- `B == 1, R == 1`: already No.
- `B == 1, R >= 4`: Yes.
- `B >= 2`: always Yes (construct snake).

Check sample: (2,3) → B=3≥2 Yes. (1,1) → No. (4,0) → R=4, B=0 Yes. Matches.

So algorithm:
For each test case:
1. If `(R, B) == (1, 1)`: print No.
2. Else if `B == 1 and R in {2, 3}`: print No.
3. Else: print Yes and output a constructed cycle.

Construction details:
Case A: `B >= 2`.
We construct a cycle that includes 2 blue cells forming a diagonal pair, surrounded by reds, plus extra pieces laid out in a snake. We need exact counts. Let's build a "Z" shape:
Coordinates (using rows 1..something, cols 1..something):
- Cell 1: Blue (1,1)
- Cell 2: Blue (2,2)
- Cell 3: Red (2,1)
- Now walk horizontally on row 2 from col 2 to col M, then drop to row 3, walk back to col 2, forming a rectangle cycle? But we must close back to (1,1). The last piece must move to (1,1). (1,1) is diagonally adjacent to (2,2) only. So the last piece must be a red at (2,2)? But (2,2) is already used. Alternative: use (1,1) and (1,2) as a red neighbor? (1,2) is not diagonal to (1,1) for blue. So the only way the cycle returns to (1,1) is from a blue moving diagonally to (1,1), i.e., the last piece is a blue at a diagonal neighbor of (1,1) such as (2,2). So the last piece must be the blue at (2,2) (or another blue at (0,0)/(0,2)/(2,0) — only (2,2) is in range). Thus the cycle is: ... → (2,2) blue → (1,1) blue. So (2,2) is the predecessor of (1,1). That means (1,1) is the successor of (2,2). In the cycle ordering, (1,1) is followed by its successor (some piece), and (2,2) is preceded by some piece and followed by (1,1). So we can place pieces as:
Sequence: B(1,1) → ... → B(2,2) → B(1,1). The first piece is (1,1), the last is (2,2), and the first's predecessor is (2,2) (closing the cycle).

So we need a path from B(1,1) to B(2,2) covering all other pieces, with B(1,1)→first move valid (B(1,1) must reach its successor diagonally). The successor of (1,1) can be a blue at (2,2) — but then path length 1, only works if R+B=2 and B=2, which is handled. Otherwise, successor of (1,1) is a red at (1,2) or (2,1) (since red moves are orthogonal). So piece 2 is Red at (1,2) or (2,1). Let's pick Red(2,1). Then Red(2,1)→ next must be orthogonal neighbor: (1,1) (used), (2,2) (blue), (3,1), (2,0) invalid. We can go to (3,1) red, then (4,1)... or (2,2) blue. To incorporate remaining blues, we can have a path: B(1,1)→R(2,1)→B(2,2)→R(2,3)→R(2,4)→...→B(3,4)→R(3,3)→... returning to (2,2)? But (2,2) is already used.

Simpler construction: Use a cycle that is a rectangle with two blues on one diagonal. Specifically:
- Blue at (1,1) and (2,2).
- Red at (1,2) and (2,1).
Cycle: B(1,1) → R(1,2) → B(2,2) → R(2,1) → B(1,1). That's length 4 with 2 blues, 2 reds. We can extend this to a larger cycle by "expanding" one of the red edges into a snake. For example, replace the edge R(1,2)→B(2,2) with: R(1,2) → R(1,3) → R(1,4) → ... → R(1, K) → B(2, K) → B(2,2), where we insert additional reds and one blue at (2,K). This adds reds and one extra blue per expansion. By repeating, we can match arbitrary R and B counts.

Let initial base cycle have 2 blues and 2 reds. Remaining pieces: R' = R-2, B' = B-2 (if B>=2). We add B' extra blues, each requiring an expansion that also adds some reds. If we add one blue at (2, k), we need to add (k-2) reds on row 1 from col 3 to k, and the red at (1,2) already exists, and we need to adjust the cycle. Let's formalize.

Base cycle (2B,2R):
1: B (1,1)
2: R (1,2)
3: B (2,2)
4: R (2,1)
back to 1.

We want to add extra pieces. We can "insert" a segment between piece 2 and piece 3. The original edge is 2→3: (1,2)→(2,2) (red to blue, orthogonal to diagonal — not a valid move! R(1,2) cannot move to B(2,2) directly because red moves orthogonally (1,2)→(2,2) is allowed! Yes, (2,2) is orthogonal to (1,2). So red can move to that blue. Good.)

To extend, replace the direct edge R(1,2)→B(2,2) with a path:
R(1,2) → R(1,3) → R(1,4) → ... → R(1, k) → B(2, k) → B(2,2).
This inserts (k-2) extra reds and 1 extra blue (at (2,k)). The moves:
- R(1,j)→R(1,j+1): valid (horizontal).
- R(1,k)→B(2,k): red to blue orthogonal move (down), valid.
- B(2,k)→B(2,2): blue to blue diagonal? (2,k)→(2,2) would be horizontal, not diagonal. Need to be diagonal. So we cannot have two blues horizontally adjacent. We need B(2,k) to reach B(2,2) via diagonal moves. We can do: B(2,k) → B(3,k-1) → B(3,k-2)? This gets complex.

Alternative: insert a vertical segment. Replace R(2,1)→B(1,1) edge? R(2,1)→B(1,1) is red to blue orthogonal (up), valid. Extend with a vertical column of reds and a blue at bottom: R(2,1) → R(3,1) → ... → R(m,1) → B(m+1,2) → ? Back to B(1,1)? Need to close.

Maybe easier: construct a cycle entirely along a diagonal "zigzag" where all blues are on the main diagonal (r,c) with r=c, and reds connect them orthogonally. For example, place blues at (1,1), (2,2), (4,4), (6,6), ... and reds in between. Each consecutive blue pair (i,i) and (i+1,i+1) are diagonally adjacent, so blue can move directly. But in the cycle, we need alternating red and blue? No, the problem says: "the i-th piece placed can move in one move to the square containing the (i+1)-th piece placed." It does NOT require alternating colors! It just requires that the piece on square i can move to square i+1 using its own movement rule. So a blue can move to a blue, a red to a red, or a red to a blue, or a blue to a red, as long as the move is valid for the piece's type.

This simplifies everything! The cycle is just a directed cycle in the graph where red nodes connect to orthogonal neighbors, blue nodes to diagonal neighbors, regardless of color of destination.

So we just need a single cycle in this graph containing exactly R red nodes and B blue nodes, with nodes distinct.

This is much easier. We can build a cycle that snakes through a grid, labeling cells as red or blue as needed, ensuring total counts match.

Simplest construction for almost all cases:
- Make a cycle that goes around a rectangle: right, down, left, up. Place pieces along this 4-edge path.
- If we make a rectangle of width W and height H, the perimeter has 2*(W+H) cells (but corners counted once, so 2*(W+H) if W,H>1; actually perimeter length = 2W+2H). We can place exactly that many pieces.
- Assign them to be red or blue to match counts.
- But we need each piece's move to be valid:
  - Horizontal moves: red piece can do horizontal, blue cannot.
  - Vertical moves: red can, blue cannot.
  - Diagonal moves: blue can, red cannot.
- So a cycle made of only horizontal/vertical moves can only contain reds. To include blues, we need diagonal moves.

Better: build a cycle that alternates horizontal and diagonal moves. For example, a "staircase":
- Move right (red), move diagonal down-right (blue), move right (red), move diagonal down-right (blue), ...
- This goes diagonally across the board. At the end, we need to return to start. This would form a long diagonal line, not a cycle.

Construct a cycle that is a "diamond" shape:
Start at (1,2), go right to (1,3) [red], diagonal down-right to (2,4) [blue], left to (2,3) [red], diagonal down-left to (3,2) [blue], left to (3,1) [red], diagonal up-left to (2,0) invalid.

Maybe a figure-8? No, single cycle.

The key insight: a single cycle exists if and only if the graph has a cycle of length L containing exactly R red and B blue nodes. The graph is connected (in fact, it's a grid graph with both orthogonal and diagonal edges — the "king's move" graph). We can find a Hamiltonian-like cycle on any sufficiently large grid subset. Since the board is huge (1e9), we can always find a cycle of any length L >= some minimum, with any color distribution, by constructing a long snake and closing it.

For L >= 4, we can construct a cycle. For L=2, only possible if both are same color and adjacent (orthogonal for red, diagonal for blue). For L=3, a triangle? Red can't do diagonal, blue can't do orthogonal. Can we have a 3-cycle? Nodes A,B,C. A→B, B→C, C→A. Each edge must be valid for the moving piece. If A is red, A→B must be orthogonal. If B is blue, B→C must be diagonal. If C is red, C→A must be orthogonal. Is there such a triangle? Example: A(1,1) red → B(1,2) red → C(2,3) blue → A(2,2) red? C(2,3) blue → A(2,2) is diagonal left-down, valid. A(2,2) red → A(1,1) is vertical up, valid. But B(1,2) red → C(2,3) is diagonal, not allowed for red. So no 3-cycle with these moves. What if A blue, B red, C blue? A(1,1) blue → B(2,2) red (diagonal, but blue can only move to diagonal squares, (2,2) is diagonal, but B is red, red can be at (2,2); blue moves to (2,2) is valid because blue moves to diagonal squares, and (2,2) is a diagonal neighbor). B(2,2) red → C(2,3) (orthogonal, valid for red). C(2,3) blue → A(1,1)? (2,3) to (1,1) is not adjacent (diff 1,2). Not valid. So 3-cycles seem impossible.

Thus L must be 2 or >=4. L=2 requires both pieces same color and adjacent (red: orthogonal, blue: diagonal). L=1 impossible since no self-loop.

Cases:
- L=2: 
  - R=2, B=0: two reds orthogonal adjacent → Yes.
  - R=0, B=2: two blues diagonal adjacent → Yes.
  - Other R+B=2: R=1,B=1 → No (red orthogonal vs blue diagonal, no common edge).
- L>=4: need to construct.
  - Is L=4 always possible? Yes, a 2x2 square: (1,1)→(1,2)→(2,2)→(2,1)→(1,1). All orthogonal moves, so all must be red. That gives 4 reds. For 4 blues? Use diagonal square: (1,1)→(2,2)→(1,3)→(2,0)? No. Diagonal cycle: (1,1)→(2,2)→(3,3)→(2,2)? Not simple. But we can have a cycle with mixed colors for L=4? (1,1)R→(1,2)R→(2,2)B→(2,1)R→(1,1). (2,2)B→(2,1)R: blue to red diagonal? (2,2) to (2,1) is orthogonal, blue can't. So that fails.
  
  Let's find a 4-cycle with 1 blue, 3 reds: (1,1)R→(1,2)R→(2,2)B→(2,1)R→(1,1). (2,2)B→(2,1)R: B at (2,2) moves to (2,1)? Diagonal: (1,1),(1,3),(3,1),(3,3). (2,1) is not diagonal. So B cannot go to (2,1). What about (1,1)R→(2,1)R→(2,2)B→(1,2)R→(1,1). (2,2)B→(1,2)R: diagonal, valid. (1,2)R→(1,1)R: orthogonal, valid. So cycle: (1,1)R→(2,1)R→(2,2)B→(1,2)R→(1,1). This works! Colors: 3 reds, 1 blue. So for (R=3,B=1), L=4 works. For (R=2,B=1), L=3 doesn't work, L=4? We need 2 reds, 1 blue. In above cycle, we have 3 reds. Can we make a 4-cycle with 2 reds, 1 blue? Total pieces 3, but L=4 means 4 pieces. Wait, (R+B) = number of pieces = L. So for R=2,B=1, total 3, but L must be 3 which is impossible, or we can't have L=4 because we only have 3 pieces. So R+B=3: (3,0) → 3 reds in a cycle? 3-cycle impossible. Can we do a 3-cycle with 3 reds? No. So (3,0) is No? Let's check: R=3,B=0. Need cycle of 3 reds. No 3-cycle in grid (bipartite, odd cycle impossible). So (3,0) is No! Similarly (1,2): 1 red, 2 blues. L=3 impossible. (0,3): 3 blues, 3-cycle? Blue moves diagonal. Diagonal graph is bipartite (black/white squares). 3-cycle impossible. So (0,3) No. (2,1): R=2,B=1, L=3 impossible → No. (1,2): L=3 impossible → No.

So for total = 3, all are No except maybe? (R,B) = (0,3) no, (1,2) no, (2,1) no, (3,0) no. So all R+B=3 are No.

For R+B=4: possible. (4,0): 4 reds in a square cycle → Yes. (3,1): 3 reds 1 blue in the cycle above → Yes. (2,2): 2 reds 2 blues. Can we? (1,1)R→(2,1)R→(2,2)B→(1,2)B→(1,1). (1,2)B→(1,1)R: diagonal, valid. (2,2)B→(1,2)B: diagonal, valid. (2,1)R→(2,2)B: orthogonal, valid. (1,1)R→(2,1)R: orthogonal, valid. Yes! (1,1)R→(2,1)R→(2,2)B→(1,2)B→(1,1). Colors: 2R,2B. Good. (1,3): 1 red 3 blues. (1,1)R→(1,2)B→(2,3)B→(1,4)B→(1,1)? (1,4)B→(1,1)R: not adjacent. Try: (1,1)R→(2,1)B? R to B: (1,1)R→(2,1) is orthogonal, but B at (2,1) is destination, fine. (2,1)B→(3,2)B diagonal. (3,2)B→(2,3)B diagonal. (2,3)B→(1,2)R orthogonal? (2,3) to (1,2) is diagonal, but piece at (2,3) is B, moves to diagonal, (1,2) is diagonal, valid for B. But (1,2)R is destination. Then (1,2)R→(1,1)R orthogonal. Cycle: R(1,1)→B(2,1)→B(3,2)→B(2,3)→R(1,2)→R(1,1). Colors: 2R? Wait, we have R(1,1), R(1,2) = 2 reds, and B(2,1),B(3,2),B(2,3) = 3 blues. Total 5. For (1,3) we need 4 pieces. Let's try: R(1,1)→B(2,2)→B(1,3)→B(2,4)→R(1,3)? No. R(1,1)→B(2,2)→B(3,3)→B(2,4)→R(1,3)? (2,4) to (1,3) diagonal valid for B, but destination is R(1,3). Then R(1,3)→R(1,1)? (1,3) to (1,1) not adjacent. 
Maybe: R(1,1)→B(2,1)→B(1,2)→B(2,3)→R(1,2)? (2,3)B→(1,2) diagonal, valid, dest R. (1,2)R→(1,1)R orthogonal, valid. Colors: R(1,1), R(1,2) = 2R; B(2,1),B(1,2)? (1,2) already used. B(2,1), B(1,0) invalid. So 2R,2B but we need 1R,3B. 
Try: B(1,1)→B(2,2)→B(3,3)→B(2,4)→R(1,3)? B(2,4)→R(1,3) diagonal valid. R(1,3)→B(1,1)? (1,3) to (1,1) not adjacent. 
What about a cycle with 1R,3B: R must be between two B diagonally. B→R (diagonal) →B. So R is at a square, with B on two diagonal neighbors. E.g., R(1,1), B(2,2) and B(0,0) invalid. R(2,2), B(1,1), B(1,3), B(3,1), B(3,3). Use B(1,1)→R(2,2)→B(1,3)→B(2,4)→? Need to close. (2,4)B→(1,3)B? (2,4) and (1,3) diagonal, valid. But (1,3) already used. (2,4)B→(3,3)B diagonal. (3,3)B→(2,2)R? (3,3) to (2,2) diagonal, valid, dest R(2,2). Then R(2,2)→(1,1)B? R moves orthogonal, (1,1) is diagonal, invalid. So no.

Actually, is (1,3) possible? Let's check parity. The graph: red nodes connect orthogonally (edges between (r,c) and (r±1,c) or (r,c±1)). Blue nodes connect diagonally (edges between (r,c) and (r±1,c±1)). This graph is not bipartite? Orthogonal edges change r+c parity. Diagonal edges preserve r+c parity. So a cycle must have even number of diagonal edges? Actually, the graph is connected and has cycles. For a cycle, the sum of parities of moves: each orthogonal move flips parity, each diagonal move preserves parity. Starting at a node, after L moves we return to same node, so number of orthogonal moves must be even. Number of diagonal moves can be anything. The colors of nodes are not directly tied to parity, but the number of reds and blues in the cycle can be any combination? Not exactly; each red node must be incident to orthogonal moves in the cycle (since a red node's outgoing and incoming edges are orthogonal? Wait, the cycle is directed. A red node has exactly one outgoing edge (orthogonal) and one incoming edge (orthogonal) in the cycle, because the piece on that square is red, and it must move to the next piece using its movement rule (orthogonal). Similarly, a blue node has one outgoing and one incoming diagonal edge. So in the cycle, red nodes have degree 2 with orthogonal edges, blue nodes have degree 2 with diagonal edges.

Thus, the cycle alternates between red and blue? No! Consecutive nodes in the cycle are adjacent, but the type of the first node determines the type of the edge to the second. The second node's type does not constrain the edge from the first to the second. So a red node can point to a red node (orthogonal edge), or to a blue node (orthogonal edge). A blue node can point to a red node (diagonal edge) or to a blue node (diagonal edge). So the cycle can have any sequence of colors; it's just a cycle in the graph where red nodes are constrained to use orthogonal edges and blue nodes to use diagonal edges.

This is equivalent to: find a cycle in the grid where each node is labeled R or B, such that the cycle uses only orthogonal edges from R nodes and only diagonal edges from B nodes.

This is always possible for L >= 4 except some small cases.

From the parity argument: number of orthogonal edges in the cycle must be even. The number of orthogonal edges equals the number of R nodes (since each R node contributes one outgoing orthogonal edge, and each orthogonal edge in the cycle is outgoing from exactly one R node? Actually, an orthogonal edge connects two nodes. If one is R and the other is B, the edge is outgoing from the R node (orthogonal) and incoming to the B node (which is fine, B can receive on orthogonal). If both are R, the edge is outgoing from one R and incoming to the other R (both orthogonal). If both are B, the edge must be diagonal, so this case is diagonal. So an edge is orthogonal if and only if at least one of its endpoints is R? No. An edge is orthogonal if the source node is R. The source node is the node from which the edge is directed in the cycle. In an undirected cycle, each edge is used once. If we orient the cycle, each node has one outgoing edge. So the number of orthogonal edges is exactly the number of R nodes (since each R node has an orthogonal outgoing edge). Similarly, number of diagonal edges equals number of B nodes. Total edges = R + B. Since orthogonal edges flip parity and diagonal preserve, the number of orthogonal edges (R) must be even. Therefore, **R must be even** for any cycle to exist! Wait, is that true? Let's verify with the (1,3) case: R=1 (odd), B=3. According to this, impossible. And we couldn't find one. For (2,1): R=2 (even), B=1. According to this, possible? But total 3, L=3, but 3-cycle impossible. For (3,0): R=3 odd → impossible. (0,3): B=3, R=0 even, but L=3 impossible. (1,2): R=1 odd → impossible. So necessary conditions: R is even, and if B=0 then R>=2 and R even. If R=0, then B must be even and >=2? But also L must be >=4 or L=2. If B=0, R=2 works (L=2). If B=0, R=4 works (L=4 square). If R=0, B=2 works (L=2 diagonal). If R=0, B=4 works (L=4? 4-cycle of blues? Blues on a diagonal cycle: (1,1)→(2,2)→(3,3)→(4,4)→(3,3)? No, need cycle. (1,1)→(2,2)→(3,3)→(2,4)→(1,3)→(2,2)? Not simple. Actually 4 blues: (1,1)→(2,2)→(3,3)→(4,4)→(3,5)→... need to close. But we can have 4 blues on a "diamond": (1,1)→(2,2)→(3,1)→(2,0) invalid. Or (1,1)→(2,2)→(1,3)→(2,2) no. Wait, 4-cycle with all blue? Each blue moves diagonally. Can we have a 4-cycle where all edges are diagonal? That means all nodes are on the same color of the checkerboard? Diagonal edges connect squares of same color. So a cycle of only diagonal edges is a cycle in the graph where edges are between same-color squares. That graph is disconnected into two components: black and white. On black squares, diagonal moves go to black squares. Is there a cycle in the black-square diagonal graph? Yes, for example: (1,1) black, (2,2) black, (3,3) black, (4,2) black? (3,3) to (4,2) diagonal yes. (4,2) to (3,1) diagonal yes. (3,1) to (1,1)? Not adjacent. But we can do a 4-cycle: (1,1)→(2,2)→(3,3)→(2,4)→(1,3)→(2,2)? No. (1,1)→(2,2)→(1,3)→(2,2) no. Actually, a 4-cycle in the diagonal graph on black squares: need 4 black squares where consecutive ones are diagonally adjacent. For example: (1,1), (2,2), (3,3), (4,2) — (3,3) and (4,2) are diagonal adjacent (diff 1,1). (4,2) and (3,1) diagonal adjacent. (3,1) and (2,2) diagonal adjacent. (2,2) and (1,1) diagonal adjacent. So cycle: (1,1)→(2,2)→(3,3)→(4,2)→(3,1)→(2,2) no, we need a simple cycle of length 4. (1,1)→(2,2)→(3,1)→(2,0) invalid. Let's find 4 black squares forming a 4-cycle under diagonal adjacency. Diagonal adjacency is a grid graph rotated 45 degrees, which is isomorphic to the standard grid. So 4-cycles exist: a square in the diagonal grid corresponds to a diamond in the original grid. For example: (1,1), (2,2), (3,1), (2,0) — (2,0) is white? (1+1)=2 even (black), (2+2)=4 even (black), (3+1)=4 even (black), (2+0)=2 even (black). Yes, all black. (1,1)→(2,2) diagonal. (2,2)→(3,1) diagonal? (2,2) to (3,1) is down-left, yes diagonal. (3,1)→(2,0) diagonal? down-left, yes. (2,0)→(1,1) diagonal? up-right, yes. So cycle of 4 blues: B(1,1)→B(2,2)→B(3,1)→B(2,0)→B(1,1). But (2,0) is column 0, invalid. We can shift: B(1,2)→B(2,3)→B(3,2)→B(2,1)→B(1,2). Check: (1,2) sum=3 odd, but we need all same parity. 1+2=3 odd, 2+3=5 odd, 3+2=5 odd, 2+1=3 odd. Yes, all odd (white). So 4-cycle of blues exists on white squares: (1,2)→(2,3)→(3,2)→(2,1)→(1,2). So (R=0,B=4) is Yes.

Thus necessary conditions: R even, and not (R=1,B=1), not (R=1,B=2?) wait R=1 is odd so no. R=2,B=1: total 3, L=3 impossible. R=2,B=3: R even, total 5. Can we have a 5-cycle? Sum of orthogonal edges = R = 2 (even), diagonal edges = 3. Is there a 5-cycle with 2 orthogonal and 3 diagonal edges? Orthogonal edges flip parity. Start at parity 0. After 2 orthogonal flips, parity 0. After 3 diagonal (no flip), parity 0. So parity is consistent. But does such a cycle exist? Let's try to construct (2,3). We already know from sample (2,3) is Yes. So (2,3) works.

What about (2,1)? R=2 even, B=1. Total 3. 3-cycle with 2 orthogonal, 1 diagonal. Parity: 2 flips → 0, 0 flips → 0. Parity ok. But can we have a 3-cycle? Nodes A,B,C. Edges: A→B, B→C, C→A. Suppose A and C are red (orthogonal out), B is blue (diagonal out). A→B orthogonal: (r1,c1)→(r2,c2) with |dr|+|dc|=1. B→C diagonal: (r2,c2)→(r3,c3) with |dr|=|dc|=1. C→A orthogonal: (r3,c3)→(r1,c1) with |dr|+|dc|=1. Sum of dr: dr12 + dr23 + dr31 = 0. dr12 ∈ {±1,0} with exactly one non-zero? Actually orthogonal move changes either r or c by ±1. Diagonal move changes both r and c by ±1. Let's try to find integer coordinates.
Let A=(0,0). A→B orthogonal: B=(1,0) or (0,1) or (-1,0) or (0,-1). Try B=(1,0). B→C diagonal: C=(0,1) or (2,1) or (0,-1) or (2,-1). C→A orthogonal: C→(0,0). If C=(0,1), then C→A is (0,1)→(0,0) orthogonal, valid. So A=(0,0), B=(1,0), C=(0,1). Check: A(0,0) red → B(1,0) orthogonal OK. B(1,0) blue → C(0,1) diagonal: |1-0|=1, |0-1|=1, yes diagonal. C(0,1) red → A(0,0) orthogonal: (0,1)→(0,0) OK. So we have a 3-cycle! But wait, A and C are red, B is blue. That's 2 reds, 1 blue. The cycle is R(0,0)→B(1,0)→R(0,1)→R(0,0). Is this valid? Let's check the rules:
- Piece 1: R at (0,0) can move to (1,0) where piece 2 is. Yes, orthogonal.
- Piece 2: B at (1,0) can move to (0,1) where piece 3 is. Yes, diagonal.
- Piece 3: R at (0,1) can move to (0,0) where piece 1 is. Yes, orthogonal.
So (R=2,B=1) is Yes! But earlier I thought 3-cycle impossible. It is possible with 2 reds and 1 blue! Let's verify with sample? Sample doesn't have (2,1). But this seems valid. Coordinates: (1,1), (2,1), (1,2) with 1-based indexing: R(1,1)→B(2,1)→R(1,2)→R(1,1). Check: R(1,1)→(2,1) down OK. B(2,1)→(1,2) diagonal up-right OK. R(1,2)→(1,1) left OK. So (2,1) is Yes!

Similarly, (1,2): R=1,B=2. 3-cycle with 1 red, 2 blues. A red, B,C blue. A→B orthogonal, B→C diagonal, C→A diagonal? C is blue, so C→A must be diagonal. But A is red, and A→B is orthogonal. Let's try: A=(0,0) red. A→B: B=(1,0) blue. B→C diagonal: C=(0,1) or (2,1). C→A diagonal: C must be diagonal to A(0,0), so C=(1,1) or (1,-1) or (-1,1) or (-1,-1). But C must be reachable from B(1,0) by diagonal: |1-cx|=1, |0-cy|=1. So C=(0,1) or (2,1) or (0,-1) or (2,-1). Intersection with diagonal to (0,0): (1,1) not in list. (1,-1) not in list. (-1,1) not in list. (-1,-1) not in list. So no 3-cycle for (1,2). So (1,2) is No.

What about (0,3)? 3 blues. Need 3-cycle with all diagonal. Parity preserved, so all on same color. Diagonal graph is grid-like, 3-cycle impossible. So (0,3) No.

(3,0): 3 reds. 3-cycle with all orthogonal. Orthogonal graph is bipartite, 3-cycle impossible. So (3,0) No.

(1,3): 4 pieces, 1R 3B. We need 4-cycle. R even? R=1 odd. So necessary condition R even fails. So (1,3) No.

(3,1): R=3 odd → No.

(0,2): R=0 even, B=2. L=2. Two blues diagonal adjacent: (1,1) and (2,2). Yes.

(2,0): R=2 even, B=0. L=2. Two reds orthogonal adjacent: (1,1) and (1,2). Yes.

(0,4): R=0, B=4. 4-cycle of blues exists as shown: (1,2)→(2,3)→(3,2)→(2,1)→(1,2). Yes.

(4,0): R=4, B=0. 4-cycle of reds: (1,1)→(1,2)→(2,2)→(2,1)→(1,1). Yes.

(2,2): R=2 even, B=2. We found a 4-cycle: R(1,1)→R(2,1)→B(2,2)→B(1,2)→R(1,1). Wait, check: R(2,1)→B(2,2) orthogonal OK. B(2,2)→B(1,2) diagonal? (2,2) to (1,2) is up, not diagonal. (2,2) diagonal neighbors: (1,1),(1,3),(3,1),(3,3). So B(2,2) cannot go to B(1,2). So that cycle is invalid. We need a valid 4-cycle for (2,2). Let's try: R(1,1)→B(1,2) (orthogonal) →B(2,3) (diagonal) →R(2,2) (diagonal? (2,3) to (2,2) is orthogonal, but B(2,3) moves to (2,2) which is not diagonal. So no.) 
R(1,1)→B(2,2) (diagonal? (1,1) to (2,2) is diagonal, but R(1,1) moves orthogonally. So no.)
R(1,1)→R(1,2)→B(2,3)→B(1,2)→R(1,1)? R(1,2)→B(2,3) diagonal, but R(1,2) moves orthogonally, invalid.
R(1,1)→R(2,1)→B(3,2)→B(2,3)→R(1,2)→R(1,1)? That's 5 pieces. We need 4.
R(1,1)→R(2,1)→B(2,2)→B(1,1)? (2,2) to (1,1) diagonal, but B(2,2) to B(1,1) is diagonal, valid. Then B(1,1)→R(1,1)? (1,1) to (1,1) same square, invalid.
R(1,1)→B(2,1)? (1,1) to (2,1) orthogonal, valid for R. B(2,1)→B(1,2) diagonal? (2,1) to (1,2) is diagonal, yes. B(1,2)→R(1,1) diagonal? (1,2) to (1,1) is orthogonal, not diagonal. So B(1,2) cannot go to (1,1). 
R(1,1)→B(2,1)→R(2,2)→B(1,1)→R(1,1). Check: R(1,1)→B(2,1) orthogonal OK. B(2,1)→R(2,2) diagonal OK. R(2,2)→B(1,1) orthogonal? (2,2) to (1,1) is diagonal, not orthogonal. Invalid.
R(1,1)→B(2,1)→B(1,2)→R(2,2)→R(1,1)? R(2,2)→R(1,1) diagonal, invalid.
R(1,1)→R(1,2)→B(2,3)→B(1,2)→R(1,1)? B(1,2)→R(1,1) diagonal? (1,2) to (1,1) orthogonal, invalid.
What about R(1,1)→B(2,2)→B(3,3)→R(2,2)→R(1,1)? R(1,1)→B(2,2) diagonal, invalid.
We need a 4-cycle with 2R,2B. Let's try to use the fact that (2,1) works as a 3-cycle. Add a piece? No, must be 4 pieces.
Maybe (1,1)R → (2,1)B → (3,2)B → (2,2)R → (1,1)? (2,2)R → (1,1) diagonal, invalid.
(1,1)R → (1,2)B → (2,1)B → (2,2)R → (1,1)? (2,2)R → (1,1) diagonal, invalid.
(1,1)R → (2,1)B → (1,2)B → (1,1)R? That's a 3-cycle plus self? No.
(1,1)R → (1,2)R → (2,1)B → (1,1)B? (2,1)B → (1,1) diagonal, valid. (1,1)B → (1,1)R? same square, invalid.
(1,1)R → (2,1)B → (3,2)R → (2,2)B → (1,1)R? Check: (1,1)R→(2,1) orth OK. (2,1)B→(3,2) diag OK. (3,2)R→(2,2) orth? (3,2) to (2,2) is up, orth OK. (2,2)B→(1,1) diag? (2,2) to (1,1) is up-left, diag OK. Colors: R(1,1), B(2,1), R(3,2), B(2,2). That's 2R, 2B! And 4 pieces. Let's verify:
1: R at (1,1) can move to (2,1) where B is. Yes, down.
2: B at (2,1) can move to (3,2) where R is. Yes, down-right diagonal.
3: R at (3,2) can move to (2,2) where B is. Yes, up.
4: B at (2,2) can move to (1,1) where R is. Yes, up-left diagonal.
Perfect! So (2,2) is Yes with this cycle: R(1,1), B(2,1), R(3,2), B(2,2).

Now we have constructions for:
- (0,2): B(1,1), B(2,2)
- (2,0): R(1,1), R(1,2)
- (0,4): B(1,2), B(2,3), B(3,2), B(2,1)
- (4,0): R(1,1), R(1,2), R(2,2), R(2,1)
- (2,1): R(1,1), B(2,1), R(1,2) [3-cycle]
- (1,2): No
- (2,2): R(1,1), B(2,1), R(3,2), B(2,2) [4-cycle]
- (1,3): No (R odd)
- (3,1): No (R odd)
- (0,3): No (L=3, all blue impossible)
- (3,0): No (L=3, all red impossible)
- (1,1): No
- General: R even, and not in the above small forbidden cases.

Wait, what about (0,1)? R+B>=2 so not.
What about (0,0)? Not.

So the only "No" cases are:
- R odd
- R=1, B=1
- R=0, B odd? B=1 not possible, B=3 No, B=5? 5-cycle all blue? Diagonal graph is bipartite, odd cycle impossible. So B odd with R=0 is No.
- R=2, B=1 is Yes.
- R=1, B=2 is No.
- R=3, B=0 No.
- R=0, B=3 No.
- R=1, B=3 No (R odd).
- R=3, B=1 No (R odd).
- R=1, B=4? R odd → No.
- R=3, B=2? R odd → No.
- R=5, B=0? R odd → No.

Wait, is R even sufficient for all larger totals? Let's check R=2, B=3 (total 5). R even. We need a 5-cycle with 2 orthogonal, 3 diagonal edges. Does it exist? Sample says Yes for (2,3). So yes.

R=2, B=4 (total 6). R even. Should be possible.
R=4, B=1 (total 5). R even. Should be possible.
R=4, B=2 (total 6). R even.
R=0, B=2 Yes. R=0, B=4 Yes. R=0, B=6? 6-cycle of blues? In diagonal graph, even cycles exist. Yes.

So condition is: R is even, and not (R=1,B=1). Wait, what about R=0, B=1? Not allowed. R=0, B=2 Yes. R=0, B=4 Yes. R=0, B=6 Yes. R=0, B=odd >0: all No (since odd cycle in diagonal graph). But also R=0, B=1 is impossible by sum>=2. So R=0, B=odd >=3: No.

What about R=2, B=0 Yes. R=4, B=0 Yes. R=6, B=0 Yes. R=odd, B=0: No (odd cycle in orthogonal graph).

What about R=1, B=odd? R odd → No.
R=1, B=even? R odd → No.

So necessary and sufficient: R is even, and (R,B) != (1,1). Also (R,B) != (0,1) but not in input. Also (R,B) != (1,0) not in input. And (R,B) != (0,3), (3,0) etc are covered by R even condition? R=0, B=3: R=0 even, but B=3 odd. Our condition "R even" is not enough for R=0. We need to handle R=0 separately: B must be even (and >=2). Similarly for B=0: R must be even (and >=2). So:
- If R=0: B must be even and >=2.
- If B=0: R must be even and >=2.
- If R>0 and B>0: R must be even. (Because B>0, R+B>=3? If R>0,B>0, R+B>=2, but (1,1) is R odd, so R even excludes (1,1) and (1,odd) and (1,even) etc. Wait, R=2,B=1: R even, works. R=2,B=2: R even, works. R=2,B=3: works. R=4,B=1: works. So for B>0, the only condition is R even? But what about R=0,B=1? Not in input. R=0,B=2: R=0 even, works. R=0,B=4: works. R=0,B=3: R=0 even but fails. So the parity condition on R is not enough when B=0? Actually R=0 is even, B=3 fails. So the condition is: the number of orthogonal edges is R. In a cycle, the number of orthogonal edges must be even. The number of diagonal edges is B. Diagonal edges can be any number. So R must be even. That's the only condition on the counts? But we saw (0,3) has R=0 even, but fails because B=3 is odd and the graph of diagonal moves is bipartite (no odd cycles). So if R=0, we need B even. If B=0, we need R even (which is given). If both >0, R even is sufficient? Let's check R=2, B=1: R even, works. R=2, B=2: works. R=2, B=3: works. R=2, B=4: works. Is there any case with R>0, B>0, R even, that fails? R=1, B=1: R odd, fails. R=1, B=2: R odd, fails. R=1, B=3: R odd, fails. R=3, B=1: R odd, fails. R=3, B=2: R odd, fails. R=4, B=1: R even, should work. R=4, B=2: works. R=4, B=3: works. So it seems the condition is:
- If R == 0: B must be even and >=2.
- If B == 0: R must be even and >=2.
- If R > 0 and B > 0: R must be even. (R+B >= 2 automatically, and (1,1) has R=1 odd so excluded).

But wait, is R=0, B=2 the only small case? R=0,B=2 works. R=0,B=4 works. R=0,B=6 works. So for R=0, B even >=2 works.
For B=0, R even >=2 works.
For R>0, B>0, R even works. But what about R=2, B=0? That's B=0 case. R=2 even works.
What about R=0, B=0? Not allowed.

So the answer is "Yes" if and only if:
- R > 0 and B > 0 and R is even, OR
- R == 0 and B is even and B >= 2, OR
- B == 0 and R is even and R >= 2.
Equivalently: R is even, and (R, B) != (1, 1), and if R == 0 then B is even.

Let's double-check (R=0, B=1): not in input. (R=1, B=0): not in input. So the only "No" cases are:
- R is odd
- R == 0 and B is odd
- R == 1 and B == 1 (but this is R odd, so already covered)
- R == 0 and B == 1 (not in input)
- R == 1 and B == 0 (not in input)
- R == 0 and B == 0 (not in input)
- R+B < 2 (not in input)

Wait, is R=0, B=2 covered by "R is even"? R=0 is even. So "R is even" is true. But we also need to exclude (0, odd B). So the condition is: R is even, and if R==0 then B is even.

Simplify: "R is even" and "not (R==0 and B%2==1)". Since B is not 1 when R=0 (due to R+B>=2), the only case is (0,3), (0,5), etc. So condition: R is even, and (R > 0 or B is even).

But also we need to ensure a construction exists for all such cases. We need to provide explicit coordinates for all "Yes" cases.

We can unify construction:
We need to build a cycle of length L = R+B.
We can use a "snake" that goes back and forth, but with diagonal segments to accommodate blues.

Since the board is huge, we can use a simple parametric construction.

Case 1: R == 0, B even >= 2.
Construction: B(1,1), B(2,2), B(3,3), ..., B(B-1, B-1), and then close? We need a cycle. A path of consecutive diagonal moves is a straight line. We need to turn back. We can use a rectangle in the diagonal grid. For example, a cycle of B blues on a "diagonal rectangle". For B=2: (1,1)-(2,2). For B=4: (1,2)-(2,3)-(3,2)-(2,1). For B=6: (1,2)-(2,3)-(3,4)-(4,3)-(3,2)-(2,1). General: for B=2k, k>=1: a cycle of length 2k in the diagonal graph. We can give coordinates: for i=0..k-1: (i+1, i+2) and (i+2, i+1)? That's 2k points. For k=2: (1,2),(2,3),(3,2),(2,1). Order: (1,2)->(2,3)->(3,2)->(2,1)->(1,2). Check moves: (1,2) to (2,3) diagonal (down-right). (2,3) to (3,2) diagonal (down-left). (3,2) to (2,1) diagonal (up-left). (2,1) to (1,2) diagonal (up-right). All valid blue moves. For k=3: add (1,3),(2,4),(3,3),(4,2),(3,1),(2,2)? That's 6 points. We can just use a rectangle of size k x (k+1) in the diagonal graph. So construction: for B=2k, use the cycle: (1,2), (2,3), ..., (k, k+1), then (k+1, k), (k, k-1), ..., (2,1), then (1,2). This is a cycle of length 2k. All moves are diagonal (down-right then down-left then up-left then up-right). Coordinates are within 1..k+1 <= 1e9 since B <= 2e5.

Case 2: B == 0, R even >= 2.
Construction: standard rectangle in orthogonal grid. For R=2: (1,1)-(1,2). For R=2k, k>=1: cycle (1,1)->(1,2)->...->(1,k)->(2,k)->(3,k)->...->(k,k)->(k,k-1)->...->(k,1)->(1,1). Wait, that's not a simple cycle; we need a single cycle. A rectangle: (1,1)->(1,2)->...->(1,k)->(2,k)->(2,k-1)->...->(2,1)->(1,1). That's 2k points. All orthogonal moves. Valid for reds.

Case 3: R > 0, B > 0, R even.
We need a cycle with R reds and B blues. Total L = R+B.
We can start with a base cycle that has some reds and blues, and extend it.
Base cycles:
- (R=2, B=1): R(1,1), B(2,1), R(1,2) [3-cycle]
- (R=2, B=2): R(1,1), B(2,1), R(3,2), B(2,2) [4-cycle]
- (R=2, B=3): we can extend (2,1) by adding more pieces.
- Actually, we can construct a "zigzag" cycle that has exactly 2 reds and B blues, and then if R > 2, we add more reds along the path.

Better: Build a cycle that is a long path that goes right, down-left, right, down-left, etc., and then returns.
For example, the 4-cycle (2,2): R(1,1) -> B(2,1) -> R(3,2) -> B(2,2) -> R(1,1).
This has 2 reds and 2 blues. We can generalize to 2 reds and B blues by extending the middle part.
For B=1: R(1,1) -> B(2,1) -> R(1,2). That's 2R,1B.
For B=2: above.
For B=3: R(1,1) -> B(2,1) -> R(3,2) -> B(4,3) -> B(3,4)? No.
Let's find a pattern for 2 reds and B blues.
We want a cycle with 2 reds and B blues. The two reds must be connected to blues. In the 3-cycle, the two reds are connected via the blue. In the 4-cycle, the two reds are also connected via a path of two blues. So we can have a path: R1 -> B1 -> B2 -> ... -> B_B -> R2 -> R1? But R2 -> R1 must be valid (orthogonal). In the 3-cycle, R2(1,2) -> R1(1,1) is orthogonal. In the 4-cycle, R2(3,2) -> R1(1,1)? That's not orthogonal; (3,2) to (1,1) is not adjacent. Wait, in the 4-cycle, the last piece is B(2,2) -> R(1,1). So R2 is not adjacent to R1; B_B is adjacent to R1. So the cycle is: R1 -> B1 -> B2 -> ... -> B_B -> R1? But that would have only 1 red if B_B goes to R1. We need 2 reds. So the path is: R1 -> B1 -> B2 -> ... -> B_{B-1} -> R2 -> R1? Then we have B blues, 2 reds. Let's try:
R1(1,1) -> B1(2,1) -> B2(3,2) -> B3(4,3) -> ... -> B_{B-1}(B, B) -> R2(?, ?) -> R1(1,1).
R2 must be orthogonal to B_{B-1} and orthogonal to R1. Also R2 must be placed such that the path of blues is a diagonal line.
The blues are on the diagonal: (2,1), (3,2), (4,3), ..., (B, B-1)? Wait, (2,1) to (3,2) is diagonal. (3,2) to (4,3) diagonal. So B_i = (i+1, i) for i=1..B-1. Then B_{B-1} = (B, B-1). We need R2 adjacent to (B, B-1) orthogonally, and adjacent to (1,1) orthogonally. Orthogonal neighbors of (B, B-1): (B-1, B-1), (B+1, B-1), (B, B-2), (B, B). Orthogonal neighbors of (1,1): (1,2), (2,1). Intersection? We need R2 to be adjacent to both. The distance between (1,1) and (B, B-1) is large. They have no common orthogonal neighbor unless B is small. For B=2, B_{B-1}=B1=(2,1). Orthogonal to (2,1): (1,1),(3,1),(2,2). Orthogonal to (1,1): (1,2),(2,1). Intersection: (2,1) but that's B1. So R2 would be (1,1) which is R1. So for B=2, we need a different arrangement (the 4-cycle we found uses two blues not in a line: B(2,1) and B(2,2), with R(1,1) and R(3,2)).

So the linear diagonal chain doesn't close nicely with 2 reds for B>2.

Alternative: Use a cycle that has more reds, but we can control counts.
General construction for R>0, B>0, R even:
We can build a cycle that is a "ladder" with rungs.
Consider a cycle that goes:
(1,1) -> (1,2) -> (2,3) -> (3,3) -> (3,2) -> (2,1) -> (1,1).
This is a 6-cycle? Let's list: (1,1) to (1,2) right. (1,2) to (2,3) diagonal down-right. (2,3) to (3,3) down. (3,3) to (3,2) left. (3,2) to (2,1) diagonal up-left. (2,1) to (1,1) up.
Colors: we can assign R to orthogonal moves, B to diagonal moves.
Moves:
(1,1) -> (1,2): orthogonal -> piece at (1,1) must be R.
(1,2) -> (2,3): diagonal -> piece at (1,2) must be B.
(2,3) -> (3,3): orthogonal -> piece at (2,3) must be R.
(3,3) -> (3,2): orthogonal -> piece at (3,3) must be R.
(3,2) -> (2,1): diagonal -> piece at (3,2) must be B.
(2,1) -> (1,1): orthogonal -> piece at (2,1) must be R.
Total: R at (1,1), (2,3), (3,3), (2,1) -> 4 reds.
B at (1,2), (3,2) -> 2 blues.
So this is a (4R, 2B) cycle.
We can extend this pattern!
Generalize: The cycle has a top horizontal segment, a diagonal down-right, a vertical segment, a bottom horizontal segment, a diagonal up-left, a vertical segment back to start.
Coordinates:
Start at (1,1).
Go right to (1, k): (1,1) -> (1,2) -> ... -> (1,k). All orthogonal -> k reds.
Then diagonal down-right: (1,k) -> (2, k+1). Diagonal -> 1 blue.
Then go down to (m, k+1): (2, k+1) -> (3