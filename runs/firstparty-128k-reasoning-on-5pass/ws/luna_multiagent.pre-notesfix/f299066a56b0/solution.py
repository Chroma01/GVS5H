import sys


def solve() -> None:
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    top_count = n // 2
    i = 0
    j = top_count
    pairs = 0

    while i < top_count and j < n:
        if 2 * a[i] <= a[j]:
            pairs += 1
            i += 1
            j += 1
        else:
            j += 1

    print(pairs)


if __name__ == "__main__":
    solve()