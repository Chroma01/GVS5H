import sys
import bisect

def main():
    input = sys.stdin.readline
    N, M, Sx, Sy = map(int, input().split())
    
    # Read houses
    houses = []
    for _ in range(N):
        x, y = map(int, input().split())
        houses.append((x, y))
    
    # Build maps: y -> sorted list of x; x -> sorted list of y
    y_to_xs = {}
    x_to_ys = {}
    for x, y in houses:
        y_to_xs.setdefault(y, []).append(x)
        x_to_ys.setdefault(x, []).append(y)
    
    # Sort lists
    for y in y_to_xs:
        y_to_xs[y].sort()
    for x in x_to_ys:
        x_to_ys[x].sort()
    
    # Read moves
    moves = []
    for _ in range(M):
        d, c = input().split()
        c = int(c)
        moves.append((d, c))
    
    cur_x, cur_y = Sx, Sy
    visited = set()
    count = 0
    
    for d, c in moves:
        if d == 'U':
            # vertical move, x constant
            x = cur_x
            y_low = cur_y
            y_high = cur_y + c
            # ensure y_low <= y_high
            if y_low > y_high:
                y_low, y_high = y_high, y_low
            # look up houses with this x
            if x in x_to_ys:
                ys = x_to_ys[x]
                # find first y >= y_low
                lo = bisect.bisect_left(ys, y_low)
                hi = bisect.bisect_right(ys, y_high)
                for i in range(lo, hi):
                    y = ys[i]
                    if (x, y) not in visited:
                        visited.add((x, y))
                        count += 1
            cur_y += c
        elif d == 'D':
            # vertical move down
            x = cur_x
            y_low = cur_y - c
            y_high = cur_y
            if y_low > y_high:
                y_low, y_high = y_high, y_low
            if x in x_to_ys:
                ys = x_to_ys[x]
                lo = bisect.bisect_left(ys, y_low)
                hi = bisect.bisect_right(ys, y_high)
                for i in range(lo, hi):
                    y = ys[i]
                    if (x, y) not in visited:
                        visited.add((x, y))
                        count += 1
            cur_y -= c
        elif d == 'L':
            # horizontal move left
            y = cur_y
            x_low = cur_x - c
            x_high = cur_x
            if x_low > x_high:
                x_low, x_high = x_high, x_low
            if y in y_to_xs:
                xs = y_to_xs[y]
                lo = bisect.bisect_left(xs, x_low)
                hi = bisect.bisect_right(xs, x_high)
                for i in range(lo, hi):
                    x = xs[i]
                    if (x, y) not in visited:
                        visited.add((x, y))
                        count += 1
            cur_x -= c
        elif d == 'R':
            # horizontal move right
            y = cur_y
            x_low = cur_x
            x_high = cur_x + c
            if x_low > x_high:
                x_low, x_high = x_high, x_low
            if y in y_to_xs:
                xs = y_to_xs[y]
                lo = bisect.bisect_left(xs, x_low)
                hi = bisect.bisect_right(xs, x_high)
                for i in range(lo, hi):
                    x = xs[i]
                    if (x, y) not in visited:
                        visited.add((x, y))
                        count += 1
            cur_x += c
    
    print(cur_x, cur_y, count)

if __name__ == "__main__":
    main()