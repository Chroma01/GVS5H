import sys


def solve():
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    groups = [[], []]

    for i in range(1, n):
        gap = x[i] - x[i - 1]
        weight = n - i
        groups[i & 1].append((gap, weight))

    answer = n * x[0]

    for group in groups:
        gaps = sorted(gap for gap, _ in group)
        weights = sorted((weight for _, weight in group), reverse=True)
        answer += sum(gap * weight for gap, weight in zip(gaps, weights))

    print(answer)


if __name__ == "__main__":
    solve()