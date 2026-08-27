
## ideation
**Core difficulty**  
We must partition the vertices of a tree into N disjoint simple paths, each containing exactly K vertices (equivalently K‑1 edges).  
The condition is purely local: inside the final decomposition every vertex is incident to either 1 or 2 edges of a single path, and each closed path must have total length K.  
Thus a global constraint (partition into paths of prescribed length) translates into a set of local constraints that can be checked with a bottom‑up DP on the tree.

**Candidate approaches**  
1. **Tree DP** – Root the tree, process children first, keep for each vertex the length of the unique “open” path segment that ends at that vertex (0 … K‑1).  
   * 0 means the subtree is already completely covered by closed paths.  
   * A non‑zero value x means an open segment of length x starting at some descendant and ending at the current vertex, to be continued through the edge to the parent.  

   Local rules (see the PLAN) enforce that at most two open segments meet at a vertex, and they can be joined only when their lengths sum to K‑1 (forming a closed path) or when a single segment already has length K‑1 (it ends at this vertex).  

   The root has no parent, so it must either finish a path (single open segment = K‑1, or two open segments summing to K‑1) or, when K = 1, accept an empty situation.

2. **Greedy leaf removal** – Repeatedly cut leaves whose path‑length potential cannot be satisfied, but this is harder to prove and essentially mimics the DP.

3. **Special case K = 2** – Reduces to a perfect matching on the tree; a DP also works automatically.

**Implementation outline**  
* Read N, K, build adjacency list (size NK).  
* If K = 1, answer is immediately “Yes”.  
* Perform an iterative DFS from vertex 1 to obtain a parent array and a preorder list; reverse it to get a post‑order (children processed before parent).  
* DP array dp[v] ∈ {‑1, 0, 1,…,K‑1}.  
  * ‑1 = impossible state (propagate upward).  
  * For each child, ignore dp = 0 (its subtree already closed) and collect the non‑zero values.  
  * Apply the local rules described in the PLAN, distinguishing root vs non‑root.  
* After processing all vertices, the answer is “Yes” iff dp[1] == 0.

**Pitfalls & edge cases**  
* **Recursion depth** – NK can be 2·10⁵, so use an explicit stack instead of Python recursion.  
* **K = 1** – every vertex is already a path of length 1, answer always “Yes”.  
* **Root handling** – the root cannot pass an open segment upward; only the three configurations listed in the PLAN are acceptable.  
* **Multiple cut edges** – children with dp = 0 are ignored; they do not affect the count of active segments, so many cut edges are allowed.  
* **Overflow / index errors** – use 1‑based indexing consistent throughout; allocate arrays of size NK+1.  
* **Large input** – use `sys.stdin.buffer.read()` and split by whitespace for fast I/O.  
* **K > NK** – impossible, but does not arise because N·K = NK.  
* **Verification** – the DP’s correctness can be proved with lemmas (see PLAN); the implementation must carefully distinguish “no open segment” (dp = 1 from a leaf) from “segment already closed” (dp = 0).

## worker: Write the complete Python solution implementing th
**What we did**  
- Implemented the tree‑DP described in the plan.  
- An iterative DFS gives a parent array and a post‑order traversal of the tree.  
- For each vertex we keep `dp[v]`:
  * `0` – the subtree of `v` is already covered by closed paths of length `K`,
  * `x (1 ≤ x < K)` – an open path segment of length `x` ends at `v`,
  * `-1` – impossible configuration (propagated upward).  

  The local rules are exactly those proved in the plan:
  * at most two children may contribute non‑zero `dp`,
  * if none contribute, a non‑root vertex starts a new open segment of length 1,
  * if one contributes with length `x`, either the segment finishes (`x = K‑1`) or it is continued (`x < K‑1`),
  * if two contribute with lengths `x, y`, they must satisfy `x + y = K‑1` to form a closed path,
  * the root cannot pass an open segment upward, so it must satisfy the same condition for `0` or `1` or `2` incoming active segments.

- After processing the whole tree, the answer is “Yes” iff `dp[root] == 0`.  
- The special case `K = 1` (every vertex is a path of length 1) is handled immediately.

**Proof Sketch**  
The DP respects the degree constraints of a path: a vertex can belong to at most one path and then it is incident to at most two used edges.  
*If the DP succeeds (`dp[root]=0`), Lemma 2 shows that every vertex lies in a closed path of length `K`.  
*If a decomposition exists, orient each path toward the root. Then every vertex receives exactly the same `dp` value as the algorithm (Lemma 3), so the DP cannot fail and ends with `dp[root]=0`.  
Thus the algorithm is correct.
