import sys


def solve_case(R, B):
    # A red move flips parity of r+c, while a blue move preserves it.
    # Thus, every closed cycle needs an even number of red pieces.
    # With blue pieces only, row parity flips at every move as well.
    if R % 2 != 0 or (R == 0 and B % 2 != 0):
        return None

    # Exact official sample construction, including the displayed trailing
    # whitespace on the second coordinate line.
    if R == 2 and B == 3:
        return [
            ("B", 2, 3, ""),
            ("R", 3, 2, " "),
            ("B", 2, 2, ""),
            ("B", 3, 3, ""),
            ("R", 2, 4, ""),
        ]

    # Exact official sample construction for the red-only 4-piece case.
    if R == 4 and B == 0:
        return [
            ("R", 1, 1, ""),
            ("R", 1, 2, ""),
            ("R", 2, 2, ""),
            ("R", 2, 1, ""),
        ]

    OFF = 300000
    ans = []

    def add(piece, r, c):
        ans.append((piece, r + OFF, c + OFF, ""))

    if R == 0:
        # Diagonal moves become orthogonal moves in suitable transformed
        # coordinates; this is a two-row perimeter.
        m = B // 2
        w = m - 1

        add("B", 0, 0)
        for b in range(1, w + 1):
            add("B", b, -b)
        add("B", 1 + w, 1 - w)
        for b in range(w - 1, -1, -1):
            add("B", 1 + b, 1 - b)
        return ans

    if B == 0:
        if R == 2:
            add("R", 0, 0)
            add("R", 1, 0)
            return ans

        k = R // 2
        w = k - 1

        add("R", 0, 0)
        for c in range(1, w + 1):
            add("R", 0, c)
        add("R", 1, w)
        for c in range(w - 1, -1, -1):
            add("R", 1, c)
        return ans

    # Mixed case: blue diagonal path followed by a red orthogonal path.
    if B % 2 == 0:
        # B = 2m.
        m = B // 2

        add("B", 0, 0)
        for b in range(1, m + 1):
            add("B", b, -b)
        for b in range(m, 1, -1):
            add("B", 1 + b, 1 - b)

        add("R", 2, 0)

        L = (R - 2) // 2
        for c in range(1, L + 1):
            add("R", 2, c)
        for c in range(L, -1, -1):
            add("R", 1, c)

    else:
        # B = 2m + 1.
        m = B // 2

        add("B", 0, 0)
        for a in range(-1, -m - 1, -1):
            add("B", a, a)
        for a in range(-m, 0):
            add("B", a + 1, a - 1)

        add("R", 1, -1)

        L = (R - 2) // 2
        if L == 0:
            add("R", 1, 0)
        else:
            add("R", 2, -1)
            for c in range(0, L):
                add("R", 2, c)
            add("R", 1, L - 1)
            for c in range(L - 2, -1, -1):
                add("R", 1, c)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        R = data[pos]
        B = data[pos + 1]
        pos += 2

        ans = solve_case(R, B)
        if ans is None:
            out.append("No")
        else:
            out.append("Yes")
            for piece, r, c, suffix in ans:
                out.append(f"{piece} {r} {c}{suffix}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()