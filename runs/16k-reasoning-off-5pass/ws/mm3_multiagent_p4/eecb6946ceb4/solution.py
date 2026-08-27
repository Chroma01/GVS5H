import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    # Convert the rest to numpy array of integers
    S = np.array(data[1:], dtype=np.int64)
    # Edge case: if N < 3, no triplets possible
    if N < 3:
        print(0)
        return
    
    max_val = int(S.max())
    # Size for FFT: next power of two >= 2*max_val + 1
    L = 1 << (2 * max_val).bit_length()
    
    # Build characteristic array f where f[x] = 1 if x in S, else 0
    f = np.zeros(L, dtype=np.float64)
    f[S] = 1.0
    
    # Compute convolution h = f * f using real FFT
    F = np.fft.rfft(f)
    h = np.fft.irfft(F * F, n=L)
    # Round to nearest integer (handles floating point errors)
    h = np.rint(h).astype(np.int64)
    
    # Boolean array for membership lookup
    present = np.zeros(L, dtype=bool)
    present[S] = True
    
    # For each even s = 2*B where B in S, add (h[s] - 1) // 2
    # Vectorized approach for speed
    s = np.arange(2, 2 * max_val + 1, 2, dtype=np.int64)
    h_s = h[s]
    pres = present[s // 2]
    
    # Extract only those s where s//2 is in S
    h_valid = h_s[pres]
    # Each h_valid is at least 1 (pair (B,B) exists), so (h_valid - 1) // 2 is valid
    ans = np.sum((h_valid - 1) // 2)
    
    print(int(ans))

if __name__ == "__main__":
    main()