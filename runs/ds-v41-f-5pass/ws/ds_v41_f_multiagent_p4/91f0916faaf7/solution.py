import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    m = n - 1
    A = data[1:1 + m]

    # smallest prime factor sieve up to 1000
    MAXA = 1000
    spf = list(range(MAXA + 1))
    i = 2
    while i * i <= MAXA:
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    # collect, for each prime, the vector e_i = v_p(A_i)
    exps = {}
    for idx in range(m):
        x = int(A[idx])
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            lst = exps.get(p)
            if lst is None:
                lst = [0] * m
                exps[p] = lst
            lst[idx] = c

    try:
        import numpy as np
        HAVE_NP = True
    except Exception:
        HAVE_NP = False

    ans = 1
    for p, e in exps.items():
        S = 0
        for v in e:
            S += v
        pw = [1] * (S + 1)
        for h in range(1, S + 1):
            pw[h] = pw[h - 1] * p % MOD

        if HAVE_NP and (S + 1) >= 256:
            L = S + 1
            npw = np.array(pw, dtype=np.int64)
            T = npw.copy()          # all nonneg walks
            U = npw.copy()          # walks that never visited 0
            U[0] = 0
            for ei in e:
                if ei == 0:
                    T = T * npw % MOD
                    U = U * npw % MOD
                else:
                    upT = np.zeros(L, dtype=np.int64)
                    upT[ei:] = T[:L - ei]
                    dnT = np.zeros(L, dtype=np.int64)
                    dnT[:L - ei] = T[ei:]
                    T = (upT + dnT) * npw % MOD

                    upU = np.zeros(L, dtype=np.int64)
                    upU[ei:] = U[:L - ei]
                    dnU = np.zeros(L, dtype=np.int64)
                    dnU[:L - ei] = U[ei:]
                    U = (upU + dnU) * npw % MOD
                    U[0] = 0
            F = (int(T.sum() % MOD) - int(U.sum() % MOD)) % MOD
        else:
            # run-length optimization on zero steps (pure python)
            nz = [j for j in range(m) if e[j]]
            lead = nz[0]
            k = lead + 1
            if k == 1:
                T = pw[:]
            else:
                T = [pow(w, k, MOD) for w in pw]
            U = T[:]
            U[0] = 0
            prev = nz[0]
            first = True
            for j in nz:
                if not first:
                    gap = j - prev - 1
                    if gap == 1:
                        T = [a * w % MOD for a, w in zip(T, pw)]
                        U = [a * w % MOD for a, w in zip(U, pw)]
                    elif gap > 1:
                        sc = [pow(w, gap, MOD) for w in pw]
                        T = [a * w % MOD for a, w in zip(T, sc)]
                        U = [a * w % MOD for a, w in zip(U, sc)]
                prev = j
                first = False
                val = e[j]
                upT = [0] * val + T[:S + 1 - val]
                dnT = T[val:] + [0] * val
                T = [(a + b) * w % MOD for a, b, w in zip(upT, dnT, pw)]
                upU = [0] * val + U[:S + 1 - val]
                dnU = U[val:] + [0] * val
                U = [(a + b) * w % MOD for a, b, w in zip(upU, dnU, pw)]
                U[0] = 0
            trail = m - 1 - nz[-1]
            if trail == 1:
                T = [a * w % MOD for a, w in zip(T, pw)]
                U = [a * w % MOD for a, w in zip(U, pw)]
            elif trail > 1:
                sc = [pow(w, trail, MOD) for w in pw]
                T = [a * w % MOD for a, w in zip(T, sc)]
                U = [a * w % MOD for a, w in zip(U, sc)]
            F = (sum(T) - sum(U)) % MOD

        ans = ans * F % MOD

    print(ans % MOD)

main()