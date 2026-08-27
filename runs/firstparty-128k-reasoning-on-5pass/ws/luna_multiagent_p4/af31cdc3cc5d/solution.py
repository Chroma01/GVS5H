import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = sorted(data[1:])

    m = n // 2
    if n % 2 == 0:
        answer = sum(a[m:]) - sum(a[:m])
    else:
        answer = sum(a[m + 1:]) - sum(a[:m])

    print(answer)


if __name__ == "__main__":
    solve()