import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    H = int(next(iterator))
    W = int(next(iterator))
    
    # Read the grid and convert each row to an integer bitmask
    # We'll treat the string as bits, where the first character is the most significant bit
    # or we can treat it as least significant. Let's be consistent.
    # Let's say A[i][0] is the leftmost character, which we'll map to bit (W-1)
    # So for row string s, row_int = sum(int(s[j]) * (1 << (W-1-j)) for j in range(W))
    
    freq = [0] * (1 << W)
    
    for _ in range(H):
        s = next(iterator)
        row_int = 0
        for j in range(W):
            if s[j] == '1':
                row_int |= (1 << (W - 1 - j))
        freq[row_int] += 1
    
    # Precompute G[m] = min(popcount(m), W - popcount(m))
    # We can compute popcount using bin(m).count('1')
    G = [0] * (1 << W)
    for m in range(1 << W):
        pc = bin(m).count('1')
        G[m] = min(pc, W - pc)
    
    # Fast Walsh-Hadamard Transform (XOR convolution)
    # FWHT for XOR: 
    # For each bit position i from 0 to W-1:
    #   For each block of size 2^(i+1):
    #     For each pair (a, b) in the block at positions (j, j+2^i):
    #       new_a = a + b
    #       new_b = a - b
    
    def fwht(arr):
        n = len(arr)
        h = 1
        while h < n:
            for i in range(0, n, h * 2):
                for j in range(i, i + h):
                    x = arr[j]
                    y = arr[j + h]
                    arr[j] = x + y
                    arr[j + h] = x - y
            h *= 2
    
    # Apply FWHT to F and G
    F = freq[:]
    fwht(F)
    fwht(G)
    
    # Pointwise multiply
    for i in range(1 << W):
        F[i] *= G[i]
    
    # Inverse FWHT: same as forward, then divide by 2^W
    fwht(F)
    n = 1 << W
    for i in range(n):
        F[i] //= n
    
    # The answer is the minimum value in F
    ans = min(F)
    print(ans)

solve()