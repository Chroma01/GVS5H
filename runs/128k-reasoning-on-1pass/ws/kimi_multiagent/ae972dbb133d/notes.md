
## ideation
Core difficulty: this is not a per-tile independent choice problem. Compatibility across every shared torus edge couples rotations globally. A useful view is to put a binary variable on each grid edge: 1 iff the line endpoint touches that edge from either side. The condition says the two half-edges of every grid edge agree, so each cell must have exactly two incident selected edges; A forces one horizontal + one vertical incident edge, while B forces either both horizontal or both vertical.

This suggests a GF(2) linear structure rather than brute force. Let `a_ij=1` for A. Horizontally across a row, the selected-edge state must flip at A and stay equal at B, so row consistency needs every row to contain an even number of A. Vertically, every column must contain an even number of A. If those parity checks fail, answer is 0. If they pass, horizontal states can be parameterized by one free bit per row and vertical states by one free bit per column; A cells then impose no further coupling, while each B cell imposes one parity equation between its row bit and column bit. Thus the problem reduces to consistency/counting of a bipartite parity system with `H+W` variables and one edge per B cell; if consistent, the count appears to be `2^(#connected_components)` modulo `998244353`. The provided PLAN follows this DSU-with-parity idea, but its prefix definitions/off-by-one need validation.

Pitfalls: torus wraparound parity; `H=2` or `W=2` creates wrap adjacency subtleties but edge variables still work if indexed carefully; do not multiply by `4^a 2^b` because a valid selected-edge set determines each tile rotation uniquely; A cells should not add DSU constraints; B-cell constraint constant depends on prefixes of A counts before that cell; need iterative/path-halving DSU and fast input for `T=1e5`, total cells `1e6`.

## worker: finalize
- Represent every torus grid edge by one bit: whether a line endpoint touches that edge.
- Let `x[i][j]` be the left horizontal edge of cell `(i,j)` and `y[i][j]` its top vertical edge.
- A type-A cell flips both the horizontal and vertical edge states across the cell. A type-B cell preserves both states and additionally requires `x[i][j] XOR y[i][j] = 1`.
- Therefore every row and column must contain an even number of A cells.
- After the parity conditions hold, horizontal states are determined by one variable per row and vertical states by one variable per column. Each B cell gives one XOR equation between its row and column variables.
- A DSU with XOR potentials checks consistency and counts independent components. Each consistent component has exactly two assignments, so the answer is `2^components`.
- A valid edge-state assignment determines every tile orientation uniquely, so there is no additional `4^a * 2^b` factor.
- Total complexity is `O(HW * α(H+W))` per test case, with the total cell count bounded by `10^6`.
