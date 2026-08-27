import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    out_edges = [[[] for _ in range(26)] for _ in range(N)]
    in_edges = [[[] for _ in range(26)] for _ in range(N)]
    out_list = [[] for _ in range(N)]
    for i in range(N):
        row = next(it)
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - ord('a')
                out_edges[i][c].append(j)
                in_edges[j][c].append(i)
                out_list[i].append((j, c))

    INF = 10**9
    dist = [[INF] * N for _ in range(N)]
    dq = deque()
    for m in range(N):
        dist[m][m] = 0
        dq.append((m, m))

    while dq:
        u, v = dq.popleft()
        d = dist[u][v]
        # weight 1: center expansion (u == v) - take one edge from u
        if u == v:
            for c in range(26):
                for u2 in out_edges[u][c]:
                    nd = d + 1
                    if nd < dist[u2][u]:
                        dist[u2][u] = nd
                        dq.appendleft((u2, u))
        # weight 1: finish a single edge u -> v
        for v2, c in out_list[u]:
            if v2 == v:
                nd = d + 1
                if nd < dist[v][v]:
                    dist[v][v] = nd
                    dq.appendleft((v, v))
                break
        # weight 1: finish a single edge v -> u
        for u2, c in out_list[v]:
            if u2 == u:
                nd = d + 1
                if nd < dist[u][u]:
                    dist[u][u] = nd
                    dq.appendleft((u, u))
                break
        # weight 2: match both sides simultaneously
        for c in range(26):
            if not out_edges[u][c] or not in_edges[v][c]:
                continue
            for u2 in out_edges[u][c]:
                for v2 in in_edges[v][c]:
                    nd = d + 2
                    if nd < dist[u2][v2]:
                        dist[u2][v2] = nd
                        dq.append((u2, v2))

    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            if dist[i][j] == INF:
                row.append("-1")
            else:
                row.append(str(dist[i][j]))
        out_lines.append(" ".join(row))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()