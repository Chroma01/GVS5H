import sys
import bisect


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    blacks = []
    whites = []

    for _ in range(m):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if c == b'B':
            blacks.append((x, y))
        else:
            whites.append((x, y))

    blacks.sort()
    xs = [p[0] for p in blacks]

    k = len(blacks)
    suffix_max_y = [0] * (k + 1)
    for i in range(k - 1, -1, -1):
        suffix_max_y[i] = max(suffix_max_y[i + 1], blacks[i][1])

    for wx, wy in whites:
        idx = bisect.bisect_left(xs, wx)
        if idx < k and suffix_max_y[idx] >= wy:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    main()