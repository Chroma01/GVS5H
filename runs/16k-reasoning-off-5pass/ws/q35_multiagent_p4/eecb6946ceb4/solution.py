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

    max_val = 1000000
    # Determine the actual maximum value in S to size arrays appropriately
    # However, constraints say S_i <= 10^6, so we can use a fixed size or dynamic.
    # Using fixed size 10^6 + 1 is safe.
    limit = 1000000
    
    # Create a boolean array for existence check (not strictly needed for FFT but good for sanity)
    # We will use the FFT approach.
    
    # Find the maximum element to determine FFT size
    if S:
        max_s = max(S)
    else:
        max_s = 0
        
    # The convolution of two polynomials of degree max_s will have degree 2*max_s.
    # We need the next power of 2 greater than 2*max_s.
    # Max possible degree is 2,000,000. Next power of 2 is 2^21 = 2,097,152.
    fft_size = 1
    while fft_size <= 2 * max_s:
        fft_size *= 2
        
    # Create the polynomial P where P[i] = 1 if i in S, else 0
    # We use complex numbers for FFT
    P = np.zeros(fft_size, dtype=np.complex128)
    
    for x in S:
        P[x] = 1.0
        
    # Compute FFT
    P_fft = np.fft.fft(P)
    
    # Square the FFT result
    P_fft_squared = P_fft * P_fft
    
    # Inverse FFT to get the convolution
    Q = np.fft.ifft(P_fft_squared)
    
    # Q contains the counts. We only care about the real parts, rounded to integers.
    # Q[k] is the number of pairs (a, b) in S such that a + b = k.
    
    total_triplets = 0
    
    # For each B in S, we want to count pairs (A, C) such that A + C = 2*B.
    # This is given by Q[2*B].
    # However, Q[2*B] includes the pair (B, B) if B is in S (which it is).
    # It also counts (A, C) and (C, A) as distinct if A != C.
    # We want distinct A, B, C with A < B < C.
    # The number of such pairs for a fixed B is (Q[2*B] - 1) / 2.
    # Subtract 1 because (B, B) contributes 1 to the count but we need A != C.
    # Divide by 2 because (A, C) and (C, A) are both counted, but we only want A < C.
    
    # Extract real parts and round to nearest integer
    # Using np.round to handle floating point inaccuracies
    Q_int = np.round(Q.real).astype(np.int64)
    
    for b in S:
        idx = 2 * b
        if idx < fft_size:
            count_pairs = Q_int[idx]
            # Subtract the case A=C=B
            # Since B is in S, (B, B) is always counted in Q[2B]
            count_valid_pairs = count_pairs - 1
            # Each valid triplet corresponds to one pair (A, C) with A < C
            # The convolution counts both (A, C) and (C, A)
            if count_valid_pairs > 0:
                total_triplets += count_valid_pairs // 2
                
    print(total_triplets)

if __name__ == '__main__':
    solve()