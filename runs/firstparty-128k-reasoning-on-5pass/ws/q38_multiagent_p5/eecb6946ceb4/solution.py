import sys
from array import array
import gc

BRUTE_LIMIT = 4000


def count_brute(arr):
    n = len(arr)
    if n < 3:
        return 0

    a = list(arr)
    s = set(a)
    contains = s.__contains__
    ans = 0

    for i in range(n - 1):
        ai = a[i]
        for j in range(i + 1, n):
            s2 = ai + a[j]
            if (s2 & 1) == 0 and contains(s2 >> 1):
                ans += 1

    return ans


def count_bigint(arr, mn, mx):
    L = mx - mn + 1

    # Pack the indicator array in base 2^20.
    # Bit 20*b is set iff mn+b is in S.
    ba_len = (20 * L + 7) // 8
    ba = bytearray(ba_len)

    for x in arr:
        b = x - mn
        t = b >> 1
        if b & 1:
            ba[5 * t + 2] = 16
        else:
            ba[5 * t] = 1

    a = int.from_bytes(ba, "little")
    del ba

    p = a * a
    del a

    # Product has digits 0 .. 2L-2, each 20 bits.
    p_len = (20 * (2 * L - 1) + 7) // 8
    pb = p.to_bytes(p_len, "little")
    del p

    ans = 0
    for x in arr:
        i = (x - mn) * 5
        val = pb[i] | (pb[i + 1] << 8) | ((pb[i + 2] & 15) << 16)
        ans += (val - 1) >> 1

    return ans


def self_test():
    # Deterministic pseudo-random tests for the packed-integer path.
    seed = 123456789
    for _ in range(30):
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        n = 1 + (seed % 60)

        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        maxv = n + (seed % 200)

        vals = set()
        while len(vals) < n:
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            vals.add(1 + (seed % maxv))

        arr = array("I", vals)
        mn = min(arr)
        mx = max(arr)

        if count_bigint(arr, mn, mx) != count_brute(arr):
            raise RuntimeError("random self-test mismatch")

    samples = [
        (5, [8, 3, 1, 5, 2], 3),
        (7, [300000, 100000, 499998, 499999, 200000, 400000, 500000], 5),
        (10, [13, 1, 16, 15, 12, 4, 7, 10, 2, 19], 10),
    ]

    for _, vals, expected in samples:
        arr = array("I", vals)
        mn = min(arr)
        mx = max(arr)

        if count_bigint(arr, mn, mx) != expected:
            raise RuntimeError("sample self-test mismatch")
        if count_brute(arr) != expected:
            raise RuntimeError("sample brute self-test mismatch")


def main():
    gc.disable()

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        self_test()
        return

    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    N = int(tokens[0])
    if N < 3:
        print(0)
        return

    it = iter(tokens)
    next(it)
    arr = array("I", map(int, it))
    del tokens, it

    if N <= BRUTE_LIMIT:
        print(count_brute(arr))
    else:
        mn = min(arr)
        mx = max(arr)
        print(count_bigint(arr, mn, mx))


if __name__ == "__main__":
    main()