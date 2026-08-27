import sys
import math
import numpy as np

def odd_part(x):
    return x >> (x & -x).bit_length() - 1

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    max_a = max(A)
    size = 1
    while size < 2 * max_a + 1:
        size <<= 1
    
    freq = np.zeros(size, dtype=np.int64)
    for x in A:
        freq[x] += 1
    
    # FFT
    F = np.fft.fft(freq)
    F = F * F
    conv = np.fft.ifft(F).real
    conv = np.rint(conv).astype(np.int64)
    
    # diag sum
    diag = 0
    for x in A:
        diag += odd_part(x)
    
    total_ordered = 0
    M = 2 * max_a
    # Precompute odd_part for all possible sums? Too memory.
    # Compute on the fly
    for s in range(2, M + 1):
        c = conv[s]
        if c == 0:
            continue
        # odd_part(s)
        v = s
        # count trailing zeros
        tz = (v & -v).bit_length() - 1
        op = v >> tz
        total_ordered += op * c
    
    ans = (total_ordered + diag) // 2
    print(ans)

if __name__ == "__main__":
    main()