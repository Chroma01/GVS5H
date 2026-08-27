import sys
from bisect import bisect_left, bisect_right

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S_x = int(next(iterator))
        S_y = int(next(iterator))
        
        houses = []
        for _ in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            houses.append((x, y))
            
        moves = []
        for _ in range(M):
            d = next(iterator)
            c = int(next(iterator))
            moves.append((d, c))
    except StopIteration:
        return

    # Group houses by X for vertical segments (U/D moves)
    # Key: X coordinate, Value: sorted list of Y coordinates
    houses_by_x = {}
    # Group houses by Y for horizontal segments (L/R moves)
    # Key: Y coordinate, Value: sorted list of X coordinates
    houses_by_y = {}
    
    for x, y in houses:
        if x not in houses_by_x:
            houses_by_x[x] = []
        houses_by_x[x].append(y)
        
        if y not in houses_by_y:
            houses_by_y[y] = []
        houses_by_y[y].append(x)
    
    # Sort the lists for binary search
    for x in houses_by_x:
        houses_by_x[x].sort()
    for y in houses_by_y:
        houses_by_y[y].sort()
        
    # Set to track visited houses to avoid double counting
    # We store the house coordinates as tuples
    visited_houses = set()
    count = 0
    
    # Current position
    curr_x = S_x
    curr_y = S_y
    
    for d, c in moves:
        if d == 'U':
            # Vertical segment: constant X = curr_x, Y from curr_y to curr_y + c
            new_y = curr_y + c
            x_const = curr_x
            y_min = min(curr_y, new_y)
            y_max = max(curr_y, new_y)
            
            # Check houses with this X coordinate
            if x_const in houses_by_x:
                y_list = houses_by_x[x_const]
                # Find indices of houses with Y in [y_min, y_max]
                left_idx = bisect_left(y_list, y_min)
                right_idx = bisect_right(y_list, y_max)
                
                # The houses in y_list[left_idx:right_idx] are on the segment
                # We need to mark them as visited and remove them from the list
                # to avoid reprocessing.
                if left_idx < right_idx:
                    # Extract the houses to be visited
                    houses_to_visit = []
                    for i in range(left_idx, right_idx):
                        houses_to_visit.append(y_list[i])
                    
                    # Remove these Y values from the list
                    # Since we are removing a contiguous block, we can slice
                    # But we need to be careful: the list might have duplicates? 
                    # No, houses are distinct, so Ys for a fixed X are distinct.
                    del houses_by_x[x_const][left_idx:right_idx]
                    
                    for y_val in houses_to_visit:
                        if (x_const, y_val) not in visited_houses:
                            visited_houses.add((x_const, y_val))
                            count += 1
            
            curr_y = new_y
            
        elif d == 'D':
            # Vertical segment: constant X = curr_x, Y from curr_y to curr_y - c
            new_y = curr_y - c
            x_const = curr_x
            y_min = min(curr_y, new_y)
            y_max = max(curr_y, new_y)
            
            if x_const in houses_by_x:
                y_list = houses_by_x[x_const]
                left_idx = bisect_left(y_list, y_min)
                right_idx = bisect_right(y_list, y_max)
                
                if left_idx < right_idx:
                    houses_to_visit = []
                    for i in range(left_idx, right_idx):
                        houses_to_visit.append(y_list[i])
                    
                    del houses_by_x[x_const][left_idx:right_idx]
                    
                    for y_val in houses_to_visit:
                        if (x_const, y_val) not in visited_houses:
                            visited_houses.add((x_const, y_val))
                            count += 1
            
            curr_y = new_y
            
        elif d == 'L':
            # Horizontal segment: constant Y = curr_y, X from curr_y to curr_y - c
            # Wait, L: (x, y) -> (x-c, y). Constant Y = curr_y, X varies.
            new_x = curr_x - c
            y_const = curr_y
            x_min = min(curr_x, new_x)
            x_max = max(curr_x, new_x)
            
            if y_const in houses_by_y:
                x_list = houses_by_y[y_const]
                left_idx = bisect_left(x_list, x_min)
                right_idx = bisect_right(x_list, x_max)
                
                if left_idx < right_idx:
                    houses_to_visit = []
                    for i in range(left_idx, right_idx):
                        houses_to_visit.append(x_list[i])
                    
                    del houses_by_y[y_const][left_idx:right_idx]
                    
                    for x_val in houses_to_visit:
                        if (x_val, y_const) not in visited_houses:
                            visited_houses.add((x_val, y_const))
                            count += 1
            
            curr_x = new_x
            
        elif d == 'R':
            # Horizontal segment: constant Y = curr_y, X from curr_y to curr_y + c
            new_x = curr_x + c
            y_const = curr_y
            x_min = min(curr_x, new_x)
            x_max = max(curr_x, new_x)
            
            if y_const in houses_by_y:
                x_list = houses_by_y[y_const]
                left_idx = bisect_left(x_list, x_min)
                right_idx = bisect_right(x_list, x_max)
                
                if left_idx < right_idx:
                    houses_to_visit = []
                    for i in range(left_idx, right_idx):
                        houses_to_visit.append(x_list[i])
                    
                    del houses_by_y[y_const][left_idx:right_idx]
                    
                    for x_val in houses_to_visit:
                        if (x_val, y_const) not in visited_houses:
                            visited_houses.add((x_val, y_const))
                            count += 1
            
            curr_x = new_x

    print(f"{curr_x} {curr_y} {count}")

if __name__ == '__main__':
    solve()