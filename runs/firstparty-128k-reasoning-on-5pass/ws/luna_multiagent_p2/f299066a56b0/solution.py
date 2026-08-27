import sys


def solve() -> None:
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    i = 0
    j = (n + 1) // 2
    pairs = 0
    limit = n // 2

    while i < limit and j < n:
        if 2 * a[i] <= a[j]:
            pairs += 1
            i += 1
            j += 1
        else:
            j += 1

    print(pairs)


if __name__ == "__main__":
    solve()