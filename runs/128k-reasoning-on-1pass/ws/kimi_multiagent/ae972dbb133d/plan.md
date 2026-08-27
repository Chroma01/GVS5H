```python
import sys
from array import array

MOD = 998244353
A = ord('A')
B = ord('B')


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    p = 0
    T = int(data[p]); p += 1
    out = []

    for _ in range(T):
        H = int(data[p]); W = int(data[p + 1]); p += 2
        rows = data[p:p + H]; p += H

        row_par = bytearray(H)
        col_par = bytearray(W)

        for i in range(H):
            r = rows[i]
            rp = 0
            for j in range(W):
                if r[j] == A:
                    rp ^= 1
                    col_par[j] ^= 1
            row_par[i] = rp

        bad = False
        for x in row_par:
            if x:
                bad = True
                break
        if not bad:
            for x in col_par:
                if x:
                    bad = True
                    break

        if bad:
            out.append("0")
            continue

        n = H + W
        parent = array('i', range(n))
        size = array('i', [1]) * n
        w = bytearray(n)  # parity to parent

        def find(x):
            if parent[x] == x:
                return x, 0
            path = []
            y = x
            while parent[y] != y:
                path.append(y)
                y = parent[y]
            root = y
            suff = 0
            for node in reversed(path):
                old = w[node]
                w[node] = suff ^ old
                parent[node] = root
                suff = w[node]
            return root, suff

        ok = True
        comp = n

        def union(a, b, d):
            nonlocal ok, comp
            ra, pa = find(a)
            rb, pb = find(b)
            if ra == rb:
                if (pa ^ pb) != d:
                    ok = False
                return False
            x = pa ^ pb ^ d  # value[ra] + value[rb]
            if size[ra] < size[rb]:
                parent[ra] = rb
                w[ra] = x
                size[rb] += size[ra]
            else:
                parent[rb] = ra
                w[rb] = x
                size[ra] += size[rb]
            comp -= 1
            return True

        # colpref[j] = xor of t_{1..i-1, j} for current row i >= 1
        colpref = bytearray(W)

        for i in range(H):
            r = rows[i]
            hpref = 0  # h_{i,0}=0; for j>0, xor of t_{i,1..j}
            for j in range(W):
                t = 1 if r[j] == A else 0
                if j > 0:
                    hpref ^= t

                if r[j] == B:
                    if i == 0:
                        pn = 1 if r[j] == A else 0  # = t_{0,j}; here 0 because cell is B
                    else:
                        pn = colpref[j]
                    d = 1 ^ pn ^ hpref
                    union(i, H + j, d)

                if i >= 1:
                    colpref[j] ^= t

        if not ok:
            out.append("0")
        else:
            out.append(str(pow(2, comp, MOD)))

    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()
```