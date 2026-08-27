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

    # Preprocess houses into two dictionaries for efficient range queries
    # by_y: y -> sorted list of x coordinates
    # by_x: x -> sorted list of y coordinates
    by_y = {}
    by_x = {}
    
    for x, y in houses:
        if y not in by_y:
            by_y[y] = []
        by_y[y].append(x)
        
        if x not in by_x:
            by_x[x] = []
        by_x[x].append(y)
    
    # Sort the lists for binary search
    for y in by_y:
        by_y[y].sort()
    for x in by_x:
        by_x[x].sort()
    
    # Set to keep track of distinct houses visited
    visited_houses = set()
    
    # Current position
    cur_x = Sx
    cur_y = Sy
    
    # Process each move
    for d, c in moves:
        if d == 'U':
            # Move Up: (cur_x, cur_y) -> (cur_x, cur_y + c)
            new_y = cur_y + c
            # Horizontal coordinate is constant: cur_x
            # Vertical range: [min(cur_y, new_y), max(cur_y, new_y)]
            if cur_x in by_x:
                y_list = by_x[cur_x]
                low = min(cur_y, new_y)
                high = max(cur_y, new_y)
                
                # Find indices of houses with y in [low, high]
                left_idx = bisect_left(y_list, low)
                right_idx = bisect_right(y_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((cur_x, y_list[i]))
            
            cur_y = new_y
            
        elif d == 'D':
            # Move Down: (cur_x, cur_y) -> (cur_x, cur_y - c)
            new_y = cur_y - c
            # Horizontal coordinate is constant: cur_x
            # Vertical range: [min(cur_y, new_y), max(cur_y, new_y)]
            if cur_x in by_x:
                y_list = by_x[cur_x]
                low = min(cur_y, new_y)
                high = max(cur_y, new_y)
                
                # Find indices of houses with y in [low, high]
                left_idx = bisect_left(y_list, low)
                right_idx = bisect_right(y_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((cur_x, y_list[i]))
            
            cur_y = new_y
            
        elif d == 'L':
            # Move Left: (cur_x, cur_y) -> (cur_x - c, cur_y)
            new_x = cur_x - c
            # Vertical coordinate is constant: cur_y
            # Horizontal range: [min(cur_x, new_x), max(cur_x, new_x)]
            if cur_y in by_y:
                x_list = by_y[cur_y]
                low = min(cur_x, new_x)
                high = max(cur_x, new_x)
                
                # Find indices of houses with x in [low, high]
                left_idx = bisect_left(x_list, low)
                right_idx = bisect_right(x_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], cur_y))
            
            cur_x = new_x
            
        elif d == 'R':
            # Move Right: (cur_x, cur_y) -> (cur_x + c, cur_y)
            new_x = cur_x + c
            # Vertical coordinate is constant: cur_y
            # Horizontal range: [min(cur_x, new_x), max(cur_x, new_x)]
            if cur_y in by_y:
                x_list = by_y[cur_y]
                low = min(cur_x, new_x)
                high = max(cur_x, new_x)
                
                # Find indices of houses with x in [low, high]
                left_idx = bisect_left(x_list, low)
                right_idx = bisect_right(x_list, high)
                
                for i in range(left_idx, right_idx):
                    visited_houses.add((x_list[i], cur_y))
            
            cur_x = new_x

    # Output the final position and the count of distinct houses
    print(f"{cur_x} {cur_y} {len(visited_houses)}")

if __name__ == '__main__':
    solve()