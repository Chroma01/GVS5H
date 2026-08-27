import sys
from collections import deque

def solve():
    # Increase recursion depth just in case, though we use iterative BFS
    sys.setrecursionlimit(10**6)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    M = int(next(iterator))
    S = int(next(iterator))
    T = int(next(iterator))
    
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        
    # BFS from S to get distS
    distS = [-1] * (N + 1)
    distS[S] = 0
    queue = deque([S])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distS[v] == -1:
                distS[v] = distS[u] + 1
                queue.append(v)
                
    # BFS from T to get distT
    distT = [-1] * (N + 1)
    distT[T] = 0
    queue = deque([T])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distT[v] == -1:
                distT[v] = distT[u] + 1
                queue.append(v)
                
    D = distS[T]
    
    # Check if there is a vertex v on a shortest path from S to T
    # that has a neighbor u such that distS[u] + distT[u] > D.
    # If such a vertex exists, the answer is 2 * D.
    possible_fast = False
    for v in range(1, N + 1):
        if distS[v] + distT[v] == D:
            # v is on a shortest path
            for u in adj[v]:
                if distS[u] + distT[u] > D:
                    possible_fast = True
                    break
        if possible_fast:
            break
            
    if possible_fast:
        print(2 * D)
        return
        
    # If not, we need to run BFS on the product graph.
    # However, if the graph is essentially a simple path between S and T,
    # it might be impossible. The BFS will determine this.
    # State: (posA, posB)
    # Initial: (S, T)
    # Target: (T, S)
    
    # To save memory, we can use a set for visited states.
    # Since N is up to 2*10^5, we can't use a 2D array.
    # We use a set of tuples.
    
    start_state = (S, T)
    target_state = (T, S)
    
    if start_state == target_state:
        print(0)
        return
        
    visited = set()
    visited.add(start_state)
    queue = deque([(S, T, 0)])
    
    while queue:
        u, v, dist = queue.popleft()
        
        # Try moving A
        for next_u in adj[u]:
            if next_u == v:
                continue # Cannot occupy same vertex
            new_state = (next_u, v)
            if new_state == target_state:
                print(dist + 1)
                return
            if new_state not in visited:
                visited.add(new_state)
                queue.append((next_u, v, dist + 1))
                
        # Try moving B
        for next_v in adj[v]:
            if next_v == u:
                continue # Cannot occupy same vertex
            new_state = (u, next_v)
            if new_state == target_state:
                print(dist + 1)
                return
            if new_state not in visited:
                visited.add(new_state)
                queue.append((u, next_v, dist + 1))
                
    print(-1)

solve()