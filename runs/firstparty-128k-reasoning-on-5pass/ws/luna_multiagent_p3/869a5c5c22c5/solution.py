import sys

BASE = 300000


def conv(x, y):
    return BASE + x + y, BASE + x - y


def make_blue(b):
    if b == 1:
        xy = [(0, 0)]
    elif b == 2:
        xy = [(0, 0), (1, 0)]
    elif b % 2 == 0:
        q = (b - 4) // 2
        xy = [(0, 0)]
        xy.extend((-i, 0) for i in range(1, q + 1))
        xy.append((-q, -1))
        xy.extend((x, -1) for x in range(-q + 1, 1))
        xy.extend([(1, -1), (1, 0)])
    else:
        q = (b - 3) // 2
        xy = [(0, 0)]
        xy.extend((-i, 0) for i in range(1, q + 1))
        xy.append((-q, 1))
        xy.extend((x, 1) for x in range(-q + 1, 1))
        xy.append((1, 1))

    return [conv(x, y) for x, y in xy]


def append_segment(path, target):
    r, c = path[-1]
    tr, tc = target

    if tr != r:
        step = 1 if tr > r else -1
        for _ in range(abs(tr - r)):
            r += step
            path.append((r, c))

    if tc != c:
        step = 1 if tc > c else -1
        for _ in range(abs(tc - c)):
            c += step
            path.append((r, c))


def make_red_path(b, r):
    """
    Return r red vertices, starting after the blue path and ending at A.
    Consecutive vertices in this list are orthogonally adjacent.
    """
    x = BASE
    y = BASE
    a = (x + 1, y)
    length = r - 1

    if b == 1:
        # The blue endpoint is (x,y), and this path starts at (x+1,y+1).
        s = (length - 1) // 2
        d = (x + 1, y + 1)
        path = [d]
        append_segment(path, (x + 1 + s, y))
        append_segment(path, a)
        return path

    if length == 1:
        if b % 2 == 0:
            d = (x + 2, y)
        else:
            d = (x + 1, y + 1)
        return [d, a]

    if b % 2 == 0:
        d = (x + 2, y)

        if length == 3:
            path = [d]
            append_segment(path, (x + 3, y))
            append_segment(path, a)
        else:
            s = (length - 3) // 2
            top = (x + 3, y - s)
            path = [d]
            append_segment(path, (x + 3, y))
            append_segment(path, top)
            append_segment(path, (x + 1, y - s))
            append_segment(path, a)
    else:
        d = (x + 3, y + 1)

        if length == 3:
            path = [d]
            append_segment(path, (x + 2, y + 1))
            append_segment(path, (x + 1, y + 1))
            append_segment(path, a)
        elif length == 5:
            path = [d]
            append_segment(path, (x + 3, y + 2))
            append_segment(path, (x + 2, y + 2))
            append_segment(path, (x + 1, y + 2))
            append_segment(path, (x + 1, y + 1))
            append_segment(path, a)
        else:
            s = (length - 5) // 2
            top = (x + 4, y + 1 + s)
            path = [d]
            append_segment(path, (x + 4, y + 1))
            append_segment(path, top)
            append_segment(path, (x + 1, y + 1 + s))
            append_segment(path, a)

    return path


def pure_red(r):
    if r == 2:
        return [(1, 1), (1, 2)]

    k = r // 2
    return (
        [(1, c) for c in range(1, k + 1)]
        + [(2, c) for c in range(k, 0, -1)]
    )


def pure_blue(b):
    if b == 2:
        return [conv(0, 0), conv(1, 0)]

    k = b // 2
    xy = [(x, 0) for x in range(k)]
    xy.extend((x, 1) for x in range(k - 1, -1, -1))
    return [conv(x, y) for x, y in xy]


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        r, b = data[pos], data[pos + 1]
        pos += 2

        if r % 2 == 1:
            out.append("No")
            continue

        if r == 0:
            if b % 2 == 1:
                out.append("No")
                continue

            ans = pure_blue(b)
            out.append("Yes")
            out.extend(f"B {row} {col}" for row, col in ans)
            continue

        if b == 0:
            ans = pure_red(r)
            out.append("Yes")
            out.extend(f"R {row} {col}" for row, col in ans)
            continue

        a = (BASE + 1, BASE)
        blue = make_blue(b)
        red = make_red_path(b, r)

        out.append("Yes")
        out.append(f"R {a[0]} {a[1]}")
        out.extend(f"B {row} {col}" for row, col in blue)
        out.extend(f"R {row} {col}" for row, col in red[:-1])

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()