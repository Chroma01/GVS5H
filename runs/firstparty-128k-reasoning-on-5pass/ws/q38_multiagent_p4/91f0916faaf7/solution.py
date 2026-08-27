import sys
import math

MOD = 998244353


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N - 1]
    m = N - 1

    if m == 0:
        print(1)
        return

    max_val = max(A)

    # Smallest prime factor sieve up to max(A)
    spf = list(range(max_val + 1))
    if max_val >= 1:
        spf[1] = 1
    for i in range(2, math.isqrt(max_val) + 1):
        if spf[i] == i:
            for j in range(i * i, max_val + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # factors[p][i] = v_p(A_i)
    factors = {}
    max_a_global = 0

    for idx, val in enumerate(A):
        x = val
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1

            if p not in factors:
                factors[p] = [0] * m
            factors[p][idx] = cnt

            if cnt > max_a_global:
                max_a_global = cnt

    if not factors:
        print(1)
        return

    # Enough for both height factors p^h and minimum-shift factors p^{i*(a-h)}.
    global_max_exp = m * max_a_global
    mod = MOD
    ans = 1

    for p, arr in factors.items():
        # Powers of p up to the maximum exponent that can appear in one transition.
        powp = [1] * (global_max_exp + 1)
        for i in range(1, global_max_exp + 1):
            powp[i] = (powp[i - 1] * p) % mod

        # dp[h] for current prefix:
        # h = B_i - min(B_1..B_i), weight is p^{sum of heights relative to current prefix min}.
        dp = [1]
        limit = 0  # maximum possible h, equal to sum of processed a's

        pp = powp

        for idx, a in enumerate(arr):
            if a == 0:
                # Height unchanged, but the new element contributes p^h.
                if limit:
                    dp = [v * pp[h] % mod for h, v in enumerate(dp)]
            else:
                step_no = idx + 1  # number of previous elements
                new_limit = limit + a
                ndp = [0] * (new_limit + 1)

                # h < a: down move creates a new prefix minimum.
                end1 = a - 1
                if end1 > limit:
                    end1 = limit

                for h in range(end1 + 1):
                    val = dp[h]
                    if val:
                        # Up move.
                        ndp[h + a] += val * pp[h + a]
                        # Down move: prefix minimum drops by (a - h).
                        ndp[0] += val * pp[step_no * (a - h)]

                # h >= a: down move does not change the prefix minimum.
                if limit >= a:
                    for h in range(a, limit + 1):
                        val = dp[h]
                        if val:
                            # Up move.
                            ndp[h + a] += val * pp[h + a]
                            # Down move.
                            ndp[h - a] += val * pp[h - a]

                dp = [x % mod for x in ndp]
                limit = new_limit

        ans = (ans * (sum(dp) % mod)) % mod

    print(ans)


if __name__ == "__main__":
    main()