import sys

MOD = 998244353
A_BYTE = b'A'


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    T = int(next(it))
    out = []

    for _ in range(T):
        H = int(next(it))
        W = int(next(it))
        rows = [next(it) for __ in range(H)]

        invalid = False
        any_A = False
        any_B = False

        # Row parity of A cells. Also detect all-A / all-B cases cheaply.
        for row in rows:
            cnt = row.count(A_BYTE)
            if cnt & 1:
                invalid = True
                break
            if cnt:
                any_A = True
            if cnt != W:
                any_B = True

        if invalid:
            out.append("0")
            continue

        # All cells are B: only two global patterns (all horizontal / all vertical).
        if not any_A:
            out.append("2")
            continue

        # All cells are A: row parity already implies W is even.
        # Column parity is valid iff H is even.
        if not any_B:
            if H & 1:
                out.append("0")
            else:
                out.append(str(pow(2, H + W, MOD)))
            continue

        # Mixed case: parity DSU on H row bits and W column bits.
        n = H + W
        parent = [-1] * n       # negative size for roots, parent index otherwise
        diff = bytearray(n)     # diff[x] = value[x] xor value[parent[x]]
        comps = n

        def union(x, y, w, parent=parent, diff=diff):
            nonlocal comps

            # find x, with xor to root
            root = x
            px = 0
            while parent[root] >= 0:
                px ^= diff[root]
                root = parent[root]
            rx = root
            resx = px

            # path compression for x
            while parent[x] >= 0:
                nxt = parent[x]
                d = diff[x]
                parent[x] = rx
                diff[x] = px
                px ^= d
                x = nxt

            # find y, with xor to root
            root = y
            py = 0
            while parent[root] >= 0:
                py ^= diff[root]
                root = parent[root]
            ry = root
            resy = py

            # path compression for y
            while parent[y] >= 0:
                nxt = parent[y]
                d = diff[y]
                parent[y] = ry
                diff[y] = py
                py ^= d
                y = nxt

            if rx == ry:
                return (resx ^ resy) == w

            # Enforce value[x] xor value[y] = w.
            t = w ^ resx ^ resy

            # Union by size (parent[root] is negative size).
            if parent[rx] > parent[ry]:  # rx is smaller
                parent[ry] += parent[rx]
                parent[rx] = ry
                diff[rx] = t
            else:
                parent[rx] += parent[ry]
                parent[ry] = rx
                diff[ry] = t

            comps -= 1
            return True

        # col_pref[j] is prefix xor of A above current row during processing,
        # and becomes final column parity after all rows are processed.
        col_pref = bytearray(W)
        ok = True

        for i, row in enumerate(rows):
            row_pref = 0
            base = i
            for j, ch in enumerate(row):
                if ch == 66:  # 'B'
                    label = 1 ^ row_pref ^ col_pref[j]
                    if not union(base, H + j, label):
                        ok = False
                        break
                else:         # 'A'
                    row_pref ^= 1
                    col_pref[j] ^= 1
            if not ok:
                break

        if ok and not any(col_pref):
            out.append(str(pow(2, comps, MOD)))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()