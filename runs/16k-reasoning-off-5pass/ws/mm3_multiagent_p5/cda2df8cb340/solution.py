import sys
import numpy as np

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    maxA = max(A)
    M = 2 * maxA + 1
    # size for FFT: next power of two >= M
    size = 1
    while size < M:
        size <<= 1
    # frequency array
    freq = np.zeros(size, dtype=np.int64)
    for x in A:
        freq[x] += 1
    # convolution using FFT (complex)
    # Using float64 for real part, complex128 for FFT
    f = freq.astype(np.complex128)
    F = np.fft.fft(f)
    F = F * F  # pointwise square
    conv = np.fft.ifft(F).real
    # round to nearest integer
    conv = np.rint(conv).astype(np.int64)
    # conv[S] now holds the number of ordered pairs (i,j) with A_i + A_j = S
    # We need the number of pairs with i <= j.
    # For i <= j, count = (conv[S] + diag[S]) // 2, where diag[S] is number of i with 2*A_i = S.
    # diag[S] = freq[S//2] if S even, else 0.
    # Build answer: sum_{S=2}^{2*maxA} ( (conv[S] + diag[S]) // 2 ) * f_odd(S)
    # f_odd(S) = S >> v2(S)
    # Precompute f_odd for all S up to 2*maxA
    odd_part = np.zeros(M, dtype=np.int64)
    for s in range(1, M):
        v = (s & -s).bit_length() - 1  # v2(s)
        odd_part[s] = s >> v
    # Compute diag array
    diag = np.zeros(M, dtype=np.int64)
    for s in range(0, M, 2):
        half = s // 2
        if half <= maxA:
            diag[s] = freq[half]
    # Compute total
    total = 0
    for s in range(2, M):
        c = (conv[s] + diag[s]) >> 1  # integer division by 2
        if c:
            total += c * odd_part[s]
    print(total)

if __name__ == "__main__":
    main()