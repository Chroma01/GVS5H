import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(2000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime_miller_rabin(n):
    """
    Deterministic Miller-Rabin primality test for n < 4,759,123,141.
    Returns True if n is prime, False otherwise.
    """
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    
    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Bases for deterministic Miller-Rabin for n < 4,759,123,141
    bases = [2, 7, 61]
    
    for a in bases:
        if a >= n: break
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

def get_prime_p(N):
    """
    Finds the smallest prime p such that p = k * N + 1.
    """
    if N == 1:
        return 1 # Special case handled outside
    
    k = 1
    # If N is odd, k*N + 1 is even for odd k. Since p > 2, p must be odd.
    # So if N is odd, k must be even.
    if N % 2 != 0:
        k = 2
    
    while True:
        p = k * N + 1
        if is_prime_miller_rabin(p):
            return p
        k += 1
        if N % 2 != 0:
            k += 1 # Skip even k for odd N to keep p odd

def get_prime_factors(n):
    """
    Returns a set of prime factors of n.
    """
    factors = set()
    d = 2
    temp = n
    # Trial division up to sqrt(n)
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    
    results = []
    
    for _ in range(T):
        try:
            N_str = next(iterator)
        except StopIteration:
            break
            
        N = int(N_str)
        
        if N == 1:
            # For N=1, A=2, M=1 works because 2^1 - 1 = 1 is divisible by 1.
            results.append("2 1")
            continue
        
        # Find prime p = k*N + 1
        p = get_prime_p(N)
        
        # Factorize N to check order conditions
        prime_factors_N = get_prime_factors(N)
        
        # Find A such that order of A mod p is N
        # We try small integers A starting from 2
        A = 2
        while True:
            # Condition 1: A^N = 1 mod p
            if pow(A, N, p) != 1:
                A += 1
                continue
            
            # Condition 2: A^(N/q) != 1 mod p for all prime factors q of N
            valid = True
            for q in prime_factors_N:
                if pow(A, N // q, p) == 1:
                    valid = False
                    break
            
            if valid:
                results.append(f"{A} {p}")
                break
            A += 1

    print('\n'.join(results))

if __name__ == '__main__':
    solve()