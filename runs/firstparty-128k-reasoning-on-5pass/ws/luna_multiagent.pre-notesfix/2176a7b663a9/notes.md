
## ideation
The core difficulty is that the graph is dense: one interval may be adjacent to Θ(N) intervals lying entirely to its left or right, so explicitly constructing edges is impossible. At the same time, arbitrary positive vertex weights mean that merely determining connectivity is insufficient; a minimum-weight path may deliberately use more vertices than an unweighted shortest path. A successful method must therefore preserve exact weighted distances while exploiting the ordering of interval endpoints and answer up to Θ(N) unrelated queries.

Important boundary details are that adjacency requires strict separation, namely \(R_i<L_j\) or \(R_j<L_i\), equal endpoints do not produce an edge, and both query endpoints contribute their weights. Connected components also need to be handled independently.

## worker: Derive a globally reusable exact weighted-distance
For overlapping query intervals `s` and `t`, any useful shortest path has at most three edges:

- A common neighbor strictly left of both gives a two-edge path.
- A common neighbor strictly right of both gives a two-edge path.
- A left neighbor of one endpoint and a right neighbor of the other are always adjacent, giving a three-edge path.
- If two candidate neighbors lie on the same side, one of them is already a common neighbor because the two queried intervals overlap.

All weights are positive, so a direct edge is always optimal whenever it exists.

Prefix minima over right endpoints answer the minimum weight interval with `R < threshold`; suffix minima over left endpoints answer the minimum weight interval with `L > threshold`. Preprocessing is `O(N)`, and each query is `O(1)`.
