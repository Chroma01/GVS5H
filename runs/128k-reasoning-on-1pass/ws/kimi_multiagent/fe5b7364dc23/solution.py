import sys
import math

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n, k = data[0], data[1]
    a = data[2:2 + n]

    # coeff[t] = C(k, t) * (-1)^(k-t) mod MOD
    coeff = [0] * (k + 1)
    for t in range(k + 1):
        c = math.comb(k, t) % MOD
        if (k - t) & 1:
            c = MOD - c
        coeff[t] = c

    # sums[m] = sum of P_j^m over already processed prefixes j < current r
    sums = [0] * (k + 1)
    sums[0] = 1  # empty prefix P_0 = 0 contributes 0^0 = 1

    pref = 0
    ans = 0

    for x in a:
        pref = (pref + x) % MOD

        pw = [1] * (k + 1)
        for t in range(1, k + 1):
            pw[t] = pw[t - 1] * pref % MOD

        add = 0
        for t in range(k + 1):
            add = (add + coeff[t] * pw[t] * sums[k - t]) % MOD
        ans = (ans + add) % MOD

        for t in range(k + 1):
            sums[t] = (sums[t] + pw[t]) % MOD

    print(ans)

if __name__ == "__main__":
    main()