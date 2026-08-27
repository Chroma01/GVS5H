import sys
import cmath

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = []
        for _ in range(N):
            S.append(int(next(iterator)))
    except StopIteration:
        return

    if N < 3:
        print(0)
        return

    # Find the maximum value to determine FFT size
    max_val = max(S)
    
    # We need to compute convolution of polynomial P(x) = sum(x^s) with itself.
    # The degree of P(x) is max_val. The degree of P(x)^2 is 2*max_val.
    # We need an FFT size that is a power of 2 and greater than 2*max_val.
    size = 1
    while size <= 2 * max_val:
        size *= 2
    
    # Create the polynomial coefficients (binary array)
    # a[i] = 1 if i is in S, else 0
    a = [0] * size
    for x in S:
        a[x] = 1
    
    # Precompute roots of unity and bit reversal
    # We will implement iterative FFT
    
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
            wlen = cmath.exp(complex(0, ang))
            
            for i in range(0, n, length):
                w = 1 + 0j
                for j in range(length // 2):
                    u = a[i + j]
                    v = a[i + j + length // 2] * w
                    a[i + j] = u + v
                    a[i + j + length // 2] = u - v
                    w *= wlen
            
            length *= 2

    # Perform FFT
    fft(a, False)
    
    # Point-wise square
    for i in range(len(a)):
        a[i] = a[i] * a[i]
    
    # Inverse FFT
    fft(a, True)
    
    # The result array 'a' now contains the coefficients of P(x)^2
    # a[k] is the number of pairs (x, y) such that x + y = k
    # We need to sum (a[2*B] - 1) for all B in S
    # Note: a[2*B] includes the case x=y=B, so we subtract 1.
    
    ans = 0
    for x in S:
        target = 2 * x
        if target < size:
            # Round to nearest integer to handle floating point errors
            count = int(round(a[target].real))
            ans += (count - 1)
            
    print(ans)

if __name__ == '__main__':
    solve()