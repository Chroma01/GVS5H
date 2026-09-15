import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:1 + N - 1]))
    m = N - 1

    # prime_exps[p][i] = v_p(A_i)
    prime_exps = defaultdict(lambda: [0] * m)
    for idx, val in enumerate(A):
        x = val
        d = 2
        while d * d <= x:
            if x % d == 0:
                cnt = 0
                while x % d == 0:
                    x //= d
                    cnt += 1
                prime_exps[d][idx] = cnt
            d += 1
        if x > 1:
            prime_exps[x][idx] = 1

    ans = 1

    for p, a in prime_exps.items():
        R = sum(a)
        if R == 0:
            continue

        powp = [1] * (R + 1)
        for h in range(1, R + 1):
            powp[h] = (powp[h - 1] * p) % MOD

        # dp0[h]: minimum of exponents so far > 0, current exponent = h
        # dp1[h]: minimum of exponents so far == 0, current exponent = h
        dp0 = [0] * (R + 1)
        dp1 = [0] * (R + 1)
        dp1[0] = 1
        for h in range(1, R + 1):
            dp0[h] = powp[h]

        for d in a:
            if d == 0:
                # exponent stays the same
                for h in range(1, R + 1):
                    f = powp[h]
                    dp0[h] = (dp0[h] * f) % MOD
                    dp1[h] = (dp1[h] * f) % MOD
            else:
                ndp0 = [0] * (R + 1)
                ndp1 = [0] * (R + 1)
                for h in range(R + 1):
                    v0 = dp0[h]
                    v1 = dp1[h]
                    if v0 == 0 and v1 == 0:
                        continue

                    # go up: h2 = h + d
                    h2 = h + d
                    if h2 <= R:
                        f = powp[h2]
                        ndp0[h2] += v0 * f
                        ndp1[h2] += v1 * f

                    # go down: h2 = h - d
                    h2 = h - d
                    if h2 >= 0:
                        f = powp[h2]
                        if h2 == 0:
                            ndp1[0] += (v0 + v1) * f
                        else:
                            ndp0[h2] += v0 * f
                            ndp1[h2] += v1 * f

                for i in range(R + 1):
                    ndp0[i] %= MOD
                    ndp1[i] %= MOD
                dp0 = ndp0
                dp1 = ndp1

        W = sum(dp1) % MOD
        ans = (ans * W) % MOD

    print(ans)

if __name__ == "__main__":
    main()