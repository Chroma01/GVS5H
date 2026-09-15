import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # N is not needed directly, but read it to consume input correctly.
    # data[0] = N, data[1] = S as bytes
    s = data[1]

    # Collect 0-based positions of all '1' characters.
    pos = []
    for i, ch in enumerate(s):
        if ch == 49:  # ord('1')
            pos.append(i)

    k = len(pos)

    # For the j-th one (0-based), if the final block starts at x,
    # its target position is x + j.
    # Cost = sum |pos[j] - (x + j)| = sum |(pos[j] - j) - x|.
    # Minimized when x is the median of a[j] = pos[j] - j.
    median = pos[k // 2] - (k // 2)

    ans = 0
    for j, p in enumerate(pos):
        ans += abs((p - j) - median)

    print(ans)

if __name__ == "__main__":
    main()