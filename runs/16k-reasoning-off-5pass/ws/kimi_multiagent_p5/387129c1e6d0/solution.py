import sys
from bisect import bisect_right
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    y = int(data[idx]); idx += 1

    houses = []
    for _ in range(N):
        hx = int(data[idx]); idx += 1
        hy = int(data[idx]); idx += 1
        houses.append((hx, hy))

    row_intervals = defaultdict(list)  # y -> list of (x1, x2)
    col_intervals = defaultdict(list)  # x -> list of (y1, y2)

    for _ in range(M):
        d = data[idx].decode(); idx += 1
        c = int(data[idx]); idx += 1
        if d == 'U':
            col_intervals[x].append((y, y + c))
            y += c
        elif d == 'D':
            col_intervals[x].append((y - c, y))
            y -= c
        elif d == 'L':
            row_intervals[y].append((x - c, x))
            x -= c
        else:  # 'R'
            row_intervals[y].append((x, x + c))
            x += c

    # Merge intervals per key; store sorted starts and ends arrays.
    def merge(intervals):
        intervals.sort()
        starts = []
        ends = []
        for a, b in intervals:
            if starts and a <= ends[-1] + 1:
                if b > ends[-1]:
                    ends[-1] = b
            else:
                starts.append(a)
                ends.append(b)
        return starts, ends

    row_merged = {}
    for k, v in row_intervals.items():
        row_merged[k] = merge(v)
    col_merged = {}
    for k, v in col_intervals.items():
        col_merged[k] = merge(v)

    def covered(starts, ends, p):
        # is p inside any merged interval?
        i = bisect_right(starts, p) - 1
        return i >= 0 and ends[i] >= p

    count = 0
    for hx, hy in houses:
        hit = False
        rm = row_merged.get(hy)
        if rm is not None and covered(rm[0], rm[1], hx):
            hit = True
        if not hit:
            cm = col_merged.get(hx)
            if cm is not None and covered(cm[0], cm[1], hy):
                hit = True
        if hit:
            count += 1

    sys.stdout.write(f"{x} {y} {count}\n")

main()