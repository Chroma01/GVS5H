import sys
from collections import defaultdict
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    houses = []
    for _ in range(N):
        houses.append((int(next(it)), int(next(it))))

    # Horizontal segments grouped by y, vertical segments grouped by x.
    h_seg = defaultdict(list)  # y -> list of (l, r)
    v_seg = defaultdict(list)  # x -> list of (l, r)

    x, y = sx, sy
    for _ in range(M):
        d = next(it)
        c = int(next(it))

        if d == b'L':
            nx = x - c
            h_seg[y].append((nx, x))
            x = nx
        elif d == b'R':
            nx = x + c
            h_seg[y].append((x, nx))
            x = nx
        elif d == b'U':
            ny = y + c
            v_seg[x].append((y, ny))
            y = ny
        else:  # b'D'
            ny = y - c
            v_seg[x].append((ny, y))
            y = ny

    def merge_segments(groups):
        starts_map = {}
        ends_map = {}
        for key, intervals in groups.items():
            intervals.sort()
            starts = []
            ends = []

            cur_l, cur_r = intervals[0]
            for l, r in intervals[1:]:
                # Adjacent integer intervals can be merged safely.
                if l <= cur_r + 1:
                    if r > cur_r:
                        cur_r = r
                else:
                    starts.append(cur_l)
                    ends.append(cur_r)
                    cur_l, cur_r = l, r

            starts.append(cur_l)
            ends.append(cur_r)
            starts_map[key] = starts
            ends_map[key] = ends

        return starts_map, ends_map

    h_starts, h_ends = merge_segments(h_seg)
    v_starts, v_ends = merge_segments(v_seg)

    ans = 0
    for hx, hy in houses:
        covered = False

        if hy in h_starts:
            starts = h_starts[hy]
            idx = bisect_right(starts, hx) - 1
            if idx >= 0 and h_ends[hy][idx] >= hx:
                covered = True

        if not covered and hx in v_starts:
            starts = v_starts[hx]
            idx = bisect_right(starts, hy) - 1
            if idx >= 0 and v_ends[hx][idx] >= hy:
                covered = True

        if covered:
            ans += 1

    print(x, y, ans)


if __name__ == "__main__":
    main()