import sys


def solve():
    input = sys.stdin.buffer.readline
    n, x = map(int, input().split())

    u = [0] * n
    d = [0] * n
    total = 0
    upper_h = 10**30

    for i in range(n):
        u[i], d[i] = map(int, input().split())
        total += u[i] + d[i]
        upper_h = min(upper_h, u[i] + d[i])

    def feasible(h):
        lo = max(0, h - d[0])
        hi = min(u[0], h)
        if lo > hi:
            return False

        for i in range(1, n):
            left = max(0, h - d[i])
            right = min(u[i], h)

            lo = max(left, lo - x)
            hi = min(right, hi + x)

            if lo > hi:
                return False

        return True

    low, high = 0, upper_h
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(total - n * low)


if __name__ == "__main__":
    solve()