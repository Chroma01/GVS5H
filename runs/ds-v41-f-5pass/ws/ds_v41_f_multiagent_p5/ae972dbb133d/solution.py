import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    T = int(data[ptr]); ptr += 1
    out = []
    for _ in range(T):
        H = int(data[ptr]); W = int(data[ptr + 1]); ptr += 2
        rows = data[ptr:ptr + H]; ptr += H

        n = H + W
        parent = list(range(n))
        par = [0] * n          # parity from node to its parent
        size = [1] * n
        comp = n               # number of connected components
        bad = False
        colq = [0] * W         # parity of A's in rows 1..i-1 of column j
        a0 = [0] * W           # [S[0][j] == 'A']

        def find(x):
            root = x
            p = 0
            while parent[root] != root:
                p ^= par[root]
                root = parent[root]
            cur = x
            curp = 0
            while parent[cur] != cur:
                nxt = parent[cur]
                npar = par[cur]
                parent[cur] = root
                par[cur] = p ^ curp
                curp ^= npar
                cur = nxt
            return root, p

        for i in range(H):
            s = rows[i]
            rowpar = 0
            cum = 0
            first = 1 if s[0] == 65 else 0   # 'A' == 65
            row_node = i
            for j in range(W):
                if s[j] == 65:               # Type A
                    rowpar ^= 1
                    cum ^= 1
                    if i:
                        colq[j] ^= 1
                    else:
                        a0[j] = 1
                else:                        # Type B: add edge U_i xor V_j = c
                    c = 1 ^ (cum ^ first) ^ colq[j]
                    rx, px = find(row_node)
                    ry, py = find(H + j)
                    if rx == ry:
                        if (px ^ py) != c:
                            bad = True
                    else:
                        w = px ^ py ^ c
                        if size[rx] < size[ry]:
                            parent[rx] = ry
                            par[rx] = w
                            size[ry] += size[rx]
                        else:
                            parent[ry] = rx
                            par[ry] = w
                            size[rx] += size[ry]
                        comp -= 1
            if rowpar:
                bad = True

        if bad:
            out.append(0)
            continue
        colbad = False
        for j in range(W):
            if colq[j] ^ a0[j]:
                colbad = True
                break
        out.append(0 if colbad else pow(2, comp, MOD))

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()