import sys

MOD = 998244353


def prime_factorization(x):
    factors = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            e = 0
            while x % d == 0:
                x //= d
                e += 1
            factors.append((d, e))
        d += 1
    if x > 1:
        factors.append((x, 1))
    return factors


def prime_contribution(p, exponents, n):
    total = sum(exponents)
    pw = [1] * (total + 1)
    for i in range(1, total + 1):
        pw[i] = pw[i - 1] * p % MOD

    # not_touched[h]: normalized height h, and zero has not appeared yet
    # touched[h]: normalized height h, and zero has appeared
    not_touched = [0] * (total + 1)
    touched = [0] * (total + 1)

    for h in range(total + 1):
        if h == 0:
            touched[h] = pw[h]
        else:
            not_touched[h] = pw[h]

    for e in exponents:
        next_not = [0] * (total + 1)
        next_touched = [0] * (total + 1)

        if e == 0:
            for h in range(total + 1):
                a = not_touched[h]
                b = touched[h]
                if a:
                    next_not[h] = (next_not[h] + a * pw[h]) % MOD
                if b:
                    next_touched[h] = (next_touched[h] + b * pw[h]) % MOD
        else:
            for h in range(total + 1):
                a = not_touched[h]
                b = touched[h]

                if a:
                    nh = h - e
                    if nh >= 0:
                        val = a * pw[nh] % MOD
                        if nh == 0:
                            next_touched[nh] = (next_touched[nh] + val) % MOD
                        else:
                            next_not[nh] = (next_not[nh] + val) % MOD

                    nh = h + e
                    if nh <= total:
                        val = a * pw[nh] % MOD
                        next_not[nh] = (next_not[nh] + val) % MOD

                if b:
                    nh = h - e
                    if nh >= 0:
                        next_touched[nh] = (
                            next_touched[nh] + b * pw[nh]
                        ) % MOD

                    nh = h + e
                    if nh <= total:
                        next_touched[nh] = (
                            next_touched[nh] + b * pw[nh]
                        ) % MOD

        not_touched, touched = next_not, next_touched

    return sum(touched) % MOD


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    prime_exponents = {}

    for i, value in enumerate(a):
        for p, e in prime_factorization(value):
            if p not in prime_exponents:
                prime_exponents[p] = [0] * (n - 1)
            prime_exponents[p][i] = e

    answer = 1
    for p, exponents in prime_exponents.items():
        answer = answer * prime_contribution(p, exponents, n) % MOD

    print(answer)


if __name__ == "__main__":
    solve()