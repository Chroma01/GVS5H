import sys

def sweep_line(houses, intervals, visited, count):
    if not houses or not intervals:
        return count
    if len(houses) > 1:
        houses.sort()
    if len(intervals) > 1:
        intervals.sort()
    idx = 0
    nh = len(houses)
    vis = visited
    it = iter(intervals)
    cur_l, cur_r = next(it)
    for l, r in it:
        if l <= cur_r:
            if r > cur_r:
                cur_r = r
        else:
            while idx < nh and houses[idx][0] < cur_l:
                idx += 1
            while idx < nh and houses[idx][0] <= cur_r:
                hid = houses[idx][1]
                if not vis[hid]:
                    vis[hid] = True
                    count += 1
                idx += 1
            cur_l, cur_r = l, r
    while idx < nh and houses[idx][0] < cur_l:
        idx += 1
    while idx < nh and houses[idx][0] <= cur_r:
        hid = houses[idx][1]
        if not vis[hid]:
            vis[hid] = True
            count += 1
        idx += 1
    return count

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    x = int(next(it))
    y = int(next(it))

    y_houses = {}
    x_houses = {}
    for i in range(N):
        hx = int(next(it))
        hy = int(next(it))
        lst = y_houses.get(hy)
        if lst is None:
            y_houses[hy] = [(hx, i)]
        else:
            lst.append((hx, i))
        lst = x_houses.get(hx)
        if lst is None:
            x_houses[hx] = [(hy, i)]
        else:
            lst.append((hy, i))

    h_intervals = {}
    v_intervals = {}
    for _ in range(M):
        d = next(it)
        c = int(next(it))
        if d == b'U':
            old = y
            y += c
            lst = v_intervals.get(x)
            if lst is None:
                v_intervals[x] = [(old, y)]
            else:
                lst.append((old, y))
        elif d == b'D':
            old = y
            y -= c
            lst = v_intervals.get(x)
            if lst is None:
                v_intervals[x] = [(y, old)]
            else:
                lst.append((y, old))
        elif d == b'L':
            old = x
            x -= c
            lst = h_intervals.get(y)
            if lst is None:
                h_intervals[y] = [(x, old)]
            else:
                lst.append((x, old))
        else:  # R
            old = x
            x += c
            lst = h_intervals.get(y)
            if lst is None:
                h_intervals[y] = [(old, x)]
            else:
                lst.append((old, x))

    del data, it

    visited = [False] * N
    count = 0

    for y_line, intervals in h_intervals.items():
        houses = y_houses.get(y_line)
        if houses:
            count = sweep_line(houses, intervals, visited, count)
            if count == N:
                break

    if count < N:
        for x_line, intervals in v_intervals.items():
            houses = x_houses.get(x_line)
            if houses:
                count = sweep_line(houses, intervals, visited, count)
                if count == N:
                    break

    sys.stdout.write(f"{x} {y} {count}\n")

if __name__ == "__main__":
    main()