import sys
from bisect import bisect_left, bisect_right


def solve():
    input = sys.stdin.buffer.readline

    first = input().split()
    if not first:
        return

    N = int(first[0])
    M = int(first[1])
    curx = int(first[2])
    cury = int(first[3])

    h_lines = {}
    v_lines = {}

    for i in range(N):
        x, y = map(int, input().split())

        lst = h_lines.get(y)
        if lst is None:
            h_lines[y] = [(x, i)]
        else:
            lst.append((x, i))

        lst = v_lines.get(x)
        if lst is None:
            v_lines[x] = [(y, i)]
        else:
            lst.append((y, i))

    for y, lst in h_lines.items():
        lst.sort()
        xs = [p[0] for p in lst]
        ids = [p[1] for p in lst]
        h_lines[y] = (xs, ids)

    for x, lst in v_lines.items():
        lst.sort()
        ys = [p[0] for p in lst]
        ids = [p[1] for p in lst]
        v_lines[x] = (ys, ids)

    h_updates = {}
    v_updates = {}

    bl = bisect_left
    br = bisect_right
    h_get = h_lines.get
    v_get = v_lines.get

    for _ in range(M):
        d, c = input().split()
        c = int(c)

        if d == b'U':
            ny = cury + c
            line = v_get(curx)
            if line is not None:
                ys = line[0]
                l = bl(ys, cury)
                r = br(ys, ny) - 1
                if l <= r:
                    lst = v_updates.get(curx)
                    if lst is None:
                        v_updates[curx] = [(l, r)]
                    else:
                        lst.append((l, r))
            cury = ny

        elif d == b'D':
            ny = cury - c
            line = v_get(curx)
            if line is not None:
                ys = line[0]
                l = bl(ys, ny)
                r = br(ys, cury) - 1
                if l <= r:
                    lst = v_updates.get(curx)
                    if lst is None:
                        v_updates[curx] = [(l, r)]
                    else:
                        lst.append((l, r))
            cury = ny

        elif d == b'L':
            nx = curx - c
            line = h_get(cury)
            if line is not None:
                xs = line[0]
                l = bl(xs, nx)
                r = br(xs, curx) - 1
                if l <= r:
                    lst = h_updates.get(cury)
                    if lst is None:
                        h_updates[cury] = [(l, r)]
                    else:
                        lst.append((l, r))
            curx = nx

        else:  # b'R'
            nx = curx + c
            line = h_get(cury)
            if line is not None:
                xs = line[0]
                l = bl(xs, curx)
                r = br(xs, nx) - 1
                if l <= r:
                    lst = h_updates.get(cury)
                    if lst is None:
                        h_updates[cury] = [(l, r)]
                    else:
                        lst.append((l, r))
            curx = nx

    covered = bytearray(N)

    for key, updates in h_updates.items():
        xs, ids = h_lines[key]
        diff = [0] * (len(xs) + 1)

        for l, r in updates:
            diff[l] += 1
            diff[r + 1] -= 1

        cur = 0
        for i in range(len(xs)):
            cur += diff[i]
            if cur > 0:
                covered[ids[i]] = 1

    for key, updates in v_updates.items():
        ys, ids = v_lines[key]
        diff = [0] * (len(ys) + 1)

        for l, r in updates:
            diff[l] += 1
            diff[r + 1] -= 1

        cur = 0
        for i in range(len(ys)):
            cur += diff[i]
            if cur > 0:
                covered[ids[i]] = 1

    sys.stdout.write(f"{curx} {cury} {sum(covered)}\n")


if __name__ == "__main__":
    solve()