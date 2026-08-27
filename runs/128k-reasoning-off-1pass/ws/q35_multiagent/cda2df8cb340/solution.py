import sys
import numpy as np

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A = list(map(int, input_data[1:1+N]))
    
    # Find maximum value to determine the size of frequency array
    M = max(A)
    max_sum = 2 * M
    
    # Create frequency array for values in A
    # cnt[v] = number of times value v appears in A
    cnt = [0] * (M + 1)
    for x in A:
        cnt[x] += 1
        
    # We need to compute the convolution of cnt with itself
    # The result C[s] will be the number of ordered pairs (i,j) such that A_i + A_j = s
    # Using FFT for efficient convolution
    
    # Determine the size for FFT (next power of 2 >= 2*M + 1)
    fft_size = 1
    while fft_size < 2 * M + 1:
        fft_size *= 2
        
    # Create arrays for FFT
    # Pad cnt to fft_size
    cnt_array = np.zeros(fft_size, dtype=np.float64)
    for i in range(M + 1):
        cnt_array[i] = cnt[i]
        
    # Compute FFT
    fft_cnt = np.fft.fft(cnt_array)
    
    # Point-wise multiplication (convolution in frequency domain)
    fft_product = fft_cnt * fft_cnt
    
    # Inverse FFT to get the convolution result
    conv_result = np.fft.ifft(fft_product)
    
    # Extract the real parts and round to nearest integer
    # C[s] = number of ordered pairs (i,j) with A_i + A_j = s
    C = [int(round(conv_result[s].real)) for s in range(2 * M + 1)]
    
    # Precompute f(s) for all s from 2 to 2*M
    # f(s) is the odd part of s, i.e., s / 2^k where 2^k is the highest power of 2 dividing s
    f = [0] * (2 * M + 1)
    for s in range(2, 2 * M + 1):
        temp = s
        while temp % 2 == 0:
            temp //= 2
        f[s] = temp
        
    # Compute the answer
    # For each sum s, count the number of pairs (i,j) with i <= j such that A_i + A_j = s
    # C[s] counts all ordered pairs (i,j) with A_i + A_j = s
    # For i <= j:
    #   - If s is even and s/2 is in A, the diagonal term (i=j) appears once in C[s]
    #   - Off-diagonal terms appear twice in C[s]
    # So number of pairs with i <= j is (C[s] + (cnt[s//2] if s is even and s//2 <= M else 0)) // 2
    
    ans = 0
    for s in range(2, 2 * M + 1):
        if C[s] == 0:
            continue
            
        # Count diagonal terms: if s is even and s/2 is a valid value in A
        if s % 2 == 0:
            half = s // 2
            if half <= M:
                diagonal = cnt[half]
            else:
                diagonal = 0
        else:
            diagonal = 0
            
        num_pairs = (C[s] + diagonal) // 2
        ans += f[s] * num_pairs
        
    print(ans)

solve()