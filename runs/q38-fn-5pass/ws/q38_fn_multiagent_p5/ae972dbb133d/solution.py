import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    A_INT = 65
    A_BYTE = b'A'

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        grid_start = idx
        idx += H

        colA = [0] * W
        row_ok = True
        b_count = 0

        # Check row parity and column parity of A cells.
        for i in range(H):
            row = data[grid_start + i]
            ac = row.count(A_BYTE)
            if ac & 1:
                row_ok = False
                break
            b_count += W - ac
            for j, ch in enumerate(row):
                if ch == A_INT:
                    colA[j] ^= 1

        if not row_ok or any(colA):
            out.append("0")
            continue

        # If there are no B cells, only the independent row/column cycles remain.
        if b_count == 0:
            out.append(str(pow(2, H + W, MOD)))
            continue

        n = H + W
        parent = list(range(n))
        size = [1] * n
        parity = [0] * n
        comps = n

        def find(x, parent=parent, parity=parity):
            r = x
            xr = 0
            while parent[r] != r:
                xr ^= parity[r]
                r = parent[r]

            res = xr
            while parent[x] != x:
                p = parent[x]
                px = parity[x]
                parent[x] = r
                parity[x] = xr
                xr ^= px
                x = p

            return r, res

        colPref = [0] * W
        ok = True

        par = parent
        sz = size
        parit = parity
        find_local = find
        Hloc = H

        # Process B-cell equations:
        # R_i xor C_j = 1 xor colPref[j] xor rowPref(i, j+1)
        for i in range(Hloc):
            row = data[grid_start + i]
            rowPref = 0

            for j, ch in enumerate(row):
                if ch == A_INT:
                    rowPref ^= 1
                    colPref[j] ^= 1
                else:
                    val = 1 ^ colPref[j] ^ rowPref
                    a = i
                    b = Hloc + j

                    ra, pa = find_local(a)
                    rb, pb = find_local(b)

                    if ra == rb:
                        if (pa ^ pb) != val:
                            ok = False
                            break
                    else:
                        tpar = pa ^ pb ^ val
                        if sz[ra] < sz[rb]:
                            par[ra] = rb
                            parit[ra] = tpar
                            sz[rb] += sz[ra]
                        else:
                            par[rb] = ra
                            parit[rb] = tpar
                            sz[ra] += sz[rb]
                        comps -= 1

            if not ok:
                break

        if ok:
            out.append(str(pow(2, comps, MOD)))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()