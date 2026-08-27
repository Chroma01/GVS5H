import sys
import bisect
from collections import defaultdict

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))

    # read all houses
    houses = [(int(next(it)), int(next(it))) for _ in range(N)]

    # intervals for horizontal (fixed y) and vertical (fixed x) moves
    y_intervals = defaultdict(list)   # y -> list of (x_left, x_right)
    x_intervals = defaultdict(list)   # x -> list of (y_low, y_high)

    cur_x, cur_y = Sx, Sy

    for _ in range(M):
        d = next(it)          # direction as bytes, e.g. b'L'
        c = int(next(it))

        if d == b'L' or d == b'R':
            # horizontal move
            new_x = cur_x - c if d == b'L' else cur_x + c
            new_y = cur_y
            xl = cur_x if cur_x < new_x else new_x
            xr = new_x if cur_x < new_x else cur_x
            y_intervals[cur_y].append((xl, xr))
        else:
            # vertical move (U or D)
            new_y = cur_y - c if d == b'D' else cur_y + c
            new_x = cur_x
            yl = cur_y if cur_y < new_y else new_y
            yr = new_y if cur_y < new_y else cur_y
            x_intervals[cur_x].append((yl, yr))

        cur_x, cur_y = new_x, new_y

    final_x, final_y = cur_x, cur_y

    # -------- merge intervals for each fixed coordinate ----------------
    def merge_intervals(interval_dict):
        merged = {}
        for key, lst in interval_dict.items():
            if not lst:
                continue
            # sort by left (or low) endpoint
            lst.sort(key=lambda p: p[0])
            merged_intervals = []
            start, end = lst[0]
            for l, r in lst[1:]:
                if l <= end:               # overlapping or touching
                    if r > end:
                        end = r
                else:
                    merged_intervals.append((start, end))
                    start, end = l, r
            merged_intervals.append((start, end))
            starts = [iv[0] for iv in merged_intervals]
            ends   = [iv[1] for iv in merged_intervals]
            merged[key] = (starts, ends)
        return merged

    y_data = merge_intervals(y_intervals)   # y -> (list of lefts, list of rights)
    x_data = merge_intervals(x_intervals)   # x -> (list of lows,  list of highs)

    # -------- count distinct visited houses ---------------------------
    visited_cnt = 0
    for hx, hy in houses:
        visited = False

        # check horizontal segments
        if hy in y_data:
            starts, ends = y_data[hy]
            idx = bisect.bisect_right(starts, hx) - 1
            if idx >= 0 and hx <= ends[idx]:
                visited = True

        # check vertical segments if not already visited
        if not visited and hx in x_data:
            starts, ends = x_data[hx]
            idx = bisect.bisect_right(starts, hy) - 1
            if idx >= 0 and hy <= ends[idx]:
                visited = True

        if visited:
            visited_cnt += 1

    # -------- output --------------------------------------------------
    sys.stdout.write(f"{final_x} {final_y} {visited_cnt}")

if __name__ == "__main__":
    solve()