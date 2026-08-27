import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rows = data[1:1 + n]

    # Per-character adjacency: out_edges[v][c] = list of w with edge v->w labeled c
    # in_edges[v][c] = list of u with edge u->v labeled c
    out_edges = [[[] for _ in range(26)] for _ in range(n)]
    in_edges = [[[] for _ in range(26)] for _ in range(n)]

    for i in range(n):
        row = rows[i]
        for j in range(n):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                out_edges[i][c].append(j)
                in_edges[j][c].append(i)

    INF = -1
    dist = [[-1] * n for _ in range(n)]
    q = deque()

    # Seeds: empty palindrome (length 0) and single-edge palindromes (length 1)
    for i in range(n):
        dist[i][i] = 0
        q.append((i, i))
    for i in range(n):
        for c in range(26):
            for j in out_edges[i][c]:
                if dist[i][j] == -1:
                    dist[i][j] = 1
                    q.append((i, j))

    # BFS: from state (u, v), wrap with matching edges a->u and v->b of same label
    while q:
        u, v = q.popleft()
        d = dist[u][v] + 2
        for c in range(26):
            ins = in_edges[u][c]
            outs = out_edges[v][c]
            if not ins or not outs:
                continue
            for a in ins:
                row = dist[a]
                for b in outs:
                    if row[b] == -1:
                        row[b] = d
                        q.append((a, b))

    out = sys.stdout
    out.write('\n'.join(' '.join(map(str, row)) for row in dist))
    out.write('\n')

main()