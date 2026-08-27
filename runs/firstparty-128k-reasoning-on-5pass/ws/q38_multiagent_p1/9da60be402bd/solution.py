import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    rows = data[1:1 + n]

    out_mask = [[0] * 26 for _ in range(n)]
    in_mask = [[0] * 26 for _ in range(n)]
    edges = []

    for i in range(n):
        row = rows[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_mask[i][c] |= 1 << j
                in_mask[j][c] |= 1 << i
                edges.append((i, j))

    pred_info = []
    for x in range(n):
        info = []
        for c in range(26):
            m = in_mask[x][c]
            if m:
                info.append((c, m))
        pred_info.append(info)

    full = (1 << n) - 1
    clear_mask = [full ^ (1 << i) for i in range(n)]
    total = n * n

    def bfs(sources, init_dist):
        dist = [[-1] * n for _ in range(n)]
        unvisited = [full] * n
        q = []
        append = q.append
        remaining = total

        for u, v in sources:
            if dist[u][v] == -1:
                dist[u][v] = init_dist
                unvisited[u] &= clear_mask[v]
                append((u, v, init_dist))
                remaining -= 1

        head = 0
        while head < len(q) and remaining > 0:
            x, y, d = q[head]
            head += 1
            nd = d + 2
            out_y = out_mask[y]

            for c, P in pred_info[x]:
                S = out_y[c]
                if not S:
                    continue

                p = P
                while p:
                    lsb_u = p & -p
                    u = lsb_u.bit_length() - 1
                    new = S & unvisited[u]
                    if new:
                        unvisited[u] ^= new
                        row_dist = dist[u]
                        bits = new
                        while bits:
                            lsb_v = bits & -bits
                            v = lsb_v.bit_length() - 1
                            row_dist[v] = nd
                            append((u, v, nd))
                            remaining -= 1
                            bits ^= lsb_v
                    p ^= lsb_u

        return dist

    even = bfs([(i, i) for i in range(n)], 0)
    odd = bfs(edges, 1)

    out_lines = []
    for i in range(n):
        ei = even[i]
        oi = odd[i]
        line = []
        for j in range(n):
            a = ei[j]
            b = oi[j]
            if a == -1:
                line.append(str(b))
            elif b == -1:
                line.append(str(a))
            else:
                line.append(str(a if a < b else b))
        out_lines.append(' '.join(line))

    sys.stdout.write('\n'.join(out_lines))


if __name__ == '__main__':
    solve()