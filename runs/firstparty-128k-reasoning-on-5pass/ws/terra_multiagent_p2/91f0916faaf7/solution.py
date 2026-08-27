import sys

MOD = 998244353


def factorize(x):
    res = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            c = 0
            while x % d == 0:
                x //= d
                c += 1
            res.append((d, c))
        d += 1 if d == 2 else 2
    if x > 1:
        res.append((x, 1))
    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a_values = data[1:]

    prime_steps = {}
    for i, x in enumerate(a_values):
        for p, e in factorize(x):
            if p not in prime_steps:
                prime_steps[p] = [0] * (n - 1)
            prime_steps[p][i] = e

    answer = 1

    for p, steps in prime_steps.items():
        h_max = sum(steps)

        powers = [1] * (h_max + 1)
        for h in range(1, h_max + 1):
            powers[h] = powers[h - 1] * p % MOD

        # all_dp[h]: weighted paths currently at height h, never below zero.
        # nozero_dp[h]: same, but paths that have never visited height zero.
        all_dp = powers[:]
        nozero_dp = powers[:]
        nozero_dp[0] = 0

        for d in steps:
            if d == 0:
                next_all = [0] * (h_max + 1)
                next_nozero = [0] * (h_max + 1)
                for h in range(h_max + 1):
                    next_all[h] = all_dp[h] * powers[h] % MOD
                for h in range(1, h_max + 1):
                    next_nozero[h] = nozero_dp[h] * powers[h] % MOD
            else:
                next_all = [0] * (h_max + 1)
                next_nozero = [0] * (h_max + 1)

                for h in range(h_max + 1):
                    v = 0
                    if h >= d:
                        v += all_dp[h - d]
                    if h + d <= h_max:
                        v += all_dp[h + d]
                    next_all[h] = (v % MOD) * powers[h] % MOD

                for h in range(1, h_max + 1):
                    v = 0
                    if h >= d:
                        v += nozero_dp[h - d]
                    if h + d <= h_max:
                        v += nozero_dp[h + d]
                    next_nozero[h] = (v % MOD) * powers[h] % MOD

            all_dp = next_all
            nozero_dp = next_nozero

        contribution = (sum(all_dp) - sum(nozero_dp)) % MOD
        answer = answer * contribution % MOD

    print(answer)


if __name__ == "__main__":
    main()