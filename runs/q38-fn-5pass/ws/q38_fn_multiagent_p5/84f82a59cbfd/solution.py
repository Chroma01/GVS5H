import sys
from math import isqrt

MAX = 1_000_000


def build_prefix():
    limit = MAX + 1
    cnt = bytearray(limit)

    # Count the prime factor 2 for every even number.
    cnt[2::2] = b'\x01' * ((limit - 1) // 2)

    # Odd primes up to MAX//2 are enough: a prime > MAX//2 cannot appear
    # in any valid base <= MAX together with another prime factor.
    half = limit // 2
    for i in range(3, half + 1, 2):
        if not cnt[i]:  # i is prime
            for j in range(i, limit, i):
                cnt[j] += 1

    # pref[x] = largest integer <= x having exactly two distinct prime factors.
    pref = [0] * limit
    last = 0
    for i in range(6, limit):
        if cnt[i] == 2:
            last = i
        pref[i] = last

    return pref


def main():
    data = sys.stdin.buffer.read()
    if not data:
        return

    n = len(data)
    idx = 0

    while idx < n and data[idx] <= 32:
        idx += 1

    q = 0
    while idx < n and data[idx] > 32:
        q = q * 10 + data[idx] - 48
        idx += 1

    if q == 0:
        return

    pref = build_prefix()

    out = [None] * q
    isqrt_local = isqrt
    pref_local = pref

    for k in range(q):
        while idx < n and data[idx] <= 32:
            idx += 1

        a = 0
        while idx < n and data[idx] > 32:
            a = a * 10 + data[idx] - 48
            idx += 1

        r = isqrt_local(a)
        m = pref_local[r]
        out[k] = str(m * m)

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()