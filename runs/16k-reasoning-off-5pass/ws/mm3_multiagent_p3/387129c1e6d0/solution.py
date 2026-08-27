import sys
import bisect
from collections import defaultdict

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))
    
    xs = [0] * N
    ys = [0] * N
    dict_x = defaultdict(list)  # key: x, value: list of (y, house_id) sorted by y
    dict_y = defaultdict(list)  # key: y, value: list of (x, house_id) sorted by x
    
    for i in range(N):
        x = int(next(it))
        y = int(next(it))
        xs[i] = x
        ys[i] = y
        dict_x[x].append((y, i))
        dict_y[y].append((x, i))
    
    # Sort each bucket for binary search
    for lst in dict_x.values():
        lst.sort()
    for lst in dict_y.values():
        lst.sort()
    
    x, y = Sx, Sy
    count = 0
    INF_ID = N  # sentinel larger than any house id
    
    for _ in range(M):
        D = next(it).decode()
        C = int(next(it))
        old_x, old_y = x, y
        
        # Update position
        if D == 'L':
            x -= C
        elif D == 'R':
            x += C
        elif D == 'U':
            y += C
        elif D == 'D':
            y -= C
        
        # Process houses on this move
        if D == 'L' or D == 'R':
            # Horizontal move: bucket is dict_y[y]
            bucket = dict_y.get(y)
            if bucket:
                lo = min(old_x, x)
                hi = max(old_x, x)
                l = bisect.bisect_left(bucket, (lo, -1))
                r = bisect.bisect_right(bucket, (hi, INF_ID))
                if l < r:
                    # Extract the slice to process
                    houses = bucket[l:r]
                    for coord, hid in houses:
                        # coord is x, hid is house id
                        count += 1
                        # Remove from the other bucket: dict_x[coord]
                        ob = dict_x[coord]
                        pos = bisect.bisect_left(ob, (y, hid))
                        # Should always be found
                        if pos < len(ob) and ob[pos] == (y, hid):
                            del ob[pos]
                        # else: inconsistency (should not happen)
                    del bucket[l:r]
        else:
            # Vertical move: bucket is dict_x[x]
            bucket = dict_x.get(x)
            if bucket:
                lo = min(old_y, y)
                hi = max(old_y, y)
                l = bisect.bisect_left(bucket, (lo, -1))
                r = bisect.bisect_right(bucket, (hi, INF_ID))
                if l < r:
                    houses = bucket[l:r]
                    for coord, hid in houses:
                        # coord is y, hid is house id
                        count += 1
                        # Remove from the other bucket: dict_y[coord]
                        ob = dict_y[coord]
                        pos = bisect.bisect_left(ob, (x, hid))
                        if pos < len(ob) and ob[pos] == (x, hid):
                            del ob[pos]
                    del bucket[l:r]
    
    print(x, y, count)

if __name__ == "__main__":
    solve()