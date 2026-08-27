import sys


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    adjusted = [i - j for j, i in enumerate(i for i, ch in enumerate(s) if ch == "1")]
    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(x - median) for x in adjusted)

    print(answer)


if __name__ == "__main__":
    solve()