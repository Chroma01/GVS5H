import sys

MOD = 998244353


def factorize(x):
    factors = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            factors.append((d, cnt))
        d += 1
    if x > 1:
        factors.append((x, 1))
    return factors


def prime_contribution(p, valuations, n):
    total_height = sum(valuations)
    if total_height == 0:
        return 1

    powers = [1] * (total_height + 1)
    for h in range(1, total_height + 1):
        powers[h] = powers[h - 1] * p % MOD

    # L[k]: weighted paths e_1,...,e_k with e_k = 0
    # and e_1,...,e_{k-1} strictly positive.
    left = [0] * n
    left[0] = 1

    forward = [0] * (total_height + 1)
    for h in range(1, total_height + 1):
        forward[h] = powers[h]

    for edge in range(n - 1):
        d = valuations[edge]
        k = edge + 1
        left[k] = forward[d]

        nxt = [0] * (total_height + 1)
        if d == 0:
            for h in range(1, total_height + 1):
                nxt[h] = forward[h] * powers[h] % MOD
        else:
            for h in range(1, total_height + 1):
                value = 0
                if h >= d:
                    value += forward[h - d]
                if h + d <= total_height:
                    value += forward[h + d]
                nxt[h] = value % MOD * powers[h] % MOD
        forward = nxt

    # right[k]: weighted nonnegative paths e_k,...,e_N with e_k = 0,
    # where the weight excludes e_k itself.
    right = [0] * n
    suffix = [1] * (total_height + 1)
    right[n - 1] = 1

    for edge in range(n - 2, -1, -1):
        d = valuations[edge]
        nxt = [0] * (total_height + 1)

        if d == 0:
            for h in range(total_height + 1):
                nxt[h] = suffix[h] * powers[h] % MOD
        else:
            for h in range(total_height + 1):
                value = 0
                if h + d <= total_height:
                    value += suffix[h + d] * powers[h + d]
                if h >= d:
                    value += suffix[h - d] * powers[h - d]
                nxt[h] = value % MOD

        suffix = nxt
        right[edge] = suffix[0]

    result = 0
    for k in range(n):
        result = (result + left[k] * right[k]) % MOD
    return result


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    valuations_by_prime = {}

    for i, value in enumerate(a):
        for p, exponent in factorize(value):
            if p not in valuations_by_prime:
                valuations_by_prime[p] = [0] * (n - 1)
            valuations_by_prime[p][i] = exponent

    answer = 1
    for p, valuations in valuations_by_prime.items():
        answer = answer * prime_contribution(p, valuations, n) % MOD

    print(answer)


if __name__ == "__main__":
    main()