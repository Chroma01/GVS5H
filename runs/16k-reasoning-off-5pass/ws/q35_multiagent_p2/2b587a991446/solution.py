import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
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

    # BFS from S
    dist_s = [-1] * (N + 1)
    dist_s[S] = 0
    queue = deque([S])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist_s[v] == -1:
                dist_s[v] = dist_s[u] + 1
                queue.append(v)

    # BFS from T
    dist_t = [-1] * (N + 1)
    dist_t[T] = 0
    queue = deque([T])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist_t[v] == -1:
                dist_t[v] = dist_t[u] + 1
                queue.append(v)

    # If T is not reachable from S (should not happen as graph is connected)
    if dist_s[T] == -1:
        print(-1)
        return

    D = dist_s[T]

    # Case 1: S and T are adjacent
    if D == 1:
        # If the graph is just a single edge between S and T, they block each other.
        # This happens if N=2 and M=1.
        # More generally, if S has only neighbor T and T has only neighbor S.
        if len(adj[S]) == 1 and len(adj[T]) == 1:
            print(-1)
        else:
            # Otherwise, one can move aside, swap, and move back.
            # Cost is 3: A moves to neighbor, B moves to S, A moves to T.
            print(3)
        return

    # Case 2: Distance > 1
    # We need to check if there is a "detour" or alternative path that allows swapping.
    # If the shortest path is unique and forms a simple path with no other edges connecting
    # vertices on the shortest path (or providing a bypass), it might be impossible.
    # However, a simpler condition for impossibility in this specific problem structure
    # is if the shortest path is unique and there are no "parallel" edges or cycles
    # involving the shortest path.
    
    # Check for detour:
    # A detour exists if there is an edge (u, v) such that it provides an alternative
    # route on the shortest path DAG. Specifically, if there is an edge (u, v) such that
    # dist_s[u] + 1 + dist_t[v] == D AND dist_s[v] + 1 + dist_t[u] == D is NOT the only way.
    # Actually, if there is ANY edge (u, v) such that dist_s[u] + 1 + dist_t[v] == D
    # and dist_s[v] + 1 + dist_t[u] == D, it means there's a "diamond" shape, allowing bypass.
    # But even simpler: if there is a vertex on the shortest path that has a neighbor
    # also on the shortest path but not the next/previous one, or a neighbor off the path
    # that connects back.
    
    # Standard solution for this problem:
    # If there is an edge (u, v) such that dist_s[u] + 1 + dist_t[v] == D and dist_s[v] + 1 + dist_t[u] == D,
    # then answer is 2*D.
    # Also, if there are multiple shortest paths, answer is 2*D.
    # If the shortest path is unique and is a simple path (no other edges connect vertices on it),
    # then it is impossible (-1).
    
    # Let's check if there is an edge (u, v) such that:
    # dist_s[u] + 1 + dist_t[v] == D and dist_s[v] + 1 + dist_t[u] == D
    # This indicates a "parallel" edge on the shortest path.
    
    has_detour = False
    
    # We can iterate over all edges to check for detours
    # To avoid O(M) check being too slow if M is large, note M <= 2*10^5, so it's fine.
    for u in range(1, N + 1):
        if dist_s[u] == -1 or dist_t[u] == -1:
            continue
        # If u is on a shortest path
        if dist_s[u] + dist_t[u] == D:
            for v in adj[u]:
                # Check if v is also on a shortest path and connected by an edge that creates a detour
                # Specifically, if there is an edge (u, v) such that both u and v are on shortest paths
                # and the edge is not the only way to traverse between them on the shortest path.
                # A simpler check: if there is an edge (u, v) such that
                # dist_s[u] + 1 + dist_t[v] == D and dist_s[v] + 1 + dist_t[u] == D
                if dist_s[v] != -1 and dist_t[v] != -1:
                    if dist_s[u] + 1 + dist_t[v] == D and dist_s[v] + 1 + dist_t[u] == D:
                        has_detour = True
                        break
            if has_detour:
                break
    
    # Also, if there are multiple shortest paths, it's a detour.
    # The condition above covers parallel edges. What about branching?
    # If there are multiple shortest paths, there must be a vertex with multiple outgoing edges
    # on the shortest path DAG. This is covered by the edge check if we consider the structure.
    # Actually, the condition `dist_s[u] + 1 + dist_t[v] == D` means (u,v) is on a shortest path.
    # If there are two such edges from u, or two such edges to v, it implies multiple paths.
    # The check `dist_s[u] + 1 + dist_t[v] == D and dist_s[v] + 1 + dist_t[u] == D` specifically
    # finds a cycle of length 2 on the shortest path DAG (a diamond).
    
    # If no such detour is found, it means the shortest path is unique and simple.
    if has_detour:
        print(2 * D)
    else:
        print(-1)

solve()