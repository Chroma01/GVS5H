
## ideation
The core difficulty is avoiding the explicit \(K \times K\) cost matrix: computing all bottleneck distances and then solving a general assignment problem is too expensive. The crucial structural fact is that bottleneck distances form an ultrametric represented by a Kruskal reconstruction tree. Every pair of original vertices has cost equal to the value of their lowest common ancestor, so all pair costs are organized by a laminar family of subtrees.

The proposed reconstruction-tree DP must treat \(A\) and \(B\) as multisets, since vertices may occur repeatedly in either sequence. At each subtree, only the unmatched surplus of one side needs to be passed to the parent. Any \(A\)- and \(B\)-occurrences that are both available inside the subtree can be paired there, and each such pair has the current subtree merge value as its cost if it is first resolved at that node. The final root should have no unmatched occurrences because both sequences have length \(K\).

Equal-weight edges require care. Processing equal-weight edges sequentially and creating binary merge nodes still gives correct bottleneck values, since every merge caused by that weight receives the same value. Alternatively, equal-weight components may be consolidated into a multifurcating level. Edges joining vertices already in the same DSU component must not create reconstruction nodes.

Several implementation concerns are important: use sufficiently wide integer arithmetic for the answer, preserve multiplicities rather than merely recording whether a vertex appears, and ensure that the root is formed even when many equal-weight merges occur. The condition \(A_i \ne B_j\) means no pair has the same endpoint vertex, but the DP should not rely on this beyond the stated input guarantee.

## worker: Implement the complete Python solution using a Kru
The Kruskal reconstruction tree represents each bottleneck distance as the weight of the LCA of two original vertices. Each subtree stores the signed surplus `(#A - #B)` after optimally matching all possible pairs inside it.

When two child subtrees have opposite surpluses, those occurrences must be matched across the current merge, and each such pair costs the current node’s edge weight. Matching as many as possible is optimal because any pair deferred to an ancestor would cost no less. The remaining signed surplus is propagated upward.

The construction, traversal, and DP all take `O(N + M log M)` time and `O(N + M)` memory.
