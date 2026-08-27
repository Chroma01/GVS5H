import sys


def detour(U, V, p, k):
    """
    Replace edge U -> V by a same-move-type rectangular detour with 2k
    inserted vertices:
      U, U+p, ..., U+kp, V+kp, ..., V+p, V
    For red, p is perpendicular to the orthogonal edge U->V.
    For blue, p is the other diagonal direction perpendicular to U->V.
    Returns only the inserted vertices, excluding U and V.
    """
    if k == 0:
        return []
    ur, uc = U
    vr, vc = V
    pr, pc = p
    res = []
    for j in range(1, k + 1):
        res.append((ur + pr * j, uc + pc * j))
    for j in range(k, 0, -1):
        res.append((vr + pr * j, vc + pc * j))
    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    pos = 1
    out_lines = []

    for _ in range(t):
        R = data[pos]
        B = data[pos + 1]
        pos += 2
        n = R + B

        if (R & 1) or (R == 0 and (B & 1)):
            out_lines.append("No")
            continue

        base = None
        red_e = blue_e = None
        red_p = blue_p = None
        red_k = blue_k = 0

        if R == 0:
            # B is even and at least 2. Two diagonally adjacent blue pieces.
            base = [('B', 0, 0), ('B', 1, 1)]
            blue_e = 0
            blue_p = (1, -1)
            blue_k = (B - 2) // 2
        elif B == 0:
            # Two orthogonally adjacent red pieces.
            base = [('R', 0, 0), ('R', 1, 0)]
            red_e = 0
            red_p = (0, 1)
            red_k = (R - 2) // 2
        elif B & 1:
            # Valid triangle: R -> B -> R -> R.
            base = [('R', 0, 0), ('B', 0, 1), ('R', 1, 0)]
            blue_e = 1          # (0,1) -> (1,0), diagonal (1,-1)
            blue_p = (1, 1)     # expand to the opposite diagonal side
            blue_k = (B - 1) // 2
            red_e = 2           # (1,0) -> (0,0), orthogonal west
            red_p = (0, -1)     # expand south, disjoint from blue side
            red_k = (R - 2) // 2
        else:
            # B is even and positive. Valid 4-cycle R B B R.
            base = [('R', 0, 0), ('B', -1, 0), ('B', 0, 1), ('R', 1, 0)]
            blue_e = 1          # (-1,0) -> (0,1), diagonal (1,1)
            blue_p = (-1, 1)    # expand northwest, away from the red detour
            blue_k = (B - 2) // 2
            red_e = 3           # (1,0) -> (0,0), orthogonal west
            red_p = (0, -1)     # expand south
            red_k = (R - 2) // 2

        m = len(base)
        cyc = []
        for i, (col, r, c) in enumerate(base):
            cyc.append((col, r, c))
            nr, nc = base[(i + 1) % m][1], base[(i + 1) % m][2]
            if i == red_e:
                for rr, cc in detour((r, c), (nr, nc), red_p, red_k):
                    cyc.append(('R', rr, cc))
            if i == blue_e:
                for rr, cc in detour((r, c), (nr, nc), blue_p, blue_k):
                    cyc.append(('B', rr, cc))

        off = n + 10
        out_lines.append("Yes")
        for col, r, c in cyc:
            out_lines.append(f"{col} {r + off} {c + off}")

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()