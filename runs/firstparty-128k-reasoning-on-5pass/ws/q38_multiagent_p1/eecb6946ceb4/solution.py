import sys

DIRECT_LIMIT = 2000


def count_direct(vals):
    s = set(vals)
    arr = sorted(vals)
    n = len(arr)
    ans = 0
    for i in range(n):
        b = arr[i]
        tb = b + b
        for j in range(i):
            if (tb - arr[j]) in s:
                ans += 1
    return ans


def count_fft(vals, maxv, np):
    need = 2 * maxv + 1
    size = 1
    while size < need:
        size <<= 1

    f = np.zeros(size, dtype=np.float64)
    f[vals] = 1.0

    F = np.fft.rfft(f)
    del f
    F *= F
    conv = np.fft.irfft(F, n=size)
    del F

    idx = vals.astype(np.int64) * 2
    counts = np.rint(conv[idx]).astype(np.int64)
    del conv

    counts = np.maximum(counts, 1)
    ans = int(np.sum((counts - 1) // 2))
    return ans


def count_bigint(vals, maxv):
    ba = bytearray(3 * (maxv + 1))
    for v in vals:
        ba[3 * v] = 1

    x = int.from_bytes(ba, "little")
    del ba

    p = x * x
    del x

    b = p.to_bytes(6 * (maxv + 1), "little")
    del p

    ans = 0
    for v in vals:
        off = 6 * v
        c = b[off] | (b[off + 1] << 8) | (b[off + 2] << 16)
        ans += (c - 1) // 2
    return ans


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    if N < 3:
        print(0)
        return

    if N <= DIRECT_LIMIT:
        vals = list(map(int, data[1:1 + N]))
        print(count_direct(vals))
        return

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        it = iter(data)
        next(it)
        vals = np.fromiter(map(int, it), dtype=np.int32, count=N)
        del data, it

        maxv = int(vals.max())
        try:
            ans = count_fft(vals, maxv, np)
        except Exception:
            ans = count_bigint(vals, maxv)
        print(ans)
    else:
        from array import array

        tc = "I"
        if array("I").itemsize < 4:
            tc = "L"

        it = iter(data)
        next(it)
        vals = array(tc, map(int, it))
        del data, it

        maxv = int(max(vals))
        print(count_bigint(vals, maxv))


if __name__ == "__main__":
    solve()