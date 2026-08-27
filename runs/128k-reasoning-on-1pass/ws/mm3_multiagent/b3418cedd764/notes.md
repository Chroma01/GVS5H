
## ideation
The problem asks for the number of assignments of values in {1,…,M} to N vertices such that along each directed edge \(i \to A_i\) the value does not decrease. The graph is a functional graph (each vertex has out‑degree 1), which decomposes into disjoint components, each consisting of a directed cycle with rooted trees whose edges point toward the cycle.  

Core difficulty:  
- Identify the cycles and the trees attached to them.  
- Enforce the constraints that all vertices on a directed cycle must share the same value (since going around the cycle forces a non‑decreasing sequence that is also periodic, hence constant).  
- For a tree whose root is adjacent to a cycle vertex with value \(c\), every vertex in the tree must have value \(\le c\).  
- Compute the number of valid assignments for each tree as a function of the root’s value, then combine them across the cycle and across components.

Candidate approaches:  
1. **Graph decomposition + DP on trees** – Remove non‑cycle vertices by repeatedly deleting indegree‑0 nodes (Kahn’s algorithm). The remaining vertices form cycles. For each tree vertex \(v\) (processed in reverse removal order) compute DP: \(dp[v][k] =\) number of ways for the subtree of \(v\) with \(x_v = k\). Use prefix sums \(pref[v][k] = \sum_{t=1}^k dp[v][t]\) for efficiency. For a component with cycle value \(c\), the number of ways is \(\prod_{\text{roots } r} pref[r][c]\). Sum over \(c=1..M\) and multiply across components. Complexity \(O(NM)\).  
2. **Brute force / exponential** – Impossible for \(N,M \le 2025\).  
3. **Inclusion–exclusion / generating functions** – The DP approach is essentially a generating function method, so the first approach is simplest.  
4. **Linear algebra / matrix exponentiation** – Not needed because the constraints are monotone and the functional graph structure yields a simple product formula.

Pitfalls:  
- Correctly detecting cycle vertices (those not eliminated by indegree‑0 removal).  
- Handling components that have no attached trees (product = 1, sum = M).  
- Managing modulo 998244353 throughout DP and summations.  
- Memory: storing an \(M\)-length array for each non‑cycle vertex fits within limits (\(\le 2025^2 \approx 4\cdot10^6\) integers).  
- Processing order: children must be processed before parents; reversed removal order works.  
- Off‑by‑one: the reference implementation uses 0‑based indexing for vertices, 1‑based for values.  
- Ensure that when a component’s cycle has size 0 (impossible) or multiple cycles, the product across components is independent.

## worker: finalize
**Algorithm Overview**

1. **Graph structure** – The given graph is a functional graph (each vertex has out‑degree 1). It decomposes into several connected components, each consisting of a directed cycle with rooted trees whose edges point toward the cycle.

2. **Cycle constraint** – All vertices on a directed cycle must have the same value, because traversing the cycle forces a non‑decreasing sequence that is also periodic, hence constant. Denote this common value by `c` (1 ≤ c ≤ M).

3. **Tree DP** – For any vertex `v` that is *not* on a cycle we compute  
   `dp[v][k] =` number of ways to assign values to the subtree of `v` with `x_v = k`.  
   The recurrence is  
   `dp[v][k] = ∏_{u child of v} ( Σ_{t=1..k} dp[u][t] )`.  
   Let `pref[v][k] = Σ_{t=1..k} dp[v][t]` (the number of ways with `x_v ≤ k`).  
   For a leaf `dp[v][k] = 1` and `pref[v][k] = k`.

   Using Kahn’s algorithm we repeatedly delete vertices of indegree 0. The order in which vertices are deleted is a topological order from leaves toward the cycle. Processing the vertices in this order guarantees that all children of a vertex are already known, so we can compute `pref` for a node when it is removed.

4. **Component contribution** – Consider a component whose cycle vertices are `C`. For a fixed cycle value `c`, each tree rooted at a child `r` of a cycle vertex can take any value `≤ c`; the number of possibilities for that tree is `pref[r][c]`. Trees are independent, so for this `c` the component contributes `∏_{r} pref[r][c]`. Summing over all possible `c` gives the total number of assignments for the component:
   `value_of_component = Σ_{c=1..M} ( ∏_{r} pref[r][c] )`.

   If a component has no attached trees, the product is 1 and the sum equals `M`.

5. **Combine components** – Different components are independent (no edges between them), so the answer is the product of the component values modulo `998244353`.

**Complexity Analysis**

* Removing non‑cycle vertices and building the component structure: `O(N)`.
* DP over all non‑cycle vertices: each vertex processes `M` values and multiplies over its children. The total number of multiplications is `M` times the number of edges from non‑cycle vertices, i.e. `O(N·M)`. Memory used is `O(N·M)` for the `pref` arrays (at most about 4 · 10⁶ integers for the given limits).
* Computing the final answer also costs `O(N·M)`.

Overall time `O(N·M)` ≤ ≈ 4·10⁶ elementary operations, easily fast enough for the constraints. Memory consumption stays well within typical limits (≈ 120 MiB in the worst case).

**Correctness Sketch**

*Lemma 1*: For a non‑cycle vertex `v`, `dp[v][k]` counts exactly the assignments of its subtree with `x_v = k`.  
*Proof*: By induction on the height. For a leaf the only assignment is itself with value `k`. For an internal node, each child subtree must respect `x_child ≤ x_v = k`; the child contributes `pref[child][k]` ways, and the product of independent children gives the total.

*Lemma 2*: `pref[v][k] = Σ_{t=1..k} dp[v][t]`, i.e. the number of assignments with `x_v ≤ k`. Immediate from definitions and Lemma 1.

*Lemma 3*: For a fixed common cycle value `c`, the number of assignments of a component equals `∏_{r} pref[r][c]`.  
*Proof*: The cycle vertices are forced to `c`. Every tree attached to the cycle can take any value not exceeding `c`; by Lemma 2 each such tree has `pref[r][c]` possibilities, and trees are independent.

*Lemma 4*: The algorithm computes `value_of_component = Σ_{c=1..M} ( ∏_{r} pref[r][c] )`. Direct from the code.

*Lemma 5*: This value equals the total number of valid assignments for the component. Follows from Lemma 3 and summation over all possible `c`.

*Lemma 6*: Assignments of different components are independent, because no edge connects two different cycles. Hence the total number of global assignments is the product of the component values.

*Theorem*: The algorithm outputs the number of sequences `x` satisfying `x_i ≤ x_{A_i}` for all `i`, modulo `998244353`.  
*Proof*: Combine Lemmas 1–6 with the final product over components.

Thus the implementation is correct.
