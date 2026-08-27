
## ideation
The problem asks for the number of ways to orient each tile (type A or B) so that on a toroidal grid every edge‑midpoint is used by either zero or two incident tiles.  
Core difficulties:

* **Toroidal topology** – equations for each cell involve neighbour cells with wrap‑around (mod H, W).  
* **Two‑dimensional consistency** – horizontal edges must agree across rows and vertical edges across columns; a type‑B tile can be oriented either horizontally or vertically and forces a relation between the two families.  
* **Large input** – up to 10⁶ cells in total, 10⁵ test cases, each test must be O(H·W) time and memory.

**Candidate approaches**

1. **Linear algebra over GF(2)** – treat the presence/absence of each edge‑midpoint as a binary variable.  
   The row constraints give `e[j‑1] XOR e[j] = h[j]`; the whole row has solutions iff the number of `A`‑cells in that row is even. The same holds for columns.  
   For each type‑B cell the two points of view give `e[i][j‑1] = f[j][i‑1]`.  
   Introducing a parity‑prefix for every row and column turns this condition into a label `D(i,j)` on the edge connecting row i and column j.  
   The problem reduces to a bipartite graph where rows and columns are vertices, edges correspond to B‑cells, each edge carries a label `D`.  
   A solution exists iff the label xor along every cycle is 0 – exactly what a BFS/DFS checking the equation `r[i] XOR c[j] = D` does.  

2. **Counting solutions** – each connected component of this graph contributes a factor 2 (the whole component can be flipped). Isolated vertices (rows/columns without any B‑cell) are also components with factor 2. Hence total answer = 2^{#components} (mod 998244353).  

**Pitfalls to watch**

* Parity condition: a row or column with an odd number of A‑cells makes solutions impossible → answer 0.  
* Updating prefix parities correctly while scanning each row: after processing column j, toggle the parity for the next cell if it is `A`.  
* When building the graph, only B‑cells create edges; isolated vertices must be counted as components.  
* Use fast modular exponentiation (binary exponentiation) for 2^k.  
* Input can be large → read with `sys.stdin.buffer` and avoid per‑character Python overhead in tight loops; store strings as `bytes`.  
* Ensure we handle up to 10⁵ test cases while keeping total time ≤ O(∑HW) and resetting data structures per case.

**Verification of the plan**

The solution outline above matches the detailed algorithm proven in the plan. The plan’s reasoning (Lemmas 1–8) confirms correctness, and the complexity O(H·W) per test case fits the limits.

## worker: finalize
The problem asks for the number of ways to orient each tile so that on a toroidal grid every edge‑midpoint is used either by zero or by two tiles.

* For a cell `(i,j)` let `r[i]` be the first horizontal edge of row `i` (0/1) and `c[j]` the first vertical edge of column `j`.  
  Horizontal edges in the whole row are `e[i][j] = r[i] XOR R[i][j]` where `R[i][j]` is the parity of `A` cells in that row before column `j`.  
  Analogously `f[j][i] = c[j] XOR C[j][i]` for vertical edges.

* The condition “every edge is used 0 or 2 times’’ translates to:
  - In each row the system `e[i][j‑1] + e[i][j] = h[i][j]` (where `h` is the number of horizontal edges of the tile) has a solution **iff** the row contains an even number of `A` cells.  
    If it has a solution it has exactly two solutions (choice of `r[i]`).

* The same holds for columns.

* For a type‑B cell the two points of view give the requirement  

```
r[i] XOR R[i][j] XOR c[j] XOR C[j][i] = 1
```

  i.e. `r[i] XOR c[j] = (R[i][j] XOR C[j][i]) XOR 1`.  
  We store the right‑hand side as the label of the edge connecting row `i` and column `j` in a bipartite graph.

* The whole problem becomes: assign binary potentials `r[i] , c[j]` such that for every edge `(i,j)` the label condition holds.  
  This is a system of equations over GF(2). It has a solution exactly when the propagation (BFS) never meets a contradiction.

* If the propagation succeeds, each connected component of the graph contributes a factor 2 (the whole component can be flipped). Isolated vertices are also components.  
  Hence the answer is `2^{#components}` (mod 998244353).

The algorithm:
1. Count `A` in each row and column; if any count is odd → answer 0.
2. Scan the grid, maintaining prefix parities `R` and `C`. For each `B` cell compute the label `(R XOR C) XOR 1` and add the edge to both adjacency lists.
3. Run BFS on the bipartite graph, counting components and detecting contradictions.
4. Output `2^{components}` modulo `998244353`.

Complexities per test case: `O(H·W)` time, `O(H·W)` memory (edges ≤ 2·#B). The sum of `H·W` over all test cases is ≤ 10⁶, well within limits.
