
## ideation
The graph is initially bipartite, so each connected component has a unique 2-coloring.  
A move adds an edge that does NOT create an odd cycle. This is equivalent to saying the new edge must connect vertices belonging to *different* color classes, either:

* in different connected components, or
* in the same component but with opposite colors.

So we can treat each **color class of each component** as a “group”.  
Let the groups be G_1, G_2, …, G_k. Their sizes sum to N.

All possible edges that are ever legal are exactly the pairs of distinct groups (since any edge inside one group would create an odd cycle, and edges across groups are always bipartite).  
The initial graph has M edges, and every initial edge connects two different groups (because the input is bipartite). Each move adds exactly one previously‑missing cross‑group edge, permanently filling that pair.

Thus the total number of moves in the whole game is fixed:

  total = (number of unordered pairs of groups) − M

and does not depend on move order. The first player (Aoki) wins iff this number is odd.

Algorithm:
1. Read N, M, edges.
2. Find connected components using DSU/Union‑Find.
3. BFS/DFS to 2‑color each component.
4. Count sizes of each (component, color) group, let k = number of groups.
5. Compute total = k*(k-1)//2 − M.
6. If total is odd → print "Aoki", else → "Takahashi".

Pitfalls:
- N and M up to 2e5, need O(N+M) time, O(N) memory.
- Components can be isolated vertices (size 1 component, both color classes, one of them size 1 and the other size 0). Empty color classes don't form a group.
- Be careful with 1‑based vs 0‑based indexing.

## worker: Implement DSU to find connected components, BFS/DF
The solution models the game as filling all possible edges between color-class groups of connected components. Since the initial graph is bipartite, each edge connects two different groups. The total number of legal moves is fixed: total possible cross-group pairs minus existing edges. The first player (Aoki) wins iff this count is odd.

The code uses DSU for component identification, BFS for 2-coloring, then counts non-empty color groups per component, computes `pairs = k*(k-1)//2 - M` and determines the winner.
