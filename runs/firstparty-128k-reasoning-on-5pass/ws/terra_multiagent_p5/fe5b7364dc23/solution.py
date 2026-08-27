import sys

MOD = 998244353


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    comb = [1] * (k + 1)
    for i in range(1, k + 1):
        comb[i] = comb[i - 1] * (k - i + 1) // i

    # moments[i] = sum of S_j^i over already processed prefix sums S_j.
    # Initially, only S_0 = 0 is included.
    # Thus sum S_j^0 = 1, while all positive powers are 0.
    moments = [0] * (k + 1)
    moments[0] = 1

    prefix = 0
    answer = 0

    for x in a:
        prefix = (prefix + x) % MOD

        powers = [1] * (k + 1)
        for i in range(1, k + 1):
            powers[i] = powers[i - 1] * prefix % MOD

        contribution = 0
        for i in range(k + 1):
            term = comb[i] * powers[k - i] % MOD
            term = term * moments[i] % MOD
            if i & 1:
                contribution -= term
            else:
                contribution += term

        answer = (answer + contribution) % MOD

        for i in range(k + 1):
            moments[i] = (moments[i] + powers[i]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()