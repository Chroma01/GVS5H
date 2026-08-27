```python
import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:]

    maxA = max(A) if A else 1
    spf = list(range(maxA + 1))
    r = int(maxA ** 0.5)
    for i in range(2, r + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    occ = {}
    for idx, x in enumerate(A):
        y = x
        while y > 1:
            p = spf[y]
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            occ.setdefault(p, []).append((idx, e))

    ans = 1

    for p, lst in occ.items():
        step = [0] * (N - 1)
        H = 0
        for idx, e in lst:
            step[idx] = e
            H += e
        if H == 0:
            continue

        powp = [1] * (H + 1)
        for i in range(1, H + 1):
            powp[i] = powp[i - 1] * p % MOD

        dp0 = [0] * (H + 1)  # not touched height 0 yet
        dp1 = [0] * (H + 1)  # already touched height 0
        for h in range(1, H + 1):
            dp0[h] = powp[h]
        dp1[0] = 1

        for a in step:
            ndp0 = [0] * (H + 1)
            ndp1 = [0] * (H + 1)
            if a == 0:
                for h in range(H + 1):
                    w = powp[h]
                    if dp0[h]:
                        ndp0[h] = dp0[h] * w % MOD
                    if dp1[h]:
                        ndp1[h] = dp1[h] * w % MOD
            else:
                for h in range(H + 1):
                    v0 = dp0[h]
                    v1 = dp1[h]
                    if v0 == 0 and v1 == 0:
                        continue

                    nh = h - a
                    if nh >= 0:
                        w = powp[nh]
                        if v0:
                            add = v0 * w % MOD
                            if nh == 0:
                                x = ndp1[0] + add
                                if x >= MOD:
                                    x -= MOD
                                ndp1[0] = x
                            else:
                                x = ndp0[nh] + add
                                if x >= MOD:
                                    x -= MOD
                                ndp0[nh] = x
                        if v1:
                            add = v1 * w % MOD
                            x = ndp1[nh] + add
                            if x >= MOD:
                                x -= MOD
                            ndp1[nh] = x

                    nh = h + a
                    if nh <= H:
                        w = powp[nh]
                        if v0:
                            add = v0 * w % MOD
                            x = ndp0[nh] + add
                            if x >= MOD:
                                x -= MOD
                            ndp0[nh] = x
                        if v1:
                            add = v1 * w % MOD
                            x = ndp1[nh] + add
                            if x >= MOD:
                                x -= MOD
                            ndp1[nh] = x

            dp0, dp1 = ndp0, ndp1

        f = sum(dp1) % MOD
        ans = ans * f % MOD

    print(ans)

if __name__ == "__main__":
    main()
```