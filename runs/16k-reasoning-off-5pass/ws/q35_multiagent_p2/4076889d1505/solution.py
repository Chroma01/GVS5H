import sys
import random

# Set recursion limit just in case, though not needed for this iterative approach
sys.setrecursionlimit(2000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime_mr(n):
    """Miller-Rabin primality test for n >= 2."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
        
    # Witnesses for Miller-Rabin up to 10^18
    # Deterministic set for n < 3.3 * 10^18
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
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

def factorize(n):
    """Returns a set of prime factors of n."""
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def find_primitive_root(p):
    """Finds a primitive root modulo p, where p is prime."""
    if p == 2:
        return 1
    if p == 3:
        return 2
    
    phi = p - 1
    factors = factorize(phi)
    
    g = 2
    while g < p:
        is_primitive = True
        for f in factors:
            if pow(g, phi // f, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g
        g += 1
    return -1 # Should not reach here for prime p

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    iterator = iter(data)
    try:
        T = int(next(iterator))
    except StopIteration:
        return
        
    results = []
    
    for _ in range(T):
        try:
            N_str = next(iterator)
            N = int(N_str)
        except StopIteration:
            break
            
        if N == 1:
            results.append("2 1")
            continue
            
        if N <= 59:
            M = (1 << N) - 1
            results.append(f"2 {M}")
            continue
            
        # For N > 59, we use the prime modulus construction
        # Find smallest prime p = k*N + 1
        k = 1
        while True:
            p = k * N + 1
            if is_prime_mr(p):
                break
            k += 1
            
        # p is a prime such that N divides p-1
        # We need an element of order N modulo p
        # Let g be a primitive root mod p.
        # Then A = g^((p-1)/N) mod p has order N.
        
        g = find_primitive_root(p)
        exponent = (p - 1) // N
        A = pow(g, exponent, p)
        
        results.append(f"{A} {p}")
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()