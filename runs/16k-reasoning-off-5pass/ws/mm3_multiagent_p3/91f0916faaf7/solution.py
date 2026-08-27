import sys
sys.setrecursionlimit(1 << 25)
MOD = 998244353

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    # factor each A_i
    # precompute smallest prime factor up to 1000
    maxA = max(A) if A else 0
    limit = 1000
    spf = list(range(limit + 1))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    # gather exponents per prime
    prime_exps = {}  # prime -> list of length N-1
    for idx, val in enumerate(A):
        factors = {}
        x = val
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            factors[p] = cnt
        for p, e in factors.items():
            if p not in prime_exps:
                prime_exps[p] = [0] * (N - 1)
            prime_exps[p][idx] = e
    # function to compute F_p for a given list of exponents e[0..N-2]
    def compute_F(e_list):
        S = sum(e_list)
        if S == 0:
            return 1  # exponent must be 0 always
        Vmax = 2 * S
        p = prime  # captured from outer scope
        # precompute p^v
        powp = [1] * (Vmax + 1)
        for i in range(1, Vmax + 1):
            powp[i] = powp[i - 1] * p % MOD
        # dp[v][z] : z=0 not visited zero, z=1 visited zero
        # we can keep two separate arrays for visited/not visited
        # initialise for i=1 (position 1)
        size = Vmax + 1
        dp0 = [0] * size  # not visited
        dp1 = [0] * size  # visited
        for v in range(S + 1):
            if v == 0:
                dp1[v] = powp[v]  # visited
            else:
                dp0[v] = powp[v]  # not visited
        # iterate over edges
        for e in e_list:
            ndp0 = [0] * size
            ndp1 = [0] * size
            for v in range(size):
                # not visited
                val0 = dp0[v]
                if val0:
                    # add
                    v2 = v + e
                    if v2 <= Vmax:
                        if v2 == 0:
                            ndp1[v2] = (ndp1[v2] + val0 * powp[v2]) % MOD
                        else:
                            ndp0[v2] = (ndp0[v2] + val0 * powp[v2]) % MOD
                    # subtract
                    if v >= e:
                        v2 = v - e
                        if v2 == 0:
                            ndp1[v2] = (ndp1[v2] + val0 * powp[v2]) % MOD
                        else:
                            ndp0[v2] = (ndp0[v2] + val0 * powp[v2]) % MOD
                # visited
                val1 = dp1[v]
                if val1:
                    # add
                    v2 = v + e
                    if v2 <= Vmax:
                        if v2 == 0:
                            ndp1[v2] = (ndp1[v2] + val1 * powp[v2]) % MOD
                        else:
                            ndp1[v2] = (ndp1[v2] + val1 * powp[v2]) % MOD
                    # subtract
                    if v >= e:
                        v2 = v - e
                        if v2 == 0:
                            ndp1[v2] = (ndp1[v2] + val1 * powp[v2]) % MOD
                        else:
                            ndp1[v2] = (ndp1[v2] + val1 * powp[v2]) % MOD
            dp0, dp1 = ndp0, ndp1
        # sum over visited states
        total = sum(dp1) % MOD
        return total

    ans = 1
    for prime, e_list in prime_exps.items():
        Fp = compute_F(e_list)
        ans = ans * Fp % MOD
    print(ans)

if __name__ == "__main__":
    solve()