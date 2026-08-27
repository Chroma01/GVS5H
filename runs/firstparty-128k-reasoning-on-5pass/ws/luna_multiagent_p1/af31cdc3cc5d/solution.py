import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = sorted(data[1:])

    k = n // 2
    answer = sum(a[n - k:]) - sum(a[:k])
    print(answer)


if __name__ == "__main__":
    solve()