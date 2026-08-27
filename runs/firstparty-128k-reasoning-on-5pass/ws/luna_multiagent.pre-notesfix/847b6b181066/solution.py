import sys


def solve():
    input = sys.stdin.readline

    N, R, C = map(int, input().split())
    S = input().strip()

    row = 0
    col = 0
    visited = {(0, 0)}
    answer = []

    for ch in S:
        if ch == "N":
            row -= 1
        elif ch == "S":
            row += 1
        elif ch == "W":
            col -= 1
        else:  # E
            col += 1

        visited.add((row, col))
        answer.append("1" if (row - R, col - C) in visited else "0")

    print("".join(answer))


if __name__ == "__main__":
    solve()