import sys

SPARSE_LIMIT = 5000
COMP_LIMIT = 5000


def parse_input(data):
    n = len(data)
    i = 0
    while i < n and data[i] <= 32:
        i += 1

    N = 0
    while i < n and data[i] > 32:
        N = N * 10 + (data[i] - 48)
        i += 1

    if N <= 0:
        return 0, [], 0

    S = [0] * N
    max_val = 0
    idx = 0
    d = data

    while i < n and idx < N:
        while i < n and d[i] <= 32:
            i += 1
        if i >= n:
            break

        num = 0
        while i < n and d[i] > 32:
            num = num * 10 + (d[i] - 48)
            i += 1

        S[idx] = num
        if num > max_val:
            max_val = num
        idx += 1

    if idx < N:
        S = S[:idx]
        N = idx

    return N, S, max_val


def sparse_count(S, N):
    present = set(S)
    contains = present.__contains__

    even = []
    odd = []
    for x in S:
        if x & 1:
            odd.append(x)
        else:
            even.append(x)

    ans = 0
    for arr in (even, odd):
        m = len(arr)
        for i in range(m - 1):
            a = arr[i]
            for j in range(i + 1, m):
                if contains((a + arr[j]) >> 1):
                    ans += 1
    return ans


def complement_count(S, max_val, missing_count):
    M = max_val
    total = ((M - 1) * (M - 1)) // 4

    if missing_count == 0:
        return total

    present = bytearray(M + 1)
    for x in S:
        present[x] = 1

    missing = []
    miss_even = []
    miss_odd = []
    single_sum = 0
    even = 0
    odd = 0

    for x in range(1, M + 1):
        if not present[x]:
            missing.append(x)
            single_sum += min(x - 1, M - x) + ((M - x) >> 1) + ((x - 1) >> 1)
            if x & 1:
                miss_odd.append(x)
                odd += 1
            else:
                miss_even.append(x)
                even += 1

    K = len(missing)

    # Pairs of missing values:
    # 1) endpoints of an AP: same parity
    pair_sum = even * (even - 1) // 2 + odd * (odd - 1) // 2

    # 2) missing values as (A, B): C = 2B - A <= M
    left = 0
    for j, y in enumerate(missing):
        threshold = 2 * y - M
        while left < j and missing[left] < threshold:
            left += 1
        pair_sum += j - left

    # 3) missing values as (B, C): A = 2B - C >= 1
    right = 0
    for i, x in enumerate(missing):
        if right < i:
            right = i
        threshold = 2 * x - 1
        while right + 1 < K and missing[right + 1] <= threshold:
            right += 1
        pair_sum += right - i

    # APs consisting entirely of missing values.
    triple_sum = 0
    for arr in (miss_even, miss_odd):
        m = len(arr)
        for i in range(m - 1):
            a = arr[i]
            for j in range(i + 1, m):
                if not present[(a + arr[j]) >> 1]:
                    triple_sum += 1

    return total - single_sum + pair_sum - triple_sum


def big_int_count(S, max_val):
    max_e = -1
    max_o = -1

    for x in S:
        if x & 1:
            c = (x - 1) >> 1
            if c > max_o:
                max_o = c
        else:
            c = x >> 1
            if c > max_e:
                max_e = c

    len_e = ((5 * (max_e + 1)) + 1) // 2 if max_e >= 0 else 0
    len_o = ((5 * (max_o + 1)) + 1) // 2 if max_o >= 0 else 0

    arr_e = bytearray(len_e)
    arr_o = bytearray(len_o)

    # Base is 2^20.  A compressed value c is stored as a 1-bit at bit 20*c.
    # Since 20*c bits = (5*c)/2 bytes, byte index is (5*c)//2.
    # If c is odd, the bit offset inside that byte is 4, otherwise 0.
    for x in S:
        if x & 1:
            c = (x - 1) >> 1
            byte = (c * 5) >> 1
            if c & 1:
                arr_o[byte] |= 16
            else:
                arr_o[byte] |= 1
        else:
            c = x >> 1
            byte = (c * 5) >> 1
            if c & 1:
                arr_e[byte] |= 16
            else:
                arr_e[byte] |= 1

    if max_e >= 0:
        X = int.from_bytes(arr_e, "little")
        del arr_e
        Y = X * X
        del X
        total_chunks = 2 * max_e + 1
        byte_len = ((5 * total_chunks) + 1) // 2 + 4
        buf_e = Y.to_bytes(byte_len, "little")
        del Y
    else:
        buf_e = b""

    if max_o >= 0:
        X = int.from_bytes(arr_o, "little")
        del arr_o
        Y = X * X
        del X
        total_chunks = 2 * max_o + 1
        byte_len = ((5 * total_chunks) + 1) // 2 + 4
        buf_o = Y.to_bytes(byte_len, "little")
        del Y
    else:
        buf_o = b""

    me = 2 * max_e if max_e >= 0 else -1
    mo = 2 * max_o if max_o >= 0 else -1
    mask = 0xFFFFF

    ans = 0
    be = buf_e
    bo = buf_o

    for B in S:
        total = 0

        # Even endpoints: A=2a, C=2c, midpoint B=a+c.
        if B <= me:
            byte = (B * 5) >> 1
            val = (
                be[byte]
                | (be[byte + 1] << 8)
                | (be[byte + 2] << 16)
                | (be[byte + 3] << 24)
            )
            if B & 1:
                val >>= 4
            total += val & mask

        # Odd endpoints: A=2a+1, C=2c+1, midpoint B=a+c+1.
        idx = B - 1
        if 0 <= idx <= mo:
            byte = (idx * 5) >> 1
            val = (
                bo[byte]
                | (bo[byte + 1] << 8)
                | (bo[byte + 2] << 16)
                | (bo[byte + 3] << 24)
            )
            if idx & 1:
                val >>= 4
            total += val & mask

        if total:
            ans += (total - 1) >> 1

    return ans


def solve_fallback(data):
    N, S, max_val = parse_input(data)
    del data

    if N < 3:
        print(0)
        return

    missing_count = max_val - N
    if missing_count < 0:
        missing_count = 0

    # Dense cases are often much faster by inclusion-exclusion over missing values.
    if missing_count <= COMP_LIMIT and missing_count < N:
        print(complement_count(S, max_val, missing_count))
        return

    # Small N: enumerate endpoint pairs of the same parity.
    if N <= SPARSE_LIMIT:
        print(sparse_count(S, N))
        return

    if missing_count <= COMP_LIMIT:
        print(complement_count(S, max_val, missing_count))
        return

    print(big_int_count(S, max_val))


def solve_numpy(np, data):
    vals = np.fromstring(data, dtype=np.int64, sep=" ")
    if vals.size < 2:
        raise ValueError("numpy parse failed")

    N = int(vals[0])
    if vals.size < N + 1:
        raise ValueError("numpy parse incomplete")

    if N < 3:
        print(0)
        return

    S = vals[1:1 + N]
    max_val = int(S.max())

    # Need length strictly greater than 2*max_val to avoid circular convolution.
    n = 1 << (2 * max_val).bit_length()

    f = np.zeros(n, dtype=np.float64)
    f[S] = 1.0

    spec = np.fft.rfft(f)
    del f

    spec *= spec
    g = np.fft.irfft(spec, n=n)
    del spec

    coeff = np.rint(g[2 * S]).astype(np.int64)
    ans = int((coeff.sum() - N) // 2)
    print(ans)


def main():
    data = sys.stdin.buffer.read()
    if not data:
        return

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        try:
            solve_numpy(np, data)
            return
        except Exception:
            try:
                import gc
                gc.collect()
            except Exception:
                pass

    solve_fallback(data)


if __name__ == "__main__":
    main()