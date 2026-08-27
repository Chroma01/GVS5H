import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    mod = 998244353
    A = 65  # ord('A')

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        n = H + W
        parent = list(range(n))
        size = [1] * n
        parity = [0] * n
        comps = n
        col_pref = [0] * W
        bad = False

        def find(x, parent=parent, parity=parity):
            r = x
            acc = 0
            while True:
                p = parent[r]
                if p == r:
                    break
                acc ^= parity[r]
                r = p
            total = acc

            while True:
                p = parent[x]
                if p == x:
                    break
                px = parity[x]
                parent[x] = r
                parity[x] = acc
                acc ^= px
                x = p

            return r, total

        f = find
        par = parent
        sz = size
        parit = parity
        cp = col_pref
        base = H

        for i in range(H):
            row = data[idx]
            idx += 1

            if bad:
                continue

            if row.count(b'A') & 1:
                bad = True
                continue

            row_pref = 0
            for j, c in enumerate(row):
                if c == A:
                    row_pref ^= 1
                    cp[j] ^= 1
                else:
                    w = 1 ^ row_pref ^ cp[j]
                    ru, pu = f(i)
                    rv, pv = f(base + j)

                    if ru == rv:
                        if (pu ^ pv) != w:
                            bad = True
                            break
                    else:
                        if sz[ru] < sz[rv]:
                            par[ru] = rv
                            parit[ru] = pu ^ pv ^ w
                            sz[rv] += sz[ru]
                        else:
                            par[rv] = ru
                            parit[rv] = pu ^ pv ^ w
                            sz[ru] += sz[rv]
                        comps -= 1

        if not bad and any(cp):
            bad = True

        if bad:
            append("0")
        else:
            append(str(pow(2, comps, mod)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()