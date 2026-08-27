import sys
import numpy as np

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # Maximum value of A_i is 10^7, so max sum is 2 * 10^7
    MAX_VAL = 10000000
    MAX_SUM = 2 * MAX_VAL
    
    # We need FFT size > MAX_SUM. Next power of 2 is 2^24 = 16777216
    # 2^24 = 16777216 > 20000000, so it's sufficient.
    FFT_SIZE = 1 << 24
    
    # Create frequency array
    # cnt[v] = number of times v appears in A
    cnt = np.zeros(FFT_SIZE, dtype=np.float64)
    for x in A:
        cnt[x] += 1.0
        
    # Perform FFT
    # Using numpy's FFT which is efficient
    F = np.fft.fft(cnt)
    
    # Square the spectrum (convolution in time domain)
    F_squared = F * F
    
    # Inverse FFT to get the convolution result
    conv = np.fft.ifft(F_squared)
    
    # Extract real parts, rounded to nearest integer
    # conv[s] should be approximately the number of ordered pairs (i,j) with A_i + A_j = s
    C = np.round(conv.real).astype(np.int64)
    
    # Now compute the answer
    # For each sum s, we need U[s] = (C[s] + D[s]) / 2
    # where D[s] = cnt[s//2] if s is even, else 0
    
    total_sum = 0
    
    # Precompute f(s) for s from 2 to MAX_SUM
    # f(s) = s / 2^(v2(s)) where v2(s) is the number of trailing zeros
    
    # We can compute f(s) efficiently
    # f(s) is the odd part of s
    
    # Iterate over all possible sums s from 2 to MAX_SUM
    # But MAX_SUM is 2*10^7, which is large but manageable in a simple loop if optimized
    
    # Let's create an array for f(s)
    # f[s] for s in range(MAX_SUM + 1)
    
    # To compute f(s) for all s up to 2*10^7:
    # f(s) = s if s is odd
    # f(s) = f(s/2) if s is even
    
    # We can use dynamic programming or just iterate
    f_arr = np.zeros(MAX_SUM + 1, dtype=np.int64)
    for s in range(1, MAX_SUM + 1):
        if s % 2 == 1:
            f_arr[s] = s
        else:
            f_arr[s] = f_arr[s // 2]
            
    # Now compute the total sum
    # U[s] = (C[s] + D[s]) / 2
    # D[s] = cnt[s//2] if s is even, else 0
    
    # Let's iterate and compute
    ans = 0
    
    # We only need to consider s from 2 to MAX_SUM
    # C[s] is the number of ordered pairs
    
    for s in range(2, MAX_SUM + 1):
        c_s = C[s]
        if c_s == 0:
            continue
            
        if s % 2 == 0:
            d_s = cnt[s // 2]
        else:
            d_s = 0
            
        u_s = (c_s + d_s) // 2
        
        if u_s > 0:
            ans += u_s * f_arr[s]
            
    print(ans)

solve()