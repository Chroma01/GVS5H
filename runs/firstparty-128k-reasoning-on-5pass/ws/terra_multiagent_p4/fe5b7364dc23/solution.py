import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:]

    comb = [0] * (k + 1)
    comb[0] = 1
    for t in range(1, k + 1):
        comb[t] = comb[t - 1] * (k - t + 1) // t

    coef = [comb[t] % MOD for t in range(k + 1)]
    for t in range(1, k + 1, 2):
        coef[t] = (-coef[t]) % MOD

    prefix_power_sum = [0] * (k + 1)
    prefix_power_sum[0] = 1  # S_0^0

    prefix = 0
    answer = 0

    for x in a:
        prefix = (prefix + x) % MOD

        powers = [1] * (k + 1)
        for e in range(1, k + 1):
            powers[e] = powers[e - 1] * prefix % MOD

        contribution = 0
        for t in range(k + 1):
            contribution += coef[t] * powers[k - t] % MOD * prefix_power_sum[t]
        answer = (answer + contribution) % MOD

        for t in range(k + 1):
            prefix_power_sum[t] = (prefix_power_sum[t] + powers[t]) % MOD

    print(answer)

if __name__ == "__main__":
    main()