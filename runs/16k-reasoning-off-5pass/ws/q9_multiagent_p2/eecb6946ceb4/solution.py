import sys
import math

# Increase recursion depth just in case, though we use iterative FFT
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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

    # If N < 3, no triplets possible
    if N < 3:
        print(0)
        return

    # Find the maximum value to determine the size of the polynomial
    max_val = max(S)
    
    # We need to compute the convolution of the indicator array with itself.
    # The size of the result array will be up to 2 * max_val.
    # We need a size that is a power of 2 and at least 2 * max_val + 1.
    size = 1
    while size <= 2 * max_val:
        size *= 2
    
    # Create the polynomial A(x) where coefficient of x^i is 1 if i in S, else 0
    # We use a list of complex numbers for FFT
    A = [0] * size
    for x in S:
        A[x] = 1.0 + 0j

    # Iterative FFT implementation
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
        
        # Butterfly operations
        length = 2
        while length <= n:
            # w_n = e^(i * 2 * PI / length)
            # For inverse, we use e^(-i * 2 * PI / length)
            angle = 2 * math.pi / length
            if invert:
                angle = -angle
            
            w_n = complex(math.cos(angle), math.sin(angle))
            
            w = complex(1, 0)
            for i in range(0, n, length):
                for j in range(length // 2):
                    u = a[i + j]
                    v = a[i + j + length // 2] * w
                    a[i + j] = u + v
                    a[i + j + length // 2] = u - v
                    w *= w_n
            length *= 2

    # Perform FFT on A
    fft(A, False)
    
    # Square the coefficients in frequency domain
    for i in range(size):
        A[i] *= A[i]
    
    # Perform Inverse FFT
    fft(A, True)
    
    # Calculate the answer
    ans = 0
    # We only care about B in S. For each B, the number of pairs (A, C) with A+C=2B
    # is given by the coefficient of x^(2B) in the convolution.
    # Since A and C are distinct and A < B < C, we have:
    # count = (coeff[2B] - 1) / 2
    # We subtract 1 because the pair (B, B) is counted (B+B=2B), but we need A != C.
    # We divide by 2 because (A, C) and (C, A) are both counted in the convolution.
    
    # Note: A[i] after IFFT might have small floating point errors.
    # We round to the nearest integer.
    
    for b in S:
        idx = 2 * b
        if idx < size:
            count = int(round(A[idx].real))
            if count > 0:
                ans += (count - 1) // 2
                
    print(ans)

if __name__ == '__main__':
    solve()