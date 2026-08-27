import sys
import math
import random

random.seed(1234567)

# ===================== solution code under test (verbatim) =====================
def _sieve(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            start = i * i
            is_p[start::i] = [False] * (((limit - start) // i) + 1)
    return [i for i, v in enumerate(is_p) if v]

SMALL_PRIMES = _sieve(1000)


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
    # Deterministic for n < 2^32
    for a in (2, 7, 61):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n)
        y = random.randrange(0, n)
        r = 1
        q = 1
        g = 1
        m = 128
        x = y
        ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r <<= 1
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
            if g == n:
                continue
        return g


def factor(n):
    """Return list of (p, e) with n = prod p^e. Requires n <= 1e9."""
    res = []
    for p in SMALL_PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            res.append((p, e))
    if n == 1:
        return res
    if is_prime(n):
        res.append((n, 1))
        return res
    # n is composite with no prime factor <= 1000 and n <= 1e9,
    # so n is a product of exactly two primes (possibly equal).
    d = pollard_rho(n)
    a, b = d, n // d
    if a == b:
        res.append((a, 2))
    else:
        res.append((a, 1))
        res.append((b, 1))
    return res


def solve_one(n):
    if n == 1:
        return 1, 1
    A = 0
    M = 1
    for p, e in factor(n):
        if p == 2:
            a = 3
            m = 4 if e == 1 else 1 << (e + 2)
        else:
            a = p + 1
            m = p ** (e + 1)
        # CRT: current A mod M, want A' ≡ a (mod m), gcd(M, m) = 1
        t = (a - A) % m
        t = t * pow(M, -1, m) % m
        A = A + M * t
        M *= m
        A %= M
    if A == 0:
        A = M
    return A, M


# ===================== verification harness =====================
LIMIT = 10 ** 18


def brute_order(a, m, cap):
    """Smallest k in [1, cap] with a^k ≡ 1 (mod m), else None. Pure iteration."""
    target = 1 % m
    x = 1 % m
    for k in range(1, cap + 1):
        x = (x * a) % m
        if x == target:
            return k
    return None


def check_factor(n):
    """Independently validate factor(): primes really prime, product equals n."""
    fac = factor(n)
    prod = 1
    seen = set()
    for p, e in fac:
        assert e >= 1 and p not in seen, (n, fac)
        seen.add(p)
        assert is_prime(p), (n, p)
        prod *= p ** e
    assert prod == n, (n, fac)
    return fac


def check(n, brute):
    fac = check_factor(n)
    a, m = solve_one(n)
    # bounds
    assert 1 <= a <= LIMIT, (n, a, m)
    assert 1 <= m <= LIMIT, (n, a, m)
    if n == 1:
        assert (a, m) == (1, 1), (n, a, m)
        return
    assert m > 1, (n, a, m)
    assert math.gcd(a, m) == 1, (n, a, m)
    assert m <= n * n, (n, a, m)
    # A^N ≡ 1 (mod M)  =>  ord_M(A) divides N
    assert pow(a, n, m) == 1, (n, a, m)
    # For every prime q | N: A^(N/q) ≢ 1 (mod M).
    # ord | N and ord ∤ N/q  =>  v_q(ord) = v_q(N) for all q  =>  ord = N.
    for q, _ in fac:
        assert pow(a, n // q, m) != 1, (n, q, a, m)
    if brute:
        # fully independent: iterate k = 1, 2, ... and find the first hit
        assert brute_order(a, m, n) == n, (n, a, m)


def main():
    tested = 0

    # 1) Exhaustive small range, verified by genuine brute force
    #    (covers N=1, 2, small powers of 2, odd prime powers, composites).
    for n in range(1, 2001):
        check(n, brute=True)
        tested += 1

    # 2) Structured edge cases (verified via the rigorous pow criterion).
    edge = set()
    edge.update(1 << k for k in range(0, 30))          # 2^0 .. 2^29 (powers of two)
    edge.update(3 ** e for e in range(1, 19))          # odd prime powers
    edge.update(5 ** e for e in range(1, 13))
    edge.update(7 ** e for e in range(1, 11))
    edge.update([
        10 ** 9, 10 ** 9 - 1, 10 ** 9 - 2,             # top of the range
        999999999,                                     # 3^3 * 37 * 333667
        999999937,                                     # large prime near 1e9
        999999929,
        998028131,                                     # 10007 * 99733 (two primes > 1000)
        999800011,
        999950884,                                     # 31622^2 = 2^2 * 15811^2
        720720, 1441440, 4324320, 9979200,             # highly composite
        86486400, 73513440, 942634200, 963761198,
    ])
    for n in sorted(edge):
        if n > 2000:
            check(n, brute=False)
            tested += 1

    # 3) Random sweep over the full input range.
    for _ in range(300):
        check(random.randrange(1, 10 ** 9 + 1), brute=False)
        tested += 1

    print("ALL TESTS PASSED:", tested, "cases")


main()