import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read
    data = input_data().split()
    
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

    # BFS from S to get distances and count shortest paths
    distS = [-1] * (N + 1)
    waysS = [0] * (N + 1)
    
    distS[S] = 0
    waysS[S] = 1
    
    queue = deque([S])
    
    while queue:
        u = queue.popleft()
        d = distS[u]
        w = waysS[u]
        
        for v in adj[u]:
            if distS[v] == -1:
                distS[v] = d + 1
                waysS[v] = w
                queue.append(v)
            elif distS[v] == d + 1:
                waysS[v] += w
                # Cap ways to avoid overflow, we only care if > 1
                if waysS[v] > 2:
                    waysS[v] = 2
    
    D = distS[T]
    
    # Check if multiple shortest paths exist
    if waysS[T] > 1:
        print(2 * D)
        return
    
    # If unique shortest path, check for existence of a path of length D+1
    # This is equivalent to checking if there exists a vertex v such that
    # distS[v] + distT[v] == D + 1
    # We need distT as well.
    
    distT = [-1] * (N + 1)
    queue = deque([T])
    distT[T] = 0
    
    while queue:
        u = queue.popleft()
        d = distT[u]
        
        for v in adj[u]:
            if distT[v] == -1:
                distT[v] = d + 1
                queue.append(v)
    
    # Check condition
    possible = False
    for v in range(1, N + 1):
        if distS[v] != -1 and distT[v] != -1:
            if distS[v] + distT[v] == D + 1:
                possible = True
                break
    
    if possible:
        print(2 * D + 1)
    else:
        print(-1)

if __name__ == '__main__':
    solve()