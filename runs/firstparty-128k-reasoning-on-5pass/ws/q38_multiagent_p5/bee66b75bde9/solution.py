import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    m = int(data[1])
    cells = []
    append = cells.append
    idx = 2

    for _ in range(m):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3

        # Sort by x descending. For the same x, process B before W.
        # order = 0 for B, 1 for W.
        append((-x, 0 if c == b'B' else 1, y))

    del data
    cells.sort()

    max_black_col = 0

    for _, is_white, y in cells:
        if is_white:
            if max_black_col >= y:
                sys.stdout.write("No\n")
                return
        else:
            if y > max_black_col:
                max_black_col = y

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    main()