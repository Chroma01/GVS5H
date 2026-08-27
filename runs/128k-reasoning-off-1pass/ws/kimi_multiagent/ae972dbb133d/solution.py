import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        H = int(data[pos]); W = int(data[pos + 1]); pos += 2
        rows = data[pos:pos + H]; pos += H
        N = H * W
        M = 2 * N
        parent = list(range(M))
        parity = bytearray(M)  # parity[x] = x XOR parent[x]
        comp = M
        bad = False

        def find(x):
            # iterative find with path compression, returns (root, parity to root)
            p = 0
            r = x
            while parent[r] != r:
                p ^= parity[r]
                r = parent[r]
            # compress
            while parent[x] != r:
                nxt = parent[x]
                old = parity[x]
                parity[x] = p
                parent[x] = r
                p ^= old
                x = nxt
            return r, p

        def union(x, y, c):
            nonlocal comp, bad
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                if (px ^ py) != c:
                    bad = True
                return
            # attach rx under ry
            parent[rx] = ry
            parity[rx] = px ^ py ^ c
            comp -= 1

        for i in range(H):
            row = rows[i]
            base = i * W
            up_base = ((i - 1) % H) * W
            for j in range(W):
                t = row[j]
                hL = base + ((j - 1) % W)
                hR = base + j
                vT = N + up_base + j
                vB = N + base + j
                if t == 65:  # 'A'
                    union(hL, hR, 1)
                    union(vT, vB, 1)
                else:  # 'B'
                    union(hL, hR, 0)
                    union(vT, vB, 0)
                    union(hR, vB, 1)
        if bad:
            out.append('0')
        else:
            out.append(str(pow(2, comp, MOD)))
    sys.stdout.write('\n'.join(out) + '\n')

solve()