import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    comb = [1] * (k + 1)
    for t in range(1, k + 1):
        comb[t] = comb[t - 1] * (k - t + 1) % MOD
        comb[t] = comb[t] * pow(t, MOD - 2, MOD) % MOD

    moments = [0] * (k + 1)
    moments[0] = 1  # Prefix sum S_0 = 0 is already present.

    prefix = 0
    ans = 0

    for x in a:
        prefix = (prefix + x) % MOD

        powers = [1] * (k + 1)
        for t in range(1, k + 1):
            powers[t] = powers[t - 1] * prefix % MOD

        contribution = 0
        for t in range(k + 1):
            term = comb[t] * powers[k - t] % MOD
            term = term * moments[t] % MOD
            if t & 1:
                contribution -= term
            else:
                contribution += term

        ans = (ans + contribution) % MOD

        for t in range(k + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()