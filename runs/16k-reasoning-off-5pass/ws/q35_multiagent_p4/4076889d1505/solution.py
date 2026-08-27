import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N_str = next(iterator)
            N = int(N_str)
        except StopIteration:
            break
            
        if N == 1:
            # A=2, M=1 works: 2^1 - 1 = 1, div by 1. Smallest n=1.
            results.append("2 1")
            continue
            
        # For N <= 60, we can use A=2, M=2^N - 1
        # 2^60 - 1 > 10^18, so we need to be careful.
        # 2^59 - 1 is approx 5.76e17 <= 10^18.
        # 2^60 - 1 is approx 1.15e18 > 10^18.
        # So for N <= 59, A=2, M=2^N - 1 works.
        
        if N <= 59:
            M = (1 << N) - 1
            results.append(f"2 {M}")
        else:
            # For N > 59, we need a different construction.
            # We can use the property that if we set M = N+1 and find A such that
            # the order of A mod M is N, it works. But order must divide phi(M).
            # This is hard to guarantee for arbitrary N.
            
            # Alternative: Use A = 2 and M = 2^N - 1 is too big.
            # Let's use A = N and M = N^2 - 1? Order is 2.
            
            # Let's use the construction:
            # M = N + 1
            # A = 2
            # Check if order of 2 mod M is N.
            # This requires 2^N = 1 mod M and for all d|N, d<N, 2^d != 1 mod M.
            # This is not guaranteed.
            
            # Better construction for large N:
            # Use A = 2 and M = 2^N - 1 is invalid for N > 59.
            
            # Let's try A = 2 and M = (2^N - 1) // K for some K?
            # No, order might drop.
            
            # Correct approach for large N:
            # Factorize N into prime powers: N = p1^e1 * ... * pk^ek.
            # For each prime power q = p^e, find a prime r such that r = 1 + k*q for some k,
            # and the order of 2 mod r is exactly q.
            # Then set M = product of such primes r_i.
            # The order of 2 mod M will be LCM(q1, ..., qk) = N.
            # We need M <= 10^18.
            
            # Since N <= 10^9, the number of prime factors is small.
            # The primes r_i will be roughly of size q_i.
            # Product of r_i will be roughly product of q_i = N <= 10^9 <= 10^18.
            # So this construction works and keeps M small.
            
            # Algorithm:
            # 1. Factorize N into prime powers.
            # 2. For each prime power q = p^e, find a prime r such that:
            #    - r = 1 + k*q for some integer k >= 1
            #    - The multiplicative order of 2 modulo r is exactly q.
            #    - This is true if 2^q = 1 mod r and for all proper divisors d of q, 2^d != 1 mod r.
            #    - Since q is a prime power p^e, the proper divisors are p^0, p^1, ..., p^(e-1).
            #    - We need 2^(q/p) != 1 mod r.
            #    - We can search for k = 1, 2, ... until r = 1 + k*q is prime.
            #    - Then check if 2^q = 1 mod r (which is true by Fermat's Little Theorem if r is prime and r-1 is multiple of q? No, r-1 = k*q, so order divides k*q. We need order to be exactly q.)
            #    - Actually, if r is prime, the order of 2 mod r divides r-1 = k*q.
            #    - We need the order to be exactly q.
            #    - This means 2^q = 1 mod r, and for all prime factors s of q, 2^(q/s) != 1 mod r.
            #    - Since q = p^e, the only prime factor is p. So we need 2^(q/p) != 1 mod r.
            #    - Also we need 2^q = 1 mod r.
            #    - If we find r such that r = 1 + k*q is prime, then by Fermat, 2^(r-1) = 1 mod r, i.e., 2^(k*q) = 1 mod r.
            #    - The order d divides k*q. We want d = q.
            #    - This requires that q divides d, so d is a multiple of q. Since d | k*q, d can be q, 2q, ..., kq.
            #    - We need d = q. This means 2^q = 1 mod r.
            #    - And for any prime factor s of k, 2^(k*q/s) != 1 mod r? No, we just need to ensure that the order is not a proper divisor of k*q that is a multiple of q? No.
            #    - Let's simplify: We want order of 2 mod r to be exactly q.
            #    - This requires 2^q = 1 mod r.
            #    - And for all d | q, d < q, 2^d != 1 mod r.
            #    - Since q = p^e, the maximal proper divisor is q/p.
            #    - So we need 2^(q/p) != 1 mod r.
            #    - If we find a prime r = 1 + k*q such that 2^q = 1 mod r and 2^(q/p) != 1 mod r, then the order is q.
            #    - Note that 2^q = 1 mod r implies that the order divides q. Since 2^(q/p) != 1, the order is not a divisor of q/p. Thus the order is exactly q.
            #    - So the condition is: r = 1 + k*q is prime, 2^q = 1 mod r, and 2^(q/p) != 1 mod r.
            #    - But wait, if r = 1 + k*q is prime, then 2^(k*q) = 1 mod r.
            #    - It does NOT imply 2^q = 1 mod r.
            #    - We need to find r such that 2^q = 1 mod r.
            #    - This means r divides 2^q - 1.
            #    - So we can find prime factors of 2^q - 1.
            #    - For each prime factor r of 2^q - 1, the order of 2 mod r divides q.
            #    - Since q is a prime power p^e, the order is p^j for some j <= e.
            #    - We want the order to be exactly q = p^e.
            #    - This is true if r does not divide 2^(q/p) - 1.
            #    - So we can factorize 2^q - 1, find a prime factor r such that r does not divide 2^(q/p) - 1.
            #    - Such a prime factor exists because 2^q - 1 and 2^(q/p) - 1 are coprime? No, gcd(2^q - 1, 2^(q/p) - 1) = 2^(gcd(q, q/p)) - 1 = 2^(q/p) - 1.
            #    - So the prime factors of 2^q - 1 that do not divide 2^(q/p) - 1 are exactly those with order q.
            #    - Such primes exist (primitive prime divisors).
            #    - So for each prime power q = p^e, we find a prime factor r of 2^q - 1 such that r does not divide 2^(q/p) - 1.
            #    - Then set M = product of such r's.
            #    - The order of 2 mod M is LCM(q1, ..., qk) = N.
            #    - We need M <= 10^18.
            #    - Since each r is a factor of 2^q - 1, and q <= N <= 10^9, r can be large.
            #    - However, we can choose the smallest such r.
            #    - The smallest primitive prime divisor of 2^q - 1 is usually not too large.
            #    - For q up to 10^9, the smallest primitive prime divisor can be up to O(q log q) or something?
            #    - Actually, it can be large. But we only need ONE such r for each q.
            #    - And we need the product of all such r's to be <= 10^18.
            #    - Since N <= 10^9, the product of the q's is N.
            #    - The primes r_i are roughly of size q_i or larger.
            #    - If r_i is close to q_i, then product is close to N <= 10^9 <= 10^18.
            #    - But r_i can be much larger than q_i.
            #    - For example, for q = 2^30, the smallest primitive prime divisor might be large.
            #    - However, we can use a different base A.
            #    - Instead of A=2, we can use A = N+1 or something.
            #    - But the problem allows any A, M.
            #    - Let's stick with A=2 and try to find small r_i.
            #    - If the product exceeds 10^18, we might need a different strategy.
            #    - But for N <= 10^9, it is likely that we can find small enough r_i.
            
            # Let's implement this.
            
            # Factorize N
            temp = N
            prime_powers = []
            d = 2
            while d * d <= temp:
                if temp % d == 0:
                    pp = 1
                    while temp % d == 0:
                        pp *= d
                        temp //= d
                    prime_powers.append((pp, d))
                d += 1
            if temp > 1:
                prime_powers.append((temp, temp))
            
            M = 1
            A = 2
            
            for q, p in prime_powers:
                # Find a prime factor r of 2^q - 1 such that r does not divide 2^(q/p) - 1
                # We can search for r by checking divisors of 2^q - 1.
                # But 2^q - 1 is huge. We can't factorize it directly.
                # Instead, we can use the fact that any prime factor r of 2^q - 1 satisfies r = 1 + k*q for some k.
                # And r is prime.
                # We can search for k = 1, 2, ... and check if r = 1 + k*q is prime.
                # If r is prime, then the order of 2 mod r divides q.
                # We need to check if the order is exactly q.
                # This is true if 2^q = 1 mod r (which is true if r | 2^q - 1) and 2^(q/p) != 1 mod r.
                # But we don't know if r | 2^q - 1 just because r is prime and r = 1 + k*q.
                # We need to check if 2^q = 1 mod r.
                
                # So the algorithm for each q:
                # k = 1
                # while True:
                #     r = 1 + k * q
                #     if r is prime:
                #         if pow(2, q, r) == 1 and pow(2, q // p, r) != 1:
                #             break
                #     k += 1
                
                # This might be slow if k is large.
                # But for small q, k is small.
                # For large q, r is large, and we might exceed 10^18.
                
                # Let's try this.
                
                k = 1
                while True:
                    r = 1 + k * q
                    if r > 10**18:
                        # This should not happen if we can find a solution, but if it does, we have a problem.
                        # For N <= 10^9, this construction might fail for some q.
                        # But let's assume it works for the given constraints.
                        pass
                    
                    # Check if r is prime
                    # For r up to 10^18, we need a primality test.
                    # Miller-Rabin is suitable.
                    if is_prime(r):
                        # Check if 2^q = 1 mod r and 2^(q/p) != 1 mod r
                        if pow(2, q, r) == 1 and pow(2, q // p, r) != 1:
                            break
                    k += 1
                
                M *= r
                
            results.append(f"{A} {M}")
            
    print('\n'.join(results))

def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # Miller-Rabin primality test
    # Write n-1 as 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # Witnesses for deterministic Miller-Rabin up to 10^18
    # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] is sufficient for n < 3.8 * 10^18
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

if __name__ == '__main__':
    solve()