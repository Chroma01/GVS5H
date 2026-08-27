import sys

def is_prime(n):
    if n < 2:
        return False
    # small primes trial division
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # Miller-Rabin deterministic for 64-bit integers
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # bases sufficient for n < 2^64
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def primitive_root(p):
    # returns a primitive root modulo prime p
    if p == 2:
        return 1
    n = p - 1
    # factorize p-1
    factors = []
    x = n
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    # test candidates starting from 2
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, n // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None  # should never happen for prime p

def solve_one(N):
    if N == 1:
        # M=1 works: A^n - 1 is always a multiple of 1, smallest n is 1
        return 20250126, 1
    # find smallest k such that p = k*N + 1 is prime
    k = 1
    while True:
        p = k * N + 1
        if p > 10**18:
            # This should not happen for N <= 1e9 based on prime distribution,
            # but as a safety fallback, we can try k=0? No, k must be positive.
            # We rely on the existence of a prime <= 10^18 in this progression.
            # In practice, for N <= 1e9, the smallest such prime is well within 10^18.
            k += 1
            continue
        if is_prime(p):
            break
        k += 1
    # find a primitive root g modulo p
    g = primitive_root(p)
    # set A = g^((p-1)/N) mod p, then ord_p(A) = N
    A = pow(g, (p - 1) // N, p)
    return A, p

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        N = int(data[i])
        A, M = solve_one(N)
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()