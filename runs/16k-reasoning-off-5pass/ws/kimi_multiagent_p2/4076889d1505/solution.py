import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    Ns = data[1:1 + t]

    LIMIT = 10**18

    # ---------- Miller-Rabin (deterministic for n < 2^64) ----------
    MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

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
        for a in MR_BASES:
            a %= n
            if a == 0:
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

    # ---------- small primes ----------
    def primes_upto(n):
        sieve = bytearray([1]) * (n + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, int(n ** 0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        return [i for i in range(2, n + 1) if sieve[i]]

    SMALL_PRIMES = primes_upto(1000)          # 168 primes
    PRESIEVE = SMALL_PRIMES[1:]               # odd primes 3..997

    # ---------- distinct prime factors of n (n <= 1e9) ----------
    def prime_factors(n):
        facs = set()
        m = n
        for p in SMALL_PRIMES:
            if p * p > m:
                break
            if m % p == 0:
                facs.add(p)
                while m % p == 0:
                    m //= p
        if m > 1:
            if is_prime(m):
                facs.add(m)
            else:
                # m = q1*q2 with 1000 < q1 <= q2 <= 31623
                q = 1009
                found = False
                while q * q <= m:
                    if m % q == 0:
                        facs.add(q)
                        facs.add(m // q)
                        found = True
                        break
                    q += 2
                if not found:
                    facs.add(m)
        return facs

    # ---------- find prime p = kN+1 <= LIMIT ----------
    def find_prime(N):
        if N % 2 == 0:
            k = 1
            step = 1
        else:
            k = 2
            step = 2
        k_max = (LIMIT - 1) // N
        while k <= k_max:
            cand = k * N + 1
            ok = True
            for sp in PRESIEVE:
                if cand % sp == 0:
                    ok = False
                    break
            if ok and is_prime(cand):
                return k, cand
            k += step
        return None, None  # should never happen for N <= 1e9

    # ---------- find A = a^k mod p with ord_p(A) = N ----------
    def find_base(N, k, p, facs):
        tests = [(N // q) for q in facs]
        a = 2
        while True:
            A = pow(a, k, p)
            if A > 1:
                good = True
                for e in tests:
                    if pow(A, e, p) == 1:
                        good = False
                        break
                if good:
                    return A
            a += 1

    cache = {}
    out = []
    for tok in Ns:
        N = int(tok)
        res = cache.get(N)
        if res is None:
            if N == 1:
                res = (2, 1)
            elif N <= 59:
                # M = 2^N - 1 < 10^18; ord_M(2) = N exactly
                res = (2, (1 << N) - 1)
            else:
                facs = prime_factors(N)
                k, p = find_prime(N)
                A = find_base(N, k, p, facs)
                res = (A, p)
            cache[N] = res
        out.append(res)

    sys.stdout.write("\n".join(f"{a} {m}" for a, m in out) + "\n")

solve()