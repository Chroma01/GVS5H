import sys
from collections import defaultdict

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N-1)]

    # Gather all distinct primes that appear in any A_i
    primes = set()
    for a in A:
        x = a
        d = 2
        while d * d <= x:
            if x % d == 0:
                primes.add(d)
                while x % d == 0:
                    x //= d
            d += 1
        if x > 1:
            primes.add(x)

    total = 1
    for p in sorted(primes):
        steps = []
        for idx, a in enumerate(A):
            e = 0
            x = a
            while x % p == 0:
                e += 1
                x //= p
            if e > 0:
                steps.append((idx, e))
        if not steps:
            continue
        M = len(steps)
        pinv = pow(p, MOD-2, MOD)
        # dp[(z, m)] = sum of p^{-sum w_i e_i s_i}
        dp = {(0, 0): 1}
        for orig_idx, e in steps:
            w = N - orig_idx
            pe = pow(p, w * e, MOD)
            inv_pe = pow(p, -w * e % (MOD-1), MOD)  # using Fermat
            new_dp = defaultdict(int)
            for (z, m), val in dp.items():
                # s = +1 (c=1) -> z += e
                z_new = z + e
                m_new = m if m >= z_new else z_new
                new_dp[(z_new, m_new)] = (new_dp[(z_new, m_new)] + val * inv_pe) % MOD
                # s = -1 (c=0) -> z -= e
                z_new = z - e
                m_new = m if m >= z_new else z_new
                new_dp[(z_new, m_new)] = (new_dp[(z_new, m_new)] + val * pe) % MOD
            dp = new_dp
        S_p = 0
        for (z, m), val in dp.items():
            factor = pow(p, N * m, MOD)
            S_p = (S_p + val * factor) % MOD
        total = total * S_p % MOD

    print(total % MOD)

if __name__ == "__main__":
    solve()