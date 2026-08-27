import sys


def solve() -> None:
    input = sys.stdin.readline
    N, R, C = map(int, input().split())
    S = input().strip()

    dr = {"N": -1, "S": 1, "W": 0, "E": 0}
    dc = {"N": 0, "S": 0, "W": -1, "E": 1}

    r = c = 0
    seen = {(0, 0)}
    answer = []

    for ch in S:
        r += dr[ch]
        c += dc[ch]

        answer.append("1" if (r - R, c - C) in seen else "0")
        seen.add((r, c))

    print("".join(answer))


if __name__ == "__main__":
    solve()