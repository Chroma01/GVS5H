import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            queries.append(int(next(iterator)))
    except StopIteration:
        return

    # Maximum value for X is sqrt(10^12) = 10^6
    MAX_X = 1000000
    
    # Sieve to count distinct prime factors
    # distinct_factors[i] will store the number of distinct prime factors of i
    distinct_factors = [0] * (MAX_X + 1)
    
    # Standard Sieve of Eratosthenes modification
    for i in range(2, MAX_X + 1):
        if distinct_factors[i] == 0:
            # i is prime
            for j in range(i, MAX_X + 1, i):
                distinct_factors[j] += 1
    
    # Identify numbers with exactly 2 distinct prime factors
    is_valid = [False] * (MAX_X + 1)
    for i in range(2, MAX_X + 1):
        if distinct_factors[i] == 2:
            is_valid[i] = True
            
    # Precompute max_valid[i]: the largest integer <= i that is valid
    # If no such integer exists, store 0 (though problem constraints imply existence for A >= 36)
    max_valid = [0] * (MAX_X + 1)
    current_max = 0
    for i in range(1, MAX_X + 1):
        if is_valid[i]:
            current_max = i
        max_valid[i] = current_max
        
    # Process queries
    results = []
    for A in queries:
        # We need largest N <= A such that N = X^2 and X has exactly 2 distinct prime factors.
        # So X <= sqrt(A). Let L = floor(sqrt(A)).
        # We need largest valid X <= L.
        L = int(A**0.5)
        if L > MAX_X:
            L = MAX_X
        
        if L < 2:
            # Should not happen based on constraints (A >= 36)
            results.append(0)
        else:
            best_x = max_valid[L]
            results.append(best_x * best_x)
            
    # Print results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()