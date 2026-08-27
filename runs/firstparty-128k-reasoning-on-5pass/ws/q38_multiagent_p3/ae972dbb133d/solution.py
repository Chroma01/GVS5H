import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    idx = 1
    out = []
    append = out.append

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        n = H + W
        parent = list(range(n))
        size = [1] * n
        parity = [0] * n
        comp = n
        col_ref = [0] * W
        bad = False

        def find(x, parent=parent, parity=parity):
            r = x
            v = 0
            while parent[r] != r:
                v ^= parity[r]
                r = parent[r]
            cur = v
            while x != r:
                p = parent[x]
                px = parity[x]
                parent[x] = r
                parity[x] = cur
                cur ^= px
                x = p
            return r, v

        for i in range(H):
            row = data[idx]
            idx += 1
            if bad:
                continue
            left_ref = 0
            for j, ch in enumerate(row):
                if ch == 66:  # 'B'
                    w = 1 ^ col_ref[j] ^ left_ref
                    ru, pu = find(i)
                    rv, pv = find(H + j)
                    if ru == rv:
                        if (pu ^ pv) != w:
                            bad = True
                            break
                    else:
                        tpar = w ^ pu ^ pv
                        if size[ru] < size[rv]:
                            parent[ru] = rv
                            parity[ru] = tpar
                            size[rv] += size[ru]
                        else:
                            parent[rv] = ru
                            parity[rv] = tpar
                            size[ru] += size[rv]
                        comp -= 1
                else:  # 'A'
                    left_ref ^= 1
                    col_ref[j] ^= 1
            if left_ref != 0:
                bad = True

        if bad:
            append('0')
        else:
            for c in col_ref:
                if c:
                    bad = True
                    break
            if bad:
                append('0')
            else:
                append(str(pow(2, comp, MOD)))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()