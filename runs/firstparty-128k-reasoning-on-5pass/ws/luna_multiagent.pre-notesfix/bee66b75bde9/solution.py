import sys


def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    black = []
    white = []

    for _ in range(m):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == "B":
            black.append((x, y))
        else:
            white.append((x, y))

    black.sort(reverse=True)
    white.sort(reverse=True)

    ptr = 0
    max_black_col = 0

    for wx, wy in white:
        while ptr < len(black) and black[ptr][0] >= wx:
            max_black_col = max(max_black_col, black[ptr][1])
            ptr += 1

        if max_black_col >= wy:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()