import sys
from bisect import bisect_left, bisect_right

def process(segs, houses, flags, other_flags):
    count = 0
    both = 0
    i = 0
    m = len(segs)
    n = len(houses)
    bl = bisect_left
    br = bisect_right
    while i < m:
        fixed = segs[i][0]
        cur_l = segs[i][1]
        cur_r = segs[i][2]
        i += 1
        while i < m and segs[i][0] == fixed:
            l = segs[i][1]
            r = segs[i][2]
            if l <= cur_r + 1:
                if r > cur_r:
                    cur_r = r
            else:
                lo = bl(houses, (fixed, cur_l, -1))
                hi = br(houses, (fixed, cur_r, n))
                for j in range(lo, hi):
                    idx = houses[j][2]
                    if not flags[idx]:
                        flags[idx] = 1
                        count += 1
                        if other_flags is not None and other_flags[idx]:
                            both += 1
                cur_l = l
                cur_r = r
            i += 1
        lo = bl(houses, (fixed, cur_l, -1))
        hi = br(houses, (fixed, cur_r, n))
        for j in range(lo, hi):
            idx = houses[j][2]
            if not flags[idx]:
                flags[idx] = 1
                count += 1
                if other_flags is not None and other_flags[idx]:
                    both += 1
    return count, both

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    x = int(next(it))
    y = int(next(it))

    houses_y = []
    houses_x = []
    for idx in range(N):
        hx = int(next(it))
        hy = int(next(it))
        houses_y.append((hy, hx, idx))
        houses_x.append((hx, hy, idx))

    horiz = []
    vert = []
    for _ in range(M):
        d = next(it)
        c = int(next(it))
        if d == b'U':
            ny = y + c
            vert.append((x, y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            vert.append((x, ny, y))
            y = ny
        elif d == b'L':
            nx = x - c
            horiz.append((y, nx, x))
            x = nx
        else:  # R
            nx = x + c
            horiz.append((y, x, nx))
            x = nx

    del data, it

    h_flags = bytearray(N)
    v_flags = bytearray(N)

    h_count = 0
    if horiz:
        houses_y.sort()
        horiz.sort()
        h_count, _ = process(horiz, houses_y, h_flags, None)
    del horiz, houses_y

    v_count = 0
    both = 0
    if vert:
        houses_x.sort()
        vert.sort()
        v_count, both = process(vert, houses_x, v_flags, h_flags)
    del vert, houses_x

    ans = h_count + v_count - both
    sys.stdout.write(f"{x} {y} {ans}\n")

if __name__ == "__main__":
    main()