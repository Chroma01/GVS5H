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

    # Preprocess houses into dictionaries for efficient range queries
    # houses_by_y: maps Y -> sorted list of Xs
    # houses_by_x: maps X -> sorted list of Ys
    houses_by_y = {}
    houses_by_x = {}
    
    for x, y in houses:
        if y not in houses_by_y:
            houses_by_y[y] = []
        if x not in houses_by_x:
            houses_by_x[x] = []
        houses_by_y[y].append(x)
        houses_by_x[x].append(y)
    
    # Sort the coordinate lists to enable binary search
    for y in houses_by_y:
        houses_by_y[y].sort()
    for x in houses_by_x:
        houses_by_x[x].sort()
    
    # Set to track distinct houses visited
    visited_houses = set()
    
    # Current position
    curr_x, curr_y = S_x, S_y
    
    # Process each move
    for d, c in moves:
        if d == 'U':
            new_y = curr_y + c
            # Vertical segment: x = curr_x, y in [min, max]
            if curr_x in houses_by_x:
                ys = houses_by_x[curr_x]
                low = min(curr_y, new_y)
                high = max(curr_y, new_y)
                idx_start = bisect_left(ys, low)
                idx_end = bisect_right(ys, high)
                for i in range(idx_start, idx_end):
                    visited_houses.add((curr_x, ys[i]))
            curr_y = new_y
            
        elif d == 'D':
            new_y = curr_y - c
            # Vertical segment: x = curr_x, y in [min, max]
            if curr_x in houses_by_x:
                ys = houses_by_x[curr_x]
                low = min(curr_y, new_y)
                high = max(curr_y, new_y)
                idx_start = bisect_left(ys, low)
                idx_end = bisect_right(ys, high)
                for i in range(idx_start, idx_end):
                    visited_houses.add((curr_x, ys[i]))
            curr_y = new_y
            
        elif d == 'L':
            new_x = curr_x - c
            # Horizontal segment: y = curr_y, x in [min, max]
            if curr_y in houses_by_y:
                xs = houses_by_y[curr_y]
                low = min(curr_x, new_x)
                high = max(curr_x, new_x)
                idx_start = bisect_left(xs, low)
                idx_end = bisect_right(xs, high)
                for i in range(idx_start, idx_end):
                    visited_houses.add((xs[i], curr_y))
            curr_x = new_x
            
        elif d == 'R':
            new_x = curr_x + c
            # Horizontal segment: y = curr_y, x in [min, max]
            if curr_y in houses_by_y:
                xs = houses_by_y[curr_y]
                low = min(curr_x, new_x)
                high = max(curr_x, new_x)
                idx_start = bisect_left(xs, low)
                idx_end = bisect_right(xs, high)
                for i in range(idx_start, idx_end):
                    visited_houses.add((xs[i], curr_y))
            curr_x = new_x

    print(f"{curr_x} {curr_y} {len(visited_houses)}")

if __name__ == '__main__':
    solve()