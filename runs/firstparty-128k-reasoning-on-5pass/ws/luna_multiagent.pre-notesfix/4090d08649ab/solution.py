import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    last = [0] * (n + 2)

    def term(v):
        return max(0, last[v] - last[v - 1])

    current = 0
    answer = 0

    for i, x in enumerate(a, 1):
        current -= term(x)
        if x + 1 <= n:
            current -= term(x + 1)

        last[x] = i

        current += term(x)
        if x + 1 <= n:
            current += term(x + 1)

        answer += current

    print(answer)


if __name__ == "__main__":
    solve()