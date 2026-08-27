import sys


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    last = [0] * (n + 2)
    current_sum = 0
    answer = 0

    for r, p in enumerate(a, 1):
        current_sum -= max(0, last[p] - last[p - 1])
        if p < n:
            current_sum -= max(0, last[p + 1] - last[p])

        last[p] = r

        current_sum += max(0, last[p] - last[p - 1])
        if p < n:
            current_sum += max(0, last[p + 1] - last[p])

        answer += current_sum

    print(answer)


if __name__ == "__main__":
    solve()