import sys


def solve():
    input = sys.stdin.readline
    n, r, c = map(int, input().split())
    s = input().strip()

    x = 0
    y = 0
    seen = {(0, 0)}
    answer = []

    for ch in s:
        if ch == "N":
            x -= 1
        elif ch == "S":
            x += 1
        elif ch == "W":
            y -= 1
        else:  # E
            y += 1

        answer.append("1" if (x - r, y - c) in seen else "0")
        seen.add((x, y))

    print("".join(answer))


if __name__ == "__main__":
    solve()