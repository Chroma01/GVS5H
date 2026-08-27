import sys

def main():
    input = sys.stdin.buffer.readline
    first = input().split()
    if not first:
        return

    N = int(first[0])
    M = int(first[1])

    # For each constrained row x, store (L, U):
    # L = maximum column index of a fixed black cell in this row
    # U = minimum (column index - 1) of a fixed white cell in this row
    bounds = {}

    for _ in range(M):
        x_s, y_s, c = input().split()
        x = int(x_s)
        y = int(y_s)

        if c == b'B':
            cur = bounds.get(x)
            if cur is None:
                bounds[x] = (y, N)
            elif y > cur[0]:
                bounds[x] = (y, cur[1])
        else:
            u = y - 1
            cur = bounds.get(x)
            if cur is None:
                bounds[x] = (0, u)
            elif u < cur[1]:
                bounds[x] = (cur[0], u)

    # Check from bottom to top.
    # max_l is the maximum lower bound among rows at or below the current row.
    max_l = 0
    for x in sorted(bounds, reverse=True):
        l, u = bounds[x]
        if l > max_l:
            max_l = l
        if max_l > u:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    main()