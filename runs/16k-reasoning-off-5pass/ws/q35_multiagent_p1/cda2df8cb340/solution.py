import numpy as np
import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:1+N]))
    
    # Maximum value of A_i is 10^7, so max sum is 2*10^7
    MAX_VAL = 10000000
    MAX_SUM = 2 * MAX_VAL
    
    # Precompute f(x) for all x from 1 to MAX_SUM
    # f(x) is the odd part of x
    # We can compute this using a sieve-like method
    f = [0] * (MAX_SUM + 1)
    for i in range(1, MAX_SUM + 1):
        f[i] = i
    
    for i in range(2, MAX_SUM + 1, 2):
        # For even numbers, divide by 2 until odd
        # But we can do this more efficiently:
        # f(2k) = f(k) if k is odd? No.
        # f(2k) = f(k) only if we keep dividing. Actually:
        # f(2k) = f(k) is not correct. f(4) = f(2) = f(1) = 1.
        # Let's use the property: f(2k) = f(k) if we define it recursively.
        # Actually, f(2k) = f(k) is true because dividing 2k by 2 gives k, and then we continue.
        # So f(2k) = f(k). This means we can compute f for all numbers by:
        # f[i] = f[i//2] if i is even, else i.
        pass
    
    # Recompute f efficiently
    f = [0] * (MAX_SUM + 1)
    f[1] = 1
    for i in range(2, MAX_SUM + 1):
        if i % 2 == 0:
            f[i] = f[i // 2]
        else:
            f[i] = i
    
    # Create frequency array
    # freq[v] = number of times v appears in A
    freq = [0] * (MAX_VAL + 1)
    for x in A:
        freq[x] += 1
    
    # Compute S_diag = sum_i f(2*A_i)
    S_diag = 0
    for x in A:
        S_diag += f[2 * x]
    
    # Use FFT to compute convolution of freq with itself
    # The convolution G = freq * freq will give G[s] = sum_{i+j=s} freq[i]*freq[j]
    # This counts all ordered pairs (i,j) such that A_i + A_j = s
    
    # Determine FFT size: need at least MAX_SUM + 1
    # Next power of 2 >= MAX_SUM + 1
    fft_size = 1
    while fft_size <= MAX_SUM:
        fft_size *= 2
    
    # Create arrays for FFT
    # freq array padded to fft_size
    freq_arr = np.zeros(fft_size, dtype=np.float64)
    for i in range(len(freq)):
        freq_arr[i] = freq[i]
    
    # Compute FFT
    freq_fft = np.fft.rfft(freq_arr)
    
    # Convolve by multiplying in frequency domain
    conv_fft = freq_fft * freq_fft
    
    # Inverse FFT
    conv = np.fft.irfft(conv_fft, n=fft_size)
    
    # Round to nearest integer since counts are integers
    conv = np.round(conv).astype(np.int64)
    
    # Compute S_all = sum_s G[s] * f[s]
    S_all = 0
    for s in range(2, MAX_SUM + 1):
        if conv[s] > 0:
            S_all += conv[s] * f[s]
    
    # The answer for i <= j is (S_all + S_diag) / 2
    ans = (S_all + S_diag) // 2
    
    print(ans)

solve()