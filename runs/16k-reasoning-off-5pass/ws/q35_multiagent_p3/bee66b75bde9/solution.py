import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    N = int(next(iterator))
    M = int(next(iterator))
    
    # We'll use dictionaries to store R_min and C_min
    # R_min[i] = max column index of black cells in row i
    # C_min[j] = max row index of black cells in col j
    R_min = {}
    C_min = {}
    
    black_cells = []
    white_cells = []
    
    for _ in range(M):
        x = int(next(iterator))
        y = int(next(iterator))
        c = next(iterator)
        
        if c == 'B':
            black_cells.append((x, y))
            if x not in R_min or y > R_min[x]:
                R_min[x] = y
            if y not in C_min or x > C_min[y]:
                C_min[y] = x
        else:
            white_cells.append((x, y))
            
    # For rows/cols not in R_min/C_min, the value is 0.
    # We need to check each white cell (x, y):
    # Condition: R_min[x] < y OR C_min[y] < x
    # If R_min[x] is not present, it's 0. Since y >= 1, 0 < y is always True.
    # So if a row has no black cells, the condition is automatically satisfied for any white cell in that row.
    # Similarly for columns.
    
    possible = True
    for (x, y) in white_cells:
        r_val = R_min.get(x, 0)
        c_val = C_min.get(y, 0)
        
        # Check if the minimal configuration satisfies the white cell constraint
        # White cell (x, y) requires: r_x < y OR c_y < x
        if not (r_val < y or c_val < x):
            possible = False
            break
            
    if possible:
        print("Yes")
    else:
        print("No")

def iterator(data):
    global next
    idx = 0
    def get_next():
        nonlocal idx
        if idx < len(data):
            val = data[idx]
            idx += 1
            return val
        return None
    next = get_next

if __name__ == '__main__':
    solve()