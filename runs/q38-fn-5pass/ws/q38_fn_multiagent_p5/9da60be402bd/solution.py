import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    chars = ''.join(data[1:])

    # in_lists[u][c] = list of p such that edge p -> u has label c
    # out_bits[v][c] = bitset of q such that edge v -> q has label c
    in_lists = [[[] for _ in range(26)] for _ in range(N)]
    out_bits = [[0] * 26 for _ in range(N)]
    edges = []

    for i in range(N):
        s = chars[i * N:(i + 1) * N]
        for j, ch in enumerate(s):
            if ch != '-':
                c = ord(ch) - 97
                in_lists[j][c].append(i)
                out_bits[i][c] |= 1 << j
                edges.append((i, j))

    in_by_letter = []
    for u in range(N):
        lst = []
        for c in range(26):
            if in_lists[u][c]:
                lst.append((c, in_lists[u][c]))
        in_by_letter.append(lst)

    full = (1 << N) - 1
    row_base = [i * N for i in range(N)]

    def bfs(q, dist, unvisited):
        if not q:
            return

        append = q.append
        popleft = q.popleft
        N_local = N
        in_by = in_by_letter
        out = out_bits
        bases = row_base

        while q:
            idx = popleft()
            d = dist[idx] + 2
            u = idx // N_local
            v = idx - u * N_local

            for c, inlist in in_by[u]:
                outmask = out[v][c]
                if not outmask:
                    continue

                for p in inlist:
                    qbits = outmask & unvisited[p]
                    if qbits:
                        unvisited[p] ^= qbits
                        qb = qbits
                        base = bases[p]

                        while qb:
                            lsb = qb & -qb
                            qq = lsb.bit_length() - 1
                            nidx = base + qq
                            dist[nidx] = d
                            append(nidx)
                            qb ^= lsb

    total = N * N

    # Even-length palindromes: centers are empty paths (v, v), length 0.
    dist_e = [-1] * total
    unvis_e = [full] * N
    qe = deque()

    for v in range(N):
        idx = row_base[v] + v
        dist_e[idx] = 0
        qe.append(idx)
        unvis_e[v] ^= 1 << v

    bfs(qe, dist_e, unvis_e)

    # Odd-length palindromes: centers are single edges (u, v), length 1.
    dist_o = [-1] * total
    unvis_o = [full] * N
    qo = deque()

    for u, v in edges:
        idx = row_base[u] + v
        if dist_o[idx] == -1:
            dist_o[idx] = 1
            qo.append(idx)
            unvis_o[u] ^= 1 << v

    bfs(qo, dist_o, unvis_o)

    lines = []
    for i in range(N):
        base = row_base[i]
        vals = []
        for j in range(N):
            idx = base + j
            a = dist_e[idx]
            b = dist_o[idx]

            if a == -1:
                vals.append(str(b))
            elif b == -1:
                vals.append(str(a))
            else:
                vals.append(str(a if a < b else b))

        lines.append(' '.join(vals))

    sys.stdout.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()