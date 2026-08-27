import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))

    # Since H,W >= 2, H+W <= H*W <= 10^6.
    pow2 = [1] * 1_000_001
    for i in range(1, len(pow2)):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = []

    for _ in range(t):
        h = int(next(it))
        w = int(next(it))
        n = h + w

        parent = list(range(n))
        size = [1] * n
        xr = [0] * n  # xor value from vertex to its parent
        components = n
        consistent = True

        def find(x):
            total = 0
            y = x
            while parent[y] != y:
                total ^= xr[y]
                y = parent[y]
            root = y

            y = x
            before = 0
            while parent[y] != y:
                nxt = parent[y]
                d = xr[y]
                parent[y] = root
                xr[y] = total ^ before
                before ^= d
                y = nxt

            return root, total

        def unite(u, v, val):
            nonlocal components
            ru, xu = find(u)
            rv, xv = find(v)

            if ru == rv:
                return (xu ^ xv) == val

            if size[ru] > size[rv]:
                ru, rv = rv, ru
                xu, xv = xv, xu

            # x_ru xor x_rv must equal val xor xu xor xv.
            parent[ru] = rv
            xr[ru] = val ^ xu ^ xv
            size[rv] += size[ru]
            components -= 1
            return True

        # vertical_prefix[j] = XOR of A cells in column j from row 0 through current row
        vertical_prefix = [0] * w

        for i in range(h):
            s = next(it)
            horizontal_prefix = 0

            for j in range(w):
                if s[j] == 65:  # 'A'
                    horizontal_prefix ^= 1
                    vertical_prefix[j] ^= 1
                else:  # 'B'
                    # h[i][j] = row_seed[i] xor horizontal_prefix
                    # v[i][j] = col_seed[j] xor vertical_prefix[j]
                    # Type B requires h[i][j] xor v[i][j] = 1.
                    label = 1 ^ horizontal_prefix ^ vertical_prefix[j]
                    if not unite(i, h + j, label):
                        consistent = False

            # Cyclic horizontal consistency requires even number of A cells in every row.
            if horizontal_prefix:
                consistent = False

        # Cyclic vertical consistency requires even number of A cells in every column.
        if any(vertical_prefix):
            consistent = False

        if consistent:
            ans.append(str(pow2[components]))
        else:
            ans.append("0")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()