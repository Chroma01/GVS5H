import sys


def transformed_point(x, y):
    return x + y, x - y


def make_blue_path_to_20(length):
    """Path in transformed coordinates from (0,0) to (2,0), length even."""
    k = (length - 2) // 2
    path = []
    for y in range(1, k + 1):
        path.append((0, y))
    path.append((1, k))
    path.append((2, k))
    for y in range(k - 1, -1, -1):
        path.append((2, y))
    return path


def make_blue_path_to_10(length):
    """Path in transformed coordinates from (0,0) to (1,0), length odd."""
    if length == 1:
        return [(1, 0)]

    k = (length - 1) // 2
    path = []
    for y in range(1, k + 1):
        path.append((0, y))
    path.append((1, k))
    for y in range(k - 1, -1, -1):
        path.append((1, y))
    return path


def solve_case(R, B):
    if R % 2:
        return None

    if R == 0:
        if B % 2:
            return None
        if B == 2:
            return [("B", 100, 100), ("B", 101, 101)]

        p = 1
        q = B // 2 - 1
        uv = []

        for u in range(p + 1):
            uv.append((u, 0))
        for v in range(1, q + 1):
            uv.append((p, v))
        for u in range(p - 1, -1, -1):
            uv.append((u, q))
        for v in range(q - 1, 0, -1):
            uv.append((0, v))

        return [
            ("B", 100 + u + v, 100 + u - v)
            for u, v in uv
        ]

    if B == 0:
        if R < 2:
            return None
        if R == 2:
            return [("R", 100, 100), ("R", 100, 101)]

        w = R // 2
        ans = []
        for c in range(w):
            ans.append(("R", 100, 100 + c))
        for c in range(w - 1, -1, -1):
            ans.append(("R", 101, 100 + c))
        return ans

    # The first red edge is A=(0,1) -> F=(0,0).
    A = (0, 1)
    F = (0, 0)
    ans = [("R", *A), ("B", *F)]

    if B % 2:
        # Blue path ends at E=(2,2), and E -> D=(1,3) is diagonal.
        blue_vertices = make_blue_path_to_20(B - 1)
        D = (1, 3)
    else:
        # Blue path ends at E=(1,1), and E -> D=(0,2) is diagonal.
        blue_vertices = make_blue_path_to_10(B - 1)
        D = (0, 2)

    for x, y in blue_vertices:
        r, c = transformed_point(x, y)
        ans.append(("B", r, c))

    ans.append(("R", *D))

    # Add the remaining red path from D to A.
    # Its required length is R-1, always odd.
    k = (R - 2) // 2

    if B % 2:
        # D=(1,3), A=(0,1), base distance is 3.
        # For R=2, use the direct 3-edge path.
        r, c = D
        if k == 0:
            ans.extend([
                ("R", 1, 3),
                ("R", 0, 3),
                ("R", *A),
            ])
        else:
            # First use a 3-edge route, then add 2-edge excursions.
            ans.extend([
                ("R", 1, 4),
                ("R", 0, 4),
                ("R", 0, 3),
            ])
            r, c = 0, 3
            for _ in range(k):
                r -= 1
                ans.append(("R", r, c))
                c -= 1
                ans.append(("R", r, c))
                r += 1
                ans.append(("R", r, c))
                c -= 1
                ans.append(("R", r, c))
            # The above route is not used; replace with a clean translated
            # rectangle below.
            ans = ans[:-4 * k]
            r, c = 1, 3
            for _ in range(k):
                r += 1
                ans.append(("R", r, c))
            ans.append(("R", r, c - 1))
            c -= 1
            for _ in range(k + 1):
                r -= 1
                ans.append(("R", r, c))
            ans.append(("R", *A))
    else:
        # D=(0,2), A=(0,1).  Move through negative rows to avoid blue squares.
        r, c = D
        for _ in range(k):
            r -= 1
            ans.append(("R", r, c))
        c -= 1
        ans.append(("R", r, c))
        for _ in range(k):
            r += 1
            ans.append(("R", r, c))

    shift = R + B + 20
    return [(p, r + shift, c + shift) for p, r, c in ans]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        R, B = data[pos], data[pos + 1]
        pos += 2

        ans = solve_case(R, B)
        if ans is None:
            out.append("No")
        else:
            out.append("Yes")
            out.extend(f"{p} {r} {c}" for p, r, c in ans)

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()