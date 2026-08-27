import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    def feasible(k):
        start = n - k
        for i in range(k):
            if 2 * a[i] > a[start + i]:
                return False
        return True

    low, high = 0, n // 2
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(low)


if __name__ == "__main__":
    solve()