import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    cells = []
    idx = 2
    for _ in range(m):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3
        cells.append((x, y, c))

    # Process rows from bottom to top.
    # In the same row, process black cells before white cells.
    cells.sort(key=lambda t: (-t[0], 0 if t[2] == b'B' else 1))

    max_black_col = 0

    for _, y, c in cells:
        if c == b'B':
            if y > max_black_col:
                max_black_col = y
        else:
            if y <= max_black_col:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    solve()