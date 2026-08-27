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


def solve_prime(p, steps):
    m = len(steps)
    total = sum(steps)

    powers = [1] * (total + 1)
    for i in range(1, total + 1):
        powers[i] = powers[i - 1] * p % MOD

    # not_seen_zero[h], seen_zero[h]:
    # weighted sums of walks currently at height h.
    not_seen = [0] * (total + 1)
    seen = [0] * (total + 1)
    seen[0] = 1
    for h in range(1, total + 1):
        not_seen[h] = powers[h]

    length = total + 1

    for d in steps:
        nxt_not = [0] * length
        nxt_seen = [0] * length

        if d == 0:
            for h in range(length):
                w = powers[h]
                nxt_not[h] = not_seen[h] * w % MOD
                nxt_seen[h] = seen[h] * w % MOD
        else:
            for h in range(length):
                a = not_seen[h]
                b = seen[h]

                lo = h - d
                if lo >= 0:
                    w = powers[lo]
                    if lo == 0:
                        nxt_seen[0] = (nxt_seen[0] + (a + b) * w) % MOD
                    else:
                        nxt_not[lo] = (nxt_not[lo] + a * w) % MOD
                        nxt_seen[lo] = (nxt_seen[lo] + b * w) % MOD

                hi = h + d
                if hi <= total:
                    w = powers[hi]
                    nxt_not[hi] = (nxt_not[hi] + a * w) % MOD
                    nxt_seen[hi] = (nxt_seen[hi] + b * w) % MOD

        not_seen = nxt_not
        seen = nxt_seen

    return sum(seen) % MOD


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    prime_steps = {}
    for i, x in enumerate(a):
        for p, e in factorize(x):
            if p not in prime_steps:
                prime_steps[p] = [0] * (n - 1)
            prime_steps[p][i] = e

    ans = 1
    for p, steps in prime_steps.items():
        ans = ans * solve_prime(p, steps) % MOD

    print(ans)


if __name__ == "__main__":
    main()