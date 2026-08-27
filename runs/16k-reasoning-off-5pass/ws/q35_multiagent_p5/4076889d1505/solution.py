import sys
import random

# Increase recursion depth just in case, though not needed here
sys.setrecursionlimit(2000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime_miller_rabin(n, k=10):
    """
    Miller-Rabin primality test.
    Returns True if n is (probably) prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
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

def get_prime_factors(n):
    """
    Returns a set of prime factors of n.
    """
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
    """
    Finds a primitive root modulo p.
    p is assumed to be prime.
    """
    if p == 2:
        return 1
    
    phi = p - 1
    factors = get_prime_factors(phi)
    
    g = 2
    while g < p:
        is_root = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                is_root = False
                break
        if is_root:
            return g
        g += 1
    return -1 # Should not happen for prime p

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
            # For N=1, any A and M=1 works.
            # Smallest n such that A^n - 1 is divisible by 1 is 1.
            results.append("2 1")
            continue
            
        if N <= 59:
            # Use A=2, M=2^N - 1
            # 2^N - 1 <= 2^59 - 1 < 10^18
            M = (1 << N) - 1
            A = 2
            results.append(f"{A} {M}")
        else:
            # For N > 59, we need M <= 10^18.
            # We look for a prime M = k*N + 1.
            # Then find an element of order N.
            
            k = 1
            M = -1
            # Search for prime M = k*N + 1
            # Since N >= 60, M grows. We need M <= 10^18.
            # Max k approx 10^18 / 60 ~ 1.6 * 10^16.
            # But prime gaps are small, so k will be small.
            
            while True:
                M = k * N + 1
                if M > 10**18:
                    # This should theoretically not happen for valid inputs within constraints
                    # but if it does, we might need a fallback. 
                    # Given constraints and prime density, this loop should terminate quickly.
                    break
                
                if is_prime_miller_rabin(M):
                    break
                k += 1
            
            # Now M is a prime such that N | M-1.
            # We need to find A such that ord_M(A) = N.
            # Let g be a primitive root mod M.
            # Then A = g^((M-1)/N) mod M has order N.
            
            g = find_primitive_root(M)
            exponent = (M - 1) // N
            A = pow(g, exponent, M)
            
            results.append(f"{A} {M}")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()