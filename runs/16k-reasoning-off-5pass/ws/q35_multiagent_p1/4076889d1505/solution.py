import sys
import random

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

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
    Returns a list of distinct prime factors of n.
    Since n <= 10^9, trial division up to sqrt(n) is efficient.
    """
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

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
            
        # Edge case N=1
        if N == 1:
            results.append("2 1")
            continue
            
        # We need to find a prime p such that N divides p-1.
        # So p = k*N + 1 for some integer k >= 1.
        # We iterate k=1, 2, ... until we find a prime p.
        # Given N <= 10^9, p will likely be found quickly and p <= 10^18.
        
        k = 1
        p = -1
        while True:
            # Calculate p = k*N + 1
            # Check for overflow relative to 10^18 roughly, though Python handles large ints
            candidate = k * N + 1
            if candidate > 2 * 10**18: # Safety bound, should not be reached
                break
            
            if is_prime_miller_rabin(candidate):
                p = candidate
                break
            
            k += 1
            
        # Now we have a prime p such that N | (p-1).
        # We need to find an element A of order N modulo p.
        # The group Z_p* is cyclic of order p-1.
        # Let g be a primitive root modulo p. Then A = g^((p-1)/N) has order N.
        # However, finding a primitive root can be slow if we don't know factorization of p-1.
        # But we know p-1 = k*N. We can just pick a random element g and check if it generates order N.
        # Actually, simpler: Pick random g in [2, p-2].
        # Let A = g^k mod p.
        # The order of A divides N.
        # To ensure order is exactly N, we check that A^(N/q) != 1 mod p for all prime factors q of N.
        
        # Factorize N to get prime factors
        prime_factors_N = get_prime_factors(N)
        
        # Find A
        while True:
            g = random.randrange(2, p - 1)
            # Compute A = g^k mod p
            # Note: k = (p-1)/N
            exponent = (p - 1) // N
            A = pow(g, exponent, p)
            
            # Check if A has order exactly N
            # Condition 1: A^N = 1 mod p (Always true by Fermat's Little Theorem / construction)
            # Condition 2: A^(N/q) != 1 mod p for all prime factors q of N
            
            is_correct_order = True
            for q in prime_factors_N:
                if pow(A, N // q, p) == 1:
                    is_correct_order = False
                    break
            
            if is_correct_order:
                break
        
        results.append(f"{A} {p}")

    print('\n'.join(results))

if __name__ == '__main__':
    solve()