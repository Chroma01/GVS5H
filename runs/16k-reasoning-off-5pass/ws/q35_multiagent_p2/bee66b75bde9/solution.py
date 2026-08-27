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

    # We need to store the minimum required thresholds for each row and column
    # based on the black cells.
    # min_r[x] = max y such that (x, y) is black. If no black cell in row x, then 0.
    # min_c[y] = max x such that (x, y) is black. If no black cell in column y, then 0.
    
    # Since N can be up to 10^9, we use dictionaries.
    min_r = {}
    min_c = {}
    
    # Store all pre-colored cells to verify later
    cells = []
    
    for _ in range(M):
        x = int(next(iterator))
        y = int(next(iterator))
        c = next(iterator)
        cells.append((x, y, c))
        
        if c == 'B':
            # Update min_r for row x
            if x in min_r:
                if y > min_r[x]:
                    min_r[x] = y
            else:
                min_r[x] = y
                
            # Update min_c for column y
            if y in min_c:
                if x > min_c[y]:
                    min_c[y] = x
            else:
                min_c[y] = x

    # Now verify all pre-colored cells against the derived thresholds
    # For any row x not in min_r, min_r[x] is effectively 0.
    # For any column y not in min_c, min_c[y] is effectively 0.
    
    for (x, y, c) in cells:
        # Get the threshold for row x, default 0
        r_x = min_r.get(x, 0)
        # Get the threshold for column y, default 0
        c_y = min_c.get(y, 0)
        
        if c == 'B':
            # Black cell at (x, y) requires:
            # y <= r_x AND x <= c_y
            if not (y <= r_x and x <= c_y):
                print("No")
                return
        else: # c == 'W'
            # White cell at (x, y) requires:
            # y > r_x OR x > c_y
            if not (y > r_x or x > c_y):
                print("No")
                return
                
    print("Yes")

if __name__ == '__main__':
    solve()