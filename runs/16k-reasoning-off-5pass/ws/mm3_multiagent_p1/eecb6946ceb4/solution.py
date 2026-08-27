import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = list(map(int, data[1:]))
    maxV = max(S)
    # Determine FFT size: smallest power of two >= 2*maxV + 1
    size = 1
    while size < 2 * maxV + 1:
        size <<= 1
    # Create indicator array
    f = np.zeros(size, dtype=np.float64)
    for v in S:
        f[v] = 1.0
    # Compute convolution via FFT
    F = np.fft.fft(f)
    G = F * F
    g = np.fft.ifft(G).real
    g = np.round(g).astype(np.int64)
    # Count triplets
    ans = 0
    for B in S:
        s = 2 * B
        if s & 1:  # odd sum
            ans += g[s] // 2
        else:      # even sum
            # Subtract self-pair if s//2 is in S
            ans += (g[s] - int(f[s // 2])) // 2
    print(ans)

if __name__ == "__main__":
    main()