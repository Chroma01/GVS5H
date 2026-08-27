import sys


def solve() -> None:
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

    def feasible(h: int) -> bool:
        left = 0
        right = 0

        for i in range(n):
            low = max(0, h - d[i])
            high = min(u[i], h)

            if i > 0:
                low = max(low, left - x)
                high = min(high, right + x)

            if low > high:
                return False

            left, right = low, high

        return True

    low = 0
    high = upper_bound + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    answer = total - n * low
    print(answer)


if __name__ == "__main__":
    solve()