import sys
import math

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
    
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
    
    # Maximum value of A is 10^12, so sqrt(A) is at most 10^6
    MAX_M = 1000000
    
    # Sieve to count distinct prime factors for each number up to MAX_M
    # distinct_prime_factors[i] will store the number of distinct prime factors of i
    distinct_prime_factors = [0] * (MAX_M + 1)
    
    for i in range(2, MAX_M + 1):
        if distinct_prime_factors[i] == 0:
            # i is prime, mark all multiples
            for j in range(i, MAX_M + 1, i):
                distinct_prime_factors[j] += 1
    
    # Collect all numbers M in [1, MAX_M] that have exactly 2 distinct prime factors
    valid_M = []
    for m in range(1, MAX_M + 1):
        if distinct_prime_factors[m] == 2:
            valid_M.append(m)
    
    # valid_M is already sorted since we iterated in order
    
    # For each query, find the largest M <= floor(sqrt(A))
    results = []
    for A in queries:
        # Compute integer square root of A
        limit = math.isqrt(A)
        
        # Binary search: find the rightmost M in valid_M such that M <= limit
        # bisect_right returns the insertion point after all elements <= limit
        # So the element at index (pos - 1) is the largest M <= limit
        import bisect
        pos = bisect.bisect_right(valid_M, limit)
        
        if pos == 0:
            # This should not happen given constraints (A >= 36, so limit >= 6, and 6 is valid)
            # But just in case, we should handle it. The problem guarantees a 400 number exists.
            # The smallest 400 number is 36 (M=6). If limit < 6, there's no solution, but constraints say A >= 36.
            results.append(0)
        else:
            M = valid_M[pos - 1]
            results.append(M * M)
    
    # Print all results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()