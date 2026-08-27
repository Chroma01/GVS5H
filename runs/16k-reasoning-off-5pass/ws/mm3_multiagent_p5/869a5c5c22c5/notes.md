
## ideation
The core difficulty is determining when a Hamiltonian-like cycle exists in a mixed-move graph (red: orthogonal, blue: diagonal) and constructing it.

Key observations:
1. **Color parity constraint**: On a checkerboard, orthogonal moves flip color, diagonal moves preserve color. In the cycle, each red piece contributes one color flip. To return to the start, the number of red pieces R must be **even**. (Including R=0.)
2. **R=0, B≥2**: Two blues diagonally adjacent form a cycle.
3. **R=1**: Odd, impossible regardless of B.
4. **R≥2, R even**: Always possible for any B≥0.

Construction idea (for R≥2 even, B≥0):
- Use a "base" of R reds arranged so they form a valid cycle with only orthogonal moves.
- For B=0, R=2k: place reds in a 2×k grid perimeter (snake).
- For B>0: extend by inserting blue pieces into the cycle.

However, a single robust construction that works for all (R even, B≥0) is needed. One clean method:
- For R=2, handle B=0,1,2,3 directly (small cases), but for R=2 with large B, we need R>2. Wait — R is given. We must handle R=2, B=100.

Actually, with R=2, B=100: the two reds must be orthogonally adjacent, and all 100 blues form a diagonal path from a neighbor of R₁ to a neighbor of R₂. By choosing R₁, R₂, B₁, B_last appropriately and using a long diagonal path (which can be arbitrarily long on the infinite grid), this is always possible. The path length constraint is satisfiable because we can route the diagonal path arbitrarily far away.

For example, R₁=(1,1), R₂=(1,2), B₁=(2,1), B_last=(2,1000001) (if reachable). But B_last must be diag-adj to R₂=(1,2), so B_last ∈ {(0,1),(0,3),(2,1),(2,3)}. Only 4 choices! So B_last is fixed to one of these, and the path length from B₁=(2,1) to B_last is limited (≤3 as computed).

So R=2 is severely limited! We need R≥4 to handle arbitrary B.

Revised condition: Yes iff R is even AND R≥2 (which is equivalent to: R even, and if R=0 then B≥2 which is given, and R=2 with B≤3, and R≥4 even for any B).

Wait, the problem says R+B ≥ 2. For R=2, B=4: I showed it's impossible. So R=2, B≥4 is No.

Let me verify: is R=2, B=4 really impossible? The cycle has 6 pieces: R, B, B, B, B, R. Two reds orth-adj. Four blues in a diagonal path. R₁→B₁ (orth), B₁→B₂→B₃→B₄ (diag), B₄→R₂ (diag), R₂→R₁ (orth).

Parity: B₁, B₂, B₃, B₄ all same parity. R₁ has opposite parity. R₂ has same parity as B's (since R₂ orth to R₁ and B₄ diag to R₂, so R₂ parity = B₄ parity = B's parity).

B₁ is orth-adj R₁ (3 choices excluding R₂). B₄ is diag-adj R₂ (4 choices). The diagonal path from B₁ to B₄ has 3 steps (4 nodes). The parity of r+c on the diagonal path is fixed. 

For R₁=(1,1), R₂=(1,2): B₁ must be parity 1 (opposite to R₁). B₁=(2,1) [only valid choice excluding (1,2) and out-of-bounds]. B₄ must be parity 1 and diag-adj R₂=(1,2): (0,1)OOB, (0,3)OOB, (2,1)=B₁, (2,3). So B₄=(2,3). Path (2,1)→?→?→(2,3) with 3 diag steps. (2,1) and (2,3) differ by (0,2). Need 3 steps with |Δr|=0, |Δc|=2. After 3 diag steps, Δr ≡ 3 (mod 2) = 1, but |Δr|=0 ≡ 0. Contradiction. So impossible.

With different R₁,R₂: R₁=(r,c), R₂=(r,c+1). B₁ orth-adj R₁, parity c+1: (r+1,c),(r-1,c),(r,c-1). B₄ diag-adj R₂=(r,c+1), parity c+1: (r-1,c),(r-1,c+2),(r+1,c),(r+1,c+2). 
For the path to have odd length (3 steps = odd), we need B₁ and B₄ to have |Δr| and |Δc| of the same parity as 3 (odd). 
If B₁=(r,c-1), B₄=(r-1,c): Δ=(-1,1), |Δr|=1 odd, |Δc|=1 odd. 3 steps, m=3 odd, consistent. Path (r,c-1)→(r-1,c) in 3 steps. m=3, |Δr|=1, |Δc|=1. Possible: (r,c-1)→(r-1,c)→(r-2,c+1)→(r-1,c+2)? Ends at (r-1,c+2), not (r-1,c). Or (r,c-1)→(r+1,c)→(r,c+1)=R₂ no. (r,c-1)→(r-1,c)→(r,c+1)→(r-1,c) but (r,c+1)=R₂ and revisit. 
Actually to end at (r-1,c) in 3 steps from (r,c-1): we need to wander and return. The walk must have net Δr=-1, Δc=1. After 3 steps, the position is (r-1,c) with 3 steps. One such path: (r,c-1)→(r-1,c)→(r-2,c+1)→(r-1,c). But the second-to-last is (r-2,c+1) and last is (r-1,c). The path is (r,c-1),(r-1,c),(r-2,c+1),(r-1,c) — but (r-1,c) appears twice! Not a simple path. 
Another: (r,c-1)→(r+1,c)→(r,c+1)→(r-1,c) — (r,c+1)=R₂ occupied.
Another: (r,c-1)→(r-1,c)→(r-2,c-1)→(r-1,c) — (r-1,c) twice.
Hmm, it seems hard to have a simple path of odd length between two specific points on the diagonal graph.

In fact, the diagonal graph (squares of fixed parity, edges between (±1,±1) neighbors) is bipartite? Let's check: (r,c)→(r+1,c+1): (r+c)→(r+c+2), same parity. So the graph on same-parity squares: is it bipartite? We need a 2-coloring. Color by (r-c) mod 2? (r,c)→(r+1,c+1): (r-c)→(r-c), same. (r,c)→(r+1,c-1): (r-c)→(r-c+2), same. So (r-c) mod 2 is preserved. So the graph is bipartite with parts (r-c) even and (r-c) odd. And a path of length m stays in one part if m is even, switches parts if m is odd.

For B₁=(r,c-1): r-(c-1)=r-c+1. For B₄=(r-1,c): (r-1)-c=r-c-1. These have different (r-c) parities. So they are in different parts of the bipartite graph. Therefore the path length must be ODD. B=4 means path of 3 blues = 2 edges... wait.

Let me recount. B=4 blues: B₁, B₂, B₃, B₄. The path is B₁→B₂→B₃→B₄, which is 3 edges. m=3 edges. For them to be in different parts, need m odd. 3 is odd. ✓ So parity of parts is fine. But we also need a simple path of length 3.

(r,c-1) and (r-1,c): different (r-c) parity. The graph distance (shortest path) between them: (r,c-1)→(r-1,c) is 1 step (diag). So distance 1. A path of length 3 would need to go there and back, which revisits. So no simple path of length 3.

General: if B₁ and B₄ are at graph distance d, any path between them has length ≥ d. For a simple path of length m, we need m ≥ d. Also, if they're in different parts, m must be odd. If same part, m even.

So for the construction to work with R=2, B large, we need B₁ and B_last at large graph distance. But B₁ and B_last are constrained (near R₁ and R₂). The max distance is limited. 

For R₁=(1,1), R₂=(1,2), the farthest B₁ and B_last are at graph distance... B₁ parity 1: (2,1),(0,1)OOB,(1,0)OOB,(1,2)=R₂. So B₁=(2,1). B_last parity 1, diag-adj R₂: (0,1)OOB,(0,3)OOB,(2,1)=B₁,(2,3). So B_last=(2,3). Distance between (2,1) and (2,3): (0,2), need m≥2, m≡0(mod 2). m=2 gives B=3. m=4 gives B=5? (2,1) to (2,3) in 4 steps: (2,1)→(3,2)→(4,3)→(3,4)→(2,3). Check: diag steps, no revisit, ends at (2,3). ✓ So B=5 works with this choice!

Wait, B=4 blues: path B₁→B₂→B₃→B₄, 3 edges, m=3. (2,1) to (2,3) in 3 steps. Distance 2, but m=3 (odd). (2,1) and (2,3) have same (r-c): (2-1)=1, (2-3)=-1≡1. Same part. So path length must be even. 3 is odd. Impossible. ✓

B=5: 5 blues, 4 edges, m=4 even. Same part. m=4≥2. Path (2,1)→(3,2)→(4,3)→(3,4)→(2,3). ✓

B=6: 6 blues, 5 edges, m=5 odd. Different parts needed, but (2,1) and (2,3) same part. Impossible.
B=7: m=6 even, same part. m=6≥2. Path possible. 

So for R₁=(1,1), R₂=(1,2), B₁=(2,1), B_last=(2,3): B must be odd (3,5,7,...). B=1: m=0, B₁=B_last, B_last=(2,1) must be diag-adj R₂. (2,1) diag-adj (1,2): |1|+|-1|? |2-1|=1,|1-2|=1. Yes! So B=1: B₁=B_last=(2,1). B=3,5,7,...

Similarly, we can get even B with other choices. So for R=2, all B≥1 are achievable! We just need to pick the right configuration.

Actually, the constraint is: the path from B₁ to B_last (through B-2 internal nodes) must exist as a simple path of length B-1. This is possible iff B-1 ≥ d and B-1 ≡ d (mod 2), where d is the graph distance, AND we can find a simple path of that exact length.

For the diagonal graph on same-parity squares (which is connected and we can make paths of any length ≥ d with the correct parity), this is always possible on a sufficiently large board. Since the board is 1e9 × 1e9, we have plenty of room.

So the answer is: **Yes iff R is even** (and if R=0, B≥2 which is given; if R=2, any B≥0; etc.).

Wait, but the cycle structure for R=2, B=0 is just two orth-adj reds. For R=2, B≥1, we showed it works for various B. The remaining case: can we always find a simple diagonal path of the required length? Yes, because the diagonal graph is Hamiltonian-connected enough; we can always route around obstacles on a large board.

For a clean solution, the condition is simply: **R is even** (i.e., R % 2 == 0), AND if R=0 then B≥2 (given), AND the construction exists.

Actually, the problem says R+B ≥ 2. So R=0, B=1 is invalid input (R+B=1). R=0, B≥2: yes. R=1: no. R≥2 even: yes.

So the condition is: **R is even** (which includes R=0, and R≥2 even; R=1 is odd so no).

Wait, R=0 is even. R=0, B≥2: yes. R=2, B=0: yes. R=1: no.

So simply: Yes if and only if R is even.

Hmm, but is R=0, B=2: (1,1)B, (2,2)B. (1,1)→(2,2) diag ✓, (2,2)→(1,1) diag ✓. Yes.

And the construction needs to be provided.

For the construction, I'll use a general method that works for all R even, B≥0.

**General construction for R even, B≥0:**

If R=0, B=2: place two blues at (1,1) and (2,2).
If R=2: use the method above (find R₁, R₂ orth-adj, B₁ orth-adj R₁, B_last diag-adj R₂, and a diagonal path).
If R≥4 even: use a larger construction.

Actually, for R≥2 even, here's a clean construction that I recall:

Place the cycle as follows (R reds and B blues):
- Make a "ladder" with 2 rows.
- Top row: place pieces going right.
- Bottom row: place pieces going left.
- Connect with vertical pieces.

Specifically, for R=2k (k≥1), B any:
- Place 2 reds at the "turning points".
- For B blues, distribute them in the straight sections.

But this is complex. Let me use a simpler explicit construction.

**Simple construction (works for R≥2 even, B≥0):**

Case 1: B=0. R=2k. Place reds in a 2×k rectangle perimeter:
(1,1), (1,2), ..., (1,k), (2,k), (2,k-1), ..., (2,1). This is 2k pieces, all orth-adj consecutively, and (2,1)→(1,1) is orth. ✓

Case 2: B≥1, R≥2 even. 
Place R₁ at (1,1), R₂ at (1,2). 
For the blues, place them in a diagonal path from (2,1) to (2, 2B+1) or something, and close with R₂ at the end.

Wait, I need B_last to be diag-adj to R₂. So B_last is at (2,3) (diag-adj to (1,2)). Then the diagonal path from (2,1) to (2,3) has B-1 edges (B blues including endpoints). For B=1: path length 0, B₁=B_last=(2,1), which is diag-adj (1,2)? (2,1) and (1,2): |1|,|1|. Yes! ✓
For B=3: path length 2, (2,1)→(3,2)→(2,3). ✓
For B=5: path length 4, (2,1)→(3,2)→(4,3)→(3,4)→(2,3). ✓
For B=2: need (2,1)→(2,3) in 1 step. Not possible (distance 2).
For B=4: (2,1)→(2,3) in 3 steps. (2,1) and (2,3) same (r-c) part, need even length. 3 is odd. No.
For B=6: 5 steps, odd, no.

So this specific configuration only gives odd B. For even B, use a different config.

For even B with R=2: R₁=(1,1), R₂=(1,2), B₁=(1,0)OOB. Hmm. 
R₁=(1,1), R₂=(2,1) [vertical]. B₁ orth-adj R₁: (2,1)=R₂, (0,1)OOB, (1,2), (1,0)OOB. B₁=(1,2). B_last diag-adj R₂=(2,1): (1,0)OOB, (1,2)=B₁, (3,0)OOB, (3,2). B_last=(3,2). Path (1,2)→(3,2): Δ=(2,0). d=2. Need m≥2, m≡0(mod 2). B-1=m. 
B=2: m=1, 1<2. No.
B=3: m=2. Path (1,2)→(2,3)→(3,2). ✓ (B=3 again)
B=4: m=3 odd, (1,2) and (3,2): (1-2)=-1, (3-2)=1, same part, need even. No.
B=5: m=4. Path (1,2)→(2,3)→(3,4)→(2,3) no revisit. (1,2)→(2,1)→(3,2)→...→(3,2)? Need to end at (3,2). (1,2)→(2,3)→(3,2)→(2,3)→(3,2) revisit. Hmm.
Actually, for a simple path of length 4 from (1,2) to (3,2): we can go (1,2)→(2,3)→(3,2)→... but that's already 2 steps. To make 4 steps: (1,2)→(2,3)→(1,4)→(2,3) no. (1,2)→(2,3)→(3,4)→(2,5)→(3,4) no. 
Let me think: (1,2) and (3,2) differ by (2,0). A path of length 4 with net (2,0). Steps: e.g., (1,1)+(1,1)=(2,2) no. We need Σ(εᵢ,δᵢ) = (2,0), each |εᵢ|=|δᵢ|=1. So 2 steps +1 in r, 2 steps -1 in r, net 0... wait, Σεᵢ=2, Σδᵢ=0. εᵢ∈{±1}, so 4 steps: say two +1 and two -1, sum=0≠2. To get sum=2, need three +1 and one -1, but then Σ|εᵢ|=4 and 3+1=4, sum=2. And Σδᵢ=0: δᵢ∈{±1}, need two +1 and two -1. So the 4 steps have specific signs. One path: (+1,+1), (+1,-1), (+1,+1), (-1,-1)? Sum: (3-1, 1-1)=(2,0). Positions: (1,2)→(2,3)→(3,2)→(4,3)→(3,2). But (3,2) is the endpoint and (2,3)→(3,2) is in the middle. The path is (1,2),(2,3),(3,2),(4,3),(3,2). Revisit at (3,2). Not simple.
Another: (1,2)→(2,1)→(3,2)→(2,3)→(3,2). (2,1)=R₂? R₂=(2,1), yes! Occupied.
Hmm. With R₂=(2,1), we can't use (2,1) for a blue.

This is getting complicated. For the actual solution, I'll use a known clean construction.

**Clean construction (from competitive programming):**

For R even (R ≥ 0), B ≥ 0, with R+B ≥ 2:
- If R = 0: trivial (B blues in diagonal cycle, e.g., 2 blues at (1,1) and (2,2)).
- If R = 2, B ≤ 1: handle directly.
- If R ≥ 4 even OR (R=2 and B≥2): use a general construction.

Actually, the simplest general construction for R ≥ 2 even, any B:

Use the "comb" construction:
1. Place R₁ at (1,1).
2. Place R₂ at (1,2).
3. For each blue i (1 to B), place it and extend the path.
4. Close with the remaining reds.

Here's a construction that definitely works (I'll verify):

For R = 2k ≥ 2, B ≥ 0:
- The cycle visits: R, then a "tail" of blues, then the other R, then more structure.
- Actually, let me use a different approach: build a long path and close it.

**Final construction plan:**

Given the complexity, I'll implement the following known solution:

For R even, R ≥ 2, B ≥ 0:
- Place pieces in a "staircase" pattern.
- Specifically, the cycle is:
  (1,1)R → (1,2)B → (2,3)B → (1,4)B → (2,5)B → ... → (1, 2B)R → (1, 2B+1)R → (2, 2B+1)R → (2, 2B)R → ... 
  Hmm, this is ad hoc.

Let me look at the sample: R=2, B=3, output:
B 2 3
R 3 2
B 2 2
B 3 3
R 2 4

Wait, the first piece is B! The problem says "R red pieces and B blue pieces" and we place them in order. The first piece placed is B at (2,3), then R at (3,2), etc. So the cycle starts with B.

In this cycle: B(2,3)→R(3,2): diag (-1,-1)? (2,3) to (3,2): (1,-1), diag ✓. 
R(3,2)→B(2,2): orth (0,-1)... no, (3,2) to (2,2) is (-1,0), orth ✓ (red moves orth).
B(2,2)→B(3,3): diag (1,1) ✓.
B(3,3)→R(2,4): diag (-1,1) ✓.
R(2,4)→B(2,3): (2,4) to (2,3) is (0,-1), orth ✓ (red moves orth).
Wait, the last move is R(2,4)→B(2,3), and the first piece is B(2,3). So R₂₃₅→B₁. In the cycle, the last piece (5th) is R, which moves to the 1st piece B. R moves orth to B: (2,4)→(2,3) orth ✓.

So the cycle is: B₁, R₂, B₃, B₄, R₅. Two reds at positions 2 and 5: (3,2) and (2,4). These are NOT orthogonally adjacent! (3,2) and (2,4): |1|+|2|=3, not orth. 

Wait, in the cycle, consecutive pieces must be able to move. The 5th piece R(2,4) moves to the 1st piece B(2,3): orth ✓. But also, the two reds don't need to be adjacent in the cycle (they are at positions 2 and 5, with B₃,B₄ between them).

Ah! I see. The cycle has alternating structure but not necessarily R and B alternating. The two reds are at positions 2 and 5, with 3 blues between them (positions 3,4) and one blue before position 2 (position 1). So the path from R₂ to R₅ is: R(3,2)→B(2,2)→B(3,3)→R(2,4). R moves orth to B(2,2). B(2,2)→B(3,3) diag. B(3,3)→R(2,4) diag. And R(2,4)→B(2,3) orth. And B(2,3)→R(3,2) diag.

So the structure is not "R, blues, R" in a simple path, but rather the cycle is:
... R → B → B → R → B → R → B → B → R → B → ...

The two reds are connected by a path of blues, and the cycle is closed by the R→B→R connections.

In the sample: B₁(2,3) → R₂(3,2) [diag] → B₃(2,2) [orth] → B₄(3,3) [diag] → R₅(2,4) [diag] → B₁(2,3) [orth].

So R₂→B₃ is orth, B₄→R₅ is diag, R₅→B₁ is orth, B₁→R₂ is diag.

This is a cycle with two reds and three blues, where:
- R₂ → B₃: red moves orth.
- B₃ → B₄: blue moves diag.
- B₄ → R₅: blue moves diag.
- R₅ → B₁: red moves orth.
- B₁ → R₂: blue moves diag.

So between the two reds R₂ and R₅, there's a path B₃, B₄ (diag path). And the other connection is R₅ → B₁ → R₂ (R moves orth to B₁, B₁ moves diag to R₂).

So the general structure with R=2 reds: 
- Two reds Rₐ and R_b.
- A diagonal path of blues from B_right (diag-adj R_b) ... B_left (diag-adj Rₐ)? No.
- Actually: R_a → (orth) → B_start → (diag path) → B_end → (diag) → R_b → (orth) → B_close → (diag) → R_a.

This requires: R_a orth to B_start, B_end diag to R_b, R_b orth to B_close, B_close diag to R_a.
And B_start, ..., B_end is a diagonal path.
B_close is a single blue (or could be part of a path).

For R=2, the structure is:
- R₁ → B₁ (orth) → B₂ → ... → B_k (diag path, k-1 edges) → R₂ (diag) → B_{k+1} (orth) → B_{k+2} → ... → B_m (diag path) → R₁ (diag).

Wait, B_close must be diag-adj R₁. So the last blue before closing to R₁ must be diag-adj R₁. But in the cycle, the piece before R₁ (which is the last piece) moves to R₁. If the last piece is blue, it moves diag to R₁.

So: ..., B_last → R₁ (diag). And R₁ → B_first (orth).

So: B_last diag-adj R₁, B_first orth-adj R₁.
And R₂ → B_mid (orth), B_mid ... B_last-1 diag, B_last-1 diag-adj R₂? Hmm.

Let me re-examine the sample structure:
Position: 1:B, 2:R, 3:B, 4:B, 5:R
Moves: 1→2 (B diag to R), 2→3 (R orth to B), 3→4 (B diag), 4→5 (B diag), 5→1 (R orth to B).

So: R₂ → B₃ (orth), then B₃→B₄→R₅ (diag path of 2 blues connecting to R₅ via diag). Then R₅→B₁ (orth), then B₁→R₂ (diag).

So the two reds are R₂ and R₅. Between R₂ and R₅ in the cycle (going forward): R₂→B₃→B₄→R₅. This is: R orth to B, then B diag to B, then B diag to R. So it's a path of length 3 (3 edges) with 2 blues.

The other arc from R₅ back to R₂: R₅→B₁→R₂. R orth to B, B diag to R. Length 2, 1 blue.

So total blues = 2 + 1 = 3. ✓
And R₂→B₃ orth, B₃→B₄ diag, B₄→R₅ diag: so the first blue B₃ is orth-adj R₂, last blue B₄ is diag-adj R₅. And R₅→B₁ orth, B₁→R₂ diag: B₁ orth-adj R₅, B₁ diag-adj R₂.

So: B₁ is orth-adj R₅ AND diag-adj R₂.
B₃ is orth-adj R₂. B₄ is diag-adj R₅.
And B₃, B₄ are diag-adj (B₃→B₄ diag).

This is a specific configuration. For general B, we generalize the "middle" path B₃→B₄ to a longer diagonal path.

So the general structure with R=2:
- Two reds R_a, R_b.
- A blue B_close that is orth-adj R_b and diag-adj R_a.
- A diagonal path of blues from B_start (orth-adj R_a) to B_end (diag-adj R_b).
- Cycle: R_a → B_start → ... → B_end → R_b → B_close → R_a.

For this to work:
1. B_close orth-adj R_b and diag-adj R_a.
2. B_start orth-adj R_a.
3. B_end diag-adj R_b.
4. B_start, ..., B_end is a diagonal path (consecutive diag).

And all positions distinct.

From 1: B_close is at a position that is both orth-adj R_b and diag-adj R_a. 
From 2: B_start orth-adj R_a.
From 3: B_end diag-adj R_b.
4: diagonal path from B_start to B_end.

Also, R_a and R_b: no direct constraint (they don't need to be adjacent; the cycle connects them through blues).

This gives much more flexibility! Because B_close connects R_b to R_a via orth+diag, and the main path connects R_a to R_b via orth+diag-path.

For B=0: no blues. R_a→R_b→R_a. R_a moves to R_b: but they're both red, so orth. R_b moves to R_a: orth. So R_a, R_b orth-adj. This is the R=2, B=0 case.

For B=1: one blue. Could be B_close (with empty middle path): R_a → R_b → B → R_a. Then R_b→B orth, B→R_a diag. So B orth-adj R_b, B diag-adj R_a. R_a, R_b orth-adj (from the R_a→R_b move).
Example: R_a=(1,1), R_b=(1,2) [orth]. B orth-adj R_b: (2,2),(0,2)OOB,(1,3),(1,1)=R_a. Excluding R_a: (2,2),(1,3). B diag-adj R_a=(1,1): (0,0)OOB,(0,2)OOB,(2,0)OOB,(2,2). So B=(2,2). Check: (1,2)R→(2,2)B orth ✓, (2,2)B→(1,1)R diag (-1,-1) ✓. Cycle (1,1)R,(1,2)R,(2,2)B. But wait, order: R_a→R_b→B→R_a means placement 1:R_a, 2:R_b, 3:B. Then 3rd B→1st R_a: (2,2)→(1,1) diag ✓. And 1st R_a→2nd R_b: (1,1)→(1,2) orth ✓. 2nd R_b→3rd B: (1,2)→(2,2) orth ✓. 

For B=3 (sample): R_a=(1,1), R_b=(1,2)? Let's try: B_close=(2,2) [as above]. Middle path: B_start orth-adj R_a=(1,1): (2,1),(0,1)OOB,(1,2)=R_b,(1,0)OOB. B_start=(2,1). B_end diag-adj R_b=(1,2): (0,1)OOB,(0,3)OOB,(2,1)=B_start? possibly,(2,3). If middle has 1 blue (B=3 total, B_close is 1, middle has 1 blue: B_start=B_end). Then B_start=B_end must be orth-adj R_a AND diag-adj R_b. (2,1) diag-adj (1,2): (1,1) yes ✓. So middle blue=(2,1). Cycle: R_a(1,1)→B_start(2,1)→R_b(1,2)→B_close(2,2)→R_a(1,1). 
Check: (1,1)→(2,1) orth ✓, (2,1)→(1,2) diag ✓, (1,2)→(2,2) orth ✓, (2,2)→(1,1) diag ✓. ✓
This gives: R(1,1), B(2,1), R(1,2), B(2,2). 2 reds, 2 blues. But sample has B=3.

For B=3: middle path has 2 blues (B_close is 1). B_start=(2,1), B_end diag-adj R_b=(1,2): excluding (2,1), B_end=(2,3). Diagonal path (2,1)→(3,2)→(2,3). 
Cycle: R_a(1,1)→B₁(2,1)→B₂(3,2)→B₃(2,3)→R_b(1,2)→B_close(2,2)→R_a(1,1).
Check: (1,1)→(2,1) orth ✓, (2,1)→(3,2) diag ✓, (3,2)→(2,3) diag ✓, (2,3)→(1,2) diag ✓, (1,2)→(2,2) orth ✓, (2,2)→(1,1) diag ✓. 
This is: R(1,1), B(2,1), B(3,2), B(2,3), R(1,2), B(2,2). 
Sample is: B(2,3), R(3,2), B(2,2), B(3,3), R(2,4). Different positions but same structure (just translated/rotated).

So the general construction for R=2, B≥0:
- R_a=(1,1), R_b=(1,2).
- B_close=(2,2) [orth-adj R_b, diag-adj R_a].
- Middle path: B_start=(2,1), then diagonal path to B_end=(2, 2B-1) or something? 
  Actually, B_end must be diag-adj R_b=(1,2), so B_end ∈ {(0,1)OOB,(0,3)OOB,(2,1),(2,3)}. So B_end is fixed to (2,3) (if B_start=(2,1)) or (2,1) (if path length 0).
  
  The diagonal path from (2,1) to (2,3) has length ≥2. Number of internal blues (excluding endpoints) can be 0,1,2,... corresponding to path length 2,4,6,... (even lengths, since same (r-c) part).
  
  Path length = number of edges = (number of middle blues) - 1 + 1 = number of middle blues. Wait, middle has k blues: B_start, B₂, ..., B_k=B_end. Path edges = k-1. And B_end=(2,3), B_start=(2,1). Path length k-1, need k-1 ≥ 2 (distance) and k-1 even (same part). So k-1 ∈ {2,4,6,...}, k ∈ {3,5,7,...}. 
  
  But B can be any value! For even k-1, we get odd k (number of middle blues). Total B = middle blues + 1 (B_close). So B = k+1 ∈ {4,6,8,...} (even) or for k=1 (B_start=B_end), B=2.
  
  Wait k=1 means middle has 1 blue = B_start=B_end. Then B_start=(2,1) must be diag-adj R_b=(1,2). (2,1) to (1,2): (1,1) diag ✓. So k=1 works, B=2.
  
  For k=3 (B=4): path (2,1)→(3,2)→(2,3), length 2. ✓
  For k=5 (B=6): (2,1)→(3,2)→(4,3)→(3,4)→(2,3), length 4. ✓
  
  So this gives B ∈ {2,4,6,8,...} and B=1 (no middle, just B_close... wait B=1: only B_close, no middle blues, but then R_a→R_b with no blues? That's B=0. For B=1: R_a→B_close→R_b→... hmm, structure is R_a→[middle]→R_b→B_close→R_a. If middle is empty, R_a→R_b directly. Then R_b→B_close→R_a. So cycle: R_a, R_b, B_close. R_a→R_b orth, R_b→B_close orth, B_close→R_a diag. This is the B=1 case! And B_close=(2,2), R_a=(1,1), R_b=(1,2). Cycle: (1,1)R,(1,2)R,(2,2)B. Moves: (1,1)→(1,2) orth, (1,2)→(2,2) orth, (2,2)→(1,1) diag ✓. B=1 with this structure. But earlier I computed B=1 needs B₁=B_last with the other structure. Here B=1 works with R_a,R_b,(2,2).
  
  So with R_a=(1,1), R_b=(1,2), B_close=(2,2): we get B ∈ {1, 2, 3, 4, 5, ...}? 
  B=1: R_a, R_b, B_close. ✓
  B=2: middle has 1 blue (2,1). Cycle: R_a, (2,1), R_b, B_close. (1,1)→(2,1) orth, (2,1)→(1,2) diag, (1,2)→(2,2) orth, (2,2)→(1,1) diag. ✓
  B=3: middle has 2 blues (2,1),(3,2). Wait, B=3: middle 2 blues + B_close 1 = 3. Path (2,1)→(3,2)→? But B_end=(2,3). (3,2) to (2,3): diag ✓. So (2,1),(3,2),(2,3). But wait, that's 3 middle blues, B=4. Let me recount.
  
  Total B = (middle blues) + 1.
  B=1: middle 0 blues. Cycle: R_a, R_b, B_close. (1,1),(1,2),(2,2). ✓
  B=2: middle 1 blue. Cycle: R_a, B_mid, R_b, B_close. (1,1),(2,1),(1,2),(2,2). The move B_mid→R_b: (2,1)→(1,2) diag ✓. And we need the path to be valid: R_a→B_mid orth, then B_mid→R_b diag. So middle is just 1 blue, and the "path" is R_a→B→R_b. But B must be both orth-adj R_a (for R_a→B) and diag-adj R_b (for B→R_b). (2,1) orth-adj (1,1) ✓, diag-adj (1,2) ✓. ✓
  B=3: middle 2 blues. B_start orth-adj R_a, B_end diag-adj R_b, path B_start→B₂→B_end. B_start=(2,1), B_end=(2,3). B₂=(3,2). Cycle: (1,1),(2,1),(3,2),(2,3),(1,2),(2,2). Moves: (1,1)→(2,1) orth, (2,1)→(3,2) diag, (3,2)→(2,3) diag, (2,3)→(1,2) diag, (1,2)→(2,2) orth, (2,2)→(1,1) diag. ✓ B=3.
  B=4: middle 3 blues. (2,1)→(3,2)→(4,3)→(3,4)→(2,3) is 4 blues, B=5. For 3 blues: (2,1)→(3,2)→(2,3) is 2 blues (B_start,B₂=B_end), that's B=3. (2,1)→(1,2)→(2,3): (1,2) is R_b, can't use. (2,1)→(3,2)→(4,1)→(3,2) revisit. Hmm. 
  Distance from (2,1) to (2,3) is 2. Path of 2 blues (1 edge apart? no, 3 blues means 2 edges). Distance 2, path length 2. (2,1)→(3,2)→(2,3). 2 edges, 3 nodes. So 3 middle blues = path length 2 = distance. That works and is the shortest. For 4 middle blues (path length 3): need a path of length 3 from (2,1) to (2,3). Distance 2, but we need length 3 (odd). (2,1) and (2,3) same (r-c) part, need even length. 3 is odd. Impossible.
  So B=4 is impossible with B_start=(2,1), B_end=(2,3).
  
  For B=4, we need a different B_start or B_end. B_end diag-adj R_b=(1,2) must be (2,3) [only valid besides (2,1),(0,1),(0,3)OOB]. So B_end=(2,3) is forced if B_start=(2,1). 
  What if B_start is different? B_start orth-adj R_a=(1,1), not R_b=(1,2): (2,1),(0,1)OOB,(1,0)OOB. Only (2,1). So B_start=(2,1) is forced. Then B_end=(2,3) forced. And the path from (2,1) to (2,3) has even length only. So B-1 (middle blues) must give even path length. Path length = (middle blues) - 1 if we count the path as B_start→...→B_end. For middle blues m, path length m-1. Need m-1 even, m odd. So m ∈ {1,3,5,7,...}. B = m+1 ∈ {2,4,6,8,...}.
  
  And B=1 (m=0): no middle, direct R_a→R_b. ✓
  
  So this gives B ∈ {1, 2, 4, 6, 8, ...}. Missing B=3,5,7,... 
  But B=3 works with m=2: path (2,1)→(3,2)→(2,3), length 2. m-1=1, 1 is odd. But distance is 2, and we need length ≥2. Length 1 is impossible (distance 2). Wait, m=2 means 2 middle blues: B_start, B₂=B_end. Path length 1. But (2,1) to (2,3) distance 2, need length ≥2. Contradiction?
  
  Oh I see my error. If m=2 middle blues, the path is B_start → B₂ → ... → B_m=B_end. That's m-1 = 1 edge. But distance between B_start and B_end is 2 (in the diagonal graph). So a path of length 1 is impossible. 
  But earlier I said B=3 works with middle blues (2,1),(3,2),(2,3) — that's 3 middle blues! Let me recount.
  
  In the B=3 cycle: (1,1)R, (2,1)B, (3,2)B, (2,3)B, (1,2)R, (2,2)B. 
  The "middle" path is R_a(1,1)→B(2,1)→B(3,2)→B(2,3)→R_b(1,2). 
  So from R_a to R_b: R_a, then 3 blues (2,1),(3,2),(2,3), then R_b.
  So middle blues = 3. B_close = 1 (at (2,2)). Total B = 4? But the cycle has 4 blues! Wait: (2,1),(3,2),(2,3),(2,2) = 4 blues. So B=4, not 3.
  
  Let me recount the sample. Sample R=2, B=3. Output has 5 pieces: B, R, B, B, R. That's 2 R and 3 B. So B=3. In my cycle above I have 4 blues. That's wrong.
  
  Let me re-examine. For B=3 with R=2, structure R_a→[middle]→R_b→B_close→R_a. Middle has m blues, B_close is 1 blue. Total B = m+1 = 3, so m=2.
  Path: R_a → B₁ → B₂ → R_b, then R_b → B_close → R_a.
  B₁ orth-adj R_a, B₂ diag-adj R_b, B₁→B₂ diag.
  B_close orth-adj R_b, B_close diag-adj R_a.
  R_a=(1,1), R_b=(1,2). B_close=(2,2). B₁=(2,1), B₂ diag-adj R_b=(1,2) and diag-adj B₁=(2,1). B₂ diag-adj (1,2): (0,1)OOB,(0,3)OOB,(2,1)=B₁,(2,3). B₂=(2,3). B₂ diag-adj B₁=(2,1): |1|+|2|... (2,3) to (2,1): (0,-2), not diag. 
  So (2,1)→(2,3) not diag. No B₂ available. 
  
  But in the sample, B=3 works! Sample cycle: B(2,3)→R(3,2)→B(2,2)→B(3,3)→R(2,4)→B(2,3). 
  Let's identify R_a, R_b. The two reds are at (3,2) and (2,4). 
  R_a=(3,2), R_b=(2,4). 
  B_close: orth-adj R_b=(2,4) and diag-adj R_a=(3,2). 
  Orth-adj (2,4): (3,4),(1,4),(2,5),(2,3). 
  Diag-adj (3,2): (2,1),(2,3),(4,1),(4,3). 
  Intersection: (2,3). So B_close=(2,3). 
  Middle path: R_a→B₁→B₂→R_b. B₁ orth-adj R_a=(3,2): (4,2),(2,2),(3,3),(3,1). B₂ diag-adj R_b=(2,4): (1,3),(1,5),(3,3),(3,5). And B₁→B₂ diag.
  B₁=(2,2) (sample), B₂=(3,3) (sample). Check: B₁→B₂: (2,2)→(3,3) diag ✓. B₁ orth-adj R_a=(3,2): (2,2) to (3,2) is (1,0) orth ✓. B₂ diag-adj R_b=(2,4): (3,3) to (2,4) is (-1,1) diag ✓. 
  Full cycle: R_a(3,2), B₁(2,2), B₂(3,3), R_b(2,4), B_close(2,3). 
  Moves: (3,2)→(2,2) orth ✓, (2,2)→(3,3) diag ✓, (3,3)→(2,4) diag ✓, (2,4)→(2,3) orth ✓, (2,3)→(3,2) diag ✓. ✓
  
  So with R_a=(3,2), R_b=(2,4), this works. And B=3.
  
  So the configuration R_a=(1,1), R_b=(1,2), B_close=(2,2) does NOT give B=3, but a different configuration (translated/rotated) does.
  
  So for R=2, we need to choose the right R_a, R_b, B_close, B_start, B_end for each B. This is getting complicated.
  
  For the actual implementation, a simpler approach: since R can be larger, and for R≥4 we have a clean construction, and for R=2 the small B cases (0,1,2,3) cover what's needed... but B can be up to 2e5 with R=2.
  
  Actually, let me reconsider. For R=2 and any B, can we always find a configuration?
  
  We need: R_a, R_b, B_close, and a diagonal path of length B-1 (B-1 blues from B_start to B_end... wait).
  
  Let me re-derive. With R=2:
  Cycle: R_a → (path of blues) → R_b → B_close → R_a.
  The path from R_a to R_b: starts with R_a moving orth to a blue, then diagonal steps, ends with a blue moving diag to R_b.
  So: R_a → B_1 (orth) → B_2 (diag) → ... → B_k (diag) → R_b (diag).
  Then R_b → B_close (orth) → R_a (diag).
  
  So the "main path" has k blues, and B_close is 1 blue. Total B = k+1.
  Constraints:
  - B_1 orth-adj R_a (3 choices, excluding R_b).
  - B_k diag-adj R_b (4 choices).
  - B_1, ..., B_k is a diagonal path (k-1 edges).
  - B_close orth-adj R_b (3 choices excluding R_a) and diag-adj R_a.
  
  The diagonal path from B_1 to B_k: needs to exist as a simple path of length k-1.
  In the diagonal graph, the distance d between B_1 and B_k, and we need k-1 ≥ d and k-1 ≡ d (mod 2) (parity of path length matches part).
  And we need to be able to make a simple path of that exact length (on a large enough grid, yes, as long as k-1 ≥ d and parity matches, we can route around).
  
  For B_close: needs to exist. B_close is at intersection of orth-nbrs(R_b)\{R_a} and diag-nbrs(R_a).
  orth-nbrs(R_b) has 4 squares, one is R_a (if orth-adj). 
  diag-nbrs(R_a) has 4 squares.
  Intersection: the 4 orth-nbrs of R_b include R_a iff R_a is orth-adj R_b. If R_a, R_b are orth-adj, then 3 orth-nbrs of R_b remain, and we need one in diag-nbrs(R_a).
  The 4 diag-nbrs of R_a are at (R_a ± 1, R_a.c ± 1). The orth-nbrs of R_b (R_a ± 1, R_a.c) or (R_a, R_a.c ± 1) depending on direction.
  If R_b = (R_a.r, R_a.c + 1) [right]: orth-nbrs of R_b: (R_a.r+1, R_a.c+1), (R_a.r-1, R_a.c+1), (R_a.r, R_a.c+2), (R_a.r, R_a.c). Last is R_a. Remaining: (R_a.r±1, R_a.c+1), (R_a.r, R_a.c+2).
  diag-nbrs of R_a: (R_a.r±1, R_a.c±1). 
  Intersection: (R_a.r+1, R_a.c+1) and (R_a.r-1, R_a.c+1) are in both. So 2 choices for B_close.
  
  So B_close always exists when R_a, R_b orth-adj. Good.
  
  Now for the main path: B_1 orth-adj R_a (3 choices excluding R_b). B_k diag-adj R_b (4 choices). We need a diagonal path between them of length k-1 = B-2.
  
  Can we always find such? We need:
  1. Graph distance d ≤ B-2.
  2. B-2 ≡ d (mod 2).
  3. Simple path of length B-2 exists.
  
  For a large enough board, condition 3 is satisfied as long as 1 and 2 hold (the diagonal graph is "traceable" for paths of sufficient length with correct parity).
  
  Conditions 1&2: d ≤ B-2 and B-2 ≡ d (mod 2).
  
  The distance d between B_1 and B_k is at most... well, B_1 is near R_a and B_k is near R_b, and R_a, R_b are orth-adj (distance 1). So d is small (at most 3 or 4).
  
  If d is small (say 1,2,3), then for large B, B-2 is large and ≥ d, and parity can be matched by choosing appropriate B_1, B_k.
  
  Specifically, we have 3 choices for B_1 and 4 for B_k, giving distances d ∈ {1,2,3,...} with different parities. By choosing the right combination, we can make d have any value in some range, and for B-2 ≥ d with B-2 ≡ d (mod 2), we're good.
  
  Since B can be large and we have flexibility in choosing B_1, B_k, this is always satisfiable. 
  
  But implementing this generically is complex. For the problem, since R≥0 even and R+B can be large, but the condition is just "R is even", and the construction is complex...
  
  Given the time, I'll implement the condition check (R even → Yes, else No) and for the construction, use a known working approach.
  
  **For the implementation**, I'll use this construction:
  
  For R even, R ≥ 0, B ≥ 0 (with R+B ≥ 2):
  - If R = 0: output two blues at (1,1) and (2,2) (and handle B>2... wait R=0 means all blues. For B≥2, need a cycle of all blues. A cycle of B blues with diagonal moves: possible for any B≥2. E.g., place them in a diagonal line: (1,1),(2,2),(3,3),...,(B,B). Check: (i,i)→(i+1,i+1) diag ✓, and (B,B)→(1,1): (B-B, B-B)=(0,0), not a move. So not a cycle. For a cycle, need to close. (1,1)→(2,2)→...→(B,B)→(1,1): last move (B,B)→(1,1) is (1-B,1-B), |Δ|=B-1. For B=2: (2,2)→(1,1) diag ✓. For B=3: (3,3)→(1,1) (2,2), not diag (|2|≠1). So this doesn't work for B>2.
  
  For R=0, B≥2: need a cycle of B blues with diagonal moves. This is a cycle in the diagonal graph. The diagonal graph is bipartite (parts based on (r-c) mod 2) and has no odd cycles. So B must be even! But B can be odd. R=0, B=3: is it possible?
  
  R=0, B=3: three blues, each consecutive pair diag, and last→first diag. (1,1)→(2,2)→(3,1)→(1,1)? (3,1)→(1,1) is (2,0), not diag. (1,1)→(2,2)→(1,3)→(1,1)? (1,3)→(1,1) (0,2) not diag. 
  In the diagonal graph, cycle of length 3: (r,c)→(r+1,c+1)→(r+2,c)→(r+1,c-1)→... (r+2,c) to (r+1,c-1) is diag (-1,-1) ✓, then to (r,c) is diag (-1,+1) ✓. That's a 4-cycle: (r,c),(r+1,c+1),(r+2,c),(r+1,c-1). 
  3-cycle: need three mutually diag-adj squares. But diag graph: (r,c) neighbors are (r±1,c±1). Degree 4. Triangle? (r,c),(r+1,c+1),(r+1,c-1): (r+1,c+1) to (r+1,c-1) is (0,-2), not diag. So no triangle. The diagonal graph is bipartite (as shown), so no odd cycles. Therefore R=0, B odd is impossible!
  
  But the problem says R=0, B=1 is invalid (R+B≥2). R=0, B=3: impossible. R=0, B=2: possible.
  
  Hmm, but earlier I said R even is the condition. R=0 is even. R=0, B=3: is it possible? No. So the condition is not simply "R is even".
  
  Let me reconsider. For R=0, B≥2: possible iff B is even (since diagonal graph is bipartite, cycle must be even length).
  For R=1: impossible (R odd).
  For R=2: possible for any B? We need to verify.
  For R≥2 even: possible for any B?
  
  Wait, for R=0, the cycle uses only diagonal moves, so it's a cycle in the diagonal graph, which is bipartite, so B must be even.
  For R≥2 even, the cycle has orth moves (which connect the two parts) and diag moves, so it can be any length.
  
  Actually, the parity argument: R=0 means all moves are diagonal, cycle is in bipartite graph, B even.
  R=1 means one orth move, cycle is in graph that's... orth moves connect the two color classes, diag moves stay. With one orth move, the cycle has one "flip" of color class. For a cycle, need even number of flips. So R must be even.
  
  But for R=0, B odd: the cycle is entirely diagonal, so it's in one color class (all squares same color). But wait, diagonal moves preserve color, so the cycle stays in one color class, and a cycle in a bipartite graph must be even. So B even.
  
  So: R=0 → B even. R≥2 even → any B. R odd → impossible.
  
  But R=0, B=2: even ✓. R=0, B=4: even ✓. R=0, B=3: odd, impossible.
  
  Is R=0, B=1 possible? R+B=1, but R+B≥2, so invalid input.
  
  So the condition is:
  - If R is odd: No.
  - If R = 0: Yes iff B is even (and B≥2).
  - If R ≥ 2 even: Yes.
  
  Combined: Yes iff (R is even) and (R ≥ 2 or B is even).
  Since if R=0, we need B even. If R≥2, any B.
  
  But R=0, B=0: R+B=0, invalid. R=0, B=2,4,...: yes. R=0, B=1,3,...: no.
  
  Let me verify with constraints. The problem says 0≤R,B and 2≤R+B. So R=0,B=1 is not in input. R=0,B=3 is in input. For R=0,B=3: No.
  
  Hmm, but is this the intended condition? Let me double-check R=0,B=4: cycle of 4 blues. (1,1),(2,2),(3,3),(4,4): (4,4)→(1,1) (3,3) not diag. (1,1),(2,2),(3,1),(2,0)... (1,1)→(2,2)→(1,3)→(2,2) no. (1,1)→(2,2)→(3,1)→(2,0)OOB. 
  4-cycle: (1,1),(2,2),(1,3),(2,2)... no. (1,1),(2,2),(3,3),(2,4): (2,4)→(1,1) (1,3) not diag. (1,1),(2,2),(3,1),(2,0)OOB. (1,1),(2,2),(1,3),(2,4): (2,4)→(1,3) diag? (-1,-1) ✓, (1,3)→(1,1) (0,-2) no. (1,1),(2,2),(3,1),(4,2): (4,2)→(1,1) (3,1) not diag. 
  Actually, a 4-cycle in the diagonal graph: (r,c)→(r+1,c+1)→(r+2,c)→(r+1,c-1)→(r,c). Check: (r+2,c)→(r+1,c-1) diag (-1,-1) ✓, (r+1,c-1)→(r,c) diag (-1,+1) ✓. So (1,1),(2,2),(3,1),(2,0)... (2,0) has col 0, invalid. (1,2),(2,3),(3,2),(2,1): all valid. (2,1)→(1,2) diag (-1,+1) ✓. So cycle: (1,2)→(2,3)→(3,2)→(2,1)→(1,2). ✓ 4 blues, B=4, R=0. ✓
  
  So R=0, B=4: yes.
  
  OK so the condition is: **Yes iff (R is even) AND (R ≥ 2 OR B is even)**.
  
  Equivalently: R is even, and (R,B) ≠ (0, odd).
  Since R+B≥2, the only invalid even-R case is R=0, B odd (R=0,B=1 is already excluded by R+B≥2, but R=0,B=3,5,... are included).
  
  Wait, R=0, B=1: R+B=1, not allowed. R=0, B=3: R+B=3, allowed. And it's No.
  
  Let me re-examine. Is R=0, B=3 really impossible? Three blues, cycle of length 3 with diagonal moves. Diagonal graph is bipartite (parts: (r-c) even and odd). Any cycle alternates parts, so length is even. 3 is odd. Impossible. ✓
  
  So the answer is No for R=0, B odd.
  
  Now, for the construction, given the complexity, and since this is a well-known problem (I believe it's from AtCoder), I'll implement a construction that handles all valid cases.
  
  **Final construction plan:**
  
  For R ≥ 2 even, B ≥ 0:
  Use a "standard" construction. Here's one that works:
  
  Place the cycle as follows (I'll describe the positions in order):
  - (1,1) R
  - (1,2) R
  - (2,2) R
  - (2,1) R
  ... this is the R=4, B=0 case.
  
  For B > 0, we need to add blues. The trick is to use the "extra" space.
  
  Actually, here's a clean construction for R ≥ 2 even, B ≥ 0 that I'll implement:
  
  Let me use the following approach:
  - Make a "base" of 4 reds at (1,1),(1,2),(2,2),(2,1) [the 2×2 square, R=4].
  - But R might not be 4. 
  
  For R=2k (k≥1), B arbitrary:
  We can make a "ladder" with k rungs. The ladder has 2k reds on the perimeter, and we can insert blues.
  
  This is taking too long. Let me just implement a known solution.
  
  Given the time I've spent, I'll implement:
  1. Check condition: R even and (R≥2 or B even).
  2. For the construction, use a recursive or template-based approach.
  
  For the construction, I'll use:
  - R=0, B=2: (1,1)B, (2,2)B
  - R=0, B=4: (1,2)B, (2,3)B, (3,2)B, (2,1)B
  - R=0, B≥2 even: construct a cycle of B blues (e.g., using a long rectangle)
  - R=2, B=0: (1,1)R, (1,2)R
  - R=2, B≥1: use the construction with B_close and a diagonal path
  - R≥4 even, B=0: snake in 2×(R/2) grid
  - R≥4 even, B≥1: similar with blues
  
  Actually, here's a unified construction that works:
  
  For R ≥ 2 even, B ≥ 0:
  Output the cycle in this order (I'll build it):
  
  The key idea: make a long horizontal path of alternating R and B, with R at the ends and turns, and close it.
  
  Specifically, for R=2k ≥ 2:
  - Top row: R, B, R, B, ..., R (alternating, starting and ending with R, length 2k or so)
  - Right side: turn down
  - Bottom row: B, R, B, R, ..., B (going left)
  - Left side: turn up
  - Close.
  
  This is getting too complicated to design from scratch. Let me just code a solution that:
  1. Checks the parity condition.
  2. For valid cases, outputs a hardcoded construction for small (R,B) and a general construction for larger.
  
  Wait, I have another idea. Here's a simple construction for ALL valid cases (R even, R≥
