import sys
import math

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        return

    # Maximum value for sqrt(A) is 10^6 since A <= 10^12
    LIMIT = 1000000
    
    # Sieve to count distinct prime factors
    # omega[i] will store the number of distinct prime factors of i
    omega = [0] * (LIMIT + 1)
    
    # Iterate from 2 to LIMIT
    for i in range(2, LIMIT + 1):
        if omega[i] == 0:  # i is prime
            # Increment count for all multiples of i
            for j in range(i, LIMIT + 1, i):
                omega[j] += 1
    
    # Precompute the largest valid K <= i
    # A valid K has exactly 2 distinct prime factors
    # valid_lookup[i] stores the largest k <= i such that omega[k] == 2
    valid_lookup = [0] * (LIMIT + 1)
    last_valid = 0
    
    for i in range(1, LIMIT + 1):
        if omega[i] == 2:
            last_valid = i
        valid_lookup[i] = last_valid
    
    results = []
    
    for _ in range(Q):
        try:
            A_str = next(iterator)
            A = int(A_str)
        except StopIteration:
            break
            
        # We need largest 400 number <= A
        # 400 number N = K^2 where K has exactly 2 distinct prime factors
        # So we need largest K <= sqrt(A) with omega[K] == 2
        # Then answer is K^2
        
        # Integer square root
        L = math.isqrt(A)
        
        # Clamp L to LIMIT just in case, though A <= 10^12 ensures L <= 10^6
        if L > LIMIT:
            L = LIMIT
            
        # Since A >= 36, L >= 6, and valid_lookup[L] will be valid
        # (smallest valid K is 6, corresponding to N=36)
        K = valid_lookup[L]
        results.append(str(K * K))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()