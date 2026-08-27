import sys
import cmath

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

    if N < 3:
        print(0)
        return

    # Find the maximum value to determine polynomial size
    max_val = max(S)
    # The maximum sum of two elements is 2 * max_val
    # We need size to be a power of 2 greater than 2 * max_val
    size = 1
    while size <= 2 * max_val:
        size *= 2
    
    # Initialize polynomial coefficients
    # coeff[i] = 1 if i is in S, else 0
    coeff = [0] * size
    for x in S:
        coeff[x] = 1
    
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
            ang = 2 * cmath.pi / length * (-1 if invert else 1)
            wlen = cmath.exp(1j * ang)
            
            for i in range(0, n, length):
                w = 1 + 0j
                for j_inner in range(length // 2):
                    u = a[i + j_inner]
                    v = a[i + j_inner + length // 2] * w
                    a[i + j_inner] = u + v
                    a[i + j_inner + length // 2] = u - v
                    w *= wlen
            
            length *= 2

    # Perform FFT
    fft(coeff, False)
    
    # Square the polynomial in frequency domain
    for i in range(size):
        coeff[i] *= coeff[i]
    
    # Inverse FFT
    fft(coeff, True)
    
    # Calculate the answer
    # The coefficient at index k in the result represents the number of pairs (A, C) such that A + C = k
    # We need pairs where A + C = 2 * B for some B in S
    # Since A, B, C are distinct and A < B < C, we count pairs {A, C} with sum 2B.
    # The FFT gives ordered pairs (A, C) and (C, A). Since A != C, these are distinct.
    # We divide by 2 to get the number of sets {A, C}, which corresponds to one valid triplet (A, B, C).
    
    ans = 0
    for b in S:
        target = 2 * b
        if target < size:
            # The real part should be the count. Due to floating point errors, we round.
            count = int(round(coeff[target].real))
            ans += count // 2
            
    print(ans)

if __name__ == '__main__':
    solve()