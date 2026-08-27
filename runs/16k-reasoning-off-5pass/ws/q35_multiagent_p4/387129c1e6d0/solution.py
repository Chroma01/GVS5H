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
        Sx = int(next(iterator))
        Sy = int(next(iterator))
    except StopIteration:
        return

    # Store houses in two dictionaries for efficient lookup
    # houses_by_x: x -> sorted list of y's
    # houses_by_y: y -> sorted list of x's
    houses_by_x = {}
    houses_by_y = {}
    
    # Set to keep track of visited houses to count distinct ones
    visited_houses = set()
    
    for _ in range(N):
        x = int(next(iterator))
        y = int(next(iterator))
        
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
        
    # Current position of Santa
    cur_x = Sx
    cur_y = Sy
    
    # Process each move
    for _ in range(M):
        D = next(iterator)
        C = int(next(iterator))
        
        if D == 'U':
            # Move up: y increases
            new_y = cur_y + C
            # Check for houses on vertical segment from (cur_x, cur_y) to (cur_x, new_y)
            # x is fixed at cur_x, y ranges from min(cur_y, new_y) to max(cur_y, new_y)
            if cur_x in houses_by_x:
                y_list = houses_by_x[cur_x]
                y_min = min(cur_y, new_y)
                y_max = max(cur_y, new_y)
                
                # Find indices in y_list that are within [y_min, y_max]
                left_idx = bisect_left(y_list, y_min)
                right_idx = bisect_right(y_list, y_max)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((cur_x, y_list[i]))
            
            cur_y = new_y
            
        elif D == 'D':
            # Move down: y decreases
            new_y = cur_y - C
            # Check for houses on vertical segment from (cur_x, cur_y) to (cur_x, new_y)
            if cur_x in houses_by_x:
                y_list = houses_by_x[cur_x]
                y_min = min(cur_y, new_y)
                y_max = max(cur_y, new_y)
                
                left_idx = bisect_left(y_list, y_min)
                right_idx = bisect_right(y_list, y_max)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((cur_x, y_list[i]))
            
            cur_y = new_y
            
        elif D == 'L':
            # Move left: x decreases
            new_x = cur_x - C
            # Check for houses on horizontal segment from (cur_x, cur_y) to (new_x, cur_y)
            # y is fixed at cur_y, x ranges from min(cur_x, new_x) to max(cur_x, new_x)
            if cur_y in houses_by_y:
                x_list = houses_by_y[cur_y]
                x_min = min(cur_x, new_x)
                x_max = max(cur_x, new_x)
                
                left_idx = bisect_left(x_list, x_min)
                right_idx = bisect_right(x_list, x_max)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], cur_y))
            
            cur_x = new_x
            
        elif D == 'R':
            # Move right: x increases
            new_x = cur_x + C
            # Check for houses on horizontal segment from (cur_x, cur_y) to (new_x, cur_y)
            if cur_y in houses_by_y:
                x_list = houses_by_y[cur_y]
                x_min = min(cur_x, new_x)
                x_max = max(cur_x, new_x)
                
                left_idx = bisect_left(x_list, x_min)
                right_idx = bisect_right(x_list, x_max)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], cur_y))
            
            cur_x = new_x
            
    # Output the final position and the number of distinct houses visited
    print(f"{cur_x} {cur_y} {len(visited_houses)}")

if __name__ == '__main__':
    solve()