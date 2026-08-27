import sys
from bisect import bisect_left, bisect_right

def solve():
    # Fast I/O
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

    # Organize houses by Y coordinate for horizontal moves
    # houses_by_y[y] = sorted list of x coordinates
    houses_by_y = {}
    for x, y in houses:
        if y not in houses_by_y:
            houses_by_y[y] = []
        houses_by_y[y].append(x)
    
    for y in houses_by_y:
        houses_by_y[y].sort()
        
    # Organize houses by X coordinate for vertical moves
    # houses_by_x[x] = sorted list of y coordinates
    houses_by_x = {}
    for x, y in houses:
        if x not in houses_by_x:
            houses_by_x[x] = []
        houses_by_x[x].append(y)
        
    for x in houses_by_x:
        houses_by_x[x].sort()
        
    # Set to store visited houses as tuples (x, y)
    visited_houses = set()
    
    cx, cy = S_x, S_y
    
    for d, c in moves:
        if d == 'U':
            ny = cy + c
            nx = cx
            # Vertical move: check houses on line x = cx between cy and ny
            if cx in houses_by_x:
                ys = houses_by_x[cx]
                low = min(cy, ny)
                high = max(cy, ny)
                
                # Find indices in sorted list
                idx_start = bisect_left(ys, low)
                idx_end = bisect_right(ys, high)
                
                for i in range(idx_start, idx_end):
                    visited_houses.add((cx, ys[i]))
                    
        elif d == 'D':
            ny = cy - c
            nx = cx
            # Vertical move: check houses on line x = cx between cy and ny
            if cx in houses_by_x:
                ys = houses_by_x[cx]
                low = min(cy, ny)
                high = max(cy, ny)
                
                idx_start = bisect_left(ys, low)
                idx_end = bisect_right(ys, high)
                
                for i in range(idx_start, idx_end):
                    visited_houses.add((cx, ys[i]))
                    
        elif d == 'L':
            nx = cx - c
            ny = cy
            # Horizontal move: check houses on line y = cy between cx and nx
            if cy in houses_by_y:
                xs = houses_by_y[cy]
                low = min(cx, nx)
                high = max(cx, nx)
                
                idx_start = bisect_left(xs, low)
                idx_end = bisect_right(xs, high)
                
                for i in range(idx_start, idx_end):
                    visited_houses.add((xs[i], cy))
                    
        elif d == 'R':
            nx = cx + c
            ny = cy
            # Horizontal move: check houses on line y = cy between cx and nx
            if cy in houses_by_y:
                xs = houses_by_y[cy]
                low = min(cx, nx)
                high = max(cx, nx)
                
                idx_start = bisect_left(xs, low)
                idx_end = bisect_right(xs, high)
                
                for i in range(idx_start, idx_end):
                    visited_houses.add((xs[i], cy))
                    
        cx, cy = nx, ny
        
    print(f"{cx} {cy} {len(visited_houses)}")

if __name__ == '__main__':
    solve()