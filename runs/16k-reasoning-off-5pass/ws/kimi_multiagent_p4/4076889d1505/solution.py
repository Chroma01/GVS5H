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
    return [i for i in range(limit + 1) if is_p[i]]

PRIMES = sieve(31623)
SMALL_PRIMES = [p for p in PRIMES if p < 100]  # cheap prefilter for candidates

MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

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
    for a in MR_BASES:
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

def prime_factors(n):
    """Distinct prime factors of n (n <= 1e9). Leftover after trial division is prime."""
    facs = []
    for p in PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            facs.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        facs.append(n)
    return facs

def solve(N):
    if N == 1:
        return (2, 1)
    facs = prime_factors(N)
    # Find prime p = k*N + 1. Parity: if N odd, k must be even for p odd.
    step = 1 if N % 2 == 0 else 2
    k = step
    while True:
        p = k * N + 1
        ok = True
        for sp in SMALL_PRIMES:
            if p % sp == 0:
                ok = False
                break
        if ok and is_prime(p):
            break
        k += step
    e = (p - 1) // N  # = k
    b = 2
    while True:
        x = pow(b, e, p)
        if x != 1:
            good = True
            for q in facs:
                if pow(x, N // q, p) == 1:
                    good = False
                    break
            if good:
                return (x, p)
        b += 1

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        A, M = solve(int(data[i]))
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out) + "\n")

main()