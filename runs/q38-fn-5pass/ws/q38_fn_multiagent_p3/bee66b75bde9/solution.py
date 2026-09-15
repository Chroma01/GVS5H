import sys

def solve():
    input = sys.stdin.buffer.readline
    first = input().split()
    if not first:
        return

    _n = int(first[0])
    m = int(first[1])

    cells = []
    for _ in range(m):
        x_b, y_b, c = input().split()
        x = int(x_b)
        y = int(y_b)
        order = 0 if c == b'W' else 1
        cells.append((x, order, y))

    cells.sort()

    min_white = 10**30
    for _, order, y in cells:
        if order == 0:
            if y < min_white:
                min_white = y
        else:
            if min_white <= y:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    solve()