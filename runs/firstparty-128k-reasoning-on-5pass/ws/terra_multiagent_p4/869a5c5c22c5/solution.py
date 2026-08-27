import sys

SHIFT = 500_000_000


def construct(R, B):
    # A red move flips checkerboard parity, so R must be even.
    # If R = 0, every move is diagonal and flips row parity, so B must be even.
    if R % 2 == 1 or (R == 0 and B % 2 == 1):
        return None

    ans = []

    def add(color, r, c):
        ans.append((color, r + SHIFT, c + SHIFT))

    if R == 0:
        # B is positive and even.
        # In transformed coordinates (u, v), map:
        # (row, col) = (u + v, u - v).
        # A unit horizontal/vertical transformed edge is a blue diagonal move.
        if B == 2:
            add("B", 0, 0)
            add("B", 1, 1)
        else:
            k = B // 2
            w = k - 1
            vertices = [(0, 0), (1, 0)]

            for v in range(1, w + 1):
                vertices.append((1, v))

            vertices.append((0, w))

            for v in range(w - 1, 0, -1):
                vertices.append((0, v))

            for u, v in vertices:
                add("B", u + v, u - v)

    elif B == 0:
        # Orthogonal rectangle perimeter with exactly R vertices.
        m = (R - 2) // 2
        add("R", 0, 0)

        for t in range(1, m + 1):
            add("R", -t, 0)

        for t in range(m, 0, -1):
            add("R", -t, 1)

        add("R", 0, 1)

    elif B % 2 == 1:
        # R = 2 + 2m, B = 2k + 1.
        m = (R - 2) // 2
        k = (B - 1) // 2

        # Red path ending at (0, 1).
        add("R", 0, 0)

        for t in range(1, m + 1):
            add("R", -t, 0)

        for t in range(m, 0, -1):
            add("R", -t, 1)

        add("R", 0, 1)

        # The preceding red moves vertically to this first blue vertex.
        add("B", 1, 1)

        # Blue path ends at (1, -1), diagonally adjacent to (0, 0).
        for v in range(1, k + 1):
            add("B", 1 + v, 1 - v)

        if k > 0:
            add("B", k, -k)

            for v in range(k - 1, 0, -1):
                add("B", v, -v)

    else:
        # R = 2 + 2m, B = 2k.
        m = (R - 2) // 2
        k = B // 2

        # First R-1 red vertices.
        add("R", 0, 0)

        for t in range(1, m + 1):
            add("R", -t, 0)

        for t in range(m, 0, -1):
            add("R", -t, 1)

        if B == 2:
            add("B", 0, 1)
            add("R", 1, 2)
            add("B", 1, 1)
        else:
            a = k - 1

            add("B", 0, 1)

            for v in range(1, a + 1):
                add("B", v, 1 - v)

            add("B", a + 1, 2 - a)

            for v in range(a - 1, 0, -1):
                add("B", 1 + v, 2 - v)

            add("R", 1, 2)
            add("B", 1, 1)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    T = data[0]
    pos = 1
    output = []

    for _ in range(T):
        R = data[pos]
        B = data[pos + 1]
        pos += 2

        ans = construct(R, B)
        if ans is None:
            output.append("No")
        else:
            output.append("Yes")
            output.extend(f"{color} {r} {c}" for color, r, c in ans)

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()