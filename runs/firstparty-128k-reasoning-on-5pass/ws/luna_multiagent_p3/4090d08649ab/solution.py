import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    last = [0] * (n + 2)

    def contribution(x: int) -> int:
        return max(0, last[x] - last[x - 1])

    cur = 0
    answer = 0

    for r, v in enumerate(a, 1):
        cur -= contribution(v)
        cur -= contribution(v + 1)

        last[v] = r

        cur += contribution(v)
        cur += contribution(v + 1)

        answer += cur

    print(answer)


if __name__ == "__main__":
    solve()