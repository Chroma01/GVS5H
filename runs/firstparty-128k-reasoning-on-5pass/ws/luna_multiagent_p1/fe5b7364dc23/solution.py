import sys

MOD = 998244353

def main():
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    comb = [1] * (K + 1)
    for t in range(1, K + 1):
        comb[t] = comb[t - 1] * (K - t + 1) // t

    moments = [0] * (K + 1)
    moments[0] = 1  # Prefix sum P_0 = 0, so P_0^0 = 1

    prefix = 0
    answer = 0

    for value in A:
        prefix = (prefix + value) % MOD

        powers = [1] * (K + 1)
        for t in range(1, K + 1):
            powers[t] = powers[t - 1] * prefix % MOD

        contribution = 0
        for t in range(K + 1):
            term = comb[t] * powers[K - t] % MOD
            term = term * moments[t] % MOD
            if t & 1:
                contribution -= term
            else:
                contribution += term

        answer = (answer + contribution) % MOD

        for t in range(K + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(answer % MOD)

if __name__ == "__main__":
    main()