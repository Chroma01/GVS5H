import sys
import numpy as np

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    if n < 3:
        print(0)
        return
    arr = np.fromiter(map(int, data[1:1 + n]), dtype=np.int64, count=n)
    M = int(arr.max())
    L = 1
    while L <= 2 * M:
        L <<= 1
    presence = np.zeros(L, dtype=np.float64)
    presence[arr] = 1.0
    F = np.fft.rfft(presence)
    conv = np.fft.irfft(F * F, n=L)
    conv = np.rint(conv).astype(np.int64)
    counts = conv[2 * arr]
    ans = (counts - 1) // 2
    print(int(ans.sum()))

if __name__ == "__main__":
    main()