import sys
from bisect import bisect_right
from collections import defaultdict


def merge_inplace(ints):
    if len(ints) <= 1:
        return
    ints.sort()
    w = 0
    cl, cr = ints[0]
    for i in range(1, len(ints)):
        l, r = ints[i]
        if l <= cr + 1:
            if r > cr:
                cr = r
        else:
            ints[w] = (cl, cr)
            w += 1
            cl, cr = l, r
    ints[w] = (cl, cr)
    del ints[w + 1:]


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0

    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    Sx = int(data[idx]); idx += 1
    Sy = int(data[idx]); idx += 1

    houses = []
    for _ in range(N):
        hx = int(data[idx])
        hy = int(data[idx + 1])
        idx += 2
        houses.append((hx, hy))

    x, y = Sx, Sy
    horizontal = defaultdict(list)
    vertical = defaultdict(list)

    for _ in range(M):
        d = data[idx]
        c = int(data[idx + 1])
        idx += 2

        if d == b'U':
            ny = y + c
            vertical[x].append((y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            vertical[x].append((ny, y))
            y = ny
        elif d == b'L':
            nx = x - c
            horizontal[y].append((nx, x))
            x = nx
        else:  # R
            nx = x + c
            horizontal[y].append((x, nx))
            x = nx

    del data

    for intervals in horizontal.values():
        merge_inplace(intervals)
    for intervals in vertical.values():
        merge_inplace(intervals)

    INF = 10 ** 30
    br = bisect_right
    h_get = horizontal.get
    v_get = vertical.get

    count = 0
    for hx, hy in houses:
        covered = False

        lst = h_get(hy)
        if lst is not None:
            i = br(lst, (hx, INF)) - 1
            if i >= 0 and lst[i][1] >= hx:
                covered = True

        if not covered:
            lst = v_get(hx)
            if lst is not None:
                i = br(lst, (hy, INF)) - 1
                if i >= 0 and lst[i][1] >= hy:
                    covered = True

        count += covered

    print(x, y, count)


if __name__ == "__main__":
    main()