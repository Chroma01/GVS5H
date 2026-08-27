import sys
from collections import defaultdict, deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    # Next N tokens are the rows
    rows = data[1:1+N]
    
    # Build adjacency lists
    out = [[] for _ in range(N)]  # out[u] = list of (v, char)
    inc = [[] for _ in range(N)]  # inc[v] = list of (u, char)
    
    for i in range(N):
        row = rows[i]
        for j in range(N):
            c = row[j]
            if c != '-':
                out[i].append((j, c))
                inc[j].append((i, c))
    
    # BFS on product graph
    INF = -1
    dist = [[INF] * N for _ in range(N)]
    q = deque()
    
    # Initialize with (k, k) states
    for k in range(N):
        dist[k][k] = 0
        q.append((k, k))
    
    while q:
        u, v = q.popleft()
        d = dist[u][v]
        # Try to extend: u -> x with label c1, y -> v with label c2, c1 == c2
        for x, c1 in out[u]:
            for y, c2 in inc[v]:
                if c1 == c2:
                    if dist[x][y] == INF:
                        dist[x][y] = d + 1
                        q.append((x, y))
    
    # Output
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(dist[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines) + '\n')

if __name__ == "__main__":
    solve()