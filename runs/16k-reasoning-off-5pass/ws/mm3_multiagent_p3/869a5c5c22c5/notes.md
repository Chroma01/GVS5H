
## ideation
The problem asks whether we can place R red and B blue pieces on a 10^9×10^9 board forming a single directed cycle where each piece can move to the next using its own movement rule (red: orthogonal, blue: diagonal). The board is large, so we just need to find conditions on R and B and provide explicit coordinates.

**Key observations**:
- The cycle does not need to alternate colors; any piece can move to any adjacent square (by its own rule).
- The graph is the "king move" graph (orthogonal + diagonal edges). We need a cycle using exactly R red nodes (each incident to 2 orthogonal edges in the cycle) and B blue nodes (each incident to 2 diagonal edges).
- In any cycle, the number of orthogonal edges equals R. Since each orthogonal move changes the parity of r+c, the number of orthogonal moves must be even, so **R must be even**.
- If B=0, the cycle is in the orthogonal grid (bipartite), so R must be even and ≥2. If R=0, the cycle is in the diagonal grid (also bipartite), so B must be even and ≥2.
- If R>0 and B>0, R even is sufficient (and necessary) except (R,B)=(1,1) which is already excluded.
- So the only "No" cases are: R odd, or (R=0 and B odd), or (R=1,B=1) (which is R odd). Since R+B≥2, (0,1) and (1,0) are not inputs.

**Construction for "Yes"**:
- **R=0, B even ≥2**: Use a diagonal rectangle cycle of length B. For B=2k, coordinates: for i=1..k: (i, i+1) and (i+1, i). Order: (1,2)→(2,3)→...→(k, k+1)→(k+1, k)→(k, k-1)→...→(2,1)→(1,2). All moves are diagonal.
- **B=0, R even ≥2**: Use an orthogonal rectangle cycle of length R. For R=2k, coordinates: (1,1)→(1,2)→...→(1,k)→(2,k)→(2,k-1)→...→(2,1)→(1,1). All moves orthogonal.
- **R>0, B>0, R even**: We build a parameterized "staircase" cycle. Use a path that goes right along a row (reds), diagonal down-right (blue), down a column (reds), left along a row (reds), diagonal up-left (blue), up a column back to start (reds). Adjust lengths to match exact R and B counts. For example, a base cycle with 4 reds and 2 blues: (1,1)→(1,2)→(2,3)→(3,3)→(3,2)→(2,1)→(1,1). Extend horizontal/vertical segments with extra reds. Add extra blues by inserting diagonal segments.

This covers all cases. We just need to implement the coordinate generator for each case.
