import sys
import math

def sieve(limit):
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = b"\x00" * (((limit - i * i) // i) + 1)
    return [i for i in range(2, limit + 1) if is_prime[i]]

PRIMES = sieve(31623)

def factor(n):
    fac = []
    for p in PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            fac.append((p, e))
    if n > 1:
        fac.append((n, 1))
    return fac

def solve_case(N):
    if N == 1:
        return (1, 1)
    fac = factor(N)
    mods = []
    rems = []
    for p, e in fac:
        if p == 2:
            m = 1 << (e + 2)   # 2^(e+2)
            a = 5              # ord_{2^(e+2)}(5) = 2^e
        else:
            m = p ** (e + 1)
            a = 1 + p          # ord_{p^(e+1)}(1+p) = p^e
        mods.append(m)
        rems.append(a % m)
    # CRT combine (moduli pairwise coprime)
    M = 1
    for m in mods:
        M *= m
    A = 0
    for m, r in zip(mods, rems):
        Mi = M // m
        inv = pow(Mi, -1, m)
        A = (A + r * Mi * inv) % M
    if A == 0:
        A = M  # shouldn't happen since each r != 0 mod m, but keep A positive
    return (A, M)

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        N = int(data[i])
        A, M = solve_case(N)
        assert 1 <= A <= 10**18 and 1 <= M <= 10**18
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out) + "\n")

main()