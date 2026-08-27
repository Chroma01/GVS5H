import sys
import math
from bisect import bisect_right

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        Q = int(next(iterator))
    except StopIteration:
        return

    # Precompute primes up to 10^6 using Sieve of Eratosthenes
    # The maximum A is 10^12, so the maximum square root is 10^6.
    LIMIT = 1000000
    is_prime = [True] * (LIMIT + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(LIMIT**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, LIMIT + 1, i):
                is_prime[j] = False
    
    primes = [i for i, prime in enumerate(is_prime) if prime]
    
    # Generate numbers with exactly 2 distinct prime factors up to LIMIT
    # Form: p^k * q^m where p < q are primes, k >= 1, m >= 1
    # These numbers Y satisfy the condition that Y^2 is a "400 number".
    valid_numbers = []
    
    # Iterate over the smaller prime p
    for i, p in enumerate(primes):
        # Calculate powers of p: p^k
        p_pow = p
        while p_pow <= LIMIT:
            # Iterate over the larger prime q
            for j in range(i + 1, len(primes)):
                q = primes[j]
                # Check if p^k * q fits
                if p_pow * q > LIMIT:
                    break
                
                # Now iterate powers of q: q^m
                q_pow = q
                while True:
                    num = p_pow * q_pow
                    if num > LIMIT:
                        break
                    valid_numbers.append(num)
                    
                    # Check for overflow before multiplying again
                    if LIMIT // q_pow < q_pow: 
                        break
                    q_pow *= q
            
            # Check for overflow before multiplying p again
            if LIMIT // p < p:
                break
            p_pow *= p
            
    # Sort the valid numbers for binary search
    valid_numbers.sort()
    
    # Process queries
    results = []
    for _ in range(Q):
        try:
            A_str = next(iterator)
            A = int(A_str)
        except StopIteration:
            break
        
        # We need the largest Y such that Y^2 <= A and Y has exactly 2 distinct prime factors.
        # So Y <= sqrt(A).
        limit_sqrt = math.isqrt(A)
        
        # Find the largest value in valid_numbers <= limit_sqrt
        # bisect_right returns the insertion point after all elements <= limit_sqrt
        idx = bisect_right(valid_numbers, limit_sqrt)
        
        if idx > 0:
            best_y = valid_numbers[idx - 1]
            results.append(str(best_y * best_y))
        else:
            # According to problem statement, a 400 number always exists <= A.
            # Since A >= 36, and 36 = 2^2 * 3^2 is the smallest, this case shouldn't happen.
            results.append("0")

    print('\n'.join(results))

if __name__ == '__main__':
    solve()