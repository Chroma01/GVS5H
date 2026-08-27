import sys

MOD = 998244353


def find(par, dif, x):
    r = x
    p = 0
    while par[r] != r:
        p ^= dif[r]
        r = par[r]
    res = p
    while par[x] != x:
        px = par[x]
        dx = dif[x]
        par[x] = r
        dif[x] = p
        p ^= dx
        x = px
    return r, res


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    next_tok = it.__next__
    T = int(next_tok())

    out = []
    append = out.append
    find_func = find
    mod = MOD

    for _ in range(T):
        H = int(next_tok())
        W = int(next_tok())

        col_parity = [0] * W
        col_has_B = [0] * W

        parent = None
        size = None
        diff = None

        active_components = 0
        allA_rows = 0
        col_B_count = 0
        allA_cols = 0
        invalid = False

        for i in range(H):
            s = next_tok()
            if invalid:
                continue

            row_parity = 0
            row_has_B = False
            j = 0

            for ch in s:
                if ch == 65:  # 'A'
                    row_parity ^= 1
                    col_parity[j] ^= 1
                else:         # 'B'
                    if not row_has_B:
                        row_has_B = True
                        active_components += 1

                    if not col_has_B[j]:
                        col_has_B[j] = 1
                        active_components += 1
                        col_B_count += 1

                    if parent is None:
                        n = H + W
                        parent = list(range(n))
                        size = [1] * n
                        diff = [0] * n

                    rhs = 1 ^ row_parity ^ col_parity[j]
                    u = i
                    v = H + j

                    ru, pu = find_func(parent, diff, u)
                    rv, pv = find_func(parent, diff, v)

                    if ru == rv:
                        if (pu ^ pv) != rhs:
                            invalid = True
                            break
                    else:
                        d = pu ^ pv ^ rhs
                        if size[ru] < size[rv]:
                            parent[ru] = rv
                            diff[ru] = d
                            size[rv] += size[ru]
                        else:
                            parent[rv] = ru
                            diff[rv] = d
                            size[ru] += size[rv]
                        active_components -= 1

                j += 1

            if invalid:
                continue

            if row_parity:
                invalid = True
                continue

            if not row_has_B:
                allA_rows += 1

        if not invalid:
            if any(col_parity):
                invalid = True
            else:
                allA_cols = W - col_B_count

        if invalid:
            append("0")
        else:
            append(str(pow(2, active_components + allA_rows + allA_cols, mod)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()