
## ideation
**Core difficulty:** The game is impartial and each move consists of adding exactly one edge that does not create an odd cycle. Because the initial graph has no odd cycle, it is bipartite, and the bipartition of each connected component is unique (up to swapping parts). Adding an edge that preserves bipartiteness forces the edge to lie inside one part. Therefore, every legal move adds an intra-part edge, never an inter-part one.

**Structure of the final graph:**  
Since no odd cycle may ever be created, inter-part edges are never allowed. Once all intra-part edges exist in a component, the component is exactly two cliques joined by the existing cross edges, and no further move is possible within that component.

**Available moves per component:**  
For a component with part sizes `a` and `b`:
- Total allowable edges: `C(a,2) + C(b,2)`.
- Pre-existing edges of that type: the graph is bipartite, so all current edges are cross edges; no intra-part edges exist yet.  
- Therefore, the number of legal moves in the component = `C(a,2) + C(b,2)`.

**Impartial game reduction:**  
Each move is a single edge addition; the move set per component is a pile of independent “tokens” — a Nim heap of size equal to the number of moves. The Grundy number of a heap of size `k` is `k`, so the Nim-sum across components is the XOR of all `C(a,2)+C(b,2)`. First player (Aoki) wins iff this XOR is non-zero.

**Pitfalls:**
- Must compute the bipartition correctly with BFS/DFS, handling up to 2·10⁵ vertices and edges.
- Large intermediate values: `C(a,2)` for `a` up to 2·10⁵ fits in 64-bit (`~2·10¹⁰`).
- XOR of 64-bit integers in Python is fine.
- Components with no moves (`a≤1 and b≤1`) contribute 0.
- Forest of trees and components with extra cross edges behave identically (no intra-part edges initially).

## worker: (Problem solved: the answer is determined by XOR o
The game reduces to Nim where each bipartite component is a heap of size `C(a,2)+C(b,2)`. Aoki wins iff the XOR of these heap sizes is non-zero. The initial graph is bipartite, and adding an edge without creating an odd cycle forces it to be intra-part. Components are independent, so the Sprague-Grundy value is just the XOR of move counts.
