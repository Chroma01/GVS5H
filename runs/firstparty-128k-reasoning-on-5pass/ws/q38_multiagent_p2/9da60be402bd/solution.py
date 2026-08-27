import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    grid = data[1:1 + n]

    inc = [[] for _ in range(n)]
    out = [[0] * n for _ in range(26)]

    for i in range(n):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                inc[j].append((i, c))
                out[c][i] |= 1 << j

    dist = [[-1] * n for _ in range(n)]
    mask = [0] * n
    q = []

    for i in range(n):
        dist[i][i] = 0
        mask[i] |= 1 << i
        q.append((i, i, 0))

    for i in range(n):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch != '-' and dist[i][j] == -1:
                dist[i][j] = 1
                mask[i] |= 1 << j
                q.append((i, j, 1))

    head = 0
    while head < len(q):
        x, y, d = q[head]
        head += 1
        nd = d + 2

        for u, c in inc[x]:
            m = out[c][y] & ~mask[u]
            if m:
                mask[u] |= m
                while m:
                    lsb = m & -m
                    v = lsb.bit_length() - 1
                    dist[u][v] = nd
                    q.append((u, v, nd))
                    m ^= lsb

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in dist))

if __name__ == "__main__":
    main()