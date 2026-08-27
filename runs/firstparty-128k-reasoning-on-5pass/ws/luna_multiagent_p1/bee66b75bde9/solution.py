import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    rows = {}

    p = 2
    for _ in range(m):
        x = int(data[p])
        y = int(data[p + 1])
        c = data[p + 2]
        p += 3

        if x not in rows:
            rows[x] = [0, n]  # [lower bound, upper bound]

        if c == b'B':
            rows[x][0] = max(rows[x][0], y)
        else:
            rows[x][1] = min(rows[x][1], y - 1)

    # Greedily keep each row's black-prefix length as large as possible.
    # The lengths must be nonincreasing from top to bottom.
    current = n

    for x in sorted(rows):
        lower, upper = rows[x]

        if lower > upper:
            print("No")
            return

        current = min(current, upper)
        if current < lower:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()