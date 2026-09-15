import sys
from bisect import bisect_right
from collections import defaultdict


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    cx = int(next(it))
    cy = int(next(it))

    hx = [0] * N
    hy = [0] * N
    for i in range(N):
        hx[i] = int(next(it))
        hy[i] = int(next(it))

    hmap = defaultdict(list)  # y -> list of x-intervals
    vmap = defaultdict(list)  # x -> list of y-intervals

    for _ in range(M):
        d = next(it)
        c = int(next(it))

        if d == b'U':
            ny = cy + c
            vmap[cx].append((cy, ny))
            cy = ny
        elif d == b'D':
            ny = cy - c
            vmap[cx].append((ny, cy))
            cy = ny
        elif d == b'L':
            nx = cx - c
            hmap[cy].append((nx, cx))
            cx = nx
        else:  # b'R'
            nx = cx + c
            hmap[cy].append((cx, nx))
            cx = nx

    del data, it

    def merge(mp):
        for key in list(mp):
            intervals = mp[key]
            intervals.sort()

            itv = iter(intervals)
            cur_l, cur_r = next(itv)

            starts = []
            ends = []

            for l, r in itv:
                # All house coordinates are integers, so adjacent integer
                # intervals can be merged without changing covered houses.
                if l <= cur_r + 1:
                    if r > cur_r:
                        cur_r = r
                else:
                    starts.append(cur_l)
                    ends.append(cur_r)
                    cur_l, cur_r = l, r

            starts.append(cur_l)
            ends.append(cur_r)
            mp[key] = (starts, ends)

    merge(hmap)
    merge(vmap)

    ans = 0
    br = bisect_right
    hget = hmap.get
    vget = vmap.get

    for i in range(N):
        px = hx[i]
        py = hy[i]

        hv = hget(py)
        if hv is not None:
            starts, ends = hv
            idx = br(starts, px) - 1
            if idx >= 0 and ends[idx] >= px:
                ans += 1
                continue

        vv = vget(px)
        if vv is not None:
            starts, ends = vv
            idx = br(starts, py) - 1
            if idx >= 0 and ends[idx] >= py:
                ans += 1

    sys.stdout.write(f"{cx} {cy} {ans}\n")


if __name__ == "__main__":
    solve()