import sys
from bisect import bisect_right

def solve():
    # Maximum value for A is 10^12, so the base X = sqrt(N) is at most 10^6.
    LIMIT = 1000000
    
    # Sieve to count distinct prime factors for each number up to LIMIT.
    # distinct_prime_factors[i] will store the number of distinct prime factors of i.
    distinct_prime_factors = [0] * (LIMIT + 1)
    
    # Iterate through each number starting from 2.
    # If distinct_prime_factors[i] is 0, then i is prime.
    # We then increment the count for all multiples of i.
    for i in range(2, LIMIT + 1):
        if distinct_prime_factors[i] == 0:
            # i is prime
            for j in range(i, LIMIT + 1, i):
                distinct_prime_factors[j] += 1
    
    # Collect all valid bases X such that X has exactly 2 distinct prime factors.
    # The problem requires N to have exactly 2 distinct prime factors.
    # Since N = X^2, the set of prime factors of N is the same as X.
    # Also, the exponents in N must be even, which is satisfied if N = X^2.
    valid_bases = []
    for i in range(1, LIMIT + 1):
        if distinct_prime_factors[i] == 2:
            valid_bases.append(i)
    
    # Generate the valid numbers N = X^2.
    # Since X <= 10^6, N <= 10^12.
    valid_numbers = [x * x for x in valid_bases]
    
    # Sort the valid numbers for binary search.
    valid_numbers.sort()
    
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
        try:
            queries.append(int(next(iterator)))
        except StopIteration:
            break
    
    # Process queries
    results = []
    for A in queries:
        # Find the largest number in valid_numbers <= A.
        # bisect_right returns an insertion point i such that all elements in valid_numbers[:i] are <= A.
        idx = bisect_right(valid_numbers, A) - 1
        
        # The problem guarantees a solution exists (A >= 36), so idx will be >= 0.
        if idx >= 0:
            results.append(valid_numbers[idx])
        else:
            # Fallback, though constraints ensure this isn't reached.
            results.append(0)
            
    # Print results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()