import sys


def solve() -> None:
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())

    cells = []
    for _ in range(m):
        x, y, c = input().split()
        cells.append((int(x), int(y), c == b"B"))

    # Sweep rows from bottom to top. For equal rows, process black cells
    # before white cells so conflicts within the same row are detected.
    cells.sort(key=lambda cell: (-cell[0], not cell[2]))

    max_black_col = 0
    for _, y, is_black in cells:
        if is_black:
            max_black_col = max(max_black_col, y)
        elif y <= max_black_col:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()