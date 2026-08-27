import sys
import numpy as np

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        print(0)
        return
    
    n = int(input_data[0])
    if n < 3:
        print(0)
        return
        
    s = []
    for i in range(1, n + 1):
        s.append(int(input_data[i]))
    
    # Find the maximum value to determine the size of our polynomial
    max_val = max(s)
    
    # Create a binary array where index i is 1 if i is in S, else 0
    # Size needs to be at least max_val + 1
    size_poly = max_val + 1
    poly = np.zeros(size_poly, dtype=np.float64)
    
    for val in s:
        poly[val] = 1.0
        
    # We need to compute the convolution of poly with itself.
    # The result will have degree up to 2 * max_val.
    # For FFT, we need size >= 2 * max_val + 1.
    # Find the smallest power of 2 >= 2 * max_val + 1
    fft_size = 1
    while fft_size < 2 * max_val + 1:
        fft_size *= 2
        
    # Pad the polynomial to fft_size
    poly_padded = np.zeros(fft_size, dtype=np.float64)
    poly_padded[:size_poly] = poly
    
    # Compute FFT
    fft_poly = np.fft.rfft(poly_padded)
    
    # Square the FFT (convolution in frequency domain)
    fft_conv = fft_poly * fft_poly
    
    # Inverse FFT to get the convolution result
    conv = np.fft.irfft(fft_conv, n=fft_size)
    
    # Round to nearest integers since we expect integer results
    conv = np.round(conv).astype(np.int64)
    
    # Now, for each B in S, the number of pairs (A, C) with A + C = 2*B is conv[2*B].
    # This includes the pair (B, B) which contributes 1.
    # Other pairs (A, C) with A != C appear twice (as (A,C) and (C,A)).
    # We want pairs with A < B < C.
    # For each B, the number of valid triplets is (conv[2*B] - 1) // 2.
    
    ans = 0
    s_set = set(s) # For quick lookup, though we iterate over s directly
    
    for b in s:
        idx = 2 * b
        if idx < len(conv):
            count = conv[idx]
            # Subtract 1 for the (B, B) pair
            # Divide by 2 to get unique pairs with A < C (which implies A < B < C)
            ans += (count - 1) // 2
            
    print(ans)

if __name__ == '__main__':
    solve()