import sys
import math
from bisect import bisect_right

def solve():
    # Maximum value for A is 10^12, so the square root limit is 10^6.
    LIMIT = 1000000
    
    # Array to store the count of distinct prime factors for each number up to LIMIT
    distinct_prime_counts = [0] * (LIMIT + 1)
    
    # Sieve-like process to count distinct prime factors
    # Iterate through each number starting from 2
    for i in range(2, LIMIT + 1):
        if distinct_prime_counts[i] == 0:
            # i is prime, increment count for all its multiples
            for j in range(i, LIMIT + 1, i):
                distinct_prime_counts[j] += 1
    
    # Collect all numbers that have exactly 2 distinct prime factors
    valid_roots = [x for x in range(2, LIMIT + 1) if distinct_prime_counts[x] == 2]
    
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        return

    results = []
    for _ in range(Q):
        try:
            A_str = next(iterator)
            A = int(A_str)
        except StopIteration:
            break
        
        # The largest 400 number <= A is X^2 where X <= sqrt(A) and X has exactly 2 distinct prime factors.
        limit_sqrt = int(math.isqrt(A))
        
        # Find the largest valid root <= limit_sqrt using binary search
        # bisect_right returns an insertion point i such that all e in a[:i] have e <= x
        idx = bisect_right(valid_roots, limit_sqrt) - 1
        
        # Since the problem guarantees a solution exists (A >= 36), idx should be >= 0
        if idx >= 0:
            ans = valid_roots[idx] * valid_roots[idx]
            results.append(str(ans))
        else:
            # Fallback, though constraints say this won't happen
            results.append("0")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()