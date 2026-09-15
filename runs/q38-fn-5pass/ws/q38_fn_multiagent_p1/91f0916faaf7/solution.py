import sys

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:]
    m = N - 1

    maxA = max(A) if A else 1
    spf = list(range(maxA + 1))
    if maxA >= 1:
        spf[1] = 1

    i = 2
    while i * i <= maxA:
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    exps = {}
    for idx, a in enumerate(A):
        x = a
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            if p not in exps:
                exps[p] = [0] * m
            exps[p][idx] = c

    ans = 1
    mod = MOD

    for p, e in exps.items():
        E = sum(e)
        if E == 0:
            continue

        powp = [1] * (E + 1)
        for h in range(1, E + 1):
            powp[h] = (powp[h - 1] * p) % mod
        pw = powp

        # suff[k] = weighted sum of nonnegative suffixes starting at k with height 0
        suff = [0] * (N + 1)
        cap = E
        dp = pw[:]  # dp for position N: dp[h] = p^h
        suff[N] = 1

        for i in range(N - 1, 0, -1):
            step = e[i - 1]

            if step == 0:
                for h in range(1, cap + 1):
                    dp[h] = (dp[h] * pw[h]) % mod
                suff[i] = dp[0]
                continue

            cap -= step
            new = [0] * (cap + 1)

            if cap < step:
                for h in range(cap + 1):
                    val = dp[h + step]
                    new[h] = (val * pw[h]) % mod
            else:
                for h in range(step):
                    val = dp[h + step]
                    new[h] = (val * pw[h]) % mod
                for h in range(step, cap + 1):
                    val = dp[h + step] + dp[h - step]
                    if val >= mod:
                        val -= mod
                    new[h] = (val * pw[h]) % mod

            dp = new
            suff[i] = dp[0]

        # Prefix DP: positive prefixes.
        # pos[h] = weighted sum of strictly positive prefixes ending at current position with height h.
        cap = E
        pos = [0] * (E + 1)
        for h in range(1, E + 1):
            pos[h] = pw[h]

        # First zero at position 1: empty prefix.
        total = suff[1]

        for k in range(2, N + 1):
            step = e[k - 2]

            if step:
                pref = pos[step]
                total = (total + pref * suff[k]) % mod

            if k == N:
                break

            if step == 0:
                for h in range(1, cap + 1):
                    pos[h] = (pos[h] * pw[h]) % mod
                continue

            cap -= step
            new = [0] * (cap + 1)

            if cap < step:
                for h in range(1, cap + 1):
                    val = pos[h + step]
                    new[h] = (val * pw[h]) % mod
            else:
                # For h <= step, previous height h-step is <= 0, which is forbidden.
                for h in range(1, step + 1):
                    val = pos[h + step]
                    new[h] = (val * pw[h]) % mod
                for h in range(step + 1, cap + 1):
                    val = pos[h + step] + pos[h - step]
                    if val >= mod:
                        val -= mod
                    new[h] = (val * pw[h]) % mod

            pos = new

        ans = (ans * total) % mod

    print(ans)


if __name__ == "__main__":
    solve()