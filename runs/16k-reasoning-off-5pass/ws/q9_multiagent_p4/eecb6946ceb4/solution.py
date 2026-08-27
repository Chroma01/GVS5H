import sys
import cmath

# Increase recursion depth just in case, though we use iterative FFT
sys.setrecursionlimit(2000)

def fft(a, invert):
    n = len(a)
    
    # Bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    
    # Iterative FFT
    length = 2
    while length <= n:
        ang = 2 * cmath.pi / length * (-1 if invert else 1)
        wlen = cmath.exp(1j * ang)
        for i in range(0, n, length):
            w = 1
            half_len = length // 2
            for k in range(half_len):
                u = a[i + k]
                v = a[i + k + half_len] * w
                a[i + k] = u + v
                a[i + k + half_len] = u - v
                w *= wlen
        length <<= 1
    
    if invert:
        for i in range(n):
            a[i] /= n

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        s = []
        for _ in range(n):
            s.append(int(next(iterator)))
    except StopIteration:
        return
    
    if n < 3:
        print(0)
        return

    max_val = 0
    for x in s:
        if x > max_val:
            max_val = x
    
    # We need to find pairs (A, C) such that A + C = 2*B.
    # The maximum sum is 2 * max_val.
    # Size must be a power of 2 and greater than 2 * max_val.
    size = 1
    while size <= 2 * max_val:
        size *= 2
    
    # Frequency array (indicator polynomial)
    # Using a list of complex numbers for FFT
    poly = [0j] * size
    for x in s:
        poly[x] = 1j # Using 1j or 1.0 works, just needs to be non-zero
    
    # FFT
    fft(poly, False)
    
    # Point-wise square
    for i in range(size):
        poly[i] *= poly[i]
    
    # Inverse FFT
    fft(poly, True)
    
    # Count triplets
    # poly[k] contains the number of pairs (A, C) such that A + C = k.
    # We need A < B < C and A + C = 2*B.
    # For a fixed B, the number of pairs (A, C) with A+C=2B is poly[2*B].
    # This count includes:
    # 1. The pair (B, B) where A=B and C=B.
    # 2. Pairs (A, C) and (C, A) which are distinct if A != C.
    # Since we want A < B < C, we need A != B and C != B, and A < C.
    # The number of valid pairs (A, C) with A < C is (poly[2*B] - 1) // 2.
    
    ans = 0
    for b in s:
        target = 2 * b
        if target < size:
            # Round to nearest integer to handle floating point errors
            count = int(round(poly[target].real))
            if count > 1:
                ans += (count - 1) // 2
    
    print(ans)

if __name__ == '__main__':
    solve()