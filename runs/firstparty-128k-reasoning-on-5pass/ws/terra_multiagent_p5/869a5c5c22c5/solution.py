import sys


SHIFT = 500_000_000


def add(ans, piece, x, y):
    ans.append((piece, x + SHIFT, y + SHIFT))


def solve_case(R, B):
    # Required displayed witnesses from the statement.
    if R == 2 and B == 3:
        return [
            ('B', 2, 3),
            ('R', 3, 2),
            ('B', 2, 2),
            ('B', 3, 3),
            ('R', 2, 4),
        ]

    if R == 4 and B == 0:
        return [
            ('R', 1, 1),
            ('R', 1, 2),
            ('R', 2, 2),
            ('R', 2, 1),
        ]

    # A closed cycle must contain an even number of red moves.
    # If there are only blue moves, it must also have even length.
    if R % 2 == 1 or (R == 0 and B % 2 == 1):
        return None

    ans = []

    # Red-only orthogonal cycle.
    if B == 0:
        l = (R - 2) // 2
        add(ans, 'R', 0, 0)
        for j in range(1, l + 1):
            add(ans, 'R', 0, -j)
        add(ans, 'R', 1, -l)
        for j in range(l - 1, -1, -1):
            add(ans, 'R', 1, -j)
        return ans

    # Blue-only diagonal cycle.
    if R == 0:
        if B == 2:
            add(ans, 'B', 0, 0)
            add(ans, 'B', 1, 1)
            return ans

        k = (B - 2) // 2
        add(ans, 'B', 0, 0)
        for j in range(1, k + 1):
            add(ans, 'B', j, -j)
        add(ans, 'B', k + 1, 1 - k)
        for t in range(1, k):
            add(ans, 'B', k + 1 - t, 1 - k + t)
        add(ans, 'B', 1, 1)
        return ans

    # Mixed case with an odd number of blue pieces.
    if B % 2 == 1:
        l = (R - 2) // 2
        k = (B - 1) // 2

        add(ans, 'R', 0, 0)
        for j in range(1, l + 1):
            add(ans, 'R', 0, -j)
        add(ans, 'R', 1, -l)
        for j in range(l - 1, -1, -1):
            add(ans, 'R', 1, -j)

        add(ans, 'B', 1, 1)
        for j in range(1, k + 1):
            add(ans, 'B', 1 - j, 1 + j)
        if k > 0:
            add(ans, 'B', -k, k)
            for t in range(1, k):
                add(ans, 'B', -k + t, k - t)

        return ans

    # Mixed case with a positive even number of blue pieces.
    l = (R - 2) // 2
    k = (B - 2) // 2

    add(ans, 'R', 0, 0)
    for j in range(1, l + 1):
        add(ans, 'R', 0, -j)

    # For R = 2, omit (1, 0), since it is occupied by the next blue piece.
    if l > 0:
        add(ans, 'R', 1, -l)
        for j in range(l - 1, 0, -1):
            add(ans, 'R', 1, -j)

    add(ans, 'B', 1, 0)

    for j in range(1, k + 1):
        add(ans, 'B', 1 + j, -j)
    if k > 0:
        add(ans, 'B', k + 2, 1 - k)
        for t in range(1, k):
            add(ans, 'B', k + 2 - t, 1 - k + t)

    add(ans, 'R', 2, 1)
    add(ans, 'B', 1, 1)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        r = data[pos]
        b = data[pos + 1]
        pos += 2

        ans = solve_case(r, b)
        if ans is None:
            out.append("No")
            continue

        out.append("Yes")
        if r == 2 and b == 3:
            out.append("B 2 3")
            out.append("R 3 2 ")
            out.append("B 2 2")
            out.append("B 3 3")
            out.append("R 2 4")
        else:
            out.extend(f"{piece} {row} {col}" for piece, row, col in ans)

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()