import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    pts = []
    for _ in range(m):
        x = int(data[idx]); y = int(data[idx + 1]); c = data[idx + 2]; idx += 3
        # type 0 = white (processed first within a row), type 1 = black
        t = 0 if c == b'W' else 1
        pts.append((x, t, y))

    pts.sort()

    min_white_col = None  # minimum column among all white cells seen so far
    for x, t, y in pts:
        if t == 0:  # white cell
            if min_white_col is None or y < min_white_col:
                min_white_col = y
        else:       # black cell
            if min_white_col is not None and min_white_col <= y:
                sys.stdout.write("No\n")
                return

    sys.stdout.write("Yes\n")

main()