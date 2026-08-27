import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    def feasible(k):
        if k == 0:
            return True

        bottom_start = n - k
        j = bottom_start

        for i in range(k):
            top = a[i]
            while j < n and 2 * top > a[j]:
                j += 1
            if j == n:
                return False
            j += 1

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