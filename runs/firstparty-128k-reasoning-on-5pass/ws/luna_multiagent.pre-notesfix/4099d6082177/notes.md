
## ideation
The core difficulty is enforcing both conditions simultaneously: every vertex must belong to exactly one path, and every path must contain exactly K vertices. Rooting the tree gives each child subtree only one connection to the rest of the tree, but the path crossing that boundary may have different possible lengths. At a vertex, only one path can use the vertex itself, so at most two unfinished child paths can be joined through it. A tempting approach that pairs many child residues at the same vertex is invalid, because the vertex cannot belong to several paths.

Important edge cases include K=1, where every singleton vertex is already a valid path, and vertices whose subtree has no unfinished path. Any state representation must ensure that a subtree is either completely partitioned or has precisely one open path ending at its root; multiple open paths cannot cross the parent edge.

## worker: Derive and implement the deterministic bottom-up r
For each rooted subtree, every completed path contributes a multiple of `K` vertices. Therefore, if the subtree is not fully decomposed, it must expose exactly one unfinished path whose length equals the subtree size modulo `K`, and this path must end at the subtree root.

At a vertex, at most two child unfinished paths can be used because the vertex can belong to only one path. With two such paths, their lengths must sum to `K - 1`; with one, the path is extended through the current vertex. More than two unfinished child paths is impossible.

The tree is processed bottom-up iteratively, avoiding recursion-depth issues. For `K = 1`, every vertex is already a valid singleton path.
