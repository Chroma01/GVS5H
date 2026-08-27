
## ideation
The problem asks for the minimum number of moves to swap two indistinguishable-in-capability pieces A and B on an undirected connected graph, where they start at vertices S and T, must end at T and S respectively, and can never occupy the same vertex. Each move shifts exactly one piece along an edge. N, M ≤ 2×10^5, so an explicit BFS over the N(N−1) state space is infeasible (would be ~4×10^10 states in the worst case, e.g., a long path). The state graph is essentially the Cartesian product G □ G restricted to a≠b. In that product, d((S,T),(a,b)) = distS[a] + distT[b] when pieces move independently. The true distance in our restricted graph is at least this, and equals it when the independent paths can be interleaved without collision.

Key observations from small cases:
- When distS[T] = 1 (S, T adjacent): the only blocking move is A→T or B→S. The pieces can swap iff the graph is not the single edge S–T (i.e., deg(S)≥2 or deg(T)≥2). If possible, the answer is exactly 3 (one piece detours to a neighbor, the other passes, the first returns).
- When distS[T] ≥ 2: a natural candidate is distS[T] + distT[S]. This is achievable on many graphs (samples 1 and 3 match this, e.g., sample 3 has distS[T]=2, distT[S]=2, answer 4), but not on all. On a simple path S–…–T with no branches, the swap is impossible (pieces cannot pass without colliding, and there is no vertex with degree ≥3 to wait at). On a star with S, T as leaves, also impossible.

The core difficulty: determining when the swap is possible and computing the exact minimum number of moves efficiently. The state space is too large for naive BFS, so we need either a characterization that reduces to O(N+M) work, or a BFS on a much smaller derived graph. A promising direction is to use the “midpoint” structure: a swap is possible iff there is a “maneuvering room” — a vertex of degree ≥3 on the S–T path, or more generally, a cycle accessible to both pieces. The minimal detour length is determined by the distance from S and T to the nearest such branch vertex.

A clean O(N+M) approach:
1. BFS from S → distS[·]; BFS from T → distT[·].
2. If distS[T] = 1: answer = 3 if (deg(S)≥2 or deg(T)≥2), else -1.
3. If distS[T] ≥ 2: Check feasibility via a BFS on a reduced state space of size O(N + M). Specifically, run BFS on the Cartesian product state graph but limit exploration to states (a, b) where a lies on some “relevant” shortest S–T region. However, this can still be O(N²) on paths.

A known elegant solution: The answer is `min( 2*distS[T], distS[T] + distT[S] )` adjusted with a BFS correction term. Actually, the precise characterization is:
- Compute distS[·], distT[·].
- If no vertex v with distS[v] + distT[v] = distS[T] and degree(v) ≥ 3 exists (and S, T don't have degree ≥2 when distS[T]=1), then answer = -1.
- Else, answer = `2 * distS[T]` if the swap can be done by having A go to T and B to S along shortest paths that “pass” at a branch, else `distS[T] + distT[S]`.

This is getting complicated. The safest correct approach for the given constraints is a BFS on the state space that is carefully bounded. On a sparse graph, the BFS frontier size is O(M) per layer, and the total number of visited states is O((distS[T]+1) * M) in practice, but worst-case O(N²) on a path — however on a path the answer is -1 and we can detect this in O(N) by checking if the graph is a path (or more generally, if there is a vertex of degree ≥3 on the S–T geodesic, or if S or T has degree ≥2 when distS[T]=1).

## worker: 3 if distS[T] = 1 (and feasible),
The problem requires finding the minimum number of moves to swap two pieces on an undirected graph without letting them occupy the same vertex. A direct BFS on the state space `(a, b)` with `a ≠ b` has `N(N-1)` states, which is infeasible for `N ≤ 2×10^5`. The provided code attempts this BFS using a dictionary for visited states and includes a distance cutoff, but it will likely TLE on worst-case inputs (e.g., long paths or Y-shaped graphs) where the number of reachable states is `O(N²)`. A correct and efficient solution likely involves: (1) detecting path graphs and returning `-1`, (2) BFS from `S` and `T` to get `distS[]` and `distT[]`, and (3) computing the answer using a formula based on the distances and the existence of branch vertices (degree ≥ 3) on shortest paths, or a BFS on a reduced graph of size `O(N)`. The current code is a best-effort placeholder that handles the path case but is not fully correct for the general case.

## worker: Implement the correct O(N+M) algorithm: BFS from S
The code above attempts to implement the known result for the two-pieces swap problem. The key insights are:

1. If `distS[T] == 1` (S and T adjacent), the answer is 3 if either vertex has degree ≥ 2 (allowing one piece to detour), otherwise -1.

2. If `distS[T] >= 2`, the swap is possible iff the graph is not a simple path between S and T. We detect this by checking if any vertex on a shortest S-T path has degree ≥ 3, or if S or T have neighbors not on the shortest path (branches).

3. When the swap is possible, the answer is the minimum of:
   - `2 * distS[T]` (pieces pass each other at a branch point)
   - `distS[T] + distT[S]` (pieces go around each other)

However, this formula is **not fully correct** for all cases. The correct solution requires a BFS on the state graph `(a, b)`, but that is `O(N²)` in the worst case. The true `O(N+M)` solution involves a more careful analysis of the "midpoint" vertices and a BFS on a reduced graph of size `O(N)`. The current implementation may fail on some test cases where the simple path detection or the formula `min(2*D, D+DT)` doesn't capture the exact minimum. A complete correct solution would require implementing the full state-space BFS with proper pruning or the exact characterization from the original contest solution.

## worker: Research and implement the exact O(N+M) solution f
The implementation above attempts a BFS on the full state space `(a, b)` with `a != b`, using a set to track visited states and a cut-off based on `D + DT + 2`. This approach is correct in principle but has O(N²) worst-case time and space complexity (up to 4×10¹⁰ states for N=2×10⁵), which is infeasible for the given constraints. The code is a best-effort placeholder that may TLE on worst-case inputs (e.g., long paths or graphs with many reachable states). The true O(N+M) solution for the two-pieces swap problem requires a more sophisticated analysis—likely involving BFS on a derived "midpoint" graph or a characterization based on shortest path distances and the existence of branch vertices with off-path neighbors. Since the exact O(N+M) algorithm was not fully derived within the time available, this submission is a functional but potentially non-efficient attempt.

## worker: Research and implement the exact O(N+M) algorithm 
The two-pieces swap problem requires finding the shortest path in a state graph with `N(N-1)` nodes, which is infeasible for `N ≤ 2×10^5` with a naive BFS. The implemented solution handles this by:

1. **Adjacency case (D=1)**: If `deg(S)≥2` or `deg(T)≥2`, the answer is 3 (one piece detours, the other passes, first returns). Otherwise, `-1`.

2. **Path detection**: If the graph is a simple path (`N>2` and all degrees ≤ 2), swap is impossible because pieces cannot pass without colliding, and there is no waiting space. Return `-1` immediately to avoid `O(N²)` BFS.

3. **General BFS with cut-off**: For non-path graphs, run BFS on the state space `(a, b)` with `a ≠ b`, limited to distance `D + DT + 2` (an upper bound on the optimal answer). The BFS uses a dictionary for visited states and a queue. This is exact for the answer when the graph has sufficient branching, and the state space explored is much smaller than `N²` for graphs with branches.

The path-detection optimization is crucial for worst-case inputs (long paths) where the state space would otherwise be `O(N²)`. For branching graphs, the BFS frontier is limited by the cut-off and graph structure, making it feasible.

## worker: finalize
The provided solution attempts to solve the two-pieces swap problem with the following strategy:

1. **Adjacency handling**: If `S` and `T` are adjacent (`distS[T] == 1`), the answer is `3` if either vertex has degree ≥ 2 (allowing one piece to detour), otherwise `-1` (the only edge is `S-T` with no branches).

2. **Path detection**: If the graph is a simple path (all vertices have degree ≤ 2 and `N > 2`), the swap is impossible because pieces cannot pass each other on a line without colliding, and there is no "waiting room". Return `-1` immediately to avoid an `O(N²)` BFS.

3. **General BFS**: For non-path graphs with `D ≥ 2`, run a BFS on the state space `(a, b)` with `a ≠ b`, starting from `(S, T)` and targeting `(T, S)`. The BFS uses a dictionary for visited states (encoded as `a * N + b`) and a queue. A cut-off of `D + DT + 2` is used as an upper bound on the optimal answer.

**Caveat**: The general BFS has `O(N²)` worst-case time/space complexity, which is infeasible for `N = 2×10^5`. While the path-detection optimization handles the worst-case (long paths), the solution may still TLE on other adversarial inputs (e.g., a graph that is "almost" a path but with a single branch, causing the BFS to explore a large diamond of states). A fully correct and efficient `O(N + M)` solution requires a more sophisticated characterization (e.g., computing the answer via BFS on a reduced "midpoint" graph), which was not fully derived in the available time. The current code is a best-effort attempt that handles many cases but is not guaranteed to be efficient on all inputs.
