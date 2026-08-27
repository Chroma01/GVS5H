import sys

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

    # Read the grid
    # Each row is a string of '0's and '1's
    rows = []
    for _ in range(H):
        rows.append(next(iterator))

    # Convert each row to an integer
    # The string is A_{i,1}...A_{i,W}, so we interpret it as a binary number
    # We'll treat the first character as the most significant bit or least significant?
    # It doesn't matter as long as we are consistent. Let's treat index 0 as bit 0 (LSB) or bit W-1.
    # Actually, for XOR convolution, the bit positions don't matter as long as they are aligned.
    # Let's just convert the string to an integer directly.
    # int("100", 2) = 4. This treats the first char as the highest power of 2.
    # This is fine.
    
    row_ints = []
    for r in rows:
        row_ints.append(int(r, 2))

    # Count frequency of each row pattern
    # There are 2^W possible patterns
    size = 1 << W
    count = [0] * size
    for r in row_ints:
        count[r] += 1

    # Precompute cost for each pattern: min(popcount, W - popcount)
    cost = [0] * size
    for i in range(size):
        pc = i.bit_count()
        cost[i] = min(pc, W - pc)

    # We want to compute S[C] = sum_{v} count[v] * cost[v ^ C]
    # This is the XOR convolution of count and cost.
    # S = count * cost (XOR convolution)
    
    # Apply FWHT to count and cost
    fwht(count)
    fwht(cost)
    
    # Pointwise multiplication
    for i in range(size):
        count[i] *= cost[i]
        
    # Inverse FWHT
    ifwt(count)
    
    # The answer is the minimum value in the resulting array
    # Note: After inverse FWHT, the values should be integers.
    # Due to division by 2^W, we need to round or ensure integer arithmetic.
    # Since we are dealing with counts, the result must be integer.
    # We'll use integer division.
    
    ans = min(count)
    print(ans)

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

def ifwt(arr):
    n = len(arr)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = arr[j]
                y = arr[j + h]
                arr[j] = (x + y) // 2
                arr[j + h] = (x - y) // 2
        h *= 2
    # The final division by n is already done in the loop above?
    # No, standard IFWHT divides by n at the end or during each step.
    # The loop above divides by 2 at each step, so after log2(n) steps, it divides by n.
    # So this is correct.

if __name__ == '__main__':
    solve()