import sys

MOD = 998244353


def factorize(x):
    result = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            e = 0
            while x % d == 0:
                x //= d
                e += 1
            result.append((d, e))
        d += 1 if d == 2 else 2
    if x > 1:
        result.append((x, 1))
    return result


def contribution_for_prime(p, exponents, n):
    total_exp = sum(exponents)
    max_power_index = n * 9
    powers = [1] * (max_power_index + 1)
    for i in range(1, max_power_index + 1):
        powers[i] = powers[i - 1] * p % MOD

    dp = [0] * (total_exp + 1)
    dp[0] = 1
    current_max = 0

    for edge in range(n - 1):
        e = exponents[edge]
        ndp = [0] * (total_exp + 1)

        if e == 0:
            for h in range(current_max + 1):
                value = dp[h]
                if value:
                    ndp[h] = value * powers[h] % MOD
        else:
            for h in range(current_max + 1):
                value = dp[h]
                if not value:
                    continue

                nh = h + e
                ndp[nh] = (ndp[nh] + value * powers[nh]) % MOD

                if h >= e:
                    nh = h - e
                    ndp[nh] = (ndp[nh] + value * powers[nh]) % MOD
                else:
                    shift = e - h
                    multiplier = powers[shift * (edge + 1)]
                    ndp[0] = (ndp[0] + value * multiplier) % MOD

            current_max += e

        dp = ndp

    return sum(dp) % MOD


def main():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    prime_exponents = {}

    for i, value in enumerate(a):
        for p, e in factorize(value):
            if p not in prime_exponents:
                prime_exponents[p] = [0] * (n - 1)
            prime_exponents[p][i] = e

    answer = 1
    for p, exponents in prime_exponents.items():
        answer = answer * contribution_for_prime(p, exponents, n) % MOD

    print(answer)


if __name__ == "__main__":
    main()