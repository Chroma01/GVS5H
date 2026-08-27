import sys

MOD = 998244353


def factorize(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res


def solve_prime(p, edges):
    n = len(edges) + 1
    total = sum(edges)

    pw = [1] * (total + 1)
    for i in range(1, total + 1):
        pw[i] = pw[i - 1] * p % MOD

    # pref[j] is the weighted sum of walks whose first zero is at position j.
    pref = [0] * n
    pref[0] = 1

    # dp[x - 1] is the weighted sum of positive walks ending at exponent x,
    # with no zero encountered so far.
    dp = pw[1:].copy()

    for i, a in enumerate(edges):
        # A transition from exponent a to zero gives the first zero here.
        # The source state exponent a is stored at dp[a - 1].
        if a > 0:
            pref[i + 1] = dp[a - 1]

        ndp = [0] * total
        if a == 0:
            for x in range(1, total + 1):
                ndp[x - 1] = dp[x - 1] * pw[x] % MOD
        else:
            for y in range(1, total + 1):
                value = 0

                x = y - a
                if x >= 1:
                    value += dp[x - 1]

                x = y + a
                if x <= total:
                    value += dp[x - 1]

                ndp[y - 1] = value % MOD * pw[y] % MOD

        dp = ndp

    # suf[j] is the weighted sum of all nonnegative suffix walks
    # starting from exponent zero at position j.
    suf = [0] * n
    q = pw[:]
    suf[n - 1] = 1

    for i in range(n - 2, -1, -1):
        a = edges[i]
        nq = [0] * (total + 1)

        if a == 0:
            for x in range(total + 1):
                nq[x] = pw[x] * q[x] % MOD
        else:
            for x in range(total + 1):
                value = 0

                y = x - a
                if y >= 0:
                    value += q[y]

                y = x + a
                if y <= total:
                    value += q[y]

                nq[x] = value % MOD * pw[x] % MOD

        q = nq
        suf[i] = q[0]

    answer = 0
    for i in range(n):
        answer = (answer + pref[i] * suf[i]) % MOD

    return answer


def main():
    input = sys.stdin.readline

    n = int(input())
    values = list(map(int, input().split()))

    prime_edges = {}

    for i, value in enumerate(values):
        for p, exponent in factorize(value).items():
            if p not in prime_edges:
                prime_edges[p] = [0] * (n - 1)
            prime_edges[p][i] = exponent

    answer = 1
    for p, edges in prime_edges.items():
        answer = answer * solve_prime(p, edges) % MOD

    print(answer)


if __name__ == "__main__":
    main()