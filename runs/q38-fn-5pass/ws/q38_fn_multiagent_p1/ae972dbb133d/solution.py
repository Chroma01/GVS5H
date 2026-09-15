import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    parent = []
    parity = []

    def find(x):
        p = parent
        par = parity

        px = p[x]
        if px == x:
            return x
        if p[px] == px:
            return px

        r = x
        acc = 0
        while p[r] != r:
            acc ^= par[r]
            r = p[r]

        cur = x
        prefix = 0
        while p[cur] != cur:
            nxt = p[cur]
            edge = par[cur]
            p[cur] = r
            par[cur] = acc ^ prefix
            prefix ^= edge
            cur = nxt

        return r

    A = 65  # ord('A')

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        n = H + W
        parent = list(range(n))
        parity = [0] * n
        rank = [0] * n
        comps = n

        col_pref = [0] * W
        bad = False

        p = parent
        par = parity
        rk = rank
        cp = col_pref
        HH = H
        f = find

        for i in range(HH):
            row = data[idx]
            idx += 1

            row_pref = 0
            row_node = i

            for j, ch in enumerate(row):
                if ch == A:
                    row_pref ^= 1
                    cp[j] ^= 1
                else:
                    label = 1 ^ row_pref ^ cp[j]
                    col_node = HH + j

                    ra = f(row_node)
                    pa = par[row_node]
                    rb = f(col_node)
                    pb = par[col_node]

                    if ra == rb:
                        if (pa ^ pb) != label:
                            bad = True
                            break
                    else:
                        x = label ^ pa ^ pb
                        if rk[ra] < rk[rb]:
                            p[ra] = rb
                            par[ra] = x
                        elif rk[ra] > rk[rb]:
                            p[rb] = ra
                            par[rb] = x
                        else:
                            p[rb] = ra
                            par[rb] = x
                            rk[ra] += 1
                        comps -= 1

            if bad:
                idx += HH - i - 1
                break

            if row_pref != 0:
                bad = True
                idx += HH - i - 1
                break

        if not bad and any(cp):
            bad = True

        if bad:
            out.append("0")
        else:
            out.append(str(pow(2, comps, MOD)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()