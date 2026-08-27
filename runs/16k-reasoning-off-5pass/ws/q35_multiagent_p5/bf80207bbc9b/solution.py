import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    H = int(next(iterator))
    W = int(next(iterator))

    # Read the grid
    # Each row is a string of '0's and '1's
    # We'll convert each row to an integer bitmask
    freq = {}
    
    for _ in range(H):
        s = next(iterator)
        # Convert binary string to integer
        mask = int(s, 2)
        freq[mask] = freq.get(mask, 0) + 1

    # Precompute popcounts for all possible masks? 
    # Actually, we can compute on the fly using int.bit_count() which is efficient in Python 3.10+
    # But to be safe and fast, let's just use it directly.
    
    # Get all distinct masks and their frequencies
    distinct_masks = list(freq.keys())
    n_distinct = len(distinct_masks)
    
    # Total number of column flip configurations
    total_configs = 1 << W
    
    min_total_ones = float('inf')
    
    # For each column flip configuration m
    for m in range(total_configs):
        current_total = 0
        for mask in distinct_masks:
            # The transformed row mask after flipping columns according to m
            transformed = mask ^ m
            # Count number of 1s in transformed
            c = transformed.bit_count()
            # We can either keep the row as is (c ones) or flip it (W - c ones)
            current_total += freq[mask] * min(c, W - c)
        
        if current_total < min_total_ones:
            min_total_ones = current_total
            
    print(min_total_ones)

if __name__ == '__main__':
    solve()