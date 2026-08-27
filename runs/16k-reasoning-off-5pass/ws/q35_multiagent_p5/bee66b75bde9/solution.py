import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # We need to store min_R and min_C. Since N can be up to 10^9, we use dictionaries.
    # min_R[r] stores the maximum Y coordinate of a black cell in row r.
    # min_C[c] stores the maximum X coordinate of a black cell in column c.
    min_R = {}
    min_C = {}
    
    # Store black and white cells separately for processing
    black_cells = []
    white_cells = []
    
    for _ in range(M):
        x = int(next(iterator))
        y = int(next(iterator))
        c = next(iterator)
        
        if c == 'B':
            black_cells.append((x, y))
        else:
            white_cells.append((x, y))
            
    # Process black cells to determine minimum required thresholds
    for x, y in black_cells:
        # Update min_R for row x
        if x in min_R:
            if y > min_R[x]:
                min_R[x] = y
        else:
            min_R[x] = y
            
        # Update min_C for column y
        if y in min_C:
            if x > min_C[y]:
                min_C[y] = x
        else:
            min_C[y] = x
            
    # Process white cells to check consistency
    # For a white cell at (x, y), it must NOT be black.
    # A cell (x, y) is black if y <= min_R[x] AND x <= min_C[y].
    # So it is white if y > min_R[x] OR x > min_C[y].
    # Note: if a row/col has no black cells, min_R[x] or min_C[y] is effectively 0.
    
    for x, y in white_cells:
        # Get the threshold for row x, default to 0 if not present
        r_threshold = min_R.get(x, 0)
        # Get the threshold for column y, default to 0 if not present
        c_threshold = min_C.get(y, 0)
        
        # Check if the cell would be black under these thresholds
        # It is black if y <= r_threshold AND x <= c_threshold
        is_black = (y <= r_threshold) and (x <= c_threshold)
        
        if is_black:
            print("No")
            return
            
    # If all white cells are consistent
    print("Yes")

if __name__ == '__main__':
    solve()