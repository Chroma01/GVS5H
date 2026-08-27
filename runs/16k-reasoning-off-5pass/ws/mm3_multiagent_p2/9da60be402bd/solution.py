import sys
from collections import deque

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    N = int(data[0].strip())
    rows = data[1:1+N]
    # adjacency list: adj[u] = list of (v, label_char)
    adj = [[] for _ in range(N)]
    for i in range(N):
        row = rows[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                adj[i].append((j, ch))
    # BFS over state (u, v, p) where p in {0,1}
    INF = 10**9
    dist = [[[INF]*2 for _ in range(N)] for __ in range(N)]
    q = deque()
    # multi-source: start from (i,i,0) for all i
    for i in range(N):
        dist[i][i][0] = 0
        q.append((i, i, 0))
    while q:
        u, v, p = q.popleft()
        d = dist[u][v][p]
        if p == 0:
            # 1) both walkers move on same label
            # iterate over edges from u and v
            for (x, cu) in adj[u]:
                for (y, cv) in adj[v]:
                    if cu == cv:
                        if dist[x][y][0] > d + 1:
                            dist[x][y][0] = d + 1
                            q.append((x, y, 0))
            # 2) move only forward walker (u)
            for (x, cu) in adj[u]:
                if dist[x][v][1] > d + 1:
                    dist[x][v][1] = d + 1
                    q.append((x, v, 1))
            # 3) move only backward walker (v)
            for (y, cv) in adj[v]:
                if dist[u][y][1] > d + 1:
                    dist[u][y][1] = d + 1
                    q.append((u, y, 1))
        else:  # p == 1
            # must move both walkers on same label to close palindrome
            for (x, cu) in adj[u]:
                for (y, cv) in adj[v]:
                    if cu == cv:
                        if dist[x][y][0] > d + 1:
                            dist[x][y][0] = d + 1
                            q.append((x, y, 0))
    # output answers
    out_lines = []
    for i in range(N):
        row_vals = []
        for j in range(N):
            d = dist[i][j][0]
            if d == INF:
                row_vals.append("-1")
            else:
                row_vals.append(str(d))
        out_lines.append(" ".join(row_vals))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()