import sys

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]

primes = sieve(31622)

def is_prime(n):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if a >= n: break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def find_prime_mod_q(q):
    k = 1
    while True:
        r = k * q + 1
        if is_prime(r):
            return r
        k += 1

def find_element_of_order_q(q, r, p):
    exp = (r - 1) // p
    for g in range(2, r):
        if pow(g, exp, r) != 1:
            return pow(g, (r - 1) // q, r)
    return None

def factorize(n):
    factors = {}
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            count = 0
            while n % p == 0:
                count += 1
                n //= p
            factors[p] = count
    if n > 1:
        factors[n] = 1
    return factors

def crt(remainders, moduli):
    M = 1
    for m in moduli:
        M *= m
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        inv = pow(Mi, m - 2, m)
        x = (x + r * Mi * inv) % M
    return x, M

def solve():
    input = sys.stdin.read
    data = input().split()
    T = int(data[0])
    results = []
    for i in range(1, T + 1):
        N = int(data[i])
        if N == 1:
            results.append("1 1")
            continue
        
        factors = factorize(N)
        q_list = []
        for p, e in factors.items():
            q_list.append((p, p ** e))
        
        remainders = []
        moduli = []
        for p, q in q_list:
            r = find_prime_mod_q(q)
            a = find_element_of_order_q(q, r, p)
            remainders.append(a)
            moduli.append(r)
        
        A, M = crt(remainders, moduli)
        results.append(f"{A} {M}")
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()