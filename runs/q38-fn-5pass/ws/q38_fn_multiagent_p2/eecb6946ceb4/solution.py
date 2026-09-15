import sys


def _autocorr(arr, np):
    n = arr.size
    if n == 0:
        return np.zeros(0, dtype=np.int64)

    conv_len = 2 * n - 1
    size = 1 << (conv_len - 1).bit_length()

    f = np.fft.rfft(arr, n=size)
    f *= f
    c = np.fft.irfft(f, n=size)[:conv_len]
    return np.rint(c).astype(np.int64)


def solve_numpy(data, np):
    try:
        arr = np.fromstring(data, dtype=np.int64, sep=' ')
    except TypeError:
        arr = np.fromstring(data.decode(), dtype=np.int64, sep=' ')

    if arr.size == 0:
        return

    n = int(arr[0])
    if arr.size < n + 1:
        raise ValueError("incomplete input parse")

    vals = arr[1:1 + n]

    if n < 3:
        sys.stdout.write("0\n")
        return

    maxv = int(vals.max())

    # E[h] = 1 iff 2h is in S
    # O[h] = 1 iff 2h+1 is in S
    le = maxv // 2 + 1
    lo = (maxv + 1) // 2

    half = vals >> 1
    even_mask = (vals & 1) == 0

    ce = np.zeros(maxv + 1, dtype=np.int64)
    co = np.zeros(maxv + 1, dtype=np.int64)

    if even_mask.any():
        e = np.bincount(half[even_mask], minlength=le).astype(np.float64)
        c = _autocorr(e, np)
        m = c.size
        if m > maxv + 1:
            m = maxv + 1
        ce[:m] = c[:m]
        del e, c

    odd_mask = ~even_mask
    if odd_mask.any():
        o = np.bincount(half[odd_mask], minlength=lo).astype(np.float64)
        c = _autocorr(o, np)
        m = c.size
        if m > maxv + 1:
            m = maxv + 1
        co[:m] = c[:m]
        del o, c

    # For middle B:
    #   even-even pairs: convE[B]
    #   odd-odd pairs:   convO[B-1]
    # The ordered-pair count includes exactly one self-pair (B, B).
    total = ce[vals] + co[vals - 1]
    ans = np.sum(np.maximum(total - 1, 0) // 2)

    sys.stdout.write(str(int(ans)) + "\n")


def _count_sparse(vals):
    st = set(vals)
    ev = []
    od = []

    for v in vals:
        if v & 1:
            od.append(v)
        else:
            ev.append(v)

    ans = 0
    contains = st.__contains__

    for arr in (ev, od):
        m = len(arr)
        for i in range(m - 1):
            ai = arr[i]
            for j in range(i + 1, m):
                if contains((ai + arr[j]) >> 1):
                    ans += 1

    return ans


def _packed_conv_bytes(ba, max_t):
    if max_t < 0:
        return None

    p = int.from_bytes(ba, "little")
    if p == 0:
        return None

    prod = p * p

    # Enough bytes to read a 20-bit coefficient at index max_t.
    needed = (20 * max_t + 26) >> 3

    prod_len = (prod.bit_length() + 7) >> 3
    if prod_len > needed:
        needed = prod_len

    return prod.to_bytes(needed, "little")


def _count_bigint(vals, maxv, even_count, odd_count):
    # Pack each parity indicator as a polynomial in base 2^20.
    # Coefficients are 0/1, and convolution coefficients are <= 500000,
    # so no carries cross a 20-bit digit boundary.
    le = maxv // 2 + 1
    lo = (maxv + 1) // 2

    ba_e = bytearray((20 * le + 7) >> 3) if even_count else None
    ba_o = bytearray((20 * lo + 7) >> 3) if odd_count else None

    for v in vals:
        h = v >> 1
        bit = h * 20
        if v & 1:
            ba_o[bit >> 3] |= 1 << (bit & 7)
        else:
            ba_e[bit >> 3] |= 1 << (bit & 7)

    be = _packed_conv_bytes(ba_e, maxv) if even_count else None
    del ba_e

    bo = _packed_conv_bytes(ba_o, maxv - 1) if odd_count else None
    del ba_o

    MASK = (1 << 20) - 1
    ans = 0

    if be is not None and bo is not None:
        for v in vals:
            if v & 1:
                # v = 2q + 1
                # ce[v] is at odd index 2q+1: unaligned 20-bit field.
                q = v >> 1
                off = 5 * q + 2
                c1 = ((be[off] | (be[off + 1] << 8) | (be[off + 2] << 16)) >> 4) & MASK

                # co[v-1] is at even index 2q: aligned.
                off = 5 * q
                c2 = (bo[off] | (bo[off + 1] << 8) | (bo[off + 2] << 16)) & MASK
            else:
                # v = 2q
                # ce[v] is at even index 2q: aligned.
                q = v >> 1
                off = 5 * q
                c1 = (be[off] | (be[off + 1] << 8) | (be[off + 2] << 16)) & MASK

                # co[v-1] is at odd index 2q-1: unaligned.
                off = 5 * q - 3
                c2 = ((bo[off] | (bo[off + 1] << 8) | (bo[off + 2] << 16)) >> 4) & MASK

            ans += (c1 + c2 - 1) >> 1

    elif be is not None:
        # Only even values exist.
        for v in vals:
            q = v >> 1
            off = 5 * q
            c = (be[off] | (be[off + 1] << 8) | (be[off + 2] << 16)) & MASK
            ans += (c - 1) >> 1

    elif bo is not None:
        # Only odd values exist.
        for v in vals:
            q = v >> 1
            off = 5 * q
            c = (bo[off] | (bo[off + 1] << 8) | (bo[off + 2] << 16)) & MASK
            ans += (c - 1) >> 1

    return ans


def solve_fallback(data):
    parts = data.split()
    if not parts:
        return

    n = int(parts[0])
    vals = list(map(int, parts[1:1 + n]))
    del parts

    if n < 3:
        sys.stdout.write("0\n")
        return

    maxv = max(vals)

    even_count = 0
    for v in vals:
        if not (v & 1):
            even_count += 1

    odd_count = n - even_count

    # Sparse pair enumeration is preferable for modest pair counts.
    pairs = (
        even_count * (even_count - 1) // 2
        + odd_count * (odd_count - 1) // 2
    )

    if pairs <= 8_000_000:
        ans = _count_sparse(vals)
    else:
        ans = _count_bigint(vals, maxv, even_count, odd_count)

    sys.stdout.write(str(ans) + "\n")


def main():
    data = sys.stdin.buffer.read()
    if not data:
        return

    try:
        import numpy as np
        solve_numpy(data, np)
    except Exception:
        solve_fallback(data)


if __name__ == "__main__":
    main()