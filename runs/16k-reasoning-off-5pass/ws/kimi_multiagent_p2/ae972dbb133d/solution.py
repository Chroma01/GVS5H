import sys
from array import array

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        H = int(data[pos]); W = int(data[pos+1]); pos += 2
        rows = data[pos:pos+H]; pos += H
        n = 2 * H * W  # variables: v edges [0, HW), h edges [HW, 2HW)
        par = array('i', range(n))
        pot = bytearray(n)          # xor from node to its parent
        sz = array('i', [1]) * n
        comp = n
        bad = False

        def find(x):
            # returns (root, parity from x to root)
            acc = 0
            r = x
            while par[r] != r:
                acc ^= pot[r]
                r = par[r]
            # path compression
            while par[x] != r:
                nx = par[x]
                px = pot[x]
                par[x] = r
                pot[x] = acc
                acc ^= px
                x = nx
            return r, acc

        def union(x, y, c):
            # enforce x ^ y = c
            nonlocal comp, bad
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                if (px ^ py) != c:
                    bad = True
                return
            if sz[rx] < sz[ry]:
                rx, ry = ry, rx
                px, py = py, px
            # attach ry under rx; t = pot[ry] must satisfy px ^ t ^ py = c
            par[ry] = rx
            pot[ry] = px ^ py ^ c
            sz[rx] += sz[ry]
            comp -= 1

        HW = H * W
        for i in range(H):
            row = rows[i]
            iup = (i - 1) % H
            base_v = i * W
            base_vu = iup * W
            base_h = HW + i * W
            for j in range(W):
                N = base_vu + j
                S = base_v + j
                E = base_h + j
                Wp = base_h + ((j - 1) % W)
                if row[j] == 65:  # 'A'
                    union(N, S, 1)
                    union(E, Wp, 1)
                else:  # 'B'
                    union(N, S, 0)
                    union(E, Wp, 0)
                    union(N, E, 1)
                if bad:
                    break
            if bad:
                break
        if bad:
            out.append('0')
        else:
            out.append(str(pow(2, comp, MOD)))
    sys.stdout.write('\n'.join(out) + '\n')

main()