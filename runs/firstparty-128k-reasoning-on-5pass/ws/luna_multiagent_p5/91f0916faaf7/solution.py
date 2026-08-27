import sys

MOD = 998244353


def factorize(x):
    result = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            result[d] = result.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        result[x] = result.get(x, 0) + 1
    return result


def prime_contribution(p, ds):
    total = sum(ds)
    max_shift = max((i * d for i, d in enumerate(ds, 1)), default=0)
    max_power = max(total, max_shift)

    powers = [1] * (max_power + 1)
    for i in range(1, max_power + 1):
        powers[i] = powers[i - 1] * p % MOD

    dp = [0] * (total + 1)
    dp[0] = 1
    current_max = 0

    for i, d in enumerate(ds, 1):
        ndp = [0] * (total + 1)

        if d == 0:
            for h in range(current_max + 1):
                value = dp[h]
                if value:
                    ndp[h] = value * powers[h] % MOD
        else:
            crossing = 0

            upper = min(d - 1, current_max)
            for h in range(upper + 1):
                value = dp[h]
                if not value:
                    continue

                ndp[h + d] = (
                    ndp[h + d] + value * powers[h + d]
                ) % MOD

                crossing = (
                    crossing + value * powers[i * (d - h)]
                ) % MOD

            if crossing:
                ndp[0] = crossing

            start = d
            if start <= current_max:
                for h in range(start, current_max + 1):
                    value = dp[h]
                    if not value:
                        continue

                    ndp[h + d] = (
                        ndp[h + d] + value * powers[h + d]
                    ) % MOD
                    ndp[h - d] = (
                        ndp[h - d] + value * powers[h - d]
                    ) % MOD

        dp = ndp
        current_max += d

    return sum(dp) % MOD


def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    edge_factors = [factorize(x) for x in a]
    primes = set()
    for factors in edge_factors:
        primes.update(factors)

    answer = 1

    for p in primes:
        ds = [factors.get(p, 0) for factors in edge_factors]
        answer = answer * prime_contribution(p, ds) % MOD

    print(answer)


if __name__ == "__main__":
    solve()