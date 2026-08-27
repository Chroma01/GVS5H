import sys
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # A valid coloring is a "staircase": black cells form an order ideal of the
    # product poset, i.e. if (r,c) is black then every (r',c') with r'<=r, c'<=c
    # is black. Equivalently, there is NO pair consisting of a white cell (r1,c1)
    # and a black cell (r2,c2) with r2 >= r1 and c2 >= c1.
    # (Sufficiency: with f(r) = max black column over rows >= r, f is
    #  non-increasing and respects all fixed cells iff no such pair exists.)
    #
    # So we only need to check: does some fixed white cell have a fixed black
    # cell weakly to its southeast (same/larger row, same/larger column)?
    # Sweep rows from bottom to top, keeping the maximum black column seen in
    # rows >= current row. Within a row, add blacks before querying whites so
    # that same-row blacks (r2 == r1) are included.

    rows = defaultdict(lambda: [[], []])  # row -> [black cols, white cols]
    for _ in range(M):
        x = int(next(it)); y = int(next(it)); c = next(it)
        if c == b'B':
            rows[x][0].append(y)
        else:
            rows[x][1].append(y)

    max_black = 0  # max column of black cells in rows >= current row
    for r in sorted(rows.keys(), reverse=True):
        blacks, whites = rows[r]
        for y in blacks:
            if y > max_black:
                max_black = y
        for y in whites:
            if max_black >= y:
                sys.stdout.write("No\n")
                return

    sys.stdout.write("Yes\n")

main()