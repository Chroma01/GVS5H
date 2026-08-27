import sys


def solve():
    input = sys.stdin.readline

    N, R, C = map(int, input().split())
    S = input().strip()

    row = 0
    col = 0
    visited = {(0, 0)}
    answer = []

    moves = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }

    for ch in S:
        dr, dc = moves[ch]
        row += dr
        col += dc

        source = (row - R, col - C)
        answer.append("1" if source in visited else "0")

        visited.add((row, col))

    print("".join(answer))


if __name__ == "__main__":
    solve()