import sys


def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    whites = []
    blacks = []

    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'W':
            whites.append((x, y))
        else:
            blacks.append((x, y))

    whites.sort()
    blacks.sort()

    p = 0
    min_white_y = 10**30

    for bx, by in blacks:
        while p < len(whites) and whites[p][0] <= bx:
            min_white_y = min(min_white_y, whites[p][1])
            p += 1

        if min_white_y <= by:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()