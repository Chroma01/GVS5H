import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    grid = [data[1 + i].decode() for i in range(n)]

    A = ord('a')
    # out_mask[l][c] = bitmask of j with C[l][j] == chr(a+c)
    out_mask = [[0] * 26 for _ in range(n)]
    # in_by_char[k][c] = list of i with C[i][k] == chr(a+c)
    in_by_char = [[None] * 26 for _ in range(n)]
    for i in range(n):
        row = grid[i]
        om = out_mask[i]
        for j in range(n):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - A
                om[c] |= (1 << j)
                lst = in_by_char[j][c]
                if lst is None:
                    in_by_char[j][c] = [i]
                else:
                    lst.append(i)
    # compact: in_pairs[k] = list of (c, ilist)
    in_pairs = []
    for k in range(n):
        pairs = []
        row = in_by_char[k]
        for c in range(26):
            if row[c] is not None:
                pairs.append((c, row[c]))
        in_pairs.append(pairs)

    NN = n * n
    dist = [-1] * NN
    full = (1 << n) - 1
    unvis = [full] * n

    q = deque()
    ap = q.append
    # distance 0 states first
    for i in range(n):
        dist[i * n + i] = 0
        unvis[i] ^= (1 << i)
        ap(i * n + i)
    # then distance 1 states
    for i in range(n):
        row = grid[i]
        base = i * n
        u = unvis[i]
        for j in range(n):
            if row[j] != '-':
                if dist[base + j] == -1:
                    dist[base + j] = 1
                    u ^= (1 << j)
                    ap(base + j)
        unvis[i] = u

    popleft = q.popleft
    while q:
        s = popleft()
        d = dist[s]
        k, l = divmod(s, n)
        nd = d + 2
        oml = out_mask[l]
        for c, ilist in in_pairs[k]:
            m = oml[c]
            if not m:
                continue
            for i in ilist:
                u = unvis[i]
                new = u & m
                if new:
                    unvis[i] = u ^ new
                    base = i * n
                    while new:
                        b = new & -new
                        new ^= b
                        j = b.bit_length() - 1
                        p = base + j
                        dist[p] = nd
                        ap(p)

    out = []
    for i in range(n):
        out.append(' '.join(map(str, dist[i * n:(i + 1) * n])))
    sys.stdout.write('\n'.join(out) + '\n')

main()