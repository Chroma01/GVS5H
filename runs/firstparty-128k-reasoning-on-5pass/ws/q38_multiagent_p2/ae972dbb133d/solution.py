import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2
        row_start = idx
        idx += H

        n = H + W
        parent = list(range(n))
        size = [1] * n
        parity = [0] * n
        comp = n
        colpref = [0] * W
        ok = True

        def find(x, p=parent, xr=parity):
            r = x
            acc = 0
            while p[r] != r:
                acc ^= xr[r]
                r = p[r]
            res = acc
            while p[x] != x:
                px = p[x]
                xx = xr[x]
                p[x] = r
                xr[x] = acc
                acc ^= xx
                x = px
            return r, res

        for i in range(H):
            row = data[row_start + i]
            left = 0
            rowpar = 0

            for j, ch in enumerate(row):
                if ch == 65:  # 'A'
                    left ^= 1
                    rowpar ^= 1
                    colpref[j] ^= 1
                else:         # 'B'
                    w = 1 ^ colpref[j] ^ left
                    rx, px = find(i)
                    ry, py = find(H + j)

                    if rx == ry:
                        if (px ^ py) != w:
                            ok = False
                            break
                    else:
                        d = px ^ py ^ w
                        if size[rx] < size[ry]:
                            parent[rx] = ry
                            parity[rx] = d
                            size[ry] += size[rx]
                        else:
                            parent[ry] = rx
                            parity[ry] = d
                            size[rx] += size[ry]
                        comp -= 1

            if not ok or rowpar:
                ok = False
                break

        if ok and any(colpref):
            ok = False

        out.append(str(pow(2, comp, MOD)) if ok else "0")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()