
## ideation
We need to find a largest connected subgraph (a tree) of the given tree where every vertex has degree 1 or 4 and at least one vertex has degree 4. This is a classic “rooted‑subtree DP” problem.

Key observations
* The given graph is a tree, so any connected subgraph is also a tree.
* In a valid subgraph each vertex has degree 1 or 4, and there is at least one degree‑4 vertex.
* If we root the original tree arbitrarily (say at 1), any valid subgraph has a unique vertex whose edge to its parent is **not** used. Call that vertex the *root* of the subgraph. For that root the incident edges in the subgraph are only to some of its children.
* Therefore every valid subgraph can be described as:
  * pick a vertex `v`;
  * decide whether `v` has degree 1 (connects to exactly one child) or degree 4 (connects to exactly four children);
  * for each chosen child we attach a connected subtree that contains the child and uses the edge to `v`.

Thus we only need DP values for a vertex when the edge to its parent **is** used.  
For a child `c` we need:
* `best_up[c]` – size of the best valid subtree inside `c`’s subtree that contains `c` and is connected to its parent (i.e. uses the edge `c–parent`).  
  The child can be a leaf (size 1) or a degree‑4 node (uses the parent edge + exactly three of its own children).  
  So `best_up[c] = max(1, deep_up[c])` where `deep_up[c]` is the size when `c` is degree 4.
* `deep_up[c]` – size when `c` is degree 4 (connected to parent).  
  This requires at least three children and `deep_up[c] = 1 + sum of the three largest `best_up` values of its children`.  
  If fewer than three children, `deep_up[c]` is impossible.

Now for a vertex `v` (treating its parent side as **not** used) we have two possibilities:

1. **Root degree 1** – `v` connects to exactly one child.  
   The whole subgraph then consists of `v` and a child subtree where that child must be degree 4 (otherwise we would have no degree‑4 vertex at all).  
   So `root1[v] = 1 + max deep_up[child]` if some child has `deep_up` defined, else impossible.

2. **Root degree 4** – `v` connects to exactly four children.  
   The subgraph always contains a degree‑4 vertex (`v` itself), so any choice of children is allowed.  
   `root4[v] = 1 + sum of the four largest best_up[child]` if `v` has at least four children, else impossible.

The answer is the maximum of all `root1[v]` and `root4[v]`. If none exist, output `-1`.

DP computation
* Root the tree at 1 and compute a parent array and a processing order (post‑order).
* For each node in post‑order collect `best_up[child]` and also track the maximum `deep_up[child]`.
* Compute `deep_up[v]`, `best_up[v]`, `root1[v]`, `root4[v]` and update the global maximum.
* Use `heapq.nlargest` to obtain the top 3 / top 4 values (O(deg · log 4) = O(deg) per node, overall O(N)).

The algorithm works in O(N) time and O(N) memory, easily handling N ≤ 2·10⁵.

## worker: Implement the DP algorithm in Python: read input, 
- The DP correctly models an alkane subgraph: internal nodes (except the root) have either 0 children (leaf) or exactly 3 children (degree 4), and the root has either 1 or 4 children.
- `deep_up[v]` captures the best subtree where `v` is degree 4 and connects to its parent; `best_up[v] = max(1, deep_up[v])` is the best size for a parent to attach.
- For a vertex as the root of the whole alkane we have two possibilities:
  * degree 1: it must attach to a child that is degree 4 (`root1`).
  * degree 4: it attaches to any four children, using their `best_up` values (`root4`).
- The global maximum over all vertices yields the largest possible alkane subgraph.
- Complexity: O(N) time and O(N) memory; each node processes its children once, and `heapq.nlargest` on at most 3 or 4 elements is constant work.
- The code handles N up to 2·10⁵, uses an iterative DFS to avoid recursion depth issues, and prints `-1` when no valid alkane exists.
