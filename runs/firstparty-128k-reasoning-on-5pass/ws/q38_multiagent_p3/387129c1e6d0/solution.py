import sys
from bisect import bisect_right


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    y = int(data[idx]); idx += 1

    houses = []
    for _ in range(N):
        hx = int(data[idx])
        hy = int(data[idx + 1])
        idx += 2
        houses.append((hx, hy))

    horizontal = {}
    vertical = {}

    for _ in range(M):
        d = data[idx]
        c = int(data[idx + 1])
        idx += 2

        ox, oy = x, y

        if d == b'U':
            y += c
        elif d == b'D':
            y -= c
        elif d == b'L':
            x -= c
        else:  # b'R'
            x += c

        if d == b'U' or d == b'D':
            if oy < y:
                a, b = oy, y
            else:
                a, b = y, oy
            vertical.setdefault(ox, []).append((a, b))
        else:
            if ox < x:
                a, b = ox, x
            else:
                a, b = x, ox
            horizontal.setdefault(y, []).append((a, b))

    del data

    def merge_intervals_by_key(groups):
        for key, intervals in groups.items():
            if len(intervals) == 1:
                s, e = intervals[0]
                groups[key] = ([s], [e])
                continue

            intervals.sort()
            starts = []
            ends = []

            cur_s, cur_e = intervals[0]
            for s, e in intervals[1:]:
                if s <= cur_e:
                    if e > cur_e:
                        cur_e = e
                else:
                    starts.append(cur_s)
                    ends.append(cur_e)
                    cur_s, cur_e = s, e

            starts.append(cur_s)
            ends.append(cur_e)
            groups[key] = (starts, ends)

    merge_intervals_by_key(horizontal)
    merge_intervals_by_key(vertical)

    count = 0
    br = bisect_right

    for hx, hy in houses:
        hit = False

        item = horizontal.get(hy)
        if item is not None:
            starts, ends = item
            i = br(starts, hx) - 1
            if i >= 0 and starts[i] <= hx <= ends[i]:
                hit = True

        if not hit:
            item = vertical.get(hx)
            if item is not None:
                starts, ends = item
                i = br(starts, hy) - 1
                if i >= 0 and starts[i] <= hy <= ends[i]:
                    hit = True

        if hit:
            count += 1

    sys.stdout.write(f"{x} {y} {count}\n")


if __name__ == "__main__":
    solve()