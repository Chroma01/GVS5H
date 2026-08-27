import sys
import numpy as np

def solve() -> None:
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

    max_val = max(S)
    
    # Create indicator vector
    # Size needs to be at least max_val + 1 to index up to max_val
    # For convolution, we need size at least 2 * max_val + 1 to avoid wrap-around
    # We'll use FFT size as next power of 2 >= 2 * max_val + 1
    
    size = max_val + 1
    v = np.zeros(size, dtype=np.float64)
    for x in S:
        v[x] = 1.0
        
    # Determine FFT size
    # Convolution of two vectors of length L1 and L2 has length L1+L2-1
    # Here both are length 'size', so result length is 2*size - 1
    # We need FFT size >= 2*size - 1
    fft_size = 1
    while fft_size < 2 * size:
        fft_size *= 2
        
    # Pad v to fft_size
    v_padded = np.zeros(fft_size, dtype=np.float64)
    v_padded[:size] = v
    
    # Compute FFT
    V = np.fft.fft(v_padded)
    
    # Square the FFT result
    V_squared = V * V
    
    # Inverse FFT
    conv = np.fft.ifft(V_squared)
    
    # Extract real parts and round to nearest integer
    # The convolution result at index k gives the number of pairs (A, C) such that A + C = k
    conv_real = np.round(conv.real).astype(np.int64)
    
    total_fine_triplets = 0
    
    # For each B in S, the number of pairs (A, C) with A+C = 2B is conv_real[2*B]
    # This count includes (B, B) once, and (A, C) and (C, A) for A != C.
    # Since we want A < B < C, we need pairs where A != C and A != B and C != B.
    # Actually, since elements are distinct, A=C implies A=C=B.
    # So conv_real[2*B] = 1 (for A=B, C=B) + 2 * (number of pairs with A < B < C)
    # Thus, count for B = (conv_real[2*B] - 1) // 2
    
    for b in S:
        idx = 2 * b
        if idx < len(conv_real):
            count = conv_real[idx]
            if count > 1:
                total_fine_triplets += (count - 1) // 2
                
    print(total_fine_triplets)

if __name__ == '__main__':
    solve()