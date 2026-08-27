
## ideation
**Understanding the operation**

- The operation picks a contiguous substring that is itself a valid parenthesis sequence, then applies a special “reverse”: position `i` becomes the opposite bracket of position `l+r-i`.
- In a valid parenthesis sequence, parentheses are properly nested. Any valid substring corresponds to a connected subgraph of the parenthesis‑matching tree: a node (the root of that substring) together with some of its descendants.
- Reversing a valid substring swaps the two “directions” along the path from the root of the substring to its deepest matched pair. In the tree view, this exchanges the left/right order of the children subtrees, but only for the subtrees that are completely inside the chosen substring.

**Key observation**

- The operation allows us to arbitrarily permute the children of any node in the parenthesis tree, while keeping the parent‑child links unchanged.
- Different orders of children produce different strings (since the concatenation order changes), and any such reordering can be achieved by a sequence of operations.
- The structure of the tree (who is parent of whom) is invariant.

## worker: Parse N and S from stdin, then build the parenthes
The solution builds the standard parenthesis tree by scanning the string with a stack. Each '(' pushes a new node id onto the stack; each ')' pops it. The parent of a node is the node currently on top of the stack when the node is created. After processing, we count how many children each node has. The operation described allows arbitrary permutation of the children of any node, so the number of distinct reachable strings is the product over all nodes of (number of children)! modulo 998244353. Factorials are precomputed up to the number of nodes (N/2). The algorithm runs in O(N) time and O(N) memory, well within the constraints.
