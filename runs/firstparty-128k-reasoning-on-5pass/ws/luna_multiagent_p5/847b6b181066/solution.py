import sys


def solve() -> None:
    input = sys.stdin.readline

    n, r, c = map(int, input().split())
    s = input().strip()

    dr = 0
    dc = 0
    seen = {(0, 0)}
    answer = []

    for ch in s:
        if ch == "N":
            dr -= 1
        elif ch == "S":
            dr += 1
        elif ch == "W":
            dc -= 1
        else:  # E
            dc += 1

        answer.append("1" if (dr - r, dc - c) in seen else "0")
        seen.add((dr, dc))

    print("".join(answer))


if __name__ == "__main__":
    solve()