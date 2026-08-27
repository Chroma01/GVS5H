```python
import sys
import math

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, K = data[0], data[1]
    A = data[2:]

    coeff = [0] * (K + 1)
    for t in range(K + 1):
        c = math.comb(K, t) % MOD
        if (K - t) & 1:
            c = (-c) % MOD
        coeff[t] = c

    sums = [0] * (K + 1)  # sums[a] = sum of previous prefix^a
    ans = 0
    pref = 0

    for i in range(N + 1):
        if i:
            pref = (pref + A[i - 1]) % MOD

        pw = [1] * (K + 1)
        cur = 1
        for t in range(K + 1):
            pw[t] = cur
            cur = cur * pref % MOD

        add = 0
        for t in range(K + 1):
            add = (add + coeff[t] * pw[t] * sums[K - t]) % MOD
        ans = (ans + add) % MOD

        for t in range(K + 1):
            sums[t] = (sums[t] + pw[t]) % MOD

    print(ans)

main()
```