import sys

def solve():
    # Increase recursion depth just in case, though not needed here
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    
    # Read the grid rows
    rows_str = data[2:]
    
    # Convert each row string to an integer
    # We assume the input strings are contiguous 0s and 1s
    row_ints = []
    for s in rows_str:
        # Convert binary string to integer
        val = int(s, 2)
        row_ints.append(val)
        
    # Count frequency of each row pattern
    # There are at most 2^W distinct patterns, but practically min(H, 2^W)
    from collections import Counter
    counts = Counter(row_ints)
    
    # Precompute popcount for all numbers up to 2^W - 1
    # Since W <= 18, 2^18 = 262144
    limit = 1 << W
    popcounts = [0] * limit
    for i in range(limit):
        popcounts[i] = bin(i).count('1')
        
    # Precompute cost for each popcount: min(p, W-p)
    costs = [min(p, W - p) for p in popcounts]
    
    # Get distinct row values and their counts
    distinct_rows = list(counts.keys())
    distinct_counts = [counts[r] for r in distinct_rows]
    num_distinct = len(distinct_rows)
    
    min_total_sum = float('inf')
    
    # Iterate over all possible column flip masks
    # Mask M represents which columns are flipped (Operation Y)
    for mask in range(limit):
        current_sum = 0
        
        # For each distinct row pattern, calculate its contribution
        # The effective row value after column flips is r ^ mask
        # The cost is min(popcount(r ^ mask), W - popcount(r ^ mask))
        
        # Optimization: Use local variables for speed
        # In Python, function calls and attribute lookups are expensive.
        
        total = 0
        for i in range(num_distinct):
            r = distinct_rows[i]
            c = distinct_counts[i]
            
            # Effective row after column flips
            eff = r ^ mask
            
            # Get precomputed cost
            # cost = min(popcounts[eff], W - popcounts[eff])
            # But we precomputed costs array directly
            total += c * costs[eff]
            
        if total < min_total_sum:
            min_total_sum = total
            
    print(min_total_sum)

if __name__ == '__main__':
    solve()