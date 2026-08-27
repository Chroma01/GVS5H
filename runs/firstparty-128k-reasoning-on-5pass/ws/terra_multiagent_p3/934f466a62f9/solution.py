import sys


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    t = next(it)
    out = []
    NEG = -10**30

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = []
        for _ in range(n):
            x = next(it)
            y = next(it)
            z = next(it)
            cakes.append((max(x, y, z), x, y, z))

        cakes.sort(reverse=True)
        base = cakes[:2 * k]
        extra = cakes[2 * k:]

        # dp_base[omitted][parity]
        dp_base = [[NEG] * 8 for _ in range(3)]
        dp_base[0][0] = 0

        for _, x, y, z in base:
            ndp = [[NEG] * 8 for _ in range(3)]
            vals = (x, y, z)
            for omitted in range(3):
                row = dp_base[omitted]
                for mask in range(8):
                    cur = row[mask]
                    if cur == NEG:
                        continue

                    if omitted < 2 and cur > ndp[omitted + 1][mask]:
                        ndp[omitted + 1][mask] = cur

                    for d in range(3):
                        nm = mask ^ (1 << d)
                        nv = cur + vals[d]
                        if nv > ndp[omitted][nm]:
                            ndp[omitted][nm] = nv
            dp_base = ndp

        # dp_extra[taken][parity]
        dp_extra = [[NEG] * 8 for _ in range(3)]
        dp_extra[0][0] = 0

        for _, x, y, z in extra:
            ndp = [row[:] for row in dp_extra]  # Skip this cake.
            vals = (x, y, z)
            for taken in range(2):
                row = dp_extra[taken]
                for mask in range(8):
                    cur = row[mask]
                    if cur == NEG:
                        continue
                    for d in range(3):
                        nm = mask ^ (1 << d)
                        nv = cur + vals[d]
                        if nv > ndp[taken + 1][nm]:
                            ndp[taken + 1][nm] = nv
            dp_extra = ndp

        ans = NEG
        for changed in range(3):
            for mask in range(8):
                v = dp_base[changed][mask] + dp_extra[changed][mask]
                if v > ans:
                    ans = v
        out.append(str(ans))

    print("\n".join(out))


if __name__ == "__main__":
    solve()