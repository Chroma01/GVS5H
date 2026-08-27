We need to partition a tree of NK vertices into N vertex-disjoint simple paths of length K (K vertices, K-1 edges each). The tree structure must allow every vertex to be used exactly once. A known necessary and sufficient condition for such a decomposition is that the tree's degree constraints match the path cover: every vertex used as an interior point of a path must have degree at least 2 (actually exactly 2 in the path, but at least 2 in the tree after accounting for path endpoints), and vertices used as path endpoints must have odd leftover degree after pairing.

More concretely, think of each path contributing: two vertices of degree 1 in the path (its endpoints) and K-2 interior vertices of degree 2. The total number of edges used in paths is N*(K-1) = NK - N. The remaining N-1 edges of the tree (if any) are unused by the paths (since tree has NK-1 edges). For a decomposition to exist, the "path degree" of each vertex (number of incident path edges at that vertex) must be ≤ its degree in the tree, and sum to 2(NK - N) across all vertices. Also the number of vertices that have path-degree 1 (endpoints) must be exactly 2N.

A known reduction: This problem is equivalent to checking whether we can "remove" N-1 edges from the tree such that every resulting component is a path of exactly K vertices. Equivalent to: can we pair up vertices of odd degree in a certain matching on edges.

A cleaner characterization: For NK=1 trivial; otherwise K≥2. Let d(v) be degree. Define excess e(v) = d(v) - 2. Sum of d(v) = 2(NK-1), so sum e(v) = 2(NK-1) - 2NK = -2. Thus number of vertices with e(v) < 0 (i.e., leaves) is at least 2. For a path decomposition, we need exactly 2N vertices with path-degree 1 (endpoints). After removing N-1 edges to break tree into N path components, each component being a path of K vertices contributes exactly 2 endpoints, so total 2N endpoints. The other vertices (interior) have path-degree 2.

A known sufficient condition (from competitive programming solutions to this exact problem on AtCoder ABC 274 F / similar): the tree can be decomposed into N paths of length K iff when we repeatedly remove leaves that belong to components of size 1 (size measured in vertices), we can process the tree. Actually the standard solution for "decompose tree into paths of length K" is a greedy/DFS approach: root the tree arbitrarily, compute subtree sizes, and for each node if its children's subtrees have accumulated size that is a multiple of K, cut them off. Also handle the remaining part going up.

Let me recall the known problem: AtCoder ABC 274 F? No, I recall a problem "Tree Decomposition" where we need to split tree into paths of length K. The solution: do DFS, for each node compute the "up" remainder size (number of vertices in the component containing this node and its parent that hasn't been assigned to a completed path). When processing children, if the child's accumulated remainder size mod K equals 0, we can finalize a path through that child up to here. Otherwise, we accumulate. At the root, the final remainder must be 0.

More precisely, for each node u, define sz[u] = size of the "incomplete path" component containing u and its parent (if any). Process DFS: for each child v, get sz[v] from recursion. If sz[v] == 0, it means child's subtree was already fully decomposed into K-paths without needing to connect to u. If sz[v] != 0, we have an incomplete path coming from v's side into u. We need to merge these partial paths.

Actually the known result: It's possible iff for every vertex v, d(v) ≤ N (something)? No, let me think more carefully.

Let me reconsider. The problem of partitioning a tree into paths of exactly K vertices each. This is a known problem. The condition is that it's possible iff when we root the tree and do DFS, at each node, the set of "open" path fragments from subtrees can be merged pairwise (since at any junction, paths going through the node must either turn (use 2 of the node's edges) or end at the node). The node has degree d(v) edges available. In the decomposition, at each node, the number of path segments that pass through the node (each such segment uses 2 edges of the node, entering and leaving) plus the number of path endpoints at the node must equal d(v). Each "through" uses 2 edges, each endpoint uses 1 edge. So: 2*through + endpoint = d(v), with through + endpoint being the contribution to path count at this node, and total endpoints across all nodes = 2N.

This is a parity/flow problem. A known approach: root the tree, do DFS. For each node, compute the "remainder" of the path fragment going up. Initially each child contributes its remainder upward. The node can pair up remainders from children (connecting two child fragments through this node, which uses 2 edges and the node becomes interior of a path). Unpaired remainders propagate up. Also, if no remainder is propagated up and the node is not the root, the node might need to start a new fragment... 

Actually, let me recall the exact algorithm from AtCoder. I think the problem is "Tree Path Decomposition" and the solution is:

DFS from root. For each node u, return the "size of the pending path" that needs to connect upward through u. When visiting a child v, we get pending[v]. If pending[v] == 0, child is done. Otherwise, we have a path fragment of length pending[v] from v's subtree that needs to extend upward. We try to extend it through u. We maintain a counter `cnt` = number of vertices accumulated in the current path going up. For each child with pending != 0, we do cnt += pending[child]. If cnt == K, great, this completes a path (using u and the contributing subtrees). If cnt > K, then... actually we should be more careful.

Let me redefine. Let's define that the DFS returns the number of vertices in the "incomplete path" component that contains the parent edge. So when we call dfs(u, parent), for each child v, we get back `s_v` = the size of the incomplete component containing the edge (u,v) — i.e., the number of vertices in v's subtree that are part of the same path fragment that must be completed by going through u and then up to u's parent.

For a leaf: returns 1 (the leaf itself is a fragment of size 1 going up).

For internal node u: collect s_v from all children. Sort them. Try to greedily match: pair smallest with others? Actually, we need to form paths of exactly K. The fragment at u can be extended by combining child fragments. The number of vertices available at u's level (from children) is sum of s_v. Plus u itself is 1 vertex. The total vertices in the component containing u's parent is 1 + sum of s_v (since u is included and all child fragments connect through u). Wait, but some child fragments might be "closed" (form a complete path of K) without needing to include u.

Rule: If s_v + 1 == K (where +1 is for u connecting to the child fragment making it length K), then that child fragment plus u form a complete K-path, so we don't propagate it up. Otherwise, s_v contributes to the upward fragment.

More precisely: we can think of it as: the incomplete component at u (going up to parent) has some size. We want this size to be such that when we finally close it (at some ancestor or root), it becomes exactly K.

A clean algorithm:
- DFS(u, parent):
  - pending = 1 (u itself)
  - For each child v:
    - s = DFS(v, u)
    - if s == 0: child fully decomposed, continue
    - if pending + s == K: complete a path here! pending = 0 (but wait, we might still have more children? Actually, once pending is used, reset to 0 meaning "we are ready to start fresh", but if there are more children with fragments, they'd start new paths. Hmm, but a single path goes through u, so we can only have one "incomplete" path going up from u at most. But u has multiple children — fragments from multiple children could merge into one path going up, but that would require the path to branch, which is impossible for a simple path.
  - So actually, at node u, we can have at most one incomplete path going up (since paths are simple and non-branching). The fragments from different children either form complete paths among themselves + u, or at most one of them (plus u and possibly other fragments) continues up.

Let me reconsider. The fragments from children are path-segments that have one endpoint at child v and the other endpoint somewhere in v's subtree. These segments need to be extended through u. Since u has degree d, and each segment passing through u uses 2 edges of u (one to child, one to parent or to another child). A path is linear, so it enters u from one child and exits to exactly one other place (another child or parent). So at u, the "incomplete segments" from children can be paired with each other (forming a path that goes child1 -> u -> child2), or one of them extends to parent, or a segment ends at u (endpoint).

In terms of our DFS returning one value, we can only propagate one segment upward (since a simple path has at most one direction to the parent). So the segments from children must be resolved at u (paired among themselves, or end at u). 

Algorithm (standard for this problem):
- DFS(u, parent) returns a multiset or just tracks the "current sum modulo K" or similar.
- Actually, I recall now: the solution uses the fact that we can decompose the tree into paths of length K iff for every vertex v, d(v) ≤ 2*N/something... no.

Let me search my memory for the exact problem. This is AtCoder ABC 274 F? No, I think it's "ABC 287 F"? No. Let me think... "N paths of length K" — this is likely "AtCoder Beginner Contest" or "AtCoder Regular Contest". The problem with NK vertices decomposed into N paths of length K.

I recall the solution: Do a DFS. At each node, collect the "return values" from children. The return value of a child is the number of vertices in the incomplete path segment in that child's subtree that is connected to this node. If the child's segment size + 1 (this node) == K, then the segment is completed (the path of K vertices is formed using the child's segment and this node). Otherwise, we add the child's segment size to a running total at this node (accumulating fragments that will form one path going up). But we can only accumulate one such "going up" path. If two children both have incomplete segments, we need to check if their sum + 1 == K, etc.

Actually, the correct greedy: At node u, we maintain `acc` = 0 initially. For each child v with return value s_v (meaning there's an incomplete path of s_v vertices in v's subtree that has one endpoint at v and extends toward u, and needs K - s_v more vertices including u going up):

- If s_v == -1 (meaning child subtree is fully decomposed, no pending), skip.
- We want to combine pending segments. The idea: a pending segment from v of length s_v, when it reaches u, can either:
  (a) combine with another pending segment from another child w to form a path v...u...w (using s_v + s_w + 1 = K vertices, where +1 is u). This completes a path and clears both.
  (b) extend upward through u to parent: the segment becomes s_v + 1 vertices long (adding u), pending up.
  (c) end at u: the segment of s_v vertices plus u (total s_v+1) might equal K, completing it.

But (c) is just the case where the segment going up has exactly K-1 vertices from child and adding u makes K, which is handled.

So at node u, we can have multiple pending segments from children, but we can only send one upward (since a path is linear and the parent is one direction). The others must either pair among themselves through u (using u as connector) or be impossible (if counts don't match).

Specifically, if we have pending segments with sizes s1, s2, ..., sm from children. We need to pair them up or send one up. Each pair (si, sj) combined through u gives a path of si + sj + 1 vertices. We need this to be K. So si + sj = K - 1. The one sent up has size s + 1 (adding u), and when it finally closes at some ancestor, the total must be K.

This is complex. But there's a simpler characterization known for this problem: The answer is "Yes" iff a certain greedy succeeds: root the tree, do DFS, and for each node, if the sum of all "incomplete" subtree sizes modulo K allows completion.

Let me look up in my mind: I think the standard solution for "partition tree into paths of length K" is:

DFS(u, p):
  total = 1  (count u)
  for each child v:
    s = DFS(v, u)
    if s == K:  (child subtree is exactly a K-path disconnected from u)
      count++ (one path completed)
      total remains as is? No.
  Actually:

Let me redefine clearly. I'll define that DFS returns the size of the connected component containing u and its parent, after removing some edges. Hmm.

OK here's the clean version I recall:

Root the tree at 1. Do DFS. For each node u, compute sz[u] = size of subtree. Then, for each node, we want to know if the subtree rooted at u can be partitioned into complete K-paths, except possibly one "open" path that extends to the parent. The open path includes u and some vertices in the subtree.

DFS(u, parent):
  Let `rem` = 1 (u is in the open path initially)
  For each child v:
    child_rem = DFS(v, u)
    if child_rem == 0: continue  (child's subtree is fully partitioned)
    if rem + child_rem == K:
      // The open path from child (of size child_rem) connects to u and forms a complete K-path
      rem = 0  // u is used in this path, no open path going up from u? But u might have more children...
      // Wait, if rem becomes 0, that means u is "used up" in the completed path. But u might have other children. Those other children must form complete paths among themselves or with other nodes.
    elif rem + child_rem > K:
      return -1 (impossible, overflow)
    else:
      rem += child_rem
  return rem

Wait, but this only handles one open path going up. What if multiple children have open paths? They need to be resolved.

The issue: at node u, we might have open paths from multiple children. A path entering u from child v and exiting to child w uses two edges at u. We can only "close" two open paths at u by connecting them. But our `rem` variable only tracks one.

So the correct algorithm handles pairing of child open paths at u. Here's the refined version:

DFS(u, parent):
  multiset or list of child open sizes.
  For each child v: get s_v = DFS(v, u). If s_v > 0, add to a list.
  Now, at node u, we have several open path segments (each of size s_v) that need to be connected through u. 
  Each pair of segments connected through u forms a path of size s_i + s_j + 1 (including u).
  If we have an odd number of segments, one connects to the parent (going up), with size s_last + 1.
  Constraints:
    - For each pair (i,j) connected at u: s_i + s_j + 1 == K, i.e., s_i + s_j == K - 1.
    - For the one going up (if odd count): s + 1 must be such that it can eventually close (we return this as the open size for u's parent).
    - The count of segments must be even or one goes up.

  We need to match the s_v values into pairs summing to K-1. This is a matching problem at each node, but since tree size is large, we need an efficient way.

  Key insight: we only need to check feasibility, not construct explicitly (though construction helps). The condition at each node is that the multiset of child open sizes can be partitioned into pairs summing to K-1, with possibly one element going up (which would then need to pair at ancestor).

  But this matching is per-node and could be O(d log d) with sorting/greedy, and since sum of degrees is O(NK), total is fine.

  Specifically, at node u, we have a list of s_v values. We want to pair them such that each pair sums to K-1. If the list size is odd, one value is passed up as the open size (call it S = s_v + 1). If even, none passed up, and all must pair to K-1.

  But wait, if even and none passed up, then u is not in any open path going up. But u must be in some path. If u has even number of open child segments and they all pair through u, then u is interior of those paths (degree 2 in path for each). But u might have degree larger than the number of child segments (parent edge counts too). If no segment goes to parent, then the parent edge is not used, meaning u is a leaf of the decomposition (endpoint of a path). But then u should not be interior of paths going up. 

  Hmm, actually, if no open path goes to parent from u, that means u's connection to parent is "cut" (edge (u,parent) is not used in the decomposition). That's fine; the decomposition is a partition of vertices into paths, not necessarily using all edges. The tree has NK-1 edges, and the paths use N*(K-1) = NK - N edges. So N-1 edges are unused. So yes, edges can be "cut".

  So at node u, the open path going up (if any) means the edge (u,parent) is used in the decomposition. If no open path goes up, the edge (u,parent) is cut (not used in any path). The vertex u is still in some path; it could be an endpoint of a path (if it has degree 1 in the path) or interior (degree 2). 

  Actually, if u has no open path going up, and all its child open paths are paired (so u is interior to those pairs, using 2 edges per pair for the paths through u), then u has path-degree 2*(number of pairs). If 0 pairs (no child open paths and no parent connection), u is isolated in the path, which is only possible if K=1 (path of single vertex).

  Let me re-examine. If u has no parent open path and some child open paths paired, u is interior. If u has no child open paths and no parent open path, u is an isolated component of size 1 (needs K=1) or is connected to nothing. If u has one child open path and no parent, then u is the endpoint of that path (the path ends at u). So that child open path of size s, the path is s+1 vertices total. We need s+1 == K.

  So generalizing: at node u, the "open path" passed to parent has some size S (number of vertices in the component containing u and the parent edge, i.e., the path segment from somewhere in subtree through u to parent). The children contribute s_v for those that are connected to u via the path. The children that are not connected (their subtrees are independent paths) are "closed".

  The number of children that connect to u via the path (the "active" children) plus 1 (for parent or endpoint) determines u's role.

  But actually, it's easier to think: DFS returns either 0 (meaning this subtree is fully partitioned into K-paths with no connection to parent) or a positive integer S (meaning there's an open path of S vertices in this subtree that includes u and is connected to the parent via the edge (u,parent)).

  When DFS(u, parent) is called:
    - It calls DFS(v, parent) for all children v.
    - Each child returns either 0 or S_v.
    - For children returning 0: their subtree is fully partitioned. Ignore.
    - For children returning S_v > 0: we have an open path segment of S_v vertices in v's subtree, with one endpoint at v, extending toward u. This segment needs to be connected through u.
    
    Now at u, we have several such segments (from different children) and the node u itself. We need to connect them. The possibilities:
      (i) Pair two segments through u: segment from v_i (size S_i) and segment from v_j (size S_j) connect as v_i-path...u...path-v_j. The total path size is S_i + S_j + 1 (including u). This must equal K. So S_i + S_j = K - 1.
      (ii) Connect one segment to parent: the segment from v (size S) connects to u and extends to parent. The open size for parent is S + 1.
      (iii) The segment from v connects to u and ends at u (u is endpoint of this path). Then the path size is S + 1, must equal K. This is equivalent to connecting to a "null parent" (if u is root, or we consider this as the segment terminating).
      (iv) Multiple segments impossible to resolve (return failure).

    But we can have at most one segment going to parent (since path is linear). So the number of active children (returning S_v > 0) must be even, or odd with one going to parent.

    Specifically:
      - Let m = number of children with S_v > 0.
      - We pair up m-1 or m of them at u (using u as connector), and possibly one goes to parent.
      - Actually, each pair uses u and gives a complete K-path.
      - If m is even: we pair all m segments into m/2 pairs, each pair summing to K-1 (including u in the sum, the constraint is S_i + S_j = K-1, and then the path of S_i + S_j + 1 = K is formed). u is interior to all these paths. No segment goes to parent. Return 0 (u is not in an open path to parent). But wait, u is in the paths! Yes, u is interior to each formed path. But we return 0 meaning "no open path to parent", which is correct because the edge (u,parent) is not used.
      - If m is odd: we pair m-1 segments into (m-1)/2 pairs (each pair sums to K-1). One segment is left. This left segment, together with u, extends to parent. The open size going up is S_left + 1. Return S_left + 1.

    But there's a subtlety: what if m=0? Then no child has an open segment. u is either:
      - An isolated vertex (path of size 1, needs K=1) — but then we should treat it as a closed component. Actually if K=1, each path is a single vertex, so no edges needed, and any tree works. We handle K=1 as a special case: always Yes.
      - Connected to parent as an open path of size 1 (just u itself, going up). Then the open size to parent is 1.
      - Or u is an endpoint of a path that goes up: but this requires the path to eventually have K vertices. If m=0 and we send 1 up, then the open size is 1. At parent, it might pair or continue.

    Wait, if m=0, we have no constraints from children. We can either:
      (a) Return 0: meaning u is fully handled (u is a component by itself, valid only if K=1, or if u is a single-vertex path — but in a partition, every vertex must be in a path, and if K=1, paths are singletons, so returning 0 means "I'm a complete K=1 path").
      (b) Return 1: meaning u is an open segment of size 1 going to parent.
      (c) Return something else? No.

    But we must cover u in some path. If we return 0 and K>1, then u is a path of size 1, which is invalid (path must have K vertices). So if K>1 and m=0, we must return 1 (send u up as open segment of size 1). Then at the parent, this segment of size 1 will be extended.

    Actually wait, if m=0 and we return 0, that means the subtree rooted at u is fully partitioned, but u has no edges used in the partition. So u is an isolated vertex. In the partition into paths, an isolated vertex is only a valid path if K=1. For K>1, this is invalid. So for K>1, we cannot return 0 when m=0 (unless u is the root and m=0, in which case the whole tree is just {u}, needs NK=1, so N=1, K=1, handled).

    So for K>1 and u not the only vertex, m=0 means we must send u up as open size 1.

    For K=1: always yes, since each vertex is a path of length 1.

    Now, the constraint at each node when pairing segments: we need to pair the S_v values into pairs (s_i, s_j) such that s_i + s_j = K-1. This is a matching problem. We can sort the S_v and use two pointers to pair smallest with largest, checking if they sum to K-1. If not, fail.

    Also, we need the left-over (if m odd) to be passed up: open size = S_left + 1.

    And at the root: we must have no open path going up (since no parent). So m must be even at root, and all pairs must satisfy the sum condition. If m=0 at root and K=1, fine. If m=0 at root and K>1, then the root is an isolated vertex, but the whole tree has NK>1 vertices (since K>1 and N>=1), so there must be other vertices, contradiction. Actually if root has m=0, it means all children's subtrees are fully partitioned and no open path connects to root. Then root is isolated, invalid unless K=1 and N=1.

    Wait, for root, the return value is discarded. We just check that the root has no open path (i.e., the pairing works and m is even, or m=0 and K=1).

    Let me verify with samples.

    Sample 1: N=3, K=2. Tree: 1-2, 2-3, 3-4, 2-5, 5-6. So edges: 1-2, 2-3, 3-4, 2-5, 5-6. Degrees: 1:1, 2:3, 3:2, 4:1, 5:2, 6:1.
    Root at 1.
    DFS(1): children of 1: {2}. Call DFS(2).
      DFS(2): parent=1, children: {3,5}. 
        DFS(3): parent=2, children: {4}. DFS(4): leaf, parent=3. m=0, so for K=2, must return 1 (open size 1). So DFS(4) returns 1.
          Back to DFS(3): m=1 (from child 4, S=1). m is odd, so pair m-1=0 pairs, left is S=1. Return S+1 = 2? Wait, S+1 = 1+1=2, return 2.
          But wait, the open size to parent is 2. But K=2, so the path would be of size 2 (just 3 and 4? No, the open size 2 means the component containing the edge (2,3) has 2 vertices. That means vertices {3,4} form an open path of size 2 going to 2. But 2 is not included in the open size! The open size S_v from child v is the number of vertices in the path segment in v's subtree, not including u. So from child 3, the open path is {3,4} of size 2, with endpoint at 3. This is passed to u=2. At u=2, we receive S_v=2 from child 3.
        So back to DFS(3): child 4 returns 1. m=1 (odd). Left S=1. Return S+1 = 2. This means the open path in {3}'s subtree is size 2 (vertices 3,4), and will be extended through 3's parent.
        Now at DFS(2): children 3 and 5.
        DFS(5): parent=2, children: {6}. DFS(6): leaf, returns 1 (open size 1, since K=2).
          DFS(5): m=1 (from 6, S=1). Return S+1 = 2.
        Now at DFS(2): children return: from 3: S=2, from 5: S=2. So list of S_v = [2,2]. m=2 (even). Need to pair them: sum must be K-1 = 1. But 2+2=4 ≠ 1. Fail!
    Hmm, this gives No, but sample 1 is Yes. What's wrong?

    Oh, I see the issue. The open size S_v is the size of the path segment in child's subtree that is connected to u. But for child 3 returning 2, that means the segment is {3,4} of size 2. When it connects to u=2, the total would be S_v + 1 = 3, but K=2. So this is already too big.

    The error is in DFS(3): child 4 returns 1. At node 3, m=1, S=1. We want to form a path of size K=2. The segment from child 4 is size 1 (just {4}). We can connect it to node 3 to form a path of size 1+1=2 = K. So the path {4,3} is complete! So we should not propagate it up. Instead, we should "close" it at node 3.

    In my earlier logic, I said if m is odd, one goes up, but that was assuming we can't close it. But we can close it if the sum works. Specifically, at node u, for each child segment S_v, we can "absorb" it by adding u to the segment. If S_v + 1 == K, the segment becomes a complete K-path including u, and u is an endpoint of that path. Then u is "used" but might still have other segments.

    Refined logic at node u:
      - We have segments from children: S_1, S_2, ..., S_m.
      - We can also have the "incoming" segment from parent (if any), but since we're computing what to pass to parent, let's denote the return value.
      - Actually, let's think: node u needs to be in a path. The path passing through u (if any) will enter from one neighbor and exit to another (or end at u). So u has "path degree" 1 or 2.
      - Case A: u is interior of a path. Then the path uses two edges at u. These two edges go to two neighbors (or one to parent and one to child, or two to children). The two segments from these neighbors are connected through u.
      - Case B: u is endpoint of a path. Then the path uses one edge at u. The segment from that neighbor connects to u, and the path ends.

      In our DFS, we propagate at most one "open" segment to the parent. This open segment, when it reaches u from a child, means the child is part of the path that extends to u. If u passes an open segment to parent, it means u is interior of the path (from child through u to parent), or u is endpoint (if u doesn't pass to parent but connects to one child).

      Let's define: DFS(u) returns the size of the open path segment in u's subtree that is connected to the parent, OR 0 if there is no such segment (meaning all of u's subtree is fully partitioned into K-paths, and the edge to parent is not used).

      When evaluating node u:
        1. Start with a multiset of "incoming" segments from children that want to connect through u.
        2. Actually, each child v returns S_v, which is the size of the open path in v's subtree that has one endpoint at v and extends toward u. If S_v > 0, the path continues through u. If S_v = 0, v's subtree is done.
        3. We can think of u as having a "buffer". For each child with S_v > 0:
           - We can try to add S_v to the buffer. If buffer == 0, we set buffer = S_v.
           - If buffer > 0, we have two segments to connect: buffer and S_v. We need buffer + S_v + 1 == K (the +1 is for u connecting them). If so, we form a complete K-path, reset buffer = 0. If not, fail.
           - If buffer == 0 and we add S_v, buffer becomes S_v.
        4. After processing all children, if buffer > 0, it means there's an open segment of size buffer + 1 (adding u) that extends to parent. So return buffer + 1.
           If buffer == 0:
             - If u is the root: great, all done. But we need to check that u is in a path. If buffer==0 and u is root, and m>0, then u was interior to paths (formed by pairing). If m=0, u is isolated, which is bad for K>1.
             - If u is not root: we need to decide. If we return 0, the edge to parent is not used, and u is in a closed component. But u has no open segment, so u is "fully handled" in the partition. But is u in a valid K-path? If m=0, u has no children segments, so u is alone, invalid for K>1. If m>0 and we paired all, then u was interior to pairs, so u is in valid paths (as interior vertex). So we can return 0.

      Wait, but in step 3, when buffer==0 and we add S_v, the segment is just sitting there. It needs to be extended. But if we just store it as buffer=S_v, then later another child comes with S_w, and we check buffer + S_w + 1 == K. This connects them. If no other child comes, we have buffer=S_v left. Then we return S_v + 1 to parent.

      But what if S_v + 1 == K? Then the segment plus u forms a K-path. We should close it at u. In this case, buffer was 0, we set buffer = S_v = K-1. Then at the end, we have buffer = K-1, and we return buffer+1 = K. But K is not a valid return value (we only return sizes of open paths that are < K, since when it reaches K it's closed). So we should check: if after adding a child segment, buffer + 1 == K, then close it (buffer=0, path complete), and continue.

      Better algorithm:
        buffer = 0
        for each child v:
          S = DFS(v, u)
          if S == 0: continue
          if buffer == 0:
            buffer = S
          else:
            // try to connect buffer and S through u
            if buffer + S + 1 == K:
              buffer = 0  // completed a K-path
            else:
              return -1 (fail)
        // after all children
        if buffer == 0:
          if u is root: // but root should have handled itself
            // if K==1, this is fine (each vertex is path). If K>1, and m=0, u is isolated, fail.
            // Actually, if buffer==0 and we are at u, and we are not the root, return 0.
            // At root, after processing, if buffer==0, we are good only if the whole tree is partitioned.
            // But root itself: if buffer==0, it means root is not in an open path. Is root in a path? If during processing, root was used as connector (buffer+S+1=K), then root is interior of that path, good. If no such thing and m=0, root is isolated.
            return 0
          else:
            return 0
        else:
          // buffer > 0, open path going up
          if buffer + 1 == K:
            // path ends at u? No, the path from child of size buffer, plus u, makes K. But we are returning to parent? If buffer+1==K, the segment plus u is a complete K-path. It should not go up.
            // Actually, if buffer>0 and buffer+1==K, that means the child segment + u = K, so the path is complete. We should not propagate to parent. So return 0.
            return 0
          else:
            return buffer + 1

      But wait, there's a case: what if at node u, buffer==0, and there are no children segments (m=0). Then we return... if u is not root, we should return 1 (u itself, going up as open path of size 1). Because u is not in any closed path, so it must go up.
      In my above, for buffer==0, I returned 0. That's wrong if m=0. Correction:
        if buffer == 0:
          if there were any children processed (m>0) and all paired: return 0 (u is interior or endpoint of closed paths)
          if m == 0:
            // u is alone in its "active" set
            if u is root and K==1: return 0 (or treat as success)
            else: return 1 (u goes up as open path of size 1)

      Actually, simpler: always return the size of the open path containing the parent edge, or 0 if no such path. 
      - If m==0 and K>1: u must go up, return 1.
      - If m==0 and K==1: u is a complete path, return 0.
      - If m>0 and all paired: u is interior to the pairs, and not going up. Return 0.
      - If m>0 and one left (buffer>0): that one, plus u, goes up. Return buffer+1 (if buffer+1 < K), or if buffer+1==K, close it and return 0.

      And the check during pairing: when we have buffer and incoming S, we need buffer + S + 1 == K. This is the condition to form a K-path through u connecting two child segments.

      Let me redo with sample 1.
      Root 1.
      DFS(1): child 2. Call DFS(2).
        DFS(2): parent=1, children 3,5.
        DFS(3): parent=2, child 4.
          DFS(4): parent=3, no children. m=0, K=2>1, so return 1.
          Back to DFS(3): S=1 from child. buffer=0, so buffer=1.
          After children: buffer=1. Check: buffer+1 = 2 == K, so close it. Return 0.
        So DFS(3) returns 0.
        DFS(5): parent=2, child 6.
          DFS(6): parent=5, no children. m=0, K=2>1, return 1.
          Back to DFS(5): buffer=1. buffer+1=2==K, close, return 0.
        So DFS(5) returns 0.
        Back to DFS(2): children 3 and 5 both return 0. So m=0. K=2>1, so return 1.
      Back to DFS(1): S=1 from child 2. buffer=0, so buffer=1.
      After children: buffer=1. Check buffer+1=2==K, close, return 0.
      Root 1: after processing, buffer was set to 1 from child, then closed. So at root, effectively the open path from child was closed at root. This means vertex 1 and the path from child form a K=2 path. The child path is {2,3,4,5,6}? No, wait. Let's trace.
      DFS(2) returned 1, meaning the open path in {2}'s subtree going to parent is of size 1 (just vertex 2? But vertex 2 has children 3 and 5, which returned 0, meaning their subtrees are fully partitioned. So the only vertex in the open path is 2 itself. Return 1. Then at root 1, buffer=1 from child. buffer+1=2=K, close. So path is {2,1} of size 2.
      But what about vertices 3,4,5,6? They were in DFS(3) and DFS(5). DFS(3) had child 4 returning 1, buffer=1, closed: path {4,3}. DFS(5) had child 6 returning 1, buffer=1, closed: path {6,5}.
      So paths are: {1,2}, {3,4}, {5,6}. This matches sample 1! 

      So the algorithm works. Let me formalize:

      def dfs(u, parent):
          buffer = 0
          has_child_segment = False
          for v in adj[u]:
              if v == parent: continue
              S = dfs(v, u)
              if S == 0: continue
              has_child_segment = True
              if buffer == 0:
                  buffer = S
              else:
                  if buffer + S + 1 == K:
                      buffer = 0  # formed a K-path
                  else:
                      return -1  # fail
          if buffer == 0:
              if not has_child_segment:
                  # no segments from children
                  if K == 1:
                      return 0  # this vertex is a K=1 path
                  else:
                      return 1  # this vertex goes up as open path of size 1
              else:
                  # had segments, all paired and closed
                  return 0
          else:
              # buffer > 0, one open segment
              if buffer + 1 == K:
                  return 0  # closes at this node
              else:
                  return buffer + 1

      At the root, after calling dfs(root, 0), we need to check that the return value is 0 (or specifically that no open path remains). Actually, the root has no parent, so any open path going up from root is invalid (can't close). So we need dfs(root, 0) == 0, AND also we need to ensure that root itself is in a path. But the return value 0 from root means either:
        - Root was interior of paired paths (buffer reset during processing), so root is in paths, good.
        - Root had no child segments and K=1, root is a K=1 path, good.
        - Root had no child segments and K>1, then we returned 1, which is not 0, so check fails.
        - Root had a buffer that was closed (buffer+1==K), so returned 0, good.
        - Root had a buffer that is passed up: but there is no parent, so this is invalid. In our code, we return buffer+1 if buffer>0 and buffer+1 != K. This would be non-zero, so root check fails.

      So the condition is: if dfs(root, 0) == 0, then Yes, else No.

      But wait, is that sufficient? Let me check sample 2.
      Sample 2: N=3, K=2. Tree: 1-2, 2-3, 3-4, 2-5, 3-6.
      Degrees: 1:1, 2:3, 3:3, 4:1, 5:1, 6:1.
      Root at 1.
      DFS(1): child 2. 
        DFS(2): parent=1, children 3,5.
        DFS(3): parent=2, children 4,6.
          DFS(4): leaf, return 1.
          DFS(6): leaf, return 1.
          Back to DFS(3): process child 4: S=1, buffer=0 -> buffer=1.
          Process child 6: S=1, buffer=1. Try buffer+S+1=1+1+1=3 != K=2. Return -1 (fail).
      So dfs(1) will get a fail from child 2, or -1 propagates. Actually, return -1 from dfs(3). Then at dfs(2), child 3 returns -1. We need to handle this: if S == -1, propagate -1 (fail).
      So dfs(2) returns -1. dfs(1) returns -1. Root gets -1 != 0, so No. Correct!

      Another test: simple path of 4 vertices, N=2, K=2.
      Tree: 1-2-3-4.
      Root 1.
      DFS(1): child 2.
        DFS(2): parent=1, child 3.
          DFS(3): parent=2, child 4.
            DFS(4): leaf, K=2>1, return 1.
          Back to DFS(3): S=1, buffer=1. buffer+1=2=K, close, return 0.
        Back to DFS(2): child 3 returns 0. has_child_segment=False. K>1, so return 1.
      Back to DFS(1): S=1 from child. buffer=0 -> buffer=1.
      After: buffer=1, buffer+1=2=K, close, return 0.
      Root: 0, Yes. Paths: {1,2} and {3,4}. Correct.

      Another: path of 3 vertices, N=1, K=3.
      Tree: 1-2-3.
      Root 1.
      DFS(1): child 2.
        DFS(2): parent=1, child 3.
          DFS(3): leaf, K=3>1, return 1.
        Back to DFS(2): S=1, buffer=1. buffer+1=2 != K=3. Return buffer+1=2.
      Back to DFS(1): S=2 from child. buffer=0 -> buffer=2.
      After: buffer=2, buffer+1=3=K, close, return 0.
      Root: 0, Yes. Path: {1,2,3}. Correct.

      Another: star with center and 3 leaves, N=2, K=2. Vertices: 1-2, 1-3, 1-4. NK=4, N=2, K=2. Tree is star at 1.
      Root 1.
      DFS(1): children 2,3,4.
      DFS(2): leaf, return 1.
      DFS(3): leaf, return 1.
      DFS(4): leaf, return 1.
      Back to DFS(1):
        child 2: S=1, buffer=0 -> buffer=1.
        child 3: S=1, buffer=1. Check: 1+1+1=3 != 2. Fail, return -1.
      So No. Indeed, with 3 leaves, we can form one path {leaf, center} and one vertex left over. Can't form two paths of 2. Correct.

      What if N=1, K=4, path of 4: Yes. Star with 3 leaves, N=1, K=4? NK=4, N=1, K=4. Star at 1 with leaves 2,3,4. Can we form a path of 4? The tree has center degree 3. A path of 4 vertices uses 3 edges, but the tree edges are 1-2,1-3,1-4. Any path in this tree has at most 2 edges (leaf-center-leaf). So max path length is 2 vertices (if we allow leaf-center) or 3? Wait, a simple path in a star: we can go leaf1-center-leaf2, that's 3 vertices. To get 4 vertices, we need to traverse center multiple times, but simple path cannot revisit. So max simple path is 3 vertices (two leaves and center). So for K=4, impossible.
      Algorithm: Root 1.
      DFS(2): leaf, return 1 (since K=4>1).
      DFS(3): leaf, return 1.
      DFS(4): leaf, return 1.
      DFS(1): process children.
        child 2: S=1, buffer=1.
        child 3: S=1, buffer=1, check 1+1+1=3 != 4, fail. Return -1.
      So No. Correct.

      What about a tree that is a "caterpillar" that works. The algorithm seems correct.

      Time complexity: O(NK) for DFS, since each edge processed once. The buffer handling is O(1) per child. So O(NK).

      Implementation details:
        - Read N, K.
        - If K == 1: always Yes (since each vertex is a path of length 1). Actually, if K=1, then paths are single vertices, any partition works. The tree structure doesn't matter. Just print Yes.
        - Otherwise (K >= 2), build adjacency list for NK vertices.
        - Run DFS from root 1.
        - If result == 0: Yes, else No.
        - Need to handle the case where the tree is just a single vertex (NK=1). Then N=1, K=1, handled. Or N=1, K=1 only possibility since NK=1.
        - Also, if K >= 2, we need K-1 to be relevant. The algorithm uses K in comparisons.

      Edge case: what if during DFS, buffer + S + 1 > K? We return -1. What if buffer + S + 1 < K? We return -1. Only == K is good.
      What if a child returns a value S where S >= K? That shouldn't happen if the child is correct, but we should handle: if S >= K, fail (or if S==K, that means child tried to return a completed path up, which is wrong, should be 0). So in the child, we only return values < K.

      Recursion depth: NK up to 2e5, recursion might stack overflow in Python. We should either set recursion limit or use iterative DFS. Let's use recursion with sys.setrecursionlimit(4e5).

      Let me double-check the algorithm with one more example: a tree that is two paths of length 3 sharing an endpoint? N=2, K=3, NK=6. Suppose vertices: 1-2-3-4-5-6 in a line. That's a path of 6. Can we partition into two paths of 3? {1,2,3} and {4,5,6}. Yes.
      Root 1.
      DFS(1): child 2.
        DFS(2): parent=1, child 3.
          DFS(3): parent=2, child 4.
            DFS(4): parent=3, child 5.
              DFS(5): parent=4, child 6.
                DFS(6): leaf, K=3>1, return 1.
              Back to DFS(5): S=1, buffer=1. buffer+1=2 !=3, return 2.
            Back to DFS(4): S=2, buffer=0 -> buffer=2.
            After: buffer=2, buffer+1=3=K, close, return 0.
          Back to DFS(3): child 4 returns 0. has_child_segment=False, return 1.
        Back to DFS(2): child 3 returns 1. buffer=0 -> buffer=1.
        After: buffer=1, buffer+1=2 !=3, return 2.
      Back to DFS(1): S=2, buffer=0 -> buffer=2.
      After: buffer=2, buffer+1=3=K, close, return 0.
      Root: 0, Yes. Paths: {6,5,4} formed at node 4? Let's see: at node 4, child 5 returned 2 (open path {5,6} of size 2). Node 4 adds itself: size 3=K, closes. So path {4,5,6}. Then node 3 has child 4 returning 0, so node 3 returns 1. Node 2 receives 1, buffer=1, returns 2 (open {2,3}? Wait, node 3 returned 1, meaning the open path in {3}'s subtree is size 1 (just vertex 3? But vertex 3 had child 4 returning 0, so no open path from child. Node 3 has no child segments, so it returns 1 (itself going up). Then node 2 gets S=1 from child 3, buffer=1, but no other children, so returns buffer+1=2 (open path {2,3} of size 2). Then node 1 gets S=2 from child 2, buffer=2, returns 0 after checking buffer+1=3=K. So path {1,2,3}. Total {1,2,3} and {4,5,6}. Correct!

      Great, the algorithm works.

      So the plan is:
        1. If K == 1, print Yes and exit.
        2. Build graph.
        3. DFS with the buffer logic.
        4. Check root result is 0.

      Let's write the code.

      One subtlety: in the DFS, when we say "has_child_segment", we mean we processed at least one child that returned a non-zero value. If all children return 0, then has_child_segment is False. Then if buffer==0, we are in the case of no active children. For K>1, we return 1. For K==1, we return 0 (but we already handled K==1 separately). So for K>=2, we return 1.

      Also, if a child returns -1, we should immediately return -1.

      Code skeleton:
        import sys
        sys.setrecursionlimit(1 << 25)
        input = sys.stdin.readline

        N, K = map(int, input().split())
        if K == 1:
            print("Yes")
            return
        total = N * K
        adj = [[] for _ in range(total + 1)]
        for _ in range(total - 1):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        def dfs(u, p):
            buffer = 0
            has_active = False
            for v in adj[u]:
                if v == p: continue
                res = dfs(v, u)
                if res == -1:
                    return -1
                if res == 0:
                    continue
                has_active = True
                if buffer == 0:
                    buffer = res
                else:
                    if buffer + res + 1 == K:
                        buffer = 0
                    else:
                        return -1
            if buffer == 0:
                if not has_active:
                    return 1  # K >= 2 here
                else:
                    return 0
            else:
                if buffer + 1 == K:
                    return 0
                else:
                    return buffer + 1

        result = dfs(1, 0)
        if result == 0:
            print("Yes")
        else:
            print("No")

      Let me trace once more with a case where the root has degree > 1 and works. E.g., N=2, K=2, tree: 1-2, 1-3, 1-4, 4-5. Wait, 5 vertices, NK=5, not divisible by 2. Need NK even.
      Try: NK=4, N=2, K=2. Tree: 1-2, 1-3, 1-4. (Star, already shown No).
      Try: 1-2, 2-3, 2-4. Degrees: 1:1, 2:3, 3:1, 4:1. NK=4.
      Root 1.
      DFS(1): child 2.
        DFS(2): parent=1, children 3,4.
          DFS(3): leaf, return 1.
          DFS(4): leaf, return 1.
        Back to DFS(2): child 3: S=1, buffer=1. child 4: S=1, buffer=1, check 1+1+1=3 !=2, fail. Return -1.
      So No. Can we partition {1,2,3,4} into two paths of 2? Paths must be edges. Edges: (1,2), (2,3), (2,4). We need two disjoint edges? But they share vertex 2. So no. Correct.

      Try: 1-2, 2-3, 3-4, 4-5. Path of 5. N=1, K=5. Should be Yes.
      Root 1.
      DFS(1): child 2.
        DFS(2): child 3.
          DFS(3): child 4.
            DFS(4): child 5.
              DFS(5): leaf, return 1.
            DFS(4): S=1, buffer=1, return 2 (1+1=2 !=5).
          DFS(3): S=2, buffer=2, return 3.
        DFS(2): S=3, buffer=3, return 4.
      DFS(1): S=4, buffer=4, buffer+1=5=K, return 0. Yes.

      Try: 1-2, 2-3, 3-4, 4-5, 3-6. Degrees: 1:1, 2:2, 3:3, 4:2, 5:1, 6:1. NK=6, N=2, K=3.
      Can we do it? Paths of 3: maybe {1,2,3} and {4,5,6}? But 6 is connected to 3, not 5. The edges are 4-5 and 3-6. To make a path containing 4,5,6, we need 4-5 and 3-6, but 3 and 4 are connected. So path could be 6-3-4-5, but that's 4 vertices. Or 5-4-3-6 (4 vertices). For K=3, maybe {1,2,3} and {4,5}? No, K=3 needs 3 vertices. {6,3,4}? Then {1,2,5}? But 1-2 and 2-5, so {1,2,5} is a path. And {6,3,4} is a path. Check edges: 6-3 yes, 3-4 yes, 1-2 yes, 2-5 yes. Disjoint vertices: {1,2,5} and {3,4,6}. Yes!
      Algorithm:
      Root 1.
      DFS(1): child 2.
        DFS(2): parent=1, child 3.
          DFS(3): parent=2, children 4,6.
            DFS(4): child 5.
              DFS(5): leaf, return 1.
            DFS(4): S=1, buffer=1, return 2.
            DFS(6): leaf, return 1.
          Back to DFS(3): child 4: S=2, buffer=0 -> buffer=2.
          child 6: S=1, buffer=2. Check: 2+1+1=4 !=3. Fail. Return -1.
      So algorithm says No. But we found a valid decomposition! What's wrong?

      Ah, the decomposition {1,2,5} and {3,4,6} uses the path 1-2-5. But 2-5 is an edge? In the tree, edges are 1-2, 2-3, 3-4, 4-5, 3-6. Yes, 2-5 is not an edge! I misread. The edge 2-5 doesn't exist. The tree is a path 1-2-3-4-5 with a leaf 6 on 3. So edges: 1-2, 2-3, 3-4, 4-5, 3-6. No 2-5 edge. So {1,2,5} is not a path (1-2 and 2-5 would be needed, but 2-5 is not an edge). So indeed, can we partition?
      We need two paths of 3. Vertices: 1,2,3,4,5,6. Edges: 1-2, 2-3, 3-4, 4-5, 3-6.
      Possible paths of length 3 (3 vertices): 
        - 1-2-3 (uses 1,2,3)
        - 2-3-4 (uses 2,3,4)
        - 3-4-5 (uses 3,4,5)
        - 6-3-4 (uses 6,3,4)
        - etc.
      We need two disjoint paths covering all 6 vertices.
      If we take {1,2,3}, remaining {4,5,6}. Edges among them: 4-5. 6 is isolated. So {4,5,6} not a path.
      If we take {2,3,4}, remaining {1,5,6}. Edges: 1 is only connected to 2 (used), so isolated. 6 connected to 3 (used), isolated. 5 connected to 4 (used), isolated. No.
      If we take {3,4,5}, remaining {1,2,6}. Edges: 1-2, 2-3(used). So 1-2 is a path, and 6 isolated. Not covered.
      If we take {6,3,2}, remaining {1,4,5}. Edges: 1-2(used), so 1 isolated. 4-5. Not covered.
      It seems impossible. So No is correct. The algorithm is right.

      Another: a tree where center has degree 4, N=2, K=2. Tree: star with center 1 and leaves 2,3,4,5. NK=5, odd, not valid for K=2 (need even). So no.
      Try NK=6, N=2, K=2. Star with 5 leaves? Then center degree 5, leaves 5. NK=6. Can we partition into two paths of 2? Each path is an edge. We need two disjoint edges. But in a star, all edges share the center. So no two disjoint edges. So No.
      Algorithm: Root at center 1.
      DFS(1): children all return 1.
      Process first: buffer=1.
      Second: S=1, check 1+1+1=3 !=2, fail. Correct.

      So the algorithm is correct. I'll implement it.

      One more check: what if N=0? Constraint says N>=1, so fine.

      What about large K? E.g., N=1, K=200000. Tree is a path of 200000. Should be Yes. The algorithm will propagate a single buffer of increasing size, finally reaching K at the root? Wait, the root is at one end. Let's see: root 1, child 2, ..., child 200000.
      DFS at leaves: return 1.
      At node 200000: buffer=1, return 2.
      At 199999: receives 2, buffer=2, return 3.
      ...
      At node 2: receives 199999, buffer=199999, return 200000? But K=200000. At node 2: buffer+1=200000=K, so close, return 0.
      At root 1: child 2 returns 0. has_active=False, return 1 (since K>1).
      Then root has buffer=1 (from itself? Wait, root processes children. Child returns 0, so no active. Then buffer=0, has_active=False, return 1. So root returns 1. But the root has no parent, so returning 1 means there's an open path of size 1 going up, but there's no up. So the final result is 1 != 0, so No!
      But the path of 200000 vertices should be decomposable into one path of K=200000. What went wrong?

      Ah, I see. In my algorithm, when the root has no active children (all children subtrees are fully partitioned or return 0), and buffer==0, I return 1. But for the root, if it returns 1, that means the root itself is an open path of size 1 going to parent (which doesn't exist). This is invalid.

      But in the path of 200000 rooted at 1, the child 2 returned 0, meaning the subtree rooted at 2 is fully partitioned into K-paths. But the subtree rooted at 2 is the entire rest of the tree (vertices 2..200000). If DFS(2) returns 0, that means the subtree {2..200000} is fully partitioned into K-paths. But the only K-path covering it is the path 2-3-...-200000 of size 199999, not 200000. Wait, K=200000, and the subtree has 199999 vertices. It cannot form a complete K=200000 path within itself; it must include the root.

      So DFS(2) should not return 0. It should return 199999 (the open path of size 199999 going up to parent 1). Let's trace the algorithm:
      At node 200000: leaf, K=200000>1, return 1.
      Node 199999: child 200000 returns 1. buffer=0 -> buffer=1. After: buffer=1, buffer+1=2 != K. Return buffer+1=2.
      ...
      Node 2: receives 199999 from child 3. buffer=0 -> buffer=199999. After: buffer=199999, buffer+1=200000=K. Close, return 0.
      So DFS(2) returns 0. This means the subtree at 2 is fully partitioned. But it has 199999 vertices, and the only way to partition 199999 into paths of K=200000 is impossible. The algorithm incorrectly returned 0.

      The error is at node 2: the buffer was 199999, and we checked if buffer+1 == K. 199999+1=200000=K, so we closed it. This means we formed a K-path of size 200000 within the subtree of 2. But the subtree of 2 only has 199999 vertices! We can't have a path of 200000 vertices in a subtree of 199999 vertices. The algorithm is wrong!

      I see the flaw. The condition buffer+1 == K means the open path from the child (size buffer) plus the current node u makes K. But the current node u is included in the path, and the path is buffer+1 vertices total. If buffer+1 == K, the path is complete and includes u. But u is the current node, which is in the subtree of u's parent. However, the child segment of size buffer is in the child's subtree, which is part of u's subtree. So the path is within u's subtree, which is correct. But the total number of vertices in the path is buffer+1. The subtree rooted at u has size 1 + sum of children's subtrees. The child's segment uses buffer vertices, plus u makes buffer+1. If this equals K, and K is the total path size, then we are saying that within the subtree of u, there is a complete K-path that includes u and the child's segment. This is valid only if the subtree is large enough. The subtree size is at least buffer+1 (since it contains u and the child's segment). The child returned buffer, meaning the child's subtree has at least buffer vertices (specifically, the open path has buffer vertices, and there might be other closed paths in the child's subtree). So the total subtree size of u is >= 1 + buffer. If we close a K-path here, we use buffer+1 vertices. The remaining vertices in u's subtree (if any) are handled by other children or left over. But in the case of a path of length 200000, when we are at node 2 (second vertex), the child is the rest of the path. The child returns 199999, meaning the open path in child's subtree is of size 199999. This uses 199999 vertices. Node 2 adds 1, total 200000 = K. So we close it. This means the path is vertices 2..200000 plus... wait, the open path of size 199999 from child 3 is the path 3..200000. Adding node 2 gives 2..200000, which is 199999 vertices? No: child is node 3. The open path from node 3 is size 199999, meaning vertices 3,4,...,200000 (that's 199998 vertices)? Let's count: vertices 3 to 200000 inclusive is 200000 - 3 + 1 = 199998 vertices. So size 199998. But the algorithm said buffer=199999. Where did 199999 come from?

      Let's trace properly:
      - Node 200000: leaf. Return 1. (size 1)
      - Node 199999: child is 200000. Receives 1. buffer=1. buffer+1=2. Return 2. (size 2: {199999, 200000})
      - Node 199998: receives 2. buffer=2. Return 3. (size 3)
      - ...
      - Node k: receives (200000 - k). buffer = 200000 - k. Return 200000 - k + 1 = 200001 - k.
      - Node 2: receives from node 3. Node 3 is child. Node 3 has subtree 3..200000. The open path from node 3 is of size 200000 - 3 = 199997? Let's compute: for node i, the return value is the size of the open path from that node to the end. For node 3, the end is 200000. The path is 3-4-...-200000. Number of vertices: 200000 - 3 + 1 = 199998. So DFS(3) should return 199998. Then at node 2, we receive 199998. buffer = 199998. Check buffer+1 = 199999 != 200000. So we do not close. We return buffer+1 = 199999.
      - Then at root 1: receives 199999 from child 2. buffer = 199999. Check buffer+1 = 200000 = K. Close, return 0.
      - Root 1: after processing, buffer was set to 199999 then closed. So the open path from child 2 (size 199999) plus root 1 makes 200000 = K. So path is 1-2-...-200000. Correct.

      So the algorithm works for the long path. The key is that the return value at node i is the size of the path from i to the far end. For node 2, the path is 2-3-...-200000, which is 199999 vertices. Return 199999. Then root receives 199999, adds 1, makes 200000. Good.

      My earlier trace was wrong; I said node 2 receives 199999, which is correct.

      So the algorithm is correct.

      Final check: what if the tree is not a simple path? The algorithm handles general trees.

      Implementation: I'll write the DFS recursively. Need to handle the case where a child returns -1 (propagate failure). Also, if any return value is >= K, it's an error (shouldn't happen if logic is correct, but we can check). Actually, in the correct execution, return values are always in [0, K-1]. 0 means no open path. Positive means open path size < K.

      Also, at the root, after DFS, we check if result == 0. If result > 0, it means there's an open path of that size that couldn't close, so No. If result == -1, No.

      One more edge case: what if N*K = 1? Then N=1, K=1. Handled by K==1 case. If we don't handle K==1, and K>=2, but total=1, impossible since N>=1, K>=2 means total>=2. So safe.

      Code: standard.

      Let me write the solution.

      Actually, there's a subtlety: when we have buffer and a new child segment S, we need to check buffer + S + 1 == K. But what if buffer + S + 1 < K? We return -1. What if >K? Also -1. Only ==K is good.

      But wait, is it possible that we should combine more than two segments at a node? For example, three segments meeting at u, and we want to connect two of them to form a path, and the third goes up. That's what our sequential buffer does: it pairs them one by one. The first sets buffer, the second pairs with buffer to form a K-path, the third sets new buffer, etc. This works if the pairing is possible. But what if the segments have sizes such that the first and second don't sum to K-1, but the first and third do, and second is left? Since we process in order, we might fail incorrectly if the matching is not in order. However, the constraint is that the sum of any pair must be K-1. So if we have segments of sizes s1, s2, s3, and s1+s2 = K-1, but we process s1 and s2 in order, it works. If the order is different, say s1=1, s2=3, s3=2 with K=5. Then K-1=4. Pairs summing to 4: (1,3) and (2) left. If we process 1, then 3: buffer=1, S=3, 1+3+1=5=K, good. Then buffer=0, next S=2, buffer=2, return 3. If we process 1, then 2: buffer=1, S=2, 1+2+1=4 !=5, fail. So the order matters! We need to match segments into pairs summing to K-1. The sequential left-to-right pairing only works if the segments are ordered such that the first and second pair, third and fourth pair, etc. But in a tree, the order of children is arbitrary. We need to ensure that there exists a pairing.

      Ah! This is a crucial flaw. The algorithm assumes that we can pair them in the order received, but we might need to sort or match them.

      In the case of the path of 4 (N=2,K=2), at the center (node 2 in sample 1? No, sample 1 is different). Let's find a case where order matters.
      Consider a node u with three children, each returning a segment of size 1, and K=3. Then K-1=2. We need pairs summing to 2. With three segments of size 1, we have three 1s. We need to pair two of them (sum 2) and one goes up. So we need to leave one 1, and pair the other two. But in sequential processing: first child sets buffer=1. Second child: S=1, buffer=1, 1+1+1=3=K? Wait, 1+1+1=3, and K=3, so it forms a K-path! That's correct. Third child: S=1, buffer=0 (since we closed). Now buffer=0, has_active=True, S=1 sets buffer=1. After: buffer=1, buffer+1=2 !=3, return 2. So the open path going up is size 2. Then at parent, this size 2 plus parent makes 3=K? 2+1=3, yes. So it works. The sequential processing happened to work.

      Another case: segments of sizes 2, 2, 1, with K=4. K-1=3. We need pairs summing to 3. Possible pairs: (2,1). So we pair one 2 with the 1, and the other 2 goes up. Sequential: first 2 sets buffer=2. Second 2: S=2, buffer=2, check 2+2+1=5 !=4, fail. But we shouldn't pair them; we should pair the first 2 with the 1, and leave the second 2. So sequential fails, but a valid matching exists.

      Can this situation occur in a tree? Yes, if a node has children with subtree structures that yield those segment sizes. For example, a node with three children: one child subtree yields an open path of size 2, another yields size 2, another yields size 1. K=4.
      Is this realizable? Let's construct: root at u, children v1, v2, v3.
      v1: a path of 2 vertices going up to u? v1 has a child w1. w1 is leaf. Then DFS(w1) returns 1. DFS(v1) receives 1, buffer=1, return 2. So v1 returns 2.
      Similarly v2 returns 2.
      v3: leaf, returns 1.
      Then at u: children return 2,2,1. K=4. K-1=3. Valid pairing: (2,1) and one 2 goes up. So we can form a path: v1-subtree(2) + u + v3-subtree(1) = 4 vertices. And v2-subtree(2) + u (going up) is an open path of size 3. Then at parent of u, it receives 3, buffer=3, buffer+1=4=K, closes. So overall, the tree can be partitioned. But the sequential algorithm fails.

      So we need a proper matching at each node: we have a multiset of segment sizes from children. We need to pair them up such that each pair sums to K-1. If the number of segments is odd, one is left and goes up (with size s+1). If even, all are paired, none go up.

      To check if such a pairing exists efficiently: we can use a greedy approach if we sort the sizes. Specifically, to pair numbers to sum to K-1, we can use two pointers: sort the list. Use two pointers, one from smallest, one from largest. If smallest + largest == K-1, pair them, move both. If < K-1, fail. If > K-1, fail (since we want exact sum, and if smallest + largest > K-1, and the largest is the max, then no pair can sum to K-1 with the largest, since all other are smaller, so sum would be <= smallest+largest > K-1, so too big. Wait, if largest is L, and we pair with smallest s, if s+L > K-1, then since s is the smallest, s' + L >= s + L > K-1 for any s' >= s. So L cannot be paired. Fail. So the two-pointer method works for checking if all can be paired to sum to K-1.

      But if we have an odd number and want to leave one out, we need to check if we can leave exactly one such that the rest pair to K-1. That is equivalent to: for each candidate to leave, check if the remaining can be paired. But that's O(m^2). However, there's a better way: if we sort the list, we can check if the list can be partitioned into pairs summing to K-1 with possibly one element left. The condition is that the list is a "complementary" sequence.

      Actually, a known fact: for a multiset of positive integers, it can be paired to sum to S iff the largest is <= S and the smallest is >= 0, and after sorting, we can greedily match. But with one left out, it's trickier.

      Alternative approach: use a frequency map or process with a counter. Since K can be large, but the segment sizes are at most K-1. We can use a dictionary to count frequencies. For each possible value v, it needs to be paired with S = K-1-v. So we can check if for all v, the count of v and count of S-v match up, possibly with one unpaired.

      Specifically, we want to know if we can pair the multiset into pairs summing to K-1, with at most one element left unpaired. This is like checking if the multiset is a subset of pairs of (v, K-1-v), with at most one exception.

      We can do this: for each v, the number of v's should equal the number of (K-1-v)'s, except possibly for one value v0 where count(v0) = count(K-1-v0) + 1 (the extra one is the one left up), and for v = K-1-v0, the count is one less. But this is only if K-1-v0 != v0. If K-1 is even, say K-1=2m, then v0=m pairs with itself. The condition is different.

      Simpler: we can use a greedy algorithm with a multiset. Process children, collect sizes in a list. Sort the list. Then use two pointers i=0, j=len-1. While i < j: if a[i] + a[j] != K-1: fail. i++, j--. After loop, if i==j (odd number left), that one is the open segment. Return its size+1. If i>j (even, all paired), return 0 (or check K). But we need to handle the case where the pairing doesn't work with this specific greedy, but another pairing might work. Is the two-pointer greedy optimal for this matching problem?

      For the problem of pairing to sum to S, with distinct elements or not, the two-pointer method on sorted array works if we want to check if a perfect matching exists. Because if the smallest a[0] and largest a[n-1] sum to > S, then no element can pair with a[n-1] (since all are >= a[0], so sum >= a[0]+a[n-1] > S). Similarly if sum < S, then a[0] cannot pair with anything (since a[n-1] is the largest, sum <= a[0]+a[n-1] < S). So we must have a[0]+a[n-1] == S. Then we pair them and recurse on the rest. So yes, the two-pointer method is necessary and sufficient for existence of perfect matching to sum to S.

      For the case with one left out: we want to know if we can remove one element such that the rest can be perfectly paired to sum to K-1. We can try each element as the candidate to remove, but that's O(m^2). However, we can observe: if a matching with one left exists, then after removing the left element, the rest must be pairable. We can check if the multiset minus the candidate works. But we can also just try to pair greedily, and if we fail, maybe a different pairing works? No, the two-pointer is the only way to pair if we fix the order. But if we leave out a different element, the pairing of the rest might require a different matching. The two-pointer on the full list (with odd length) will fail at the last step because we have one left. We need to see if that one can be the "left out" one.

      Actually, the condition is: there exists an element x such that the multiset without x can be partitioned into pairs summing to K-1. We can find x by looking at the sorted list. Since the two-pointer matching is unique (if it exists), we can check.

      Alternative method: use a hash map. For each size s in the list, we want to pair it with K-1-s. We can count frequencies. Let cnt[s] be the count. For each s from 1 to K-2 (since sizes are in [1, K-1]), we need cnt[s] == cnt[K-1-s], except possibly for one value. But if K-1 is even, say K-1=2m, then the value m pairs with itself. We need cnt[m] to be even, or if odd, we can have one m left over. So the condition is: for all s, let required_pair = K-1-s. If s < required_pair, then cnt[s] must equal cnt[required_pair]. If s == required_pair, then cnt[s] must be even (or if odd, one can be left over). After processing all, the number of "excess" elements (where cnt[s] is odd for s = required_pair) should be at most 1, and the unpaired element must be valid (i.e., we can have at most one s with cnt[s] odd, or something).

      More precisely, the number of elements left unpaired should be 0 or 1. We can compute the minimum number of unpaired elements by matching. The condition for being able to pair all but at most one is: the multiset can be paired with at most one exception. This is equivalent to: for every s, the count of s must equal the count of K-1-s, except possibly for one s where it exceeds by 1, and for s = K-1-s, the count must be even or exactly one odd.

      Implementation: collect the list of S_v from children. We want to know if we can pair them to sum to K-1, leaving at most one.
      We can use a Counter. For each s in the list, we check if there is an available K-1-s. But we need to do this carefully.

      A simpler way: since the sum of all S_v plus the number of pairs * (K-1) plus the unpaired one = total sum. But that's not directly helpful.

      Another approach: at each node, instead of returning a single buffer, we can return a multiset, but that's heavy.

      Actually, the standard solution to this problem (I recall now) is exactly the buffer approach with the two-pointer matching at each node. Many implementations use a multiset or sort the children's return values. Since the degree of a node can be up to NK, but sum of degrees is O(NK), sorting at each node might be expensive overall if a high-degree node has many children. But sum over nodes of d(v) log d(v) could be O(NK log NK) in worst case (star graph: one node with degree NK, sort takes O(NK log NK), others constant). NK <= 2e5, so O(NK log NK) is fine.

      So we can do: at node u, collect all S_v > 0 into a list. Sort the list. Then try to pair smallest with largest. Use two pointers i=0, j=len-1. While i < j: if a[i] + a[j] != K-1: return -1. i++, j--. After loop, if i == j: one left, call it x. Then return x+1 (if x+1 < K, else if x+1==K, return 0). If i > j: all paired, return 0.

      But wait, if i == j, the one left is a[i]. We return a[i]+1. However, is it guaranteed that a[i]+1 is the correct open size? Yes, because that one segment plus u will go up. And the size is a[i] (from child) + 1 (u) = a[i]+1.

      But we must also check that a[i]+1 <= K. If a[i]+1 == K, we should close it and return 0. If a[i]+1 > K, impossible (shouldn't happen if children's values are < K, but check).

      Also, if the list is empty (no children with S>0), then for K>=2, we return 1 (u goes up alone). For K==1, handled separately.

      This two-pointer method is correct because for a set of numbers to be pairable to sum to S, the necessary and sufficient condition is that when sorted, a[0]+a[n-1]=S, a[1]+a[n-2]=S, etc. This is a well-known fact.

      So the algorithm is:
        DFS(u, p):
          segments = []
          for v in adj[u]:
            if v == p: continue
            s = DFS(v, u)
            if s == -1: return -1
            if s > 0: segments.append(s)
          if not segments:
            if K == 1: return 0
            else: return 1
          segments.sort()
          i, j = 0, len(segments)-1
          while i < j:
            if segments[i] + segments[j] != K-1:
              return -1
            i += 1
            j -= 1
          if i == j:  # one left
            left = segments[i]
            if left + 1 == K:
              return 0
            elif left + 1 < K:
              return left + 1
            else:
              return -1
          else:  # i > j, all paired
            return 0

      Then at root, if result == 0, Yes, else No.

      Let's test with the problematic case: node with segments [2,2,1], K=4. K-1=3. Sorted: [1,2,2]. i=0, j=2: 1+2=3=K-1, good. i=1, j=1: i==j, left=2. left+1=3 < K=4, return 3. So open size 3. At parent, receives 3, buffer... actually in this algorithm, we return the open size directly, and at parent, it's just one of the segments. The parent will collect segments and do the same. So it works.

      Test with [1,1,1], K=3. Sorted: [1,1,1]. i=0,j=2: 1+1=2=K-1, good. i=1,j=1: left=1. left+1=2 != K=3, return 2. Open size 2. At parent, this is one segment of size 2. If parent has K=3, and this is the only segment, then at parent: segments=[2]. i=0,j=0, left=2. left+1=3=K, return 0. So path closes at parent. Good.

      Test with [1,1], K=2. K-1=1. Sorted: [1,1]. i=0,j=1: 1+1=2 !=1, fail. Return -1. Correct, as we saw.

      Test with [2,2], K=4. K-1=3. 2+2=4 !=3, fail. Return -1. But can we pair them? No, because we need sum 3. So fail is correct.

      Test with [3,1], K=5. K-1=4. 3+1=4, good. i=0,j=1, after loop i=1,j=0, i>j, return 0. Good.

      So the algorithm is correct.

      Now, we need to be careful with the return value type and propagation. If any DFS returns -1, we propagate -1.

      Also, at the root, we need to check that the return value is exactly 0. If it is -1 or positive, No.

      One more case: what if the root has segments and they all pair, but the root itself is not in any path? For example, root with two children both returning 1, K=3. K-1=2. Sorted [1,1]. 1+1=2=K-1, good. i=0,j=1, after i=1,j=0, i>j, return 0. This means the two segments paired through root to form a K-path. The path is child1 + root + child2 = 1+1+1=3=K. Root is interior of this path. So it's valid. Return 0 from root means success.

      What if root has segments [1], K=2. Sorted [1]. i=0,j=0, left=1. left+1=2=K, return 0. This means the child segment plus root makes K=2. Path is child + root. Root is endpoint. Valid.

      What if root has segments [1], K=3. left=1, left+1=2 <3, return 2. But root has no parent, so returning 2 means an open path of size 2 that can't close. So final check: result != 0, so No. Indeed, a path of 3 needs 3 vertices, but we only have a segment of 2 at root. Invalid.

      So the algorithm is solid.

      Now, complexity: O(NK log D) where D is max degree, but sum of d log d is fine.

      Let's code it.

      Pseudocode:
        def solve():
            import sys
            sys.setrecursionlimit(1 << 25)
            input = sys.stdin.readline
            N, K = map(int, input().split())
            if K == 1:
                print("Yes")
                return
            total = N * K
            adj = [[] for _ in range(total + 1)]
            for _ in range(total - 1):
                u, v = map(int, input().split())
                adj[u].append(v)
                adj[v].append(u)
            sys.setrecursionlimit(max(1000000, total * 2))
            def dfs(u, p):
                segs = []
                for v in adj[u]:
                    if v == p: continue
                    s = dfs(v, u)
                    if s == -1: return -1
                    if s > 0:
                        segs.append(s)
                if not segs:
                    return 1  # K >= 2
                segs.sort()
                i, j = 0, len(segs) - 1
                while i < j:
                    if segs[i] + segs[j] != K - 1:
                        return -1
                    i += 1
                    j -= 1
                if i == j:
                    left = segs[i]
                    val = left + 1
                    if val == K:
                        return 0
                    elif val < K:
                        return val
                    else:
                        return -1
                else:
                    return 0
            res = dfs(1, 0)
            print("Yes" if res == 0 else "No")

      Edge case: total=1, N=1, K=1. Handled.
      Edge case: N=0? Not possible.
      Edge case: K >= total? But N>=1, K>=1, NK = total. If N=1, K=total. Tree is a path or any tree? Actually, with N=1, we need one path of K=total vertices. A path exists if the tree is a path. But the tree can be any tree? The problem asks to decompose into N paths of length K. If N=1, we need one path containing all vertices. This is possible only if the tree itself is a path (i.e., has exactly two leaves and all others degree 2, or total=1). Our algorithm should handle this.
      For N=1, K=total. The tree is a general tree. We need to traverse all vertices in one path. This is possible iff the tree is a path. Our algorithm will check this.
      Example: star with 3 leaves, total=4, N=1, K=4. Should be No.
      Root at center 1. Children 2,3,4.
      DFS(2): leaf, segs=[], return 1.
      Similarly 3,4 return 1.
      At root: segs=[1,1,1]. K=4, K-1=3. Sorted [1,1,1]. i=0,j=2: 1+1=2 !=3, fail. Return -1. So No. Correct.
      Example: path of 4, N=1, K=4. Should be Yes.
      Root 1. DFS(1) child 2.
      ... as before, returns 0. Yes.

      So the algorithm is correct.

      One final check: the recursion depth. NK up to 2e5. A path of 2e5 vertices. Recursion depth 2e5. Python default recursion limit is 1000. We need to set it higher. I'll set sys.setrecursionlimit(1 << 25) or 500000.

      Also, we need to handle the case where the tree might not be connected? The problem says it's a tree, so connected.

      Implementation: straightforward.

      Let me write the final code.</mm:think>### PLAN
We need to determine if a tree of NK vertices can be partitioned into N vertex-disjoint simple paths, each containing exactly K vertices. This is a tree decomposition problem. A known necessary and sufficient condition is that the tree can be recursively processed via DFS: at each node, the "open" path segments coming from children must be matched in pairs summing to K-1 (forming a complete K-path through the node), with at most one segment left unpaired to extend upward to the parent. If a node has no active children, it forms an open segment of size 1 going up (since K≥2). At the root, no open segment may remain. The algorithm is:
1. If K=1, always output "Yes" (each vertex is a path).
2. Run a DFS. For each node, collect the open segment sizes returned by children. Sort them and use a two-pointer method to pair the smallest with the largest, requiring each pair to sum to K-1. If an odd segment remains, it extends upward (size+1). If any check fails, return failure.
3. After DFS on the root, if no open segment remains, output "Yes", else "No".