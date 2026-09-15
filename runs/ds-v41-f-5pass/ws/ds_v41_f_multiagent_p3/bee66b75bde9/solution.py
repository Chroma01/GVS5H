import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    M = int(data[1])
    events = []
    idx = 2

    for _ in range(M):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3

        if c == b'B':
            events.append((x, 1, y))  # black
        else:
            events.append((x, 0, y))  # white

    # Sort by row; in the same row, process white before black.
    events.sort()

    INF = 10**18
    min_white_col = INF

    for _, typ, col in events:
        if typ == 0:
            if col < min_white_col:
                min_white_col = col
        else:
            if min_white_col <= col:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    main()