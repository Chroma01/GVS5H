- **Potential reduction:** Let `P[v]` be the prefix sum of road strengths before town `v`. A rightward trip on `[l,r]` requires `P[l]=P[r]` and every interior potential greater; a leftward trip requires the same endpoint equality and every interior potential smaller.

- **Conflict characterization:** A selected family is feasible iff it contains no conflicting pair. Pair conflicts are equal normalized left endpoints, equal normalized right endpoints, opposite directions on equal endpoints, and properly crossing intervals with equal direction signs. Disjoint intervals and strict containment are compatible.

- **Range reduction:** Let `prev[i]` be the greatest earlier person index conflicting with person `i`. A query `[L,R]` is feasible iff `max(prev[L..R]) < L`. A standard segment-tree RMQ answers each query.

- **Endpoint conflicts:** Dictionaries store the latest prior trip for every normalized left endpoint, normalized right endpoint, and directed endpoint pair.

- **Crossing conflicts:** For `[l,r]`, same-direction earlier crossings occur in either rectangle `(a,b)` with `a<l<b<r` or `l<a<r<b`. Dynamic 2D range maximum structures are maintained separately by direction.

- **Packed inner tree correction:** Every inner segment tree is located at `tree_offsets[node]` in one packed array. Segment-tree arithmetic must be done with local indices. In both update and query, shifting `>>= 1` is now applied only to local indices; array accesses use `seg[start + local]`. Using absolute packed indices incorrectly mixed unrelated inner trees whenever offsets were nonzero.

- **Complexity:** Preprocessing is `O(M log^2 N + M log M)` time and `O(M log N)` memory. Queries take `O(log M)` time.
