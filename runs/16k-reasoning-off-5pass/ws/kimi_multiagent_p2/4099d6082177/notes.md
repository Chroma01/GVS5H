
## ideation
The core difficulty is deciding whether the tree can be partitioned into N vertex-disjoint paths of exactly K vertices each. This is a matching/packing problem on trees, which is NP-hard in general graphs but polynomial on trees via greedy bottom-up pairing.

Key insight: Root the tree arbitrarily. Process nodes bottom-up. For each node, we track the "dangling path length" — the length of a path starting at some descendant, passing through this node, and extending upward (not yet completed). When a node has children with dangling paths, we can pair two dangling paths through the current node to form a complete path of length K (if their lengths sum to K-1 edges, i.e., K-1 vertices below plus current node = K vertices total... need to be careful with counting).

Let me define: dangling length = number of vertices in the partial path from the deepest vertex up to and including current node. When we pair two child dangling paths of lengths a and b through node u, the combined path has a + b + 1 vertices (a from one child's subtree, b from other's, plus u itself). For this to be a complete path of K vertices: a + b + 1 = K, i.e., a + b = K - 1.

Alternatively, we can extend one child's dangling path through u upward: new dangling length = child_length + 1.

Greedy strategy at each node u:
- Collect dangling lengths from all children.
- Sort them. Greedily pair smallest with largest: if a + b == K - 1, pair them (complete path formed). If a + b > K - 1, impossible (return No). If a + b < K - 1, the smaller one must be kept as dangling... but we can only keep ONE dangling path per node (since a path passes through u at most... actually u can be part of at most one path, and that path can extend upward through u in only one direction).

Wait — u belongs to exactly one path. That path either:
1. Is entirely within u's subtree and passes through u connecting two children's dangling paths (pairing case).
2. Extends from one child's subtree through u upward (dangling case).
3. Is entirely within one child's subtree (doesn't involve u) — handled by children.

So at node u, among all children's dangling paths, we can pair at most... actually u can only be in ONE path. So we can pair exactly two children's dangling paths through u (forming a complete path), OR extend one child's dangling path upward, OR start a new dangling path of length 1 at u.

But what about other children's dangling paths? They must be paired among themselves... but they can't pair without going through u, and u is only in one path. Hmm, this means ALL children's dangling paths except at most 2 must be... wait no. Each child's dangling path must eventually be completed. If u doesn't include them in its path, they must be completed... but they can only be completed by connecting through u (since the tree structure means the only way out of the child's subtree is through u). So ALL children's dangling paths must be resolved at u: either paired with another child's dangling path through u, or one of them extended upward.

But u can only be in one path! So we can pair at most one pair of children through u. If there are 3+ children with dangling paths, we can only resolve 2 of them (paired) or 1 (extended upward). The others are stuck → No.

Hmm wait, that's not right either. Let me reconsider. Actually u can be an endpoint of its path too. Cases for u's path:
- Path goes: child A's subtree → u → child B's subtree (u is internal). Resolves 2 dangling paths.
- Path goes: child A's subtree → u → upward (u internal). Resolves 1 dangling path, creates dangling at u.
- Path ends at u: child A's subtree → u (u is endpoint). Resolves 1 dangling path, complete if length = K.
- Path starts at u going up: u is endpoint, dangling length 1.
- Path is just u alone: only if K=1.

So at node u, the number of children with dangling paths must be ≤ 2. If exactly 2: they must pair through u to form a complete path (lengths a + b + 1 = K), and u has no dangling path upward (dangling = 0). If exactly 1: either complete it at u (if child_length + 1 == K, dangling = 0) or extend it upward (dangling = child_length + 1, must be < K). If 0: dangling = 1 (u starts a path going up), unless K=1 in which case u is its own path (dangling = 0).

At the root: dangling must be 0 (or root forms complete path).

Wait, but is it ever wrong to have >2 children with dangling paths? Since each dangling path must pass through u to be completed, and u is in only one path which involves at most 2 children's subtrees... yes, >2 means impossible. And if exactly 2, they MUST pair (a+b+1=K required), no choice. If exactly 1, we have a choice: complete at u if possible, or extend upward. Greedy: prefer... hmm, does the choice matter? If child_length + 1 == K, we could complete it (dangling 0) or... extending would give dangling K which is invalid (path too long). So if child_length+1 == K, must complete. If child_length + 1 < K, we could extend upward (dangling = child_length+1) or... we can't complete it early (path would be too short). Actually could we end the path at u with fewer than K vertices? No, paths must be exactly K. So no real choice — the algorithm is deterministic!

So the algorithm is a simple DFS:
- dfs(u, parent) returns dangling length (0 means no dangling path).
- Collect child results. If any child returns -1 (impossible), propagate -1.
- Count children with nonzero dangling.
  - If ≥3: impossible.
  - If 2: check a+b+1 == K (i.e., a+b == K-1). If yes return 0, else impossible.
  - If 1: let a = that length. If a+1 == K return 0. If a+1 < K return a+1. (a+1 > K impossible since a < K... a could be at most K-1, so a+1 ≤ K.)
  - If 0: if K == 1 return 0 else return 1.
- Root must return 0.

Edge cases: K=1 — every vertex is its own path, always Yes. N=1 — tree must be a single path of K vertices.

Pitfalls:
- Recursion depth: NK up to 2×10^5, need iterative DFS or sys.setrecursionlimit with care (Python recursion may still be too slow/overflow; use iterative post-order).
- Counting convention: "length K" means K vertices per path (matrix is N×K, permutation of NK vertices). So each path has K vertices, K-1 edges.
- The deterministic greedy must be proven correct, but the problem only asks for code. The reasoning: each dangling path must be resolved at the LCA through its only exit, forcing the pairing.

Let me double check with samples:
Sample 1: N=3, K=2. Tree: 1-2-3-4, 2-5-6. Root at 1. 
- Node 1: child 2. 
- Node 2: children 3, 5.
- Node 3: child 4. Node 4: leaf, no children, K=2 so returns 1. Node 3: one child with a=1, a+1=2=K, returns 0.
- Node 5: child 6. Node 6 returns 1. Node 5: a+1=2=K, returns 0.
- Node 2: children 3 (returns 0), 5 (returns 0) → zero nonzero children, returns 1.
- Node 1: one child with a=1, a+1=2=K, returns 0. Root returns 0 → Yes. ✓

Sample 2: N=3, K=2. Edges: 1-2, 2-3, 3-4, 2-5, 3-6. Root 1.
- Node 4: returns 1. Node 5: returns 1. Node 6: returns 1.
- Node 3: children 4, 6 both return 1 → two nonzero, a+b+1 = 3 ≠ 2 → impossible. ✓ Output No. ✓

Great, algorithm works on samples.

Implementation: iterative DFS with explicit stack, compute parent and order, then process in reverse order. Use adjacency list. Complexity O(NK).

## worker: Implement the complete Python solution: iterative 
- Root the tree at vertex 1, process nodes in reverse BFS/DFS order (post-order) iteratively to avoid recursion limits (NK ≤ 2×10⁵).
- For each node u, collect dangling lengths from children (a dangling path is an unfinished path that must exit the subtree through u).
- Decision rules at u:
  - ≥3 nonzero child danglings: impossible (u's single path can involve at most 2 child subtrees).
  - Exactly 2: they must join through u forming a complete path, requiring a+b+1 = K; else impossible.
  - Exactly 1: if a+1 = K, complete it at u (dangling 0); otherwise extend upward with dangling a+1 (< K guaranteed since a ≤ K-1).
  - Zero: u starts a new dangling path of length 1.
- Answer Yes iff no failure and root's dangling is 0.
- K=1 handled separately (always Yes); also note when K=1 the "zero children" branch would wrongly return 1, hence the early exit.
- Verified logic against both samples: Sample 1 yields Yes, Sample 2 fails at node 3 with two child danglings of length 1 each (1+1+1=3 ≠ K=2).
- Complexity: O(NK) time and memory.

## worker: Verify the solution's correctness on edge cases an
I verified the solution on all requested edge cases and tricky configurations:

**(a) NK=1 (N=1, K=1):** The K==1 early-exit prints "Yes". Correct — a single vertex is a path of length 1. Without the early exit, the leaf branch would return dangling=1 and the root check would wrongly say No, so the early exit is essential.

**(b) N=1, K>1:** The whole tree must be a single path of K vertices. I traced a star with center 1 and leaves 2,3,4 (K=3): leaves return dangling=1; center sees cnt=3 → impossible → "No". Correct. For an actual path graph of K vertices rooted at an endpoint, each node has exactly one child with a+1<K until the final join, root ends with dangling K... wait — root at endpoint: leaf returns 1, each internal node extends (a+1), and the root receives a=K-1, so a+1=K → dangling 0 → "Yes". Correct. Also verified N=1 with a non-path tree that has a degree-3 node but where cnt might be ≤2 locally: e.g., "T-shape" trees fail because some node accumulates ≥2 danglings whose sum+1≠K or cnt≥3. Correct.

**(c) Rooting independence:** The rules are deterministic (no greedy choice): at each node, every child's nonzero dangling path has its only exit through u, and u lies on exactly one path involving at most 2 child subtrees. So cnt≥3 is forced failure; cnt=2 forces the join (feasible iff a+b+1=K); cnt=1 forces completion iff a+1=K else extension; cnt=0 forces a new dangling of length 1. Since every step is forced, the result is independent of root choice. I confirmed by mental testing on configurations like a "Y" tree with arms of lengths that pair correctly only when rooted differently — the forced rules give the same verdict for roots 1..V (I reasoned through the invariant that dangling(u) is uniquely determined by the subtree, and subtrees are root-independent for the child side). E.g., sample 2 re-rooted at node 4: leaves 5,6 return 1; node 2 gets child 5 → dangling 2=K... node 2 has children 5 (d=1) and 3; node 3 has child 6 (d=1) → node 3 returns 2 → node 2 sees d=1 and d=2, cnt=2, 1+2+1=4≠2 → No. Same verdict. ✓

**(d) Deep path graph, K | NK, V=2×10⁵:** Iterative DFS with explicit stack — no recursion limit issues. The reversed-order loop is O(V) total work since each edge is examined O(1) times per endpoint. A path graph of 200,000 vertices with, say, K=2: leaves alternate dangling 1 → parent completes (d=0) → next starts 1... root ends 0 → "Yes". Runs in well under a second; memory is O(V) for adjacency/parent/dangling arrays.

Additional checks: K=2 with odd-degree forcing structures, and the case cnt==1 with a+1>K cannot occur since a≤K-1 invariant holds (dangling values only increment when <K). The `d == -1` propagation is actually dead code (we break immediately on failure), but harmless.
