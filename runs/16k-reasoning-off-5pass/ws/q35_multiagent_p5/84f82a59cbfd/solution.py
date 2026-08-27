import sys
import bisect

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

    MAX_K = 10**6
    
    # Sieve of Eratosthenes to find primes up to MAX_K
    # and also to help count distinct prime factors or just generate them.
    # Actually, we can just iterate primes and their powers.
    
    is_prime = [True] * (MAX_K + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, MAX_K + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_K + 1, i):
                if is_prime[j]:
                    is_prime[j] = False
                    
    # Generate all k <= 10^6 with exactly 2 distinct prime factors.
    # k = p^a * q^b where p < q are primes, a >= 1, b >= 1.
    # We will store these k values, then square them to get 400 numbers.
    
    valid_ks = set()
    
    # Iterate over the first prime p
    for i, p in enumerate(primes):
        # p^a <= MAX_K
        pa = p
        a = 1
        while pa <= MAX_K:
            # Iterate over the second prime q > p
            # We can start from the next prime in the list
            for j in range(i + 1, len(primes)):
                q = primes[j]
                # q^b * pa <= MAX_K
                qb = q
                while qb * pa <= MAX_K:
                    valid_ks.add(pa * qb)
                    # Check if next power of q will exceed
                    if MAX_K // q < qb:
                        break
                    qb *= q
                # If even q^1 * pa > MAX_K, then no larger q will work
                if pa * q > MAX_K:
                    break
            
            # Check if next power of p will exceed
            if MAX_K // p < pa:
                break
            pa *= p
            a += 1
            
    # Convert to sorted list of 400 numbers (k^2)
    four_hundred_numbers = sorted([k * k for k in valid_ks])
    
    # Answer queries using binary search
    results = []
    for A in queries:
        # Find the rightmost index where 400 number <= A
        idx = bisect.bisect_right(four_hundred_numbers, A)
        if idx == 0:
            # Should not happen per constraints (A >= 36, smallest 400 number is 36)
            results.append("0") # Fallback
        else:
            results.append(str(four_hundred_numbers[idx - 1]))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()