import sys

def build_detour(L, k):
    """
    Diagonal path b1..bL (L >= 1) such that:
      - b1 is orthogonally adjacent to Ra = (2, k+1),
      - consecutive squares are diagonally adjacent,
      - bL is diagonally adjacent to Rb = (3, k+1),
      - all squares are distinct and lie in the empty region
        (row 1, or column >= k+2, or row >= 4),
      so they never collide with the red skeleton on rows 2-3, cols 2..k+1.
    """
    if L == 1:
        return [(2, k + 2)]
    if L == 2:
        return [(1, k + 1), (2, k + 2)]
    if L == 3:
        return [(2, k + 2), (3, k + 3), (4, k + 2)]
    if L == 4:
        return [(1, k + 1), (2, k + 2), (3, k + 3), (4, k + 2)]

    path = []
    if L % 2 == 1:
        # L = 2t+1, t >= 2. Outward zigzag on rows 2,3 starting (2,k+2).
        t = (L - 1) // 2
        if t % 2 == 0:
            # t even: t outward squares, last is (3, k+1+t); one step down to row 4.
            path.append((2, k + 2))
            for j in range(2, t + 1):
                path.append((3 if j % 2 == 0 else 2, k + 1 + j))
            path.append((4, k + 2 + t))
            col = k + 2 + t
        else:
            # t odd >= 3: t-1 (even) outward squares ending on row 3,
            # then two down-steps to reach row 4 with correct parity.
            te = t - 1
            path.append((2, k + 2))
            for j in range(2, te + 1):
                path.append((3 if j % 2 == 0 else 2, k + 1 + j))
            path.append((4, k + 2 + te))
            path.append((5, k + 3 + te))
            path.append((4, k + 4 + te))
            col = k + 4 + te
    else:
        # L = 2t+2, t >= 2. Outward zigzag on rows 1,2 starting (1,k+1).
        t = (L - 2) // 2
        path.append((1, k + 1))
        for j in range(2, t + 1):
            path.append((2 if j % 2 == 0 else 1, k + j))
        if t % 2 == 0:
            # last outward square is (2, k+t); go down through col >= k+2.
            path.append((3, k + t + 1))
            path.append((4, k + t + 2))
            col = k + t + 2
        else:
            # last outward square is (1, k+t); three down-steps for parity.
            path.append((2, k + t + 1))
            path.append((3, k + t + 2))
            path.append((4, k + t + 3))
            col = k + t + 3

    # Return leg: zigzag left along rows 5,4 with decreasing columns,
    # finishing at (4, k+2), which is diagonally adjacent to Rb = (3, k+1).
    r = 5
    c = col - 1
    while c >= k + 3:
        path.append((r, c))
        r = 4 if r == 5 else 5
        c -= 1
    path.append((4, k + 2))
    return path


def solve():
    data = sys.stdin.buffer.read().split()
    T = int(data[0])
    pos = 1
    out = []
    for _ in range(T):
        R = int(data[pos]); B = int(data[pos + 1]); pos += 2

        # Necessary conditions:
        #  - each red piece's move flips (r+c) parity, blue preserves it,
        #    so around the closed cycle R must be even;
        #  - with R = 0 every move flips r-parity, so B must be even.
        if (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue

        pieces = []
        if R == 0:
            # All blue, B even >= 2: two diagonal legs forming a loop.
            # Leg 1: (1,1),(2,2),...,(k,k); leg 2: (k+1,k),(k,k-1),...,(2,1).
            kk = B // 2
            for i in range(1, kk + 1):
                pieces.append(('B', i, i))
            for i in range(1, kk + 1):
                pieces.append(('B', kk + 2 - i, kk + 1 - i))
        elif B == 0:
            # All red, R even >= 2: perimeter of a 2 x k rectangle (rows 2-3).
            kk = R // 2
            if kk == 1:
                pieces.append(('R', 2, 2))
                pieces.append(('R', 3, 2))
            else:
                for c in range(2, kk + 2):
                    pieces.append(('R', 2, c))
                for c in range(kk + 1, 1, -1):
                    pieces.append(('R', 3, c))
        else:
            # R even >= 2, B >= 1:
            # red skeleton = perimeter of 2 x k rectangle (rows 2-3, cols 2..k+1),
            # with all blues inserted as one diagonal detour between the
            # vertical red pair Ra = (2,k+1) and Rb = (3,k+1).
            kk = R // 2
            if kk == 1:
                skel = [(2, 2), (3, 2)]
            else:
                skel = [(2, c) for c in range(2, kk + 2)]
                skel += [(3, c) for c in range(kk + 1, 1, -1)]
            blues = build_detour(B, kk)
            for i in range(kk):
                pieces.append(('R', skel[i][0], skel[i][1]))
            for (r, c) in blues:
                pieces.append(('B', r, c))
            for i in range(kk, R):
                pieces.append(('R', skel[i][0], skel[i][1]))

        out.append("Yes")
        for p in pieces:
            out.append(f"{p[0]} {p[1]} {p[2]}")

    sys.stdout.write("\n".join(out) + "\n")

solve()