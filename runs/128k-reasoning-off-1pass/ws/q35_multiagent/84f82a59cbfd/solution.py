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

    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))

    # Maximum value for A is 10^12, so sqrt(A) is at most 10^6
    MAX_K = 1000000
    
    # Step 1: Sieve to count distinct prime factors for each number up to MAX_K
    # num_distinct_primes[i] will store the number of distinct prime factors of i
    num_distinct_primes = [0] * (MAX_K + 1)
    
    for i in range(2, MAX_K + 1):
        if num_distinct_primes[i] == 0:
            # i is prime
            for j in range(i, MAX_K + 1, i):
                num_distinct_primes[j] += 1
                
    # Step 2: Collect all k such that k has exactly 2 distinct prime factors
    valid_ks = []
    for k in range(1, MAX_K + 1):
        if num_distinct_primes[k] == 2:
            valid_ks.append(k)
            
    # valid_ks is already sorted since we iterated in order
    
    # Step 3: Process each query
    results = []
    for A in queries:
        # Find largest k such that k^2 <= A, i.e., k <= sqrt(A)
        # Use integer square root to avoid floating point issues
        S = math.isqrt(A)
        
        # Find the largest valid_k <= S
        # bisect_right returns the insertion point to maintain order
        # all values to the left are <= S
        idx = bisect_right(valid_ks, S)
        
        if idx == 0:
            # This should not happen given constraints A >= 36
            # The smallest valid k is 6 (2*3), so k^2 = 36
            # If S < 6, then no solution, but problem guarantees existence
            results.append(0)
        else:
            best_k = valid_ks[idx - 1]
            results.append(best_k * best_k)
            
    # Print all results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()