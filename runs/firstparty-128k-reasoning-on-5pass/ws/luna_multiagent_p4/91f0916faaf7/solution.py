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
        d += 1
    if x > 1:
        result.append((x, 1))
    return result


def prime_contribution(p, exponents, n):
    total_exp = sum(exponents)

    powers = [1] * (total_exp + 1)
    for i in range(1, total_exp + 1):
        powers[i] = powers[i - 1] * p % MOD

    # dp[y] is the total weight of normalized walks whose
    # current normalized height is y.
    dp = [0] * (total_exp + 1)
    dp[0] = 1
    current_max = 0

    for position, e in enumerate(exponents, start=1):
        nxt = [0] * (total_exp + 1)

        if e == 0:
            for y in range(current_max + 1):
                if dp[y]:
                    nxt[y] = dp[y] * powers[y] % MOD
            dp = nxt
            continue

        for y in range(current_max + 1):
            w = dp[y]
            if not w:
                continue

            # Positive signed difference: new height is y + e.
            z = y + e
            nxt[z] = (nxt[z] + w * powers[z]) % MOD

            # Negative signed difference: new raw height is y - e.
            if y >= e:
                z = y - e
                nxt[z] = (nxt[z] + w * powers[z]) % MOD
            else:
                # A new minimum is reached. The previous position
                # heights are all shifted upward by e - y.
                shift = e - y
                factor = pow(p, position * shift, MOD)
                nxt[0] = (nxt[0] + w * factor) % MOD

        dp = nxt
        current_max += e

    return sum(dp[:current_max + 1]) % MOD


def solve():
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
        answer = answer * prime_contribution(p, exponents, n) % MOD

    print(answer)


if __name__ == "__main__":
    solve()