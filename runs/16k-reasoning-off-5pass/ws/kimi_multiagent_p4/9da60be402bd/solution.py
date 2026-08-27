import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    rows = [data[1 + i].decode() for i in range(n)]

    # in_list[u][c]: list of predecessors x with edge x->u labeled c
    # in_letters[u]: 26-bit mask of letters present on incoming edges of u
    # out_mask[v][c]: bitmask (int) of successors y with edge v->y labeled c
    # out_letters[v]: 26-bit mask of letters present on outgoing edges of v
    in_list = [[None] * 26 for _ in range(n)]
    in_letters = [0] * n
    out_mask = [[0] * 26 for _ in range(n)]
    out_letters = [0] * n

    dist = [[-1] * n for _ in range(n)]
    vis = [0] * n  # vis[x]: bitmask of y such that (x, y) discovered
    q = deque()

    # Seed 1: (i, i) with distance 0 (empty palindrome) -- enqueued first
    for i in range(n):
        dist[i][i] = 0
        vis[i] |= (1 << i)
        q.append(i * n + i)

    # Parse edges; seed 2: (i, j) with distance 1 for each edge i->j
    for i in range(n):
        row = rows[i]
        oi = out_mask[i]
        for j in range(n):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                oi[c] |= (1 << j)
                out_letters[i] |= (1 << c)
                lst = in_list[j][c]
                if lst is None:
                    in_list[j][c] = [i]
                else:
                    lst.append(i)
                in_letters[j] |= (1 << c)
                if dist[i][j] == -1:
                    dist[i][j] = 1
                    vis[i] |= (1 << j)
                    q.append(i * n + j)

    # Multi-source BFS over pair-states; every transition adds exactly 2,
    # and initial queue is ordered (all 0s then all 1s), so first discovery
    # of a state is its shortest distance.
    while q:
        s = q.popleft()
        u, v = divmod(s, n)
        d = dist[u][v]
        nd = d + 2
        common = in_letters[u] & out_letters[v]
        om_v = out_mask[v]
        in_u = in_list[u]
        while common:
            lb = common & -common
            c = lb.bit_length() - 1
            common ^= lb
            om = om_v[c]
            if om:
                for x in in_u[c]:
                    new = om & ~vis[x]
                    if new:
                        vis[x] |= new
                        dx = dist[x]
                        m = new
                        base = x * n
                        while m:
                            b = m & -m
                            y = b.bit_length() - 1
                            m ^= b
                            dx[y] = nd
                            q.append(base + y)

    out_lines = [' '.join(map(str, row)) for row in dist]
    sys.stdout.write('\n'.join(out_lines) + '\n')

main()