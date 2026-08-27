import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    Q = int(input_data[0])
    queries = []
    for i in range(Q):
        queries.append(int(input_data[i + 1]))
    
    MAX_M = 1000000  # sqrt(10^12) = 10^6
    
    # Sieve to count distinct prime factors for each number up to MAX_M
    # distinct_prime_count[i] will store the number of distinct prime factors of i
    distinct_prime_count = [0] * (MAX_M + 1)
    
    for i in range(2, MAX_M + 1):
        if distinct_prime_count[i] == 0:  # i is prime
            for j in range(i, MAX_M + 1, i):
                distinct_prime_count[j] += 1
    
    # Collect all M in [1, MAX_M] that have exactly 2 distinct prime factors
    valid_M = []
    for m in range(1, MAX_M + 1):
        if distinct_prime_count[m] == 2:
            valid_M.append(m)
    
    # valid_M is already sorted since we iterated in order
    
    # For each query, find the largest M in valid_M such that M <= floor(sqrt(A))
    # Then answer is M^2
    
    import bisect
    
    results = []
    for A in queries:
        limit = int(math.isqrt(A))
        # Find the rightmost position where limit could be inserted while maintaining order
        # bisect_right returns the insertion point after any existing entries of limit
        idx = bisect.bisect_right(valid_M, limit)
        if idx == 0:
            # No valid M <= limit, but problem guarantees a 400 number exists
            # This shouldn't happen given constraints (A >= 36, so limit >= 6, and 6 is valid)
            results.append(0)
        else:
            best_M = valid_M[idx - 1]
            results.append(best_M * best_M)
    
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()