import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:2 + n]

    comb = [1] * (k + 1)
    for j in range(1, k + 1):
        comb[j] = comb[j - 1] * (k - j + 1) // j

    moments = [0] * (k + 1)
    moments[0] = 1  # P_0 = 0, so 0^0 is treated as 1

    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for power in range(1, k + 1):
            powers[power] = powers[power - 1] * prefix % MOD

        contribution = 0
        for j in range(k + 1):
            term = comb[j] * powers[k - j] % MOD
            term = term * moments[j] % MOD
            if j & 1:
                contribution -= term
            else:
                contribution += term

        answer = (answer + contribution) % MOD

        for j in range(k + 1):
            moments[j] = (moments[j] + powers[j]) % MOD

    print(answer % MOD)

if __name__ == "__main__":
    solve()