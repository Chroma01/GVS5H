
## ideation
The problem is a classic state-space BFS on a product graph but the state space is O(N²) — too large for N up to 2e5. We need an efficient method.

Key observations:
- The state graph is the Cartesian product G □ G minus the diagonal (x=y). Moves change exactly one coordinate by traversing an edge.
- The unconstrained distance in G □ G from (S,T) to (T,S) is 2·dist(S,T). This is achievable if there exist two vertex-disjoint shortest paths from S to T (so the tokens can use different routes).
- If no such disjoint paths exist, one token must "step aside" onto a branch or longer path, increasing the number of moves.
- The minimum swap distance can be computed using the distances from S and T (d_S[v], d_T[v]) and checking for a "detour" vertex: a vertex w such that d_S[w] = d_T[w] = k (for some k) and w has a neighbor x with d_S[x] = k+1 and d_T[x] = k+1. If such a pair exists, the answer can be reduced; otherwise a longer detour is needed.
- For adjacent vertices (dist=1), the answer is 3 if a common neighbor exists, else -1.
- For larger distances, the answer is generally 2·dist(S,T) if disjoint shortest paths exist; otherwise 2·dist(S,T)+1, 2·dist(S,T)+2, or -1 depending on the graph structure.

The exact solution involves:
1. BFS from S to compute d_S.
2. BFS from T to compute d_T.
3. Check the parity and the "middle layer" to determine the minimum extra steps.
4. Handle the case dist=1 separately.

This matches the known AtCoder problem "Two Pieces" (ABC 268 F? actually it's ABC 211 D? No, it's ABC 232 F? No, it's actually a well-known problem with solution based on distances and middle-layer analysis).
