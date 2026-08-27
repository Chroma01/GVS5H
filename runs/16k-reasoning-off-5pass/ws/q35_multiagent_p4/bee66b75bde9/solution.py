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

    # We need to store constraints for each row and column.
    # R_min[r] = minimum valid R_r (number of black cells in row r from left)
    # C_min[c] = minimum valid C_c (number of black cells in col c from top)
    # Since N can be up to 10^9, we cannot use arrays of size N.
    # We will use dictionaries to store only the rows/cols that have black cells.
    
    R_min = {}
    C_min = {}
    
    # Store white cells to verify later
    white_cells = []
    
    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        color = next(iterator)
        
        if color == 'B':
            # Update lower bound for row r
            if r not in R_min or c > R_min[r]:
                R_min[r] = c
            
            # Update lower bound for column c
            if c not in C_min or r > C_min[c]:
                C_min[c] = r
        else:
            # Store white cell for verification
            white_cells.append((r, c))
            
    # Now verify all white cells
    # For a white cell (r, c), we must have:
    # c > R_r OR r > C_c
    # Where R_r is the final chosen value for row r, and C_c for column c.
    # As reasoned, we choose R_r = R_min[r] if r in R_min else 0
    # and C_c = C_min[c] if c in C_min else 0.
    
    for (r, c) in white_cells:
        # Get the effective R_r and C_c
        r_val = R_min.get(r, 0)
        c_val = C_min.get(c, 0)
        
        # Check if the white cell is incorrectly classified as black
        # A cell is black if c <= R_r AND r <= C_c
        # So it is white if c > R_r OR r > C_c
        # If it fails this, it means c <= R_r AND r <= C_c, which contradicts it being white.
        if c <= r_val and r <= c_val:
            print("No")
            return
            
    # If all white cells are satisfied, then a valid configuration exists.
    # The black cells are satisfied by construction of R_min and C_min.
    print("Yes")

if __name__ == '__main__':
    solve()