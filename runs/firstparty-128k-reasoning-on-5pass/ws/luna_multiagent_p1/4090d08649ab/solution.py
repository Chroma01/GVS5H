import sys


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    last = [0] * (n + 2)

    def contribution(x):
        return max(last[x] - last[x - 1], 0)

    current = 0
    answer = 0

    for pos, v in enumerate(a, 1):
        current -= contribution(v)
        current -= contribution(v + 1)

        last[v] = pos

        current += contribution(v)
        current += contribution(v + 1)

        answer += current

    print(answer)


if __name__ == "__main__":
    solve()