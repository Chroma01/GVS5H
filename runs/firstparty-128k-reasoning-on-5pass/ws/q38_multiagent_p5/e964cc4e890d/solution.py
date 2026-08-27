import sys
from itertools import permutations

MOD = 998244353


def brute(N, S):
    if S[0] == 'W' or S[-1] == 'B':
        return 0

    black_pos = [i for i, ch in enumerate(S) if ch == 'B']
    D = [0] * N
    for a in range(1, N + 1):
        if a < N:
            D[a - 1] = black_pos[a] - a
        else:
            D[a - 1] = N - 1

    cnt = 0
    for perm in permutations(range(1, N + 1)):
        mx = 0
        ok = True
        for a in range(N):
            v = perm[a]
            if v > mx:
                mx = v
            if mx <= D[a]:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]

    if S[0] == 'W' or S[-1] == 'B':
        print(0)
        return

    if N <= 8:
        print(brute(N, S))
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # Keep only first occurrences of distinct D values x with L <= x.
    L = []
    X = []
    prev = -1
    b = 0
    for pos, ch in enumerate(S):
        if ch == 'B':
            b += 1
            a = b - 1
            if 1 <= a <= N - 1:
                x = pos - a
                if x != prev:
                    if a <= x:
                        L.append(a)
                        X.append(x)
                    prev = x

    m = len(L)
    if m == 0:
        print(fact[N] % MOD)
        return

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Pack factorial digits in base 2^80 (10 bytes per digit).
    fp = bytearray(10 * (N + 1))
    for k, d in enumerate(fact):
        o = 10 * k
        fp[o] = d & 255
        fp[o + 1] = (d >> 8) & 255
        fp[o + 2] = (d >> 16) & 255
        fp[o + 3] = (d >> 24) & 255
    fact_packed = bytes(fp)
    del fp

    A = [0] * m
    contrib = [0] * m

    SMALL = 64
    DIRECT_LIMIT = 30000
    NZ_DIRECT = 32
    sys.setrecursionlimit(1_000_000)

    def direct_cross(l, mid, r):
        Aloc = A
        Lloc = L
        Xloc = X
        factloc = fact
        contribloc = contrib
        for i in range(mid, r):
            xi = Xloc[i]
            s = 0
            for j in range(l, mid):
                s += Aloc[j] * factloc[xi - Lloc[j]]
            contribloc[i] += s

    def big_cross(l, mid, r):
        Aloc = A
        Lloc = L
        Xloc = X
        factloc = fact
        contribloc = contrib

        a = Lloc[l]
        nF = Lloc[mid - 1] - a + 1
        glen = Xloc[r - 1] - a + 1

        # If only few left coefficients are non-zero, direct is faster.
        small = []
        nz = 0
        for j in range(l, mid):
            d = Aloc[j]
            if d:
                nz += 1
                if nz <= NZ_DIRECT:
                    small.append((d, Lloc[j]))
                else:
                    break

        if nz == 0:
            return

        if nz <= NZ_DIRECT:
            for i in range(mid, r):
                xi = Xloc[i]
                s = 0
                for d, Lj in small:
                    s += d * factloc[xi - Lj]
                contribloc[i] += s
            return

        # Big-integer convolution in base 2^80.
        ba = bytearray(10 * nF)
        for j in range(l, mid):
            d = Aloc[j]
            if d:
                o = 10 * (Lloc[j] - a)
                ba[o] = d & 255
                ba[o + 1] = (d >> 8) & 255
                ba[o + 2] = (d >> 16) & 255
                ba[o + 3] = (d >> 24) & 255

        F = int.from_bytes(ba, 'little')
        del ba

        G = int.from_bytes(fact_packed[:10 * glen], 'little')
        prod = F * G
        buf = prod.to_bytes(10 * (nF + glen), 'little')
        del F, G, prod

        for i in range(mid, r):
            o = 10 * (Xloc[i] - a)
            c = (buf[o] | (buf[o + 1] << 8) | (buf[o + 2] << 16) | (buf[o + 3] << 24) |
                 (buf[o + 4] << 32) | (buf[o + 5] << 40) | (buf[o + 6] << 48) |
                 (buf[o + 7] << 56) | (buf[o + 8] << 64) | (buf[o + 9] << 72))
            contribloc[i] += c

    def cdq(l, r):
        if r - l <= SMALL:
            Aloc = A
            Lloc = L
            Xloc = X
            factloc = fact
            invloc = invfact
            contribloc = contrib
            MODloc = MOD

            for i in range(l, r):
                xi = Xloc[i]
                s = 0
                for j in range(l, i):
                    s += Aloc[j] * factloc[xi - Lloc[j]]
                contribloc[i] += s
                val = (factloc[xi] + contribloc[i]) % MODloc
                Aloc[i] = (-val * invloc[xi - Lloc[i]]) % MODloc
            return

        mid = (l + r) >> 1
        cdq(l, mid)

        left_len = mid - l
        right_len = r - mid
        if left_len * right_len <= DIRECT_LIMIT:
            direct_cross(l, mid, r)
        else:
            big_cross(l, mid, r)

        cdq(mid, r)

    cdq(0, m)

    ans = fact[N]
    total = 0
    for i in range(m):
        total += A[i] * fact[N - L[i]]
    print((ans + total) % MOD)


if __name__ == "__main__":
    solve()