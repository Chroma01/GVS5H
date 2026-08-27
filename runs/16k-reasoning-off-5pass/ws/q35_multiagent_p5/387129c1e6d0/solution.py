import sys
import bisect

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    M = int(next(iterator))
    Sx = int(next(iterator))
    Sy = int(next(iterator))
    
    houses = []
    for i in range(N):
        x = int(next(iterator))
        y = int(next(iterator))
        houses.append((x, y))
    
    moves = []
    for i in range(M):
        d = next(iterator)
        c = int(next(iterator))
        moves.append((d, c))
    
    # Group houses by y-coordinate and x-coordinate
    by_y = {}
    by_x = {}
    
    for (x, y) in houses:
        if y not in by_y:
            by_y[y] = []
        by_y[y].append(x)
        
        if x not in by_x:
            by_x[x] = []
        by_x[x].append(y)
    
    # Sort the lists
    for y in by_y:
        by_y[y].sort()
    for x in by_x:
        by_x[x].sort()
    
    # Create Fenwick trees for each line
    # fenw_by_y[y] is a list for the Fenwick tree for line y
    fenw_by_y = {}
    for y in by_y:
        n = len(by_y[y])
        fenw = [0] * (n + 1)
        fenw_by_y[y] = fenw
        
    fenw_by_x = {}
    for x in by_x:
        n = len(by_x[x])
        fenw = [0] * (n + 1)
        fenw_by_x[x] = fenw
    
    # Fenwick tree operations
    def fenw_update(fenw, i, delta):
        # i is 1-indexed
        n = len(fenw)
        while i < n:
            fenw[i] += delta
            i += i & (-i)
            
    def fenw_query(fenw, i):
        # i is 1-indexed, returns sum from 1 to i
        s = 0
        while i > 0:
            s += fenw[i]
            i -= i & (-i)
        return s
    
    visited_houses = set()
    count = 0
    
    cur_x, cur_y = Sx, Sy
    
    for (d, c) in moves:
        old_x, old_y = cur_x, cur_y
        if d == 'U':
            new_x, new_y = cur_x, cur_y + c
        elif d == 'D':
            new_x, new_y = cur_x, cur_y - c
        elif d == 'L':
            new_x, new_y = cur_x - c, cur_y
        elif d == 'R':
            new_x, new_y = cur_x + c, cur_y
        
        cur_x, cur_y = new_x, new_y
        
        if old_y == new_y:
            # Horizontal move
            y = old_y
            x1, x2 = old_x, new_x
            if x1 > x2:
                x1, x2 = x2, x1
            
            if y in by_y:
                xs = by_y[y]
                fenw = fenw_by_y[y]
                n = len(xs)
                
                # Find rank range [L, R] (0-indexed)
                L = bisect.bisect_left(xs, x1)
                R = bisect.bisect_right(xs, x2) - 1
                
                if L <= R:
                    while L <= R:
                        # Binary search for the first unvisited rank in [L, R]
                        low, high = L, R
                        ans = -1
                        while low <= high:
                            mid = (low + high) // 2
                            # Number of visited in [L, mid] (0-indexed)
                            # = fenw_query(mid+1) - fenw_query(L)
                            visited_count = fenw_query(fenw, mid+1) - fenw_query(fenw, L)
                            unvisited_count = (mid - L + 1) - visited_count
                            if unvisited_count > 0:
                                ans = mid
                                high = mid - 1
                            else:
                                low = mid + 1
                        
                        if ans == -1:
                            break
                            
                        # Mark ans as visited
                        fenw_update(fenw, ans+1, 1)
                        x = xs[ans]
                        house = (x, y)
                        if house not in visited_houses:
                            visited_houses.add(house)
                            count += 1
                        L = ans + 1
        else:
            # Vertical move
            x = old_x
            y1, y2 = old_y, new_y
            if y1 > y2:
                y1, y2 = y2, y1
                
            if x in by_x:
                ys = by_x[x]
                fenw = fenw_by_x[x]
                n = len(ys)
                
                # Find rank range [L, R] (0-indexed)
                L = bisect.bisect_left(ys, y1)
                R = bisect.bisect_right(ys, y2) - 1
                
                if L <= R:
                    while L <= R:
                        # Binary search for the first unvisited rank in [L, R]
                        low, high = L, R
                        ans = -1
                        while low <= high:
                            mid = (low + high) // 2
                            # Number of visited in [L, mid] (0-indexed)
                            visited_count = fenw_query(fenw, mid+1) - fenw_query(fenw, L)
                            unvisited_count = (mid - L + 1) - visited_count
                            if unvisited_count > 0:
                                ans = mid
                                high = mid - 1
                            else:
                                low = mid + 1
                        
                        if ans == -1:
                            break
                            
                        # Mark ans as visited
                        fenw_update(fenw, ans+1, 1)
                        y = ys[ans]
                        house = (x, y)
                        if house not in visited_houses:
                            visited_houses.add(house)
                            count += 1
                        L = ans + 1
    
    print(f"{cur_x} {cur_y} {count}")

if __name__ == '__main__':
    main()