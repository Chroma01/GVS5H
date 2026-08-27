import sys
import random

# Set recursion limit just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def power(a, b, m):
    """Computes (a^b) % m efficiently."""
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def is_prime_miller_rabin(n, k=20):
    """Miller-Rabin primality test."""
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
    """Returns a list of distinct prime factors of n."""
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
            
        if N == 1:
            results.append("2 1")
            continue
            
        if N <= 60:
            M = (1 << N) - 1
            results.append(f"2 {M}")
            continue
            
        # For N > 60, we look for a prime p = k*N + 1 such that order of 2 mod p is N.
        # This requires:
        # 1. p is prime
        # 2. 2^N = 1 mod p
        # 3. For all prime factors q of N, 2^(N/q) != 1 mod p
        
        prime_factors_N = get_prime_factors(N)
        
        k = 1
        found = False
        while not found:
            p = k * N + 1
            
            # Check bounds
            if p > 10**18:
                # This should theoretically not be reached for valid N <= 10^9
                # But if it is, we might need a fallback or larger search.
                # Given constraints and properties of primitive prime divisors,
                # a small k should suffice.
                break
                
            if is_prime_miller_rabin(p):
                # Check if order of 2 mod p is N
                # Condition 1: 2^N = 1 mod p
                if power(2, N, p) != 1:
                    k += 1
                    continue
                
                # Condition 2: For all q | N, 2^(N/q) != 1 mod p
                valid_order = True
                for q in prime_factors_N:
                    if power(2, N // q, p) == 1:
                        valid_order = False
                        break
                
                if valid_order:
                    results.append(f"2 {p}")
                    found = True
                else:
                    k += 1
            else:
                k += 1
                
    print('\n'.join(results))

if __name__ == '__main__':
    solve()