
## ideation
The core difficulty is handling two coupled issues efficiently: first, determining whether all XOR constraints are mutually consistent; second, minimizing the sum when each connected component has one arbitrary XOR offset. Once a component is rooted and each vertex has a potential `p[v]` satisfying `p[u] XOR p[v] = Z` along every edge, every valid assignment in that component has the form `A[v] = p[v] XOR t` for one common offset `t`. Consistency must be checked whenever a previously visited vertex is reached.

The minimization separates independently by binary bit. For a fixed bit, choosing the corresponding bit of `t` either preserves or flips every potential bit in the component. Therefore, choose the value that makes fewer final vertex bits equal to one; ties can be resolved arbitrarily. The resulting component choices are independent, and isolated vertices naturally receive zero.

Important pitfalls include using XOR rather than addition when propagating potentials, checking self-loops correctly, processing disconnected vertices, and ensuring that the bit range includes all bits appearing in the constraints. Since every potential is an XOR of input values, bits through the highest bit of the `Z` values are sufficient. The total complexity should be near-linear in `N + M`, with only a small factor for the number of bits.

## worker: Produce the final iterative graph-traversal Python
Each edge imposes a relation `A[u] XOR A[v] = z`. During graph traversal, assign each vertex a potential relative to its component root. A previously assigned vertex reached through an edge must have the same expected potential; otherwise the constraints are contradictory.

For a consistent component, every valid assignment is `potential[v] XOR t` for one common offset `t`. Each bit can be optimized independently: choose the offset bit that makes the minority of the component’s potential bits become `1`. Isolated vertices form valid components with potential zero and therefore receive value zero.

The traversal is iterative and runs in `O(N + M)`, while bit optimization takes `O(BN)` where `B <= 30`.
