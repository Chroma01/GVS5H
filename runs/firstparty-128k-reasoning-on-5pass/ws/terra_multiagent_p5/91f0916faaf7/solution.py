import sys

MOD = 998244353


def solve():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    M = N - 1

    prime_exp = {}

    for i, x in enumerate(A):
        d = 2
        while d * d <= x:
            if x % d == 0:
                if d not in prime_exp:
                    prime_exp[d] = [0] * M
                cnt = 0
                while x % d == 0:
                    x //= d
                    cnt += 1
                prime_exp[d][i] = cnt
            d += 1 if d == 2 else 2
        if x > 1:
            if x not in prime_exp:
                prime_exp[x] = [0] * M
            prime_exp[x][i] = 1

    answer = 1

    for p, inc in prime_exp.items():
        D = sum(inc)

        pw = [1] * (D + 1)
        for h in range(1, D + 1):
            pw[h] = pw[h - 1] * p % MOD

        # dp0[h]: weighted walks currently at h that have not visited height 0.
        # dp1[h]: weighted walks currently at h that have visited height 0.
        dp0 = [0] * (D + 1)
        dp1 = [0] * (D + 1)

        dp1[0] = 1
        for h in range(1, D + 1):
            dp0[h] = pw[h]

        for a in inc:
            ndp0 = [0] * (D + 1)
            ndp1 = [0] * (D + 1)

            if a == 0:
                for h in range(D + 1):
                    w = pw[h]
                    if dp0[h]:
                        ndp0[h] = dp0[h] * w % MOD
                    if dp1[h]:
                        ndp1[h] = dp1[h] * w % MOD
            else:
                for h in range(D + 1):
                    v0 = dp0[h]
                    v1 = dp1[h]
                    if v0 == 0 and v1 == 0:
                        continue

                    t = h - a
                    if t >= 0:
                        w = pw[t]
                        if t == 0:
                            ndp1[t] = (ndp1[t] + (v0 + v1) * w) % MOD
                        else:
                            if v0:
                                ndp0[t] = (ndp0[t] + v0 * w) % MOD
                            if v1:
                                ndp1[t] = (ndp1[t] + v1 * w) % MOD

                    t = h + a
                    if t <= D:
                        w = pw[t]
                        if t == 0:
                            ndp1[t] = (ndp1[t] + (v0 + v1) * w) % MOD
                        else:
                            if v0:
                                ndp0[t] = (ndp0[t] + v0 * w) % MOD
                            if v1:
                                ndp1[t] = (ndp1[t] + v1 * w) % MOD

            dp0, dp1 = ndp0, ndp1

        ways_for_prime = sum(dp1) % MOD
        answer = answer * ways_for_prime % MOD

    print(answer)


if __name__ == "__main__":
    solve()