- **Tree representation:** Each matching parenthesis pair is a rooted node, and the nodes directly enclosed by it are its ordered children. The whole string is an ordered forest; concatenation corresponds to siblings.
- **Effect of an operation:** Any valid contiguous substring is a consecutive sequence of siblings at some nesting level. Reversing it while swapping parentheses maps every selected subtree to its mirror (children in reverse order, recursively) and reverses the order of the selected sibling sequence.
- **Invariant:** Mirroring does not change the unordered rooted-tree shape of a subtree. Therefore every operation preserves, for every node and for the outer forest, the multiset of child unordered types.
- **Reachability:** A single subtree can be mirrored by selecting that subtree. For adjacent sibling subtrees \(A,B\), reversing their concatenation produces mirror\((B)\), mirror\((A)\); mirroring each singleton afterward produces \(B,A\). Thus adjacent siblings can be swapped. Adjacent swaps give arbitrary sibling permutations, and operations inside a child can be performed independently. Consequently, every ordered forest with the same unordered rooted shape is reachable.
- **Counting one type:** Suppose a node has child types with multiplicities \(m_t\). Their positions can be arranged in \(\frac{k!}{\prod_t m_t!}\) type sequences. Each occurrence of type \(t\) independently has `ways[t]` realizations, so the total is
  \[
  \frac{k!}{\prod_t m_t!}\prod_t \text{ways}[t]^{m_t}.
  \]
  The same formula applies to the outer forest using a virtual root.
- **Canonicalization:** Parse bottom-up. A node’s canonical key is the sorted tuple of its child type IDs. Equal keys represent the same unordered rooted type and share one computed count.
- **Complexity:** There are at most \(N/2\) nodes. Sorting child lists costs \(O(N\log N)\) in total worst-case bounds, and the memory usage is \(O(N)\) apart from tuple storage.
