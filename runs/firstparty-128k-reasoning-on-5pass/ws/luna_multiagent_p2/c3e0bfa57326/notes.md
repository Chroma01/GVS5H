- **Forest model:** Represent the valid parenthesis sequence as an ordered rooted forest. Each matched pair is a node, and its children are the consecutive top-level components inside the pair. The whole string is the forest rooted at a virtual root.

- **Effect of an operation:** Every valid substring is a consecutive interval of sibling subtrees. Reverse-complementing such an interval reverses the order of those subtrees and mirror-transforms each subtree recursively.

- **Invariant:** Define the type of a node recursively as the multiset of the types of its children. For a forest, define its type similarly as the multiset of its component types. An operation only reverses components and mirror-transforms them; mirroring does not change the recursive multiset type. Hence the root multiset type is invariant.

- **Completeness:** A whole node can be selected, so every subtree can independently undergo any transformation reachable inside it. Two adjacent sibling components can be swapped while preserving their current concrete forms: reverse the pair, then reverse each component individually. Therefore arbitrary sibling permutations and independent choices of reachable forms are possible. Inductively, every ordered forest with the same recursive multiset type is reachable.

- **Counting:** If a type has child types with multiplicities \(c_1,c_2,\ldots\), and `ways[t]` is the number of concrete reachable strings for type \(t\), then
  \[
  \text{ways} = \frac{k!}{\prod c_i!}\prod \text{ways}[t_i]^{c_i},
  \]
  where \(k\) is the number of children. The same formula applies to the virtual root forest.

- **Duplicates:** Components with equal recursive types are indistinguishable for permutation counting, giving the factorial denominator. Their concrete realizations are still independently selectable, producing the corresponding power of `ways`.

- **Complexity:** Parsing is \(O(N)\). Sorting child type lists costs \(O(N\log N)\) in total worst case. Memory usage is \(O(N)\).
