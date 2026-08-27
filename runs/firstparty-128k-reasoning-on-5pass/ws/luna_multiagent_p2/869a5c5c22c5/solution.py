import sys


def build_cycle(vectors):
    r = c = 0
    points = []
    labels = []

    for kind, dr, dc in vectors:
        points.append((r, c))
        labels.append(kind)
        r += dr
        c += dc

    min_r = min(r for r, _ in points)
    min_c = min(c for _, c in points)
    shift_r = 1 - min_r
    shift_c = 1 - min_c

    return [
        (kind, r + shift_r, c + shift_c)
        for kind, (r, c) in zip(labels, points)
    ]


def solve_case(red, blue):
    # Every red move changes checkerboard parity, while every blue
    # move preserves it. Hence the number of red pieces must be even.
    if red % 2 == 1:
        return None

    if red == 0:
        # A blue cycle also needs an even number of blue moves.
        if blue % 2 == 1:
            return None

        side = blue // 2 - 1
        vectors = (
            [("B", 1, 1)]
            + [("B", 1, -1)] * side
            + [("B", -1, -1)]
            + [("B", -1, 1)] * side
        )
        return build_cycle(vectors)

    if blue == 0:
        side = red // 2 - 1
        vectors = (
            [("R", 1, 0)]
            + [("R", 0, 1)] * side
            + [("R", -1, 0)]
            + [("R", 0, -1)] * side
        )
        return build_cycle(vectors)

    # The first R-1 red moves form a detour from (0,0) to (0,1).
    d = (red - 2) // 2
    vectors = (
        [("R", -1, 0)] * d
        + [("R", 0, 1)]
        + [("R", 1, 0)] * d
    )

    if blue % 2 == 0:
        q = blue // 2
        vectors += (
            [("B", 1, 1)] * (q - 1)
            + [("B", 1, -1)]
            + [("B", -1, -1)] * q
            + [("R", 0, 1)]
        )
    else:
        q = blue // 2
        vectors += (
            [("B", 1, 1)] * q
            + [("B", 1, -1)]
            + [("B", -1, -1)] * q
            + [("R", -1, 0)]
        )

    return build_cycle(vectors)


def main():
    input = sys.stdin.readline
    t = int(input())
    output = []

    for _ in range(t):
        red, blue = map(int, input().split())
        result = solve_case(red, blue)

        if result is None:
            output.append("No")
        else:
            output.append("Yes")
            output.extend(
                f"{kind} {row} {col}"
                for kind, row, col in result
            )

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()