
## ideation
**Reading the operation.** For a substring `S[l..r]`, the rule `S_i ← complement(S_{l+r-i})` is exactly the "mirror" of a balanced string: check `(())` → `(())`, `()()` → `()()`, `(())()` → `()(())`. So on the tree/forest model (each matched pair = a node, nesting = parent/child, top level = children of a virtual root), a valid substring is precisely a **contiguous block of sibling subtrees**, and the operation replaces that block `T_1 T_2 … T_k` by `M(T_k) … M(T_1)`, where `M` recursively reverses the child order at every node of a subtree.

**Why the answer is "all orderings of an unordered forest".**
- Invariant: the operation never changes the *unordered* forest (multiset-of-children) shape. So reachable strings ⊆ orderings of that unordered forest.
- Generating adjacent sibling swaps: take a block of exactly two adjacent siblings `T_1 T_2` → `M(T_2) M(T_1)`; then apply the operation to each of them alone (a single subtree `(A)` is itself a valid substring, and mirroring it once more gives `M(M(T))=T`) → `T_2 T_1`, with nothing else touched. Hence at every node (incl. virtual root) all adjacent transpositions of children are available ⇒ full symmetric group, independently per node.
- Therefore reachable set = **all ordered forests isomorphic to S as an unordered forest**, and since ordered forest ↔ string is a bijection, the count of distinct strings is
  ∏_{v ∈ nodes ∪ {virtual root}} c_v! / ∏_j m_{v,j}!, where c_v = #children, m_{v,j} = multiplicities of isomorphic child subtrees.
- Sanity: `(())()` → virtual root has children {`(())`, `()`}, distinct ⇒ 2!/1!1! = 2 ✓. `()` → 1!/1! = 1 ✓.

**Implementation sketch.** Parse with an explicit stack (no recursion; depth can reach 2500). For each closed node, compute a canonical id = intern(sorted tuple of children canonical ids) in a dict. While popping, multiply the answer by `c! * ∏ inv(m_j!)` mod 998244353. Precompute factorials/inverse factorials up to N/2+1.

**Pitfalls.**
- Don't use recursive DFS (RecursionError on `((((…))))`).
- Canonical form must be *unordered* (sort child ids) — using the raw substring would over-count.
- Multiplicities must be counted among children of the same node only; the virtual root's children must be included (easy to forget).
- Answer is mod p; may legitimately be 0 mod p, so no early-exit tricks based on value.
- Complexity: ≤2500 nodes; total sorting/tuple work is O(N log N)-ish. Building tuples of children is fine; total children count = #nodes.
- N is even for any valid non-empty sequence; still, guard N=0/edge input parsing (possible trailing whitespace in S).

## worker: Write the complete Python program: read N and S fr
Implemented exactly the planned algorithm.

- **Model**: each matched pair is a node; nesting gives parent/child; the top level are children of a virtual root. The operation `S_i ← complement(S_{l+r-i})` on a balanced substring is the mirror of a contiguous block of sibling subtrees: `T_1…T_k → M(T_k)…M(T_1)` where `M` reverses child order recursively.
- **Reachability**: the unordered forest is invariant; conversely, applying the op to a 2-sibling block then to each resulting subtree individually (`M(M(T))=T`) realizes an adjacent transposition of siblings with nothing else changed. So every node's children can be permuted arbitrarily and independently ⇒ reachable strings = all ordered forests isomorphic to S as an unordered forest, count = ∏_v c_v!/∏_j m_{v,j}!.
- **Implementation**: single left-to-right scan with an explicit stack of child-id lists (no recursion, so depth 2500 nesting is fine). Canonical unordered subtree id via interning `tuple(sorted(children_ids))` in a dict. Multinomial factor `fact[c]·∏ inv_fact[m_j]` multiplied in at each pop, and finally for the virtual root's list.

**Hand verification (no execution):**
- `()`: pop empty list → id0 (factor 1); top = `[0]` → `1!/1! = 1`. ✓
- `(())()`: inner `()` → id0; outer → key `(0,)` → id1, factor `1!` = 1; then `()` → id0. Top = `[1,0]` → `2!/(1!1!) = 2`. ✓
- `()()`: top = `[0,0]` → `2!/2! = 1`. ✓
- `(())(())()`: top = `[1,1,0]` → `3!/(2!·1!) = 3`. ✓

**Performance**: ≤2500 nodes; each pop sorts its child list, total child count = #nodes, so ~O(N log N). Flat 2500 siblings: one sort of 2500 ids plus a Counter — trivial. Deep nesting 2500: stack depth 2500 in a plain list, no recursion limits.

Edge cases: whitespace stripped; non-`()` chars ignored; defensive guards if the stack were to underflow; result printed mod p (0 is a legitimate output value, no early exits).
