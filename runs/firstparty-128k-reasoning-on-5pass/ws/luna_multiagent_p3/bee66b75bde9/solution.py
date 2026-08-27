import sys


def solve() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())

    # For each constrained row x:
    #   lower[x] = maximum y among black cells in row x
    #   upper[x] = minimum y - 1 among white cells in row x
    # Thus the row threshold must lie in [lower[x], upper[x]].
    rows = {}

    for _ in range(m):
        x, y, c = input().split()
        x = int(x)
        y = int(y)

        if x not in rows:
            rows[x] = [0, n]

        if c == "B":
            rows[x][0] = max(rows[x][0], y)
        else:
            rows[x][1] = min(rows[x][1], y - 1)

    # Row thresholds must be nonincreasing from top to bottom.
    # Greedily keep each threshold as large as possible, since that
    # leaves the most freedom for later rows.
    previous = n

    for x in sorted(rows):
        lower, upper = rows[x]
        current = min(previous, upper)

        if current < lower:
            print("No")
            return

        previous = current

    print("Yes")


if __name__ == "__main__":
    solve()