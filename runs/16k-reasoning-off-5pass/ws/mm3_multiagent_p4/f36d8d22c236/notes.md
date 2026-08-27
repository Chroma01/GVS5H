
## ideation
The core difficulty is determining the minimum number of operations after ensuring consistency. The problem reduces to analyzing a functional graph on 26 letters. The key observations are:
1. Each letter in S must map to a unique target in T; otherwise, it's impossible.
2. The mapping forms a directed graph where each node (letter) has out-degree at most 1.
3. The graph decomposes into connected components, each with exactly one cycle (possibly a self-loop).
4. For a component with no cycle (a tree rooted at a node whose target is outside the component), the minimum operations is the number of nodes.
5. For a component with a self-loop cycle, the minimum operations is (number of nodes - 1) because the self-loop needs no operation.
6. For a component with a cycle of length ≥ 2, the minimum operations is (number of nodes + 1) because we need an extra operation to break the cycle (e.g., mapping a cycle node to a letter outside the cycle or to itself).

Pitfalls:
- Must handle letters not appearing in S correctly (they have no outgoing edge).
- When building components, only include letters that appear in S; the DFS should not follow edges to unused letters.
- Ensure that the cycle detection correctly identifies self-loops versus longer cycles.

## worker: Read N, S, and T from standard input.
The solution works by first ensuring the mapping from each letter in S to its target in T is consistent. If not, we output -1. Otherwise, we build a functional graph on the letters that appear in S, where each node points to its target. We then find connected components in the undirected sense (since cycles can be broken through reverse edges). For each component, we determine if it has a cycle. If it has no cycle (i.e., some node's target lies outside the component), the minimum operations equals the number of nodes. If it has a self-loop cycle, the minimum operations is (number of nodes - 1). If it has a cycle of length ≥ 2, the minimum operations is (number of nodes + 1). The sum over all components gives the answer. The algorithm runs in O(N + 26^2) time, which is efficient for N up to 2×10⁵.
