import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n - 1]))

    # SPF sieve up to 1000
    LIM = 1000
    spf = list(range(LIM + 1))
    for i in range(2, int(LIM ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, LIM + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # prime -> per-edge exponent array (length n-1)
    primes = {}
    for idx, a in enumerate(A):
        x = a
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            if p not in primes:
                primes[p] = [0] * (n - 1)
            primes[p][idx] = c

    ans = 1
    for p, exps in primes.items():
        a_max = max(exps)
        A_p = sum(exps)
        L = max(A_p, (n - 1) * a_max)
        pw = [1] * (L + 1)
        for k in range(1, L + 1):
            pw[k] = pw[k - 1] * p % MOD

        dp = [0] * (A_p + 1)
        dp[0] = 1
        cur_max = 0
        for j in range(1, n):  # edge j (1-indexed); positions so far = j
            a = exps[j - 1]
            dp2 = [0] * (A_p + 1)
            if a == 0:
                for d in range(cur_max + 1):
                    v = dp[d]
                    if v:
                        dp2[d] = (dp2[d] + v * pw[d]) % MOD
                new_max = cur_max
            else:
                for d in range(cur_max + 1):
                    v = dp[d]
                    if not v:
                        continue
                    # up step: P gets p^a
                    nd = d + a
                    dp2[nd] = (dp2[nd] + v * pw[nd]) % MOD
                    # down step: Q gets p^a
                    if d >= a:
                        nd = d - a
                        dp2[nd] = (dp2[nd] + v * pw[nd]) % MOD
                    else:
                        delta = a - d
                        dp2[0] = (dp2[0] + v * pw[j * delta]) % MOD
                new_max = cur_max + a
            dp = dp2
            cur_max = new_max
        S = sum(dp) % MOD
        ans = ans * S % MOD

    print(ans)

main()