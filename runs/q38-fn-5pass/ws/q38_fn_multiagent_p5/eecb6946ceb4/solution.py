import sys
import math


def solve_numpy(raw, np):
    # Fast text parsing in C.  np.fromstring is deprecated but still widely
    # available and much faster than Python-level parsing for 1e6 integers.
    arr = np.fromstring(raw.decode("ascii"), dtype=np.int64, sep=" ")
    if arr.size == 0:
        return

    n = int(arr[0])
    S = arr[1:1 + n]

    if S.size < 3:
        sys.stdout.write("0\n")
        return

    # Affine normalization: translation and division by gcd of differences
    # preserve 3-term arithmetic progressions and can shrink the universe.
    mn = int(S.min())
    if mn != 0:
        S = S - mn

    try:
        g = int(np.gcd.reduce(S))
        if g > 1:
            S = S // g
    except Exception:
        pass

    max_s = int(S.max())

    indicator = np.zeros(max_s + 1, dtype=np.float64)
    indicator[S] = 1.0

    # Need cyclic convolution length at least 2*max_s + 1.
    nfft = 1 << (2 * max_s + 1).bit_length()

    f = np.fft.rfft(indicator, n=nfft)
    f *= f
    conv = np.fft.irfft(f, n=nfft)

    idx = S.astype(np.int64, copy=False) * 2
    vals = np.floor(conv[idx] + 0.5 + 1e-9).astype(np.int64)

    ans = int(np.sum((vals - 1) // 2, dtype=np.int64))
    sys.stdout.write(str(ans) + "\n")


def parse_fallback(raw):
    # Memory-friendly parser: avoids creating 1e6 temporary bytes objects.
    nums = []
    append = nums.append
    num = 0
    in_num = False

    for b in raw:
        if b > 32:  # digit in valid input
            num = num * 10 + (b - 48)
            in_num = True
        elif in_num:
            append(num)
            num = 0
            in_num = False

    if in_num:
        append(num)

    if not nums:
        return []

    n = nums[0]
    return nums[1:1 + n]


def normalize_list(S):
    if len(S) <= 1:
        return S

    mn = min(S)
    g = 0

    for x in S:
        y = x - mn
        g = math.gcd(g, y)
        if g == 1:
            break

    if mn == 0 and g == 1:
        return S

    if g > 1:
        return [(x - mn) // g for x in S]

    return [x - mn for x in S]


def solve_sparse(S, max_s, evens=None, odds=None):
    present = bytearray(max_s + 1)
    for x in S:
        present[x] = 1

    if evens is None:
        evens = []
        odds = []
        for x in S:
            if x & 1:
                odds.append(x)
            else:
                evens.append(x)

    ans = 0
    pres = present

    # Endpoints of a valid triplet must have the same parity.
    for arr in (evens, odds):
        m = len(arr)
        for i in range(m - 1):
            a = arr[i]
            for j in range(i + 1, m):
                ans += pres[(a + arr[j]) >> 1]

    sys.stdout.write(str(ans) + "\n")


def solve_bigint(S, max_s):
    # Exact convolution using base 2^24 digits.
    # Maximum convolution coefficient is at most N <= 1e6 < 2^24,
    # so no carries occur between base-2^24 digits.
    buf = bytearray((max_s + 1) * 3)

    for s in S:
        buf[s * 3] = 1

    x = int.from_bytes(buf, "little")
    del buf

    sq = x * x
    del x

    length = 3 * (2 * max_s + 1)
    data = sq.to_bytes(length, "little")
    del sq

    ans = 0
    d = data

    for b in S:
        o = b * 6  # byte offset of digit 2*b
        c = d[o] | (d[o + 1] << 8) | (d[o + 2] << 16)
        ans += (c - 1) >> 1

    sys.stdout.write(str(ans) + "\n")


def solve_fallback(S):
    n = len(S)
    if n < 3:
        sys.stdout.write("0\n")
        return

    S = normalize_list(S)
    max_s = max(S)

    # For moderately small N and large universe, endpoint enumeration can be
    # faster than a large big-integer square.
    if n <= 12000:
        evens = []
        odds = []
        for x in S:
            if x & 1:
                odds.append(x)
            else:
                evens.append(x)

        pair_count = (
            len(evens) * (len(evens) - 1) // 2
            + len(odds) * (len(odds) - 1) // 2
        )

        if pair_count <= 30_000_000 and max_s > 200_000:
            solve_sparse(S, max_s, evens, odds)
            return

    solve_bigint(S, max_s)


def main():
    raw = sys.stdin.buffer.read()
    if not raw:
        return

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        try:
            solve_numpy(raw, np)
            return
        except Exception:
            pass

    S = parse_fallback(raw)
    del raw
    solve_fallback(S)


if __name__ == "__main__":
    main()