import sys
import random

def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def factor(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors

def find_prime(N):
    k = 1
    while True:
        p = k * N + 1
        if p > 10**18:
            return None
        if is_prime(p):
            return p, k
        k += 1

def find_primitive_root(p, factors):
    if p == 2:
        return 1
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, (p - 1) // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []
    for _ in range(T):
        N = int(input())
        if N == 1:
            out.append("2 1")
            continue
        
        result = find_prime(N)
        if result is None:
            out.append("2 1")
            continue
        p, k = result
        
        # Factor p-1 = k*N
        # We need to find an element of order N
        # Factor k (small) and N
        factors_N = factor(N)
        factors_k = factor(k)
        # Combine unique prime factors of p-1
        all_factors = list(set(factors_N + factors_k))
        
        g = find_primitive_root(p, all_factors)
        if g is None:
            out.append("2 1")
            continue
        
        # Element of order N is g^k
        A = pow(g, k, p)
        M = p
        out.append(f"{A} {M}")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()