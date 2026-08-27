import sys

def sieve(limit):
    is_p = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_p[0] = 0
    if limit >= 1:
        is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = b"\x00" * (((limit - i * i) // i) + 1)
    return [i for i in range(2, limit + 1) if is_p[i]]

PRIMES = sieve(31623)

_MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _MR_BASES:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

_factor_cache = {}

def distinct_prime_factors(n):
    # returns list of distinct prime factors of n (n >= 1)
    if n in _factor_cache:
        return _factor_cache[n]
    res = []
    m = n
    for p in PRIMES:
        if p * p > m:
            break
        if m % p == 0:
            res.append(p)
            while m % p == 0:
                m //= p
    if m > 1:
        res.append(m)
    _factor_cache[n] = res
    return res

def solve_one(N):
    if N == 1:
        return (2, 1)
    facN = distinct_prime_factors(N)
    k = 1
    while True:
        p = k * N + 1
        if is_prime(p):
            # distinct prime factors of p-1 = k*N
            fset = set(facN)
            if k > 1:
                fset.update(distinct_prime_factors(k))
            facs = list(fset)
            pm1 = p - 1
            # find primitive root
            g = 2
            while True:
                ok = True
                for q in facs:
                    if pow(g, pm1 // q, p) == 1:
                        ok = False
                        break
                if ok:
                    break
                g += 1
            A = pow(g, pm1 // N, p)
            if A <= 1:
                A += p  # shouldn't happen for N >= 2, but keep A positive and valid
            return (A, p)
        k += 1

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        N = int(data[i])
        A, M = solve_one(N)
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out) + "\n")

main()