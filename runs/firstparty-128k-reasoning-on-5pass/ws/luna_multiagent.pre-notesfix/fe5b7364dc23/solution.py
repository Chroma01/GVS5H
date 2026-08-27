import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:2 + n]

    comb = [1] * (k + 1)
    for i in range(1, k + 1):
        comb[i] = comb[i - 1] * (k - i + 1) // i

    moments = [0] * (k + 1)
    moments[0] = 1  # P_0^0
    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for t in range(1, k + 1):
            powers[t] = powers[t - 1] * prefix % MOD

        current = 0
        for t in range(k + 1):
            term = comb[t] * powers[k - t] % MOD
            term = term * moments[t] % MOD
            if t % 2:
                current -= term
            else:
                current += term

        answer = (answer + current) % MOD

        for t in range(k + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(answer % MOD)

if __name__ == "__main__":
    solve()