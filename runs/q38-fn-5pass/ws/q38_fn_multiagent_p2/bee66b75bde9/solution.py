import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # N is not needed for the dominance check, but parse it to consume input.
    n = int(data[0])
    m = int(data[1])

    cells = []
    idx = 2
    for _ in range(m):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3

        # White cells must be processed before black cells in the same row.
        kind = 0 if c == b'W' else 1
        cells.append((x, kind, y))

    cells.sort()

    INF = 10**18
    min_white_col = INF

    for _, kind, y in cells:
        if kind == 0:  # white
            if y < min_white_col:
                min_white_col = y
        else:  # black
            # A previous/same-row white cell with column <= y is northwest of this black cell.
            if y >= min_white_col:
                sys.stdout.write("No\n")
                return

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    solve()