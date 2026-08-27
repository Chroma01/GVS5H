import sys

def sieve(limit):
    is_p = bytearray(b"\x01") * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = b"\x00" * (((limit - i * i) // i) + 1)
    return [i for i in range(2, limit + 1) if is_p[i]]

PRIMES = sieve(31623)

def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    # deterministic for n < 3,474,749,660,383; plenty since p = kN+1 stays small
    for a in (2, 3, 5, 7, 11, 13, 17):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def factor_distinct(n, res):
    for p in PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            res.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        res.append(n)

def solve(N, out):
    if N == 1:
        out.append("2 1")
        return
    k = 1
    while True:
        p = k * N + 1
        if is_prime(p):
            break
        k += 1
    # distinct prime factors of p-1 = k*N
    facs = []
    factor_distinct(N, facs)
    factor_distinct(k, facs)
    facs = list(set(facs))
    m = p - 1
    g = 2
    while True:
        ok = True
        for q in facs:
            if pow(g, m // q, p) == 1:
                ok = False
                break
        if ok:
            break
        g += 1
    A = pow(g, m // N, p)
    out.append(f"{A} {p}")

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        solve(int(data[i]), out)
    sys.stdout.write("\n".join(out) + "\n")

main()