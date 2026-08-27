- **Tree representation:** Every matching parenthesis pair is a node. Its children are the maximal parenthesis-pair components directly inside it. The whole input is an ordered forest of root nodes.
- **Effect of an operation:** Any valid parenthesis substring is exactly a consecutive block of siblings in this forest representation. Reverse-complementing such a block reverses the order of those siblings and reverse-complements each selected subtree.
- **Generated transformations:** Applying an operation to one complete child subtree gives its reverse-complement transformation. Applying it to two adjacent sibling subtrees, followed by independently transforming each of them, swaps the two siblings without changing their final individual choices. Adjacent swaps generate every permutation, so children can be permuted arbitrarily and each child can independently be replaced by any string in its own reachable orbit.
- **Canonical class:** A node is characterized only by the multiset of canonical classes of its children. Thus its key is the sorted tuple of child class IDs. Equal keys are interned to the same class, regardless of the original child order.
- **Orbit count:** Suppose class \(t\) occurs \(m_t\) times among a node’s children, and one child of that class has \(r_t\) reachable encodings. The number of class-order patterns is \((\sum_t m_t)!/\prod_t m_t!\). For every occurrence, its encoding can be chosen independently, contributing \(r_t^{m_t}\). Therefore:
  \[
  f=\frac{k!}{\prod_t m_t!}\prod_t r_t^{m_t}.
  \]
  The same formula applies to the top-level forest.
- **Bottom-up processing:** On reading a closing parenthesis, all child nodes are already assigned canonical IDs, so the node can be sorted, interned, and assigned its orbit count immediately.
- **Complexity:** Sorting child ID lists costs \(\sum_v O(d_v\log d_v)\), bounded by \(O(N\log N)\). Hash-table interning and counting are linear apart from sorting. Memory usage is \(O(N)\).
- **Modular arithmetic:** Factorials and inverse factorials are precomputed through \(N/2\). All multiplicities are below \(998244353\), so modular inverses are valid.
