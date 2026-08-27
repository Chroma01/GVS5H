import sys

def solve():
    # Increase recursion depth just in case, though we won't use recursion
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    
    # Read the grid rows
    rows_str = data[2:]
    
    # Convert each row string to an integer bitmask
    # The string is A_{i,1}...A_{i,W}. We treat it as a binary number.
    # Let's say index 0 is the most significant bit or least significant?
    # It doesn't matter as long as we are consistent.
    # Let's map A_{i,1} to bit (W-1) and A_{i,W} to bit 0.
    # Or simply: int(row_str, 2).
    
    freq = [0] * (1 << W)
    
    for s in rows_str:
        val = int(s, 2)
        freq[val] += 1
        
    # Precompute g[v] = min(popcount(v), W - popcount(v))
    # We can compute popcount for all v in 0..2^W-1
    limit = 1 << W
    g = [0] * limit
    
    # Efficient popcount for all numbers up to limit
    # Using bit_count() in Python 3.10+ is fast enough for 2^18
    for v in range(limit):
        pc = v.bit_count()
        g[v] = min(pc, W - pc)
        
    # FWHT implementation
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

    # Apply FWHT to freq and g
    fwht(freq)
    fwht(g)
    
    # Pointwise multiplication
    for i in range(limit):
        freq[i] *= g[i]
        
    # Inverse FWHT
    # The inverse transform is the same as forward, but we divide by n at the end
    fwht(freq)
    
    # Divide by 2^W
    # Since we are dealing with integers, and the result should be integer,
    # we can use integer division.
    n = limit
    for i in range(n):
        freq[i] //= n
        
    # The answer is the minimum value in the resulting array
    ans = min(freq)
    print(ans)

if __name__ == '__main__':
    solve()