import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    s = np.frombuffer(b" ".join(data[1:1 + n]), dtype=np.int64, sep=b" ")
    # Fallback in case frombuffer parsing fails (shouldn't happen)
    if s.size != n:
        s = np.array(list(map(int, data[1:1 + n])), dtype=np.int64)

    if n < 3:
        print(0)
        return

    m = int(s.max())

    size = 1
    while size < 2 * m + 1:
        size <<= 1

    f = np.zeros(size, dtype=np.float64)
    f[s] = 1.0

    F = np.fft.rfft(f)
    conv = np.fft.irfft(F * F, size)

    idx = 2 * s
    vals = np.rint(conv[idx]).astype(np.int64)
    ans = int(((vals - 1) // 2).sum())
    print(ans)

main()