import sys
from math import comb

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + N]))

    # coef[t] = C(K, t) * (-1)^t mod MOD
    coef = [0] * (K + 1)
    for t in range(K + 1):
        c = comb(K, t) % MOD
        coef[t] = c if t % 2 == 0 else (-c) % MOD

    # S[t] = sum_{i=0}^{j-1} P_i^t
    S = [0] * (K + 1)
    S[0] = 1  # P_0 = 0, and 0^0 is treated as 1 for the binomial term

    ans = 0
    pref = 0

    for a in A:
        pref = (pref + a) % MOD

        # powers of the current prefix sum
        pw = [1] * (K + 1)
        for t in range(1, K + 1):
            pw[t] = pw[t - 1] * pref % MOD

        # add all subarrays ending at this position
        for t in range(K + 1):
            ans = (ans + coef[t] * pw[K - t] % MOD * S[t]) % MOD

        # now include the current prefix sum for future right endpoints
        for t in range(K + 1):
            S[t] = (S[t] + pw[t]) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    main()