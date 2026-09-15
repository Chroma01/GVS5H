import sys
from bisect import bisect_right


def merge_groups(groups):
    for key in groups:
        intervals = groups[key]

        if len(intervals) == 1:
            s, e = intervals[0]
            groups[key] = ((s,), (e,))
            continue

        intervals.sort()
        it = iter(intervals)
        cs, ce = next(it)

        starts = []
        ends = []

        for s, e in it:
            if s <= ce + 1:
                if e > ce:
                    ce = e
            else:
                starts.append(cs)
                ends.append(ce)
                cs, ce = s, e

        starts.append(cs)
        ends.append(ce)

        groups[key] = (tuple(starts), tuple(ends))


def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0

    N = int(data[idx])
    idx += 1
    M = int(data[idx])
    idx += 1
    x = int(data[idx])
    idx += 1
    y = int(data[idx])
    idx += 1

    houses = [None] * N
    for i in range(N):
        hx = int(data[idx])
        hy = int(data[idx + 1])
        idx += 2
        houses[i] = (hx, hy)

    horizontal = {}
    vertical = {}

    for _ in range(M):
        d = data[idx]
        c = int(data[idx + 1])
        idx += 2

        if d == b'U':
            ny = y + c
            interval = (y, ny) if y <= ny else (ny, y)

            lst = vertical.get(x)
            if lst is None:
                vertical[x] = [interval]
            else:
                lst.append(interval)

            y = ny

        elif d == b'D':
            ny = y - c
            interval = (y, ny) if y <= ny else (ny, y)

            lst = vertical.get(x)
            if lst is None:
                vertical[x] = [interval]
            else:
                lst.append(interval)

            y = ny

        elif d == b'L':
            nx = x - c
            interval = (nx, x) if nx <= x else (x, nx)

            lst = horizontal.get(y)
            if lst is None:
                horizontal[y] = [interval]
            else:
                lst.append(interval)

            x = nx

        else:  # 'R'
            nx = x + c
            interval = (x, nx) if x <= nx else (nx, x)

            lst = horizontal.get(y)
            if lst is None:
                horizontal[y] = [interval]
            else:
                lst.append(interval)

            x = nx

    data = None

    merge_groups(horizontal)
    merge_groups(vertical)

    br = bisect_right
    h_get = horizontal.get
    v_get = vertical.get

    ans = 0

    for hx, hy in houses:
        se = h_get(hy)
        if se is not None:
            starts, ends = se
            i = br(starts, hx) - 1
            if i >= 0 and ends[i] >= hx:
                ans += 1
                continue

        se = v_get(hx)
        if se is not None:
            starts, ends = se
            i = br(starts, hy) - 1
            if i >= 0 and ends[i] >= hy:
                ans += 1

    sys.stdout.write(f"{x} {y} {ans}\n")


if __name__ == "__main__":
    solve()