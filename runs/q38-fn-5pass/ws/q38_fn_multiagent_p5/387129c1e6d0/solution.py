import sys
from bisect import bisect_right
from collections import defaultdict


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    N = int(data[idx])
    idx += 1
    M = int(data[idx])
    idx += 1
    x = int(data[idx])
    idx += 1
    y = int(data[idx])
    idx += 1

    houses = []
    for _ in range(N):
        hx = int(data[idx])
        hy = int(data[idx + 1])
        idx += 2
        houses.append((hx, hy))

    horiz = defaultdict(list)  # y -> list of (x_left, x_right)
    vert = defaultdict(list)   # x -> list of (y_low, y_high)

    for _ in range(M):
        direction = data[idx]
        c = int(data[idx + 1])
        idx += 2

        if direction == b'U':
            ny = y + c
            vert[x].append((y, ny))
            y = ny
        elif direction == b'D':
            ny = y - c
            vert[x].append((ny, y))
            y = ny
        elif direction == b'R':
            nx = x + c
            horiz[y].append((x, nx))
            x = nx
        else:  # b'L'
            nx = x - c
            horiz[y].append((nx, x))
            x = nx

    del data

    def merge(d):
        for key, lst in d.items():
            if not lst:
                continue
            if len(lst) == 1:
                l, r = lst[0]
                d[key] = ([l], [r])
                continue

            lst.sort()
            starts = []
            ends = []

            it = iter(lst)
            cl, cr = next(it)

            for l, r in it:
                # All house coordinates are integers, so intervals with
                # l == cr + 1 have no integer point in the gap.
                if l <= cr + 1:
                    if r > cr:
                        cr = r
                else:
                    starts.append(cl)
                    ends.append(cr)
                    cl, cr = l, r

            starts.append(cl)
            ends.append(cr)
            d[key] = (starts, ends)

    merge(horiz)
    merge(vert)

    ans = 0
    hget = horiz.get
    vget = vert.get
    br = bisect_right

    for hx, hy in houses:
        # Check horizontal coverage first. If covered, do not check vertical,
        # so houses at intersections are counted once.
        se = hget(hy)
        if se is not None:
            starts, ends = se
            i = br(starts, hx) - 1
            if i >= 0 and ends[i] >= hx:
                ans += 1
                continue

        se = vget(hx)
        if se is not None:
            starts, ends = se
            i = br(starts, hy) - 1
            if i >= 0 and ends[i] >= hy:
                ans += 1

    print(x, y, ans)


if __name__ == "__main__":
    solve()