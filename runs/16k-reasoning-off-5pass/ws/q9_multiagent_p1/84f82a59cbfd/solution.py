import sys
from bisect import bisect_right

def solve():
    # Precompute primes up to 1,000,000 using Sieve of Eratosthenes
    # Since N <= 10^12 and N = X^2, X <= 10^6.
    LIMIT_X = 1000000
    is_prime = [True] * (LIMIT_X + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(LIMIT_X**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, LIMIT_X + 1, i):
                is_prime[j] = False
    
    primes = [i for i, val in enumerate(is_prime) if val]
    
    # Generate all valid X <= 10^6 such that X = p^k * q^m with p < q distinct primes
    # We store the squares N = X^2 in a list.
    # The condition "exactly 2 distinct prime factors" for N implies X has exactly 2 distinct prime factors.
    # The condition "even number of times" for N implies exponents in N are even, so exponents in X are integers >= 1.
    
    valid_squares = []
    
    # Iterate over pairs of primes (p, q) with p < q
    # We only need to check p up to sqrt(LIMIT_X) because p*q <= LIMIT_X implies p <= sqrt(LIMIT_X)
    for i in range(len(primes)):
        p = primes[i]
        if p * p > LIMIT_X:
            break
            
        for j in range(i + 1, len(primes)):
            q = primes[j]
            if p * q > LIMIT_X:
                break
            
            # Generate all numbers of form p^k * q^m <= LIMIT_X
            # We iterate powers of p, and for each, iterate powers of q
            val_p = p
            while True:
                val_q = q
                while val_p * val_q <= LIMIT_X:
                    valid_squares.append((val_p * val_q) ** 2)
                    if LIMIT_X // q < val_q:
                        break
                    val_q *= q
                
                if LIMIT_X // p < val_p:
                    break
                val_p *= p

    valid_squares.sort()
    
    # Read input
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
            # Find largest square <= A using binary search
            # bisect_right returns the insertion point to maintain order.
            # All elements to the left are <= A.
            idx = bisect_right(valid_squares, A) - 1
            if idx >= 0:
                results.append(str(valid_squares[idx]))
            else:
                # According to problem constraints, a solution always exists for A >= 36.
                # If A < 36, this branch is theoretically unreachable per constraints.
                results.append("0") 
        except StopIteration:
            break
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()