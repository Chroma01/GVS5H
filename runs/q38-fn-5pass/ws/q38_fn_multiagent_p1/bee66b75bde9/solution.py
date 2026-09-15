import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    cells = []
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        # Process white cells before black cells in the same row.
        cells.append((x, 0 if c == b'W' else 1, y))

    cells.sort()

    min_white_col = 10**30

    for _, kind, y in cells:
        if kind == 0:  # white
            if y < min_white_col:
                min_white_col = y
        else:  # black
            if y >= min_white_col:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    solve()