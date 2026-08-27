import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    rows = data[1:1 + n]

    # out_mask[v][c] is a bitmask of vertices j such that edge v -> j has label c.
    out_mask = [[0] * 26 for _ in range(n)]

    # in_edges[u] contains (c, i) for every edge i -> u with label c.
    in_edges = [[] for _ in range(n)]

    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_mask[i][c] |= 1 << j
                in_edges[j].append((c, i))

    dist = [[-1] * n for _ in range(n)]

    # row_unvisited[i] has bit j set iff dist[i][j] has not been assigned yet.
    all_mask = (1 << n) - 1
    row_unvisited = [all_mask] * n

    q = deque()
    visited = 0

    # Base case: empty palindrome from i to i, length 0.
    for i in range(n):
        dist[i][i] = 0
        row_unvisited[i] &= ~(1 << i)
        q.append((i, i))
        visited += 1

    # Base case: single edge i -> j, length 1.
    # Diagonal self-loops are skipped because length 0 is shorter.
    for i in range(n):
        di = dist[i]
        ru = row_unvisited[i]
        for j, ch in enumerate(rows[i]):
            if ch != '-' and i != j:
                if di[j] == -1:
                    di[j] = 1
                    ru &= ~(1 << j)
                    q.append((i, j))
                    visited += 1
        row_unvisited[i] = ru

    total = n * n

    # Multi-source BFS over pair-states (u, v).
    # From inner state (u, v), add matching outer edges i -> u and v -> j.
    while q and visited < total:
        u, v = q.popleft()
        nd = dist[u][v] + 2
        out_v = out_mask[v]

        for c, i in in_edges[u]:
            new = out_v[c] & row_unvisited[i]
            if new:
                # All bits in new are currently unvisited in row i.
                row_unvisited[i] ^= new
                di = dist[i]
                m = new
                while m:
                    lsb = m & -m
                    j = lsb.bit_length() - 1
                    di[j] = nd
                    q.append((i, j))
                    visited += 1
                    m ^= lsb

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in dist))

if __name__ == "__main__":
    solve()