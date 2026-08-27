import sys
import math

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]

small_primes = sieve(10000)

def is_prime_miller_rabin(n):
    if n < 2:
        return False
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Deterministic bases for 64-bit integers
    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in bases:
        if a % n == 0:
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

def factorize(n):
    factors = set()
    temp = n
    for p in small_primes:
        if p * p > temp:
            break
        if temp % p == 0:
            factors.add(p)
            while temp % p == 0:
                temp //= p
    if temp > 1:
        factors.add(temp)
    return factors

def solve():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    T = int(input_data[0])
    out_lines = []
    idx = 1
    for _ in range(T):
        N = int(input_data[idx]); idx += 1
        if N == 1:
            out_lines.append("2 1")
            continue
        # Get prime factors of N
        prime_factors = factorize(N)
        # Find prime p = k*N + 1 with gcd(k, N) = 1
        p = None
        k = 0
        while True:
            k += 1
            if math.gcd(k, N) != 1:
                continue
            p_candidate = k * N + 1
            if p_candidate > 10**18:
                # This should not happen in practice, but break to avoid infinite loop
                p = None
                break
            if is_prime_miller_rabin(p_candidate):
                p = p_candidate
                break
        if p is None:
            # Fallback (should not be reached)
            out_lines.append("2 1")
            continue
        # Find base g such that g^{(p-1)/q} != 1 for all q in prime_factors
        g = 1
        while True:
            g += 1
            ok = True
            for q in prime_factors:
                if pow(g, (p-1)//q, p) == 1:
                    ok = False
                    break
            if ok:
                break
        A = pow(g, k, p)
        out_lines.append(f"{A} {p}")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()