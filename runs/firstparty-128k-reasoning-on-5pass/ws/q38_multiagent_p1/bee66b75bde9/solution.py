import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    events = []
    for _ in range(m):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        # color order: black before white in the same row
        events.append((-x, 0 if c == b'B' else 1, y))

    events.sort()

    max_y_black = 0
    for _, color, y in events:
        if color == 0:  # black
            if y > max_y_black:
                max_y_black = y
        else:  # white
            if y <= max_y_black:
                sys.stdout.write("No\n")
                return

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    main()