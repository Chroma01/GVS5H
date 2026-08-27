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

    # Build lookup structures
    # houses_by_y: y -> set of x coordinates
    houses_by_y = {}
    # houses_by_x: x -> set of y coordinates
    houses_by_x = {}
    
    for x, y in houses:
        if y not in houses_by_y:
            houses_by_y[y] = set()
        houses_by_y[y].add(x)
        
        if x not in houses_by_x:
            houses_by_x[x] = set()
        houses_by_x[x].add(y)
        
    visited_houses = set()
    count = 0
    
    # Current position
    cur_x = Sx
    cur_y = Sy
    
    for d, c in moves:
        if d == 'U':
            # Move up: y increases
            new_y = cur_y + c
            # Vertical segment at x = cur_x, from cur_y to new_y
            x_const = cur_x
            y1 = min(cur_y, new_y)
            y2 = max(cur_y, new_y)
            
            if x_const in houses_by_x:
                # We need to find houses with x = x_const and y in [y1, y2]
                # We iterate over a copy or handle removal carefully
                # Since we want to remove visited houses, we can iterate and remove
                ys_to_remove = []
                for y_h in houses_by_x[x_const]:
                    if y1 <= y_h <= y2:
                        if (x_const, y_h) not in visited_houses:
                            visited_houses.add((x_const, y_h))
                            count += 1
                            ys_to_remove.append(y_h)
                            # Also remove from houses_by_y
                            if y_h in houses_by_y:
                                houses_by_y[y_h].discard(x_const)
                                if not houses_by_y[y_h]:
                                    del houses_by_y[y_h]
                for y_h in ys_to_remove:
                    houses_by_x[x_const].discard(y_h)
                    if not houses_by_x[x_const]:
                        del houses_by_x[x_const]
            
            cur_y = new_y
            
        elif d == 'D':
            # Move down: y decreases
            new_y = cur_y - c
            # Vertical segment at x = cur_x, from new_y to cur_y
            x_const = cur_x
            y1 = min(cur_y, new_y)
            y2 = max(cur_y, new_y)
            
            if x_const in houses_by_x:
                ys_to_remove = []
                for y_h in houses_by_x[x_const]:
                    if y1 <= y_h <= y2:
                        if (x_const, y_h) not in visited_houses:
                            visited_houses.add((x_const, y_h))
                            count += 1
                            ys_to_remove.append(y_h)
                            if y_h in houses_by_y:
                                houses_by_y[y_h].discard(x_const)
                                if not houses_by_y[y_h]:
                                    del houses_by_y[y_h]
                for y_h in ys_to_remove:
                    houses_by_x[x_const].discard(y_h)
                    if not houses_by_x[x_const]:
                        del houses_by_x[x_const]
            
            cur_y = new_y
            
        elif d == 'L':
            # Move left: x decreases
            new_x = cur_x - c
            # Horizontal segment at y = cur_y, from new_x to cur_x
            y_const = cur_y
            x1 = min(cur_x, new_x)
            x2 = max(cur_x, new_x)
            
            if y_const in houses_by_y:
                xs_to_remove = []
                for x_h in houses_by_y[y_const]:
                    if x1 <= x_h <= x2:
                        if (x_h, y_const) not in visited_houses:
                            visited_houses.add((x_h, y_const))
                            count += 1
                            xs_to_remove.append(x_h)
                            if x_h in houses_by_x:
                                houses_by_x[x_h].discard(y_const)
                                if not houses_by_x[x_h]:
                                    del houses_by_x[x_h]
                for x_h in xs_to_remove:
                    houses_by_y[y_const].discard(x_h)
                    if not houses_by_y[y_const]:
                        del houses_by_y[y_const]
            
            cur_x = new_x
            
        elif d == 'R':
            # Move right: x increases
            new_x = cur_x + c
            # Horizontal segment at y = cur_y, from cur_x to new_x
            y_const = cur_y
            x1 = min(cur_x, new_x)
            x2 = max(cur_x, new_x)
            
            if y_const in houses_by_y:
                xs_to_remove = []
                for x_h in houses_by_y[y_const]:
                    if x1 <= x_h <= x2:
                        if (x_h, y_const) not in visited_houses:
                            visited_houses.add((x_h, y_const))
                            count += 1
                            xs_to_remove.append(x_h)
                            if x_h in houses_by_x:
                                houses_by_x[x_h].discard(y_const)
                                if not houses_by_x[x_h]:
                                    del houses_by_x[x_h]
                for x_h in xs_to_remove:
                    houses_by_y[y_const].discard(x_h)
                    if not houses_by_y[y_const]:
                        del houses_by_y[y_const]
            
            cur_x = new_x

    print(f"{cur_x} {cur_y} {count}")

if __name__ == '__main__':
    solve()