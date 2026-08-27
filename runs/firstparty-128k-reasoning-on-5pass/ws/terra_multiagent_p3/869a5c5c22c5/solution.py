import sys

SHIFT = 300000


def cardinal_cycle(n):
    # A simple cardinal cycle with n vertices, for even n >= 2.
    h = (n - 2) // 2
    pts = [(0, 0)]
    for r in range(1, h + 1):
        pts.append((r, 0))
    pts.append((h, 1))
    for r in range(h - 1, -1, -1):
        pts.append((r, 1))
    return pts


def build(R, B):
    # A red move flips parity of r+c, while a blue move preserves it.
    if R % 2:
        return None

    # With blue moves only, every move flips row parity.
    if R == 0 and B % 2:
        return None

    if B == 0:
        return [("R", r, c) for r, c in cardinal_cycle(R)]

    if R == 0:
        # For x=(r+c)/2, y=(r-c)/2, a cardinal move in (x,y)
        # becomes a diagonal move in board coordinates.
        return [
            ("B", x + y, x - y)
            for x, y in cardinal_cycle(B)
        ]

    ans = []

    if B % 2 == 0:
        # Red path from A=(0,0) to P=(0,2), with P becoming
        # the first blue vertex.
        h = (R - 2) // 2
        red_path = [(0, 0)]
        for r in range(1, h + 1):
            red_path.append((r, 0))
        red_path.append((h, 1))
        red_path.append((h, 2))
        for r in range(h - 1, -1, -1):
            red_path.append((r, 2))

        # Blue path in transformed coordinates from P=(1,-1)
        # back to A=(0,0).
        k = (B - 2) // 2
        blue_path = [(1, -1)]
        for y in range(-2, -k - 2, -1):
            blue_path.append((1, y))
        blue_path.append((0, -k - 1))
        for y in range(-k, 1):
            blue_path.append((0, y))

        ans.extend(("R", r, c) for r, c in red_path[:-1])
        ans.extend(("B", x + y, x - y) for x, y in blue_path[:-1])

    else:
        # Red path from A=(0,0) to P=(1,1).
        h = (R - 2) // 2
        red_path = [(0, 0)]
        for r in range(1, h + 2):
            red_path.append((r, 0))
        red_path.append((h + 1, 1))
        for r in range(h, 0, -1):
            red_path.append((r, 1))

        # Blue path in transformed coordinates from P=(1,0)
        # back to A=(0,0).
        k = (B - 1) // 2
        blue_path = [(1, 0)]
        for y in range(-1, -k - 1, -1):
            blue_path.append((1, y))
        blue_path.append((0, -k))
        for y in range(-k + 1, 1):
            blue_path.append((0, y))

        ans.extend(("R", r, c) for r, c in red_path[:-1])
        ans.extend(("B", x + y, x - y) for x, y in blue_path[:-1])

    return ans


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    T = data[0]
    idx = 1
    out = []

    for _ in range(T):
        R = data[idx]
        B = data[idx + 1]
        idx += 2

        placement = build(R, B)

        if placement is None:
            out.append("No")
            continue

        out.append("Yes")
        for piece, r, c in placement:
            out.append(f"{piece} {r + SHIFT} {c + SHIFT}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()