import sys

# Increase recursion depth just in case, though not needed for this iterative solution
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

    # Convert rows to integers (bitmasks)
    # We treat the string as a binary number. 
    # The problem statement says A_{i,j} is at column j.
    # Let's map the first character of the string to the most significant bit or least significant bit consistently.
    # Since we only care about XOR and popcount, the direction doesn't matter as long as it's consistent.
    # Let's map index 0 (leftmost) to bit W-1, index W-1 (rightmost) to bit 0.
    row_masks = []
    for r in rows:
        mask = 0
        for char in r:
            mask = (mask << 1) | int(char)
        row_masks.append(mask)

    # Count frequency of each row mask
    # There are 2^W possible masks.
    limit = 1 << W
    cnt = [0] * limit
    for m in row_masks:
        cnt[m] += 1

    # Precompute the cost function h[mask] = min(popcount(mask), W - popcount(mask))
    # This represents the cost for a single row if the column configuration is 'mask'
    # and the row itself is '0' (all zeros). 
    # Actually, the formula derived is: cost = sum over rows of min(popcount(row ^ col_mask), W - popcount(row ^ col_mask))
    # Let h[x] = min(popcount(x), W - popcount(x)).
    # Then total cost for a column mask C is sum_{r} cnt[r] * h[r ^ C].
    # This is the convolution of cnt and h under XOR.
    
    h = [0] * limit
    for i in range(limit):
        # Count set bits
        c = bin(i).count('1')
        h[i] = min(c, W - c)

    # Fast Walsh-Hadamard Transform (FWHT)
    # We need to compute (cnt * h)[C] = sum_{r} cnt[r] * h[r ^ C]
    # FWHT(cnt) * FWHT(h) point-wise, then Inverse FWHT.
    
    def fwht(a):
        n = len(a)
        if n == 1:
            return
        # Iterate over size of blocks
        length = 1
        while length < n:
            for i in range(0, n, length * 2):
                for j in range(i, i + length):
                    x = a[j]
                    y = a[j + length]
                    a[j] = x + y
                    a[j + length] = x - y
            length *= 2

    def ifwht(a):
        n = len(a)
        if n == 1:
            return
        length = 1
        while length < n:
            for i in range(0, n, length * 2):
                for j in range(i, i + length):
                    x = a[j]
                    y = a[j + length]
                    a[j] = (x + y) // 2
                    a[j + length] = (x - y) // 2
            length *= 2

    # Apply FWHT to cnt and h
    fwht(cnt)
    fwht(h)
    
    # Point-wise multiplication
    for i in range(limit):
        cnt[i] *= h[i]
    
    # Apply Inverse FWHT
    ifwht(cnt)

    # The answer is the minimum value in cnt array
    # Since we used integer arithmetic with subtraction, values might be negative before division?
    # No, FWHT with integer inputs produces integers. The division by 2 in ifwht is exact for this problem because the sum of products is always even?
    # Actually, standard FWHT for convolution:
    # Forward: a'[i] = sum (-1)^{|i & j|} a[j]
    # Inverse: a[i] = (1/N) sum (-1)^{|i & j|} a'[j]
    # The implementation above uses x+y and x-y which corresponds to the transform matrix.
    # The inverse divides by 2 at each step (or by N at the end).
    # Since we divide by 2 at each step in the loop, it's equivalent to dividing by N at the end.
    # The values should be non-negative integers.
    
    ans = min(cnt)
    print(ans)

if __name__ == '__main__':
    solve()