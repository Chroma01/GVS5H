import sys

MOD = 998244353


def main():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))

    # Store v_p(A_i) arrays for every occurring prime.
    vals = {}
    for i, x in enumerate(A):
        d = 2
        y = x
        while d * d <= y:
            if y % d == 0:
                c = 0
                while y % d == 0:
                    y //= d
                    c += 1
                if d not in vals:
                    vals[d] = [0] * (N - 1)
                vals[d][i] = c
            d += 1 if d == 2 else 2
        if y > 1:
            if y not in vals:
                vals[y] = [0] * (N - 1)
            vals[y][i] = 1

    answer = 1

    for p, a in vals.items():
        total = sum(a)

        # powp[h] = p^h, the contribution of a vertex of height h.
        powp = [1] * (total + 1)
        for h in range(1, total + 1):
            powp[h] = powp[h - 1] * p % MOD

        # dp0[h]: paths currently at h which have not visited height 0.
        # dp1[h]: paths currently at h which have visited height 0.
        dp0 = [0] * (total + 1)
        dp1 = [0] * (total + 1)

        # Choose e_1. Its vertex weight is p^e_1.
        dp1[0] = 1
        for h in range(1, total + 1):
            dp0[h] = powp[h]

        for d in a:
            ndp0 = [0] * (total + 1)
            ndp1 = [0] * (total + 1)

            if d == 0:
                # Equality is a single transition, not two sign choices.
                for h in range(total + 1):
                    w = powp[h]
                    if dp0[h]:
                        ndp0[h] = dp0[h] * w % MOD
                    if dp1[h]:
                        ndp1[h] = dp1[h] * w % MOD
            else:
                for h in range(total + 1):
                    x0 = dp0[h]
                    x1 = dp1[h]
                    if x0 == 0 and x1 == 0:
                        continue

                    lo = h - d
                    if lo >= 0:
                        w = powp[lo]
                        if lo == 0:
                            if x0:
                                ndp1[lo] = (ndp1[lo] + x0 * w) % MOD
                            if x1:
                                ndp1[lo] = (ndp1[lo] + x1 * w) % MOD
                        else:
                            if x0:
                                ndp0[lo] = (ndp0[lo] + x0 * w) % MOD
                            if x1:
                                ndp1[lo] = (ndp1[lo] + x1 * w) % MOD

                    hi = h + d
                    if hi <= total:
                        w = powp[hi]
                        if x0:
                            ndp0[hi] = (ndp0[hi] + x0 * w) % MOD
                        if x1:
                            ndp1[hi] = (ndp1[hi] + x1 * w) % MOD

            dp0, dp1 = ndp0, ndp1

        contribution = sum(dp1) % MOD
        answer = answer * contribution % MOD

    print(answer)


if __name__ == "__main__":
    main()