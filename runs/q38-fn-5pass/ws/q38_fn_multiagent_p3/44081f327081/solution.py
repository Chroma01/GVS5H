import sys
import math
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    out = sys.stdout.buffer
    is_cpython = sys.implementation.name == "cpython"

    # If K == 1, the answer is A_i itself.
    if K == 1:
        chunk = []
        append = chunk.append
        end = 2 + N
        for i in range(2, end):
            append(data[i])
            if len(chunk) >= 10000:
                out.write(b"\n".join(chunk) + b"\n")
                chunk.clear()
        if chunk:
            out.write(b"\n".join(chunk) + b"\n")
        return

    # If K == N, every element must be chosen, so the answer is gcd(A).
    if K == N:
        g = 0
        gcd = math.gcd
        to_int = int
        end = 2 + N
        for i in range(2, end):
            g = gcd(g, to_int(data[i]))
            if g == 1:
                break

        line = (str(g) + "\n").encode()
        chunk = line * 10000
        full = N // 10000
        rem = N % 10000
        for _ in range(full):
            out.write(chunk)
        if rem:
            out.write(line * rem)
        return

    # Store original order.  On CPython use compact array; on PyPy list is faster.
    if is_cpython:
        A = array("I", [0]) * N
    else:
        A = [0] * N

    maxA = 0
    minA = 1_000_001
    to_int = int
    base = 2

    for i in range(N):
        x = to_int(data[base + i])
        A[i] = x
        if x > maxA:
            maxA = x
        if x < minA:
            minA = x

    del data

    # All values equal: choosing any K copies gives that value.
    if minA == maxA:
        line = (str(maxA) + "\n").encode()
        chunk = line * 10000
        full = N // 10000
        rem = N % 10000
        for _ in range(full):
            out.write(chunk)
        if rem:
            out.write(line * rem)
        return

    M = maxA
    M1 = M + 1

    # Frequency of each value.
    freq = [0] * M1
    for x in A:
        freq[x] += 1

    # cnt[d] = number of array elements divisible by d.
    cnt = freq[:]
    cnt[1] = N
    half = M // 2

    fr = freq
    ct = cnt

    # On CPython, move small-d work to C-level sum/slice operations.
    # On PyPy, plain loops are usually better for JIT.
    if is_cpython:
        TH = math.isqrt(M) * 2 + 1
        if TH > 2000:
            TH = 2000
        if TH > M:
            TH = M
    else:
        TH = 0

    limit = half if half < TH else TH

    # Small divisors: sum over a strided slice.
    for d in range(2, limit + 1):
        ct[d] = sum(fr[d::d])

    # Larger divisors: explicit harmonic loop.
    start = limit + 1
    if start < 2:
        start = 2
    for d in range(start, half + 1):
        s = ct[d]
        for m in range(d + d, M1, d):
            s += fr[m]
        ct[d] = s

    del freq, fr

    # best[x] = largest divisor d of x with cnt[d] >= K.
    # d = 1 is always valid because K <= N.
    best = [1] * M1
    st = best
    K_local = K

    small_limit = TH if TH < M else M

    # Small divisors: extended slice assignment.
    for d in range(2, small_limit + 1):
        if ct[d] >= K_local:
            st[d::d] = [d] * (M // d)

    # Larger divisors: explicit harmonic loop.
    start = small_limit + 1
    if start < 2:
        start = 2
    for d in range(start, M1):
        if ct[d] >= K_local:
            for m in range(d, M1, d):
                st[m] = d

    del cnt, ct

    # Output answers in original order, chunked to avoid huge temporary strings.
    write = sys.stdout.write
    chunk = []
    append = chunk.append

    for x in A:
        append(str(st[x]))
        if len(chunk) >= 10000:
            write("\n".join(chunk) + "\n")
            chunk.clear()

    if chunk:
        write("\n".join(chunk) + "\n")


if __name__ == "__main__":
    main()