import sys

def solve():
    # Read all input at once
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
    # Each row is a string of '0's and '1's
    # We convert each row to an integer bitmask
    # A_{i,j} corresponds to the j-th bit (0-indexed from left to right)
    # Let's say the string is s, then bitmask = int(s, 2)
    
    row_masks = []
    for _ in range(H):
        s = next(iterator)
        # Convert binary string to integer
        mask = int(s, 2)
        row_masks.append(mask)
        
    # Count frequency of each unique row mask
    # Using a dictionary to store counts
    counts = {}
    for mask in row_masks:
        if mask in counts:
            counts[mask] += 1
        else:
            counts[mask] = 1
            
    # Precompute popcount for all possible values up to 2^W - 1
    # Actually, we can just use int.bit_count() which is efficient in Python 3.10+
    # But to be safe and potentially faster in a tight loop, we can precompute
    # However, int.bit_count() is implemented in C and very fast.
    # Let's use it directly.
    
    # The number of unique masks
    unique_masks = list(counts.keys())
    num_unique = len(unique_masks)
    
    # Precompute popcount for all 2^W values might be useful if we iterate differently,
    # but here we compute popcount(m ^ col_mask) for each pair.
    # Since W <= 18, 2^W = 262144.
    # We can precompute popcount for all x in [0, 2^W - 1]
    limit = 1 << W
    popcounts = [0] * limit
    for i in range(limit):
        popcounts[i] = i.bit_count()
        
    min_total_ones = float('inf')
    
    # Iterate over all possible column flip masks
    for col_mask in range(limit):
        current_total = 0
        for mask in unique_masks:
            # The effective row after column flips is mask ^ col_mask
            effective = mask ^ col_mask
            # Number of 1s in the effective row
            ones = popcounts[effective]
            # We can flip the row or not.
            # If we don't flip, cost is ones.
            # If we flip, cost is W - ones.
            # We take the minimum.
            cost = ones if ones < W - ones else W - ones
            current_total += counts[mask] * cost
            
        if current_total < min_total_ones:
            min_total_ones = current_total
            
    print(min_total_ones)

if __name__ == '__main__':
    solve()