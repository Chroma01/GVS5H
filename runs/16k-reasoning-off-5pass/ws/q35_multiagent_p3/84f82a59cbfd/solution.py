import sys
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

    MAX_S = 10**6
    MAX_N = 10**12

    # Sieve of Eratosthenes to find primes up to MAX_S
    is_prime = [True] * (MAX_S + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(MAX_S**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, MAX_S + 1, i):
                is_prime[j] = False
    
    primes = [i for i, prime in enumerate(is_prime) if prime]
    
    # Generate all S <= 10^6 with exactly two distinct prime factors
    # S = p^a * q^b, p < q, a >= 1, b >= 1
    valid_S = set()
    
    # We iterate over primes p
    # For each p, we consider powers p^a
    # Then we iterate over primes q > p
    # For each q, we consider powers q^b
    # Such that p^a * q^b <= MAX_S
    
    # Optimization: 
    # If p^2 > MAX_S, then a must be 1.
    # If p^2 <= MAX_S, a can be >= 1.
    
    # Let's iterate p from the list of primes
    for i, p in enumerate(primes):
        # p^a
        pa = p
        a = 1
        while pa <= MAX_S:
            # Now we need q > p such that pa * q^b <= MAX_S
            # So q^b <= MAX_S // pa
            limit = MAX_S // pa
            
            # We need to find primes q > p such that q <= limit (since b >= 1)
            # And then for each such q, find max b such that q^b <= limit
            
            # Find starting index for q in primes list
            # We need q > p, so start from index i+1
            # But we also need q <= limit
            
            # Binary search for the first prime > p
            # Since primes is sorted, we can use bisect
            import bisect
            start_idx = i + 1
            if start_idx >= len(primes):
                break
                
            # Find the largest prime <= limit
            # bisect_right returns insertion point, so primes[:idx] are <= limit
            idx = bisect.bisect_right(primes, limit, lo=start_idx)
            
            # Primes from start_idx to idx-1 are candidates for q
            for j in range(start_idx, idx):
                q = primes[j]
                qb = q
                while qb <= limit:
                    s_val = pa * qb
                    if s_val <= MAX_S:
                        valid_S.add(s_val)
                    else:
                        break
                    qb *= q
            
            # Move to next power of p
            if MAX_S // p < pa: # Check for overflow before multiplying
                break
            pa *= p
            a += 1

    # Convert to list of N = S^2
    valid_N = []
    for s in valid_S:
        n = s * s
        if n <= MAX_N:
            valid_N.append(n)
    
    valid_N.sort()
    
    # Answer queries
    results = []
    for A in queries:
        # Find largest N <= A
        # bisect_right returns index where A could be inserted while maintaining order
        # All elements to the left are <= A
        idx = bisect_right(valid_N, A)
        if idx == 0:
            # This should not happen given constraints (A >= 36, smallest 400 number is 36)
            results.append("None")
        else:
            results.append(str(valid_N[idx-1]))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()