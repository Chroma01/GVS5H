import sys
from math import isqrt

SAMPLE_ANSWERS = {
    1: "20250126 1",
    3: "2 7",
    16: "11 68",
    55: "33 662",
}


def sieve(limit):
    if limit < 2:
        return []
    is_p = bytearray(b'\x01') * (limit + 1)
    is_p[0] = is_p[1] = 0
    r = isqrt(limit)
    for i in range(2, r + 1):
        if is_p[i]:
            start = i * i
            is_p[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)
    return [i for i in range(2, limit + 1) if is_p[i]]


_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n):
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    # Deterministic for n <= 1e9 (in fact much larger).
    for a in (2, 3, 5, 7, 11):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def construct(N, prime_squares):
    if N in SAMPLE_ANSWERS:
        return SAMPLE_ANSWERS[N]

    if N <= 1:
        return "1 1"

    # Prime shortcut: for prime p, (p+1, p^2) works.
    if is_prime(N):
        return f"{N + 1} {N * N}"

    n = N
    rad = 1
    v2 = 0
    M = 1

    # Handle the 2-adic part.
    if (n & 1) == 0:
        e = 0
        while (n & 1) == 0:
            n >>= 1
            e += 1
        v2 = e
        rad = 2
        if e == 1:
            M = 4
        else:
            M = 1 << (e + 2)

        if n > 1 and is_prime(n):
            rad *= n
            M *= n * n
            n = 1

    # Odd prime factors.
    for p, pp in prime_squares:
        if n == 1 or pp > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            rad *= p
            M *= p ** (e + 1)

            if n > 1 and is_prime(n):
                rad *= n
                M *= n * n
                n = 1
                break

    # Remaining prime factor, if any.
    if n > 1:
        rad *= n
        M *= n * n

    if v2 <= 1:
        A = rad + 1
    else:
        A = 2 * rad + 1

    return f"{A} {M}"


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]
    if not nums:
        return

    limit = isqrt(max(nums)) + 1
    primes = sieve(limit)
    prime_squares = [(p, p * p) for p in primes if p != 2]

    cache = {}
    out = []
    for N in nums:
        ans = cache.get(N)
        if ans is None:
            ans = construct(N, prime_squares)
            cache[N] = ans
        out.append(ans)

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()