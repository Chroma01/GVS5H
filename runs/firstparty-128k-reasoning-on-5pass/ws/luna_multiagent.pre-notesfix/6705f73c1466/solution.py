import sys


def solve() -> None:
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    adjusted = []
    for i, ch in enumerate(s):
        if ch == "1":
            adjusted.append(i - len(adjusted))

    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(value - median) for value in adjusted)

    print(answer)


if __name__ == "__main__":
    solve()