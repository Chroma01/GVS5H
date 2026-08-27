import sys

# Increase recursion depth just in case, though we use iterative FFT
sys.setrecursionlimit(2000)

def fft(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    
    length = 2
    while length <= n:
        ang = 2 * 3.141592653589793 / length * (-1 if invert else 1)
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = complex(1, 0)
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w
                a[i + j] = u + v
                a[i + j + length // 2] = u - v
                w *= wlen
        length <<= 1
    
    if invert:
        for i in range(n):
            a[i] /= n

def solve():
    import math
    
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
    
    # The maximum sum we need to consider is 2 * max_val.
    # The convolution size needs to be at least 2 * max_val + 1.
    # We need a power of 2 for FFT.
    size = 1
    while size <= 2 * max_val:
        size *= 2
    
    # Create polynomial P
    # P[i] = 1 if i is in S, else 0
    P = [complex(0, 0)] * size
    for x in S:
        P[x] = complex(1, 0)
    
    # FFT
    fft(P, False)
    
    # Point-wise square
    for i in range(size):
        P[i] *= P[i]
        
    # Inverse FFT
    fft(P, True)
    
    # Extract integer counts
    # Q[k] is the number of pairs (A, C) in S such that A + C = k
    # Since we used complex numbers, we round to nearest integer
    Q = [int(round(x.real)) for x in P]
    
    ans = 0
    for B in S:
        target_sum = 2 * B
        if target_sum < size:
            count_pairs = Q[target_sum]
            # count_pairs includes (B, B) if B is in S (which it is)
            # It also includes (A, C) and (C, A) for A != C.
            # We want pairs with A < C.
            # Number of pairs with A != C is count_pairs - 1 (subtracting (B,B))
            # Number of pairs with A < C is (count_pairs - 1) // 2
            if count_pairs > 0:
                ans += (count_pairs - 1) // 2
                
    print(ans)

if __name__ == '__main__':
    solve()