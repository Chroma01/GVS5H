import sys

# Deterministic Miller-Rabin for 64-bit integers
def is_prime(n):
    if n < 2:
        return False
    # small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    # Deterministic bases for 2^64
    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in bases:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def factor(n):
    """Return a list of prime factors of n (with multiplicity)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def get_distinct_prime_factors(n_val, n_factors):
    """Return the set of distinct prime factors of n_val, given prime factors of N (subset)."""
    distinct_primes = set(n_factors)
    temp = n_val
    for p in distinct_primes:
        while temp % p == 0:
            temp //= p
    # temp now contains the part of n_val coprime to all primes in distinct_primes
    # Factor temp by trial division (temp is small, as it's essentially k/gcd(k, N))
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            distinct_primes.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        distinct_primes.add(temp)
    return distinct_primes

def find_primitive_root(p, prime_factors):
    """Find a primitive root modulo p given the distinct prime factors of p-1."""
    if p == 2:
        return 1
    g = 2
    while True:
        ok = True
        for q in prime_factors:
            if pow(g, (p - 1) // q, p) == 1:
                ok = False
                break
        if ok:
            return g
        g += 1

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    T = int(input_data[0])
    out_lines = []
    idx = 1
    for _ in range(T):
        N = int(input_data[idx]); idx += 1
        if N == 1:
            out_lines.append("2 1")
            continue
        if N <= 60:
            out_lines.append(f"2 {2**N - 1}")
            continue
        # Factor N
        n_factors = factor(N)
        # Determine starting k and step
        if N % 2 == 1:
            k = 2
            step = 2
        else:
            k = 1
            step = 1
        found = False
        max_k = (10**18 - 1) // N
        while k <= max_k:
            p = k * N + 1
            if p > 10**18:
                break
            if is_prime(p):
                p_minus_1 = p - 1
                distinct_primes = get_distinct_prime_factors(p_minus_1, n_factors)
                g = find_primitive_root(p, distinct_primes)
                A = pow(g, (p - 1) // N, p)
                out_lines.append(f"{A} {p}")
                found = True
                break
            k += step
        if not found:
            # Fallback: continue with step 1 (should not be needed)
            while True:
                p = k * N + 1
                if p > 10**18:
                    p = 10**18 + 1
                    break
                if is_prime(p):
                    p_minus_1 = p - 1
                    distinct_primes = get_distinct_prime_factors(p_minus_1, n_factors)
                    g = find_primitive_root(p, distinct_primes)
                    A = pow(g, (p - 1) // N, p)
                    out_lines.append(f"{A} {p}")
                    found = True
                    break
                k += 1
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()