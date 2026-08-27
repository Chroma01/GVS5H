import sys
import numpy as np

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:1+N]))
    
    if N == 0:
        print(0)
        return
    
    max_val = max(A)
    max_sum = 2 * max_val
    
    # Frequency array
    cnt = np.zeros(max_sum + 1, dtype=np.int64)
    for x in A:
        cnt[x] += 1
    
    # Determine FFT size: next power of 2 greater than max_sum
    size = 1
    while size <= max_sum:
        size *= 2
    
    # Prepare arrays for FFT
    # We need to convolve cnt with itself
    # Create complex arrays for FFT
    fa = np.zeros(size, dtype=np.complex128)
    fa[:len(cnt)] = cnt.astype(np.float64)
    
    # FFT
    fa = np.fft.fft(fa)
    
    # Pointwise multiplication
    fa *= fa
    
    # Inverse FFT
    conv = np.fft.ifft(fa)
    
    # Extract real parts and round to nearest integer
    # conv[s] gives the number of ordered pairs (i,j) such that A[i] + A[j] = s
    conv_int = np.round(conv.real).astype(np.int64)
    
    # Now compute the answer
    # For each sum s, we need the number of pairs with i <= j
    # Let C[s] = conv_int[s]
    # If s is odd: pairs with i <= j = C[s] / 2
    # If s is even: let k = s // 2, pairs with i <= j = (C[s] + cnt[k]) / 2
    
    ans = 0
    
    # Precompute f(s) for all s from 2 to max_sum
    # f(s) = s >> (s & -s).bit_length() ... actually f(s) = s // (s & -s)
    # But we can compute it on the fly or precompute
    
    for s in range(2, max_sum + 1):
        c = conv_int[s]
        if c == 0:
            continue
        
        if s % 2 == 1:
            # Odd sum: all pairs have i != j
            num_pairs = c // 2
        else:
            # Even sum
            k = s // 2
            if k <= max_val:
                cnt_k = cnt[k]
            else:
                cnt_k = 0
            num_pairs = (c + cnt_k) // 2
        
        if num_pairs == 0:
            continue
        
        # Compute f(s): remove all factors of 2
        # f(s) = s / 2^v2(s) where v2(s) is the number of trailing zeros
        # Using bit manipulation: s & -s gives the lowest set bit
        # f(s) = s // (s & -s)
        low_bit = s & (-s)
        f_s = s // low_bit
        
        ans += num_pairs * f_s
    
    print(ans)

solve()