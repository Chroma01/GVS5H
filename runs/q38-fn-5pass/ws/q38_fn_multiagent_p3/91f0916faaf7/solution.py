import sys
from math import gcd

MOD = 998244353


def factorize(x):
    res = []
    if x % 2 == 0:
        c = 0
        while x % 2 == 0:
            x //= 2
            c += 1
        res.append((2, c))
    d = 3
    while d * d <= x:
        if x % d == 0:
            c = 0
            while x % d == 0:
                x //= d
                c += 1
            res.append((d, c))
        d += 2
    if x > 1:
        res.append((x, 1))
    return res


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    L = N - 1
    A = data[1:1 + L]

    prime_steps = {}
    for idx, val in enumerate(A):
        for p, c in factorize(val):
            lst = prime_steps.get(p)
            if lst is None:
                lst = [0] * L
                prime_steps[p] = lst
            lst[idx] = c

    mod = MOD
    ans = 1

    for p, steps in prime_steps.items():
        g = 0
        M = 0
        for a in steps:
            if a:
                M += a
                if g == 0:
                    g = a
                else:
                    g = gcd(g, a)

        if M == 0:
            continue

        if g > 1:
            q = pow(p, g, mod)
            for j in range(L):
                if steps[j]:
                    steps[j] //= g
            M //= g
        else:
            q = p % mod

        powq = [1] * (M + 1)
        for i in range(1, M + 1):
            powq[i] = powq[i - 1] * q % mod

        touched = [0] * (M + 1)
        touched[0] = 1
        untouched = [0] + powq[1:]

        tq = touched
        uq = untouched
        pw = powq

        max_t = 0
        max_u = M
        rem = M

        i = 0
        while i < L:
            a = steps[i]

            if a == 0:
                z = 0
                while i < L and steps[i] == 0:
                    z += 1
                    i += 1

                if max_t == 0 and max_u == 0:
                    continue

                if z == 1:
                    for e in range(max_t + 1):
                        v = tq[e]
                        if v:
                            tq[e] = v * pw[e] % mod
                    for e in range(1, max_u + 1):
                        v = uq[e]
                        if v:
                            uq[e] = v * pw[e] % mod
                else:
                    if z == 2:
                        factor = q * q % mod
                    else:
                        factor = pow(q, z, mod)

                    if factor == 1:
                        continue

                    cur = 1
                    for e in range(max_t + 1):
                        v = tq[e]
                        if v:
                            tq[e] = v * cur % mod
                        cur = cur * factor % mod

                    cur = factor
                    for e in range(1, max_u + 1):
                        v = uq[e]
                        if v:
                            uq[e] = v * cur % mod
                        cur = cur * factor % mod

                continue

            rem_after = rem - a

            new_t = [0] * (M + 1)
            new_u = [0] * (M + 1)
            nt = new_t
            nu = new_u

            mt = -1
            mu = -1

            val0 = 0
            if a <= max_t:
                val0 = tq[a]
            if a <= max_u:
                val0 += uq[a]
                if val0 >= mod:
                    val0 -= mod
            if val0:
                nt[0] = val0
                mt = 0

            max_t_new = max_t + a
            if max_t_new > M:
                max_t_new = M

            for e in range(1, max_t_new + 1):
                val = 0
                if e >= a:
                    val = tq[e - a]
                if e + a <= max_t:
                    val += tq[e + a]
                    if val >= mod:
                        val -= mod
                if val:
                    nt[e] = val * pw[e] % mod
                    if e > mt:
                        mt = e

            if max_u:
                max_u_new = max_u + a
                if max_u_new > M:
                    max_u_new = M
                if max_u_new > rem_after:
                    max_u_new = rem_after

                for e in range(1, max_u_new + 1):
                    val = 0
                    if e >= a:
                        val = uq[e - a]
                    if e + a <= max_u:
                        val += uq[e + a]
                        if val >= mod:
                            val -= mod
                    if val:
                        nu[e] = val * pw[e] % mod
                        if e > mu:
                            mu = e

            tq = nt
            uq = nu
            max_t = mt if mt >= 0 else 0
            rem = rem_after
            max_u = mu if mu >= 0 else 0

            i += 1

        contrib = sum(tq) % mod
        ans = ans * contrib % mod
        if ans == 0:
            break

    print(ans)


if __name__ == "__main__":
    solve()