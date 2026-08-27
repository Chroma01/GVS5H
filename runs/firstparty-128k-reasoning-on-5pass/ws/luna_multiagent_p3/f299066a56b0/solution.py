import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    def feasible(k):
        for i in range(k):
            if 2 * a[i] > a[n - k + i]:
                return False
        return True

    low = 0
    high = n // 2 + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    solve()