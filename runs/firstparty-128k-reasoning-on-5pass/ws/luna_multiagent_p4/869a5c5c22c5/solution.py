import sys

SHIFT = 500_000_000


def red_rectangle_cycle(n):
    if n == 2:
        return [(0, 0), (1, 0)]

    a = 1
    b = n // 2 - 1
    points = []
    x = y = 0

    for _ in range(a):
        points.append((x, y))
        x += 1
    for _ in range(b):
        points.append((x, y))
        y += 1
    for _ in range(a):
        points.append((x, y))
        x -= 1
    for _ in range(b):
        points.append((x, y))
        y -= 1

    return points


def blue_rectangle_cycle(n):
    return [(x + y, x - y) for x, y in red_rectangle_cycle(n)]


def mixed_cycle(red_count, blue_count):
    if blue_count & 1:
        k = (blue_count - 1) // 2

        grid_path = [(0, 0)]
        for j in range(1, k + 1):
            grid_path.append((0, -j))
        grid_path.append((1, -k))
        for y in range(-k + 1, 1):
            grid_path.append((1, y))

        start = (0, 0)
        finish = (1, 1)
    else:
        k = (blue_count - 2) // 2

        grid_path = [(0, 0)]
        for j in range(1, k + 1):
            grid_path.append((0, -j))
        grid_path.append((1, -k))
        for y in range(-k + 1, 2):
            grid_path.append((1, y))

        start = (0, 0)
        finish = (2, 0)

    blue_path = [(x + y, x - y) for x, y in grid_path]

    m = (red_count - 2) // 2
    red_path = [finish, (1, 0)]

    if m == 0:
        red_path.append(start)
    else:
        for j in range(1, m + 1):
            red_path.append((1, -j))
        red_path.append((0, -m))
        for j in range(m - 1, -1, -1):
            red_path.append((0, -j))

    result = []

    for r, c in red_path[:-1]:
        result.append(("R", r + SHIFT, c + SHIFT))

    for r, c in blue_path[:-1]:
        result.append(("B", r + SHIFT, c + SHIFT))

    return result


def solve_case(red_count, blue_count):
    if red_count & 1:
        return None

    if red_count == 0:
        if blue_count & 1:
            return None
        points = blue_rectangle_cycle(blue_count)
        return [("B", r + SHIFT, c + SHIFT) for r, c in points]

    if blue_count == 0:
        points = red_rectangle_cycle(red_count)
        return [("R", r + SHIFT, c + SHIFT) for r, c in points]

    return mixed_cycle(red_count, blue_count)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    index = 1
    output = []

    for _ in range(t):
        red_count = data[index]
        blue_count = data[index + 1]
        index += 2

        answer = solve_case(red_count, blue_count)

        if answer is None:
            output.append("No")
        else:
            output.append("Yes")
            output.extend(
                f"{piece} {row} {col}"
                for piece, row, col in answer
            )

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()