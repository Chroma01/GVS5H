
## ideation
- **Core difficulty**: The operation "replace all x with y" is global and affects every occurrence of x. This can be modeled as building a directed graph of required transformations (S[i] -> T[i] for S[i] != T[i]). The challenge is determining when the transformation is possible and finding the minimum number of operations.
- **Key insight**: The graph is a functional graph (out-degree ≤ 1) because each source letter can map to at most one target. The transformation is possible iff:
  1. Consistency: No letter in S maps to two different targets. (Check via sets of targets for each source letter.)
  2. No "dangling" target: Every letter that appears in T and has outgoing edges must have at least one incoming edge. (Otherwise it cannot be produced.)
- **Minimum operations**: The graph splits into connected components. For a component with `n` nodes and `m` edges:
  - If it's a tree (m = n - 1): cost = n - 1.
  - If it contains a cycle (m = n): cost = n + 1 (need an extra operation to break the cycle using a temporary letter).
  Sum over all components.
- **Pitfalls**:
  - Self-loops (x -> x) are not added because S[i] != T[i] is required.
  - Letters that appear in T but not in S must be produced; they will be targets with in-degree ≥ 1.
  - Consistency check must consider all positions, not just differing ones (a letter might need to stay the same in some positions and change in others).
  - Isolated nodes (no edges) cost 0.
  - The impossibility condition (target with out-degree > 0 and in-degree = 0) is not caught by the consistency check alone; both checks are needed.

## worker: Implement the solution in Python as described in t
The solution works by:
1. **Consistency check**: For each letter `c` in S, all positions where `S[i]=c` must map to the same target character in T. If any letter needs to become two different things, it's impossible.
2. **Graph modeling**: Build a functional graph where an edge `c -> target[c]` exists for each letter that needs to change. The graph has out-degree ≤ 1.
3. **Cycle detection**: In a functional graph, each weakly connected component has at most one directed cycle. Cycles are not impossible (unlike some similar problems) but require one extra operation to break using a temporary letter.
4. **Cost calculation**: 
   - Each edge (source letter needing change) requires one operation.
   - Each component containing a cycle requires one additional operation.
   - Total = number of edges + number of cycle components.
5. **Finding cycle components**: Use topological removal (Kahn's algorithm) to strip away all nodes not in cycles. The remaining nodes form disjoint cycles. Count the number of connected components among them.

The algorithm is O(N + 26) and handles all edge cases correctly.
