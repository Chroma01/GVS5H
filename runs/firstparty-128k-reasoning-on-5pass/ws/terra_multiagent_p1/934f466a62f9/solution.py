import sys


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    t = next(it)
    ans = []

    NEG = -(10 ** 30)

    for _ in range(t):
        n = next(it)
        k = next(it)
        m = 2 * k

        cakes = []
        for idx in range(n):
            x = next(it)
            y = next(it)
            z = next(it)
            v = max(x, y, z)
            cakes.append((v, x, y, z, idx))

        cakes.sort(reverse=True)
        base = cakes[:m]
        outside = cakes[m:]

        # At most two cakes need to be exchanged with cakes outside the base.
        # For each final label, retain the best two possible outside candidates.
        ext_indices = set()
        for d in range(3):
            best = sorted(outside, key=lambda a: a[d + 1], reverse=True)[:2]
            for cake in best:
                ext_indices.add(cake[4])

        ext = [cake for cake in outside if cake[4] in ext_indices]

        # dp[q][mask]:
        # maximum value after processing base cakes,
        # excluding exactly q of them, with label parity mask.
        dp = [[NEG] * 8 for _ in range(3)]
        dp[0][0] = 0

        for _, x, y, z, _ in base:
            vals = (x, y, z)
            ndp = [[NEG] * 8 for _ in range(3)]

            for q in range(3):
                for mask in range(8):
                    cur = dp[q][mask]
                    if cur == NEG:
                        continue

                    # Keep this cake and assign one of three labels.
                    for d in range(3):
                        nm = mask ^ (1 << d)
                        nv = cur + vals[d]
                        if nv > ndp[q][nm]:
                            ndp[q][nm] = nv

                    # Exclude this base cake.
                    if q < 2 and cur > ndp[q + 1][mask]:
                        ndp[q + 1][mask] = cur

            dp = ndp

        # edp[r][mask]:
        # maximum value by selecting exactly r outside candidates.
        edp = [[NEG] * 8 for _ in range(3)]
        edp[0][0] = 0

        for _, x, y, z, _ in ext:
            vals = (x, y, z)
            nedp = [row[:] for row in edp]

            for r in range(2):
                for mask in range(8):
                    cur = edp[r][mask]
                    if cur == NEG:
                        continue
                    for d in range(3):
                        nm = mask ^ (1 << d)
                        nv = cur + vals[d]
                        if nv > nedp[r + 1][nm]:
                            nedp[r + 1][nm] = nv

            edp = nedp

        best_answer = NEG
        for q in range(3):
            for mask in range(8):
                a = dp[q][mask]
                b = edp[q][mask]
                if a != NEG and b != NEG:
                    best_answer = max(best_answer, a + b)

        ans.append(str(best_answer))

    print("\n".join(ans))


if __name__ == "__main__":
    solve()