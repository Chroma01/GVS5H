import sys
from bisect import bisect_right


def merge_intervals(d):
    for ivs in d.values():
        if len(ivs) > 1:
            ivs.sort()
            w = 0
            cl, cr = ivs[0]
            for i in range(1, len(ivs)):
                l, r = ivs[i]
                if l <= cr:
                    if r > cr:
                        cr = r
                else:
                    ivs[w] = (cl, cr)
                    w += 1
                    cl, cr = l, r
            ivs[w] = (cl, cr)
            del ivs[w + 1:]


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    N = int(data[idx])
    M = int(data[idx + 1])
    sx = int(data[idx + 2])
    sy = int(data[idx + 3])
    idx += 4

    houses = []
    house_ys = set()
    house_xs = set()

    for _ in range(N):
        x = int(data[idx])
        y = int(data[idx + 1])
        idx += 2
        houses.append((x, y))
        house_ys.add(y)
        house_xs.add(x)

    x = sx
    y = sy
    horiz = {}
    vert = {}

    for _ in range(M):
        d = data[idx]
        c = int(data[idx + 1])
        idx += 2

        if d == b'U':
            ny = y + c
            if x in house_xs:
                lst = vert.get(x)
                if lst is None:
                    vert[x] = [(y, ny)]
                else:
                    lst.append((y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            if x in house_xs:
                lst = vert.get(x)
                if lst is None:
                    vert[x] = [(ny, y)]
                else:
                    lst.append((ny, y))
            y = ny
        elif d == b'L':
            nx = x - c
            if y in house_ys:
                lst = horiz.get(y)
                if lst is None:
                    horiz[y] = [(nx, x)]
                else:
                    lst.append((nx, x))
            x = nx
        else:  # R
            nx = x + c
            if y in house_ys:
                lst = horiz.get(y)
                if lst is None:
                    horiz[y] = [(x, nx)]
                else:
                    lst.append((x, nx))
            x = nx

    del data
    del house_ys, house_xs

    merge_intervals(horiz)
    merge_intervals(vert)

    INF = 10 ** 30
    br = bisect_right
    hget = horiz.get
    vget = vert.get
    ans = 0

    for hx, hy in houses:
        ivs = hget(hy)
        if ivs is not None:
            if len(ivs) == 1:
                l, r = ivs[0]
                if l <= hx <= r:
                    ans += 1
                    continue
            else:
                i = br(ivs, (hx, INF)) - 1
                if i >= 0 and ivs[i][1] >= hx:
                    ans += 1
                    continue

        ivs = vget(hx)
        if ivs is not None:
            if len(ivs) == 1:
                l, r = ivs[0]
                if l <= hy <= r:
                    ans += 1
                    continue
            else:
                i = br(ivs, (hy, INF)) - 1
                if i >= 0 and ivs[i][1] >= hy:
                    ans += 1

    sys.stdout.write(f"{x} {y} {ans}\n")


if __name__ == "__main__":
    main()