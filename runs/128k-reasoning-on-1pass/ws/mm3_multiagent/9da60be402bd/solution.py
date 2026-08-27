import sys
from collections import deque

def solve() -> None:
    input = sys.stdin.readline
    N_line = input()
    while N_line.strip() == "":
        N_line = input()
    N = int(N_line)

    # out[u][c] : list of vertices w with edge u -> w labelled c (c = 0..25)
    out_adj = [ [ [] for _ in range(26) ] for _ in range(N) ]
    # inc[u][c] : list of vertices w with edge w -> u labelled c
    inc_adj = [ [ [] for _ in range(26) ] for _ in range(N) ]

    for i in range(N):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_adj[i][c].append(j)
                inc_adj[j][c].append(i)

    INF = 10 ** 9
    dist = [ [ INF ] * N for _ in range(N) ]

    # empty walk (length 0)
    for i in range(N):
        dist[i][i] = 0

    # walks of length 1 (direct edge)
    for i in range(N):
        for c in range(26):
            for j in out_adj[i][c]:
                if dist[i][j] > 1:
                    dist[i][j] = 1

    q = deque()
    for i in range(N):
        for j in range(N):
            if dist[i][j] != INF:
                q.append((i, j))

    while q:
        u, v = q.popleft()
        cur = dist[u][v]
        nd = cur + 2
        inc_u = inc_adj[u]
        out_v = out_adj[v]
        for c in range(26):
            pre = inc_u[c]          # vertices x with edge x -> u (label c)
            nxt = out_v[c]          # vertices y with edge v -> y (label c)
            if not pre or not nxt:
                continue
            for x in pre:
                for y in nxt:
                    if dist[x][y] > nd:
                        dist[x][y] = nd
                        q.append((x, y))

    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            val = dist[i][j]
            row.append(str(val) if val != INF else "-1")
        out_lines.append(" ".join(row))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()