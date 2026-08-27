import sys

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

    if N < 3:
        print(0)
        return

    # Determine the maximum value to size the FFT
    max_val = 0
    for x in S:
        if x > max_val:
            max_val = x
    
    # The polynomial degree needed is up to 2 * max_val.
    # We need a size that is a power of 2 and >= 2 * max_val + 1.
    limit = 2 * max_val + 1
    n_fft = 1
    while n_fft < limit:
        n_fft *= 2
    
    # Create the polynomial array
    # poly[i] = 1 if i in S, else 0
    poly = [0] * n_fft
    for x in S:
        poly[x] = 1
        
    # Iterative FFT implementation
    # Precompute roots of unity
    # We need roots for size n_fft
    # Using complex numbers
    
    # Bit-reversal permutation
    j = 0
    for i in range(1, n_fft):
        bit = n_fft >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            poly[i], poly[j] = poly[j], poly[i]
            
    # Cooley-Tukey iterative FFT
    length = 2
    while length <= n_fft:
        angle = 2 * 3.141592653589793 / length
        # w_len = complex(math.cos(angle), math.sin(angle))
        # To avoid importing math, we can compute cos/sin or use cmath
        # But cmath is standard. Let's import it.
        import cmath
        w_len = cmath.exp(cmath.rect(1, angle))
        
        for i in range(0, n_fft, length):
            w = 1 + 0j
            for j in range(length // 2):
                u = poly[i + j]
                v = poly[i + j + length // 2] * w
                poly[i + j] = u + v
                poly[i + j + length // 2] = u - v
                w *= w_len
        length <<= 2

    # Square the FFT coefficients
    for i in range(n_fft):
        poly[i] = poly[i] * poly[i]
        
    # Inverse FFT
    # Conjugate, FFT, conjugate, divide by n
    # Or use the standard inverse formula
    
    # Bit-reversal is already done, but we need to re-do it or just use the same permutation?
    # Actually, for inverse FFT, we can use the same bit-reversal if we handle the order correctly.
    # Standard approach: conjugate inputs, do forward FFT, conjugate outputs, divide by N.
    
    # Let's conjugate
    for i in range(n_fft):
        poly[i] = poly[i].conjugate()
        
    # Re-run bit reversal for inverse? 
    # The bit reversal permutation is symmetric. If we apply it again, we get original order?
    # No, the bit reversal permutation is its own inverse.
    # So we can just re-apply the bit reversal logic to put elements in correct order for inverse?
    # Actually, the standard iterative FFT code above assumes input is bit-reversed.
    # For inverse, we can just conjugate, run the same loop (with w_len conjugated or angle negated), then conjugate and divide.
    
    # Let's just negate the angle for inverse
    length = 2
    while length <= n_fft:
        angle = -2 * 3.141592653589793 / length
        w_len = cmath.exp(cmath.rect(1, angle))
        
        for i in range(0, n_fft, length):
            w = 1 + 0j
            for j in range(length // 2):
                u = poly[i + j]
                v = poly[i + j + length // 2] * w
                poly[i + j] = u + v
                poly[i + j + length // 2] = u - v
                w *= w_len
        length <<= 2
        
    # Conjugate and divide by n_fft
    for i in range(n_fft):
        poly[i] = poly[i].conjugate() / n_fft
        
    # Count the triplets
    ans = 0
    for b in S:
        # We want the coefficient of x^(2*b)
        idx = 2 * b
        if idx < n_fft:
            # The coefficient is the number of pairs (A, C) such that A + C = 2*b
            # This includes (b, b).
            # We need to subtract (b, b) and then divide by 2 to get unordered pairs {A, C} with A != C.
            # Since A < B < C implies A != C and A != B and C != B.
            # The pair (b, b) is the only case where A=C=B.
            # Pairs (A, C) with A != C are counted twice: (A, C) and (C, A).
            # We want the number of pairs with A < B < C.
            # Since A + C = 2B, if A < B then C > B.
            # So exactly half of the pairs with A != C satisfy A < B.
            val = round(poly[idx].real)
            # Subtract the (B, B) case
            val -= 1
            if val > 0:
                ans += val // 2
                
    print(ans)

if __name__ == '__main__':
    solve()