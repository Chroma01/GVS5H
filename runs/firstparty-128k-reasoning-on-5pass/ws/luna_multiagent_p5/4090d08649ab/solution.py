import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    last = [0] * (n + 2)
    total_for_right = 0
    answer = 0

    for pos, v in enumerate(a, 1):
        d = last[v] - last[v - 1]
        if d > 0:
            total_for_right -= d

        if v + 1 <= n:
            d = last[v + 1] - last[v]
            if d > 0:
                total_for_right -= d

        last[v] = pos

        d = last[v] - last[v - 1]
        if d > 0:
            total_for_right += d

        if v + 1 <= n:
            d = last[v + 1] - last[v]
            if d > 0:
                total_for_right += d

        answer += total_for_right

    print(answer)


if __name__ == "__main__":
    solve()