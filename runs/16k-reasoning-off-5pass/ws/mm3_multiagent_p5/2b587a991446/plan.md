We model the state as the ordered pair of positions (a, b) of the two pieces, with a ≠ b. From a state (a, b), valid moves are: move A to a neighbor `na` of a such that `na != b`, or move B to a neighbor `nb` of b such that `nb != a`. Goal: start state (S, T) → (T, S). This is a shortest path problem on a graph of up to N*(N-1) states, but the graph is huge.

Key insight: The relative ordering of A and B matters. We can separate the problem into two cases:
- Reach a state where A = T, B = S directly (this is the goal).
- If we ever reach a state where A = T but B ≠ S, or A ≠ T but B = S, we can still potentially finish by a short sequence.

A standard reduction: Let `dist[v]` = distance from S to v. The minimum number of moves for A to reach T alone is `dist[T]`, but B is in the way when A arrives at vertices equal to B. We can think of moving B out of the way.

Better approach: BFS on the state space is too large. We can compute the answer as:
1. `d1 =` minimum moves to reach (T, S) directly via BFS where A moves toward T and B stays (or moves only when forced). But B can also move.

Actually, the standard solution for this problem (AtCoder ABC 196 E? No, this is ABC 199 D? Let me think... This is "Two Pieces" type problem). 

The known solution: The answer is the minimum of three quantities:
- `dist1[S][T] + dist2[T][S]` style: but we need careful BFS.

Let me reconsider. State space BFS with N*(N-1) ≈ 4e10 is too much. But there's a smarter approach.

Observation: We can decompose. Let's define:
- `d_A(v)` = shortest distance from S to v in the original graph.
- `d_B(v)` = shortest distance from T to v.

Case 1: A moves from S to T along a shortest path, while B moves from T to S along a (possibly different) shortest path, never colliding. The collision-free condition: when A is at vertex x on its path and B is at vertex y on its path, we need x ≠ y at the same time step, OR we interleave.

Actually, the standard trick: Consider the state where pieces have swapped. The minimum moves to swap two tokens on a graph where they can't occupy the same vertex is a known problem.

For an unweighted graph, we can compute the answer as:
- If there's a path from S to T not using certain edges, etc.

Let me think differently. The state space can be reduced by noting that we can "simulate" BFS on the state graph by considering pairs. But N up to 2e5, so we need O(N) or O(M) solution.

Standard approach for "two pieces swap" problem:
1. BFS from S alone to get `distS[v]`.
2. BFS from T alone to get `distT[v]`.
3. The answer is either:
   - `distS[T] + distT[S]` if there's no conflict, but this isn't quite right because pieces can meet.

Wait, the pieces start at S and T (different), need to reach T and S (different). The minimum moves for A to go S→T is `distS[T]`, and B to go T→S is `distT[S]`. But they can't be on same vertex at same time.

The classic solution (this is ABC 244 F? No... this is likely "Two Pieces" from some contest): Use BFS on state space but with a clever bound, OR compute as:
- answer = distS[T] + distT[S] if they can do it without meeting, else some other path.

Actually, the known solution: The answer equals:
`2 * distS[T]` if S and T are adjacent? No.

Let me recall: This is AtCoder ABC 282 F? No. It's "Two Pieces" — I think it's ABC 244? Let me think of the structure.

I recall a problem: "Two Pieces" where you compute distances and the answer is min over certain paths. The state (a, b) with a ≠ b BFS can be bounded: a is within `distS[T] + 1` of S or within `distS[T]` of T? 

Standard solution:
- Compute `dS[v]` = distance S to v.
- Compute `dT[v]` = distance T to v.
- BFS on state graph (a, b) but we only need states where `dS[a] + dT[b]` is small? No, that's not bounded.

Alternative: BFS from start state (S, T) on the state graph, but limit: a's position is within distance dS[T] from S, and b's position is within distance dT[S] from T? That gives at most dS[T] * dT[S] states which could be large.

Hmm, but actually for this problem, the known solution is:
1. BFS from S to get `distS[]`.
2. BFS from T to get `distT[]`.
3. The answer is `distS[T] + distT[S]`, but only if there's a way to schedule without collision. Otherwise, we need to detour.

The full solution: The answer is `distS[T] + distT[S]` if and only if we can find "compatible" paths. Otherwise, we need to consider the state graph.

Let me reconsider the state space size. N ≤ 2e5, M ≤ 2e5. BFS on full state space is infeasible. But we can do BFS on a reduced state space.

Key insight: In the state (a, b), consider the "difference" — we can use the graph's structure. Actually, one approach: do BFS on the state graph, but represent states where the two pieces are "close" or "far". 

I think the intended solution for this specific problem (looks like AtCoder ABC 282 F or similar) is:

Multi-source BFS approach. But let me think of the swap problem more carefully.

The answer is: compute distances from S and from T. Then the answer equals:
- If there exists a vertex v on a shortest S-T path such that v has degree ≥ 2 (or specific structure), use that.

I think I'm overcomplicating. Let me just do BFS on the state graph but with a trick: only explore states (a, b) where the pair is "reachable" efficiently. Since M ≤ 2e5, the state graph has up to ~4e10 states but we only visit a subset.

Actually, a better bound: In BFS from (S, T), the state (a, b) is reached in k steps. Then a is reachable from S in ≤ k steps, and b is reachable from T in ≤ k steps. So a is in the "k-ball" around S, b in "k-ball" around T. For k = answer ≤ 2*N or so, this could still be large.

Wait, for a path graph, the answer could be 2*(N-1) - 1 or similar, and the number of reachable states at distance k is O(k), so total O(N^2)? Hmm.

Let me look at this from a different angle. The state graph has N*(N-1) nodes. BFS visiting all is too much. But perhaps the graph structure (sparse) means we can use meet-in-the-middle or another approach.

Actually, I recall now: this is ABC 282 F? No. Let me just think of the algorithm.

The answer to "swap two tokens" on an unweighted graph with the constraint they never share a vertex:
- Token A goes S→T, token B goes T→S.
- Equivalent: A traces path S→T, B traces path T→S, and they execute moves in some order, never simultaneously on same vertex.

This is equivalent to: find two paths P_A (S to T) and P_B (T to S) and an interleaving of their edges such that at each step, the two current vertices differ.

A known result: minimum swaps = `dS[T] + dT[S]` if there's a "good" interleaving, else more.

Specifically, the minimum is achieved by one of:
1. `dS[T] + dT[S]`: A goes S→T along shortest, B goes T→S along shortest, interleaved so they don't collide. This works if for some shortest S-T path and T-S path, we can interleave. But the T-S path reversed is an S-T path. So both are shortest S-T paths? No, B's path T→S is a shortest T-S path, which reversed is a shortest S-T path.

Hmm, this is getting complex. Let me think of the BFS on state space with a practical bound.

Given the constraints (N, M ≤ 2e5), a BFS that visits O(N*M) or O(N^2) states in worst case might be too slow, but O(N + M) per BFS layer could work if total states is manageable.

Actually, for this problem I think the intended solution is BFS on the state graph, and the total number of visited states is bounded. Why? Because in state (a, b), the edge from a to b in the state graph: from (a, b), we go to (na, b) for na ∈ N(a) \ {b} or (a, nb) for nb ∈ N(b) \ {a}. The state graph is a subgraph of the tensor/composition.

Total edges in state graph: for each edge (u,v) in original, we have transitions. Each state (a, b) has up to deg(a) + deg(b) neighbors. The number of states is N*(N-1). The number of edges in state graph: for each (a, b), deg(a) + deg(b) edges, so sum = Σ_{(a,b)} (deg(a) + deg(b)) = (N-1) * Σ deg(a) + (N-1) * Σ deg(b) = 2(N-1)*2M = 4M(N-1), which is huge.

So BFS on full state graph is infeasible.

OK here's the real insight for this problem (I'm now fairly sure this is a known problem). The minimum number of moves to swap is:
- If we can find a vertex v ≠ S, T on some shortest path, with certain properties.

Let me think about it as: we want min over states of (dist from (S,T) to (T,S) in state graph). 

I recall a cleaner formulation: The answer equals `distS[T] + distT[S]`, UNLESS every shortest path from S to T and T to S forces a collision, in which case the answer is larger.

Specifically, consider the set of "midpoint" vertices. Actually, let me try a different approach.

Algorithm: 
1. BFS from S: `dS[v]` = distance S to v.
2. BFS from T: `dT[v]` = distance T to v.
3. Let `L = dS[T]`. The "level" of vertex v from S is `dS[v]`.
4. A going S→T along a shortest path takes L steps, ending at T at step L.
5. B going T→S along a shortest path takes `dT[S]` steps, ending at S at step `dT[S]`.

The answer is at least `max(dS[T], dT[S])` and we can try various interleavings.

Actually, I think for this problem the answer is simply `dS[T] + dT[S]`, because we can always interleave: move A one step, move B one step, alternating, as long as A and B don't collide. They start at S and T (different), and we want to ensure that at each step, the partial positions differ.

Hmm, but consider a graph that's a path 1-2-3-4, S=1, T=4. dS[T]=3, dT[S]=3, sum=6. Can we swap in 6 moves? A: 1→2→3→4, B: 4→3→2→1. Interleave: A to 2, B to 3, A to 3? No, B is at 3. So A to 2, B to 3, B to 2? No, A at 2. So this doesn't work trivially.

We need: after move sequence, A at 4, B at 1. Try: A:1→2, B:4→3, A:2→3? B is at 3. A:2→1? Then A back. B:3→2, A:2→3, B:2→1, A:3→4. That's 6 moves and it works! A trace: 1,2,2,2,3,3,4. B trace: 4,4,3,2,2,1,1. Check collisions: (2,4),(2,3),(2,2)? No! At step 3 (after A moves to 2 the second time? Let me recount).

Move 1: A 1→2, B at 4. State (2,4). ✓
Move 2: B 4→3, A at 2. State (2,3). ✓
Move 3: A 2→3? B at 3. Invalid.
Move 3: A 2→1. State (1,3). 
Move 4: B 3→2. State (1,2).
Move 5: A 1→2? B at 2. Invalid. A stays? No, we must move or... we choose to move. A 1→2 invalid. 
Hmm, A can only go to neighbors of 1, which is 2. B at 2. So A can't move. Dead end.

So 6 doesn't work for the path 1-2-3-4. The answer must be larger? But dS[T]+dT[S] = 6, and we showed it fails. So the answer > 6.

Let me think for path 1-2-3-4, S=1, T=4. The answer: 
A needs to go 1→4 (3 steps), B needs to go 4→1 (3 steps). They share vertices {1,2,3,4}. 
Move 1: A 1→2. (2,4)
Move 2: A 2→3. (3,4)
Move 3: A 3→4. (4,4)? B at 4. Invalid.
So A can't reach 4 while B is there. B must move first or A must detour.
Move 1: B 4→3. (1,3)
Move 2: B 3→2. (1,2)
Move 3: B 2→1? A at 1. Invalid. B 2→3? Back.
Hmm, B is stuck at 2 or must go back.
Move 1: A 1→2, B 4→3. (2,3)
Move 2: A 2→1? Then (1,3). B 3→2. (1,2). A 1→2? B at 2. 
This is tricky. Let me try:
(1,4) → A→2 → (2,4) → B→3 → (2,3) → B→2? A at 2. Invalid. A→3 → (3,3)? B at 3. Invalid. A→1 → (1,3) → B→2 → (1,2) → A→? A neighbors: 2 (B there). Dead end.

(1,4) → B→3 → (1,3) → A→2 → (2,3) → B→2? A there. B→4 → (2,4) → A→3 → (3,4) → B→3? A there. 
(1,4) → B→3 → (1,3) → B→2 → (1,2) → A can't go to 2. A→? only neighbor 2. Dead.
(1,4) → A→2 → (2,4) → A→3 → (3,4) → B→3? A there. B→? neighbors of 4: 3 (A there). Dead.
(1,4) → A→2 → (2,4) → B→3 → (2,3) → A→1 → (1,3) → B→2 → (1,2) → ... dead.

It seems impossible on a path of 4 vertices? But the problem says connected graph. Path 1-2-3-4 with S=1, T=4: is it possible? The pieces must swap. A goes 1→4, B goes 4→1. They must cross. The path has only one route. They have to pass each other, but can't be on same vertex. In a path, the middle vertices must be traversed by both, so they must "pass" — but they can't share a vertex, and edges are undirected. To pass on a path, one must wait at an endpoint. But endpoints are the targets.

Actually on a path 1-2-3-4, A at 1, B at 4. A needs to reach 4, B needs to reach 1. They both need to traverse edges 1-2, 2-3, 3-4. A traverses them forward, B traverses them backward. They can't be on the same vertex. Consider vertex 2: A passes through 2, B passes through 2. They can't both be at 2. Similarly for 3. So at some point, one piece is at 2 and the other is past 2, or vice versa. But vertex 1 and 4 are the only "parking" spots, and those are the destinations. So this should be impossible! 

Wait, but the problem allows any number of moves and any order. Can A go 1→2→1→2→3→... to let B pass? 
(1,4) → A→2 → (2,4) → B→3 → (2,3) → A→1 → (1,3) → B→2 → (1,2) → A→? A can go to 2 (B there). Dead.
(1,4) → B→3 → (1,3) → A→2 → (2,3) → B→4 → (2,4) → A→3 → (3,4) → B→3? A there. B stuck at 4 (only neighbor 3, A there).
So yes, impossible on path 1-2-3-4! The answer is -1.

But wait, dS[T] + dT[S] = 3+3 = 6, and we might think the answer is finite, but it's actually -1. Hmm, but the problem might have examples where it's impossible. Let me check sample 2: N=2, M=1, S=1, T=2. Graph: 1-2. A at 1, B at 2. A→2? B at 2. B→1? A at 1. They can't move without colliding. So -1. Yes, matches.

So the answer can be -1, and the formula isn't simply dS[T]+dT[S].

OK so the problem is genuinely hard. The state space BFS with N*(N-1) states is too large, but we need some BFS.

I think the solution involves BFS on the state graph but with a crucial optimization. Let me think...

For the state graph BFS, from state (a, b), we transition to (na, b) or (a, nb). This is exactly the "strong product" minus diagonal. BFS on this is standard, but size is N^2.

However! We can use the fact that the graph is sparse (M ≤ 2e5) to do the BFS efficiently. In BFS, from state (a, b), we enumerate neighbors. The number of edges in state graph is huge, but we can enumerate them on-the-fly: for each (a, b) in the BFS frontier, neighbors of (a, b) are {na} × {b} ∪ {a} × {nb} where na ∈ N(a)\{b}, nb ∈ N(b)\{a}. The issue is the BFS queue size.

The BFS will visit some subset of states. For a graph with M edges, how many states are visited? In the worst case (e.g., a long path), the BFS might visit O(N^2) states, which is too many.

But wait, on a long path, as we showed, the answer might be -1, and BFS would explore everything to confirm. O(N^2) = 4e10, too slow.

So we need a smarter approach. Let me think of the problem structure.

New idea: The problem has a nice structure. The two pieces move on the graph. This is equivalent to a single "walker" on the graph G × G minus diagonal. But we want shortest path from (S,T) to (T,S).

Observation: (T, S) is reachable from (S, T) iff the graph is not "bipartite-separated" in some sense. Specifically, if S and T are in different connected components after removing some structure... hmm.

Actually, for the path 1-2-3-4 with S=1, T=4, we showed it's impossible. Why? Because the two pieces are confined to the path and must cross, but can't share a vertex, and there are no "branches" to wait. With branches (higher degree), pieces can wait at branch points.

So the problem is solvable iff there's enough "room" (branches) for the pieces to maneuver.

This suggests: compute the answer using the structure of the graph. Specifically, we can think of the state space, but prune by distance.

Here's a key insight for the algorithm: BFS from (S, T) on the state graph, but represent visited states compactly. We can use the fact that the state graph is the strong product. But still N^2.

Alternative: For each vertex v, maintain which other vertices u have (v, u) been visited. But that's still N^2.

Wait, I think the intended solution is to realize that the BFS state space is actually manageable because we can bound it. Let me reconsider.

Hmm, let me look at this from a known-problem perspective. This is "Two Pieces" from JOI or AtCoder. I believe the solution is:

1. BFS from S to get dS[].
2. BFS from T to get dT[].
3. The answer is min over "strategies". A strategy is characterized by a sequence of moves.

Actually, I found a different angle. The state (a, b) with the swap constraint can be related to a single BFS on a modified graph. 

Consider the line graph or the "state graph" but use the following: the answer is `2 * dS[T]` if S and T are "compatible" in some way, or involves a BFS on a smaller graph.

Let me think about small cases and try to derive the answer formula.

For the path 1-2-3-4, S=1, T=4: impossible, answer -1.
For a path 1-2-3, S=1, T=3: A at 1, B at 3. dS[T]=2. 
(1,3) → A→2 → (2,3) → B→2? A there. B→? only neighbor 2. Dead. 
(1,3) → B→2 → (1,2) → A→2? B there. Dead.
So impossible for path 1-2-3 too? Let me double-check. N=3, M=2, edges 1-2, 2-3. S=1, T=3. A at 1, B at 3. Any move: A→2 or B→2. After A→2: (2,3), then B→2 invalid (A there), B has no other neighbor. So B is stuck. A→3? A at 2, neighbor 3, but B at 3. Invalid. So from (2,3), A can go to 1 or 3(invalid), so A→1, state (1,3) back. B from (2,3) can go to 3(invalid, A at 2, wait B at 3, neighbors of B(3) is {2}, and 2≠A=2, so B can go to 2! But A is at 2. So B→2 invalid because A is at 2. B's only neighbor is 2, and A is at 2, so B can't move. A from (2,3): neighbors {1,3}, 3 has B, so A→1. State (1,3). 

So on path 1-2-3 with S=1, T=3, it's impossible. Makes sense — the graph is a tree with branching factor ≤ 2, and S, T are at distance 2 with only one intermediate.

Path 1-2-3-4-5, S=1, T=5: probably impossible too (no branches).

What if there's a branch? E.g., 1-2-3, 2-4, S=1, T=3. Then vertex 2 is a branch. (1,3) → B→2? neighbors of 3: {2}, so B→2, state (1,2). A from (1,2): neighbors {2}, 2 has B, so A can't move. Dead. 
(1,3) → A→2 → (2,3). B→? neighbors of 3: {2}, A at 2, invalid. B stuck. A→? neighbors of 2: {1,3,4}, 3 has B, so A→1 or A→4.
A→4: (4,3). B→2: (4,2). A→2? B at 2. A→? neighbors of 4: {2}, 2 has B. Dead.
A→1: (1,3) back.
Hmm, seems hard. Let me try harder.
(1,3) → A→2 → (2,3) → A→4 → (4,3) → B→2 → (4,2) → A→? neighbors of 4: {2}, B at 2. Dead. 
(4,2) → B→? neighbors of 2: {1,3,4}, 4 has A. B→1 or B→3.
B→1: (4,1). A→2: (2,1). B→2? A at 2. B→? neighbors of 1: {2}, A at 2. Dead.
B→3: (4,3) back.
This is frustrating. Let me try:
(1,3) → A→2 → (2,3) → A→4 → (4,3) → B→2 → (4,2) → B→3 → (4,3) back.
(4,2) → B→1 → (4,1) → A→2 → (2,1) → B→2? A there. B→? neighbors of 1: {2}. Dead.
(2,1) → A→? neighbors: {1,3,4}. A→4: (4,1) back. A→3: (3,1). B→2: (3,2). A→2? B there. A→? neighbors of 3: {2}, B at 2. Dead.

I think with S=1, T=3 in this graph (1-2-3, 2-4), it might be impossible too. But intuitively, with the branch at 2, maybe not. Let me think... A needs to go 1→3, B 3→1. They both pass through 2. With branch 4 attached to 2, A can go 1→2→4, then B goes 3→2, then A goes 4→2? B there. A goes 4→... only neighbor 2. 

Wait, I need A to end at 3 and B at 1. A's path: 1→2→3 (length 2). B's path: 3→2→1 (length 2). With the constraint, they both need vertex 2. If A goes to 4 first: 1→2→4, then B 3→2, but A needs to get to 3. From 4, A can only go to 2 (B there). Dead. Unless A goes 1→2→4→2, but 2 has B.

Hmm, I think for S=1, T=3 in this graph, it might be impossible. But let me check: (1,3) → A→2 → (2,3) → B→? B stuck. So after one A move, B is stuck. Unless we move B first: (1,3) → B→2 → (1,2) → A stuck. So impossible. 

So the graph needs more structure. What if we have a cycle? 1-2-3-1 (triangle), S=1, T=2. dS[T]=1. (1,2) → A→3 → (3,2) → B→3? A there. B→1 → (3,1) → A→2 → (2,1) → B→2? A there. B→? neighbors of 1: {2,3}, A at 2. B→3: (2,3) → A→1: (1,3) → B→2: (1,2) back. 

(1,2) → B→3 → (1,3) → A→2 → (2,3) → B→1 → (2,1) → A→3 → (3,1) → B→2 → (3,2) → A→1 → (1,2) back. 

Hmm, going in circles. Let me try to reach (2,1):
(1,2) → A→3 → (3,2) → A→1 → (1,2) back.
(1,2) → B→3 → (1,3) → B→2? A at 1, wait B at 3 going to 2. (1,2) back.
(1,2) → A→3 → (3,2) → B→1 → (3,1) → A→2 → (2,1). Yes! 

So (1,2) → A→3 → (3,2) → B→1 → (3,1) → A→2. Now A at 2, B at 1. That's (2,1), the goal! 3 moves.

So triangle with S=1, T=2: answer 3. dS[T]=1, dT[S]=1, sum=2, but answer is 3 > 2. So dS[T]+dT[S] is a lower bound but not tight.

OK so the answer is not simply dS[T]+dT[S]. We genuinely need to solve the state space BFS or find a formula.

For the triangle, state space has 3*2=6 states, and BFS finds 3. For larger graphs, state space is too big.

I think I need to look up or re-derive the algorithm. Given the constraints, the algorithm must be polynomial in N+M.

Key insight: The state space BFS can be bounded. Specifically, in BFS from (S, T), the state (a, b) is visited only if `dS[a] + dT[b]` is small, OR if we detour. But actually, the BFS could visit states far from S and T.

Wait, here's an important observation: the BFS on the state graph from (S,T) to (T,S) is symmetric: the graph is vertex-transitive in some sense? No.

Let me think about the structure of the state graph. The state (a, b) corresponds to the two pieces. The goal is to swap. This is equivalent to: one piece (say B) stays still, and A moves around B? No, B also moves.

Alternative formulation: Consider the "relative position". But since they can't occupy the same vertex, this is tricky.

I think the solution is the following BFS with a bound:
- BFS from (S, T) on the state graph.
- But we observe that in the BFS, the state (a, b) is reached, and then we can "symmetrize": also BFS from (T, S), and meet in the middle.
- Meet in the middle: BFS from both ends up to depth D. The state space explored is the union of two balls of radius D. If the two BFS balls meet, we found the path. The size of each ball: number of states within distance D. 

In the worst case, D = answer/2 ≈ N, and the ball has O(N^2) states. Still too big.

Hmm. Let me think about what makes the state space large. In a long path, the ball of radius D has O(D^2) states (since a is within D of S, b within D of T, and they must differ). For N=2e5, D=1e5, O(1e10) states. Too big.

So meet-in-the-middle doesn't directly help unless the graph structure limits the ball size.

Wait, I think the crucial insight is: the answer is either small (like O(N)) and we can compute it via a clever BFS, or it's -1, and we can detect -1 efficiently.

When is the answer -1? When the two pieces can never swap. As we saw, on a path, it's -1. More generally, the pieces can swap iff... hmm.

Let me reconsider the problem. I think this is a known problem and the solution is:
1. BFS from S: dS[].
2. BFS from T: dT[].
3. If dS[T] == -1 (disconnected, but problem says connected so not), or...
4. The answer is computed via BFS on the state graph, but with the key observation that the state graph BFS is equivalent to BFS on a graph of size O(N + M) or we use a trick.

New idea: The state (a, b) with a ≠ b. Consider the "swap" as moving both pieces simultaneously. The constraint is a ≠ b at all times. This is like a pebble motion problem. 

The minimum number of moves to swap two pebbles on a graph (where one move = one pebble to adjacent vertex, pebbles can't collide) is a known problem. For an unweighted graph, it's polynomial but might be complex.

Given the contest nature, there's likely a clean solution. Let me guess: 

The answer is `2 * dS[T]` if there's a "detour" available, else... hmm.

Let me try the triangle example: dS[T]=1, answer=3. 2*dS[T]=2 ≠ 3.
Path 1-2-3-4, S=1, T=4: dS[T]=3, answer=-1.

What about a graph where S=1, T=2, and 1-2, 1-3, 2-4, 3-4? (4-cycle). 
(1,2) → ? A→3: (3,2) → B→4: (3,4) → A→2: (2,4) → B→1: (2,1) → A→? goal (2,1) but goal is (T,S)=(2,1). Yes! 4 moves. 
Can we do better? (1,2) → B→4: (1,4) → A→3: (3,4) → B→1: (3,1) → A→2: (2,1). 4 moves.
(1,2) → A→3: (3,2) → A→4? neighbors of 3: {1,2,4}, 2 has B. A→4: (4,2) → B→4? A there. B→1: (4,1) → A→3: (3,1) → B→2: (3,2) back. Hmm.
(1,2) → A→3 → (3,2) → B→1 → (3,1) → A→4 → (4,1) → B→2 → (4,2) → A→3 → (3,2)... not reaching (2,1).
(1,2) → A→3 → (3,2) → B→1 → (3,1) → A→2 → (2,1). 3 moves! Check: (1,2)→A to 3→(3,2)→B to 1→(3,1)→A to 2→(2,1). Valid! 3 moves.
But dS[T]=1, so 2*dS[T]=2, and 3 moves. Hmm, 3 = 2*1 + 1 = 2*dS[T] + 1? 

Triangle gave 3, dS[T]=1. 4-cycle gave 3, dS[T]=1. Both have answer 3 when dS[T]=1 and answer exists.

For 4-cycle S=1, T=3 (diagonal): dS[T]=2. 
(1,3) → A→2 → (2,3) → B→4 → (2,4) → A→1 → (1,4) → B→3 → (1,3) back. 
(1,3) → A→2 → (2,3) → B→2? A there. B→4: (2,4) → A→1: (1,4) → A→3? neighbors of 1: {2,3}, 3 has B at 3? B at 4. A→3: (3,4) → B→1: (3,1) → A→2: (2,1) → B→3: (2,3) back. 
(1,3) → B→4 → (1,4) → A→2 → (2,4) → B→3 → (2,3) → A→1 → (1,3) back.
(1,3) → B→4 → (1,4) → A→2 → (2,4) → B→1 → (2,1) → A→3 → (3,1) → B→2 → (3,2) → A→4 → (4,2) → B→3 → (4,3) → A→1 → (1,3)... 
This is going in circles. Let me try to reach (3,1):
(1,3) → A→2 → (2,3) → A→1 → (1,3) back.
(1,3) → B→4 → (1,4) → B→3? A at 1. B→? neighbors of 4: {2,3}, 3 is free (A at 1), so B→3: (1,3) back.
Hmm, B from (1,4) can go to 2 or 3. 3→(1,3). 2→(1,2). 
(1,4) → B→2 → (1,2) → A→3 → (3,2) → B→1 → (3,1). 4 moves to reach (3,1)! Check:
Move 1: A 1→? neighbors 2,3. A→2. (2,3). Wait, goal is (3,1), start (1,3). Let me redo.
Start (1,3).
Move 1: B 3→4. State (1,4).
Move 2: B 4→2. State (1,2).
Move 3: A 1→3. State (3,2).
Move 4: B 2→1. State (3,1). 
Valid? (1,4): A=1, B=4 ✓. (1,2): A=1, B=2 ✓. (3,2): A=3, B=2 ✓. (3,1): A=3, B=1 ✓. Yes, 4 moves.
So 4-cycle S=1, T=3, answer=4. dS[T]=2. 

Can we do it in fewer? dS[T]+dT[S]=2+2=4. So 4=dS[T]+dT[S].

For 4-cycle S=1, T=2, dS[T]=1, dT[S]=1, sum=2, but answer=3 > 2. So when dS[T]=1 (adjacent), the answer is 3 if possible.

Hmm, interesting. So:
- dS[T] = 1: answer is 3 (if possible).
- dS[T] ≥ 2: answer might be dS[T] + dT[S] or more.

For the path 1-2-3-4, S=1, T=4, dS[T]=3, but answer=-1 (impossible). So we need a condition for possibility.

I think the condition for possibility is: the graph is not a "path" between S and T with no branches? More precisely, the two pieces can swap iff there's a cycle or enough connectivity.

A known condition: two pebbles can be swapped on a connected graph iff the graph is not a tree where S and T are... hmm, even on a tree, if there's a branch, maybe they can swap.

Wait, on a tree, can two pebbles always swap if there's a branch? Let's see: path 1-2-3-4 with extra leaf 5 connected to 2. S=1, T=4. A at 1, B at 4. A→2: (2,4). B→3: (2,3). A→5: (5,3). B→2: (5,2). A→? neighbors of 5: {2}, B at 2. A stuck. A→2? B there. 
(5,3) → B→2 → (5,2) → A→? stuck as above.
(2,3) → A→5 → (5,3) → B→2 → (5,2) → B→3 → (5,3) back.
(2,3) → A→1 → (1,3) → B→2 → (1,2) → A→? stuck.
Hmm, seems hard. Let me try:
(1,4) → A→2 → (2,4) → A→5 → (5,4) → B→3 → (5,3) → A→2 → (2,3) → B→2? A there. B→4 → (2,4) → A→5 → ... 

(1,4) → A→2 → (2,4) → B→3 → (2,3) → A→1 → (1,3) → B→2 → (1,2) → A→? neighbors of 1: {2}, B at 2. Dead.
(1,4) → B→3 → (1,3) → A→2 → (2,3) → B→4 → (2,4) → A→5 → (5,4) → B→3 → (5,3) → A→2 → (2,3) → B→2? A there.

I think on a tree, if S and T are not adjacent, and the tree is "thin" (long path), it might be impossible. The condition for swap on a tree: I recall that on a tree, two pieces can be swapped iff there's a vertex of degree ≥ 3 on the path between S and T, or S and T are adjacent with a branch. 

Actually, the condition is: the swap is possible iff the tree is not "S-T path with no branches" where S and T are the only leaves of interest. More precisely, on a tree, swap possible iff there's a vertex with degree ≥ 3 whose removal separates S and T in a way that... 

Hmm, for general graphs, the condition is more complex. But I think the problem expects a BFS-based solution.

Let me reconsider the BFS size. For the state graph BFS, the number of visited states: in the worst case (a graph like a long path), the BFS might visit many states. But actually, on a long path, the answer is -1, and BFS would need to visit all reachable states to confirm. That could be O(N^2).

But wait, on a long path from S=1 to T=N, the state (a, b) with a,b ∈ {1,...,N}, a≠b. The state graph restricted to the path: from (a,b), we can go to (a±1, b) or (a, b±1), with constraint a≠b. This is a 2D grid. BFS from (1, N) to (N, 1) on this grid. The grid has O(N^2) cells, and BFS visits them all? No, the BFS finds the shortest path which is O(N), but the BFS explores a "diamond" of states. The number of states at distance k from (1, N) is O(k) for k ≤ N, and the total states visited is O(N^2) in the worst case (a diamond of radius N). For N=2e5, O(N^2) is too big.

So BFS on state graph is too slow for worst case. We need a different approach.

Here's the key realization (I think I've got it now): 

We can reduce the problem by considering that the BFS on the state graph is equivalent to BFS on a "line graph" or we can use the distance from S and T to prune.

Specifically, a state (a, b) is only "interesting" if it's on some shortest path or near it. But formally:

The answer is min of:
1. `dS[T] + dT[S]`: this corresponds to both moving along shortest paths. But they might collide. The actual answer is `dS[T] + dT[S]` if there exist shortest S-T path and T-S path that can be interleaved without collision. The interleaving is possible iff... hmm.

Actually, the condition for `dS[T] + dT[S]` to be achievable: we need to interleave a shortest S→T path and a shortest T→S path. The T→S path reversed is an S→T path. So we need two (possibly same) shortest S→T paths, say P (for A) and Q (for B, traversed T→S), and an interleaving of their edges such that at no point are A and B on the same vertex.

The interleaving is a sequence of edges, each labeled A or B, forming a walk. This is complex.

I think the correct and clean solution is:

**The answer equals `2 * dS[T]` if and only if there exists a vertex v with dS[v] = floor(dS[T]/2) or similar, with degree ≥ 3... no.**

Let me just go with the state-space BFS but with a crucial optimization. Since the graph is sparse, the BFS can be implemented efficiently if we don't materialize the state graph.

Actually, I recall now: for this problem (it's AtCoder ABC 244 F? No...), the solution is to do BFS on the state graph, but the state space is O(N * dS[T]) or O(N * dT[S]) because we only explore states (a, b) where dS[a] and dT[b] satisfy some bound. Specifically, in any shortest swap sequence, a is always within dS[T] + something of S? No.

Hmm, let me think about the BFS from (S, T) and bound the "a-coordinate". In k steps, A is at some vertex a. Since A started at S, a is at distance ≤ k from S, so dS[a] ≤ k. Similarly dT[b] ≤ k. So at step k, a is in the k-ball around S (size O(min(k^d, N)) and b in k-ball around T. For k up to the answer (≤ 2N), the total states could be O(N^2) in the worst case.

But wait, for a graph with M=2e5 edges, the k-ball around S has at most min(N, 1 + M*... ) vertices. For k=1, it's deg(S)+1. For larger k, it grows. In a path, the k-ball around S has O(k) vertices. So for k=O(N), O(N^2) total states. 

For M=2e5 and N=2e5, the worst case is a path, and O(N^2) states. This is the bottleneck.

But! On a path, the answer is -1, and we want to detect this quickly without O(N^2) BFS.

So the algorithm must exploit the graph structure to either compute the answer efficiently or detect impossibility.

I believe the solution is:

The state (a, b) BFS can be bounded because the answer (if finite) is at most O(N + something), but more importantly, we can use the fact that the "midpoint" states are few.

Actually, here's a thought: the BFS on the state graph is equivalent to BFS on the graph G with a certain "potential". We can use Dijkstra (but unweighted, so BFS) with a state representation.

Given the time, let me just implement the BFS on the state graph with the understanding that it might be too slow for worst case, but hoping the problem expects it. But N=2e5, N^2 is 4e10, definitely too slow.

Wait, I think I've been wrong. Let me reconsider the BFS on the state graph size. 

In BFS, from state (a, b), neighbors are (na, b) for na ∈ N(a)\{b} and (a, nb) for nb ∈ N(b)\{a}. The BFS visits states in layers. The state (a, b) is visited at distance d(a,b) from (S,T). 

Claim: d(a,b) = dS[a] + dT[b] if a and b don't interact, or more if they do. But in the state graph BFS, d(a,b) is the shortest path length in the state graph, which accounts for interactions.

Now, the key: for any state (a, b), d(a,b) ≥ |dS[a] - dT[b]| and d(a,b) ≥ something. But importantly, d(a,b) could be as large as dS[a] + dT[b] (if they avoid each other) or larger (if they need to detour).

The BFS on the state graph has N*(N-1) nodes. The BFS finds the shortest path from (S,T) to (T,S). The length of this path is the answer. 

The BFS can be implemented as standard BFS on a graph with N*(N-1) nodes, but we need to avoid O(N^2) memory and time.

**Crucial insight**: The state graph BFS can be performed by BFS on the original graph with "two walkers". The state is (a, b). We can run BFS, and the visited set has at most... well, in the worst case, O(N^2). 

But! For this problem, I claim the BFS is actually efficient because we can prune: a state (a, b) is only reachable in ≤ dS[a] + dT[b] + C steps for some constant C, and the BFS layers are thin? No, in a path, layers are fat (O(k) states).

I'm stuck. Let me just look at the problem from the answer's perspective and guess the formula.

Given the samples:
Sample 1: N=4, edges: 2-4, 1-4, 3-4, 2-3. So graph: 4 connected to 1,2,3; 2-3. S=3, T=4. dS[T]=1 (3-4). Answer=3.
Sample 3: N=5, edges: 1-2, 2-3, 1-5, 2-4, 1-3, 2-5. S=3, T=5. dS[5]: 3→2→5, length 2. Or 3→1→5, length 2. dS[T]=2. Answer=4.

For sample 3, dS[T]=2, dT[S]=2, sum=4. Answer=4. So dS[T]+dT[S] works here.

For sample 1, dS[T]=1, answer=3. dS[T]+dT[S]=1+1=2, but answer=3.

So the formula is: answer = dS[T] + dT[S] when dS[T] ≥ 2, and 3 when dS[T]=1 (and possible).

But wait, what if dS[T]=1 and impossible? Like the path 1-2 with S=1, T=2: dS[T]=1, answer=-1.

So the condition is: if dS[T]=1, answer is 3 if the graph allows it, else -1. When does dS[T]=1 allow the swap? When S and T are adjacent. Then A at S, B at T. A→T is blocked (B there). B→S is blocked (A there). A must go to another neighbor, or B must. If both S and T have degree ≥ 2 (or one has degree ≥ 2 and the other ≥ 1), we can maneuver. Specifically, if deg(S) ≥ 2 or deg(T) ≥ 2, we can start. If both have degree 1, we're stuck (only the edge between them). 

If both S and T have degree 1, the graph is just the edge S-T (since connected and N=2), or... if N>2, but S and T have degree 1, then the graph is a path with S and T as endpoints. If the path has length 1 (N=2, edge S-T), deg(S)=deg(T)=1, impossible. If the path has length >1, say S=1, T=3 in path 1-2-3-4, deg(S)=1, deg(T)=1, and dS[T]=2, not 1. So dS[T]=1 with both degree 1 means N=2 or a leaf-to-leaf with edge between? No, if dS[T]=1, they are adjacent. If both have degree 1, the only edge is S-T, so N=2, impossible.

If dS[T]=1 and (deg(S) ≥ 2 or deg(T) ≥ 2), then answer=3.

Now for dS[T] ≥ 2: the answer is dS[T] + dT[S]? Not always, as the path 1-2-3-4 shows: dS[T]=3, dT[S]=3, sum=6, but answer=-1.

So we need a condition for dS[T] ≥ 2. The answer is dS[T] + dT[S] if the swap is possible along shortest paths, else we need to detour, making it larger, or it's impossible.

For the path 1-2-3-4, the swap is impossible. For sample 3, the swap is possible with dS[T]+dT[S]=4.

So the general answer is: 
- If dS[T]=1: answer=3 if deg(S)≥2 or deg(T)≥2, else -1.
- If dS[T]≥2: answer= dS[T] + dT[S], UNLESS some condition makes it larger or -1.

What condition? For the path 1-2-3-4, S=1, T=4, dS[T]=3. The condition for swap on a path: impossible if the path is "thin" (no branches) and S,T are not the "middle" in a way that allows passing. Actually, on a path, swap is impossible unless... I showed path 1-2-3 is impossible. Path 1-2-3-4 impossible. I believe on any path, swap is impossible (for S≠T).

Why? On a path, the two pieces are confined to the path. They need to swap positions. But the path is a line, and they can't pass each other (can't share a vertex). So they must "go around", but there's no cycle. Hence impossible. (Unless one piece goes back and forth, but that doesn't help because the other is blocked.)

Wait, is swap possible on a cycle? Cycle 1-2-3-4-1, S=1, T=2. dS[T]=1, answer=3 (as computed for 4-cycle? Wait, 4-cycle is 1-2-4-3-1. Let me redo for cycle 1-2-3-4-1: 1-2, 2-3, 3-4, 4-1. S=1, T=2. (1,2) → A→4 → (4,2) → B→3 → (4,3) → A→1 → (1,3) → B→2 → (1,2) back. Hmm. (1,2) → A→4 → (4,2) → B→1? A at 4, B at 2. B→1: (4,1) → A→? neighbors of 4: {3,1}, 1 has B. A→3: (3,1) → B→2: (3,2) → A→4: (4,2) back. (3,1) → B→4? A at 3. B→? neighbors of 1: {2,4}, A at 3. B→2 or B→4. B→2: (3,2) → A→? neighbors of 3: {2,4}, 2 has B. A→4: (4,2) back. A→2? B there. Dead. B→4 from (3,1): (3,4) → A→2: (2,4) → B→3: (2,3) → A→1: (1,3) → B→2: (1,2) back.

(1,2) → A→4 → (4,2) → A→3 → (3,2) → B→4? A at 3. B→1: (3,1) → A→4? B at 1. A→2? B→1, A→2: (2,1) ← goal! Let me check:
Move 1: A 1→4. (4,2).
Move 2: A 4→3. (3,2).
Move 3: B 2→1. (3,1).
Move 4: A 3→2. (2,1). ✓ Goal!
4 moves. Can we do 3? (1,2) in 3 moves to (2,1). 
(1,2) → A→4 → (4,2) → B→1 → (4,1) → A→3 → (3,1). Not (2,1).
(1,2) → A→4 → (4,2) → B→3 → (4,3) → A→1 → (1,3). Not.
(1,2) → B→3 → (1,3) → A→2 → (2,3) → B→1 → (2,1). 3 moves! Check:
Move 1: B 2→3. (1,3).
Move 2: A 1→2. (2,3).
Move 3: B 3→1. (2,1). ✓
3 moves! So cycle 1-2-3-4-1, S=1, T=2, answer=3.

So on a cycle with S,T adjacent, answer=3.

For cycle 1-2-3-4-1, S=1, T=3 (opposite). dS[T]=2. 
(1,3) → A→2 → (2,3) → B→4 → (2,4) → A→1 → (1,4) → B→3 → (1,3) back.
(1,3) → A→2 → (2,3) → B→2? A there. B→4: (2,4) → A→1: (1,4) → A→? neighbors of 1: {2,4}, 4 has B. A→2: (2,4) back. Dead.
(1,3) → A→2 → (2,3) → A→1 → (1,3) back.
(1,3) → B→4 → (1,4) → A→2 → (2,4) → B→3 → (2,3) → A→1 → (1,3) back.
(1,3) → B→2 → (1,2) → A→? neighbors of 1: {2,4}, 2 has B. A→4: (4,2) → B→3: (4,3) → A→1: (1,3) back. B→1: (4,1) → A→2: (2,1) → B→4: (2,4) → A→3: (3,4) → B→1: (3,1) → A→2: (2,1) back? (2,1) → A→? neighbors of 2: {1,3}, 1 has B. A→3: (3,1) → B→2: (3,2) → A→4: (4,2) → B→3: (4,3) → A→1: (1,3) back.

(1,3) → B→2 → (1,2) → A→4 → (4,2) → B→3 → (4,3) → A→1 → (1,3) back.
(1,3) → B→4 → (1,4) → B→2 → (1,2) → A→4? B at 2. A→? neighbors of 1: {2,4}. A→4: (4,2) → B→3: (4,3) → A→1: (1,3) back.

(1,3) → B→2 → (1,2) → B→? neighbors of 2: {1,3}, 1 has A, 3 free. B→3: (1,3) back.
(1,3) → A→4 → (4,3) → A→1 → (1,3) back. A→? neighbors of 4: {1,3}, 3 has B. A→1: back.
(1,3) → A→2 → (2,3) → A→? neighbors of 2: {1,3}, 3 has B. A→1: back.

Hmm, hard to reach (3,1). Let me try:
(1,3) → A→2 → (2,3) → B→4 → (2,4) → A→3? neighbors of 2: {1,3,4}, 4 has B. A→3: (3,4) → B→1: (3,1) ← goal! 4 moves.
Check: (1,3)→A to 2→(2,3)→B to 4→(2,4)→A to 3→(3,4)→B to 1→(3,1). 
Move 4: A 2→3. State (3,4).
Move 5: B 4→1. State (3,1). 
Wait, that's 5 moves total? Let me recount:
1. A: 1→2. (2,3)
2. B: 3→4. (2,4)
3. A: 2→3. (3,4)
4. B: 4→1. (3,1)
4 moves. And (3,1) is the goal (T,S)=(3,1). Yes! 4 moves. dS[T]+dT[S]=2+2=4. Matches.

Can we do 3? Probably not, since dS[T]+dT[S]=4 and they "interfere" minimally.

So for the cycle with S,T at distance 2, answer = dS[T] + dT[S] = 4.

So the pattern:
- dS[T]=1: answer=3 (if possible).
- dS[T]≥2: answer = dS[T] + dT[S] (if possible).

When is it possible for dS[T]≥2? On a path, never. On a graph with cycles, usually yes.

The condition for possibility: I think it's that the graph is not a path, OR if it's a path, the swap is impossible. For a path (tree with max degree 2), dS[T]≥1, and swap is impossible (as I showed for paths of length 1,2,3).

For a tree with a branch (degree ≥3), can we always swap? Let's see: star graph, center c, leaves. S=leaf1, T=leaf2. dS[T]=2. A at leaf1, B at leaf2. (leaf1, leaf2) → A→c → (c, leaf2) → B→c? A there. B→? neighbors of leaf2: {c}, c has A. B stuck. 
(leaf1, leaf2) → B→c → (leaf1, c) → A→c? B there. Dead.
So on a star with S,T leaves, dS[T]=2, but it's impossible? Let me check.
(c, leaf2): A at c, B at leaf2. A can go to any leaf except leaf2 (since B at leaf2). A→leaf3: (leaf3, leaf2). Then B→c: (leaf3, c). A→c? B there. A→leaf1: (leaf1, c). B→leaf2: (leaf1, leaf2) back. 
(leaf3, c) → B→leaf2: (leaf3, leaf2) → A→c: (c, leaf2) back. A→leaf4: (leaf4, leaf2) ...
This seems impossible because the only path between any two leaves is through c, and c can only hold one piece. So two pieces on leaves can't swap.

So on a star, swap between two leaves is impossible. dS[T]=2, but impossible.

So the formula "answer = dS[T]+dT[S] for dS[T]≥2" is wrong for the star.

So the answer depends heavily on graph structure. We really need the state-space BFS or a clever characterization.

Given the complexity, I think the intended solution is the state-space BFS, and it passes because... hmm, but the state space is N^2.

Wait, maybe the BFS on the state graph is not O(N^2) because of the graph sparsity and BFS properties. Let me think again.

In BFS on the state graph, we process states layer by layer. The number of states in layer k is the number of (a,b) with d((S,T),(a,b)) = k. In the worst case (a long path), this is O(k) for k ≤ N, and the total states visited is O(N^2). For N=2e5, 4e10, too slow.

But the problem has M ≤ 2e5. For a path, M = N-1. The BFS on the state graph for a path: the state graph is a 2D grid (with diagonal forbidden), and BFS from (1,N) to (N,1) visits O(N^2) cells. So the BFS is O(N^2), too slow.

Therefore, the BFS on the full state graph is NOT the intended solution. There must be a smarter algorithm.

Let me think about the problem structure. The two pieces are indistinguishable? No, piece A must go to T, piece B to S. So A's target is T, B's target is S.

The minimum number of moves for A to reach T alone is dS[T]. Similarly dT[S] for B. But with the interaction, it takes more or is impossible.

Here's a key insight: The problem is equivalent to finding the shortest path in a graph where the state is (a, b), a≠b. But we can decompose: consider the "time" and the "position".

Alternative: The answer is the length of the shortest path in the state graph. The state graph has N*(N-1) nodes. But the graph is highly structured: it's the strong product G ⊠ G minus the diagonal, where ⊠ is the strong product (neighbors if differ in one coordinate by an edge).

The strong product of a graph with itself. BFS on G ⊠ G. The number of nodes is N^2. But the graph is the strong product, which has a nice structure.

In the strong product G ⊠ G, (a,b) ~ (a',b') if a=a' and b~b', or a~a' and b=b', or a~a' and b~b'. In our problem, (a,b) ~ (a',b) if a~a' and a'≠b. So it's the strong product minus states where a=b, and minus some edges (when a~a' and a'=b, i.e., the new position equals the other piece).

Hmm, it's G ⊠ G restricted to a≠b, with edges: (a,b)-(a',b) if a~a' and a'≠b, and (a,b)-(a,b') if b~b' and b'≠a, and (a,b)-(a',b') if a~a' and b~b' and a'≠b' — wait, in the strong product, we also have edges when both move. But in our problem, we move only one piece at a time! So the state graph is NOT the strong product. It's the "box product" or the "Cartesian product" with self-loops? No.

From (a,b), we move to (a', b) [move A] or (a, b') [move B]. This is exactly the Cartesian product G □ G, restricted to a≠b, minus the diagonal states. The Cartesian product G □ G has (a,b)~(a',b) if a~a' and a'=a... wait, in the Cartesian product, (a,b) is adjacent to (a',b) if a~a' and a'=a? No, (a,b) ~ (a',b) if a~a' (and the second coordinate is the same). And (a,b) ~ (a,b') if b~b'. So the Cartesian product G □ G has edges along the "A-moves" and "B-moves" separately. This is exactly our state graph (minus the a=b diagonal, and with the constraint a'≠b for A-moves).

So the state graph is the Cartesian product G □ G, with nodes having a≠b. The number of nodes is N*(N-1). The BFS is on this graph.

The Cartesian product G □ G has a nice property: BFS distances satisfy d_{(a,b)}((a,b)) and d_{(S,T)}((a,b)) can be related to dS and dT.

In the Cartesian product, d((S,T), (a,b)) = dS[a] + dT[b]! Because we can move A independently to reach a, and B independently to reach b, and the moves commute. The shortest path in G □ G from (S,T) to (a,b) is exactly dS[a] + dT[b]: move A along a shortest S-a path (dS[a] steps), then move B along a shortest T-b path (dT[b] steps), or interleave