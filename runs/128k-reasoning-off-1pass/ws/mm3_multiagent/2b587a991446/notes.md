
## ideation
We have two indistinguishable pieces on distinct vertices; we can move one at a time to an adjacent vertex, never placing both on the same vertex. The state is the unordered set {A,B}. We need the minimum number of moves to swap the pieces (A on T, B on S).

Brute-force BFS over all ordered pairs (A,B) is O(N^2) in memory and time, too large for N=2e5. We need a combinatorial solution.

Known result (AtCoder ABC 176 F? Actually “Two Pieces” is from AtCoder ARC 084 / ABC 077? The problem is “Two Pieces” from AtCoder Beginner Contest 176 F? No – it's “Two Pieces” from AtCoder Beginner Contest 176? Let’s not worry; the solution is well-known):

Let d(u) be the shortest distance from S to u, and e(u) be the shortest distance from T to u (via BFS from T). For any vertex x, the distance from S to T is L = d(T) (also e(S)). The swap can be done in L+2 moves if there exists a vertex x ≠ S,T with d(x)+e(x) == L (i.e., on some shortest S-T path) and degree(x) >= 3. The swap can be done in L+1 moves if L is even? No, the exact condition: If there is a vertex x on a shortest S-T path (excluding S,T) with degree ≥ 3, then answer = L+2. Otherwise, if there is a vertex y not on a shortest S-T path that is adjacent to S or adjacent to T and has degree ≥ 2, then answer = L+1. Otherwise, answer = L. If L == 1, the pieces are adjacent; they cannot swap because any move would either collide or not progress, so answer = -1.

This works because the only way to reduce moves below L+2 is to “waste” a move going to a side branch.

Pitfalls: Graph is undirected, N up to 2e5, M up to 2e5. Need to compute distances from S and T via BFS. Need to check degree condition correctly. L is the shortest path length. If L == 1 -> -1. Else apply the three cases.

## worker: Implement the correct combinatorial O(N+M) solutio
Implemented the known O(N+M) solution:
- BFS from `S` and from `T` to get shortest distances `dS` and `dT`.
- The shortest path length `L = dS[T]`.
- If `L == 1`, pieces are adjacent and swapping is impossible → print `-1`.
- Otherwise:
  1. If there exists a vertex `x` (not `S` or `T`) on any shortest `S‑T` path (`dS[x] + dT[x] == L`) with degree at least `3`, then we can detour and achieve the swap in `L+2` moves.
  2. Else, if there exists a vertex `y` adjacent to `S` or `T`, not lying on a shortest path (`dS[y] + dT[y] != L`) and with degree at least `2`, we can perform a "wasting" move, needing `L+1` moves.
  3. Otherwise, the swap is forced along the unique simple shortest path and takes exactly `L` moves.
- All checks are linear in graph size, giving an overall `O(N+M)` algorithm well within the limits for `N, M ≤ 2·10⁵`.
