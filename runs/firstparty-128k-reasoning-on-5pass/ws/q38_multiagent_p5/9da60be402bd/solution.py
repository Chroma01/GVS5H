import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    s = ''.join(data[1:])
    C = [s[i * N:(i + 1) * N] for i in range(N)]

    INF = 10**9
    dist = [[INF] * N for _ in range(N)]

    # in_edges[x]: list of (u, c) for edges u -> x with label c
    in_edges = [[] for _ in range(N)]

    # out_bits[c][y]: bitmask of v such that edge y -> v has label c
    out_bits = [[0] * N for _ in range(26)]

    edges = []

    for i in range(N):
        row = C[i]
        for j, ch in enumerate(row):
            if ch == '-':
                continue
            c = ord(ch) - 97
            in_edges[j].append((i, c))
            out_bits[c][i] |= 1 << j
            if i != j:
                edges.append((i, j))

    all_mask = (1 << N) - 1
    row_unvis = [all_mask] * N
    q = deque()
    unvis = N * N

    # Distance 0 sources: empty palindromic path at each vertex.
    for i in range(N):
        bit = 1 << i
        dist[i][i] = 0
        row_unvis[i] &= ~bit
        unvis -= 1
        q.append((i, i))

    # Distance 1 sources: single-edge palindromic paths.
    # Self-loops are skipped because distance 0 already dominates them.
    for u, v in edges:
        bit = 1 << v
        if row_unvis[u] & bit:
            dist[u][v] = 1
            row_unvis[u] &= ~bit
            unvis -= 1
            q.append((u, v))

    # Multi-source BFS. Every transition adds exactly 2.
    while q and unvis:
        x, y = q.popleft()
        nd = dist[x][y] + 2

        for u, c in in_edges[x]:
            M = out_bits[c][y] & row_unvis[u]
            if M:
                row_unvis[u] &= ~M
                unvis -= M.bit_count()

                du = dist[u]
                m = M
                while m:
                    lsb = m & -m
                    v = lsb.bit_length() - 1
                    du[v] = nd
                    q.append((u, v))
                    m ^= lsb

    out_lines = []
    for i in range(N):
        out_lines.append(
            ' '.join(str(dist[i][j] if dist[i][j] != INF else -1) for j in range(N))
        )
    sys.stdout.write('\n'.join(out_lines))

if __name__ == '__main__':
    solve()