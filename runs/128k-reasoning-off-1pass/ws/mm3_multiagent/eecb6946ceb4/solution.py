import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    if n < 3:
        print(0)
        return
    max_val = max(arr)
    # size must be power of two >= 2*max_val+1
    size = 1
    while size < 2 * max_val + 1:
        size <<= 1
    f = np.zeros(size, dtype=np.int8)
    f[arr] = 1
    # real FFT
    F = np.fft.rfft(f)
    G = F * F
    g = np.fft.irfft(G, n=size)
    # round to nearest integer
    g_int = np.rint(g).astype(np.int64)
    # sum over B in S: (g[2B] - 1) // 2
    # g_int is an array; we index it.
    # However, g_int size is `size`, and 2B <= 2*max_val < size.
    # Make sure we don't go out of bounds.
    # Compute total
    ans = 0
    for b in arr:
        idx = 2 * b
        # bounds check
        if idx >= len(g_int):
            continue
        c = int(g_int[idx])
        ans += (c - 1) // 2
    print(ans)

if __name__ == "__main__":
    main()