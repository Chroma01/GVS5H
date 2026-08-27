import sys
import random

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def power(a, b, m):
    """Computes (a^b) % m efficiently using binary exponentiation."""
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def is_prime_miller_rabin(n):
    """
    Checks if n is prime using the Miller-Rabin primality test.
    Returns True if n is (probably) prime, False if n is composite.
    Uses deterministic bases for n < 2^64.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witnesses to test. For n < 2^64, these bases are sufficient for deterministic check
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
        if n <= a:
            break
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def get_prime_factors(n):
    """Returns a list of unique prime factors of n."""
    factors = []
    d = 2
    temp = n
    # Optimization: handle 2 separately
    if temp % d == 0:
        factors.append(d)
        while temp % d == 0:
            temp //= d
    d = 3
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 2
    if temp > 1:
        factors.append(temp)
    return factors

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
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
            # For N=1, any A, M=1 works because A^1 - 1 is divisible by 1.
            # Smallest n is 1.
            results.append("2 1")
            continue
        
        # For N > 1, we look for a prime p = k*N + 1.
        # Then the multiplicative group modulo p has order p-1 = k*N.
        # We need an element A of order exactly N.
        # We can find such A by picking a random g and setting A = g^((p-1)/N) mod p.
        # Then A^N = g^(p-1) = 1 mod p.
        # The order of A is N / gcd(N, discrete_log(g)).
        # To ensure order is N, we check A^(N/q) != 1 for all prime factors q of N.
        
        # We iterate k starting from 1.
        # Since N <= 10^9, p = k*N + 1 can go up to 10^18.
        # We expect to find a prime quickly.
        
        prime_factors_N = get_prime_factors(N)
        
        found = False
        k = 1
        while not found:
            p = k * N + 1
            if p > 10**18:
                # Should not happen given constraints and density of primes
                break
            
            if is_prime_miller_rabin(p):
                # Found a prime p = k*N + 1
                # Now find A
                # We need A such that A^N = 1 mod p and A^(N/q) != 1 for all q|N
                
                # Try random bases until we find a valid A
                # The probability of success is phi(N)/N which is reasonably high.
                # We can try a few random bases.
                
                exponent = (p - 1) // N
                
                # Try a few random candidates
                attempts = 0
                while attempts < 100:
                    g = random.randint(2, p - 1)
                    A = power(g, exponent, p)
                    
                    # Check if order is exactly N
                    valid = True
                    for q in prime_factors_N:
                        if power(A, N // q, p) == 1:
                            valid = False
                            break
                    
                    if valid:
                        results.append(f"{A} {p}")
                        found = True
                        break
                    attempts += 1
            
            k += 1

    print('\n'.join(results))

if __name__ == '__main__':
    solve()