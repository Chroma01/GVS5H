import sys
from collections import deque

def solve():
    # Increase recursion depth just in case, though we use iterative BFS
    sys.setrecursionlimit(300000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = int(next(iterator))
        T = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # BFS to compute shortest distances from a source
    def bfs(start_node):
        dist = [-1] * (N + 1)
        dist[start_node] = 0
        queue = deque([start_node])
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return dist

    distS = bfs(S)
    distT = bfs(T)
    
    # If T is not reachable from S (should not happen in connected graph, but safe check)
    if distS[T] == -1:
        print(-1)
        return

    # Check if S and T are adjacent
    is_adjacent = (distS[T] == 1)
    
    if is_adjacent:
        # If they are adjacent, they block each other directly.
        # We need a "detour" vertex.
        # If N=2, there are no other vertices, so impossible.
        if N == 2:
            print(-1)
        else:
            # If N > 2, since the graph is connected, at least one of S or T
            # must have a neighbor other than the other (unless they are isolated leaves connected only to each other, which implies N=2).
            # Actually, if N > 2 and connected, and S-T is an edge, can both S and T have degree 1?
            # If deg(S)=1 and deg(T)=1, then S and T are only connected to each other.
            # This means the rest of the graph (N-2 nodes) is not connected to S or T.
            # But the graph is connected. So this is impossible for N > 2.
            # Therefore, if N > 2, there is always a vertex v != S, T adjacent to S or T.
            # The cost is distS[T] + distT[S] + 1 = 1 + 1 + 1 = 3.
            print(3)
    else:
        # They are not adjacent.
        # If the graph has a cycle (M >= N), we can always find a detour or use the cycle to bypass.
        # If the graph is a tree (M == N-1), and they are not adjacent, they block each other on the unique path.
        if M >= N:
            # Has a cycle, so we can swap.
            # The minimum moves is simply the sum of distances because we can route around.
            # Note: Even if the shortest paths overlap, the existence of a cycle allows one piece to wait/detour.
            # The cost is exactly distS[T] + distT[S].
            print(distS[T] + distT[S])
        else:
            # Tree and not adjacent -> impossible to swap without blocking on the unique path.
            print(-1)

solve()