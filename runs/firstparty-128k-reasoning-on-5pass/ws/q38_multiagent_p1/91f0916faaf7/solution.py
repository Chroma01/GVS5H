import sys
from math import gcd

MOD = 998244353


def apply_zero(T, P, powB, W, zero, B, mod):
    if zero == 1:
        for h in range(1, W + 1):
            T[h] = (T[h] * powB[h]) % mod
            P[h] = (P[h] * powB[h]) % mod
    else:
        f = pow(B, zero, mod)
        mult = 1
        for h in range(1, W + 1):
            mult = (mult * f) % mod
            T[h] = (T[h] * mult) % mod
            P[h] = (P[h] * mult) % mod


def step(T, P, powB, W, a, mod):
    newT = [0] * (W + 1)
    newP = [0] * (W + 1)
    R = W - a

    if a <= R:
        newT[0] = T[a]

        for h in range(1, a):
            ph = powB[h]
            newT[h] = (T[h + a] * ph) % mod
            newP[h] = (P[h + a] * ph) % mod

        for h in range(a, R + 1):
            sT = T[h - a] + T[h + a]
            if sT >= mod:
                sT -= mod
            sP = P[h - a] + P[h + a]
            if sP >= mod:
                sP -= mod
            ph = powB[h]
            newT[h] = (sT * ph) % mod
            newP[h] = (sP * ph) % mod

        for h in range(R + 1, W + 1):
            ph = powB[h]
            newT[h] = (T[h - a] * ph) % mod
            newP[h] = (P[h - a] * ph) % mod
    else:
        newT[0] = T[a]

        for h in range(1, R + 1):
            ph = powB[h]
            newT[h] = (T[h + a] * ph) % mod
            newP[h] = (P[h + a] * ph) % mod

        for h in range(a, W + 1):
            ph = powB[h]
            newT[h] = (T[h - a] * ph) % mod
            newP[h] = (P[h - a] * ph) % mod

    return newT, newP


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:]

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    facs = []
    prime_set = set()

    for a in A:
        x = a
        fac = {}
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                cnt = 0
                while x % p == 0:
                    x //= p
                    cnt += 1
                fac[p] = cnt
                prime_set.add(p)
        if x > 1:
            fac[x] = fac.get(x, 0) + 1
            prime_set.add(x)
        facs.append(fac)

    ans = 1
    mod = MOD

    for p in sorted(prime_set):
        e = [0] * (N - 1)
        W = 0
        g = 0

        for i, fac in enumerate(facs):
            c = fac.get(p, 0)
            e[i] = c
            W += c
            g = gcd(g, c)

        if W == 0:
            continue

        if g > 1:
            W //= g
            B = pow(p, g, mod)
            for i in range(len(e)):
                e[i] //= g
        else:
            B = p % mod

        powB = [1] * (W + 1)
        for i in range(1, W + 1):
            powB[i] = (powB[i - 1] * B) % mod

        T = powB[:]
        P = [0] * (W + 1)
        if W >= 1:
            P[1:] = powB[1:]

        zero = 0
        for a in e:
            if a == 0:
                zero += 1
            else:
                if zero:
                    apply_zero(T, P, powB, W, zero, B, mod)
                    zero = 0
                T, P = step(T, P, powB, W, a, mod)

        if zero:
            apply_zero(T, P, powB, W, zero, B, mod)

        fp = (sum(T) - sum(P)) % mod
        ans = (ans * fp) % mod

    print(ans)


if __name__ == "__main__":
    main()