import sys
import random

def is_prime(n):
    if n < 2:
        return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for r in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def find_order(p, N):
    # find order of 2 mod p
    # order divides p-1, and we know it must be a multiple of N if p=kN+1
    # actually we want order exactly N
    # since p = 2*k*N + 1, order of 2 is 2*N or a divisor
    # we want order N, so we need to check that 2^N ≡ 1 mod p and 2^(N/q) != 1 for prime factors q of N
    if pow(2, N, p) != 1:
        return -1
    # check that for all prime factors q of N, 2^(N/q) != 1
    n = N
    factors = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    for q in factors:
        if pow(2, N//q, p) == 1:
            return -1
    return N

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    T = int(input_data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(input_data[idx]); idx += 1
        if N == 1:
            out.append("1 1")
        elif N <= 60:
            M = (1 << N) - 1
            out.append(f"2 {M}")
        else:
            found = False
            # try k up to large
            for k in range(1, 2000000):
                p = 2 * k * N + 1
                if p > 10**18:
                    break
                if is_prime(p):
                    ord_val = find_order(p, N)
                    if ord_val == N:
                        out.append(f"2 {p}")
                        found = True
                        break
            if not found:
                out.append(f"2 {(1 << 60) - 1}")
    print("\n".join(out))

solve()