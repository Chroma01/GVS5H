import sys


def solve() -> None:
    input = sys.stdin.readline

    n, x = map(int, input().split())
    u = [0] * n
    d = [0] * n

    total = 0
    upper_h = 10**30

    for i in range(n):
        u[i], d[i] = map(int, input().split())
        total += u[i] + d[i]
        upper_h = min(upper_h, u[i] + d[i])

    def feasible(h: int) -> bool:
        low = max(0, h - d[0])
        high = min(u[0], h)

        if low > high:
            return False

        for i in range(1, n):
            allowed_low = max(0, h - d[i])
            allowed_high = min(u[i], h)

            low = max(allowed_low, low - x)
            high = min(allowed_high, high + x)

            if low > high:
                return False

        return True

    lo, hi = 0, upper_h
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    answer = total - n * lo
    print(answer)


if __name__ == "__main__":
    solve()