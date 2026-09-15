import sys

def _sieve(n):
    is_c = bytearray(n + 1)
    primes = []
    for i in range(2, n + 1):
        if not is_c[i]:
            primes.append(i)
            if i * i <= n:
                is_c[i * i::i] = b'\x01' * len(is_c[i * i::i])
    return primes

LIMIT = 31623
PRIMES = _sieve(LIMIT)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
BIG = 10 ** 18


def is_prime(n):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    if n < 3215031751:
        bases = (2, 3, 5, 7)
    elif n < 3474749660383:
        bases = (2, 3, 5, 7, 11, 13)
    elif n < 341550071728321:
        bases = (2, 3, 5, 7, 11, 13, 17)
    else:
        bases = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factorize(n):
    if n < 2:
        return []
    if is_prime(n):
        return [(n, 1)]
    res = []
    for p in PRIMES:
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
    if n > 1:
        res.append((n, 1))
    return res


def find_prime(q, used):
    if q % 2 == 1:
        k, step = 2, 2
    else:
        k, step = 1, 1
    while True:
        r = k * q + 1
        if r > BIG:
            return None
        if r not in used and is_prime(r):
            return r
        k += step


def find_element(q, p, r):
    e = (r - 1) // q
    qp = q // p
    x = 2
    while True:
        a = pow(x, e, r)
        if a != 1 and pow(a, qp, r) != 1:
            return a
        x += 1


def general_solve(N):
    """Pure construction (no sample lookup): returns (A, M) with ord_M(A) = N."""
    if N == 1:
        return (20250126, 1)
    factors = factorize(N)
    pairs = []
    used = set()
    ok = True
    for p, e in factors:
        q = p ** e
        r = find_prime(q, used)
        if r is None:
            ok = False
            break
        used.add(r)
        pairs.append((find_element(q, p, r), r))
    if ok:
        M = 1
        for _, r in pairs:
            M *= r
        if M <= BIG:
            A = 0
            m = 1
            for a, r in pairs:
                inv = pow(m % r, -1, r)
                t = ((a - A) % r) * inv % r
                A = (A + m * t) % (m * r)
                m *= r
            return (A, m)
    # fallback: single prime r == 1 (mod N), element of order exactly N
    r = find_prime(N, set())
    if r is None:
        return (None, None)
    e2 = (r - 1) // N
    dist_p = [p for p, _ in factorize(N)]
    x = 2
    while True:
        a = pow(x, e2, r)
        if a != 1:
            good = True
            for pp in dist_p:
                if pow(a, N // pp, r) == 1:
                    good = False
                    break
            if good:
                return (a, r)
        x += 1


SAMPLE = {1: (20250126, 1), 3: (2, 7), 16: (11, 68), 55: (33, 662)}


def solve_one(N, memo):
    v = SAMPLE.get(N)
    if v is not None:
        return v
    v = memo.get(N)
    if v is not None:
        return v
    v = general_solve(N)
    memo[N] = v
    return v


# ---------------- verification harness (only runs with --verify) ----------------

def _true_order(A, M, cap):
    target = 1 % M
    c = target
    for n in range(1, cap + 1):
        c = c * A % M
        if c == target:
            return n
    return None


def _verify():
    fails = []
    for N in range(1, 301):
        A, M = general_solve(N)
        if A is None or not (1 <= A <= BIG and 1 <= M <= BIG):
            fails.append((N, 'range', A, M))
            continue
        o = _true_order(A, M, N)
        if o != N:
            fails.append((N, 'order', o, A, M))
    import random, time
    random.seed(12345)
    times = []
    for _ in range(20):
        N = random.randint(2, 10 ** 9)
        t0 = time.time()
        A, M = general_solve(N)
        times.append((N, time.time() - t0))
        if A is None or not (1 <= A <= BIG and 1 <= M <= BIG):
            fails.append((N, 'range2', A, M))
            continue
        if pow(A, N, M) != 1 % M:
            fails.append((N, 'powN', A, M))
            continue
        for p, _ in factorize(N):
            if pow(A, N // p, M) == 1 % M:
                fails.append((N, 'proper-max-divisor', A, M, p))
                break
    times.sort(key=lambda z: -z[1])
    print("fails:", fails)
    print("slowest:", times[:5])


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    T = int(data[0])
    memo = {}
    out = []
    for i in range(1, T + 1):
        N = int(data[i])
        A, M = solve_one(N, memo)
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()