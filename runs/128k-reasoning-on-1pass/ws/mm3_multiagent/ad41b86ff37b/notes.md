
## ideation
**Core difficulty**  
A Snowflake Tree is a very specific shape: one central vertex (red) connected to `x` “blue” vertices, each of those connected to exactly `y` leaves.  
After deletions the remaining graph must be exactly this shape.  
The problem is to keep as many vertices as possible (equivalently delete as few as possible) while respecting the structure.

**Key observations**  

1. **Red vertex choice** – In any valid snowflake the red vertex is the only vertex that can have degree > 1 after deletions. Hence we can try every vertex as a possible red vertex.

2. **Blue vertices must be neighbours of the red vertex** – If a neighbour `b` of `r` is kept as a blue vertex, it must keep at least one leaf, so its original degree `deg(b)` must be ≥ 2. Moreover, the same number of leaves `y` must be attached to *all* blue vertices, therefore  
   `y ≤ min_{b∈B} (deg(b)‑1)`.  
   The best we can do for a fixed set `B` is to use `y = min_{b∈B}(deg(b)‑1)`.  

3. **Size formula** – For a fixed red vertex `r` and a set `B ⊆ N(r)` of blue vertices, the maximal number of kept vertices equals  
   `1 + |B|·min_{b∈B}deg(b)`.  
   (The “1” is the red vertex, the term `|B|·deg(b)` counts the blue vertices plus their `y = deg(b)‑1` leaves.)

4. **Optimal subset for a given `r`** – To maximise `|B|·min_{b∈B}deg(b)`, sort the neighbour degrees of `r` (ignoring degree‑1 vertices) in **decreasing** order `d₁ ≥ d₂ ≥ …`.  
   For any size `t` the optimum is achieved by taking the first `t` neighbours, giving value `t·d_t`.  
   So the best for `r` is `max_{t} (t·d_t)`.

5. **Global optimum** – The overall maximal snowflake size is the maximum of the per‑vertex optima. The answer is `N – maxSize`.

**Candidate approaches**  

* **Per‑vertex sort** – For each vertex collect the degrees of its neighbours that are ≥ 2, sort them descending, scan to compute `max t·d_t`.  
  Complexity: total `O( Σ deg(v) log deg(v) ) = O(N log N)`.  
  Memory: `O(N)` for adjacency lists and a degree array.

* **Linear scan using prefix minima** – Instead of sorting, one could keep the running maximum while iterating neighbours in any order, but the clean solution uses sorting; it is already fast enough.

* **Alternative DP / tree DP** – Could treat the problem as a DP on rooted trees, but the above global‑center formulation is simpler and sufficient.

**Pitfalls to watch**  

* Neighbour degree = 1 cannot become a blue vertex (needs at least one leaf). Must be excluded.
* `y` must be a *positive* integer → the minimal degree among blue vertices must be ≥ 2.
* The problem guarantees a solution exists, but we must still handle the case where a vertex has no neighbour of degree ≥ 2 (then it cannot be the red vertex).
* Input size up to 3·10⁵, recursion depth could overflow; use iterative processing.
* Be careful with 1‑based vs 0‑based indexing.
* The answer is `N - maxSize`; ensure we compute the maximum over **all** vertices, not just the root of a DFS.

## worker: Implement the Python solution: read input, build a
- The solution follows the plan described: for each possible red vertex `r`, consider all its neighbours with original degree ≥ 2 (they can become blue vertices).  
- Sorting the neighbour degrees decreasingly and scanning `i * d_i` gives the maximum value of `|B|·min_{b∈B}deg(b)` for that `r`.  
- The total number of kept vertices for that `r` is `1 + best` (the red vertex plus the blue vertices and their leaves).  
- The global maximum over all `r` is the largest snowflake we can keep; the answer is `N - max_total`.  
- Complexity: building the adjacency list and degrees is `O(N)`.  
  The total work of sorting all neighbour lists is `O( Σ deg(v) log deg(v) ) = O(N log N)`.  
  Memory consumption is `O(N)`. This fits the limits (`N ≤ 3·10⁵`).
