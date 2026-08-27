import sys


def build_cycle(R, B):
    edges = []

    if R == 0:
        # Blue-only cycles require an even number of pieces.
        if B == 2:
            edges = [
                ("B", 0, 0),
                ("B", 1, 1),
            ]
        else:
            half = B // 2
            edges.extend([("B", 1, 1)] * (half - 1))
            edges.append(("B", 1, -1))
            edges.extend([("B", -1, -1)] * (half - 1))
            edges.append(("B", -1, 1))

    elif B == 0:
        if R == 2:
            edges = [
                ("R", 0, 0),
                ("R", 0, 1),
            ]
        else:
            half = R // 2
            edges.extend([("R", 0, 1)] * (half - 1))
            edges.append(("R", 1, 0))
            edges.extend([("R", 0, -1)] * (half - 1))
            edges.append(("R", -1, 0))

    elif B % 2 == 0:
        # East^a, southeast^b, west^a, northwest^b.
        a = R // 2
        b = B // 2

        edges.extend([("R", 0, 1)] * a)
        edges.extend([("B", 1, 1)] * b)
        edges.extend([("R", 0, -1)] * a)
        edges.extend([("B", -1, -1)] * b)

    else:
        # R = 2a, B = 2l + 1.
        # Red path: east^a, north, west^(a-1).
        # Blue path: northwest^l, southwest, southeast^l.
        a = R // 2
        l = (B - 1) // 2

        edges.extend([("R", 0, 1)] * a)
        edges.append(("R", -1, 0))
        edges.extend([("R", 0, -1)] * (a - 1))

        edges.extend([("B", -1, -1)] * l)
        edges.append(("B", 1, -1))
        edges.extend([("B", 1, 1)] * l)

    shift = R + B + 10
    row = shift
    col = shift
    placement = []

    for piece, dr, dc in edges:
        placement.append((piece, row, col))
        row += dr
        col += dc

    return placement


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    index = 1
    output = []

    for _ in range(t):
        R = data[index]
        B = data[index + 1]
        index += 2

        # A red move changes checkerboard color, while a blue move does not.
        # Hence the number of red pieces in a cycle must be even.
        # If there are no red pieces, the diagonal graph is bipartite as well,
        # so the number of blue pieces must also be even.
        possible = (R % 2 == 0) and (R != 0 or B % 2 == 0)

        if not possible:
            output.append("No")
            continue

        placement = build_cycle(R, B)

        output.append("Yes")
        for piece, row, col in placement:
            output.append(f"{piece} {row} {col}")

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()