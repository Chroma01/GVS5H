import sys
from bisect import bisect_left, bisect_right

# Increase recursion depth just in case, though iterative find is used
sys.setrecursionlimit(300005)

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

    # Organize houses by x and y coordinates
    # houses_by_x[x] -> sorted list of y coordinates
    # houses_by_y[y] -> sorted list of x coordinates
    houses_by_x = {}
    houses_by_y = {}
    
    for x, y in houses:
        if x not in houses_by_x:
            houses_by_x[x] = []
        if y not in houses_by_y:
            houses_by_y[y] = []
        houses_by_x[x].append(y)
        houses_by_y[y].append(x)
        
    # Sort the lists for binary search
    for x in houses_by_x:
        houses_by_x[x].sort()
    for y in houses_by_y:
        houses_by_y[y].sort()
        
    # DSU structures to track visited houses
    # For each x, we maintain a DSU on the indices of houses_by_x[x]
    # For each y, we maintain a DSU on the indices of houses_by_y[y]
    # parent_x[x][i] stores the next unvisited index in houses_by_x[x] starting from i
    # parent_y[y][i] stores the next unvisited index in houses_by_y[y] starting from i
    
    # We use a dictionary mapping coordinate -> list of parents
    # To save space and time, we only create lists when needed
    parent_x = {}
    parent_y = {}
    
    def get_parent_x(x):
        if x not in parent_x:
            parent_x[x] = []
        return parent_x[x]
        
    def get_parent_y(y):
        if y not in parent_y:
            parent_y[y] = []
        return parent_y[y]

    # Iterative find with path compression to avoid recursion depth issues
    def find(parent, i):
        path = []
        root = i
        while parent[root] != root:
            path.append(root)
            root = parent[root]
        for node in path:
            parent[node] = root
        return root

    def union(parent, i):
        # Union i with i+1. We want find(i) to point to the next available.
        # If i is the last element, it points to itself (or we handle bounds check externally)
        # Standard DSU union: root of i becomes root of i+1
        # But here we specifically want to skip i.
        # So we set parent[i] = find(parent, i+1)
        root_i = find(parent, i)
        root_next = find(parent, i + 1)
        if root_i != root_next:
            parent[root_i] = root_next
        return root_next

    current_x, current_y = S_x, S_y
    visited_count = 0
    
    # Process moves
    for d, c in moves:
        if d == 'U':
            # Move from (current_x, current_y) to (current_x, current_y + c)
            # Vertical line at x = current_x
            y_start, y_end = current_y, current_y + c
            x_coord = current_x
            
            # Find range of houses on this vertical line
            if x_coord in houses_by_x:
                ys = houses_by_x[x_coord]
                # Find indices in ys that are within [min(y_start, y_end), max(y_start, y_end)]
                low_idx = bisect_left(ys, min(y_start, y_end))
                high_idx = bisect_right(ys, max(y_start, y_end)) - 1
                
                # If there are houses in this range
                if low_idx <= high_idx:
                    # Get the parent list for this x
                    p = get_parent_x(x_coord)
                    # Ensure the list is long enough (lazy initialization)
                    while len(p) <= high_idx + 1:
                        p.append(len(p)) # Initialize with self
                    
                    # Iterate and count unvisited houses
                    idx = low_idx
                    while idx <= high_idx:
                        idx = find(p, idx)
                        if idx > high_idx:
                            break
                        # House at ys[idx] is visited
                        visited_count += 1
                        # Mark as visited by unioning with next
                        union(p, idx)
                        
        elif d == 'D':
            # Move from (current_x, current_y) to (current_x, current_y - c)
            y_start, y_end = current_y, current_y - c
            x_coord = current_x
            
            if x_coord in houses_by_x:
                ys = houses_by_x[x_coord]
                low_idx = bisect_left(ys, min(y_start, y_end))
                high_idx = bisect_right(ys, max(y_start, y_end)) - 1
                
                if low_idx <= high_idx:
                    p = get_parent_x(x_coord)
                    while len(p) <= high_idx + 1:
                        p.append(len(p))
                        
                    idx = low_idx
                    while idx <= high_idx:
                        idx = find(p, idx)
                        if idx > high_idx:
                            break
                        visited_count += 1
                        union(p, idx)
                        
        elif d == 'L':
            # Move from (current_x, current_y) to (current_x - c, current_y)
            # Horizontal line at y = current_y
            x_start, x_end = current_x, current_x - c
            y_coord = current_y
            
            if y_coord in houses_by_y:
                xs = houses_by_y[y_coord]
                low_idx = bisect_left(xs, min(x_start, x_end))
                high_idx = bisect_right(xs, max(x_start, x_end)) - 1
                
                if low_idx <= high_idx:
                    p = get_parent_y(y_coord)
                    while len(p) <= high_idx + 1:
                        p.append(len(p))
                        
                    idx = low_idx
                    while idx <= high_idx:
                        idx = find(p, idx)
                        if idx > high_idx:
                            break
                        visited_count += 1
                        union(p, idx)
                        
        elif d == 'R':
            # Move from (current_x, current_y) to (current_x + c, current_y)
            x_start, x_end = current_x, current_x + c
            y_coord = current_y
            
            if y_coord in houses_by_y:
                xs = houses_by_y[y_coord]
                low_idx = bisect_left(xs, min(x_start, x_end))
                high_idx = bisect_right(xs, max(x_start, x_end)) - 1
                
                if low_idx <= high_idx:
                    p = get_parent_y(y_coord)
                    while len(p) <= high_idx + 1:
                        p.append(len(p))
                        
                    idx = low_idx
                    while idx <= high_idx:
                        idx = find(p, idx)
                        if idx > high_idx:
                            break
                        visited_count += 1
                        union(p, idx)
                        
        # Update current position
        if d == 'U':
            current_y += c
        elif d == 'D':
            current_y -= c
        elif d == 'L':
            current_x -= c
        elif d == 'R':
            current_x += c
            
    print(f"{current_x} {current_y} {visited_count}")

if __name__ == '__main__':
    solve()