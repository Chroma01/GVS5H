import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    blacks = []
    whites = []

    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'B':
            blacks.append((x, y))
        else:
            whites.append((x, y))

    # Sort by row descending. For each prefix, store the maximum column
    # among black cells whose row is at least that prefix's row.
    blacks.sort(reverse=True)
    neg_rows = []
    prefix_max_col = []

    current_max = -1
    for x, y in blacks:
        neg_rows.append(-x)
        if y > current_max:
            current_max = y
        prefix_max_col.append(current_max)

    for xw, yw in whites:
        # Number of black cells with xb >= xw:
        # -xb <= -xw, so use bisect_right on ascending neg_rows.
        count = bisect_right(neg_rows, -xw)
        if count > 0 and prefix_max_col[count - 1] >= yw:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()