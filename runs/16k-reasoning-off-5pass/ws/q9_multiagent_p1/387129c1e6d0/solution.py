import sys
from bisect import bisect_left, bisect_right

def solve():
    # Read all input from stdin efficiently
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

    # Organize houses by their coordinates for efficient lookup
    # houses_by_y[y] will store a sorted list of x-coordinates for houses at y
    # houses_by_x[x] will store a sorted list of y-coordinates for houses at x
    
    houses_by_y = {}
    houses_by_x = {}
    
    for x, y in houses:
        if y not in houses_by_y:
            houses_by_y[y] = []
        houses_by_y[y].append(x)
        
        if x not in houses_by_x:
            houses_by_x[x] = []
        houses_by_x[x].append(y)
        
    # Sort the lists for binary search
    for y in houses_by_y:
        houses_by_y[y].sort()
    for x in houses_by_x:
        houses_by_x[x].sort()
        
    # Set to store distinct houses visited (store as tuples)
    visited_houses = set()
    
    # Current position
    curr_x, curr_y = S_x, S_y
    
    # Process each move
    for d, c in moves:
        if d == 'U':
            # Move Up: (curr_x, curr_y) -> (curr_x, curr_y + c)
            target_y = curr_y + c
            if curr_x in houses_by_x:
                y_list = houses_by_x[curr_x]
                low = min(curr_y, target_y)
                high = max(curr_y, target_y)
                
                left_idx = bisect_left(y_list, low)
                right_idx = bisect_right(y_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((curr_x, y_list[i]))
                    
        elif d == 'D':
            # Move Down: (curr_x, curr_y) -> (curr_x, curr_y - c)
            target_y = curr_y - c
            if curr_x in houses_by_x:
                y_list = houses_by_x[curr_x]
                low = min(curr_y, target_y)
                high = max(curr_y, target_y)
                
                left_idx = bisect_left(y_list, low)
                right_idx = bisect_right(y_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((curr_x, y_list[i]))
                    
        elif d == 'L':
            # Move Left: (curr_x, curr_y) -> (curr_x - c, curr_y)
            target_x = curr_x - c
            if curr_y in houses_by_y:
                x_list = houses_by_y[curr_y]
                low = min(curr_x, target_x)
                high = max(curr_x, target_x)
                
                left_idx = bisect_left(x_list, low)
                right_idx = bisect_right(x_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], curr_y))
                    
        elif d == 'R':
            # Move Right: (curr_x, curr_y) -> (curr_x + c, curr_y)
            target_x = curr_x + c
            if curr_y in houses_by_y:
                x_list = houses_by_y[curr_y]
                low = min(curr_x, target_x)
                high = max(curr_x, target_x)
                
                left_idx = bisect_left(x_list, low)
                right_idx = bisect_right(x_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], curr_y))
        
        # Update current position
        if d == 'U':
            curr_y += c
        elif d == 'D':
            curr_y -= c
        elif d == 'L':
            curr_x -= c
        elif d == 'R':
            curr_x += c
            
    print(f"{curr_x} {curr_y} {len(visited_houses)}")

if __name__ == '__main__':
    solve()