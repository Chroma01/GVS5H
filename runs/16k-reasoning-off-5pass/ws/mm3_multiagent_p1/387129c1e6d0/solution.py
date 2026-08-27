import sys
import bisect

def solve() -> None:
    data = sys.stdin.read().split()
    it = iter(data)
    try:
        N = int(next(it))
    except StopIteration:
        return
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))

    xs = [0] * N
    ys = [0] * N
    for i in range(N):
        xs[i] = int(next(it))
        ys[i] = int(next(it))

    # Build maps: x -> list of (y, index), y -> list of (x, index)
    by_x = {}
    by_y = {}
    for i in range(N):
        x = xs[i]
        y = ys[i]
        if x not in by_x:
            by_x[x] = []
        by_x[x].append((y, i))
        if y not in by_y:
            by_y[y] = []
        by_y[y].append((x, i))

    # Sort lists for binary search
    for lst in by_x.values():
        lst.sort(key=lambda p: p[0])
    for lst in by_y.values():
        lst.sort(key=lambda p: p[0])

    seen = [False] * N
    count = 0

    # Pre-fetch bisect functions for speed
    bisect_left = bisect.bisect_left
    bisect_right = bisect.bisect_right

    cur_x = Sx
    cur_y = Sy

    for _ in range(M):
        d = next(it)
        c = int(next(it))
        if d == 'L':
            new_x = cur_x - c
            lo, hi = new_x, cur_x
            lst = by_y.get(cur_y)
            if lst is not None:
                # Houses with y == cur_y, varying x in [lo, hi]
                # lst sorted by x
                l = bisect_left(lst, (lo, -1))
                r = bisect_right(lst, (hi, float('inf')))
                for k in range(l, r):
                    idx = lst[k][1]
                    if not seen[idx]:
                        seen[idx] = True
                        count += 1
            cur_x = new_x
        elif d == 'R':
            new_x = cur_x + c
            lo, hi = cur_x, new_x
            lst = by_y.get(cur_y)
            if lst is not None:
                l = bisect_left(lst, (lo, -1))
                r = bisect_right(lst, (hi, float('inf')))
                for k in range(l, r):
                    idx = lst[k][1]
                    if not seen[idx]:
                        seen[idx] = True
                        count += 1
            cur_x = new_x
        elif d == 'D':
            new_y = cur_y - c
            lo, hi = new_y, cur_y
            lst = by_x.get(cur_x)
            if lst is not None:
                # lst sorted by y
                l = bisect_left(lst, (lo, -1))
                r = bisect_right(lst, (hi, float('inf')))
                for k in range(l, r):
                    idx = lst[k][1]
                    if not seen[idx]:
                        seen[idx] = True
                        count += 1
            cur_y = new_y
        else:  # 'U'
            new_y = cur_y + c
            lo, hi = cur_y, new_y
            lst = by_x.get(cur_x)
            if lst is not None:
                l = bisect_left(lst, (lo, -1))
                r = bisect_right(lst, (hi, float('inf')))
                for k in range(l, r):
                    idx = lst[k][1]
                    if not seen[idx]:
                        seen[idx] = True
                        count += 1
            cur_y = new_y

    sys.stdout.write(f"{cur_x} {cur_y} {count}")

if __name__ == "__main__":
    solve()