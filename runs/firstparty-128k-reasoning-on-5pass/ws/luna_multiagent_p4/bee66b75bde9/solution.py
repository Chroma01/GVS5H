import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    events = []
    pos = 2
    for _ in range(m):
        x = int(data[pos])
        y = int(data[pos + 1])
        c = data[pos + 2]
        pos += 3

        # Whites must be processed before blacks at the same row.
        if c == b"W":
            events.append((x, 0, y))
        else:
            events.append((x, 1, y))

    events.sort()

    minimum_white_column = n + 1

    for _, kind, y in events:
        if kind == 0:
            if y < minimum_white_column:
                minimum_white_column = y
        else:
            if minimum_white_column <= y:
                print("No")
                return

    print("Yes")


if __name__ == "__main__":
    solve()