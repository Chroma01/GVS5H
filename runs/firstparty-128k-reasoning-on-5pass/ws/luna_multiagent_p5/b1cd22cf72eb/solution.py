import sys


def solve():
    input = sys.stdin.readline
    n, x = map(int, input().split())

    u = [0] * n
    d = [0] * n
    total = 0
    upper_bound = 10**30

    for i in range(n):
        u[i], d[i] = map(int, input().split())
        total += u[i] + d[i]
        upper_bound = min(upper_bound, u[i] + d[i])

    def feasible(h):
        left = right = None

        for i in range(n):
            lo = max(0, h - d[i])
            hi = min(u[i], h)

            if lo > hi:
                return False

            if i == 0:
                left, right = lo, hi
            else:
                left = max(lo, left - x)
                right = min(hi, right + x)
                if left > right:
                    return False

        return True

    low, high = 0, upper_bound + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(total - n * low)


if __name__ == "__main__":
    solve()