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
    
    # Read grid rows
    # Each row is a string of '0' and '1'
    # We convert each row to an integer bitmask
    # The j-th character (0-indexed) corresponds to the j-th bit (0-indexed)
    # We'll treat the string as a binary number where the first char is the most significant bit
    # or least significant? It doesn't matter as long as it's consistent.
    # Let's say index 0 of string is bit W-1, index W-1 is bit 0.
    
    row_counts = [0] * (1 << W)
    
    for _ in range(H):
        s = next(iterator)
        val = 0
        for char in s:
            val = (val << 1) | int(char)
        row_counts[val] += 1
        
    n = 1 << W
    
    # Prepare array A: frequency of each row pattern
    A = list(row_counts)
    
    # Prepare array B: cost for a single row if the column flip mask is 'mask'
    # B[mask] = min(popcount(mask), W - popcount(mask))
    # This represents the cost contribution of ONE row with pattern 0 (all zeros)
    # if we apply column flips 'mask'.
    # Wait, the convolution logic:
    # We want sum over r of (count[r] * cost(r, c))
    # cost(r, c) = min(popcount(r ^ c), W - popcount(r ^ c))
    # Let B[x] = min(popcount(x), W - popcount(x))
    # Then cost(r, c) = B[r ^ c]
    # The sum is sum_r (A[r] * B[r ^ c])
    # This is exactly the XOR convolution of A and B.
    
    B = [0] * n
    for i in range(n):
        # Count bits in i
        cnt = bin(i).count('1')
        B[i] = min(cnt, W - cnt)
        
    # Fast Walsh-Hadamard Transform (FWHT) for XOR
    def fwht(a):
        length = len(a)
        h = 1
        while h < length:
            for i in range(0, length, h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = x + y
                    a[j + h] = x - y
            h *= 2
            
    def ifwht(a):
        length = len(a)
        h = 1
        while h < length:
            for i in range(0, length, h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = (x + y) // 2
                    a[j + h] = (x - y) // 2
            h *= 2

    # Transform A and B
    fwht(A)
    fwht(B)
    
    # Pointwise multiplication
    C = [A[i] * B[i] for i in range(n)]
    
    # Inverse transform
    ifwht(C)
    
    # The answer is the minimum value in C
    # Note: C[i] should be the total minimum cost for column configuration i
    ans = min(C)
    
    print(ans)

if __name__ == '__main__':
    solve()