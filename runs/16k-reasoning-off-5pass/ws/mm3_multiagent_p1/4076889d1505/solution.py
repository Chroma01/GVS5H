import sys
import math

def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin primality test for 64-bit integers."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def factor_distinct(n: int) -> list:
    """Return list of distinct prime factors of n via trial division."""
    factors = []
    temp = n
    if temp % 2 == 0:
        factors.append(2)
        while temp % 2 == 0:
            temp //= 2
    p = 3
    while p * p <= temp:
        if temp % p == 0:
            factors.append(p)
            while temp % p == 0:
                temp //= p
        p += 2
    if temp > 1:
        factors.append(temp)
    return factors

def solve_one(N: int) -> tuple:
    if N == 1:
        return (2, 1)
    
    prime_factors = factor_distinct(N)
    max_k = 10**18 // N
    
    for k in range(1, max_k + 1):
        p = k * N + 1
        if not is_prime(p):
            continue
        if pow(2, N, p) != 1:
            continue
        ok = True
        for q in prime_factors:
            if pow(2, N // q, p) == 1:
                ok = False
                break
        if ok:
            return (2, p)
    
    M = 2**N - 1
    if M <= 10**18:
        return (2, M)
    
    for base in [3, 5, 7, 11, 13]:
        for k in range(1, max_k + 1):
            p = k * N + 1
            if not is_prime(p):
                continue
            if pow(base, N, p) != 1:
                continue
            ok = True
            for q in prime_factors:
                if pow(base, N // q, p) == 1:
                    ok = False
                    break
            if ok:
                return (base, p)
    
    return (2, 1)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    T = int(data[0])
    out_lines = []
    for i in range(1, T + 1):
        N = int(data[i])
        A, M = solve_one(N)
        out_lines.append(f"{A} {M}")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()