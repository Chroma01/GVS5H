
## ideation
The problem asks for a non‑negative integer sequence A of length N satisfying M XOR constraints  
`A_{X_i} XOR A_{Y_i} = Z_i`.  
If a solution exists we must output the one with minimum sum of elements.

**Core difficulty**  
The XOR operation is not linear over the integers, but it is linear over each binary digit.  
Thus the whole system can be split into independent systems, one for each bit position k (0 ≤ k ≤ 30, because Z_i ≤ 10^9).  
For a fixed bit k we have a system of equations over GF(2):  

```
a_{X_i}^{(k)} XOR a_{Y_i}^{(k)} = z_i^{(k)}   (z_i^{(k)} is the k‑th bit of Z_i)
```

Each such system is a graph problem: vertices are the indices 1…N, edges are the constraints, each edge carries a required XOR value (0 or 1).  
The graph may be disconnected; each connected component can be solved independently.

**Solving one component**  
Pick any vertex as root, set its value to 0 (or 1). Propagate values along edges using the rule  
`value[neighbor] = value[current] XOR edge_z`.  
If during BFS/DFS we encounter an already visited vertex whose forced value differs from the previously stored one, the component (and the whole system) is infeasible.

If the component is consistent, there are exactly two possible assignments: root = 0 or root = 1.  
All other vertices are forced once the root is fixed.

**Choosing the assignment with minimum total sum**  
The total sum is Σ A_i = Σ ( Σ_k 2^k * a_i^{(k)} ).  
Bits are independent, but their weights differ.  
For a fixed component, the two possible assignments correspond to two integer vectors.  
The contribution of the component to the total sum is the integer formed by concatenating the bits of all its vertices (or, more simply, the sum of the vertex values).  
Because the two assignments differ only by flipping every bit of every vertex in the component, the integer formed by the component under assignment 0 is some number C0, and under assignment 1 is C1 = (2^{len_bits} - 1) XOR C0 (where len_bits = (number_of_vertices)*(max_bit+1)).  
The smaller of C0 and C1 is the optimal choice for that component.  
Since components are independent, we can minimise each component separately and sum the results – this yields the global minimum sum.

**Algorithm outline**
1. Read N, M and the M triples (X_i, Y_i, Z_i).
2. Build adjacency list: for each edge store neighbour and the integer Z_i (its bits will be used later).
3. For each unvisited vertex:
   * BFS/DFS the whole connected component.
   * Keep two arrays `val0` and `val1` (size = component size) representing the values of the vertices when the root is forced to 0 and to 1 respectively.
   * Detect contradictions; if any, output `-1`.
   * After the traversal, compute the integer contribution of the component for both assignments.  
     The contribution can be obtained by iterating over bit positions k, counting how many vertices have bit 1 in `val0` (call it cnt0_k) and in `val1` (cnt1_k = component_size - cnt0_k).  
     The sum contributed by the component under assignment 0 is Σ_k cnt0_k * 2^k; under assignment 1 it is Σ_k cnt1_k * 2^k.  
     Choose the smaller sum and store the corresponding values into the global answer array.
4. After processing all components, print the answer array (space‑separated) or `-1` if a contradiction was found.

## worker: Implement the complete Python solution as describe
The solution models each XOR constraint as a graph where each edge carries the required XOR value. For each connected component we perform a BFS assigning values relative to a root. Setting the root to 0 yields one valid assignment; setting it to 1 yields the other. We compute the total sum for both assignments and pick the smaller one, because components are independent and minimizing each component locally yields the global minimum.

During BFS, if a vertex is reached with a different forced value, the system is infeasible and we output -1.

Complexities: O((N+M)·log MaxZ) time and O(N+M) memory, which fits the constraints (N≤2·10⁵, M≤10⁵, MaxZ≤10⁹).

## worker: Implement the complete Python solution as describe
The solution follows the classic XOR‑equation reduction:
- Each bit position is independent, so we can treat the whole integer system as a graph where each edge carries the required XOR value `Z_i`.
- For every connected component, picking a root and fixing its value to `0` forces a unique assignment; fixing the root to `1` gives the complementary assignment (every vertex's value is flipped in all bits).
- While traversing the component we detect contradictions (a vertex forced to two different values) → output `-1`.
- The two candidate assignments for the component are compared by total sum (`sum0` vs `sum1`). Since components are independent, minimizing each component locally yields the global minimum sum.
- Self‑loops are handled: a constraint `A_x xor A_x = z` forces `z = 0`; otherwise the system is infeasible.
- Complexity: each edge is processed once per BFS → `O(N + M)` operations, each involving bitwise XOR on at most 30 bits, so overall `O((N+M)·log MaxZ)`. Memory is `O(N + M)`.

## worker: Replace per‑component dictionaries `val0` and `val
- The solution replaces the per‑component dictionaries `val0` and `val1` with arrays (`val0_arr` and `val1_arr`) that are indexed by the order nodes are discovered during BFS, reducing overhead.
- Self‑loops are handled early: if `X_i == Y_i` and `Z_i != 0`, the system is immediately infeasible.
- The BFS propagates two candidate assignments (root=0 and root=1) and checks for contradictions. If any contradiction occurs, the program outputs `-1`.
- The total sum for each assignment is computed by iterating over the component arrays, and the smaller sum is selected, guaranteeing global minimum because components are independent.
- The algorithm runs in `O((N+M)·log MaxZ)` time (each edge processed once, each operation is XOR on up to 30 bits) and uses `O(N+M)` memory.
- The code reads all input at once for speed, uses `deque` for BFS, and writes output with `sys.stdout.write` for efficiency.
- The solution has been tested on the provided samples (Sample 1 outputs `0 3 4`, Sample 2 outputs `-1`, Sample 3 outputs `0 2 9 6 0`) and edge cases such as `N=1, M=0` (output `0`) and contradictory self‑loops (output `-1`).

## worker: finalize
The solution treats each XOR constraint `A_x XOR A_y = Z` as an edge in a graph carrying the value `Z`. For each connected component we perform BFS, fixing a root's value to 0 (yielding one candidate assignment) and to 1 (the complementary assignment where every bit is flipped). While traversing, contradictions (a vertex forced to two different values) are detected, which makes the whole system infeasible → output `-1`. Since components are independent, minimizing each component's contribution to the total sum yields the global minimum. Self-loops are handled early: if `X == Y` and `Z != 0`, the system is impossible. The algorithm runs in `O((N+M)·log MaxZ)` time (at most 30 bits) and `O(N+M)` memory, well within the constraints. The provided samples are satisfied.
