import sys

MOD = 998244353
MAX_A = 1000


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:]
    L = N - 1

    # Smallest prime factor up to 1000.
    spf = list(range(MAX_A + 1))
    for i in range(2, int(MAX_A ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAX_A + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # exps[p][i] = v_p(A_i)
    exps = {}
    for i, x in enumerate(A):
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            if p not in exps:
                exps[p] = [0] * L
            exps[p][i] = cnt

    ans = 1

    for p, arr in exps.items():
        M = sum(arr)
        if M == 0:
            continue

        # powp[h] = p^h mod MOD
        powp = [1] * (M + 1)
        for h in range(1, M + 1):
            powp[h] = (powp[h - 1] * p) % MOD

        # dp0[h]: weight of walks ending at height h, never touched 0.
        # dp1[h]: weight of walks ending at height h, already touched 0.
        dp0 = [0] * (M + 1)
        dp1 = [0] * (M + 1)

        dp1[0] = 1
        for h in range(1, M + 1):
            dp0[h] = powp[h]

        i = 0
        while i < L:
            a = arr[i]

            # Consecutive zero steps keep the height unchanged, but each
            # position still contributes p^height. A run of length r multiplies
            # height h by p^(r*h).
            if a == 0:
                j = i + 1
                while j < L and arr[j] == 0:
                    j += 1
                run = j - i

                base = pow(p, run, MOD)
                cur = 1
                d0 = dp0
                d1 = dp1
                mod = MOD

                for h in range(M + 1):
                    if d0[h]:
                        d0[h] = (d0[h] * cur) % mod
                    if d1[h]:
                        d1[h] = (d1[h] * cur) % mod
                    cur = (cur * base) % mod

                i = j
                continue

            ndp0 = [0] * (M + 1)
            ndp1 = [0] * (M + 1)

            d0 = dp0
            d1 = dp1
            n0 = ndp0
            n1 = ndp1
            pp = powp
            MM = M
            aa = a

            for h in range(MM + 1):
                v0 = d0[h]
                v1 = d1[h]
                if not (v0 or v1):
                    continue

                # Move up: h -> h + a
                nh = h + aa
                if nh <= MM:
                    w = pp[nh]
                    if v0:
                        n0[nh] += v0 * w
                    if v1:
                        n1[nh] += v1 * w

                # Move down: h -> h - a
                nh = h - aa
                if nh >= 0:
                    if nh == 0:
                        # Touching zero makes untouched paths touched.
                        n1[0] += v0 + v1
                    else:
                        w = pp[nh]
                        if v0:
                            n0[nh] += v0 * w
                        if v1:
                            n1[nh] += v1 * w

            mod = MOD
            dp0 = [x % mod for x in ndp0]
            dp1 = [x % mod for x in ndp1]
            i += 1

        contrib = sum(dp1) % MOD
        ans = (ans * contrib) % MOD

    print(ans)


if __name__ == "__main__":
    solve()