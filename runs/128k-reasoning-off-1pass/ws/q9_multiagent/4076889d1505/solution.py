import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def is_prime_miller_rabin(n):
    """
    Deterministic Miller-Rabin primality test for n < 10^18.
    Bases sufficient for n < 3,317,044,064,279,371 are [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37].
    For n < 10^18, the first 9 primes are sufficient.
    """
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
    
    # Bases for deterministic Miller-Rabin up to 10^18
    # Using the first 9 primes is sufficient for n < 3.8 * 10^18
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    for a in bases:
        if a >= n:
            break
        
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

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(num_test_cases):
        try:
            n_str = next(iterator)
            N = int(n_str)
        except StopIteration:
            break
        
        # We need to find a pair (A, M) such that the multiplicative order of A mod M is N.
        # Strategy:
        # 1. Choose M = k*N + 1.
        # 2. We want M to be prime.
        # 3. If M is prime and M % 8 is 3 or 5, then (2/M) = -1 (Legendre symbol).
        #    This implies 2^((M-1)/2) = 2^N = -1 mod M.
        #    The order of 2 mod M is 2*N.
        #    The order of 4 = 2^2 mod M is (2*N) / gcd(2, 2*N) = N.
        #    So (A, M) = (4, M) is a valid solution.
        # 4. We iterate k starting from 1 to find the first such M.
        
        k = 1
        while True:
            M = k * N + 1
            
            # Check condition M % 8 in {3, 5}
            if M % 8 == 3 or M % 8 == 5:
                if is_prime_miller_rabin(M):
                    results.append(f"4 {M}")
                    break
            
            k += 1
            # Safety break, though theoretically we should find one quickly.
            # M must be <= 10^18. N <= 10^9. k will be small.
            if M > 10**18:
                # Fallback if something goes wrong (should not happen with valid inputs)
                # For N=1, k=1 -> M=3 (prime, 3%8=3) -> 4 3.
                pass

    print('\n'.join(results))

if __name__ == '__main__':
    solve()