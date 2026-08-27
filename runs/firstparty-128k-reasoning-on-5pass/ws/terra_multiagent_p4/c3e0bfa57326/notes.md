- **Forest model:** Parse the parenthesis sequence as an ordered rooted forest with a virtual root. Every matched pair is a node, and its direct balanced components are its children.

- **Reachability characterization:** At every node, its children can be transformed independently and then permuted arbitrarily. Singleton reflections allow mirroring a child independently, and a length-two reflection followed by singleton reflections swaps adjacent children without changing their final states. Thus every sibling permutation is reachable.

- **Invariant:** Ignoring sibling order, the rooted forest structure is invariant under every operation. A mirrored subtree has the same unordered rooted-tree type.

- **Canonical type:** Define the unordered type of a node as the sorted tuple of unordered types of its children. Equal tuples give equal types. This can be assigned deterministically bottom-up using a dictionary from tuples to integer IDs.

- **Counting a node type:** Suppose a node has `k` children. For each child unordered type `t`, occurring `m_t` times, let `F[t]` be the number of distinct reachable ordered serializations of that type. Child types have disjoint serialization languages, since parsing a serialization recovers its unordered type. Therefore:
  `F[node] = k! * product_t(F[t] ^ m_t / m_t!)`.
  The multinomial factor chooses positions for child types, and each occurrence independently chooses one of `F[t]` ordered representations.

- **Virtual root:** Apply exactly the same formula to the multiset of top-level component types. Its answer is the number of final parenthesis strings, without adding an enclosing pair.

- **Algorithm:** Build the forest in `O(N)`. Process nodes in reverse creation order, which is postorder because nodes are created before descendants. Sort each child-type list, intern the tuple, and compute its value once per type. Finally evaluate the virtual root formula.

- **Complexity:** There are at most `N/2` nodes. Total sorting cost is `O(N log N)` in the worst case, with `O(N)` stored tree data aside from signature tuples. Modular factorials and inverse factorials handle divisions modulo `998244353`.
