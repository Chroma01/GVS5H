import sys
import bisect

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
        
        houses_by_y = {}
        houses_by_x = {}
        x_coords_by_y = {}
        y_coords_by_x = {}
        
        for i in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            
            if y not in houses_by_y:
                houses_by_y[y] = []
                x_coords_by_y[y] = []
            houses_by_y[y].append((x, i))
            x_coords_by_y[y].append(x)
            
            if x not in houses_by_x:
                houses_by_x[x] = []
                y_coords_by_x[x] = []
            houses_by_x[x].append((y, i))
            y_coords_by_x[x].append(y)
            
        for y in houses_by_y:
            houses_by_y[y].sort(key=lambda p: p[0])
            x_coords_by_y[y].sort()
            
        for x in houses_by_x:
            houses_by_x[x].sort(key=lambda p: p[0])
            y_coords_by_x[x].sort()
            
        moves = []
        for i in range(M):
            d = next(iterator)
            c = int(next(iterator))
            moves.append((d, c))
            
    except StopIteration:
        return

    dsu_y = {}
    dsu_x = {}
    
    for y, lst in houses_by_y.items():
        dsu_y[y] = list(range(len(lst) + 1))
        
    for x, lst in houses_by_x.items():
        dsu_x[x] = list(range(len(lst) + 1))
        
    def find_dsu(parent, i):
        root = i
        while parent[root] != root:
            root = parent[root]
        
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    visited = [False] * N
    visited_count = 0
    
    cx, cy = Sx, Sy
    
    for d, c in moves:
        if d == 'L':
            x_start = cx - c
            x_end = cx
            
            if cy in houses_by_y:
                lst = houses_by_y[cy]
                x_coords = x_coords_by_y[cy]
                dsu = dsu_y[cy]
                
                idx_start = bisect.bisect_left(x_coords, x_start)
                idx_end = bisect.bisect_right(x_coords, x_end)
                
                if idx_start < idx_end:
                    curr = find_dsu(dsu, idx_start)
                    while curr < idx_end:
                        h_id = lst[curr][1]
                        if not visited[h_id]:
                            visited[h_id] = True
                            visited_count += 1
                        
                        next_idx = find_dsu(dsu, curr + 1)
                        dsu[curr] = next_idx
                        curr = next_idx
            
            cx = x_start
            
        elif d == 'R':
            x_start = cx
            x_end = cx + c
            
            if cy in houses_by_y:
                lst = houses_by_y[cy]
                x_coords = x_coords_by_y[cy]
                dsu = dsu_y[cy]
                
                idx_start = bisect.bisect_left(x_coords, x_start)
                idx_end = bisect.bisect_right(x_coords, x_end)
                
                if idx_start < idx_end:
                    curr = find_dsu(dsu, idx_start)
                    while curr < idx_end:
                        h_id = lst[curr][1]
                        if not visited[h_id]:
                            visited[h_id] = True
                            visited_count += 1
                        
                        next_idx = find_dsu(dsu, curr + 1)
                        dsu[curr] = next_idx
                        curr = next_idx
            
            cx = x_end
            
        elif d == 'U':
            y_start = cy
            y_end = cy + c
            
            if cx in houses_by_x:
                lst = houses_by_x[cx]
                y_coords = y_coords_by_x[cx]
                dsu = dsu_x[cx]
                
                idx_start = bisect.bisect_left(y_coords, y_start)
                idx_end = bisect.bisect_right(y_coords, y_end)
                
                if idx_start < idx_end:
                    curr = find_dsu(dsu, idx_start)
                    while curr < idx_end:
                        h_id = lst[curr][1]
                        if not visited[h_id]:
                            visited[h_id] = True
                            visited_count += 1
                        
                        next_idx = find_dsu(dsu, curr + 1)
                        dsu[curr] = next_idx
                        curr = next_idx
            
            cy = y_end
            
        elif d == 'D':
            y_start = cy - c
            y_end = cy
            
            if cx in houses_by_x:
                lst = houses_by_x[cx]
                y_coords = y_coords_by_x[cx]
                dsu = dsu_x[cx]
                
                idx_start = bisect.bisect_left(y_coords, y_start)
                idx_end = bisect.bisect_right(y_coords, y_end)
                
                if idx_start < idx_end:
                    curr = find_dsu(dsu, idx_start)
                    while curr < idx_end:
                        h_id = lst[curr][1]
                        if not visited[h_id]:
                            visited[h_id] = True
                            visited_count += 1
                        
                        next_idx = find_dsu(dsu, curr + 1)
                        dsu[curr] = next_idx
                        curr = next_idx
            
            cy = y_start

    print(f"{cx} {cy} {visited_count}")

if __name__ == '__main__':
    solve()