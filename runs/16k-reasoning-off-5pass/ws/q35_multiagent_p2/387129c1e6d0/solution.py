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

    # Group houses by y-coordinate for horizontal moves
    # by_y[y] = sorted list of x-coordinates of houses at y
    by_y = {}
    # Group houses by x-coordinate for vertical moves
    # by_x[x] = sorted list of y-coordinates of houses at x
    by_x = {}
    
    # Also keep a set of visited houses to count distinct ones
    visited = set()
    
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
        
    # Current position
    cur_x = Sx
    cur_y = Sy
    
    count = 0
    
    for d, c in moves:
        prev_x = cur_x
        prev_y = cur_y
        
        if d == 'U':
            cur_y += c
        elif d == 'D':
            cur_y -= c
        elif d == 'L':
            cur_x -= c
        elif d == 'R':
            cur_x += c
            
        # Determine the segment
        if d == 'U' or d == 'D':
            # Vertical move: x is constant, y changes
            x_const = cur_x
            y1 = min(prev_y, cur_y)
            y2 = max(prev_y, cur_y)
            
            # Check if there are any houses at this x
            if x_const in by_x:
                y_list = by_x[x_const]
                # Find indices of houses with y in [y1, y2]
                left_idx = bisect_left(y_list, y1)
                right_idx = bisect_right(y_list, y2)
                
                # Iterate through the candidates
                # We need to check each house in this range
                # To avoid O(N) per query in worst case, we rely on the fact that
                # we only count each house once. But we still iterate over visited houses.
                # This is the best we can do with stdlib.
                for i in range(left_idx, right_idx):
                    y_h = y_list[i]
                    # The house is at (x_const, y_h)
                    if (x_const, y_h) not in visited:
                        visited.add((x_const, y_h))
                        count += 1
                        
        else:
            # Horizontal move: y is constant, x changes
            y_const = cur_y
            x1 = min(prev_x, cur_x)
            x2 = max(prev_x, cur_x)
            
            # Check if there are any houses at this y
            if y_const in by_y:
                x_list = by_y[y_const]
                # Find indices of houses with x in [x1, x2]
                left_idx = bisect_left(x_list, x1)
                right_idx = bisect_right(x_list, x2)
                
                for i in range(left_idx, right_idx):
                    x_h = x_list[i]
                    # The house is at (x_h, y_const)
                    if (x_h, y_const) not in visited:
                        visited.add((x_h, y_const))
                        count += 1
                        
    print(f"{cur_x} {cur_y} {count}")

if __name__ == '__main__':
    solve()