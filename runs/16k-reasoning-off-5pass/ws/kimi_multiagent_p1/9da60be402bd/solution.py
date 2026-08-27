import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    rows = data[1:1 + n]

    # Per-vertex, per-label predecessor and successor bitmasks.
    # pred[c][u] = bitmask of x such that edge x -> u has label c
    # succ[c][v] = bitmask of y such that edge v -> y has label c
    pred = [[0] * n for _ in range(26)]
    succ = [[0] * n for _ in range(26)]
    for i in range(n):
        row = rows[i]
        for j in range(n):
            ch = row[j]
            if ch != 45:  # '-'
                c = ch - 97
                succ[c][i] |= 1 << j
                pred[c][j] |= 1 << i

    NEG = -1
    dist = [[NEG] * n for _ in range(n)]
    q = deque()

    # Length 0 palindromes: empty string at (i, i)
    for i in range(n):
        dist[i][i] = 0
        q.append(i * n + i)

    # Length 1 palindromes: single edge i -> j
    for c in range(26):
        sc = succ[c]
        for u in range(n):
            m = sc[u]
            v = 0
            while m:
                if m & 1:
                    if dist[u][v] == NEG:
                        dist[u][v] = 1
                        q.append(u * n + v)
                m >>= 1
                v += 1

    # Multi-source BFS over pair states (u, v).
    # Extension: edges x -> u and v -> y with same label c give (x, y) at d + 2.
    while q:
        cur = q.popleft()
        u, v = divmod(cur, n)
        d = dist[u][v] + 2
        for c in range(26):
            xs = pred[c][u]
            if not xs:
                continue
            ys = succ[c][v]
            if not ys:
                continue
            # enumerate set bits of xs
            xm = xs
            while xm:
                lb = xm & -xm
                x = lb.bit_length() - 1
                xm ^= lb
                dx = dist[x]
                base = x * n
                ym = ys
                while ym:
                    lby = ym & -ym
                    y = lby.bit_length() - 1
                    ym ^= lby
                    if dx[y] == NEG:
                        dx[y] = d
                        q.append(base + y)

    out = sys.stdout
    write = out.write
    for i in range(n):
        write(' '.join(map(str, dist[i])))
        write('\n')

main()