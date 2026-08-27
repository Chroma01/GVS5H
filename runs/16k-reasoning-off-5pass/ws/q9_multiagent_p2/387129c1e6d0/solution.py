import sys
from bisect import bisect_left, bisect_right

# Increase recursion depth just in case, though iterative DSU is preferred
sys.setrecursionlimit(300000)

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
            houses.append((int(next(iterator)), int(next(iterator))))
            
        moves = []
        for _ in range(M):
            d = next(iterator)
            c = int(next(iterator))
            moves.append((d, c))
    except StopIteration:
        return

    # Group houses by X and Y
    # houses_by_x[x] -> list of y coordinates (sorted)
    # houses_by_y[y] -> list of x coordinates (sorted)
    houses_by_x = {}
    houses_by_y = {}
    
    for x, y in houses:
        if x not in houses_by_x:
            houses_by_x[x] = []
        houses_by_x[x].append(y)
        
        if y not in houses_by_y:
            houses_by_y[y] = []
        houses_by_y[y].append(x)
        
    # Sort the lists
    for x in houses_by_x:
        houses_by_x[x].sort()
    for y in houses_by_y:
        houses_by_y[y].sort()
        
    # DSU structures
    # dsu_x[x] stores the parent array for the vertical line at x
    # dsu_y[y] stores the parent array for the horizontal line at y
    dsu_x = {}
    dsu_y = {}
    
    # Helper to initialize DSU for a line
    def init_dsu(coord_list):
        size = len(coord_list)
        # parent[i] = i initially. 
        # We add a sentinel at the end (size) pointing to itself.
        # If find returns size, it means no more houses in this line.
        return list(range(size + 1))

    # Iterative find with path compression
    def find(parent, i):
        path = []
        root = i
        while parent[root] != root:
            path.append(root)
            root = parent[root]
        for node in path:
            parent[node] = root
        return root

    # Union i and j. We want to point i to j (conceptually skipping i).
    # Since we process in order, we usually union i with i+1.
    def union(parent, i, j):
        root_i = find(parent, i)
        root_j = find(parent, j)
        if root_i != root_j:
            parent[root_i] = root_j

    # Global visited set
    visited = set()
    count = 0
    
    curr_x, curr_y = S_x, S_y
    
    # Process moves
    for d, c in moves:
        if d == 'U':
            # Move Up: (curr_x, curr_y) -> (curr_x, curr_y + c)
            if curr_x not in houses_by_x:
                curr_y += c
                continue
                
            y_list = houses_by_x[curr_x]
            start_y = min(curr_y, curr_y + c)
            end_y = max(curr_y, curr_y + c)
            
            l = bisect_left(y_list, start_y)
            r = bisect_right(y_list, end_y) - 1
            
            if l > r:
                curr_y += c
                continue
                
            if curr_x not in dsu_x:
                dsu_x[curr_x] = init_dsu(y_list)
            
            parent = dsu_x[curr_x]
            
            idx = find(parent, l)
            while idx <= r:
                y_val = y_list[idx]
                visited.add((curr_x, y_val))
                count += 1
                union(parent, idx, idx + 1)
                idx = find(parent, idx)
                
            curr_y += c
            
        elif d == 'D':
            # Move Down: (curr_x, curr_y) -> (curr_x, curr_y - c)
            if curr_x not in houses_by_x:
                curr_y -= c
                continue
                
            y_list = houses_by_x[curr_x]
            start_y = min(curr_y, curr_y - c)
            end_y = max(curr_y, curr_y - c)
            
            l = bisect_left(y_list, start_y)
            r = bisect_right(y_list, end_y) - 1
            
            if l > r:
                curr_y -= c
                continue
                
            if curr_x not in dsu_x:
                dsu_x[curr_x] = init_dsu(y_list)
                
            parent = dsu_x[curr_x]
            
            idx = find(parent, l)
            while idx <= r:
                y_val = y_list[idx]
                visited.add((curr_x, y_val))
                count += 1
                union(parent, idx, idx + 1)
                idx = find(parent, idx)
                
            curr_y -= c
            
        elif d == 'L':
            # Move Left: (curr_x, curr_y) -> (curr_x - c, curr_y)
            if curr_y not in houses_by_y:
                curr_x -= c
                continue
                
            x_list = houses_by_y[curr_y]
            start_x = min(curr_x, curr_x - c)
            end_x = max(curr_x, curr_x - c)
            
            l = bisect_left(x_list, start_x)
            r = bisect_right(x_list, end_x) - 1
            
            if l > r:
                curr_x -= c
                continue
                
            if curr_y not in dsu_y:
                dsu_y[curr_y] = init_dsu(x_list)
                
            parent = dsu_y[curr_y]
            
            idx = find(parent, l)
            while idx <= r:
                x_val = x_list[idx]
                visited.add((x_val, curr_y))
                count += 1
                union(parent, idx, idx + 1)
                idx = find(parent, idx)
                
            curr_x -= c
            
        elif d == 'R':
            # Move Right: (curr_x, curr_y) -> (curr_x + c, curr_y)
            if curr_y not in houses_by_y:
                curr_x += c
                continue
                
            x_list = houses_by_y[curr_y]
            start_x = min(curr_x, curr_x + c)
            end_x = max(curr_x, curr_x + c)
            
            l = bisect_left(x_list, start_x)
            r = bisect_right(x_list, end_x) - 1
            
            if l > r:
                curr_x += c
                continue
                
            if curr_y not in dsu_y:
                dsu_y[curr_y] = init_dsu(x_list)
                
            parent = dsu_y[curr_y]
            
            idx = find(parent, l)
            while idx <= r:
                x_val = x_list[idx]
                visited.add((x_val, curr_y))
                count += 1
                union(parent, idx, idx + 1)
                idx = find(parent, idx)
                
            curr_x += c

    print(f"{curr_x} {curr_y} {count}")

if __name__ == '__main__':
    solve()