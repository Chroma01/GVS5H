import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    S = int(next(it))
    T = int(next(it))
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
    
    # BFS on state space (posA, posB) with posA != posB
    # Use list of dictionaries to store visited states efficiently
    visited = [dict() for _ in range(N + 1)]
    q = deque()
    q.append((S, T))
    visited[S][T] = 0
    
    while q:
        a, b = q.popleft()
        d = visited[a][b]
        if a == T and b == S:
            print(d)
            return
        # Move piece A
        for x in adj[a]:
            if x != b and b not in visited[x]:
                visited[x][b] = d + 1
                q.append((x, b))
        # Move piece B
        for y in adj[b]:
            if y != a and y not in visited[a]:
                visited[a][y] = d + 1
                q.append((a, y))
    
    print(-1)

if __name__ == "__main__":
    solve()