import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))
    
    # Group houses by y for horizontal moves, by x for vertical moves
    # by_y[y] = list of (x, index)
    # by_x[x] = list of (y, index)
    by_y = {}
    by_x = {}
    
    for idx in range(N):
        x = int(next(it))
        y = int(next(it))
        if y not in by_y:
            by_y[y] = []
        by_y[y].append((x, idx))
        if x not in by_x:
            by_x[x] = []
        by_x[x].append((y, idx))
    
    # Sort and split into separate arrays for bisect
    # For each y: sorted x list, and parallel index list
    y_to_xs = {}  # y -> sorted list of x
    y_to_idxs = {} # y -> list of house indices aligned with xs
    for y, lst in by_y.items():
        lst.sort()
        xs = [item[0] for item in lst]
        idxs = [item[1] for item in lst]
        y_to_xs[y] = xs
        y_to_idxs[y] = idxs
    
    x_to_ys = {}
    x_to_idxs = {}
    for x, lst in by_x.items():
        lst.sort()
        ys = [item[0] for item in lst]
        idxs = [item[1] for item in lst]
        x_to_ys[x] = ys
        x_to_idxs[x] = idxs
    
    visited = [False] * N
    count = 0
    
    cur_x, cur_y = Sx, Sy
    
    for _ in range(M):
        D = next(it).decode()
        C = int(next(it))
        
        if D == 'L':
            new_x = cur_x - C
            # Horizontal move along y = cur_y
            if cur_y in y_to_xs:
                xs = y_to_xs[cur_y]
                idxs = y_to_idxs[cur_y]
                lo = min(cur_x, new_x)
                hi = max(cur_x, new_x)
                left = bisect.bisect_left(xs, lo)
                right = bisect.bisect_right(xs, hi)
                for i in range(left, right):
                    hidx = idxs[i]
                    if not visited[hidx]:
                        visited[hidx] = True
                        count += 1
            cur_x = new_x
        elif D == 'R':
            new_x = cur_x + C
            if cur_y in y_to_xs:
                xs = y_to_xs[cur_y]
                idxs = y_to_idxs[cur_y]
                lo = min(cur_x, new_x)
                hi = max(cur_x, new_x)
                left = bisect.bisect_left(xs, lo)
                right = bisect.bisect_right(xs, hi)
                for i in range(left, right):
                    hidx = idxs[i]
                    if not visited[hidx]:
                        visited[hidx] = True
                        count += 1
            cur_x = new_x
        elif D == 'D':
            new_y = cur_y - C
            if cur_x in x_to_ys:
                ys = x_to_ys[cur_x]
                idxs = x_to_idxs[cur_x]
                lo = min(cur_y, new_y)
                hi = max(cur_y, new_y)
                left = bisect.bisect_left(ys, lo)
                right = bisect.bisect_right(ys, hi)
                for i in range(left, right):
                    hidx = idxs[i]
                    if not visited[hidx]:
                        visited[hidx] = True
                        count += 1
            cur_y = new_y
        elif D == 'U':
            new_y = cur_y + C
            if cur_x in x_to_ys:
                ys = x_to_ys[cur_x]
                idxs = x_to_idxs[cur_x]
                lo = min(cur_y, new_y)
                hi = max(cur_y, new_y)
                left = bisect.bisect_left(ys, lo)
                right = bisect.bisect_right(ys, hi)
                for i in range(left, right):
                    hidx = idxs[i]
                    if not visited[hidx]:
                        visited[hidx] = True
                        count += 1
            cur_y = new_y
    
    print(cur_x, cur_y, count)

if __name__ == "__main__":
    solve()