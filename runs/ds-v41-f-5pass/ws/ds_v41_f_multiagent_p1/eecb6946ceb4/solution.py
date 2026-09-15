import sys


def solve_numpy(S, n, np):
    maxS = max(S)
    # Need convolution length strictly greater than 2*maxS to avoid wraparound.
    L = 1
    while L <= 2 * maxS:
        L <<= 1
    arr = np.array(S, dtype=np.int64)
    f = np.zeros(L, dtype=np.float64)
    f[arr] = 1.0
    F = np.fft.rfft(f)
    conv = np.fft.irfft(F * F, L)
    conv = np.rint(conv).astype(np.int64)
    # conv[s] counts ordered pairs (x,y) in S with x+y=s.
    # For each B in S: (conv[2B]-1)//2 unordered distinct pairs.
    total = int(conv[2 * arr].sum())
    return (total - n) // 2


def solve_bigint(S, n):
    maxS = max(S)
    # Pack indicator into 3 bytes (24 bits) per value; coefficients < 2^24 so no carry.
    ba = bytearray(3 * (maxS + 1))
    for v in S:
        ba[3 * v] = 1
    X = int.from_bytes(ba, 'little')
    X2 = X * X
    data2 = X2.to_bytes(3 * (2 * maxS + 1), 'little')
    total = 0
    for B in S:
        o = 6 * B  # sum = 2B -> byte offset 3*(2B)
        total += data2[o] | (data2[o + 1] << 8) | (data2[o + 2] << 16)
    return (total - n) // 2


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    try:
        import numpy as np
        ans = solve_numpy(S, n, np)
    except ImportError:
        ans = solve_bigint(S, n)
    sys.stdout.write(str(ans) + "\n")


main()