import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    rows = [data[1 + i].decode() for i in range(N)]

    # in_mask[c][u] = bitmask of x such that edge x->u has label c
    # out_mask[c][v] = bitmask of y such that edge v->y has label c
    in_mask = [[0] * N for _ in range(26)]
    out_mask = [[0] * N for _ in range(26)]
    for u in range(N):
        row = rows[u]
        for v in range(N):
            ch = row[v]
            if ch != '-':
                c = ord(ch) - 97
                out_mask[c][u] |= 1 << v
                in_mask[c][v] |= 1 << u

    visited = [0] * N          # visited[u] = bitmask over v of known states
    dist = [[-1] * N for _ in range(N)]
    q = deque()

    # Even-length centres: empty path, distance 0
    for i in range(N):
        visited[i] |= 1 << i
        dist[i][i] = 0
        q.append(i * N + i)

    # Odd-length centres: single edge, distance 1
    for u in range(N):
        row = rows[u]
        for v in range(N):
            if row[v] != '-' and not ((visited[u] >> v) & 1):
                visited[u] |= 1 << v
                dist[u][v] = 1
                q.append(u * N + v)

    # Expand outward: from (u,v) at distance d, pair an incoming c-edge x->u
    # with an outgoing c-edge v->y, giving (x,y) at distance d+2.
    while q:
        s = q.popleft()
        u = s // N
        v = s - u * N
        nd = dist[u][v] + 2
        for c in range(26):
            X = in_mask[c][u]
            if not X:
                continue
            Y = out_mask[c][v]
            if not Y:
                continue
            xx = X
            while xx:
                b = xx & (-xx)
                x = b.bit_length() - 1
                xx ^= b
                new = Y & ~visited[x]
                if new:
                    visited[x] |= new
                    yy = new
                    while yy:
                        b2 = yy & (-yy)
                        y = b2.bit_length() - 1
                        yy ^= b2
                        dist[x][y] = nd
                        q.append(x * N + y)

    out = [' '.join(map(str, dist[i])) for i in range(N)]
    sys.stdout.write('\n'.join(out) + '\n')


main()