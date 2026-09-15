import sys
from array import array


def try_numpy(vals, presence, max_val):
    try:
        import numpy as np
    except Exception:
        return None

    try:
        nfft = 1 << (2 * max_val).bit_length()
        if nfft < 1:
            nfft = 1

        arr = np.zeros(nfft, dtype=np.float64)
        arr[:max_val + 1] = np.frombuffer(presence, dtype=np.uint8, count=max_val + 1)

        spec = np.fft.rfft(arr)
        spec *= spec
        conv = np.fft.irfft(spec, n=nfft)

        conv = np.rint(conv).astype(np.int64)

        if vals.itemsize == 4:
            vals_np = np.frombuffer(vals, dtype=np.uint32)
        else:
            vals_np = np.frombuffer(vals.tobytes(), dtype=np.uint32)

        coeffs = conv[vals_np * 2]

        # For a present middle B, the true ordered-pair count is odd and at least 1.
        if np.any(coeffs < 1) or np.any((coeffs & 1) != 1):
            return None

        ans = np.sum((coeffs - 1) >> 1)
        return int(ans)
    except Exception:
        return None


def solve():
    data = sys.stdin.buffer.read()

    vals = array('I')
    presence = bytearray(1000001)

    max_val = 0
    num = 0
    in_num = False
    first = True

    for c in data:
        if c > 32:
            num = num * 10 + (c - 48)
            in_num = True
        elif in_num:
            if first:
                first = False
            else:
                vals.append(num)
                presence[num] = 1
                if num > max_val:
                    max_val = num
            num = 0
            in_num = False

    if in_num:
        if not first:
            vals.append(num)
            presence[num] = 1
            if num > max_val:
                max_val = num

    del data

    n = len(vals)
    if n < 3:
        sys.stdout.write("0\n")
        return

    # For small N, direct parity-split endpoint enumeration is faster and simpler.
    SMALL = 2000
    if n <= SMALL:
        even = []
        odd = []
        for x in vals:
            if x & 1:
                odd.append(x)
            else:
                even.append(x)

        ans = 0
        pres = presence

        for arr in (even, odd):
            L = len(arr)
            for i in range(L - 1):
                ai = arr[i]
                for j in range(i + 1, L):
                    if pres[(ai + arr[j]) >> 1]:
                        ans += 1

        sys.stdout.write(str(ans) + "\n")
        return

    ans = try_numpy(vals, presence, max_val)
    if ans is not None:
        sys.stdout.write(str(ans) + "\n")
        return

    # Exact pure-Python fallback.
    # Split endpoints by parity p.  For x = 2*t + p, use compressed index t.
    # If P_p(y) = sum y^t, then coefficient of y^(B-p) in P_p(y)^2 counts
    # ordered endpoint pairs of parity p with A + C = 2B.
    # The self-pair exists iff B-p is even.
    max_t = max_val >> 1
    in_len = (20 * (max_t + 1) + 7) // 8

    b0 = bytearray(in_len)  # even endpoints
    b1 = bytearray(in_len)  # odd endpoints
    has0 = False
    has1 = False

    # Pack each indicator as a 1-bit at bit offset 20*t.
    for x in vals:
        t = x >> 1
        off = 5 * (t >> 1)
        if t & 1:
            off += 2
            bit = 16
        else:
            bit = 1

        if x & 1:
            b1[off] |= bit
            has1 = True
        else:
            b0[off] |= bit
            has0 = True

    out_len = (20 * (max_val + 1) + 7) // 8

    if has0:
        p0 = int.from_bytes(b0, 'little')
        del b0
        q0 = p0 * p0
        del p0
        pb0 = q0.to_bytes(out_len, 'little')
        del q0
    else:
        pb0 = None

    if has1:
        p1 = int.from_bytes(b1, 'little')
        del b1
        q1 = p1 * p1
        del p1
        pb1 = q1.to_bytes(out_len, 'little')
        del q1
    else:
        pb1 = None

    del presence

    mask = (1 << 20) - 1
    ans = 0

    # Extract 20-bit fields from little-endian product bytes.
    # Field k even: starts at byte 5*(k//2), bit 0.
    # Field k odd : starts at byte 5*(k//2)+2, bit 4.
    if pb0 is not None and pb1 is not None:
        for B in vals:
            m = B >> 1
            if B & 1:
                # Even endpoints: coefficient at k = B = 2*m + 1.
                off = 5 * m + 2
                coeff = ((pb0[off] >> 4) |
                         (pb0[off + 1] << 4) |
                         (pb0[off + 2] << 12)) & mask
                ans += coeff >> 1

                # Odd endpoints: coefficient at k = B - 1 = 2*m.
                off = 5 * m
                coeff = (pb1[off] |
                         (pb1[off + 1] << 8) |
                         (pb1[off + 2] << 16)) & mask
                ans += (coeff - 1) >> 1
            else:
                # Even endpoints: coefficient at k = B = 2*m.
                off = 5 * m
                coeff = (pb0[off] |
                         (pb0[off + 1] << 8) |
                         (pb0[off + 2] << 16)) & mask
                ans += (coeff - 1) >> 1

                # Odd endpoints: coefficient at k = B - 1 = 2*m - 1.
                off = 5 * m - 3
                coeff = ((pb1[off] >> 4) |
                         (pb1[off + 1] << 4) |
                         (pb1[off + 2] << 12)) & mask
                ans += coeff >> 1

    elif pb0 is not None:
        # All values are even.
        for B in vals:
            off = 5 * (B >> 1)
            coeff = (pb0[off] |
                     (pb0[off + 1] << 8) |
                     (pb0[off + 2] << 16)) & mask
            ans += (coeff - 1) >> 1

    elif pb1 is not None:
        # All values are odd.
        for B in vals:
            off = 5 * (B >> 1)
            coeff = (pb1[off] |
                     (pb1[off + 1] << 8) |
                     (pb1[off + 2] << 16)) & mask
            ans += (coeff - 1) >> 1

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()