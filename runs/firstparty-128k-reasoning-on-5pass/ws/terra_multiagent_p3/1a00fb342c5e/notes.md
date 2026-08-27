- **Graph model:** Treat each condition as an undirected edge `(x, y, z)` requiring `A[x] XOR A[y] = z`.
- **Feasibility:** In each connected component, assign a temporary XOR label `label[v]` by BFS from an arbitrary root with label zero. Traversing edge `(v, to, z)` requires `label[to] = label[v] XOR z`. If an already assigned vertex has a different required label, constraints are inconsistent and the answer is `-1`.
- **Form of all solutions:** For a connected component, after temporary labels are fixed, every valid assignment has form `A[v] = label[v] XOR shift`, where `shift` is one common non-negative integer for the entire component.
- **Minimization:** Optimize each bit of `shift` independently. For bit `b`, if `ones` temporary labels have that bit set among `size` component vertices, then:
  - leaving the shift bit zero gives `ones` output ones;
  - setting the shift bit one gives `size - ones` output ones.
  Set the shift bit iff `ones > size - ones`. Either value is optimal on ties.
- **Bit bound:** Since all edge values are at most `10^9 < 2^30`, all derived labels only use bits `0..29`. Setting higher shift bits would add positive cost for every component vertex, so they are never optimal.
- **Complexity:** BFS and edge checks take `O(N + M)`. Per-component bit counting costs `O(30 * N)` total. Memory usage is `O(N + M)`.
- **Edge cases:** Self-loops and duplicate edges are handled by the ordinary consistency check. Isolated vertices become zero, which is optimal.
