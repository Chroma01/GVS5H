import sys


def solve_bigint(S, maxS):
    # X = sum_{x in S} 2^(20*x)
    xlen = (20 * maxS >> 3) + 1
    xb = bytearray(xlen)
    for x in S:
        p = 20 * x
        xb[p >> 3] |= 1 << (p & 7)
    X = int.from_bytes(xb, 'little')
    P = X * X

    # product fits in <= 40*maxS + 2 bits; need byte index up to 5*maxS + 2
    plen = 5 * maxS + 5
    Y = P.to_bytes(plen, 'little')

    ans = 0
    for B in S:
        i = 5 * B  # byte offset of bit 20*(2B) = 40*B
        c = Y[i] | (Y[i + 1] << 8) | ((Y[i + 2] & 0x0F) << 16)
        ans += (c - 1) >> 1
    return ans


def solve_numpy(np, data, n):
    S_np = np.fromiter(map(int, data[1:1 + n]), dtype=np.int64, count=n)
    maxS = int(S_np.max())

    # L = smallest power of two strictly greater than 2*maxS
    L = 1
    while L <= 2 * maxS:
        L <<= 1

    arr = np.zeros(L, dtype=np.float64)
    arr[S_np] = 1.0

    F = np.fft.rfft(arr)
    conv = np.fft.irfft(F * F, L)
    conv = np.rint(conv).astype(np.int64)

    coeffs = conv[2 * S_np]
    return int(np.sum((coeffs - 1) // 2))


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n < 3:
        sys.stdout.write("0\n")
        return

    try:
        import numpy as np
        ans = solve_numpy(np, data, n)
    except ImportError:
        S = list(map(int, data[1:1 + n]))
        ans = solve_bigint(S, max(S))

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()