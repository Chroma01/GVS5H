We need to partition a tree of `NK` vertices into `N` simple paths, each of exactly `K` vertices. Each path must consist of edges, so internal vertices have degree 2 within the path, while endpoints have degree 1 within the path (except when `K=1`, where a path is a single vertex).

A standard necessary condition is that the number of odd-degree vertices must be exactly `2N` (each path contributes two endpoints). If `K=1`, every vertex is a path endpoint so we need every vertex to be a "path" alone, which is always possible — output `Yes`.

If `K>=2`, a necessary and sufficient condition for partitioning a tree into simple paths of fixed length is: the number of leaves (degree 1) must be at most `2N`, and the number of vertices of degree 1 plus twice the number of vertices of degree >= 3 must allow the tree to be "pruned" of `N` paths of length `K`.

The standard approach uses bottom-up DP/greedy: root the tree, do DFS, and at each node collect leftover "half-paths" from children. Each child returns the length of the dangling path it can pair with a sibling. If two child half-paths exist, they merge into a full path of `K` vertices (counted as one completed path). Otherwise, if only one half-path exists and we can extend it through this node, it becomes a half-path of length+1 propagated upward. If a child returns a full completed path, we just count it.

Specifically, in DFS at node `u` (parent `p`):
- Initialize `cnt = 0` (number of half-paths from children that we can still pair).
- For each child `v != p`:
  - Get `path_len` from child `v`.
  - If `path_len == 0`: child `v` completed its own full path internally (in its subtree), do nothing.
  - Else if `path_len == K`: impossible (path longer than needed).
  - Else (1 <= path_len < K): this child has a dangling path of `path_len` vertices. Increment `cnt` by 1.
- After processing children, if `cnt >= 2`: pair two of them (their combined path with current node as middle would be at most K+2, but we only need the dangling segments to be merged with this node). Specifically, if we pair two half-paths of length `a` and `b` through node `u`, total path length becomes `a + b + 1`. If `a + b + 1 == K`, we have completed a path; else if `< K`, the merged half-path has length `a + b + 1` and propagates up.
- If `cnt == 1`: we have one dangling half-path of length `a`. We can extend it through `u` to length `a + 1` and propagate up (only if `a + 1 < K`).
- If `cnt == 0`: return 0 (no dangling path).

If at any point we attempt to propagate a half-path of length `K`, we get a full path; that means we pair it with a "virtual" parent path or it's a leaf-to-leaf path. Actually a cleaner formulation:

At each node, gather all child "dangle lengths" `d` where `0 < d < K`. We can greedily pair the longest with the shortest, or simply sort and pair. Pairing two dangles of lengths `a, b` through node `u` makes a path of length `a + b + 1`. If this equals `K`, we completed a path (count it, don't propagate). If `< K`, the merged dangle of length `a+b+1` is added back to the pool. After pairing, at most one dangle remains (since the tree is a tree and paths are simple). That remaining dangle propagates up to the parent.

At the root (parent = 0), after processing, there should be at most one dangle of length `< K`, and the total number of completed paths should be exactly `N` (or `N-1` if root has one dangle of length `K`... but root has no parent, so a dangle must be a full path of length `K`; that counts as a completed path).

Let me reconsider. When the DFS returns to its parent, the value returned is the length of the dangling path (or 0 if none). The parent then tries to merge. Actually let's define:
- Each leaf returns a dangle of length 1.
- When node `u` with parent `p` processes children, it collects their dangles. It sorts and tries to pair them. Each pair of dangles of lengths `a, b` from children: if `a + b + 1 == K`, that's a complete path; if `a + b + 1 < K`, add `a+b+1` back to the pool; if `> K`, impossible. After greedy pairing (pair largest with smallest, or any valid pairing), at most one dangle remains. That dangle (length `L < K`) is returned to the parent.

At the root, if the final dangle has length `K`, it counts as a path. Otherwise it must be 0 and the number of completed paths equals `N`.

Greedy: sort dangle lengths. Use two pointers or a multiset. Actually, since we just need to know feasibility, we can: collect all dangle lengths from children, sort ascending. Greedily pair shortest with longest? No, the constraint is `a + b + 1 <= K` and we want exactly `K` to complete. Hmm, but actually we don't need exactly `K` when pairing — if `a + b + 1 < K`, we propagate a longer dangle. 

Let me think again with a cleaner DP.

**DP formulation** (standard for "tree partition into paths of length L"):
- Root the tree at an arbitrary node, say node 1.
- DFS returns: the length of the longest "upward" dangle path that hasn't been closed, or -1 if none (meaning subtree is fully decomposed). But the dangle length must be between 1 and K-1 (if K>=2).
- Actually, let's define `f(u)` = the length of the dangle path from `u` going up to its parent, where this dangle is an unclosed path of length `d` (1 <= d < K) within `u`'s subtree that needs to be closed by ancestors. If no such dangle, return 0.

At node `u` (parent `p`):
- Collect `dangles = [f(v) for v child of u, v != p, where f(v) > 0]`.
- Sort `dangles`.
- Try to pair dangles: pair shortest with longest such that sum + 1 <= K. When we pair two dangles of length `a` and `b` through `u`, the total path length is `a + b + 1`. If equals K, great (path closed). If < K, the new dangle has length `a + b + 1`. This is like a multiset operation.

Greedy strategy: repeatedly take the two smallest dangles, check if `a + b + 1 == K` (close) or `< K` (merge into new dangle) or `> K` (impossible). Use a min-heap or sort and use two pointers. Since we're at a single node and tree size is up to 2e5, this must be efficient.

Actually, the standard approach is: since we want to minimize the number of leftover dangles and maximize closed paths, we can sort dangles ascending and use two pointers (smallest and largest) to pair them. For each pair (a, b) where a <= b: if a + b + 1 == K, closed; if a + b + 1 < K, then the new dangle of length a+b+1 must be paired with someone else (so add to a list of "intermediate" dangles). But this gets complicated.

Let me use a cleaner greedy: multiset of dangle lengths. While size >= 2:
- Take two smallest a, b.
- If a + b + 1 == K: closed (count++).
- If a + b + 1 < K: push a+b+1 back.
- If a + b + 1 > K: impossible.

Wait, taking two smallest might not be optimal. Consider a + b + 1 < K for the two smallest, but the result needs to be paired with the next smallest, etc. Actually this is similar to the problem of partitioning into groups with sum constraints.

Let me reconsider. The standard solution for AtCoder ABC's "Tree Path" problem (this looks like it):

The problem is: given a tree, can it be partitioned into paths of length K? This is a known problem. The solution:
- K = 1: always Yes.
- Otherwise, necessary condition: number of leaves = L must be <= 2N (since each path has 2 endpoints, but a path can have 0 leaves if it's internal? No, every path has exactly 2 endpoints, but if K = NK, the single path has 2 endpoints which are leaves or the whole tree). Actually the condition is that the number of vertices of degree 1 must be <= 2N.
- Sufficient condition: Use the greedy DFS described, and also check that no node has degree > some limit? Actually if K is small, a high-degree node might need to pair many dangles.

Let me look up the standard approach for this exact problem. The problem matches AtCoder ABC 133 F or similar? Actually it looks like ABC 149 F? No, it's "Tree Decomposition" type.

The problem: partition tree into N paths of length K. NK vertices.

**Algorithm (standard)**:
1. If K = 1: output Yes.
2. Root tree at node 1. Do DFS.
3. In DFS(u, p):
   - If u is a leaf (only edge to p): return 1 (dangle of length 1).
   - Collect `dangles = []`.
   - For each child v: `d = DFS(v, u)`; if d == 0, continue; if d == -1, return -1; else `dangles.append(d)`.
   - Sort dangles.
   - Use two pointers: i = 0, j = len(dangles)-1.
   - While i < j:
     - a = dangles[i], b = dangles[j].
     - total = a + b + 1.
     - If total == K: i++, j--, count++ (closed a path).
     - Elif total < K: we can't pair i with j if total < K because we need exactly K? Wait, if total < K, then this pair doesn't close a path. We need to merge. But if we pair smallest with largest and total < K, then all pairs would also be < K. This means we have too much "slack". Hmm.
     - Actually, we want to pair dangles such that a + b + 1 = K to close paths. If we can't achieve exactly K, we might need to propagate a dangle.

Let me reconsider. The dangle from a child of length `d` means there's an unclosed path of `d` vertices in the child's subtree, and the `d`-th vertex is adjacent to `u`. When we bring it to `u`, we can:
- Close it with another dangle: if we have two dangles of length `a` and `b`, and `a + b + 1 == K`, we close the path (u is the middle, or one of them is).
- Extend one dangle: take one dangle of length `a`, the path is extended through `u`, new dangle length `a + 1`. This happens when there's an odd one out.
- Or if no dangles, return 0.

So at node `u`, we have a multiset of dangle lengths from children. We can:
1. Pair two dangles: if `a + b + 1 == K`, remove both, increment count.
2. If after pairing all possible (a+b+1=K), there are leftover dangles, we can only have at most one leftover, and its length is whatever remains.

But the pairing is not straightforward because the order matters. Actually, since we're at a single node and all dangles meet at `u`, any two dangles can be paired through `u`. The new path is the concatenation of the two dangle paths plus `u`. The length is `a + b + 1`. We want this to equal `K` to form a complete path.

But what if `a + b + 1 != K`? Then we can't form a complete path with this pair. We have two options:
- Form a new dangle of length `a + b + 1 < K` (if sum < K) and put it back in the pool. But then this new dangle's "endpoint" is at `u`, and it must be closed by an ancestor.
- Or if `a + b + 1 > K`, impossible.

So the operation is: take two dangles a, b, if a+b+1 < K, replace with a+b+1; if a+b+1 == K, remove both (closed); if > K, fail.

We want to end up with at most one dangle of length < K (which propagates up), and maximize the number of closed paths.

**Greedy**: Since we want to close as many paths as possible and minimize the leftover dangle length, we should pair dangles such that `a + b + 1` is as close to K as possible. Actually, we want `a + b + 1 = K` exactly to close. If we pair and get < K, the new dangle is longer, which is better (closer to K) for future pairing.

Standard approach: sort dangles. Use a deque or multiset. Pair smallest with largest. If a+b+1 < K, the new dangle is inserted; if == K, closed; if > K, impossible. Since pairing smallest with largest minimizes the max sum, this greedy works.

Wait, pairing smallest with largest: if smallest + largest + 1 < K, then all pairs (smallest, x) would have x >= smallest, so sum >= 2*smallest + 1. Hmm.

Let me test: dangles = [1, 1, 1], K = 4. Pair 1 and 1: 1+1+1=3 < 4, new dangle 3. Pool: [1, 3]. Pair 1 and 3: 1+3+1=5 > 4, fail. So we should have paired 1 and 1 differently? No, only one way. Result: fail, but is it really impossible? Let's see: node u has 3 children, each with dangle 1. We can form one path of length 3 (1+1+1) which is < 4, and have one dangle of length 1 left, and one dangle of length 3 left. They can't pair (1+3+1=5>4). So we have leftover dangle 3 and dangle 1. We can only propagate one. So we need to choose: propagate the 3 (and lose the 1, but the 1 is "wasted" or rather the subtree under the 1-child is not fully decomposed — wait, no, the dangle 1 means a path of length 1 going up, which is just the child itself. If we don't close it, it propagates up. But we can only propagate one.

Hmm, but the child with dangle 1: that means in its subtree, there's a path of length 1 (just the child vertex) that needs to be closed by an ancestor. If we don't close it here, we propagate it. But the child subtree might be fully decomposed except for this dangle. Actually, the dangle represents an unclosed path. We must close it somewhere.

So with dangles [1,1,1] and K=4: we can close one path of length 1+1+1=3 < 4, which gives a dangle 3, but we also have the third dangle 1. We can pair dangle 3 and dangle 1: 3+1+1=5 > 4, fail. So we can either:
- Close the 1+1 pair (length 3, dangle 3) and propagate dangle 3, leaving dangle 1 "unclosed" in its subtree. But the child returned dangle 1, meaning that child's subtree has an unclosed path of length 1. If we don't close it at u, it propagates up. But we can only propagate one dangle from u. So the other dangle is lost — impossible.

Wait, I think the issue is that we can't just "lose" a dangle. Every dangle must be either closed at u or propagated up. Since we propagate at most one, the rest must be closed at u. So we need to pair all dangles into closed paths or one leftover.

So the question is: can we pair dangles from a multiset into groups (pairs) such that each pair sums to K-1, with at most one leftover? This is a matching problem.

For the example [1,1,1], K=4, we need pairs summing to 3. We have three 1s. We can form one pair (1,1) summing to 2 < 3, and one leftover 1. But (1,1) sums to 2, not 3. To close, we need exactly K-1=3. So a+b must equal 3. 1+1=2 != 3. So we can't close any path. Thus fail.

But wait, the dangle from a child of length 1 means a path of 1 vertex in the child subtree. When we combine two dangles a=1 and b=1 through u, the total path is child_a - u - child_b, which has 1+1+1 = 3 vertices. For K=4, this is too short. We can't close it. So we can only form a dangle of length 3 going up. But we have three dangles, so we can form one dangle of length 3 (from two of the 1s) and have one dangle of length 1 left. These can't merge (3+1+1=5>4). So we'd need to propagate the 3, but the 1 is left unclosed. Impossible.

What if we propagate the 1? Then the 3 is left. 1 propagates up (dangle 1), and we have a dangle 3 from the pair. But the pair (1,1) through u is a path of length 3. If we don't close it, it's a dangle of length 3. So the multiset at u becomes {3} (from the pair) and {1} (the third child). We must close or propagate. Since we can propagate at most one, and 3+1+1=5>4, impossible.

So the algorithm needs to pair dangles to form closed paths (sum exactly K-1) or merge them into a new dangle (sum < K-1). The greedy of pairing smallest with largest and checking if sum+1 == K is correct for the "close" case, but for the "merge" case, we need to be careful.

Actually, here's a cleaner greedy from the editorial of similar problems (e.g., AtCoder ABC 149 F or Codeforces):