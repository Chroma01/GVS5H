import sys


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    cells = []
    for _ in range(m):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        # Whites must be processed before blacks in the same row.
        cells.append((x, 0 if c == "W" else 1, y))

    cells.sort()

    min_white_col = n + 1

    for _, kind, y in cells:
        if kind == 0:
            min_white_col = min(min_white_col, y)
        else:
            if y >= min_white_col:
                print("No")
                return

    print("Yes")


if __name__ == "__main__":
    solve()