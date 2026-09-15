import sys


def solve():
    MOD = 998244353
    A = 65  # ord('A')

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

        rows = []
        col_parity = [0] * W
        cp = col_parity

        row_ok = True
        has_a = False
        has_b = False

        # First pass: row/column parity checks and all-A/all-B detection.
        for _ in range(H):
            s = data[idx]
            idx += 1
            rows.append(s)

            p = 0
            for j, ch in enumerate(s):
                if ch == A:
                    has_a = True
                    p ^= 1
                    cp[j] ^= 1
                else:
                    has_b = True

            if p:
                row_ok = False

        if not row_ok or any(col_parity):
            out.append("0")
            continue

        # No B tiles: every row bit and column bit is free.
        if not has_b:
            out.append(str(pow(2, H + W, MOD)))
            continue

        # No A tiles: complete bipartite constraint graph, one connected component.
        if not has_a:
            out.append("2")
            continue

        n = H + W
        parent = list(range(n))
        size = [1] * n
        parity = [0] * n  # parity[x] = value[x] xor value[parent[x]]

        col_pref = [0] * W
        cp = col_pref

        comp = n
        bad = False
        H_local = H

        # Second pass: maintain prefix parities and add XOR constraints for B cells.
        for i, s in enumerate(rows):
            rp = 0
            rv = i

            for j, ch in enumerate(s):
                if ch == A:
                    rp ^= 1
                    cp[j] ^= 1
                else:
                    w = 1 ^ rp ^ cp[j]

                    # find x = row vertex i
                    x = rv
                    root = x
                    acc = 0
                    while parent[root] != root:
                        acc ^= parity[root]
                        root = parent[root]
                    px = acc
                    while parent[x] != x:
                        nxt = parent[x]
                        p = parity[x]
                        parent[x] = root
                        parity[x] = acc
                        acc ^= p
                        x = nxt
                    rx = root

                    # find y = column vertex H + j
                    y = H_local + j
                    root = y
                    acc = 0
                    while parent[root] != root:
                        acc ^= parity[root]
                        root = parent[root]
                    py = acc
                    while parent[y] != y:
                        nxt = parent[y]
                        p = parity[y]
                        parent[y] = root
                        parity[y] = acc
                        acc ^= p
                        y = nxt
                    ry = root

                    if rx == ry:
                        if (px ^ py) != w:
                            bad = True
                            break
                    else:
                        d = w ^ px ^ py
                        if size[rx] < size[ry]:
                            parent[rx] = ry
                            parity[rx] = d
                            size[ry] += size[rx]
                        else:
                            parent[ry] = rx
                            parity[ry] = d
                            size[rx] += size[ry]
                        comp -= 1

            if bad:
                break

        if bad:
            out.append("0")
        else:
            out.append(str(pow(2, comp, MOD)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()