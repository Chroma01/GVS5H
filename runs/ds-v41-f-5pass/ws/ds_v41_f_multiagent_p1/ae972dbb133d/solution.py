import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    T = int(data[ptr]); ptr += 1
    MOD = 998244353
    out = []
    for _ in range(T):
        H = int(data[ptr]); W = int(data[ptr + 1]); ptr += 2
        rows = data[ptr:ptr + H]; ptr += H

        # Parity precondition: every row and every column must have an even
        # number of A tiles, else the internal cycles of D/R edges conflict.
        colxor = [0] * W
        bad = False
        for i in range(H):
            row = rows[i]
            rp = 0
            for j in range(W):
                if row[j] == 65:  # 'A'
                    rp ^= 1
                    colxor[j] ^= 1
            if rp:
                bad = True
        if not bad:
            for v in colxor:
                if v:
                    bad = True
                    break
        if bad:
            out.append('0')
            continue

        # Parity DSU over H row-variables and W column-variables.
        n = H + W
        parent = list(range(n))
        par = [0] * n      # par[x] = x XOR parent[x]
        size = [1] * n

        def find(x):
            root = x
            acc = 0
            while parent[root] != root:
                acc ^= par[root]
                root = parent[root]
            cur = x
            pacc = acc
            while parent[cur] != root:
                nxt = parent[cur]
                w = par[cur]
                parent[cur] = root
                par[cur] = pacc
                pacc ^= w
                cur = nxt
            return root, acc

        colPre = [0] * W     # colPre[j] = XOR_{k=0}^{i-1} A(k,j)
        consistent = True
        for i in range(H):
            row = rows[i]
            rowPre = 0       # rowPre = XOR_{k=0}^{j-1} A(i,k)
            for j in range(W):
                a = 1 if row[j] == 65 else 0
                if a == 0:   # type B cell -> cross equation alpha_j XOR beta_i = const
                    const = 1 ^ colPre[j] ^ rowPre
                    rx, px = find(H + j)
                    ry, py = find(i)
                    d = const ^ px ^ py
                    if rx == ry:
                        if d:
                            consistent = False
                            break
                    else:
                        if size[rx] < size[ry]:
                            rx, ry = ry, rx
                        parent[ry] = rx
                        par[ry] = d
                        size[rx] += size[ry]
                rowPre ^= a
                colPre[j] ^= a
            if not consistent:
                break

        if not consistent:
            out.append('0')
            continue

        comp = 0
        for x in range(n):
            if parent[x] == x:
                comp += 1
        out.append(str(pow(2, comp, MOD)))

    sys.stdout.write('\n'.join(out) + '\n')

main()