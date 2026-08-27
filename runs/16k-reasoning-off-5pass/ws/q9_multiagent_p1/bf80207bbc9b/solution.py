import sys

# Increase recursion depth just in case, though we use iterative FWHT
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read the grid rows
    # Each row is a string of '0' and '1'
    rows = []
    for _ in range(H):
        rows.append(next(iterator))

    # We need to count the frequency of each row pattern.
    # Since W is small (<= 18), we can represent each row as an integer.
    # The mask will have the j-th bit set if the j-th character is '1'.
    
    cnt = [0] * (1 << W)
    
    for r in rows:
        mask = 0
        for char in r:
            if char == '1':
                mask = (mask << 1) | 1
            else:
                mask = mask << 1
        cnt[mask] += 1

    N = 1 << W
    
    # Precompute the cost for each column mask if we were to flip rows optimally
    # For a fixed column mask 'c', the cost contributed by a row 'r' is:
    # min(popcount(r ^ c), W - popcount(r ^ c))
    # However, we can't just precompute this for all pairs directly in O(N^2).
    # We use FWHT (Fast Walsh-Hadamard Transform) to compute the convolution.
    
    # Let A[mask] = cnt[mask]
    # Let B[mask] = min(popcount(mask), W - popcount(mask))
    # We want to compute C[c] = sum_{r} cnt[r] * B[r ^ c]
    # This is exactly the XOR convolution of A and B.
    # C = A *_{XOR} B
    
    # Step 1: Prepare array B
    B = [0] * N
    for mask in range(N):
        # Count set bits
        bits = bin(mask).count('1')
        # The cost for a row with pattern 'mask' against column flips '0'
        # is min(bits, W - bits).
        # Wait, the logic is:
        # If we choose column flips C, then for a row R, the resulting row has bits = popcount(R ^ C).
        # We can flip the row to minimize 1s. So cost is min(popcount(R ^ C), W - popcount(R ^ C)).
        # In the convolution formula: C[C] = sum_R cnt[R] * cost(R, C)
        # cost(R, C) = min(popcount(R ^ C), W - popcount(R ^ C))
        # Let X = R ^ C. Then cost is min(popcount(X), W - popcount(X)).
        # So B[X] = min(popcount(X), W - popcount(X)).
        # Then C[C] = sum_R cnt[R] * B[R ^ C].
        # This matches the XOR convolution definition.
        
        B[mask] = min(bits, W - bits)

    # Step 2: Apply FWHT to A and B
    # FWHT definition: H(A)[i] = sum_j A[j] * (-1)^(popcount(i & j))
    # Iterative FWHT
    
    def fwht(a):
        n = len(a)
        h = 1
        while h < n:
            for i in range(0, n, h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = x + y
                    a[j + h] = x - y
            h *= 2
        return a

    def ifwht(a):
        n = len(a)
        h = 1
        while h < n:
            for i in range(0, n, h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = (x + y) // 2
                    a[j + h] = (x - y) // 2
            h *= 2
        return a

    # Transform A
    A = list(cnt)
    fwht(A)
    
    # Transform B
    B_t = list(B)
    fwht(B_t)
    
    # Pointwise multiplication
    C = [A[i] * B_t[i] for i in range(N)]
    
    # Inverse Transform
    ifwht(C)
    
    # The result C[c] is the total sum of 1s for column configuration c.
    # We need the minimum value.
    ans = min(C)
    
    print(ans)

if __name__ == '__main__':
    solve()