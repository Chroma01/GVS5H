import sys

M = 998244353

try:
    import numpy as np
    HAVE_NP = True
except Exception:
    HAVE_NP = False


if HAVE_NP:
    def powvec(q, n):
        """array [q^0, q^1, ..., q^{n-1}] mod M, built by doubling (O(n) element ops)"""
        q = int(q) % M
        res = np.ones(1, dtype=np.int64)
        while res.shape[0] < n:
            k = res.shape[0]
            f = pow(q, k, M)
            res = np.concatenate([res, res * f % M])
        return res[:n].copy()

    def solve_prime(p, a):
        """a = list of v_p(A_i); returns T_p = sum over valid exponent seqs of p^{sum e_i}"""
        tot = sum(a)
        if tot == 0:
            return 1
        L = tot + 1
        pw = powvec(p % M, L)              # p^s for s = 0..tot
        v = np.ones(1, dtype=np.int64)     # state r = 0 with weight 1
        t = 0                              # pending zero-steps (lazy)
        for i, ai in enumerate(a, 1):
            if ai == 0:
                t += 1
                continue
            cur = v.shape[0]
            if t:
                q = pow(p, t, M)
                v = v * powvec(q, cur) % M
                t = 0
            nl = cur + ai
            nv = np.zeros(nl, dtype=np.int64)
            nv[ai:] = v                                  # r -> r + ai
            if cur > ai:                                 # r -> r - ai (no new minimum)
                nv[:cur - ai] = (nv[:cur - ai] + v[ai:]) % M
            nv = nv * pw[:nl] % M                        # each new element adds p^{r'}
            # reflection: new minimum reached (r < ai), drop delta = ai - r,
            # all i already-placed elements gain delta each
            pj = pow(p, i, M)
            lim = ai if ai < cur else cur
            extra = 0
            vl = v[:lim].tolist()
            for r in range(lim):
                if vl[r]:
                    extra = (extra + vl[r] * pow(pj, ai - r, M)) % M
            if extra:
                nv[0] = (int(nv[0]) + extra) % M
            v = nv
        if t:
            q = pow(p, t, M)
            v = v * powvec(q, v.shape[0]) % M
        return int(v.sum() % M)

else:
    def solve_prime(p, a):
        tot = sum(a)
        if tot == 0:
            return 1
        pw = [1] * (tot + 1)
        for s in range(1, tot + 1):
            pw[s] = pw[s - 1] * p % M
        v = [1]
        t = 0
        for i, ai in enumerate(a, 1):
            if ai == 0:
                t += 1
                continue
            if t:
                q = pow(p, t, M)
                f = 1
                for s in range(len(v)):
                    if s:
                        f = f * q % M
                    v[s] = v[s] * f % M
                t = 0
            cur = len(v)
            nl = cur + ai
            nv = [0] * nl
            for s in range(nl):
                x = v[s - ai] if s >= ai else 0
                if s + ai < cur:
                    x += v[s + ai]
                nv[s] = x % M * pw[s] % M
            pj = pow(p, i, M)
            lim = ai if ai < cur else cur
            extra = 0
            for r in range(lim):
                if v[r]:
                    extra = (extra + v[r] * pow(pj, ai - r, M)) % M
            nv[0] = (nv[0] + extra) % M
            v = nv
        if t:
            q = pow(p, t, M)
            f = 1
            for s in range(len(v)):
                if s:
                    f = f * q % M
                v[s] = v[s] * f % M
        return sum(v) % M


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + (n - 1)]]

    LIM = 1001
    spf = list(range(LIM))
    i = 2
    while i * i < LIM:
        if spf[i] == i:
            for j in range(i * i, LIM, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    facs = []
    primes = set()
    for x in A:
        d = {}
        y = x
        while y > 1:
            pp = spf[y]
            c = 0
            while y % pp == 0:
                y //= pp
                c += 1
            d[pp] = c
            primes.add(pp)
        facs.append(d)

    if not primes:
        print(1)
        return

    ans = 1
    for p in sorted(primes):
        arr = [d.get(p, 0) for d in facs]
        ans = ans * solve_prime(p, arr) % M
    print(ans % M)


main()